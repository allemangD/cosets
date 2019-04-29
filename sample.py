import util
from mirrors import PlaneAngles
from toddcox import solve
from util import schlafli, Vec, V


def apply(point, word, mirrors):
    point = Vec(point)

    for gen in word:
        mirror = mirrors[gen]
        point = point.reflect(mirror)

    return point


def dodeca_points():
    gens, subgens, rels = schlafli('xyz', 'xy', (5, 3))
    cos = solve(gens, subgens, rels)

    gens, subgens, rels = schlafli('xy', '', (5,))
    face_cos = solve(gens, subgens, rels)

    angles = PlaneAngles('xyz', **{'xy': 5, 'yz': 3})
    mirrors = angles.normals

    print(cos)
    print(face_cos)
    print(mirrors)

    print(cos.words)
    print(face_cos.words)

    points = [apply((1, 1, 1), word, mirrors) for word in face_cos.words]

    import turtle
    pen = turtle.Turtle()
    pen.penup()
    for point in points:
        for word in cos.words:
            p = apply(point, word, mirrors)
            pen.setpos(*p[:2] * 100)
            pen.dot(5, 'red')
    pen.penup()
    turtle.done()


def make_all(gens, subgens, coeffs):
    angles = PlaneAngles(gens)
    for (x, y), a in zip(util.pairwise(gens), coeffs):
        angles[x, y] = a

    mirrors = angles.normals
    cosets = solve(*schlafli(gens, subgens, coeffs))
    elements = solve(*schlafli(subgens, '', coeffs[:len(subgens) - 1]))

    return mirrors, cosets.words, elements.words


def draw_all(gens, subgens, rels, P, pen):
    def proj(point):
        x, y, z = point[:3]
        return V(x + .2 * z, y + .1 * z)

    mirrors, cos_words, el_words = make_all(gens, subgens, rels)

    for cos in cos_words:
        pen.penup()
        for el in el_words:
            p = apply(P, el + cos, mirrors)
            pen.setpos(*proj(p) * 300)
            pen.dot(5)
            pen.pendown()


def dodeca_edges():
    import turtle
    pen = turtle.Turtle()
    pen.speed(0)

    mults = (5, 3)
    P = V(.91, .28, .19)

    # mults = (4, 3)
    # P = V(-.9, .9, 1)


    pen.color('red')
    draw_all('rgb', 'r', mults, P, pen)
    # pen.color('green')
    # draw_all('rgb', 'g', mults, P, pen)
    pen.color('blue')
    draw_all('rgb', 'b', mults, P, pen)

    turtle.done()


if __name__ == '__main__':
    dodeca_edges()
