from mirrors import PlaneAngles
from toddcox import solve
from util import schlafli


def main():
    gens, subgens, rels = schlafli('xyz', 'xy', (5, 3))
    cos = solve(gens, subgens, rels)

    gens, subgens, rels = schlafli('x', '', ())
    face_cos = solve(gens, subgens, rels)

    angles = PlaneAngles('xyz', **{'xy': 5, 'yz': 3})
    normals = angles.normals

    print(cos)
    print(face_cos)
    print(normals)

    print(cos.words)


if __name__ == '__main__':
    main()
