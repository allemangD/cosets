from mirrors import PlaneAngles
from toddcox import solve
from util import schlafli


def main():
    cos = solve(*schlafli('xyz', 'xy', (5, 3)))
    face_cos = solve(*schlafli('xy', '', (5,)))

    angles = PlaneAngles('xyz', **{'xy': 5, 'yz': 3})
    normals = angles.normals

    print(cos)
    print(face_cos)
    print(normals)


if __name__ == '__main__':
    main()
