# -*- coding: utf-8 -*-
"""Provides the :class:`.Selector` class.
"""


__all__ = ('Selector',)


class Selector(dict):
    """A replacement for ``SCons.Util.Selector`` class.

    :class:`.Selector` returns a dictionary value for the longest matched
    source suffix found in the dictionary.

    To have an example, for the following selector

    .. code-block:: python

            sel = Selector({'.h': 'H', '.t.h': 'TH'})

    all the assertions below hold

    .. code-block:: python

            assert sel(env, ['foo.h']) == 'H'
            assert sel(env, ['foo.t.h']) == 'TH'

    The original ``SCons.Util.Selector`` would only select ``'H'``, no matter
    what you do.
    """
    def __call__(self, env, source, ext=None):
        select_from = _get_selector_func(source, ext)
        items = []
        for x_dict in _separate_literals(self.items(), env):
            try:
                item = select_from(x_dict)
            except KeyError:
                pass
            else:
                items.append(item)
        try:
            return _choose_better(items)
        except IndexError:
            return self.get(None)


def _get_selector_func(source, ext):
    if ext is not None:
        return lambda x_dict, e=ext: (e, x_dict[e])
    try:
        src = str(source[0])
    except IndexError:
        return lambda x_dict: ('', x_dict[''])
    else:
        return lambda x_dict, s=src: _select_best(x_dict.items(), s)


def _separate_literals(items, env):
    # Split-up items into two dictionaries. First one with items whose keys
    # were given literally, and the second with items whose keys had
    # substitutions.
    (l_dict, s_dict) = ({}, {})
    for item in items:
        _separate_handle_item(env, (l_dict, s_dict), item)
    return (l_dict, {s_k: x[1] for (s_k, x) in s_dict.items()})


def _separate_handle_item(env, dicts, item):
    (l_dict, s_dict) = dicts
    (k, v) = item
    if k is None:
        return
    s_k = env.subst(k)
    if k == s_k:
        l_dict[k] = v  # it's literal
    else:
        if s_k in s_dict:
            # We only raise an error when variables point
            # to the same suffix. If one suffix is literal
            # and a variable suffix contains this literal,
            # the literal wins and we don't raise an error.
            raise KeyError(s_dict[s_k][0], k, s_k)
        s_dict[s_k] = item


def _select_best(items, src):
    ml = [(suf, v) for (suf, v) in items if src.endswith(suf)]
    if not ml:
        raise KeyError('suffix not found for %s' % repr(src))
    ml = list(sorted(ml, key=lambda x: len(x[0]), reverse=True))
    return ml[0]


def _choose_better(items):
    (k, v) = items[0]
    if len(items) == 2 and len(items[1][0]) > len(k):
        (k, v) = items[1]
    return v


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
