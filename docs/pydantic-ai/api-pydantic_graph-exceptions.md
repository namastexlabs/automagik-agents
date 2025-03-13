# pydantic_graph.exceptions

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_graph.exceptions

```
pydantic_graph.exceptions
```

[](https://ai.pydantic.dev)

### GraphSetupError

Bases: TypeError

```
TypeError
```

[TypeError](https://docs.python.org/3/library/exceptions.html#TypeError)

Error caused by an incorrectly configured graph.

```
pydantic_graph/pydantic_graph/exceptions.py
```

```
1
2
3
4
5
6
7
8
9
```

```
class GraphSetupError(TypeError):
    """Error caused by an incorrectly configured graph."""

    message: str
    """Description of the mistake."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
```

```
class GraphSetupError(TypeError):
    """Error caused by an incorrectly configured graph."""

    message: str
    """Description of the mistake."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
```

#### message

instance-attribute

```
instance-attribute
```

```
message: str = message
```

```
message: str = message
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Description of the mistake.

### GraphRuntimeError

Bases: RuntimeError

```
RuntimeError
```

[RuntimeError](https://docs.python.org/3/library/exceptions.html#RuntimeError)

Error caused by an issue during graph execution.

```
pydantic_graph/pydantic_graph/exceptions.py
```

```
12
13
14
15
16
17
18
19
20
```

```
class GraphRuntimeError(RuntimeError):
    """Error caused by an issue during graph execution."""

    message: str
    """The error message."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
```

```
class GraphRuntimeError(RuntimeError):
    """Error caused by an issue during graph execution."""

    message: str
    """The error message."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
```

#### message

instance-attribute

```
instance-attribute
```

```
message: str = message
```

```
message: str = message
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The error message.

