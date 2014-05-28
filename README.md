# DiceBox

`DiceBox` is a Python library for rolling dice.

## Usage

A die is created using the `d` function and then rolled whenever it is called.

```python
>>> from dicebox import d
>>> d20 = d(20)
>>> d20()
4
>>> d20()
17
>>> d20()
8
```

You can do basic arithmetic on a die as well. For example, say you want to roll for an attack that does `2d10+5` damage:

```python
>>> attack = 2 * d(10) + 5
>>> attack()
[4, 8, 5]
>>> attack()
[9, 1, 5]
>>> attack()
[8, 9, 5]
```

Operations stack as well. Say you wanted to roll the previous attack for 3 hits:

```python
>>> (attack * 3)()
[[2, 2, 5], [7, 9, 5], [4, 4, 5]]
```

You can use `>>` and `<<` to get the best and worst n rolls respectively:

```python
>>> (10 * d(20) >> 3)()
[13, 16, 20]
```


