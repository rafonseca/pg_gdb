from gdb.printing import register_pretty_printer, RegexpCollectionPrettyPrinter
from gdb import Value, Type, ValuePrinter, pretty_printers, lookup_type


tNode = lookup_type("Node")
tList = lookup_type("List")
tNodeTag = lookup_type("NodeTag")

IDENT_SPACES = 2


class IdentPrinter(ValuePrinter):
    ident = 0
    
class NodePrinter(IdentPrinter):
    def __init__(self, val: Value,label="NODE*") -> None:
        self._val = val
        self._label = label
        
    def to_string(self):
        return self._label

    def children(self):
        def _iter():
            IdentPrinter.ident += IDENT_SPACES
            for field in self._val.type.fields():
                assert field.name is not None
                yield  " "*IdentPrinter.ident + field.name, self._val[field.name]
            IdentPrinter.ident -= IDENT_SPACES

        return _iter()


class ListPrinter(IdentPrinter):
    def __init__(self, val: Value) -> None:
        self._val = val

    def to_string(self):
        return f"LIST"

    def children(self):
        def _iter():
            IdentPrinter.ident += IDENT_SPACES
            for i in range(self._val["length"]):
                try:
                    yield " "*IdentPrinter.ident + f"[{i}]", (
                        self._val["elements"][i]["ptr_value"]
                        .cast(tNode.pointer())
                        .format_string()
                    )
                except:
                    continue
            IdentPrinter.ident -= IDENT_SPACES
        return _iter()


def dispatcher(val: Value):
    if val.type in [lookup_type(t) for t in ["Plan","Expr","Integer"]]:
        return NodePrinter(val,label="NODE")
    try:
        val = val.dereference()
    except:
        # only dispatch pointer fields. non-pointer fields are handled
        # by other printers
        return

    if val.type == tNodeTag:
        # the dispatcher will be invoked in format_string below. we
        # should early return None, when val is a NodeTag. Otherwise
        # we'll incur in infinite recursion.
        return

    try:
        node_type = val.cast(tNode)["type"].format_string()
        if node_type in ["T_Invalid","T_AllocSetContext"]:
            return 
    except:
        return

    if node_type in ["T_List"]:  # TODO: handle other types of list
        return ListPrinter(val.cast(tList))
    if node_type.startswith("T_"):
        val = val.cast(lookup_type(node_type[2:]))
        return NodePrinter(val)


pretty_printers.insert(0, dispatcher)
