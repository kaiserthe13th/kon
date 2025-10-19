import abc
from typing import Iterable, Protocol, TypeVar, cast, Union, runtime_checkable

from .parser import KonParser, MultilineStringBehaviour
from .types import KonObject, KonDictionary

try:
    from typing_extensions import Reader, Writer # type: ignore
except ImportError:
    # Taken from typing_extensions.pyi, licensed under
    _T_co = TypeVar("_T_co", covariant=True)  # Any type covariant containers.
    _T_contra = TypeVar("_T_contra", contravariant=True)

    @runtime_checkable
    class Reader(Protocol[_T_co]):
        @abc.abstractmethod
        def read(self, size: int = ..., /) -> _T_co: ...

    @runtime_checkable
    class Writer(Protocol[_T_contra]):
        @abc.abstractmethod
        def write(self, data: _T_contra, /) -> int: ...


def _dump_dict(
    object: KonDictionary,
    pretty: bool = False,
    indent_width: int = 2,
    _depth: int = 0,
    _is_top_level=False,
) -> str:
    """Serialize a dictionary to KON format string."""

    if len(object) == 0:
        return '{}'
    
    def _child_top_level(child: KonObject):
        """Check if a child object should be treated as top-level for formatting."""
        if not pretty:
            return False
        if isinstance(child, dict):
            return len(child) == 1
        elif isinstance(child, Iterable) and not isinstance(child, str):
            child = list(child)
            return len(child) == 1
        return False
    
    rl = []
    for k, v in object.items():
        # Determine separator between key and value
        # Use space for dict values, no space for iterables, an equals sign for primitives
        inbetween = " = "
        if isinstance(v, dict):
            inbetween = " "
        elif isinstance(v, Iterable) and not isinstance(v, str):
            inbetween = ""
        rl.append(
            dumps(
                k,
                _is_top_level=False,
                pretty=pretty and len(object) != 1,
                indent_width=indent_width,
                _depth=_depth + 1 if not _is_top_level else _depth,
            )
            + inbetween
            + dumps(
                v,
                _is_top_level=_child_top_level(v),
                _no_indent=True,
                pretty=pretty,
                indent_width=indent_width,
                _depth=_depth if _is_top_level or (pretty and len(object) == 1) else _depth + 1,
            )
        )

    prefix = _depth * indent_width * " " if pretty else ""
    if pretty and len(object) != 1:
        prefp = "{\n"
        postp = f"\n{prefix}}}"
        join_str = "\n"
    else:
        prefp = "{"
        postp = "}"
        join_str = ", "

    if _is_top_level:
        return join_str.join(rl)
    return prefp + join_str.join(rl) + postp


def _dump_list(
    object: Iterable[KonObject],
    pretty: bool = False,
    indent_width: int = 2,
    _depth: int = 0,
) -> str:
    prefix = _depth * indent_width * " " if pretty else ""
    object = list(object)
    if len(object) == 0:
        return '()'
    if pretty and len(object) != 1:
        prefp = "(\n"
        postp = f"\n{prefix})"
        join_str = "\n"
    else:
        prefp = "("
        postp = ")"
        join_str = ", "

    return (
        prefp
        + join_str.join(
            dumps(
                i,
                _is_top_level=False,
                pretty=pretty and len(object) != 1,
                indent_width=indent_width,
                _depth=_depth if len(object) == 1 else _depth + 1,
            )
            for i in object
        )
        + postp
    )


def dumps(
    object: KonObject,
    *,
    pretty: bool = False,
    indent_width: int = 2,
    _no_indent: bool = False,
    _depth: int = 0,
    _is_top_level=True,
) -> str:
    """
    Serializes a Python object into a Kon-formatted string.
        Args:
            object (KonObject): The Python object to be serialized. Must be a
                valid `KonObject` (dict, list, str, int, float, bool, or None).
            pretty (bool, optional): If True, the output string will be formatted
                with newlines and indentation for readability. Defaults to False.
            indent_width (int, optional): The number of spaces for each indentation
                level when `pretty` is True. Defaults to 2.

        Raises:
            TypeError: If the object contains a type that cannot be serialized.

        Returns:
            str: The serialized string representation of the object.
    """
    prefix = _depth * indent_width * " " if pretty and not _no_indent else ""
    if isinstance(object, dict):
        return prefix + _dump_dict(cast(KonDictionary, object), pretty, indent_width, _depth, _is_top_level)
    elif isinstance(object, (int, float, bool)):
        return prefix + str(object).lower()
    elif isinstance(object, str):
        if object.isidentifier():
            return prefix + object
        return prefix + repr(object)
    elif isinstance(object, Iterable):
        return prefix + _dump_list(object, pretty, indent_width, _depth)
    elif object is None:
        return prefix + "null"
    else:
        raise TypeError(
            f"Dumped value must be a {KonObject}, but found value is {object!r}"
        )


def loads(source: Union[str, bytes, bytearray], *, allow_implicit_dicts=True, multiline_string_behaviour: MultilineStringBehaviour = MultilineStringBehaviour.IGNORE, **kwargs) -> KonObject:
    """
    Parse a Kon-formatted string, bytes, or bytearray into a Python object.

    Args:
        source (str | bytes | bytearray): The Kon-formatted data to be parsed.
        allow_implicit_dicts (bool, optional): If True, allows the parser to
            interpret unquoted strings at the start of a line as keys for an
            implicit dictionary. Defaults to True.
        multiline_string_behaviour (MultilineStringBehaviour, optional): Defines
            how multiline strings are handled. Defaults to
            MultilineStringBehaviour.IGNORE.
        **kwargs: Additional keyword arguments to be passed to the `KonParser`.

    Returns:
        KonObject: An object representing the parsed Kon data.
    """
    parser = KonParser(source, allow_implicit_dicts=allow_implicit_dicts, multiline_string_behaviour=multiline_string_behaviour, **kwargs)
    return parser.parse()


def dump(object: KonObject, file: Writer, **kwargs):
    result = dumps(object, **kwargs)
    file.write(result)

    
def load(file: Reader, **kwargs) -> KonObject:
    src = file.read()
    return loads(src, **kwargs)

__all__ = ('dumps', 'loads', 'dump', 'load', 'KonParser', 'MultilineStringBehaviour', 'KonDictionary', 'KonObject')
