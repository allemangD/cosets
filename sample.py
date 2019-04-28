from util import schlafli
from toddcox import solve


def main():
    gens, subgens, rels = schlafli('rgby', 'rg', (5, 3, 3))

    print(solve(gens, subgens, rels))


if __name__ == '__main__':
    main()
