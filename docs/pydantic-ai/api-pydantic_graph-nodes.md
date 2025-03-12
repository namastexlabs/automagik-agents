# pydantic_graph.nodes

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_graph.nodes

```
pydantic_graph.nodes
```

[](https://ai.pydantic.dev)

### GraphRunContext

dataclass

```
dataclass
```

Bases: Generic[StateT, DepsT]

```
Generic[StateT, DepsT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

Context for a graph.

```
pydantic_graph/pydantic_graph/nodes.py
```

```
27
28
29
30
31
32
33
34
35
36
```

```
@dataclass
class GraphRunContext(Generic[StateT, DepsT]):
    """Context for a graph."""

    # TODO: Can we get rid of this struct and just pass both these things around..?

    state: StateT
    """The state of the graph."""
    deps: DepsT
    """Dependencies for the graph."""
```

```
@dataclass
class GraphRunContext(Generic[StateT, DepsT]):
    """Context for a graph."""

    # TODO: Can we get rid of this struct and just pass both these things around..?

    state: StateT
    """The state of the graph."""
    deps: DepsT
    """Dependencies for the graph."""
```

#### state

instance-attribute

```
instance-attribute
```

```
state: StateT
```

```
state: StateT
```

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The state of the graph.

#### deps

instance-attribute

```
instance-attribute
```

```
deps: DepsT
```

```
deps: DepsT
```

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

Dependencies for the graph.

### BaseNode

Bases: ABC, Generic[StateT, DepsT, NodeRunEndT]

```
ABC
```

[ABC](https://docs.python.org/3/library/abc.html#abc.ABC)

```
Generic[StateT, DepsT, NodeRunEndT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

[NodeRunEndT](https://ai.pydantic.dev#pydantic_graph.nodes.NodeRunEndT)

Base class for a node.

```
pydantic_graph/pydantic_graph/nodes.py
```

```
39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
```

```
class BaseNode(ABC, Generic[StateT, DepsT, NodeRunEndT]):
    """Base class for a node."""

    docstring_notes: ClassVar[bool] = False
    """Set to `True` to generate mermaid diagram notes from the class's docstring.

    While this can add valuable information to the diagram, it can make diagrams harder to view, hence
    it is disabled by default. You can also customise notes overriding the
    [`get_note`][pydantic_graph.nodes.BaseNode.get_note] method.
    """

    @abstractmethod
    async def run(self, ctx: GraphRunContext[StateT, DepsT]) -> BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]:
        """Run the node.

        This is an abstract method that must be implemented by subclasses.

        !!! note "Return types used at runtime"
            The return type of this method are read by `pydantic_graph` at runtime and used to define which
            nodes can be called next in the graph. This is displayed in [mermaid diagrams](mermaid.md)
            and enforced when running the graph.

        Args:
            ctx: The graph context.

        Returns:
            The next node to run or [`End`][pydantic_graph.nodes.End] to signal the end of the graph.
        """
        ...

    @classmethod
    @cache
    def get_id(cls) -> str:
        """Get the ID of the node."""
        return cls.__name__

    @classmethod
    def get_note(cls) -> str | None:
        """Get a note about the node to render on mermaid charts.

        By default, this returns a note only if [`docstring_notes`][pydantic_graph.nodes.BaseNode.docstring_notes]
        is `True`. You can override this method to customise the node notes.
        """
        if not cls.docstring_notes:
            return None
        docstring = cls.__doc__
        # dataclasses get an automatic docstring which is just their signature, we don't want that
        if docstring and is_dataclass(cls) and docstring.startswith(f'{cls.__name__}('):
            docstring = None
        if docstring:
            # remove indentation from docstring
            import inspect

            docstring = inspect.cleandoc(docstring)
        return docstring

    @classmethod
    def get_node_def(cls, local_ns: dict[str, Any] | None) -> NodeDef[StateT, DepsT, NodeRunEndT]:
        """Get the node definition."""
        type_hints = get_type_hints(cls.run, localns=local_ns, include_extras=True)
        try:
            return_hint = type_hints['return']
        except KeyError as e:
            raise exceptions.GraphSetupError(f'Node {cls} is missing a return type hint on its `run` method') from e

        next_node_edges: dict[str, Edge] = {}
        end_edge: Edge | None = None
        returns_base_node: bool = False
        for return_type in _utils.get_union_args(return_hint):
            return_type, annotations = _utils.unpack_annotated(return_type)
            edge = next((a for a in annotations if isinstance(a, Edge)), Edge(None))
            return_type_origin = get_origin(return_type) or return_type
            if return_type_origin is End:
                end_edge = edge
            elif return_type_origin is BaseNode:
                # TODO: Should we disallow this?
                returns_base_node = True
            elif issubclass(return_type_origin, BaseNode):
                next_node_edges[return_type.get_id()] = edge
            else:
                raise exceptions.GraphSetupError(f'Invalid return type: {return_type}')

        return NodeDef(
            cls,
            cls.get_id(),
            cls.get_note(),
            next_node_edges,
            end_edge,
            returns_base_node,
        )
```

```
class BaseNode(ABC, Generic[StateT, DepsT, NodeRunEndT]):
    """Base class for a node."""

    docstring_notes: ClassVar[bool] = False
    """Set to `True` to generate mermaid diagram notes from the class's docstring.

    While this can add valuable information to the diagram, it can make diagrams harder to view, hence
    it is disabled by default. You can also customise notes overriding the
    [`get_note`][pydantic_graph.nodes.BaseNode.get_note] method.
    """

    @abstractmethod
    async def run(self, ctx: GraphRunContext[StateT, DepsT]) -> BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]:
        """Run the node.

        This is an abstract method that must be implemented by subclasses.

        !!! note "Return types used at runtime"
            The return type of this method are read by `pydantic_graph` at runtime and used to define which
            nodes can be called next in the graph. This is displayed in [mermaid diagrams](mermaid.md)
            and enforced when running the graph.

        Args:
            ctx: The graph context.

        Returns:
            The next node to run or [`End`][pydantic_graph.nodes.End] to signal the end of the graph.
        """
        ...

    @classmethod
    @cache
    def get_id(cls) -> str:
        """Get the ID of the node."""
        return cls.__name__

    @classmethod
    def get_note(cls) -> str | None:
        """Get a note about the node to render on mermaid charts.

        By default, this returns a note only if [`docstring_notes`][pydantic_graph.nodes.BaseNode.docstring_notes]
        is `True`. You can override this method to customise the node notes.
        """
        if not cls.docstring_notes:
            return None
        docstring = cls.__doc__
        # dataclasses get an automatic docstring which is just their signature, we don't want that
        if docstring and is_dataclass(cls) and docstring.startswith(f'{cls.__name__}('):
            docstring = None
        if docstring:
            # remove indentation from docstring
            import inspect

            docstring = inspect.cleandoc(docstring)
        return docstring

    @classmethod
    def get_node_def(cls, local_ns: dict[str, Any] | None) -> NodeDef[StateT, DepsT, NodeRunEndT]:
        """Get the node definition."""
        type_hints = get_type_hints(cls.run, localns=local_ns, include_extras=True)
        try:
            return_hint = type_hints['return']
        except KeyError as e:
            raise exceptions.GraphSetupError(f'Node {cls} is missing a return type hint on its `run` method') from e

        next_node_edges: dict[str, Edge] = {}
        end_edge: Edge | None = None
        returns_base_node: bool = False
        for return_type in _utils.get_union_args(return_hint):
            return_type, annotations = _utils.unpack_annotated(return_type)
            edge = next((a for a in annotations if isinstance(a, Edge)), Edge(None))
            return_type_origin = get_origin(return_type) or return_type
            if return_type_origin is End:
                end_edge = edge
            elif return_type_origin is BaseNode:
                # TODO: Should we disallow this?
                returns_base_node = True
            elif issubclass(return_type_origin, BaseNode):
                next_node_edges[return_type.get_id()] = edge
            else:
                raise exceptions.GraphSetupError(f'Invalid return type: {return_type}')

        return NodeDef(
            cls,
            cls.get_id(),
            cls.get_note(),
            next_node_edges,
            end_edge,
            returns_base_node,
        )
```

#### docstring_notes

class-attribute

```
class-attribute
```

```
docstring_notes: bool = False
```

```
docstring_notes: bool = False
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Set to True to generate mermaid diagram notes from the class's docstring.

```
True
```

While this can add valuable information to the diagram, it can make diagrams harder to view, hence
it is disabled by default. You can also customise notes overriding the
get_note method.

```
get_note
```

#### run

abstractmethod
async

```
abstractmethod
```

```
async
```

```
run(
    ctx: GraphRunContext[StateT, DepsT],
) -> BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]
```

```
run(
    ctx: GraphRunContext[StateT, DepsT],
) -> BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]
```

[GraphRunContext](https://ai.pydantic.dev#pydantic_graph.nodes.GraphRunContext)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

[BaseNode](https://ai.pydantic.dev#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

[End](https://ai.pydantic.dev#pydantic_graph.nodes.End)

[NodeRunEndT](https://ai.pydantic.dev#pydantic_graph.nodes.NodeRunEndT)

Run the node.

This is an abstract method that must be implemented by subclasses.

Return types used at runtime

The return type of this method are read by pydantic_graph at runtime and used to define which
nodes can be called next in the graph. This is displayed in mermaid diagrams
and enforced when running the graph.

```
pydantic_graph
```

Parameters:

```
ctx
```

```
GraphRunContext[StateT, DepsT]
```

[GraphRunContext](https://ai.pydantic.dev#pydantic_graph.nodes.GraphRunContext)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

The graph context.

Returns:

```
BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]
```

[BaseNode](https://ai.pydantic.dev#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

[End](https://ai.pydantic.dev#pydantic_graph.nodes.End)

[NodeRunEndT](https://ai.pydantic.dev#pydantic_graph.nodes.NodeRunEndT)

The next node to run or End to signal the end of the graph.

```
End
```

```
pydantic_graph/pydantic_graph/nodes.py
```

```
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
```

```
@abstractmethod
async def run(self, ctx: GraphRunContext[StateT, DepsT]) -> BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]:
    """Run the node.

    This is an abstract method that must be implemented by subclasses.

    !!! note "Return types used at runtime"
        The return type of this method are read by `pydantic_graph` at runtime and used to define which
        nodes can be called next in the graph. This is displayed in [mermaid diagrams](mermaid.md)
        and enforced when running the graph.

    Args:
        ctx: The graph context.

    Returns:
        The next node to run or [`End`][pydantic_graph.nodes.End] to signal the end of the graph.
    """
    ...
```

```
@abstractmethod
async def run(self, ctx: GraphRunContext[StateT, DepsT]) -> BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]:
    """Run the node.

    This is an abstract method that must be implemented by subclasses.

    !!! note "Return types used at runtime"
        The return type of this method are read by `pydantic_graph` at runtime and used to define which
        nodes can be called next in the graph. This is displayed in [mermaid diagrams](mermaid.md)
        and enforced when running the graph.

    Args:
        ctx: The graph context.

    Returns:
        The next node to run or [`End`][pydantic_graph.nodes.End] to signal the end of the graph.
    """
    ...
```

#### get_id

cached
classmethod

```
cached
```

```
classmethod
```

```
get_id() -> str
```

```
get_id() -> str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Get the ID of the node.

```
pydantic_graph/pydantic_graph/nodes.py
```

```
69
70
71
72
73
```

```
@classmethod
@cache
def get_id(cls) -> str:
    """Get the ID of the node."""
    return cls.__name__
```

```
@classmethod
@cache
def get_id(cls) -> str:
    """Get the ID of the node."""
    return cls.__name__
```

#### get_note

classmethod

```
classmethod
```

```
get_note() -> str | None
```

```
get_note() -> str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Get a note about the node to render on mermaid charts.

By default, this returns a note only if docstring_notes
is True. You can override this method to customise the node notes.

```
docstring_notes
```

```
True
```

```
pydantic_graph/pydantic_graph/nodes.py
```

```
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
```

```
@classmethod
def get_note(cls) -> str | None:
    """Get a note about the node to render on mermaid charts.

    By default, this returns a note only if [`docstring_notes`][pydantic_graph.nodes.BaseNode.docstring_notes]
    is `True`. You can override this method to customise the node notes.
    """
    if not cls.docstring_notes:
        return None
    docstring = cls.__doc__
    # dataclasses get an automatic docstring which is just their signature, we don't want that
    if docstring and is_dataclass(cls) and docstring.startswith(f'{cls.__name__}('):
        docstring = None
    if docstring:
        # remove indentation from docstring
        import inspect

        docstring = inspect.cleandoc(docstring)
    return docstring
```

```
@classmethod
def get_note(cls) -> str | None:
    """Get a note about the node to render on mermaid charts.

    By default, this returns a note only if [`docstring_notes`][pydantic_graph.nodes.BaseNode.docstring_notes]
    is `True`. You can override this method to customise the node notes.
    """
    if not cls.docstring_notes:
        return None
    docstring = cls.__doc__
    # dataclasses get an automatic docstring which is just their signature, we don't want that
    if docstring and is_dataclass(cls) and docstring.startswith(f'{cls.__name__}('):
        docstring = None
    if docstring:
        # remove indentation from docstring
        import inspect

        docstring = inspect.cleandoc(docstring)
    return docstring
```

#### get_node_def

classmethod

```
classmethod
```

```
get_node_def(
    local_ns: dict[str, Any] | None,
) -> NodeDef[StateT, DepsT, NodeRunEndT]
```

```
get_node_def(
    local_ns: dict[str, Any] | None,
) -> NodeDef[StateT, DepsT, NodeRunEndT]
```

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev#pydantic_graph.nodes.DepsT)

[NodeRunEndT](https://ai.pydantic.dev#pydantic_graph.nodes.NodeRunEndT)

Get the node definition.

```
pydantic_graph/pydantic_graph/nodes.py
```

```
95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
```

```
@classmethod
def get_node_def(cls, local_ns: dict[str, Any] | None) -> NodeDef[StateT, DepsT, NodeRunEndT]:
    """Get the node definition."""
    type_hints = get_type_hints(cls.run, localns=local_ns, include_extras=True)
    try:
        return_hint = type_hints['return']
    except KeyError as e:
        raise exceptions.GraphSetupError(f'Node {cls} is missing a return type hint on its `run` method') from e

    next_node_edges: dict[str, Edge] = {}
    end_edge: Edge | None = None
    returns_base_node: bool = False
    for return_type in _utils.get_union_args(return_hint):
        return_type, annotations = _utils.unpack_annotated(return_type)
        edge = next((a for a in annotations if isinstance(a, Edge)), Edge(None))
        return_type_origin = get_origin(return_type) or return_type
        if return_type_origin is End:
            end_edge = edge
        elif return_type_origin is BaseNode:
            # TODO: Should we disallow this?
            returns_base_node = True
        elif issubclass(return_type_origin, BaseNode):
            next_node_edges[return_type.get_id()] = edge
        else:
            raise exceptions.GraphSetupError(f'Invalid return type: {return_type}')

    return NodeDef(
        cls,
        cls.get_id(),
        cls.get_note(),
        next_node_edges,
        end_edge,
        returns_base_node,
    )
```

```
@classmethod
def get_node_def(cls, local_ns: dict[str, Any] | None) -> NodeDef[StateT, DepsT, NodeRunEndT]:
    """Get the node definition."""
    type_hints = get_type_hints(cls.run, localns=local_ns, include_extras=True)
    try:
        return_hint = type_hints['return']
    except KeyError as e:
        raise exceptions.GraphSetupError(f'Node {cls} is missing a return type hint on its `run` method') from e

    next_node_edges: dict[str, Edge] = {}
    end_edge: Edge | None = None
    returns_base_node: bool = False
    for return_type in _utils.get_union_args(return_hint):
        return_type, annotations = _utils.unpack_annotated(return_type)
        edge = next((a for a in annotations if isinstance(a, Edge)), Edge(None))
        return_type_origin = get_origin(return_type) or return_type
        if return_type_origin is End:
            end_edge = edge
        elif return_type_origin is BaseNode:
            # TODO: Should we disallow this?
            returns_base_node = True
        elif issubclass(return_type_origin, BaseNode):
            next_node_edges[return_type.get_id()] = edge
        else:
            raise exceptions.GraphSetupError(f'Invalid return type: {return_type}')

    return NodeDef(
        cls,
        cls.get_id(),
        cls.get_note(),
        next_node_edges,
        end_edge,
        returns_base_node,
    )
```

### End

dataclass

```
dataclass
```

Bases: Generic[RunEndT]

```
Generic[RunEndT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[RunEndT](https://ai.pydantic.dev#pydantic_graph.nodes.RunEndT)

Type to return from a node to signal the end of the graph.

```
pydantic_graph/pydantic_graph/nodes.py
```

```
131
132
133
134
135
136
```

```
@dataclass
class End(Generic[RunEndT]):
    """Type to return from a node to signal the end of the graph."""

    data: RunEndT
    """Data to return from the graph."""
```

```
@dataclass
class End(Generic[RunEndT]):
    """Type to return from a node to signal the end of the graph."""

    data: RunEndT
    """Data to return from the graph."""
```

#### data

instance-attribute

```
instance-attribute
```

```
data: RunEndT
```

```
data: RunEndT
```

[RunEndT](https://ai.pydantic.dev#pydantic_graph.nodes.RunEndT)

Data to return from the graph.

### Edge

dataclass

```
dataclass
```

Annotation to apply a label to an edge in a graph.

```
pydantic_graph/pydantic_graph/nodes.py
```

```
139
140
141
142
143
144
```

```
@dataclass
class Edge:
    """Annotation to apply a label to an edge in a graph."""

    label: str | None
    """Label for the edge."""
```

```
@dataclass
class Edge:
    """Annotation to apply a label to an edge in a graph."""

    label: str | None
    """Label for the edge."""
```

#### label

instance-attribute

```
instance-attribute
```

```
label: str | None
```

```
label: str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Label for the edge.

### DepsT

module-attribute

```
module-attribute
```

```
DepsT = TypeVar('DepsT', default=None, contravariant=True)
```

```
DepsT = TypeVar('DepsT', default=None, contravariant=True)
```

Type variable for the dependencies of a graph and node.

### RunEndT

module-attribute

```
module-attribute
```

```
RunEndT = TypeVar('RunEndT', covariant=True, default=None)
```

```
RunEndT = TypeVar('RunEndT', covariant=True, default=None)
```

Covariant type variable for the return type of a graph run.

```
run
```

### NodeRunEndT

module-attribute

```
module-attribute
```

```
NodeRunEndT = TypeVar(
    "NodeRunEndT", covariant=True, default=Never
)
```

```
NodeRunEndT = TypeVar(
    "NodeRunEndT", covariant=True, default=Never
)
```

[Never](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Never)

Covariant type variable for the return type of a node run.

```
run
```

