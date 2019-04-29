import math


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

    def project(self, target):
        target = Vec(target)
        return (self @ target) / target.norm2 * target

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


# noinspection PyPep8Naming
def V(*components):
    return Vec(components)


class PlaneAngles:
    default = math.pi / 2

    def __init__(self, planes=None, **angles):
        self.angles = {}
        self.planes = planes if planes is not None else set()

        for (p, q), a in angles.items():
            self[p, q] = a

    def __getitem__(self, pair):
        p, q = pair

        if p == q:
            return 0.0

        if (p, q) not in self.angles:
            p, q = q, p

        return self.angles.get((p, q), self.default)

    def __setitem__(self, pair, value):
        p, q = pair
        self.angles[p, q] = math.pi / value
        self.planes |= {p, q}

    def __getattr__(self, item):
        return self[item]

    def __len__(self):
        return len(self.planes)

    def __str__(self):
        return str(self.planes)

    @property
    def normals(self):
        planes = sorted(self.planes)
        normals = []

        for p in planes:
            vp = []
            for m, (q, vq) in enumerate(zip(planes, normals)):
                vpm = (math.cos(self[p, q]) - vq[:m] @ vp[:m]) / vq[m]
                vp.append(round(vpm, 15))
            vp.append(round(math.sqrt(1 - Vec(vp).norm2), 15))
            normals.append(Vec(vp))

        return {p: n[:len(normals)] for p, n in zip(planes, normals)}


if __name__ == '__main__':
    v = V(1, 2, 3)

    pa = PlaneAngles(xy=4, yz=3)
    ns = pa.normals
    print(ns)
