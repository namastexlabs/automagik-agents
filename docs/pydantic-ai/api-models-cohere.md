# pydantic_ai.models.cohere

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.cohere

```
pydantic_ai.models.cohere
```

## Setup

For details on how to set up authentication with this model, see model configuration for Cohere.

[](https://ai.pydantic.dev)

### LatestCohereModelNames

module-attribute

```
module-attribute
```

```
LatestCohereModelNames = Literal[
    "c4ai-aya-expanse-32b",
    "c4ai-aya-expanse-8b",
    "command",
    "command-light",
    "command-light-nightly",
    "command-nightly",
    "command-r",
    "command-r-03-2024",
    "command-r-08-2024",
    "command-r-plus",
    "command-r-plus-04-2024",
    "command-r-plus-08-2024",
    "command-r7b-12-2024",
]
```

```
LatestCohereModelNames = Literal[
    "c4ai-aya-expanse-32b",
    "c4ai-aya-expanse-8b",
    "command",
    "command-light",
    "command-light-nightly",
    "command-nightly",
    "command-r",
    "command-r-03-2024",
    "command-r-08-2024",
    "command-r-plus",
    "command-r-plus-04-2024",
    "command-r-plus-08-2024",
    "command-r7b-12-2024",
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Latest Cohere models.

### CohereModelName

module-attribute

```
module-attribute
```

```
CohereModelName = Union[str, LatestCohereModelNames]
```

```
CohereModelName = Union[str, LatestCohereModelNames]
```

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[LatestCohereModelNames](https://ai.pydantic.dev#pydantic_ai.models.cohere.LatestCohereModelNames)

Possible Cohere model names.

Since Cohere supports a variety of date-stamped models, we explicitly list the latest models but
allow any name in the type hints.
See Cohere's docs for a list of all available models.

### CohereModelSettings

Bases: ModelSettings

```
ModelSettings
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Settings used for a Cohere model request.

```
pydantic_ai_slim/pydantic_ai/models/cohere.py
```

```
82
83
```

```
class CohereModelSettings(ModelSettings):
    """Settings used for a Cohere model request."""
```

```
class CohereModelSettings(ModelSettings):
    """Settings used for a Cohere model request."""
```

### CohereModel

dataclass

```
dataclass
```

Bases: Model

```
Model
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

A model that uses the Cohere API.

Internally, this uses the Cohere Python client to interact with the API.

Apart from __init__, all methods are private or match those of the base class.

```
__init__
```

```
pydantic_ai_slim/pydantic_ai/models/cohere.py
```

```
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
146
147
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
167
168
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
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
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
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
```

```
@dataclass(init=False)
class CohereModel(Model):
    """A model that uses the Cohere API.

    Internally, this uses the [Cohere Python client](
    https://github.com/cohere-ai/cohere-python) to interact with the API.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    client: AsyncClientV2 = field(repr=False)

    _model_name: CohereModelName = field(repr=False)
    _system: str | None = field(default='cohere', repr=False)

    def __init__(
        self,
        model_name: CohereModelName,
        *,
        api_key: str | None = None,
        cohere_client: AsyncClientV2 | None = None,
        http_client: AsyncHTTPClient | None = None,
    ):
        """Initialize an Cohere model.

        Args:
            model_name: The name of the Cohere model to use. List of model names
                available [here](https://docs.cohere.com/docs/models#command).
            api_key: The API key to use for authentication, if not provided, the
                `CO_API_KEY` environment variable will be used if available.
            cohere_client: An existing Cohere async client to use. If provided,
                `api_key` and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._model_name: CohereModelName = model_name
        if cohere_client is not None:
            assert http_client is None, 'Cannot provide both `cohere_client` and `http_client`'
            assert api_key is None, 'Cannot provide both `cohere_client` and `api_key`'
            self.client = cohere_client
        else:
            self.client = AsyncClientV2(api_key=api_key, httpx_client=http_client)

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, result.Usage]:
        check_allow_model_requests()
        response = await self._chat(messages, cast(CohereModelSettings, model_settings or {}), model_request_parameters)
        return self._process_response(response), _map_usage(response)

    @property
    def model_name(self) -> CohereModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    async def _chat(
        self,
        messages: list[ModelMessage],
        model_settings: CohereModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> ChatResponse:
        tools = self._get_tools(model_request_parameters)
        cohere_messages = list(chain(*(self._map_message(m) for m in messages)))
        try:
            return await self.client.chat(
                model=self._model_name,
                messages=cohere_messages,
                tools=tools or OMIT,
                max_tokens=model_settings.get('max_tokens', OMIT),
                temperature=model_settings.get('temperature', OMIT),
                p=model_settings.get('top_p', OMIT),
                seed=model_settings.get('seed', OMIT),
                presence_penalty=model_settings.get('presence_penalty', OMIT),
                frequency_penalty=model_settings.get('frequency_penalty', OMIT),
            )
        except ApiError as e:
            if (status_code := e.status_code) and status_code >= 400:
                raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=e.body) from e
            raise

    def _process_response(self, response: ChatResponse) -> ModelResponse:
        """Process a non-streamed response, and prepare a message to return."""
        parts: list[ModelResponsePart] = []
        if response.message.content is not None and len(response.message.content) > 0:
            # While Cohere's API returns a list, it only does that for future proofing
            # and currently only one item is being returned.
            choice = response.message.content[0]
            parts.append(TextPart(choice.text))
        for c in response.message.tool_calls or []:
            if c.function and c.function.name and c.function.arguments:
                parts.append(
                    ToolCallPart(
                        tool_name=c.function.name,
                        args=c.function.arguments,
                        tool_call_id=c.id,
                    )
                )
        return ModelResponse(parts=parts, model_name=self._model_name)

    def _map_message(self, message: ModelMessage) -> Iterable[ChatMessageV2]:
        """Just maps a `pydantic_ai.Message` to a `cohere.ChatMessageV2`."""
        if isinstance(message, ModelRequest):
            yield from self._map_user_message(message)
        elif isinstance(message, ModelResponse):
            texts: list[str] = []
            tool_calls: list[ToolCallV2] = []
            for item in message.parts:
                if isinstance(item, TextPart):
                    texts.append(item.content)
                elif isinstance(item, ToolCallPart):
                    tool_calls.append(self._map_tool_call(item))
                else:
                    assert_never(item)
            message_param = AssistantChatMessageV2(role='assistant')
            if texts:
                message_param.content = [TextAssistantMessageContentItem(text='\n\n'.join(texts))]
            if tool_calls:
                message_param.tool_calls = tool_calls
            yield message_param
        else:
            assert_never(message)

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[ToolV2]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    @staticmethod
    def _map_tool_call(t: ToolCallPart) -> ToolCallV2:
        return ToolCallV2(
            id=_guard_tool_call_id(t=t, model_source='Cohere'),
            type='function',
            function=ToolCallV2Function(
                name=t.tool_name,
                arguments=t.args_as_json_str(),
            ),
        )

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> ToolV2:
        return ToolV2(
            type='function',
            function=ToolV2Function(
                name=f.name,
                description=f.description,
                parameters=f.parameters_json_schema,
            ),
        )

    @classmethod
    def _map_user_message(cls, message: ModelRequest) -> Iterable[ChatMessageV2]:
        for part in message.parts:
            if isinstance(part, SystemPromptPart):
                yield SystemChatMessageV2(role='system', content=part.content)
            elif isinstance(part, UserPromptPart):
                if isinstance(part.content, str):
                    yield UserChatMessageV2(role='user', content=part.content)
                else:
                    raise RuntimeError('Cohere does not yet support multi-modal inputs.')
            elif isinstance(part, ToolReturnPart):
                yield ToolChatMessageV2(
                    role='tool',
                    tool_call_id=_guard_tool_call_id(t=part, model_source='Cohere'),
                    content=part.model_response_str(),
                )
            elif isinstance(part, RetryPromptPart):
                if part.tool_name is None:
                    yield UserChatMessageV2(role='user', content=part.model_response())
                else:
                    yield ToolChatMessageV2(
                        role='tool',
                        tool_call_id=_guard_tool_call_id(t=part, model_source='Cohere'),
                        content=part.model_response(),
                    )
            else:
                assert_never(part)
```

```
@dataclass(init=False)
class CohereModel(Model):
    """A model that uses the Cohere API.

    Internally, this uses the [Cohere Python client](
    https://github.com/cohere-ai/cohere-python) to interact with the API.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    client: AsyncClientV2 = field(repr=False)

    _model_name: CohereModelName = field(repr=False)
    _system: str | None = field(default='cohere', repr=False)

    def __init__(
        self,
        model_name: CohereModelName,
        *,
        api_key: str | None = None,
        cohere_client: AsyncClientV2 | None = None,
        http_client: AsyncHTTPClient | None = None,
    ):
        """Initialize an Cohere model.

        Args:
            model_name: The name of the Cohere model to use. List of model names
                available [here](https://docs.cohere.com/docs/models#command).
            api_key: The API key to use for authentication, if not provided, the
                `CO_API_KEY` environment variable will be used if available.
            cohere_client: An existing Cohere async client to use. If provided,
                `api_key` and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._model_name: CohereModelName = model_name
        if cohere_client is not None:
            assert http_client is None, 'Cannot provide both `cohere_client` and `http_client`'
            assert api_key is None, 'Cannot provide both `cohere_client` and `api_key`'
            self.client = cohere_client
        else:
            self.client = AsyncClientV2(api_key=api_key, httpx_client=http_client)

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, result.Usage]:
        check_allow_model_requests()
        response = await self._chat(messages, cast(CohereModelSettings, model_settings or {}), model_request_parameters)
        return self._process_response(response), _map_usage(response)

    @property
    def model_name(self) -> CohereModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    async def _chat(
        self,
        messages: list[ModelMessage],
        model_settings: CohereModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> ChatResponse:
        tools = self._get_tools(model_request_parameters)
        cohere_messages = list(chain(*(self._map_message(m) for m in messages)))
        try:
            return await self.client.chat(
                model=self._model_name,
                messages=cohere_messages,
                tools=tools or OMIT,
                max_tokens=model_settings.get('max_tokens', OMIT),
                temperature=model_settings.get('temperature', OMIT),
                p=model_settings.get('top_p', OMIT),
                seed=model_settings.get('seed', OMIT),
                presence_penalty=model_settings.get('presence_penalty', OMIT),
                frequency_penalty=model_settings.get('frequency_penalty', OMIT),
            )
        except ApiError as e:
            if (status_code := e.status_code) and status_code >= 400:
                raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=e.body) from e
            raise

    def _process_response(self, response: ChatResponse) -> ModelResponse:
        """Process a non-streamed response, and prepare a message to return."""
        parts: list[ModelResponsePart] = []
        if response.message.content is not None and len(response.message.content) > 0:
            # While Cohere's API returns a list, it only does that for future proofing
            # and currently only one item is being returned.
            choice = response.message.content[0]
            parts.append(TextPart(choice.text))
        for c in response.message.tool_calls or []:
            if c.function and c.function.name and c.function.arguments:
                parts.append(
                    ToolCallPart(
                        tool_name=c.function.name,
                        args=c.function.arguments,
                        tool_call_id=c.id,
                    )
                )
        return ModelResponse(parts=parts, model_name=self._model_name)

    def _map_message(self, message: ModelMessage) -> Iterable[ChatMessageV2]:
        """Just maps a `pydantic_ai.Message` to a `cohere.ChatMessageV2`."""
        if isinstance(message, ModelRequest):
            yield from self._map_user_message(message)
        elif isinstance(message, ModelResponse):
            texts: list[str] = []
            tool_calls: list[ToolCallV2] = []
            for item in message.parts:
                if isinstance(item, TextPart):
                    texts.append(item.content)
                elif isinstance(item, ToolCallPart):
                    tool_calls.append(self._map_tool_call(item))
                else:
                    assert_never(item)
            message_param = AssistantChatMessageV2(role='assistant')
            if texts:
                message_param.content = [TextAssistantMessageContentItem(text='\n\n'.join(texts))]
            if tool_calls:
                message_param.tool_calls = tool_calls
            yield message_param
        else:
            assert_never(message)

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[ToolV2]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    @staticmethod
    def _map_tool_call(t: ToolCallPart) -> ToolCallV2:
        return ToolCallV2(
            id=_guard_tool_call_id(t=t, model_source='Cohere'),
            type='function',
            function=ToolCallV2Function(
                name=t.tool_name,
                arguments=t.args_as_json_str(),
            ),
        )

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> ToolV2:
        return ToolV2(
            type='function',
            function=ToolV2Function(
                name=f.name,
                description=f.description,
                parameters=f.parameters_json_schema,
            ),
        )

    @classmethod
    def _map_user_message(cls, message: ModelRequest) -> Iterable[ChatMessageV2]:
        for part in message.parts:
            if isinstance(part, SystemPromptPart):
                yield SystemChatMessageV2(role='system', content=part.content)
            elif isinstance(part, UserPromptPart):
                if isinstance(part.content, str):
                    yield UserChatMessageV2(role='user', content=part.content)
                else:
                    raise RuntimeError('Cohere does not yet support multi-modal inputs.')
            elif isinstance(part, ToolReturnPart):
                yield ToolChatMessageV2(
                    role='tool',
                    tool_call_id=_guard_tool_call_id(t=part, model_source='Cohere'),
                    content=part.model_response_str(),
                )
            elif isinstance(part, RetryPromptPart):
                if part.tool_name is None:
                    yield UserChatMessageV2(role='user', content=part.model_response())
                else:
                    yield ToolChatMessageV2(
                        role='tool',
                        tool_call_id=_guard_tool_call_id(t=part, model_source='Cohere'),
                        content=part.model_response(),
                    )
            else:
                assert_never(part)
```

#### __init__

```
__init__(
    model_name: CohereModelName,
    *,
    api_key: str | None = None,
    cohere_client: AsyncClientV2 | None = None,
    http_client: AsyncClient | None = None
)
```

```
__init__(
    model_name: CohereModelName,
    *,
    api_key: str | None = None,
    cohere_client: AsyncClientV2 | None = None,
    http_client: AsyncClient | None = None
)
```

[CohereModelName](https://ai.pydantic.dev#pydantic_ai.models.cohere.CohereModelName)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Initialize an Cohere model.

Parameters:

```
model_name
```

```
CohereModelName
```

[CohereModelName](https://ai.pydantic.dev#pydantic_ai.models.cohere.CohereModelName)

The name of the Cohere model to use. List of model names
available here.

```
api_key
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The API key to use for authentication, if not provided, the
CO_API_KEY environment variable will be used if available.

```
CO_API_KEY
```

```
None
```

```
cohere_client
```

```
AsyncClientV2 | None
```

An existing Cohere async client to use. If provided,
api_key and http_client must be None.

```
api_key
```

```
http_client
```

```
None
```

```
None
```

```
http_client
```

```
AsyncClient | None
```

An existing httpx.AsyncClient to use for making HTTP requests.

```
httpx.AsyncClient
```

```
None
```

```
pydantic_ai_slim/pydantic_ai/models/cohere.py
```

```
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
def __init__(
    self,
    model_name: CohereModelName,
    *,
    api_key: str | None = None,
    cohere_client: AsyncClientV2 | None = None,
    http_client: AsyncHTTPClient | None = None,
):
    """Initialize an Cohere model.

    Args:
        model_name: The name of the Cohere model to use. List of model names
            available [here](https://docs.cohere.com/docs/models#command).
        api_key: The API key to use for authentication, if not provided, the
            `CO_API_KEY` environment variable will be used if available.
        cohere_client: An existing Cohere async client to use. If provided,
            `api_key` and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._model_name: CohereModelName = model_name
    if cohere_client is not None:
        assert http_client is None, 'Cannot provide both `cohere_client` and `http_client`'
        assert api_key is None, 'Cannot provide both `cohere_client` and `api_key`'
        self.client = cohere_client
    else:
        self.client = AsyncClientV2(api_key=api_key, httpx_client=http_client)
```

```
def __init__(
    self,
    model_name: CohereModelName,
    *,
    api_key: str | None = None,
    cohere_client: AsyncClientV2 | None = None,
    http_client: AsyncHTTPClient | None = None,
):
    """Initialize an Cohere model.

    Args:
        model_name: The name of the Cohere model to use. List of model names
            available [here](https://docs.cohere.com/docs/models#command).
        api_key: The API key to use for authentication, if not provided, the
            `CO_API_KEY` environment variable will be used if available.
        cohere_client: An existing Cohere async client to use. If provided,
            `api_key` and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._model_name: CohereModelName = model_name
    if cohere_client is not None:
        assert http_client is None, 'Cannot provide both `cohere_client` and `http_client`'
        assert api_key is None, 'Cannot provide both `cohere_client` and `api_key`'
        self.client = cohere_client
    else:
        self.client = AsyncClientV2(api_key=api_key, httpx_client=http_client)
```

#### model_name

property

```
property
```

```
model_name: CohereModelName
```

```
model_name: CohereModelName
```

[CohereModelName](https://ai.pydantic.dev#pydantic_ai.models.cohere.CohereModelName)

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

