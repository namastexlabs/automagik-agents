# pydantic_ai.models.anthropic

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.anthropic

```
pydantic_ai.models.anthropic
```

## Setup

For details on how to set up authentication with this model, see model configuration for Anthropic.

[](https://ai.pydantic.dev)

### LatestAnthropicModelNames

module-attribute

```
module-attribute
```

```
LatestAnthropicModelNames = Literal[
    "claude-3-7-sonnet-latest",
    "claude-3-5-haiku-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-opus-latest",
]
```

```
LatestAnthropicModelNames = Literal[
    "claude-3-7-sonnet-latest",
    "claude-3-5-haiku-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-opus-latest",
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Latest Anthropic models.

### AnthropicModelName

module-attribute

```
module-attribute
```

```
AnthropicModelName = Union[str, LatestAnthropicModelNames]
```

```
AnthropicModelName = Union[str, LatestAnthropicModelNames]
```

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[LatestAnthropicModelNames](https://ai.pydantic.dev#pydantic_ai.models.anthropic.LatestAnthropicModelNames)

Possible Anthropic model names.

Since Anthropic supports a variety of date-stamped models, we explicitly list the latest models but
allow any name in the type hints.
See the Anthropic docs for a full list.

### AnthropicModelSettings

Bases: ModelSettings

```
ModelSettings
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Settings used for an Anthropic model request.

```
pydantic_ai_slim/pydantic_ai/models/anthropic.py
```

```
89
90
91
92
93
94
95
```

```
class AnthropicModelSettings(ModelSettings):
    """Settings used for an Anthropic model request."""

    anthropic_metadata: MetadataParam
    """An object describing metadata about the request.

    Contains `user_id`, an external identifier for the user who is associated with the request."""
```

```
class AnthropicModelSettings(ModelSettings):
    """Settings used for an Anthropic model request."""

    anthropic_metadata: MetadataParam
    """An object describing metadata about the request.

    Contains `user_id`, an external identifier for the user who is associated with the request."""
```

#### anthropic_metadata

instance-attribute

```
instance-attribute
```

```
anthropic_metadata: MetadataParam
```

```
anthropic_metadata: MetadataParam
```

An object describing metadata about the request.

Contains user_id, an external identifier for the user who is associated with the request.

```
user_id
```

### AnthropicModel

dataclass

```
dataclass
```

Bases: Model

```
Model
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

A model that uses the Anthropic API.

Internally, this uses the Anthropic Python client to interact with the API.

Apart from __init__, all methods are private or match those of the base class.

```
__init__
```

Note

The AnthropicModel class does not yet support streaming responses.
We anticipate adding support for streaming responses in a near-term future release.

```
AnthropicModel
```

```
pydantic_ai_slim/pydantic_ai/models/anthropic.py
```

```
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
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
```

```
@dataclass(init=False)
class AnthropicModel(Model):
    """A model that uses the Anthropic API.

    Internally, this uses the [Anthropic Python client](https://github.com/anthropics/anthropic-sdk-python) to interact with the API.

    Apart from `__init__`, all methods are private or match those of the base class.

    !!! note
        The `AnthropicModel` class does not yet support streaming responses.
        We anticipate adding support for streaming responses in a near-term future release.
    """

    client: AsyncAnthropic = field(repr=False)

    _model_name: AnthropicModelName = field(repr=False)
    _system: str | None = field(default='anthropic', repr=False)

    def __init__(
        self,
        model_name: AnthropicModelName,
        *,
        api_key: str | None = None,
        anthropic_client: AsyncAnthropic | None = None,
        http_client: AsyncHTTPClient | None = None,
    ):
        """Initialize an Anthropic model.

        Args:
            model_name: The name of the Anthropic model to use. List of model names available
                [here](https://docs.anthropic.com/en/docs/about-claude/models).
            api_key: The API key to use for authentication, if not provided, the `ANTHROPIC_API_KEY` environment variable
                will be used if available.
            anthropic_client: An existing
                [`AsyncAnthropic`](https://github.com/anthropics/anthropic-sdk-python?tab=readme-ov-file#async-usage)
                client to use, if provided, `api_key` and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._model_name = model_name
        if anthropic_client is not None:
            assert http_client is None, 'Cannot provide both `anthropic_client` and `http_client`'
            assert api_key is None, 'Cannot provide both `anthropic_client` and `api_key`'
            self.client = anthropic_client
        elif http_client is not None:
            self.client = AsyncAnthropic(api_key=api_key, http_client=http_client)
        else:
            self.client = AsyncAnthropic(api_key=api_key, http_client=cached_async_http_client())

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        check_allow_model_requests()
        response = await self._messages_create(
            messages, False, cast(AnthropicModelSettings, model_settings or {}), model_request_parameters
        )
        return self._process_response(response), _map_usage(response)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        check_allow_model_requests()
        response = await self._messages_create(
            messages, True, cast(AnthropicModelSettings, model_settings or {}), model_request_parameters
        )
        async with response:
            yield await self._process_streamed_response(response)

    @property
    def model_name(self) -> AnthropicModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[True],
        model_settings: AnthropicModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncStream[RawMessageStreamEvent]:
        pass

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[False],
        model_settings: AnthropicModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AnthropicMessage:
        pass

    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: bool,
        model_settings: AnthropicModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AnthropicMessage | AsyncStream[RawMessageStreamEvent]:
        # standalone function to make it easier to override
        tools = self._get_tools(model_request_parameters)
        tool_choice: ToolChoiceParam | None

        if not tools:
            tool_choice = None
        else:
            if not model_request_parameters.allow_text_result:
                tool_choice = {'type': 'any'}
            else:
                tool_choice = {'type': 'auto'}

            if (allow_parallel_tool_calls := model_settings.get('parallel_tool_calls')) is not None:
                tool_choice['disable_parallel_tool_use'] = not allow_parallel_tool_calls

        system_prompt, anthropic_messages = await self._map_message(messages)

        try:
            return await self.client.messages.create(
                max_tokens=model_settings.get('max_tokens', 1024),
                system=system_prompt or NOT_GIVEN,
                messages=anthropic_messages,
                model=self._model_name,
                tools=tools or NOT_GIVEN,
                tool_choice=tool_choice or NOT_GIVEN,
                stream=stream,
                temperature=model_settings.get('temperature', NOT_GIVEN),
                top_p=model_settings.get('top_p', NOT_GIVEN),
                timeout=model_settings.get('timeout', NOT_GIVEN),
                metadata=model_settings.get('anthropic_metadata', NOT_GIVEN),
            )
        except APIStatusError as e:
            if (status_code := e.status_code) >= 400:
                raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=e.body) from e
            raise

    def _process_response(self, response: AnthropicMessage) -> ModelResponse:
        """Process a non-streamed response, and prepare a message to return."""
        items: list[ModelResponsePart] = []
        for item in response.content:
            if isinstance(item, TextBlock):
                items.append(TextPart(content=item.text))
            else:
                assert isinstance(item, ToolUseBlock), 'unexpected item type'
                items.append(
                    ToolCallPart(
                        tool_name=item.name,
                        args=cast(dict[str, Any], item.input),
                        tool_call_id=item.id,
                    )
                )

        return ModelResponse(items, model_name=response.model)

    async def _process_streamed_response(self, response: AsyncStream[RawMessageStreamEvent]) -> StreamedResponse:
        peekable_response = _utils.PeekableAsyncStream(response)
        first_chunk = await peekable_response.peek()
        if isinstance(first_chunk, _utils.Unset):
            raise UnexpectedModelBehavior('Streamed response ended without content or tool calls')

        # Since Anthropic doesn't provide a timestamp in the message, we'll use the current time
        timestamp = datetime.now(tz=timezone.utc)
        return AnthropicStreamedResponse(
            _model_name=self._model_name, _response=peekable_response, _timestamp=timestamp
        )

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[ToolParam]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    async def _map_message(self, messages: list[ModelMessage]) -> tuple[str, list[MessageParam]]:
        """Just maps a `pydantic_ai.Message` to a `anthropic.types.MessageParam`."""
        system_prompt: str = ''
        anthropic_messages: list[MessageParam] = []
        for m in messages:
            if isinstance(m, ModelRequest):
                user_content_params: list[ToolResultBlockParam | TextBlockParam | ImageBlockParam] = []
                for request_part in m.parts:
                    if isinstance(request_part, SystemPromptPart):
                        system_prompt += request_part.content
                    elif isinstance(request_part, UserPromptPart):
                        async for content in self._map_user_prompt(request_part):
                            user_content_params.append(content)
                    elif isinstance(request_part, ToolReturnPart):
                        tool_result_block_param = ToolResultBlockParam(
                            tool_use_id=_guard_tool_call_id(t=request_part, model_source='Anthropic'),
                            type='tool_result',
                            content=request_part.model_response_str(),
                            is_error=False,
                        )
                        user_content_params.append(tool_result_block_param)
                    elif isinstance(request_part, RetryPromptPart):
                        if request_part.tool_name is None:
                            retry_param = TextBlockParam(type='text', text=request_part.model_response())
                        else:
                            retry_param = ToolResultBlockParam(
                                tool_use_id=_guard_tool_call_id(t=request_part, model_source='Anthropic'),
                                type='tool_result',
                                content=request_part.model_response(),
                                is_error=True,
                            )
                        user_content_params.append(retry_param)
                anthropic_messages.append(MessageParam(role='user', content=user_content_params))
            elif isinstance(m, ModelResponse):
                assistant_content_params: list[TextBlockParam | ToolUseBlockParam] = []
                for response_part in m.parts:
                    if isinstance(response_part, TextPart):
                        assistant_content_params.append(TextBlockParam(text=response_part.content, type='text'))
                    else:
                        tool_use_block_param = ToolUseBlockParam(
                            id=_guard_tool_call_id(t=response_part, model_source='Anthropic'),
                            type='tool_use',
                            name=response_part.tool_name,
                            input=response_part.args_as_dict(),
                        )
                        assistant_content_params.append(tool_use_block_param)
                anthropic_messages.append(MessageParam(role='assistant', content=assistant_content_params))
            else:
                assert_never(m)
        return system_prompt, anthropic_messages

    @staticmethod
    async def _map_user_prompt(part: UserPromptPart) -> AsyncGenerator[ImageBlockParam | TextBlockParam]:
        if isinstance(part.content, str):
            yield TextBlockParam(text=part.content, type='text')
        else:
            for item in part.content:
                if isinstance(item, str):
                    yield TextBlockParam(text=item, type='text')
                elif isinstance(item, BinaryContent):
                    if item.is_image:
                        yield ImageBlockParam(
                            source={'data': io.BytesIO(item.data), 'media_type': item.media_type, 'type': 'base64'},  # type: ignore
                            type='image',
                        )
                    else:
                        raise RuntimeError('Only images are supported for binary content')
                elif isinstance(item, ImageUrl):
                    try:
                        response = await cached_async_http_client().get(item.url)
                        response.raise_for_status()
                        yield ImageBlockParam(
                            source={
                                'data': io.BytesIO(response.content),
                                'media_type': item.media_type,
                                'type': 'base64',
                            },
                            type='image',
                        )
                    except ValueError:
                        # Download the file if can't find the mime type.
                        client = cached_async_http_client()
                        response = await client.get(item.url, follow_redirects=True)
                        response.raise_for_status()
                        base64_encoded = base64.b64encode(response.content).decode('utf-8')
                        if (mime_type := response.headers['Content-Type']) in (
                            'image/jpeg',
                            'image/png',
                            'image/gif',
                            'image/webp',
                        ):
                            yield ImageBlockParam(
                                source={'data': base64_encoded, 'media_type': mime_type, 'type': 'base64'},
                                type='image',
                            )
                        else:  # pragma: no cover
                            raise RuntimeError(f'Unsupported image type: {mime_type}')
                else:
                    raise RuntimeError(f'Unsupported content type: {type(item)}')

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> ToolParam:
        return {
            'name': f.name,
            'description': f.description,
            'input_schema': f.parameters_json_schema,
        }
```

```
@dataclass(init=False)
class AnthropicModel(Model):
    """A model that uses the Anthropic API.

    Internally, this uses the [Anthropic Python client](https://github.com/anthropics/anthropic-sdk-python) to interact with the API.

    Apart from `__init__`, all methods are private or match those of the base class.

    !!! note
        The `AnthropicModel` class does not yet support streaming responses.
        We anticipate adding support for streaming responses in a near-term future release.
    """

    client: AsyncAnthropic = field(repr=False)

    _model_name: AnthropicModelName = field(repr=False)
    _system: str | None = field(default='anthropic', repr=False)

    def __init__(
        self,
        model_name: AnthropicModelName,
        *,
        api_key: str | None = None,
        anthropic_client: AsyncAnthropic | None = None,
        http_client: AsyncHTTPClient | None = None,
    ):
        """Initialize an Anthropic model.

        Args:
            model_name: The name of the Anthropic model to use. List of model names available
                [here](https://docs.anthropic.com/en/docs/about-claude/models).
            api_key: The API key to use for authentication, if not provided, the `ANTHROPIC_API_KEY` environment variable
                will be used if available.
            anthropic_client: An existing
                [`AsyncAnthropic`](https://github.com/anthropics/anthropic-sdk-python?tab=readme-ov-file#async-usage)
                client to use, if provided, `api_key` and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._model_name = model_name
        if anthropic_client is not None:
            assert http_client is None, 'Cannot provide both `anthropic_client` and `http_client`'
            assert api_key is None, 'Cannot provide both `anthropic_client` and `api_key`'
            self.client = anthropic_client
        elif http_client is not None:
            self.client = AsyncAnthropic(api_key=api_key, http_client=http_client)
        else:
            self.client = AsyncAnthropic(api_key=api_key, http_client=cached_async_http_client())

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        check_allow_model_requests()
        response = await self._messages_create(
            messages, False, cast(AnthropicModelSettings, model_settings or {}), model_request_parameters
        )
        return self._process_response(response), _map_usage(response)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        check_allow_model_requests()
        response = await self._messages_create(
            messages, True, cast(AnthropicModelSettings, model_settings or {}), model_request_parameters
        )
        async with response:
            yield await self._process_streamed_response(response)

    @property
    def model_name(self) -> AnthropicModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[True],
        model_settings: AnthropicModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncStream[RawMessageStreamEvent]:
        pass

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[False],
        model_settings: AnthropicModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AnthropicMessage:
        pass

    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: bool,
        model_settings: AnthropicModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AnthropicMessage | AsyncStream[RawMessageStreamEvent]:
        # standalone function to make it easier to override
        tools = self._get_tools(model_request_parameters)
        tool_choice: ToolChoiceParam | None

        if not tools:
            tool_choice = None
        else:
            if not model_request_parameters.allow_text_result:
                tool_choice = {'type': 'any'}
            else:
                tool_choice = {'type': 'auto'}

            if (allow_parallel_tool_calls := model_settings.get('parallel_tool_calls')) is not None:
                tool_choice['disable_parallel_tool_use'] = not allow_parallel_tool_calls

        system_prompt, anthropic_messages = await self._map_message(messages)

        try:
            return await self.client.messages.create(
                max_tokens=model_settings.get('max_tokens', 1024),
                system=system_prompt or NOT_GIVEN,
                messages=anthropic_messages,
                model=self._model_name,
                tools=tools or NOT_GIVEN,
                tool_choice=tool_choice or NOT_GIVEN,
                stream=stream,
                temperature=model_settings.get('temperature', NOT_GIVEN),
                top_p=model_settings.get('top_p', NOT_GIVEN),
                timeout=model_settings.get('timeout', NOT_GIVEN),
                metadata=model_settings.get('anthropic_metadata', NOT_GIVEN),
            )
        except APIStatusError as e:
            if (status_code := e.status_code) >= 400:
                raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=e.body) from e
            raise

    def _process_response(self, response: AnthropicMessage) -> ModelResponse:
        """Process a non-streamed response, and prepare a message to return."""
        items: list[ModelResponsePart] = []
        for item in response.content:
            if isinstance(item, TextBlock):
                items.append(TextPart(content=item.text))
            else:
                assert isinstance(item, ToolUseBlock), 'unexpected item type'
                items.append(
                    ToolCallPart(
                        tool_name=item.name,
                        args=cast(dict[str, Any], item.input),
                        tool_call_id=item.id,
                    )
                )

        return ModelResponse(items, model_name=response.model)

    async def _process_streamed_response(self, response: AsyncStream[RawMessageStreamEvent]) -> StreamedResponse:
        peekable_response = _utils.PeekableAsyncStream(response)
        first_chunk = await peekable_response.peek()
        if isinstance(first_chunk, _utils.Unset):
            raise UnexpectedModelBehavior('Streamed response ended without content or tool calls')

        # Since Anthropic doesn't provide a timestamp in the message, we'll use the current time
        timestamp = datetime.now(tz=timezone.utc)
        return AnthropicStreamedResponse(
            _model_name=self._model_name, _response=peekable_response, _timestamp=timestamp
        )

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[ToolParam]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    async def _map_message(self, messages: list[ModelMessage]) -> tuple[str, list[MessageParam]]:
        """Just maps a `pydantic_ai.Message` to a `anthropic.types.MessageParam`."""
        system_prompt: str = ''
        anthropic_messages: list[MessageParam] = []
        for m in messages:
            if isinstance(m, ModelRequest):
                user_content_params: list[ToolResultBlockParam | TextBlockParam | ImageBlockParam] = []
                for request_part in m.parts:
                    if isinstance(request_part, SystemPromptPart):
                        system_prompt += request_part.content
                    elif isinstance(request_part, UserPromptPart):
                        async for content in self._map_user_prompt(request_part):
                            user_content_params.append(content)
                    elif isinstance(request_part, ToolReturnPart):
                        tool_result_block_param = ToolResultBlockParam(
                            tool_use_id=_guard_tool_call_id(t=request_part, model_source='Anthropic'),
                            type='tool_result',
                            content=request_part.model_response_str(),
                            is_error=False,
                        )
                        user_content_params.append(tool_result_block_param)
                    elif isinstance(request_part, RetryPromptPart):
                        if request_part.tool_name is None:
                            retry_param = TextBlockParam(type='text', text=request_part.model_response())
                        else:
                            retry_param = ToolResultBlockParam(
                                tool_use_id=_guard_tool_call_id(t=request_part, model_source='Anthropic'),
                                type='tool_result',
                                content=request_part.model_response(),
                                is_error=True,
                            )
                        user_content_params.append(retry_param)
                anthropic_messages.append(MessageParam(role='user', content=user_content_params))
            elif isinstance(m, ModelResponse):
                assistant_content_params: list[TextBlockParam | ToolUseBlockParam] = []
                for response_part in m.parts:
                    if isinstance(response_part, TextPart):
                        assistant_content_params.append(TextBlockParam(text=response_part.content, type='text'))
                    else:
                        tool_use_block_param = ToolUseBlockParam(
                            id=_guard_tool_call_id(t=response_part, model_source='Anthropic'),
                            type='tool_use',
                            name=response_part.tool_name,
                            input=response_part.args_as_dict(),
                        )
                        assistant_content_params.append(tool_use_block_param)
                anthropic_messages.append(MessageParam(role='assistant', content=assistant_content_params))
            else:
                assert_never(m)
        return system_prompt, anthropic_messages

    @staticmethod
    async def _map_user_prompt(part: UserPromptPart) -> AsyncGenerator[ImageBlockParam | TextBlockParam]:
        if isinstance(part.content, str):
            yield TextBlockParam(text=part.content, type='text')
        else:
            for item in part.content:
                if isinstance(item, str):
                    yield TextBlockParam(text=item, type='text')
                elif isinstance(item, BinaryContent):
                    if item.is_image:
                        yield ImageBlockParam(
                            source={'data': io.BytesIO(item.data), 'media_type': item.media_type, 'type': 'base64'},  # type: ignore
                            type='image',
                        )
                    else:
                        raise RuntimeError('Only images are supported for binary content')
                elif isinstance(item, ImageUrl):
                    try:
                        response = await cached_async_http_client().get(item.url)
                        response.raise_for_status()
                        yield ImageBlockParam(
                            source={
                                'data': io.BytesIO(response.content),
                                'media_type': item.media_type,
                                'type': 'base64',
                            },
                            type='image',
                        )
                    except ValueError:
                        # Download the file if can't find the mime type.
                        client = cached_async_http_client()
                        response = await client.get(item.url, follow_redirects=True)
                        response.raise_for_status()
                        base64_encoded = base64.b64encode(response.content).decode('utf-8')
                        if (mime_type := response.headers['Content-Type']) in (
                            'image/jpeg',
                            'image/png',
                            'image/gif',
                            'image/webp',
                        ):
                            yield ImageBlockParam(
                                source={'data': base64_encoded, 'media_type': mime_type, 'type': 'base64'},
                                type='image',
                            )
                        else:  # pragma: no cover
                            raise RuntimeError(f'Unsupported image type: {mime_type}')
                else:
                    raise RuntimeError(f'Unsupported content type: {type(item)}')

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> ToolParam:
        return {
            'name': f.name,
            'description': f.description,
            'input_schema': f.parameters_json_schema,
        }
```

#### __init__

```
__init__(
    model_name: AnthropicModelName,
    *,
    api_key: str | None = None,
    anthropic_client: AsyncAnthropic | None = None,
    http_client: AsyncClient | None = None
)
```

```
__init__(
    model_name: AnthropicModelName,
    *,
    api_key: str | None = None,
    anthropic_client: AsyncAnthropic | None = None,
    http_client: AsyncClient | None = None
)
```

[AnthropicModelName](https://ai.pydantic.dev#pydantic_ai.models.anthropic.AnthropicModelName)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Initialize an Anthropic model.

Parameters:

```
model_name
```

```
AnthropicModelName
```

[AnthropicModelName](https://ai.pydantic.dev#pydantic_ai.models.anthropic.AnthropicModelName)

The name of the Anthropic model to use. List of model names available
here.

```
api_key
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The API key to use for authentication, if not provided, the ANTHROPIC_API_KEY environment variable
will be used if available.

```
ANTHROPIC_API_KEY
```

```
None
```

```
anthropic_client
```

```
AsyncAnthropic | None
```

An existing
AsyncAnthropic
client to use, if provided, api_key and http_client must be None.

```
AsyncAnthropic
```

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
pydantic_ai_slim/pydantic_ai/models/anthropic.py
```

```
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
```

```
def __init__(
    self,
    model_name: AnthropicModelName,
    *,
    api_key: str | None = None,
    anthropic_client: AsyncAnthropic | None = None,
    http_client: AsyncHTTPClient | None = None,
):
    """Initialize an Anthropic model.

    Args:
        model_name: The name of the Anthropic model to use. List of model names available
            [here](https://docs.anthropic.com/en/docs/about-claude/models).
        api_key: The API key to use for authentication, if not provided, the `ANTHROPIC_API_KEY` environment variable
            will be used if available.
        anthropic_client: An existing
            [`AsyncAnthropic`](https://github.com/anthropics/anthropic-sdk-python?tab=readme-ov-file#async-usage)
            client to use, if provided, `api_key` and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._model_name = model_name
    if anthropic_client is not None:
        assert http_client is None, 'Cannot provide both `anthropic_client` and `http_client`'
        assert api_key is None, 'Cannot provide both `anthropic_client` and `api_key`'
        self.client = anthropic_client
    elif http_client is not None:
        self.client = AsyncAnthropic(api_key=api_key, http_client=http_client)
    else:
        self.client = AsyncAnthropic(api_key=api_key, http_client=cached_async_http_client())
```

```
def __init__(
    self,
    model_name: AnthropicModelName,
    *,
    api_key: str | None = None,
    anthropic_client: AsyncAnthropic | None = None,
    http_client: AsyncHTTPClient | None = None,
):
    """Initialize an Anthropic model.

    Args:
        model_name: The name of the Anthropic model to use. List of model names available
            [here](https://docs.anthropic.com/en/docs/about-claude/models).
        api_key: The API key to use for authentication, if not provided, the `ANTHROPIC_API_KEY` environment variable
            will be used if available.
        anthropic_client: An existing
            [`AsyncAnthropic`](https://github.com/anthropics/anthropic-sdk-python?tab=readme-ov-file#async-usage)
            client to use, if provided, `api_key` and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._model_name = model_name
    if anthropic_client is not None:
        assert http_client is None, 'Cannot provide both `anthropic_client` and `http_client`'
        assert api_key is None, 'Cannot provide both `anthropic_client` and `api_key`'
        self.client = anthropic_client
    elif http_client is not None:
        self.client = AsyncAnthropic(api_key=api_key, http_client=http_client)
    else:
        self.client = AsyncAnthropic(api_key=api_key, http_client=cached_async_http_client())
```

#### model_name

property

```
property
```

```
model_name: AnthropicModelName
```

```
model_name: AnthropicModelName
```

[AnthropicModelName](https://ai.pydantic.dev#pydantic_ai.models.anthropic.AnthropicModelName)

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

### AnthropicStreamedResponse

dataclass

```
dataclass
```

Bases: StreamedResponse

```
StreamedResponse
```

[StreamedResponse](https://ai.pydantic.dev/base/#pydantic_ai.models.StreamedResponse)

Implementation of StreamedResponse for Anthropic models.

```
StreamedResponse
```

```
pydantic_ai_slim/pydantic_ai/models/anthropic.py
```

```
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
```

```
@dataclass
class AnthropicStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for Anthropic models."""

    _model_name: AnthropicModelName
    _response: AsyncIterable[RawMessageStreamEvent]
    _timestamp: datetime

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        current_block: ContentBlock | None = None
        current_json: str = ''

        async for event in self._response:
            self._usage += _map_usage(event)

            if isinstance(event, RawContentBlockStartEvent):
                current_block = event.content_block
                if isinstance(current_block, TextBlock) and current_block.text:
                    yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=current_block.text)
                elif isinstance(current_block, ToolUseBlock):
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=current_block.id,
                        tool_name=current_block.name,
                        args=cast(dict[str, Any], current_block.input),
                        tool_call_id=current_block.id,
                    )
                    if maybe_event is not None:
                        yield maybe_event

            elif isinstance(event, RawContentBlockDeltaEvent):
                if isinstance(event.delta, TextDelta):
                    yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=event.delta.text)
                elif (
                    current_block and event.delta.type == 'input_json_delta' and isinstance(current_block, ToolUseBlock)
                ):
                    # Try to parse the JSON immediately, otherwise cache the value for later. This handles
                    # cases where the JSON is not currently valid but will be valid once we stream more tokens.
                    try:
                        parsed_args = json_loads(current_json + event.delta.partial_json)
                        current_json = ''
                    except JSONDecodeError:
                        current_json += event.delta.partial_json
                        continue

                    # For tool calls, we need to handle partial JSON updates
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=current_block.id,
                        tool_name='',
                        args=parsed_args,
                        tool_call_id=current_block.id,
                    )
                    if maybe_event is not None:
                        yield maybe_event

            elif isinstance(event, (RawContentBlockStopEvent, RawMessageStopEvent)):
                current_block = None

    @property
    def model_name(self) -> AnthropicModelName:
        """Get the model name of the response."""
        return self._model_name

    @property
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._timestamp
```

```
@dataclass
class AnthropicStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for Anthropic models."""

    _model_name: AnthropicModelName
    _response: AsyncIterable[RawMessageStreamEvent]
    _timestamp: datetime

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        current_block: ContentBlock | None = None
        current_json: str = ''

        async for event in self._response:
            self._usage += _map_usage(event)

            if isinstance(event, RawContentBlockStartEvent):
                current_block = event.content_block
                if isinstance(current_block, TextBlock) and current_block.text:
                    yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=current_block.text)
                elif isinstance(current_block, ToolUseBlock):
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=current_block.id,
                        tool_name=current_block.name,
                        args=cast(dict[str, Any], current_block.input),
                        tool_call_id=current_block.id,
                    )
                    if maybe_event is not None:
                        yield maybe_event

            elif isinstance(event, RawContentBlockDeltaEvent):
                if isinstance(event.delta, TextDelta):
                    yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=event.delta.text)
                elif (
                    current_block and event.delta.type == 'input_json_delta' and isinstance(current_block, ToolUseBlock)
                ):
                    # Try to parse the JSON immediately, otherwise cache the value for later. This handles
                    # cases where the JSON is not currently valid but will be valid once we stream more tokens.
                    try:
                        parsed_args = json_loads(current_json + event.delta.partial_json)
                        current_json = ''
                    except JSONDecodeError:
                        current_json += event.delta.partial_json
                        continue

                    # For tool calls, we need to handle partial JSON updates
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=current_block.id,
                        tool_name='',
                        args=parsed_args,
                        tool_call_id=current_block.id,
                    )
                    if maybe_event is not None:
                        yield maybe_event

            elif isinstance(event, (RawContentBlockStopEvent, RawMessageStopEvent)):
                current_block = None

    @property
    def model_name(self) -> AnthropicModelName:
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
model_name: AnthropicModelName
```

```
model_name: AnthropicModelName
```

[AnthropicModelName](https://ai.pydantic.dev#pydantic_ai.models.anthropic.AnthropicModelName)

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

