# pydantic_ai.usage

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.usage

```
pydantic_ai.usage
```

[](https://ai.pydantic.dev)

### Usage

dataclass

```
dataclass
```

LLM usage associated with a request or run.

Responsibility for calculating usage is on the model; PydanticAI simply sums the usage information across requests.

You'll need to look up the documentation of the model you're using to convert usage to monetary costs.

```
pydantic_ai_slim/pydantic_ai/usage.py
```

```
11
12
13
14
15
16
17
18
19
20
21
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
34
35
36
37
38
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
```

```
@dataclass
class Usage:
    """LLM usage associated with a request or run.

    Responsibility for calculating usage is on the model; PydanticAI simply sums the usage information across requests.

    You'll need to look up the documentation of the model you're using to convert usage to monetary costs.
    """

    requests: int = 0
    """Number of requests made to the LLM API."""
    request_tokens: int | None = None
    """Tokens used in processing requests."""
    response_tokens: int | None = None
    """Tokens used in generating responses."""
    total_tokens: int | None = None
    """Total tokens used in the whole run, should generally be equal to `request_tokens + response_tokens`."""
    details: dict[str, int] | None = None
    """Any extra details returned by the model."""

    def incr(self, incr_usage: Usage, *, requests: int = 0) -> None:
        """Increment the usage in place.

        Args:
            incr_usage: The usage to increment by.
            requests: The number of requests to increment by in addition to `incr_usage.requests`.
        """
        self.requests += requests
        for f in 'requests', 'request_tokens', 'response_tokens', 'total_tokens':
            self_value = getattr(self, f)
            other_value = getattr(incr_usage, f)
            if self_value is not None or other_value is not None:
                setattr(self, f, (self_value or 0) + (other_value or 0))

        if incr_usage.details:
            self.details = self.details or {}
            for key, value in incr_usage.details.items():
                self.details[key] = self.details.get(key, 0) + value

    def __add__(self, other: Usage) -> Usage:
        """Add two Usages together.

        This is provided so it's trivial to sum usage information from multiple requests and runs.
        """
        new_usage = copy(self)
        new_usage.incr(other)
        return new_usage

    def opentelemetry_attributes(self) -> dict[str, int]:
        """Get the token limits as OpenTelemetry attributes."""
        result = {
            'gen_ai.usage.input_tokens': self.request_tokens,
            'gen_ai.usage.output_tokens': self.response_tokens,
        }
        for key, value in (self.details or {}).items():
            result[f'gen_ai.usage.details.{key}'] = value
        return {k: v for k, v in result.items() if v is not None}
```

```
@dataclass
class Usage:
    """LLM usage associated with a request or run.

    Responsibility for calculating usage is on the model; PydanticAI simply sums the usage information across requests.

    You'll need to look up the documentation of the model you're using to convert usage to monetary costs.
    """

    requests: int = 0
    """Number of requests made to the LLM API."""
    request_tokens: int | None = None
    """Tokens used in processing requests."""
    response_tokens: int | None = None
    """Tokens used in generating responses."""
    total_tokens: int | None = None
    """Total tokens used in the whole run, should generally be equal to `request_tokens + response_tokens`."""
    details: dict[str, int] | None = None
    """Any extra details returned by the model."""

    def incr(self, incr_usage: Usage, *, requests: int = 0) -> None:
        """Increment the usage in place.

        Args:
            incr_usage: The usage to increment by.
            requests: The number of requests to increment by in addition to `incr_usage.requests`.
        """
        self.requests += requests
        for f in 'requests', 'request_tokens', 'response_tokens', 'total_tokens':
            self_value = getattr(self, f)
            other_value = getattr(incr_usage, f)
            if self_value is not None or other_value is not None:
                setattr(self, f, (self_value or 0) + (other_value or 0))

        if incr_usage.details:
            self.details = self.details or {}
            for key, value in incr_usage.details.items():
                self.details[key] = self.details.get(key, 0) + value

    def __add__(self, other: Usage) -> Usage:
        """Add two Usages together.

        This is provided so it's trivial to sum usage information from multiple requests and runs.
        """
        new_usage = copy(self)
        new_usage.incr(other)
        return new_usage

    def opentelemetry_attributes(self) -> dict[str, int]:
        """Get the token limits as OpenTelemetry attributes."""
        result = {
            'gen_ai.usage.input_tokens': self.request_tokens,
            'gen_ai.usage.output_tokens': self.response_tokens,
        }
        for key, value in (self.details or {}).items():
            result[f'gen_ai.usage.details.{key}'] = value
        return {k: v for k, v in result.items() if v is not None}
```

#### requests

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
requests: int = 0
```

```
requests: int = 0
```

[int](https://docs.python.org/3/library/functions.html#int)

Number of requests made to the LLM API.

#### request_tokens

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
request_tokens: int | None = None
```

```
request_tokens: int | None = None
```

[int](https://docs.python.org/3/library/functions.html#int)

Tokens used in processing requests.

#### response_tokens

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
response_tokens: int | None = None
```

```
response_tokens: int | None = None
```

[int](https://docs.python.org/3/library/functions.html#int)

Tokens used in generating responses.

#### total_tokens

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
total_tokens: int | None = None
```

```
total_tokens: int | None = None
```

[int](https://docs.python.org/3/library/functions.html#int)

Total tokens used in the whole run, should generally be equal to request_tokens + response_tokens.

```
request_tokens + response_tokens
```

#### details

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
details: dict[str, int] | None = None
```

```
details: dict[str, int] | None = None
```

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[int](https://docs.python.org/3/library/functions.html#int)

Any extra details returned by the model.

#### incr

```
incr(incr_usage: Usage, *, requests: int = 0) -> None
```

```
incr(incr_usage: Usage, *, requests: int = 0) -> None
```

[Usage](https://ai.pydantic.dev#pydantic_ai.usage.Usage)

[int](https://docs.python.org/3/library/functions.html#int)

Increment the usage in place.

Parameters:

```
incr_usage
```

```
Usage
```

[Usage](https://ai.pydantic.dev#pydantic_ai.usage.Usage)

The usage to increment by.

```
requests
```

```
int
```

[int](https://docs.python.org/3/library/functions.html#int)

The number of requests to increment by in addition to incr_usage.requests.

```
incr_usage.requests
```

```
0
```

```
pydantic_ai_slim/pydantic_ai/usage.py
```

```
31
32
33
34
35
36
37
38
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
```

```
def incr(self, incr_usage: Usage, *, requests: int = 0) -> None:
    """Increment the usage in place.

    Args:
        incr_usage: The usage to increment by.
        requests: The number of requests to increment by in addition to `incr_usage.requests`.
    """
    self.requests += requests
    for f in 'requests', 'request_tokens', 'response_tokens', 'total_tokens':
        self_value = getattr(self, f)
        other_value = getattr(incr_usage, f)
        if self_value is not None or other_value is not None:
            setattr(self, f, (self_value or 0) + (other_value or 0))

    if incr_usage.details:
        self.details = self.details or {}
        for key, value in incr_usage.details.items():
            self.details[key] = self.details.get(key, 0) + value
```

```
def incr(self, incr_usage: Usage, *, requests: int = 0) -> None:
    """Increment the usage in place.

    Args:
        incr_usage: The usage to increment by.
        requests: The number of requests to increment by in addition to `incr_usage.requests`.
    """
    self.requests += requests
    for f in 'requests', 'request_tokens', 'response_tokens', 'total_tokens':
        self_value = getattr(self, f)
        other_value = getattr(incr_usage, f)
        if self_value is not None or other_value is not None:
            setattr(self, f, (self_value or 0) + (other_value or 0))

    if incr_usage.details:
        self.details = self.details or {}
        for key, value in incr_usage.details.items():
            self.details[key] = self.details.get(key, 0) + value
```

#### __add__

```
__add__(other: Usage) -> Usage
```

```
__add__(other: Usage) -> Usage
```

[Usage](https://ai.pydantic.dev#pydantic_ai.usage.Usage)

[Usage](https://ai.pydantic.dev#pydantic_ai.usage.Usage)

Add two Usages together.

This is provided so it's trivial to sum usage information from multiple requests and runs.

```
pydantic_ai_slim/pydantic_ai/usage.py
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
```

```
def __add__(self, other: Usage) -> Usage:
    """Add two Usages together.

    This is provided so it's trivial to sum usage information from multiple requests and runs.
    """
    new_usage = copy(self)
    new_usage.incr(other)
    return new_usage
```

```
def __add__(self, other: Usage) -> Usage:
    """Add two Usages together.

    This is provided so it's trivial to sum usage information from multiple requests and runs.
    """
    new_usage = copy(self)
    new_usage.incr(other)
    return new_usage
```

#### opentelemetry_attributes

```
opentelemetry_attributes() -> dict[str, int]
```

```
opentelemetry_attributes() -> dict[str, int]
```

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[int](https://docs.python.org/3/library/functions.html#int)

Get the token limits as OpenTelemetry attributes.

```
pydantic_ai_slim/pydantic_ai/usage.py
```

```
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
def opentelemetry_attributes(self) -> dict[str, int]:
    """Get the token limits as OpenTelemetry attributes."""
    result = {
        'gen_ai.usage.input_tokens': self.request_tokens,
        'gen_ai.usage.output_tokens': self.response_tokens,
    }
    for key, value in (self.details or {}).items():
        result[f'gen_ai.usage.details.{key}'] = value
    return {k: v for k, v in result.items() if v is not None}
```

```
def opentelemetry_attributes(self) -> dict[str, int]:
    """Get the token limits as OpenTelemetry attributes."""
    result = {
        'gen_ai.usage.input_tokens': self.request_tokens,
        'gen_ai.usage.output_tokens': self.response_tokens,
    }
    for key, value in (self.details or {}).items():
        result[f'gen_ai.usage.details.{key}'] = value
    return {k: v for k, v in result.items() if v is not None}
```

### UsageLimits

dataclass

```
dataclass
```

Limits on model usage.

The request count is tracked by pydantic_ai, and the request limit is checked before each request to the model.
Token counts are provided in responses from the model, and the token limits are checked after each response.

Each of the limits can be set to None to disable that limit.

```
None
```

```
pydantic_ai_slim/pydantic_ai/usage.py
```

```
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
```

```
@dataclass
class UsageLimits:
    """Limits on model usage.

    The request count is tracked by pydantic_ai, and the request limit is checked before each request to the model.
    Token counts are provided in responses from the model, and the token limits are checked after each response.

    Each of the limits can be set to `None` to disable that limit.
    """

    request_limit: int | None = 50
    """The maximum number of requests allowed to the model."""
    request_tokens_limit: int | None = None
    """The maximum number of tokens allowed in requests to the model."""
    response_tokens_limit: int | None = None
    """The maximum number of tokens allowed in responses from the model."""
    total_tokens_limit: int | None = None
    """The maximum number of tokens allowed in requests and responses combined."""

    def has_token_limits(self) -> bool:
        """Returns `True` if this instance places any limits on token counts.

        If this returns `False`, the `check_tokens` method will never raise an error.

        This is useful because if we have token limits, we need to check them after receiving each streamed message.
        If there are no limits, we can skip that processing in the streaming response iterator.
        """
        return any(
            limit is not None
            for limit in (self.request_tokens_limit, self.response_tokens_limit, self.total_tokens_limit)
        )

    def check_before_request(self, usage: Usage) -> None:
        """Raises a `UsageLimitExceeded` exception if the next request would exceed the request_limit."""
        request_limit = self.request_limit
        if request_limit is not None and usage.requests >= request_limit:
            raise UsageLimitExceeded(f'The next request would exceed the request_limit of {request_limit}')

    def check_tokens(self, usage: Usage) -> None:
        """Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token limits."""
        request_tokens = usage.request_tokens or 0
        if self.request_tokens_limit is not None and request_tokens > self.request_tokens_limit:
            raise UsageLimitExceeded(
                f'Exceeded the request_tokens_limit of {self.request_tokens_limit} ({request_tokens=})'
            )

        response_tokens = usage.response_tokens or 0
        if self.response_tokens_limit is not None and response_tokens > self.response_tokens_limit:
            raise UsageLimitExceeded(
                f'Exceeded the response_tokens_limit of {self.response_tokens_limit} ({response_tokens=})'
            )

        total_tokens = usage.total_tokens or 0
        if self.total_tokens_limit is not None and total_tokens > self.total_tokens_limit:
            raise UsageLimitExceeded(f'Exceeded the total_tokens_limit of {self.total_tokens_limit} ({total_tokens=})')
```

```
@dataclass
class UsageLimits:
    """Limits on model usage.

    The request count is tracked by pydantic_ai, and the request limit is checked before each request to the model.
    Token counts are provided in responses from the model, and the token limits are checked after each response.

    Each of the limits can be set to `None` to disable that limit.
    """

    request_limit: int | None = 50
    """The maximum number of requests allowed to the model."""
    request_tokens_limit: int | None = None
    """The maximum number of tokens allowed in requests to the model."""
    response_tokens_limit: int | None = None
    """The maximum number of tokens allowed in responses from the model."""
    total_tokens_limit: int | None = None
    """The maximum number of tokens allowed in requests and responses combined."""

    def has_token_limits(self) -> bool:
        """Returns `True` if this instance places any limits on token counts.

        If this returns `False`, the `check_tokens` method will never raise an error.

        This is useful because if we have token limits, we need to check them after receiving each streamed message.
        If there are no limits, we can skip that processing in the streaming response iterator.
        """
        return any(
            limit is not None
            for limit in (self.request_tokens_limit, self.response_tokens_limit, self.total_tokens_limit)
        )

    def check_before_request(self, usage: Usage) -> None:
        """Raises a `UsageLimitExceeded` exception if the next request would exceed the request_limit."""
        request_limit = self.request_limit
        if request_limit is not None and usage.requests >= request_limit:
            raise UsageLimitExceeded(f'The next request would exceed the request_limit of {request_limit}')

    def check_tokens(self, usage: Usage) -> None:
        """Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token limits."""
        request_tokens = usage.request_tokens or 0
        if self.request_tokens_limit is not None and request_tokens > self.request_tokens_limit:
            raise UsageLimitExceeded(
                f'Exceeded the request_tokens_limit of {self.request_tokens_limit} ({request_tokens=})'
            )

        response_tokens = usage.response_tokens or 0
        if self.response_tokens_limit is not None and response_tokens > self.response_tokens_limit:
            raise UsageLimitExceeded(
                f'Exceeded the response_tokens_limit of {self.response_tokens_limit} ({response_tokens=})'
            )

        total_tokens = usage.total_tokens or 0
        if self.total_tokens_limit is not None and total_tokens > self.total_tokens_limit:
            raise UsageLimitExceeded(f'Exceeded the total_tokens_limit of {self.total_tokens_limit} ({total_tokens=})')
```

#### request_limit

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
request_limit: int | None = 50
```

```
request_limit: int | None = 50
```

[int](https://docs.python.org/3/library/functions.html#int)

The maximum number of requests allowed to the model.

#### request_tokens_limit

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
request_tokens_limit: int | None = None
```

```
request_tokens_limit: int | None = None
```

[int](https://docs.python.org/3/library/functions.html#int)

The maximum number of tokens allowed in requests to the model.

#### response_tokens_limit

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
response_tokens_limit: int | None = None
```

```
response_tokens_limit: int | None = None
```

[int](https://docs.python.org/3/library/functions.html#int)

The maximum number of tokens allowed in responses from the model.

#### total_tokens_limit

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
total_tokens_limit: int | None = None
```

```
total_tokens_limit: int | None = None
```

[int](https://docs.python.org/3/library/functions.html#int)

The maximum number of tokens allowed in requests and responses combined.

#### has_token_limits

```
has_token_limits() -> bool
```

```
has_token_limits() -> bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Returns True if this instance places any limits on token counts.

```
True
```

If this returns False, the check_tokens method will never raise an error.

```
False
```

```
check_tokens
```

This is useful because if we have token limits, we need to check them after receiving each streamed message.
If there are no limits, we can skip that processing in the streaming response iterator.

```
pydantic_ai_slim/pydantic_ai/usage.py
```

```
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
```

```
def has_token_limits(self) -> bool:
    """Returns `True` if this instance places any limits on token counts.

    If this returns `False`, the `check_tokens` method will never raise an error.

    This is useful because if we have token limits, we need to check them after receiving each streamed message.
    If there are no limits, we can skip that processing in the streaming response iterator.
    """
    return any(
        limit is not None
        for limit in (self.request_tokens_limit, self.response_tokens_limit, self.total_tokens_limit)
    )
```

```
def has_token_limits(self) -> bool:
    """Returns `True` if this instance places any limits on token counts.

    If this returns `False`, the `check_tokens` method will never raise an error.

    This is useful because if we have token limits, we need to check them after receiving each streamed message.
    If there are no limits, we can skip that processing in the streaming response iterator.
    """
    return any(
        limit is not None
        for limit in (self.request_tokens_limit, self.response_tokens_limit, self.total_tokens_limit)
    )
```

#### check_before_request

```
check_before_request(usage: Usage) -> None
```

```
check_before_request(usage: Usage) -> None
```

[Usage](https://ai.pydantic.dev#pydantic_ai.usage.Usage)

Raises a UsageLimitExceeded exception if the next request would exceed the request_limit.

```
UsageLimitExceeded
```

```
pydantic_ai_slim/pydantic_ai/usage.py
```

```
102
103
104
105
106
```

```
def check_before_request(self, usage: Usage) -> None:
    """Raises a `UsageLimitExceeded` exception if the next request would exceed the request_limit."""
    request_limit = self.request_limit
    if request_limit is not None and usage.requests >= request_limit:
        raise UsageLimitExceeded(f'The next request would exceed the request_limit of {request_limit}')
```

```
def check_before_request(self, usage: Usage) -> None:
    """Raises a `UsageLimitExceeded` exception if the next request would exceed the request_limit."""
    request_limit = self.request_limit
    if request_limit is not None and usage.requests >= request_limit:
        raise UsageLimitExceeded(f'The next request would exceed the request_limit of {request_limit}')
```

#### check_tokens

```
check_tokens(usage: Usage) -> None
```

```
check_tokens(usage: Usage) -> None
```

[Usage](https://ai.pydantic.dev#pydantic_ai.usage.Usage)

Raises a UsageLimitExceeded exception if the usage exceeds any of the token limits.

```
UsageLimitExceeded
```

```
pydantic_ai_slim/pydantic_ai/usage.py
```

```
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
```

```
def check_tokens(self, usage: Usage) -> None:
    """Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token limits."""
    request_tokens = usage.request_tokens or 0
    if self.request_tokens_limit is not None and request_tokens > self.request_tokens_limit:
        raise UsageLimitExceeded(
            f'Exceeded the request_tokens_limit of {self.request_tokens_limit} ({request_tokens=})'
        )

    response_tokens = usage.response_tokens or 0
    if self.response_tokens_limit is not None and response_tokens > self.response_tokens_limit:
        raise UsageLimitExceeded(
            f'Exceeded the response_tokens_limit of {self.response_tokens_limit} ({response_tokens=})'
        )

    total_tokens = usage.total_tokens or 0
    if self.total_tokens_limit is not None and total_tokens > self.total_tokens_limit:
        raise UsageLimitExceeded(f'Exceeded the total_tokens_limit of {self.total_tokens_limit} ({total_tokens=})')
```

```
def check_tokens(self, usage: Usage) -> None:
    """Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token limits."""
    request_tokens = usage.request_tokens or 0
    if self.request_tokens_limit is not None and request_tokens > self.request_tokens_limit:
        raise UsageLimitExceeded(
            f'Exceeded the request_tokens_limit of {self.request_tokens_limit} ({request_tokens=})'
        )

    response_tokens = usage.response_tokens or 0
    if self.response_tokens_limit is not None and response_tokens > self.response_tokens_limit:
        raise UsageLimitExceeded(
            f'Exceeded the response_tokens_limit of {self.response_tokens_limit} ({response_tokens=})'
        )

    total_tokens = usage.total_tokens or 0
    if self.total_tokens_limit is not None and total_tokens > self.total_tokens_limit:
        raise UsageLimitExceeded(f'Exceeded the total_tokens_limit of {self.total_tokens_limit} ({total_tokens=})')
```

