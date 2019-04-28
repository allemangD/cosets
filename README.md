# Cosets

A Python implementation of the Todd-Coxeter algorithm for coset enumeration

# Usage:

## `toddcox.solve(gens, subgens, rels)`

Given the presentation of a group G and a subgroup H, enumerate the cosets of H in G and determine the relations between them.

`gens` an iterable of names for generators of G.

`subgens` an iterable of generators of H. Each element in `subgens` must also appear in `gens`.

`rels` an iterable of words, where each word is considered an identity element of G. 

For example, `solve('xyz', 'xy', ('xx', 'yy', 'xz'))` enumerates the cosets of `<x, y>` in `<x, y, z | xx = yy = xz = 1>`. 

The function returns the coset table after completing the Todd-Coxeter algorithm.

For example, solving cosets of the trivial subgroup of the symmetric group S3:

```python
from toddcox import solve
print(solve('ab', '', ('a' * 2, 'b' * 2, 'ab' * 3)))
```

```text
    a b
0 | 1 2
1 | 0 3
2 | 4 0
3 | 5 1
4 | 2 5
5 | 3 4
```


## `util.coxeter(gens, subgens, rels)`

Given a coxeter graph, compute the relations of the group.

`gens` an iterable of names for generators of G.

`subgens` an iterable of generators of H. Each element in `subgens` must also appear in `gens`.

`rels` an iterable of words, where each word is considered an identity element of G. For pairs of generators in `gens` which are *not* related in `rels`, a relation is automatically added between the two generators with multiplicity 2. Additionally, the square of each generator is added as a relation.

For example, `coxeter('xyz', 'xy', ('xy' * 4, 'yz' * 3))` would produce `'xyz', 'xy', ('xy' * 4, 'yz' * 3, 'xz' * 2, 'x' * 2, 'y' * 2, 'z' * 2)`.

Note the addition of `'xz' * 2` and `'x' * 2, 'y' * 2, 'z' * 2` in the result.

### `util.schlafli(gens, subgens, rels)`

Given a schlafli symbol, compute the relations of the group.

`gens` an iterable of names for generators of G.

`subgens` an iterable of generators of H. Each element in `subgens` must also appear in `gens`.

`rels` is an iterable of multiplicities, where each multiplicity relates the corresponding pair of generators in `gens`. For example, `schlafli('xyzw', 'xy', (5, 4, 3))` is equivalent to `coxeter('xyzw', 'xy', ('xy' * 5, 'yz' * 4, 'zw' * 3))`