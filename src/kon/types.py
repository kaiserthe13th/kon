from typing import Iterable, Dict, Union

# Type alias for KON (Key-Object Notation) objects
# Supports nested dicts, iterables, primitives (int, float, str, bool), and None
KonDictionary = Dict[Union[str, int, float, bool, None], "KonObject"]
KonObject = Union[KonDictionary, Iterable["KonObject"], int, float, str, bool, None]

__all__ = ('KonDictionary', 'KonObject')
