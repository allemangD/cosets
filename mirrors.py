import math

from util import Vec, V


class PlaneAngles:
    default = math.pi / 2

    def __init__(self, planes, **angles):
        self.angles = {}
        self.planes = planes

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
        assert p in self.planes and q in self.planes
        self.angles[p, q] = math.pi / value

    def __getattr__(self, item):
        return self[item]

    def __len__(self):
        return len(self.planes)

    def __str__(self):
        return str(self.planes)

    @property
    def normals(self):
        normals = []

        for p in self.planes:
            vp = []
            for m, (q, vq) in enumerate(zip(self.planes, normals)):
                vpm = (math.cos(self[p, q]) - vq[:m] @ vp[:m]) / vq[m]
                vp.append(round(vpm, 15))
            vp.append(round(math.sqrt(1 - Vec(vp).norm2), 15))
            normals.append(Vec(vp))

        return {p: n[:len(normals)] for p, n in zip(self.planes, normals)}


if __name__ == '__main__':
    v = V(1, 2, 3)

    pa = PlaneAngles(xy=4, yz=3)
    ns = pa.normals
    print(ns)
