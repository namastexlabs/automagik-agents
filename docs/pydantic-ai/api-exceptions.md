# pydantic_ai.exceptions

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.exceptions

```
pydantic_ai.exceptions
```

[](https://ai.pydantic.dev)

### ModelRetry

Bases: Exception

```
Exception
```

[Exception](https://docs.python.org/3/library/exceptions.html#Exception)

Exception raised when a tool function should be retried.

The agent will return the message to the model and ask it to try calling the function/tool again.

```
pydantic_ai_slim/pydantic_ai/exceptions.py
```

```
22
23
24
25
26
27
28
29
30
31
32
33
```

```
class ModelRetry(Exception):
    """Exception raised when a tool function should be retried.

    The agent will return the message to the model and ask it to try calling the function/tool again.
    """

    message: str
    """The message to return to the model."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
```

```
class ModelRetry(Exception):
    """Exception raised when a tool function should be retried.

    The agent will return the message to the model and ask it to try calling the function/tool again.
    """

    message: str
    """The message to return to the model."""

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

The message to return to the model.

### UserError

Bases: RuntimeError

```
RuntimeError
```

[RuntimeError](https://docs.python.org/3/library/exceptions.html#RuntimeError)

Error caused by a usage mistake by the application developer â You!

```
pydantic_ai_slim/pydantic_ai/exceptions.py
```

```
36
37
38
39
40
41
42
43
44
```

```
class UserError(RuntimeError):
    """Error caused by a usage mistake by the application developer â You!"""

    message: str
    """Description of the mistake."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
```

```
class UserError(RuntimeError):
    """Error caused by a usage mistake by the application developer â You!"""

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

### AgentRunError

Bases: RuntimeError

```
RuntimeError
```

[RuntimeError](https://docs.python.org/3/library/exceptions.html#RuntimeError)

Base class for errors occurring during an agent run.

```
pydantic_ai_slim/pydantic_ai/exceptions.py
```

```
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
```

```
class AgentRunError(RuntimeError):
    """Base class for errors occurring during an agent run."""

    message: str
    """The error message."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message
```

```
class AgentRunError(RuntimeError):
    """Base class for errors occurring during an agent run."""

    message: str
    """The error message."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message
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

### UsageLimitExceeded

Bases: AgentRunError

```
AgentRunError
```

[AgentRunError](https://ai.pydantic.dev#pydantic_ai.exceptions.AgentRunError)

Error raised when a Model's usage exceeds the specified limits.

```
pydantic_ai_slim/pydantic_ai/exceptions.py
```

```
61
62
```

```
class UsageLimitExceeded(AgentRunError):
    """Error raised when a Model's usage exceeds the specified limits."""
```

```
class UsageLimitExceeded(AgentRunError):
    """Error raised when a Model's usage exceeds the specified limits."""
```

### UnexpectedModelBehavior

Bases: AgentRunError

```
AgentRunError
```

[AgentRunError](https://ai.pydantic.dev#pydantic_ai.exceptions.AgentRunError)

Error caused by unexpected Model behavior, e.g. an unexpected response code.

```
pydantic_ai_slim/pydantic_ai/exceptions.py
```

```
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
```

```
class UnexpectedModelBehavior(AgentRunError):
    """Error caused by unexpected Model behavior, e.g. an unexpected response code."""

    message: str
    """Description of the unexpected behavior."""
    body: str | None
    """The body of the response, if available."""

    def __init__(self, message: str, body: str | None = None):
        self.message = message
        if body is None:
            self.body: str | None = None
        else:
            try:
                self.body = json.dumps(json.loads(body), indent=2)
            except ValueError:
                self.body = body
        super().__init__(message)

    def __str__(self) -> str:
        if self.body:
            return f'{self.message}, body:\n{self.body}'
        else:
            return self.message
```

```
class UnexpectedModelBehavior(AgentRunError):
    """Error caused by unexpected Model behavior, e.g. an unexpected response code."""

    message: str
    """Description of the unexpected behavior."""
    body: str | None
    """The body of the response, if available."""

    def __init__(self, message: str, body: str | None = None):
        self.message = message
        if body is None:
            self.body: str | None = None
        else:
            try:
                self.body = json.dumps(json.loads(body), indent=2)
            except ValueError:
                self.body = body
        super().__init__(message)

    def __str__(self) -> str:
        if self.body:
            return f'{self.message}, body:\n{self.body}'
        else:
            return self.message
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

Description of the unexpected behavior.

#### body

instance-attribute

```
instance-attribute
```

```
body: str | None = dumps(loads(body), indent=2)
```

```
body: str | None = dumps(loads(body), indent=2)
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[dumps](https://docs.python.org/3/library/json.html#json.dumps)

[loads](https://docs.python.org/3/library/json.html#json.loads)

The body of the response, if available.

### ModelHTTPError

Bases: AgentRunError

```
AgentRunError
```

[AgentRunError](https://ai.pydantic.dev#pydantic_ai.exceptions.AgentRunError)

Raised when an model provider response has a status code of 4xx or 5xx.

```
pydantic_ai_slim/pydantic_ai/exceptions.py
```

```
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
```

```
class ModelHTTPError(AgentRunError):
    """Raised when an model provider response has a status code of 4xx or 5xx."""

    status_code: int
    """The HTTP status code returned by the API."""

    model_name: str
    """The name of the model associated with the error."""

    body: object | None
    """The body of the response, if available."""

    message: str
    """The error message with the status code and response body, if available."""

    def __init__(self, status_code: int, model_name: str, body: object | None = None):
        self.status_code = status_code
        self.model_name = model_name
        self.body = body
        message = f'status_code: {status_code}, model_name: {model_name}, body: {body}'
        super().__init__(message)
```

```
class ModelHTTPError(AgentRunError):
    """Raised when an model provider response has a status code of 4xx or 5xx."""

    status_code: int
    """The HTTP status code returned by the API."""

    model_name: str
    """The name of the model associated with the error."""

    body: object | None
    """The body of the response, if available."""

    message: str
    """The error message with the status code and response body, if available."""

    def __init__(self, status_code: int, model_name: str, body: object | None = None):
        self.status_code = status_code
        self.model_name = model_name
        self.body = body
        message = f'status_code: {status_code}, model_name: {model_name}, body: {body}'
        super().__init__(message)
```

#### message

instance-attribute

```
instance-attribute
```

```
message: str
```

```
message: str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The error message with the status code and response body, if available.

#### status_code

instance-attribute

```
instance-attribute
```

```
status_code: int = status_code
```

```
status_code: int = status_code
```

[int](https://docs.python.org/3/library/functions.html#int)

The HTTP status code returned by the API.

#### model_name

instance-attribute

```
instance-attribute
```

```
model_name: str = model_name
```

```
model_name: str = model_name
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The name of the model associated with the error.

#### body

instance-attribute

```
instance-attribute
```

```
body: object | None = body
```

```
body: object | None = body
```

[object](https://docs.python.org/3/library/functions.html#object)

The body of the response, if available.

### FallbackExceptionGroup

Bases: ExceptionGroup

```
ExceptionGroup
```

A group of exceptions that can be raised when all fallback models fail.

```
pydantic_ai_slim/pydantic_ai/exceptions.py
```

```
114
115
```

```
class FallbackExceptionGroup(ExceptionGroup):
    """A group of exceptions that can be raised when all fallback models fail."""
```

```
class FallbackExceptionGroup(ExceptionGroup):
    """A group of exceptions that can be raised when all fallback models fail."""
```

