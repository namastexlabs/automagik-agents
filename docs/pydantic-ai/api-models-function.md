# pydantic_ai.models.function

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.function

```
pydantic_ai.models.function
```

A model controlled by a local function.

FunctionModel is similar to TestModel,
but allows greater control over the model's behavior.

```
FunctionModel
```

```
TestModel
```

Its primary use case is for more advanced unit testing than is possible with TestModel.

```
TestModel
```

Here's a minimal example:

```
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
from pydantic_ai.models.function import FunctionModel, AgentInfo

my_agent = Agent('openai:gpt-4o')


async def model_function(
    messages: list[ModelMessage], info: AgentInfo
) -> ModelResponse:
    print(messages)
    """
    [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content='Testing my agent...',
                    timestamp=datetime.datetime(...),
                    part_kind='user-prompt',
                )
            ],
            kind='request',
        )
    ]
    """
    print(info)
    """
    AgentInfo(
        function_tools=[], allow_text_result=True, result_tools=[], model_settings=None
    )
    """
    return ModelResponse(parts=[TextPart('hello world')])


async def test_my_agent():
    """Unit test for my_agent, to be run by pytest."""
    with my_agent.override(model=FunctionModel(model_function)):
        result = await my_agent.run('Testing my agent...')
        assert result.data == 'hello world'
```

```
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
from pydantic_ai.models.function import FunctionModel, AgentInfo

my_agent = Agent('openai:gpt-4o')


async def model_function(
    messages: list[ModelMessage], info: AgentInfo
) -> ModelResponse:
    print(messages)
    """
    [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content='Testing my agent...',
                    timestamp=datetime.datetime(...),
                    part_kind='user-prompt',
                )
            ],
            kind='request',
        )
    ]
    """
    print(info)
    """
    AgentInfo(
        function_tools=[], allow_text_result=True, result_tools=[], model_settings=None
    )
    """
    return ModelResponse(parts=[TextPart('hello world')])


async def test_my_agent():
    """Unit test for my_agent, to be run by pytest."""
    with my_agent.override(model=FunctionModel(model_function)):
        result = await my_agent.run('Testing my agent...')
        assert result.data == 'hello world'
```

See Unit testing with FunctionModel for detailed documentation.

```
FunctionModel
```

[](https://ai.pydantic.dev)

### FunctionModel

dataclass

```
dataclass
```

Bases: Model

```
Model
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

A model controlled by a local function.

Apart from __init__, all methods are private or match those of the base class.

```
__init__
```

```
pydantic_ai_slim/pydantic_ai/models/function.py
```

```
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
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
```

```
@dataclass(init=False)
class FunctionModel(Model):
    """A model controlled by a local function.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    function: FunctionDef | None = None
    stream_function: StreamFunctionDef | None = None

    _model_name: str = field(repr=False)
    _system: str | None = field(default=None, repr=False)

    @overload
    def __init__(self, function: FunctionDef, *, model_name: str | None = None) -> None: ...

    @overload
    def __init__(self, *, stream_function: StreamFunctionDef, model_name: str | None = None) -> None: ...

    @overload
    def __init__(
        self, function: FunctionDef, *, stream_function: StreamFunctionDef, model_name: str | None = None
    ) -> None: ...

    def __init__(
        self,
        function: FunctionDef | None = None,
        *,
        stream_function: StreamFunctionDef | None = None,
        model_name: str | None = None,
    ):
        """Initialize a `FunctionModel`.

        Either `function` or `stream_function` must be provided, providing both is allowed.

        Args:
            function: The function to call for non-streamed requests.
            stream_function: The function to call for streamed requests.
            model_name: The name of the model. If not provided, a name is generated from the function names.
        """
        if function is None and stream_function is None:
            raise TypeError('Either `function` or `stream_function` must be provided')
        self.function = function
        self.stream_function = stream_function

        function_name = self.function.__name__ if self.function is not None else ''
        stream_function_name = self.stream_function.__name__ if self.stream_function is not None else ''
        self._model_name = model_name or f'function:{function_name}:{stream_function_name}'

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        agent_info = AgentInfo(
            model_request_parameters.function_tools,
            model_request_parameters.allow_text_result,
            model_request_parameters.result_tools,
            model_settings,
        )

        assert self.function is not None, 'FunctionModel must receive a `function` to support non-streamed requests'

        if inspect.iscoroutinefunction(self.function):
            response = await self.function(messages, agent_info)
        else:
            response_ = await _utils.run_in_executor(self.function, messages, agent_info)
            assert isinstance(response_, ModelResponse), response_
            response = response_
        response.model_name = self._model_name
        # TODO is `messages` right here? Should it just be new messages?
        return response, _estimate_usage(chain(messages, [response]))

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        agent_info = AgentInfo(
            model_request_parameters.function_tools,
            model_request_parameters.allow_text_result,
            model_request_parameters.result_tools,
            model_settings,
        )

        assert self.stream_function is not None, (
            'FunctionModel must receive a `stream_function` to support streamed requests'
        )

        response_stream = PeekableAsyncStream(self.stream_function(messages, agent_info))

        first = await response_stream.peek()
        if isinstance(first, _utils.Unset):
            raise ValueError('Stream function must return at least one item')

        yield FunctionStreamedResponse(_model_name=self._model_name, _iter=response_stream)

    @property
    def model_name(self) -> str:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system
```

```
@dataclass(init=False)
class FunctionModel(Model):
    """A model controlled by a local function.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    function: FunctionDef | None = None
    stream_function: StreamFunctionDef | None = None

    _model_name: str = field(repr=False)
    _system: str | None = field(default=None, repr=False)

    @overload
    def __init__(self, function: FunctionDef, *, model_name: str | None = None) -> None: ...

    @overload
    def __init__(self, *, stream_function: StreamFunctionDef, model_name: str | None = None) -> None: ...

    @overload
    def __init__(
        self, function: FunctionDef, *, stream_function: StreamFunctionDef, model_name: str | None = None
    ) -> None: ...

    def __init__(
        self,
        function: FunctionDef | None = None,
        *,
        stream_function: StreamFunctionDef | None = None,
        model_name: str | None = None,
    ):
        """Initialize a `FunctionModel`.

        Either `function` or `stream_function` must be provided, providing both is allowed.

        Args:
            function: The function to call for non-streamed requests.
            stream_function: The function to call for streamed requests.
            model_name: The name of the model. If not provided, a name is generated from the function names.
        """
        if function is None and stream_function is None:
            raise TypeError('Either `function` or `stream_function` must be provided')
        self.function = function
        self.stream_function = stream_function

        function_name = self.function.__name__ if self.function is not None else ''
        stream_function_name = self.stream_function.__name__ if self.stream_function is not None else ''
        self._model_name = model_name or f'function:{function_name}:{stream_function_name}'

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        agent_info = AgentInfo(
            model_request_parameters.function_tools,
            model_request_parameters.allow_text_result,
            model_request_parameters.result_tools,
            model_settings,
        )

        assert self.function is not None, 'FunctionModel must receive a `function` to support non-streamed requests'

        if inspect.iscoroutinefunction(self.function):
            response = await self.function(messages, agent_info)
        else:
            response_ = await _utils.run_in_executor(self.function, messages, agent_info)
            assert isinstance(response_, ModelResponse), response_
            response = response_
        response.model_name = self._model_name
        # TODO is `messages` right here? Should it just be new messages?
        return response, _estimate_usage(chain(messages, [response]))

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        agent_info = AgentInfo(
            model_request_parameters.function_tools,
            model_request_parameters.allow_text_result,
            model_request_parameters.result_tools,
            model_settings,
        )

        assert self.stream_function is not None, (
            'FunctionModel must receive a `stream_function` to support streamed requests'
        )

        response_stream = PeekableAsyncStream(self.stream_function(messages, agent_info))

        first = await response_stream.peek()
        if isinstance(first, _utils.Unset):
            raise ValueError('Stream function must return at least one item')

        yield FunctionStreamedResponse(_model_name=self._model_name, _iter=response_stream)

    @property
    def model_name(self) -> str:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system
```

#### __init__

```
__init__(
    function: FunctionDef, *, model_name: str | None = None
) -> None
```

```
__init__(
    function: FunctionDef, *, model_name: str | None = None
) -> None
```

[FunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.FunctionDef)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
__init__(
    *,
    stream_function: StreamFunctionDef,
    model_name: str | None = None
) -> None
```

```
__init__(
    *,
    stream_function: StreamFunctionDef,
    model_name: str | None = None
) -> None
```

[StreamFunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.StreamFunctionDef)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
__init__(
    function: FunctionDef,
    *,
    stream_function: StreamFunctionDef,
    model_name: str | None = None
) -> None
```

```
__init__(
    function: FunctionDef,
    *,
    stream_function: StreamFunctionDef,
    model_name: str | None = None
) -> None
```

[FunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.FunctionDef)

[StreamFunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.StreamFunctionDef)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
__init__(
    function: FunctionDef | None = None,
    *,
    stream_function: StreamFunctionDef | None = None,
    model_name: str | None = None
)
```

```
__init__(
    function: FunctionDef | None = None,
    *,
    stream_function: StreamFunctionDef | None = None,
    model_name: str | None = None
)
```

[FunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.FunctionDef)

[StreamFunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.StreamFunctionDef)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Initialize a FunctionModel.

```
FunctionModel
```

Either function or stream_function must be provided, providing both is allowed.

```
function
```

```
stream_function
```

Parameters:

```
function
```

```
FunctionDef | None
```

[FunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.FunctionDef)

The function to call for non-streamed requests.

```
None
```

```
stream_function
```

```
StreamFunctionDef | None
```

[StreamFunctionDef](https://ai.pydantic.dev#pydantic_ai.models.function.StreamFunctionDef)

The function to call for streamed requests.

```
None
```

```
model_name
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The name of the model. If not provided, a name is generated from the function names.

```
None
```

```
pydantic_ai_slim/pydantic_ai/models/function.py
```

```
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
```

```
def __init__(
    self,
    function: FunctionDef | None = None,
    *,
    stream_function: StreamFunctionDef | None = None,
    model_name: str | None = None,
):
    """Initialize a `FunctionModel`.

    Either `function` or `stream_function` must be provided, providing both is allowed.

    Args:
        function: The function to call for non-streamed requests.
        stream_function: The function to call for streamed requests.
        model_name: The name of the model. If not provided, a name is generated from the function names.
    """
    if function is None and stream_function is None:
        raise TypeError('Either `function` or `stream_function` must be provided')
    self.function = function
    self.stream_function = stream_function

    function_name = self.function.__name__ if self.function is not None else ''
    stream_function_name = self.stream_function.__name__ if self.stream_function is not None else ''
    self._model_name = model_name or f'function:{function_name}:{stream_function_name}'
```

```
def __init__(
    self,
    function: FunctionDef | None = None,
    *,
    stream_function: StreamFunctionDef | None = None,
    model_name: str | None = None,
):
    """Initialize a `FunctionModel`.

    Either `function` or `stream_function` must be provided, providing both is allowed.

    Args:
        function: The function to call for non-streamed requests.
        stream_function: The function to call for streamed requests.
        model_name: The name of the model. If not provided, a name is generated from the function names.
    """
    if function is None and stream_function is None:
        raise TypeError('Either `function` or `stream_function` must be provided')
    self.function = function
    self.stream_function = stream_function

    function_name = self.function.__name__ if self.function is not None else ''
    stream_function_name = self.stream_function.__name__ if self.stream_function is not None else ''
    self._model_name = model_name or f'function:{function_name}:{stream_function_name}'
```

#### model_name

property

```
property
```

```
model_name: str
```

```
model_name: str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The model name.

#### system

property

```
property
```

```
system: str | None
```

```
system: str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The system / model provider.

### AgentInfo

dataclass

```
dataclass
```

Information about an agent.

This is passed as the second to functions used within FunctionModel.

```
FunctionModel
```

```
pydantic_ai_slim/pydantic_ai/models/function.py
```

```
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
```

```
@dataclass(frozen=True)
class AgentInfo:
    """Information about an agent.

    This is passed as the second to functions used within [`FunctionModel`][pydantic_ai.models.function.FunctionModel].
    """

    function_tools: list[ToolDefinition]
    """The function tools available on this agent.

    These are the tools registered via the [`tool`][pydantic_ai.Agent.tool] and
    [`tool_plain`][pydantic_ai.Agent.tool_plain] decorators.
    """
    allow_text_result: bool
    """Whether a plain text result is allowed."""
    result_tools: list[ToolDefinition]
    """The tools that can called as the final result of the run."""
    model_settings: ModelSettings | None
    """The model settings passed to the run call."""
```

```
@dataclass(frozen=True)
class AgentInfo:
    """Information about an agent.

    This is passed as the second to functions used within [`FunctionModel`][pydantic_ai.models.function.FunctionModel].
    """

    function_tools: list[ToolDefinition]
    """The function tools available on this agent.

    These are the tools registered via the [`tool`][pydantic_ai.Agent.tool] and
    [`tool_plain`][pydantic_ai.Agent.tool_plain] decorators.
    """
    allow_text_result: bool
    """Whether a plain text result is allowed."""
    result_tools: list[ToolDefinition]
    """The tools that can called as the final result of the run."""
    model_settings: ModelSettings | None
    """The model settings passed to the run call."""
```

#### function_tools

instance-attribute

```
instance-attribute
```

```
function_tools: list[ToolDefinition]
```

```
function_tools: list[ToolDefinition]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ToolDefinition](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolDefinition)

The function tools available on this agent.

These are the tools registered via the tool and
tool_plain decorators.

```
tool
```

```
tool_plain
```

#### allow_text_result

instance-attribute

```
instance-attribute
```

```
allow_text_result: bool
```

```
allow_text_result: bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether a plain text result is allowed.

#### result_tools

instance-attribute

```
instance-attribute
```

```
result_tools: list[ToolDefinition]
```

```
result_tools: list[ToolDefinition]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ToolDefinition](https://ai.pydantic.dev/tools/#pydantic_ai.tools.ToolDefinition)

The tools that can called as the final result of the run.

#### model_settings

instance-attribute

```
instance-attribute
```

```
model_settings: ModelSettings | None
```

```
model_settings: ModelSettings | None
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

The model settings passed to the run call.

### DeltaToolCall

dataclass

```
dataclass
```

Incremental change to a tool call.

Used to describe a chunk when streaming structured responses.

```
pydantic_ai_slim/pydantic_ai/models/function.py
```

```
169
170
171
172
173
174
175
176
177
178
179
180
181
```

```
@dataclass
class DeltaToolCall:
    """Incremental change to a tool call.

    Used to describe a chunk when streaming structured responses.
    """

    name: str | None = None
    """Incremental change to the name of the tool."""
    json_args: str | None = None
    """Incremental change to the arguments as JSON"""
    tool_call_id: str | None = None
    """Incremental change to the tool call ID."""
```

```
@dataclass
class DeltaToolCall:
    """Incremental change to a tool call.

    Used to describe a chunk when streaming structured responses.
    """

    name: str | None = None
    """Incremental change to the name of the tool."""
    json_args: str | None = None
    """Incremental change to the arguments as JSON"""
    tool_call_id: str | None = None
    """Incremental change to the tool call ID."""
```

#### name

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
name: str | None = None
```

```
name: str | None = None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Incremental change to the name of the tool.

#### json_args

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
json_args: str | None = None
```

```
json_args: str | None = None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Incremental change to the arguments as JSON

#### tool_call_id

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
tool_call_id: str | None = None
```

```
tool_call_id: str | None = None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Incremental change to the tool call ID.

### DeltaToolCalls

module-attribute

```
module-attribute
```

```
DeltaToolCalls: TypeAlias = dict[int, DeltaToolCall]
```

```
DeltaToolCalls: TypeAlias = dict[int, DeltaToolCall]
```

[TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias)

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[int](https://docs.python.org/3/library/functions.html#int)

[DeltaToolCall](https://ai.pydantic.dev#pydantic_ai.models.function.DeltaToolCall)

A mapping of tool call IDs to incremental changes.

### FunctionDef

module-attribute

```
module-attribute
```

```
FunctionDef: TypeAlias = Callable[
    [list[ModelMessage], AgentInfo],
    Union[ModelResponse, Awaitable[ModelResponse]],
]
```

```
FunctionDef: TypeAlias = Callable[
    [list[ModelMessage], AgentInfo],
    Union[ModelResponse, Awaitable[ModelResponse]],
]
```

[TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[AgentInfo](https://ai.pydantic.dev#pydantic_ai.models.function.AgentInfo)

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[ModelResponse](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelResponse)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[ModelResponse](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelResponse)

A function used to generate a non-streamed response.

### StreamFunctionDef

module-attribute

```
module-attribute
```

```
StreamFunctionDef: TypeAlias = Callable[
    [list[ModelMessage], AgentInfo],
    AsyncIterator[Union[str, DeltaToolCalls]],
]
```

```
StreamFunctionDef: TypeAlias = Callable[
    [list[ModelMessage], AgentInfo],
    AsyncIterator[Union[str, DeltaToolCalls]],
]
```

[TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[AgentInfo](https://ai.pydantic.dev#pydantic_ai.models.function.AgentInfo)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[DeltaToolCalls](https://ai.pydantic.dev#pydantic_ai.models.function.DeltaToolCalls)

A function used to generate a streamed response.

While this is defined as having return type of AsyncIterator[Union[str, DeltaToolCalls]], it should
really be considered as Union[AsyncIterator[str], AsyncIterator[DeltaToolCalls],

```
AsyncIterator[Union[str, DeltaToolCalls]]
```

```
Union[AsyncIterator[str], AsyncIterator[DeltaToolCalls]
```

E.g. you need to yield all text or all DeltaToolCalls, not mix them.

```
DeltaToolCalls
```

### FunctionStreamedResponse

dataclass

```
dataclass
```

Bases: StreamedResponse

```
StreamedResponse
```

[StreamedResponse](https://ai.pydantic.dev/base/#pydantic_ai.models.StreamedResponse)

Implementation of StreamedResponse for FunctionModel.

```
StreamedResponse
```

```
pydantic_ai_slim/pydantic_ai/models/function.py
```

```
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
```

```
@dataclass
class FunctionStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for [FunctionModel][pydantic_ai.models.function.FunctionModel]."""

    _model_name: str
    _iter: AsyncIterator[str | DeltaToolCalls]
    _timestamp: datetime = field(default_factory=_utils.now_utc)

    def __post_init__(self):
        self._usage += _estimate_usage([])

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        async for item in self._iter:
            if isinstance(item, str):
                response_tokens = _estimate_string_tokens(item)
                self._usage += usage.Usage(response_tokens=response_tokens, total_tokens=response_tokens)
                yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=item)
            else:
                delta_tool_calls = item
                for dtc_index, delta_tool_call in delta_tool_calls.items():
                    if delta_tool_call.json_args:
                        response_tokens = _estimate_string_tokens(delta_tool_call.json_args)
                        self._usage += usage.Usage(response_tokens=response_tokens, total_tokens=response_tokens)
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=dtc_index,
                        tool_name=delta_tool_call.name,
                        args=delta_tool_call.json_args,
                        tool_call_id=delta_tool_call.tool_call_id,
                    )
                    if maybe_event is not None:
                        yield maybe_event

    @property
    def model_name(self) -> str:
        """Get the model name of the response."""
        return self._model_name

    @property
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._timestamp
```

```
@dataclass
class FunctionStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for [FunctionModel][pydantic_ai.models.function.FunctionModel]."""

    _model_name: str
    _iter: AsyncIterator[str | DeltaToolCalls]
    _timestamp: datetime = field(default_factory=_utils.now_utc)

    def __post_init__(self):
        self._usage += _estimate_usage([])

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        async for item in self._iter:
            if isinstance(item, str):
                response_tokens = _estimate_string_tokens(item)
                self._usage += usage.Usage(response_tokens=response_tokens, total_tokens=response_tokens)
                yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=item)
            else:
                delta_tool_calls = item
                for dtc_index, delta_tool_call in delta_tool_calls.items():
                    if delta_tool_call.json_args:
                        response_tokens = _estimate_string_tokens(delta_tool_call.json_args)
                        self._usage += usage.Usage(response_tokens=response_tokens, total_tokens=response_tokens)
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=dtc_index,
                        tool_name=delta_tool_call.name,
                        args=delta_tool_call.json_args,
                        tool_call_id=delta_tool_call.tool_call_id,
                    )
                    if maybe_event is not None:
                        yield maybe_event

    @property
    def model_name(self) -> str:
        """Get the model name of the response."""
        return self._model_name

    @property
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._timestamp
```

#### model_name

property

```
property
```

```
model_name: str
```

```
model_name: str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Get the model name of the response.

#### timestamp

property

```
property
```

```
timestamp: datetime
```

```
timestamp: datetime
```

[datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime)

Get the timestamp of the response.

