---
markdown:
  path: README.md
export_on_save:
  markdown: true
---

# graphX {ignore=true}
A graph theory library that isn't *super* gross.

[TOC]

## Installing

**graphX does not work with Python 2. Make sure you have an up to date version of Python installed.**

```bash
$ pip3 install graphX
```

*note the capital `X`.*

graphX relies on [algorthimX](https://algrx.github.io) for visualisation. So you might have to install that as well.

## Quick Start
for using with your favourite text editor and running a server (recomened):
```python
import graphX as gx

g = gx.Graph()

@g.run_web
def code():
    # put all the code you want here, will be run everytime someone presses play/reload.
    g.add_node("A")
    g.add_node("B")

code()
```

## Methods

### Graph Methods: 
##### `run_web()`
a decorator function that starts the websever and runs your code on it.

```py
g = gx.Graph()

@g.run_web
def code():
    # code to run

code()
```

##### `add_node(n)`
adds the node `n` to the graph. Ignoring duplicate nodes.
```py
g.add_node("A")
g.add_node(42) 
```

##### `add_nodes(n_list)`
adds each element in the iterable (list or other type) `n_list` to the graph.
```py
g.add_nodes(["A","B",1,2,3]) 
g.add_ndoes("hello!") 
```

##### `get_nodes()`
returns a list of nodes.
```py
g.add_node("A")
g.add_node("B")
g.get_nodes() # returns: [Node("A", {}), Node("B", {})]
```

##### `get_node(val)`
returns the `Node` with that specific value (whatever `n` was when you ran `add_node(n)`).
```py
g.add_node("A")
g.get_node("A") # returns a Node object. `Node("A", {})`
```

##### `del_node(val)`
deletes the `Node` with that specific value (whatever `n` was when you ran `add_node(n)`).
```py
g.add_node("A")
g.del_node("A")
```

##### `add_edge(source, target)`
adds an edge between the source and target nodes.
```py
g.add_nodes("AB")

g.add_edge("A","B")

# use a different edge value:
g.add_edge("A","B", value=4) # defaults to 1

# set the edge to be directed.
g.add_edge("A","B", directed=True) # defaults to False
```

##### `del_edge(source, target)`
deletes the edge between the source and target nodes.
```py
g.add_nodes("ABC")
g.add_edge("A", "B")
g.add_edge("B", "C")

g.del_edge("A", "B")
```

##### `pause(time=1)`
pauses the code for `time` seconds.
```py
g.add_node("A")
g.pause()
g.add_node("B")
```

##### `clear()`
clears all nodes and edges from the graph.
```py
g.add_nodes("AB")
g.add_edge("A", "B")

g.clear()
```

### Node Methods:
##### `set_attr(attr, value)`
sets a Node's attribute to be `value`.
```py
g.add_node("A")
n = g.get_node("A")
n.set_attr("seen", False)
```

##### `get_attr(attr)`
gets an attribute's value from a Node.
```py
g.add_node("A")
n = g.get_node("A")
n.set_attr("seen", False)
n.get_attr("seen") # returns `False`
```

## Important Notes
##### Multiple Edges Between Two Nodes
graphX doesn't support having multiple edges between the same pair of nodes. Instead you should create dummy nodes.

```py
g.add_nodes("AB")
g.add_edge("A","B", 2)
g.add_edge("A","B", 3) # this won't make multiple edges, just use the latest one.

# so instead, use:
g.add_nodes("CD")
g.add_nodes("ab")
g.add_edge("C", "a", 2)
g.add_edge("C", "b", 3)
g.add_edge("a", "D", 0)
g.add_edge("b", "D", 0)
```

whilst this might initially look quite gross, it is better to be explicit than implicit. And from my experience, having the same two nodes connected by more than one edge is rarely used.


---

## Previous Works
* **[pynode](https://alexsocha.github.io/pynode/)** is the project that inspired this new library, mostly because pynode doesn't work well on macOS. Nor does it support jupyter notebooks, which nowadays are an incredibly handy tool.
* **[algorithmX](https://algrx.github.io)** provides all of the graph-rendering technology used under the hood of graphX. However, it is more complicated than pynode and has less useful features, with certain things needing to be implemented by third-parties (like graphX).
* **[root-11/graph-theory](https://github.com/root-11/graph-theory)** is one of the simplest implementations of graph thinking out there. And as been an excellent source for ways to implement stuff.

---

#### <3 Thanks {ignore}
Written by [@ehne](https://github.com/ehne) in 2020/21.  Give this project a star if you found it helpful. 