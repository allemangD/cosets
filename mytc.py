from collections import defaultdict
from itertools import permutations, tee


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Row:
    def __init__(self, rel, i):
        """
        :param i: index of this row
        :param num: number of terms in relation
        """

        self.rel = rel
        self.row = [i] * (len(rel) + 1)
        self.left = 0
        self.right = len(rel)

    @property
    def left_coset(self):
        return self.row[self.left]

    @property
    def right_target(self):
        return self.row[self.right]

    @property
    def left_gen(self):
        return self.rel[self.left]

    @property
    def right_gen(self):
        return self.rel[self.right - 1]

    @property
    def complete(self):
        return not self.unknown

    @property
    def unknown(self):
        """ return range of unknown data"""
        return range(self.left + 1, self.right)

    @property
    def learned(self):
        """ give the information learned by this row, or none if not complete """
        if not self.complete:
            return None

        return self.left_coset, self.left_gen, self.right_target

    def apply(self, cosets: 'Cosets'):
        updated = False

        while not self.complete:
            left_target = cosets.get(self.left_coset, self.left_gen)
            if left_target is None:
                break

            updated = True
            self.left += 1
            self.row[self.left] = left_target

        while not self.complete:
            right_coset = cosets.rget(self.right_gen, self.right_target)
            if right_coset is None:
                break

            updated = True
            self.right -= 1
            self.row[self.right] = right_coset

        return updated

    def __str__(self):
        return ' '.join('?' if i in self.unknown else str(d) for i, d in enumerate(self.row))


class Relation:
    def __init__(self, rel, rows=1):
        self.rel = rel
        self.rows = []

        for _ in range(rows):
            self.add_row()

    def __len__(self):
        return len(self.rows)

    @property
    def complete(self):
        return all(row.complete for row in self.rows)

    def add_row(self):
        i = len(self)
        self.rows.append(Row(self.rel, i))
        return i

    def apply(self, cosets: 'Cosets'):
        """:returns the set of relations learned"""
        learned = set()

        for row in self.rows:
            if row.apply(cosets):
                row_learned = row.learned

                if row_learned:
                    learned.add(row_learned)

        return learned

    def __str__(self):
        return '\n'.join([
            ' ' + ' '.join(str(r) for r in self.rel),
            '\n'.join(str(row) for row in self.rows)
        ]) + '\n'


class Cosets:
    def __init__(self, gens):
        self.gens = gens
        self.cosets = defaultdict(lambda: {g: None for g in self.gens})

    def get(self, coset, gen):
        target = self.cosets[coset][gen]
        return target

    def rget(self, gen, target):
        for i, coset in self.cosets.items():
            if coset[gen] == target:
                return i
        return None

    def set(self, coset, gen, target):
        self.cosets[coset][gen] = target

    def add_coset(self):
        for i, coset in self.cosets.items():
            for gen, target in coset.items():
                if target is None:
                    self.set(i, gen, len(self.cosets))
                    _ = self.cosets[len(self.cosets)]  # to create the row in defaultdict

                    return True
        return False

    def __str__(self):
        table = [
                    [' ', ' '] + [str(g) for g in self.gens],
                ] + [
                    [str(coset), '|'] + [str(targets[gen]) for gen in self.gens]
                    for coset, targets in self.cosets.items()
                ]

        return '\n'.join(' '.join(row) for row in table) + '\n'


class Solution:
    def __init__(self, cosets, rels):
        self.cosets = cosets
        self.rels = rels

    def __str__(self):
        return str(self.cosets)


def solve(gens, subgens, rels):
    cosets = Cosets(gens)
    subgens = subgens
    rels = [Relation(rel, rows=1) for rel in rels]

    for gen in subgens:
        cosets.set(0, gen, 0)

    while not all(rel.complete for rel in rels):
        while True:
            changed = False

            for rel in rels:
                learned = rel.apply(cosets)
                if learned:
                    changed = True
                for cos, gen, tar in learned:
                    cosets.set(cos, gen, tar)

            if not changed:
                break

        if cosets.add_coset():
            for rel in rels:
                rel.add_row()
        else:
            break

    return Solution(cosets, rels)


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

    return solve(gens, subgens, rels)


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


def main():
    print(schlafli('rgby', 'rgb', (4, 3, 3)))


if __name__ == '__main__':
    main()
