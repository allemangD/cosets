from collections import defaultdict


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

    def add_row(self):
        i = len(self)
        self.rows.append(Row(self.rel, i))
        return i

    def apply(self, cosets: 'Cosets'):
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
        ])


class Cosets:
    def __init__(self, gens):
        self.gens = gens
        self.cosets = defaultdict(lambda: defaultdict(lambda: None))

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


class Solver:
    def __init__(self, gens, subgens, rels):
        self.cosets = Cosets(gens)
        self.subgens = subgens
        self.rels = [Relation(rel, rows=1) for rel in rels]

        for gen in subgens:
            self.cosets.set(0, gen, 0)


def main():
    c = Cosets('rgb')
    c.set(0, 'r', 1)

    r = Relation('rr')
    r.add_row()
    r.add_row()

    print(r, end='\n\n')
    learned = r.apply(c)
    for cos, gen, tar in learned:
        c.set(cos, gen, tar)

    print(r, end='\n\n')


if __name__ == '__main__':
    main()
