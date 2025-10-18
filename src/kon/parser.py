from enum import Enum, auto
from typing import List, Optional, Union
import textwrap

from .types import KonObject, KonDictionary

class MultilineStringBehaviour(Enum):
    """
    Specifies how to handle multiline string values.

    Attributes:
        IGNORE: Keep the multiline string as is, with original indentation.
        DEDENT: Remove common leading whitespace from every line in the string.
        VALUE_ERROR: Raise a ValueError if a multiline string is encountered.
    """
    IGNORE = auto()
    DEDENT = auto()
    VALUE_ERROR = auto()

class KonParser:
    """
    A parser for the Kon configuration file format.
    This class takes a Kon-formatted string, bytes, or bytearray and provides
    a `parse` method to convert it into corresponding Python objects.
    The parser supports:
    - Basic types: strings (single, double, and unquoted), integers (decimal,
      hex, octal, binary), floats, booleans (`true`, `false`), and `null`.
    - Data structures: lists enclosed in `()` and dictionaries enclosed in `{}`.
    - Implicit dictionaries: A sequence of values like `key1 key2 key3 = value`
      is parsed as `{'key1': {'key2': {'key3': 'value'}}}`.
    - Multiline strings: Prefixed with `<` for dedenting or `|` for preserving
      whitespace.
    Attributes:
        source (str): The input string to be parsed.
        allow_implicit_dicts (bool): If True, allows parsing sequences of values
            as nested dictionaries.
        multiline_string_behaviour (MultilineStringBehaviour): The default
            behaviour for handling multiline strings (when not prefixed).
    """
    source: str
    allow_implicit_dicts: bool
    multiline_string_behaviour: MultilineStringBehaviour

    def __init__(self, source: Union[str, bytes, bytearray], *, multiline_string_behaviour: MultilineStringBehaviour = MultilineStringBehaviour.IGNORE, allow_implicit_dicts: bool = True) -> None:
        """
        Initializes the parser with the KON source data.

        Args:
            source: The KON data to be parsed, provided as a string,
                bytes, or bytearray. Bytes-like objects are decoded as UTF-8.
            multiline_string_behaviour: Defines how multiline
                strings are handled. Defaults to MultilineStringBehaviour.IGNORE.
            allow_implicit_dicts: If True, allows key-value pairs
                at the root level without enclosing braces. Defaults to True.

        Raises:
            TypeError: If the source is not a str, bytes, or bytearray.
            ValueError: If the source is empty or contains only whitespace.
        """
        self.allow_implicit_dicts = allow_implicit_dicts
        self.multiline_string_behaviour = multiline_string_behaviour
        if isinstance(source, str):
            self.source = source.strip()
        elif isinstance(source, (bytes, bytearray)):
            self.source = source.decode('utf-8').strip()
        else:
            raise TypeError(f'source must be of type {str}, {bytes} or {bytearray}')
        if self.source == '':
            raise ValueError('empty source not allowed')
        self.position = 0

    def _peek(self, i: int = 0):
        """Peeks from current position by `i` characters, if beyond the end, returns ''"""
        return self.source[self.position+i:self.position+i+1]

    def _parse_numeric(self) -> Union[int, float]:
        start = self.position
        if self._peek() == '0' and self._peek(1) in 'xob':
            self.position += 2
            base_char = self.source[self.position-1]
            valid_digits = ''
            if base_char == 'x':
                valid_digits = '0123456789abcdefABCDEF'
            elif base_char == 'o':
                valid_digits = '01234567'
            else: # 'b'
                valid_digits = '01'
            
            while self._peek() in valid_digits:
                self.position += 1
            num_str = self.source[start:self.position]
            return int(num_str, 0)

        while self._peek().isdigit():
            self.position += 1
        if self._peek() == ".":
            self.position += 1
            while self._peek().isdigit():
                self.position += 1
        if self._peek() in "eE":
            self.position += 1
            if self._peek() in "+-":
                self.position += 1
            while self._peek().isdigit():
                self.position += 1
        
        num_str = self.source[start : self.position]
        if "." in num_str or "e" in num_str or "E" in num_str:
            return float(num_str)
        return int(num_str)

    def _parse_str(self, *, multiline: Optional[MultilineStringBehaviour] = None) -> str:
        r"""
        Parse a quoted string. Supports single-line strings and multiline strings
        introduced with a leading '<' (dedent) or '|' (ignore). When a multiline
        marker is present the next character must be a quote (" or ').

        Supported escapes: \\, \" , \' , \n , \r , \t , \xNN , \uNNNN
        """
        # Determine whether a multiline marker is present at the current
        # position. If a marker is present we use the marker's behaviour
        # ("<" -> DEDENT, "|" -> IGNORE). If no marker is present, the
        # provided `multiline` argument is treated as the default behaviour
        # (it does not restrict marker usage). Only when the parser's global
        # default is VALUE_ERROR and `multiline` is None should encountering
        # a marker raise an error.
        mark = self._peek()
        if multiline is None:
            multiline = self.multiline_string_behaviour
        if mark in ('<', '|'):
            # consume the marker and set behaviour based on it
            self.position += 1
        is_multiline = False

        # Next char must be a quote
        q = self._peek()
        if q not in ('"', "'"):
            raise ValueError(f'expected string quote at index {self.position}, found {q!r}')
        quote = q
        self.position += 1

        chars: list[str] = []
        while True:
            ch = self._peek()
            if ch == "":
                raise ValueError('unterminated string')
            if ch == '\n':
                is_multiline = True
            # handle escapes
            if ch == "\\":
                self.position += 1
                esc = self._peek()
                if esc == "":
                    raise ValueError('unterminated escape sequence in string')
                # simple escapes
                if esc == 'n':
                    chars.append('\n')
                    self.position += 1
                elif esc == 'r':
                    chars.append('\r')
                    self.position += 1
                elif esc == 't':
                    chars.append('\t')
                    self.position += 1
                elif esc in ('\\', '"', "'"):
                    chars.append(esc)
                    self.position += 1
                elif esc == 'x':
                    # two hex digits
                    self.position += 1
                    h1 = self._peek()
                    h2 = self._peek(1)
                    if h1 == '' or h2 == '':
                        raise ValueError('incomplete \\x escape')
                    hexstr = h1 + h2
                    try:
                        chars.append(chr(int(hexstr, 16)))
                    except ValueError:
                        raise ValueError('invalid \\x escape')
                    self.position += 2
                elif esc == 'u':
                    # four hex digits
                    self.position += 1
                    hx = self.source[self.position:self.position+4]
                    if len(hx) < 4:
                        raise ValueError('incomplete \\u escape')
                    try:
                        chars.append(chr(int(hx, 16)))
                    except ValueError:
                        raise ValueError('invalid \\u escape')
                    self.position += 4
                elif esc == '\r' and self._peek(1) == '\n':
                    self.position += 2
                elif esc.isspace():
                    self.position += 1
                else:
                    # unknown escape, keep the character as-is
                    chars.append(esc)
                    self.position += 1
                continue

            # closing quote
            if ch == quote:
                self.position += 1
                break

            # normal character (including newlines in multiline strings)
            chars.append(ch)
            self.position += 1

        result = ''.join(chars)

        if is_multiline:
            # If this was a multiline literal with dedent behaviour, use
            # textwrap.dedent to remove common leading indentation and normalize.
            if multiline is MultilineStringBehaviour.DEDENT:
                # textwrap.dedent will remove common indentation; strip a leading
                # single newline which is a common writer pattern
                if result.startswith('\n'):
                    result = result[1:]
                result = textwrap.dedent(result)

            # If VALUE_ERROR is configured as the global default and the caller
            # didn't override it, raise now when the parsed string contains a
            # newline (i.e. it is multiline). This defers the decision until we
            # actually parsed the content.
            elif multiline is MultilineStringBehaviour.VALUE_ERROR:
                raise ValueError('multiline strings are not allowed')

        return result

    def _parse_list_like(self, start: str, end: str) -> List[KonObject]:
        if self._peek() != start:
            raise ValueError(f'expected "{start}" at index {self.position}, but found {self._peek() or "<END>"}')
        self.position += 1
        result = []
        while True:
            self._skip_whitespace()
            if self._peek() == end:
                self.position += 1
                break
            v = self.parse(_top_level = False)
            self._skip_whitespace(newlines=False)
            if self._peek() not in f'\n,{end}' and self._peek() != '':
                raise ValueError(f'expected a newline, "{end}" or a comma at index {self.position}, but found {self._peek() or "<END>"}')
            self.position += 1
            result.append(v)
            if self._peek(-1) == end:
                break
        return result

    def _parse_list(self) -> List[KonObject]:
        return self._parse_list_like('(', ')')
    
    def _parse_dict(self) -> KonDictionary:
        mlist = self._parse_list_like('{', '}')
        if len(mlist) == 0:
            return {}
        if all(isinstance(i, dict) for i in mlist):
            mlist.reverse()
            result = mlist.pop()
            while len(mlist) > 0:
                result.update(mlist.pop()) # type: ignore
            return result # type: ignore
        raise ValueError(f'unset key {mlist[-1]} in dictionary@({" ".join(str(i) for i in mlist[:-1])})')

    def parse(self, _top_level: bool = True, *, _until: Optional[int] = None) -> KonObject:
        """
        Parses the source string into a KonObject.

        This is the main entry point for the parser. It iteratively consumes
        the source string, identifying and parsing different data types
        (numerics, strings, identifiers, lists, dictionaries).

        It ignores line comments specified by a hash symbol (`#`).

        The parsing logic handles different contexts via the `_top_level` flag.
        When at the top level, newlines are treated as simple whitespace.
        Inside structures like lists or dictionaries (`_top_level=False`),
        newlines can act as terminators.

        A key feature is the "collapsing" of parts. The parser can handle
        implicit key-value structures like `key1 key2 = "value"`, which is
        equivalent to `{ "key1": { "key2": "value" } }`. This is achieved
        by parsing primitive values into a temporary list and then collapsing
        them with the subsequent value (e.g., an int, or str, ...).

        At the top level, if the source consists of multiple dictionaries,
        they are merged into a single dictionary.

        Args:
            _top_level (bool): A boolean indicating if the parser is at the top
                level of the source. Defaults to True.
            _until (int): An optional integer position in the source string at which
                to stop parsing. Used for nested structures. Defaults to None,
                which means parsing until the end of the source.

        Returns:
            The parsed KonObject, which can be a dictionary, list, string,
            number, or other supported type.

        Raises:
            ValueError: If the source is empty, contains unexpected characters,
                or has an invalid structure (e.g., a key without a value).
        """
        if _until is None:
            _until = len(self.source)
        parts: list[KonObject] = []
        while _until > self.position:
            self._skip_whitespace(newlines=_top_level)
            ch = self._peek()
            if ch == '+':
                self.position += 1
            elif ch == '-':
                self.position += 1
                self._skip_whitespace()
                n = self.parse(_top_level = False)
                if not isinstance(n, (int, float)):
                    raise TypeError(f'cannot negate a(n) {type(n).__name__}, only an int or float')
                parts.append(-n)
            elif ch.isdigit():
                parts.append(self._parse_numeric())
            elif ch in ('"', "'"):
                parts.append(self._parse_str())
            elif ch == '<' and self._peek(1) in ('"', "'"):
                parts.append(self._parse_str(multiline=MultilineStringBehaviour.DEDENT))
            elif ch == '|' and self._peek(1) in ('"', "'"):
                parts.append(self._parse_str(multiline=MultilineStringBehaviour.IGNORE))
            elif ch.isidentifier() or ch in "$-:":
                parts.append(self._parse_identifier_str())
            elif ch == '{':
                result = self._parse_dict()
                result = self._collapse_parts(parts, result)
                parts.append(result)
            elif ch == '(':
                result = self._parse_list()
                result = self._collapse_parts(parts, result)
                parts.append(result)
            elif ch == '=':
                self.position += 1
                result = self.parse(_top_level = False)
                result = self._collapse_parts(parts, result)
                parts.append(result)
            elif ch == '#':
                while self._peek() not in '\n':
                    self.position += 1
                self.position += 1
            else:
                if ch in '\n,)}':
                    if not _top_level:
                        break
                    else:
                        self.position += 1
                        continue
                raise ValueError(f'unexpected character: {ch!r} at index {self.position}')
            self._skip_whitespace(newlines=_top_level)

        if len(parts) == 0:
            raise ValueError('empty or otherwise invalid source')
        elif len(parts) == 1:
            return parts[0]
        if _top_level and all(isinstance(i, dict) for i in parts):
            parts.reverse()
            result = parts.pop()
            while len(parts) > 0:
                result.update(parts.pop()) # type: ignore
            return result
        # Logically everything after this is an invalid source with an unset key
        raise ValueError(f'unset key {parts[-1]} in dictionary@({" ".join(str(i) for i in parts[:-1])})')

    def _collapse_parts(self, parts: List[KonObject], result: KonObject):
        while len(parts) > 0:
            key = parts.pop()
            if key is not None and not isinstance(key, (str, int, float, bool)):
                parts.append(key)
                break
            result = {key: result}
        return result

    def _skip_whitespace(self, newlines: bool = True):
        while self._peek().isspace() and (newlines or self._peek() != '\n'):
            self.position += 1

    def _parse_identifier_str(self) -> Union[str, None, bool, float]:
        """
        Parse an identifier-like token (unquoted string). Recognize
        keywords null/true/false and otherwise return the identifier string.
        """
        start = self.position
        # identifier chars: letters, digits, underscore, and a few punctuation
        while True:
            ch = self._peek()
            if ch == '' or not (ch.isidentifier() or ch.isdigit() or ch in '_-:$'):
                break
            self.position += 1
        ident = self.source[start:self.position]
        if ident == 'null':
            return None
        if ident == 'true':
            return True
        if ident == 'false':
            return False
        if ident in ('inf', 'infinity', 'Inf', 'Infinity') or ident in ('nan', 'Nan', 'NaN'):
            return float(ident)
        return ident
