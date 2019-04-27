from itertools import tee, permutations


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def coxeter(gens, subgens, rels):
    """
    specify relations in terms of coxeter diagram

    for example the following are equivalent:
    coxeter('xyz', H, ('xy' * 4, 'yz' * 3))
      solve('xyz', H, ('xy' * 2, 'yz' * 3, 'xz' * 2, 'x' * 2, 'y' * 2, 'z' * 2))
    """

    assert isinstance(rels, tuple)

    inc_links = {frozenset(rel) for rel in rels}
    all_links = {frozenset(rel) for rel in permutations(gens, r=2)}
    missing_links = all_links - inc_links

    rels += tuple(''.join(link) * 2 for link in missing_links)
    rels += tuple(gen * 2 for gen in gens)

    return gens, subgens, rels


def schlafli(gens, subgens, rels):
    """
    specify relations in terms of the Schlafli symbol

    for example the following are equivalent:
    schlafli('xyz', H, (4, 3))
     coxeter('xyz', H, ('xy' * 4, 'yz' * 3))
       solve('xyz', H, ('xy' * 2, 'yz' * 3, 'xz' * 2, 'x' * 2, 'y' * 2, 'z' * 2))

    """

    assert len(gens) == len(rels) + 1

    cox_rels = tuple(
        ''.join(pair) * coeff
        for pair, coeff in zip(pairwise(gens), rels)
    )

    return coxeter(gens, subgens, cox_rels)