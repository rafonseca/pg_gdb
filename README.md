In Postgres codebase,`Node` and `List` structures are pervasive. Composing this structures we obtain, parse trees, plan trees, execution trees, etc.

The file [pg_gdb.py](./pg_gdb.py) is a gdb python extension that provides gdb printers for these structs. In particular, the printer will traverse the whole tree printing from top to bottom. The python code uses reflection to specialize printing for the different kind of nodes, so it should handle new kind of nodes from future versions as well

# Install

There is no install. We provide a package spec but it is only for development purposes.

# Usage

Inside a gdb session:
```
source PATH/TO/pg_gdb.py
```

In a given frame where `parsetree_list` is visible:
```
p parsetree_list
```
or
```
p --pretty -- parsetree_list
```

# Known issues
- GDB native identation does not follow custom printer identation

# See also
- [gdb-dashboard](https://github.com/cyrus-and/gdb-dashboard)

# Bugs
Please, open a issue to report any bug.
