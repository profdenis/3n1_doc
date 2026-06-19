# 5. Multiple Inheritance

Multiple inheritance in Python is a powerful feature that allows a class to inherit attributes and methods from more
than one parent class. This is a significant difference from Java, which only supports single inheritance for classes
(though Java does allow implementing multiple interfaces).

## How Multiple Inheritance Works in Python

In Python, multiple inheritance is implemented by listing all parent classes in the class definition, separated by
commas:

```python
class Parent1:
    def method1(self):
        print("Method from Parent1")


class Parent2:
    def method2(self):
        print("Method from Parent2")


class Child(Parent1, Parent2):
    pass


# Creating an instance
child = Child()
child.method1()  # Output: Method from Parent1
child.method2()  # Output: Method from Parent2
```

In this example, the `Child` class inherits methods from both `Parent1` and `Parent2`, allowing it to use both
`method1()` and `method2()`.

## Practical Example: The Mythical Unicorn

Let's consider a more concrete example using a mythical creature:

```python
class Horse:
    def __init__(self, name):
        self.name = name

    def run(self):
        return f"{self.name} is running."

    def eat_hay(self):
        return f"{self.name} is eating hay."


class Narwhal:
    def swim(self):
        return f"{self.name} is swimming."

    def has_horn(self):
        return True


class Unicorn(Horse, Narwhal):
    def magic_powers(self):
        return f"{self.name} is using magical powers!"
```

Here, `Unicorn` inherits characteristics from both `Horse` (running, eating hay) and `Narwhal` (swimming, having a
horn), plus adds its own unique ability.

## Method Resolution Order (MRO)

When a method is called on an instance, Python needs to determine which implementation to use, especially if multiple
parent classes define the same method. Python uses the C3 linearization algorithm to establish a Method Resolution
Order (MRO):

```python
class A:
    def greet(self):
        return "Hello from A"


class B:
    def greet(self):
        return "Hello from B"


class C(A, B):
    pass


c = C()
print(c.greet())  # Output: Hello from A
print(C.__mro__)  # Shows the method resolution order
```

The method from the first parent class in the inheritance list (`A` in this case) is used.

## Advantages of Multiple Inheritance

1. **Code Reusability**: Allows combining functionalities from different classes, reducing code duplication.

2. **Flexibility in Class Design**: Enables creating complex class structures by inheriting from multiple base classes.

3. **Modularity**: Supports creating mixins (specialized classes providing specific functionality) that can be combined
   with various classes.

## Disadvantages of Multiple Inheritance

1. **Ambiguity and Name Clashes**: When multiple parent classes define methods with the same name, it can lead to
   confusion.

2. **Complexity and Maintenance**: As the inheritance hierarchy grows, understanding and maintaining the relationships
   between classes becomes more challenging.

3. **Diamond Problem**: When a class inherits from two classes that have a common ancestor, ambiguity can arise about
   which implementation to use.

4. **Tight Coupling**: Changes in one base class may have unintended effects on derived classes.

## The Diamond Problem

The diamond problem is a specific challenge in multiple inheritance:

```python
class A:
    def method(self):
        print("Method from A")


class B(A):
    def method(self):
        print("Method from B")


class C(A):
    def method(self):
        print("Method from C")


class D(B, C):
    pass


d = D()
d.method()  # Which method gets called?
```

Python's MRO resolves this by following a specific order, but it's still a complexity to be aware of.

Multiple inheritance is a powerful tool in Python, but it should be used judiciously. When used appropriately, it can
lead to elegant, modular code. When overused, it can create maintenance challenges.


## How `super()` Works with Multiple Inheritance in Python

When a Python class inherits from two or more classes, the behavior of `super()` is determined by the **method
resolution order (MRO)**, as discussed above.

### Which Class Does `super()` Refer To?

In a class that inherits from multiple parent classes, `super()` refers to the **next class in the MRO**, not
necessarily the first parent listed in the class definition. For example:

```python
class A:
    def __init__(self):
        print("A initialized")


class B:
    def __init__(self):
        print("B initialized")


class C(A, B):
    def __init__(self):
        super().__init__()
        print("Child initialized")


child = C()
```

**Output:**

```
A initialized
C initialized
```

Here, `super().__init__()` in `Child` calls `A.__init__()` because `A` is the next class in the MRO after
`C`[5][6]. The MRO for `C` is `[C, A, B, object]`.

### How to Refer to the Other Parent Class?

If you want to explicitly call a method from a specific parent class (not just the next in the MRO), you can do so by
directly referencing the class:

```python
class C(A, B):
    def __init__(self):
        super().__init__()  # Calls A.__init__()
        B.__init__(self)  # Explicitly calls B.__init__()
        print("C initialized")
```

This way, both parent initializers are called, but be cautious-if both parent classes call `super()`, you may end up
calling the same method multiple times, depending on the MRO and class design[1][5].

### Advanced Use: Customizing `super()`

You can also customize where `super()` starts its search by passing arguments:

```python
super(B, self).__init__()
```

This tells Python to start looking for the method after `Parent2` in the MRO of `self`[7]. This is rarely needed in
typical class designs, but it can be useful in advanced multiple inheritance scenarios.

### Summary Table

| Scenario                       | What `super()` Calls            | How to Call the Other Parent      |
|--------------------------------|---------------------------------|-----------------------------------|
| Multiple inheritance `C(A, B)` | Next class in MRO after current | Explicitly: `B.method(self, ...)` |
| Customizing `super()`          | After specified class in MRO    | Use `super(C, self).method()`     |

### Key Points

- `super()` always refers to the next class in the MRO, not necessarily the first parent in the class definition[6][5].
- To call a specific parent class's method, use the parent class name directly.
- Be careful with multiple inheritance and `super()` to avoid duplicate calls or missed initializations.

For most cases, stick to using `super()` consistently and design your classes to cooperate with it, especially when
building frameworks or mixins[6][7].


## Example with the diamond problem

```python
class Alpha:
    def __init__(self):
        print("Alpha initialized")


class A(Alpha):
    def __init__(self):
        super().__init__()
        print("A initialized")


class B(Alpha):
    def __init__(self):
        super().__init__()
        print("B initialized")


class C(A, B):
    def __init__(self):
        super().__init__()  # Calls A.__init__()
        B.__init__(self)  # Explicitly calls B.__init__()
        print("C initialized")


child = C()
print(C.__mro__)
```

### Output

```text
Alpha initialized
B initialized
A initialized
Alpha initialized
B initialized
C initialized
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Alpha'>, <class 'object'>)
```

**Why do we get multiple calls to the exact same `__init__` methods ?**

Let's break down why this happens step-by-step:

### Key Explanation

The output occurs because of two factors:

1. **Method Resolution Order (MRO)** in multiple inheritance
2. **Explicit call to `B.__init__`** in class `C`

Here's how the code executes:

---

### Execution Flow

1. **`C()` is created** → Calls `C.__init__`
2. **`super().__init__()` in `C`** → Follows MRO to call `A.__init__`
3. **`A.__init__` runs**:
    - `super().__init__()` → Next in MRO is `B` (not `Alpha`!), so `B.__init__` runs
    - `B.__init__` → `super().__init__()` calls `Alpha.__init__` (prints "Alpha initialized")
    - `B.__init__` completes (prints "B initialized")
    - Back to `A.__init__` (prints "A initialized")
4. **Explicit `B.__init__(self)` in `C`** → Directly calls `B.__init__` again:
    - `super().__init__()` → Calls `Alpha.__init__` again (prints "Alpha initialized")
    - `B.__init__` completes again (prints "B initialized")
5. **`C.__init__` finishes** (prints "C initialized")

---

### Why MRO Matters

The MRO for `C` is **`C → A → B → Alpha → object`** (visible in the output). This means:

- When `super()` is called in `A`, it looks for the next class in the MRO chain (`B`), **not** `A`'s direct parent (
  `Alpha`).

---

### Why "Alpha" Appears Twice?

1. First "Alpha" comes from the `A → B → Alpha` chain via `super()` in `C`
2. Second "Alpha" comes from the explicit `B.__init__` call in `C`, which triggers `B → Alpha` again

---

### How to Fix This (If Needed)

If you want to avoid duplicate initializations:

```python
class C(A, B):
    def __init__(self):
        # Let MRO handle all parent initializations
        super().__init__()  # Follows C→A→B→Alpha chain
        print("C initialized")
```

**Output with this fix**:

```
Alpha initialized
B initialized
A initialized
C initialized
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Alpha'>, <class 'object'>) 
```

---

### Key Takeaways

1. **MRO determines `super()` behavior**, not just parent classes
2. **Explicit parent calls** (`B.__init__`) bypass MRO and can cause duplicates
3. **Consistent `super()` usage** is safer in complex inheritance

Don't forget to run `print(C.__mro__)` to see the exact method resolution order.

