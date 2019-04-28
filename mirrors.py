import math
from itertools import combinations


def dot(u, v):
    return sum((x * y for x, y, in zip(u, v)))


def len2(u):
    return dot(u, u)


def s(v, i):
    return v[:i]


def solve(planes, angles):
    assert len(planes) == len(angles)
    n = len(planes)
    vn = []
    for m in range(len(planes)):
        vnm = math.cos(angles[m]) - dot(s(planes[m], m), s(vn, m)) / planes[m][m]
        vn.append(vnm)
    vnn = math.sqrt(1 - len2(s(vn, n)))
    vn.append(vnn)

    return tuple(vn)


def solve_all(all_angles):
    planes = []
    for angles in all_angles:
        v = solve(planes, angles)
        planes.append(v)
    return planes


if __name__ == '__main__':
    a = [[], [math.radians(45)], [math.radians(60), math.radians(90)]]

    print(solve_all(a))

# def solve(plane_angles):
#     """
#     For example, normals(ab=4, bc=3, ac=2) solves the normals for
#     planes a, b, c where the dihedral angle between a and b is
#     180/4 degrees, between b and c is 180/3 degrees, and between
#     a and c is 180/2 degrees.
#
#     :param plane_angles: dictionary, where keys are 2-tuples (or
#     strings) of plane labels, and values are the fraction of
#     180deg for the angle between planes.
#     :return: a dictionary, where keys are the plane labels given
#     in plane_angles and values are the normal vectors for each plane
#     """
#
#     plane_angles = {(p1, p2): a for (p1, p2), a in plane_angles.items()}
#     planes = [p for pair in plane_angles for p in pair]
#     for p1, p2 in combinations(planes, r=2):
#         assert (p1, p2) in plane_angles or (p2, p1) in plane_angles
#
#     normals = [(1,)]
