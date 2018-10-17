# -*- coding: utf8 -*-
"""Miscellaneous utilities.
"""

__all__ = ('add_dict_property_ro',
           'ensure_kwarg_in',
           'ensure_kwarg_not_in',
           'check_kwarg',
           'check_kwargs')


def add_dict_property_ro(cls, dictattr, attr, default=None, **kw):
    """Add to class **cls** a read-only property returning a predefined entry
       from a dict.

       :param type cls:
            the target class to be modified,
       :param str dictattr:
            name of the attribute of **cls** being the source dict,
       :param str,tuple attr:
            name of the generated attribute, or a tuple ``(attr, key)``,
            where ``attr`` is the generated attribute name and ``key`` is
            the corresponding key in the dictionary,
       :param default:
            default value returned by the property, if the dictionary
            has no requested key.
       :keyword str doc:
            optional documentation string, the string may use substitutions,
            such as ``"%(cls)s"``, ``"%(dictattr)s"``, ``"%(attr)s"``,
            ``"%(key)s"``, ``"%(default)s"``. Extra variables for necessary
            substitutions may be provided via keyword arguments ``**kw``.
    """
    if isinstance(attr, str):
        key = attr
    else:
        (attr, key) = attr  # assumed it's a tuple or alike

    def getter(obj, k=key):
        return getattr(obj, dictattr).get(k, default)

    try:
        tdoc = kw['doc']
    except KeyError:
        doc = None
    else:
        locs = {k: v for k, v in locals().items()
                if k not in ('tdoc', 'kw', 'getter')}
        doc = tdoc % dict(locs, **kw)
    setattr(cls, attr, property(getter, doc=doc))


def ensure_kwarg_in(caller, key, allowed):
    """Checks a single **key** from keyword arguments against allowed keys.

       If **key** is not in **allowed** keys, throws :exc:`TypeError`.

       :param str caller: name of the caller,
       :param str key: the key to be examined,
       :param allowed: sequence of allowed keys.

       :return: True
    """
    if allowed is not None and key not in allowed:
        msg = "%s got an unexpected keyword argument %r" % \
                (str(caller), key)
        raise TypeError(msg)
    return True


def ensure_kwarg_not_in(caller, key, forbidden):
    """Checks a single **key** from keyword arguments against forbidden keys.

       If **key** is in **forbidden** keys, throws :exc:`TypeError`.

       :param str caller: name of the caller,
       :param str key: the key to be examined,
       :param forbidden: sequence of forbidden keys.

       :return: True
    """
    if forbidden is not None and key in forbidden:
        msg = "%s got a forbidden keyword argument %r" % \
                (str(caller), key)
        raise TypeError(msg)
    return True


def check_kwarg(caller, key, allowed=None, forbidden=None):
    """Checks a single **key** from keyword arguments against allowed and
       forbidden keys.

       If **key** is not in **allowed** keys or it is in **forbidden** keys,
       throws :exc:`TypeError`.

       :param str caller: name of the caller,
       :param str key: the key to be examined,
       :param allowed: sequence of allowed keys.
       :param forbidden: sequence of forbidden keys.

       :return: True
    """
    ensure_kwarg_in(caller, key, allowed)
    ensure_kwarg_not_in(caller, key, forbidden)
    return True


def check_kwargs(caller, kw, allowed=None, forbidden=None):
    """Checks all keys from keyword arguments **kw** against allowed and
       forbidden keys.

       If **key** is not in **allowed** keys or it is in **forbidden** keys,
       throws :exc:`TypeError`.

       :param str caller: name of the caller,
       :param str key: the key to be examined,
       :param allowed: sequence of allowed keys.
       :param forbidden: sequence of forbidden keys.

       :return: True
    """
    for key in kw:
        check_kwarg(caller, key, allowed, forbidden)
    return True


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4: