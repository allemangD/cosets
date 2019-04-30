import math
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


class Vec(tuple):
    @property
    def norm2(self):
        return self @ self

    @property
    def norm(self):
        return math.sqrt(self.norm2)

    @property
    def dim(self):
        return tuple.__len__(self)

    @property
    def normalized(self):
        return self / self.norm

    def project(self, target):
        target = Vec(target)
        return (self @ target) / (target @ target) * target

    def reflect(self, axis):
        return self - 2 * self.project(axis)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Vec(self[i] for i in range(*item.indices(item.stop)))

        if item < self.dim:
            return super(Vec, self).__getitem__(item)

        return 0.0

    def __len__(self):
        return self.dim

    def __matmul__(self, other):
        return sum(x * y for x, y in zip(self, other))

    def __rmatmul__(self, other):
        return sum(x * y for x, y in zip(self, other))

    def __mul__(self, other):
        return Vec(x * other for x in self)

    def __rmul__(self, other):
        return Vec(other * x for x in self)

    def __truediv__(self, other):
        return Vec(x / other for x in self)

    def __add__(self, other):
        return Vec(x + y for x, y in zip(self, other))

    def __radd__(self, other):
        return Vec(y + x for x, y in zip(self, other))

    def __sub__(self, other):
        return Vec(x - y for x, y in zip(self, other))

    def __rsub__(self, other):
        return Vec(y - x for x, y in zip(self, other))

    def __repr__(self):
        return f'<{", ".join(str(x) for x in self)}>'


def V(*components):
    return Vec(components)
