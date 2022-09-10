r"""
Iterable of the keys of a Mapping associated with nonzero values
"""

from collections.abc import MappingView, Sequence, Set


class SupportView(MappingView, Sequence, Set):
    r"""
    Dynamic view of the set of keys of a dictionary that are associated with nonzero values

    It behaves like the objects returned by the :meth:`keys`, :meth:`values`,
    :meth:`items` of a dictionary (or other :class:`collections.abc.Mapping`
    classes).

    INPUT:

    - ``mapping`` -- a :class:`dict` or another :class:`collections.abc.Mapping`.

    - ``zero`` -- (optional) test for zeroness by comparing with this value.

    EXAMPLES::

        sage: d = {'a': 47, 'b': 0, 'c': 11}
        sage: from sage.structure.support_view import SupportView
        sage: supp = SupportView(d); supp
        SupportView({'a': 47, 'b': 0, 'c': 11})
        sage: 'a' in supp, 'b' in supp, 'z' in supp
        (True, False, False)
        sage: len(supp)
        2
        sage: list(supp)
        ['a', 'c']
        sage: supp[0], supp[1]
        ('a', 'c')
        sage: supp[-1]
        'c'
        sage: supp[:]
        ('a', 'c')

    It reflects changes to the underlying dictionary::

        sage: d['b'] = 815
        sage: len(supp)
        3
    """

    def __init__(self, mapping, *, zero=None):
        r"""
        TESTS::

            sage: from sage.structure.support_view import SupportView
            sage: supp = SupportView({'a': 'b', 'c': ''}, zero='')
            sage: len(supp)
            1
        """
        self._mapping = mapping
        self._zero = zero

    def __len__(self):
        r"""
        TESTS::

            sage: d = {'a': 47, 'b': 0, 'c': 11}
            sage: from sage.structure.support_view import SupportView
            sage: supp = SupportView(d); supp
            SupportView({'a': 47, 'b': 0, 'c': 11})
            sage: len(supp)
            2
        """
        length = 0
        for key in self:
            length += 1
        return length

    def __getitem__(self, index):
        r"""
        TESTS::

            sage: d = {'a': 47, 'b': 0, 'c': 11}
            sage: from sage.structure.support_view import SupportView
            sage: supp = SupportView(d); supp
            SupportView({'a': 47, 'b': 0, 'c': 11})
            sage: supp[2]
            Traceback (most recent call last):
            ...
            IndexError
        """
        if isinstance(index, slice):
            return tuple(self)[index]
        if index < 0:
            return tuple(self)[index]
        for i, key in enumerate(self):
            if i == index:
                return key
        raise IndexError

    def __iter__(self):
        r"""
        TESTS::

            sage: d = {'a': 47, 'b': 0, 'c': 11}
            sage: from sage.structure.support_view import SupportView
            sage: supp = SupportView(d); supp
            SupportView({'a': 47, 'b': 0, 'c': 11})
            sage: iter(supp)
            <generator object SupportView.__iter__ at 0x7f7ebbb97e40>
        """
        zero = self._zero
        if zero is None:
            for key, value in self._mapping.items():
                if value:
                    yield key
        else:
            for key, value in self._mapping.items():
                if value != zero:
                    yield key

    def __contains__(self, key):
        r"""
        TESTS::

            sage: d = {'a': 47, 'b': 0, 'c': 11}
            sage: from sage.structure.support_view import SupportView
            sage: supp = SupportView(d); supp
            SupportView({'a': 47, 'b': 0, 'c': 11})
            sage: 'a' in supp, 'b' in supp, 'z' in supp
            (True, False, False)
        """
        try:
            value = self._mapping[key]
        except KeyError:
            return False
        zero = self._zero
        if zero is None:
            return bool(value)
        return value != zero
