from util import schlafli
from toddcox import solve


def main():
    # gens, subgens, rels = schlafli('rgby', 'rg', (5, 3, 3))

    print(solve('ab', '', ('a' * 2, 'b' * 2, 'ab' * 3)))


if __name__ == '__main__':
    main()
