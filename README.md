# DiceBox

`DiceBox` is a Python library for rolling dice.

The project started as a thought experiment. Could I create an expressive domain-specific language for describing dice rolls that was also valid Python? After some careful thought and liberal application of operator overloading I ended up with what you see here.

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

You can do basic arithmetic on a die as well. For example, say you want to roll for an attack that does `2d10+5` damage.

```python
>>> attack = 2 * d(10) + 5
>>> attack()
[4, 8, 5]
>>> attack()
[9, 1, 5]
>>> attack()
[8, 9, 5]
```

Operations stack as well. Say you wanted to roll the previous attack for 3 hits.

```python
>>> (attack * 3)()
[[2, 2, 5], [7, 9, 5], [4, 4, 5]]
```

You can use `>>` and `<<` to get the best and worst n rolls respectively. If more items are requested than exist, all the items are returned.

```python
>>> (10 * d(20) >> 3)()
[13, 16, 20]

>>> (3 * d(20) >> 1000)()
[8, 9, 10]
```

Calling `int` on the result of an operation will cause its result to be summed. So `int(5 * d(20))` will return the total value of the 5 rolls. When any operation is performed between 2 rollable objects, the one on the right is converted to an int. For example:

```python
>>> int(3 * d(10))
18

>>> (d(10) * d(5))()
[1, 10, 6, 9]
```
