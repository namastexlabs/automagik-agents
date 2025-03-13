# pydantic_ai.models.openai

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.openai

```
pydantic_ai.models.openai
```

## Setup

For details on how to set up authentication with this model, see model configuration for OpenAI.

[](https://ai.pydantic.dev)

### OpenAIModelName

module-attribute

```
module-attribute
```

```
OpenAIModelName = Union[str, ChatModel]
```

```
OpenAIModelName = Union[str, ChatModel]
```

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Possible OpenAI model names.

Since OpenAI supports a variety of date-stamped models, we explicitly list the latest models but
allow any name in the type hints.
See the OpenAI docs for a full list.

Using this more broad type for the model name instead of the ChatModel definition
allows this model to be used more easily with other model types (ie, Ollama, Deepseek).

### OpenAIModelSettings

Bases: ModelSettings

```
ModelSettings
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Settings used for an OpenAI model request.

```
pydantic_ai_slim/pydantic_ai/models/openai.py
```

```
77
78
79
80
81
82
83
84
85
```

```
class OpenAIModelSettings(ModelSettings):
    """Settings used for an OpenAI model request."""

    openai_reasoning_effort: chat.ChatCompletionReasoningEffort
    """
    Constrains effort on reasoning for [reasoning models](https://platform.openai.com/docs/guides/reasoning).
    Currently supported values are `low`, `medium`, and `high`. Reducing reasoning effort can
    result in faster responses and fewer tokens used on reasoning in a response.
    """
```

```
class OpenAIModelSettings(ModelSettings):
    """Settings used for an OpenAI model request."""

    openai_reasoning_effort: chat.ChatCompletionReasoningEffort
    """
    Constrains effort on reasoning for [reasoning models](https://platform.openai.com/docs/guides/reasoning).
    Currently supported values are `low`, `medium`, and `high`. Reducing reasoning effort can
    result in faster responses and fewer tokens used on reasoning in a response.
    """
```

#### openai_reasoning_effort

instance-attribute

```
instance-attribute
```

```
openai_reasoning_effort: ChatCompletionReasoningEffort
```

```
openai_reasoning_effort: ChatCompletionReasoningEffort
```

Constrains effort on reasoning for reasoning models.
Currently supported values are low, medium, and high. Reducing reasoning effort can
result in faster responses and fewer tokens used on reasoning in a response.

```
low
```

```
medium
```

```
high
```

### OpenAIModel

dataclass

```
dataclass
```

Bases: Model

```
Model
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

A model that uses the OpenAI API.

Internally, this uses the OpenAI Python client to interact with the API.

Apart from __init__, all methods are private or match those of the base class.

```
__init__
```

```
pydantic_ai_slim/pydantic_ai/models/openai.py
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
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
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
```

```
@dataclass(init=False)
class OpenAIModel(Model):
    """A model that uses the OpenAI API.

    Internally, this uses the [OpenAI Python client](https://github.com/openai/openai-python) to interact with the API.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    client: AsyncOpenAI = field(repr=False)
    system_prompt_role: OpenAISystemPromptRole | None = field(default=None)

    _model_name: OpenAIModelName = field(repr=False)
    _system: str | None = field(repr=False)

    @overload
    def __init__(
        self,
        model_name: OpenAIModelName,
        *,
        provider: Literal['openai', 'deepseek'] | Provider[AsyncOpenAI] = 'openai',
        system_prompt_role: OpenAISystemPromptRole | None = None,
        system: str | None = 'openai',
    ) -> None: ...

    @deprecated('Use the `provider` parameter instead of `base_url`, `api_key`, `openai_client` and `http_client`.')
    @overload
    def __init__(
        self,
        model_name: OpenAIModelName,
        *,
        provider: None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncHTTPClient | None = None,
        system_prompt_role: OpenAISystemPromptRole | None = None,
        system: str | None = 'openai',
    ) -> None: ...

    def __init__(
        self,
        model_name: OpenAIModelName,
        *,
        provider: Literal['openai', 'deepseek'] | Provider[AsyncOpenAI] | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncHTTPClient | None = None,
        system_prompt_role: OpenAISystemPromptRole | None = None,
        system: str | None = 'openai',
    ):
        """Initialize an OpenAI model.

        Args:
            model_name: The name of the OpenAI model to use. List of model names available
                [here](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7)
                (Unfortunately, despite being ask to do so, OpenAI do not provide `.inv` files for their API).
            provider: The provider to use. Defaults to `'openai'`.
            base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
                will be used if available. Otherwise, defaults to OpenAI's base url.
            api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
                will be used if available.
            openai_client: An existing
                [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
                client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
            system_prompt_role: The role to use for the system prompt message. If not provided, defaults to `'system'`.
                In the future, this may be inferred from the model name.
            system: The model provider used, defaults to `openai`. This is for observability purposes, you must
                customize the `base_url` and `api_key` to use a different provider.
        """
        self._model_name = model_name

        if provider is not None:
            if isinstance(provider, str):
                self.client = infer_provider(provider).client
            else:
                self.client = provider.client
        else:  # pragma: no cover
            # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
            # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
            if (
                api_key is None
                and 'OPENAI_API_KEY' not in os.environ
                and base_url is not None
                and openai_client is None
            ):
                api_key = 'api-key-not-set'

            if openai_client is not None:
                assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
                assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
                assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
                self.client = openai_client
            elif http_client is not None:
                self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=http_client)
            else:
                self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=cached_async_http_client())
        self.system_prompt_role = system_prompt_role
        self._system = system

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        check_allow_model_requests()
        response = await self._completions_create(
            messages, False, cast(OpenAIModelSettings, model_settings or {}), model_request_parameters
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
        response = await self._completions_create(
            messages, True, cast(OpenAIModelSettings, model_settings or {}), model_request_parameters
        )
        async with response:
            yield await self._process_streamed_response(response)

    @property
    def model_name(self) -> OpenAIModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    @overload
    async def _completions_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[True],
        model_settings: OpenAIModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncStream[ChatCompletionChunk]:
        pass

    @overload
    async def _completions_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[False],
        model_settings: OpenAIModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> chat.ChatCompletion:
        pass

    async def _completions_create(
        self,
        messages: list[ModelMessage],
        stream: bool,
        model_settings: OpenAIModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> chat.ChatCompletion | AsyncStream[ChatCompletionChunk]:
        tools = self._get_tools(model_request_parameters)

        # standalone function to make it easier to override
        if not tools:
            tool_choice: Literal['none', 'required', 'auto'] | None = None
        elif not model_request_parameters.allow_text_result:
            tool_choice = 'required'
        else:
            tool_choice = 'auto'

        openai_messages: list[chat.ChatCompletionMessageParam] = []
        for m in messages:
            async for msg in self._map_message(m):
                openai_messages.append(msg)

        try:
            return await self.client.chat.completions.create(
                model=self._model_name,
                messages=openai_messages,
                n=1,
                parallel_tool_calls=model_settings.get('parallel_tool_calls', NOT_GIVEN),
                tools=tools or NOT_GIVEN,
                tool_choice=tool_choice or NOT_GIVEN,
                stream=stream,
                stream_options={'include_usage': True} if stream else NOT_GIVEN,
                max_tokens=model_settings.get('max_tokens', NOT_GIVEN),
                temperature=model_settings.get('temperature', NOT_GIVEN),
                top_p=model_settings.get('top_p', NOT_GIVEN),
                timeout=model_settings.get('timeout', NOT_GIVEN),
                seed=model_settings.get('seed', NOT_GIVEN),
                presence_penalty=model_settings.get('presence_penalty', NOT_GIVEN),
                frequency_penalty=model_settings.get('frequency_penalty', NOT_GIVEN),
                logit_bias=model_settings.get('logit_bias', NOT_GIVEN),
                reasoning_effort=model_settings.get('openai_reasoning_effort', NOT_GIVEN),
            )
        except APIStatusError as e:
            if (status_code := e.status_code) >= 400:
                raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=e.body) from e
            raise

    def _process_response(self, response: chat.ChatCompletion) -> ModelResponse:
        """Process a non-streamed response, and prepare a message to return."""
        timestamp = datetime.fromtimestamp(response.created, tz=timezone.utc)
        choice = response.choices[0]
        items: list[ModelResponsePart] = []
        if choice.message.content is not None:
            items.append(TextPart(choice.message.content))
        if choice.message.tool_calls is not None:
            for c in choice.message.tool_calls:
                items.append(ToolCallPart(c.function.name, c.function.arguments, c.id))
        return ModelResponse(items, model_name=response.model, timestamp=timestamp)

    async def _process_streamed_response(self, response: AsyncStream[ChatCompletionChunk]) -> OpenAIStreamedResponse:
        """Process a streamed response, and prepare a streaming response to return."""
        peekable_response = _utils.PeekableAsyncStream(response)
        first_chunk = await peekable_response.peek()
        if isinstance(first_chunk, _utils.Unset):
            raise UnexpectedModelBehavior('Streamed response ended without content or tool calls')

        return OpenAIStreamedResponse(
            _model_name=self._model_name,
            _response=peekable_response,
            _timestamp=datetime.fromtimestamp(first_chunk.created, tz=timezone.utc),
        )

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[chat.ChatCompletionToolParam]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    async def _map_message(self, message: ModelMessage) -> AsyncIterable[chat.ChatCompletionMessageParam]:
        """Just maps a `pydantic_ai.Message` to a `openai.types.ChatCompletionMessageParam`."""
        if isinstance(message, ModelRequest):
            async for item in self._map_user_message(message):
                yield item
        elif isinstance(message, ModelResponse):
            texts: list[str] = []
            tool_calls: list[chat.ChatCompletionMessageToolCallParam] = []
            for item in message.parts:
                if isinstance(item, TextPart):
                    texts.append(item.content)
                elif isinstance(item, ToolCallPart):
                    tool_calls.append(self._map_tool_call(item))
                else:
                    assert_never(item)
            message_param = chat.ChatCompletionAssistantMessageParam(role='assistant')
            if texts:
                # Note: model responses from this model should only have one text item, so the following
                # shouldn't merge multiple texts into one unless you switch models between runs:
                message_param['content'] = '\n\n'.join(texts)
            if tool_calls:
                message_param['tool_calls'] = tool_calls
            yield message_param
        else:
            assert_never(message)

    @staticmethod
    def _map_tool_call(t: ToolCallPart) -> chat.ChatCompletionMessageToolCallParam:
        return chat.ChatCompletionMessageToolCallParam(
            id=_guard_tool_call_id(t=t, model_source='OpenAI'),
            type='function',
            function={'name': t.tool_name, 'arguments': t.args_as_json_str()},
        )

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> chat.ChatCompletionToolParam:
        return {
            'type': 'function',
            'function': {
                'name': f.name,
                'description': f.description,
                'parameters': f.parameters_json_schema,
            },
        }

    async def _map_user_message(self, message: ModelRequest) -> AsyncIterable[chat.ChatCompletionMessageParam]:
        for part in message.parts:
            if isinstance(part, SystemPromptPart):
                if self.system_prompt_role == 'developer':
                    yield chat.ChatCompletionDeveloperMessageParam(role='developer', content=part.content)
                elif self.system_prompt_role == 'user':
                    yield chat.ChatCompletionUserMessageParam(role='user', content=part.content)
                else:
                    yield chat.ChatCompletionSystemMessageParam(role='system', content=part.content)
            elif isinstance(part, UserPromptPart):
                yield await self._map_user_prompt(part)
            elif isinstance(part, ToolReturnPart):
                yield chat.ChatCompletionToolMessageParam(
                    role='tool',
                    tool_call_id=_guard_tool_call_id(t=part, model_source='OpenAI'),
                    content=part.model_response_str(),
                )
            elif isinstance(part, RetryPromptPart):
                if part.tool_name is None:
                    yield chat.ChatCompletionUserMessageParam(role='user', content=part.model_response())
                else:
                    yield chat.ChatCompletionToolMessageParam(
                        role='tool',
                        tool_call_id=_guard_tool_call_id(t=part, model_source='OpenAI'),
                        content=part.model_response(),
                    )
            else:
                assert_never(part)

    @staticmethod
    async def _map_user_prompt(part: UserPromptPart) -> chat.ChatCompletionUserMessageParam:
        content: str | list[ChatCompletionContentPartParam]
        if isinstance(part.content, str):
            content = part.content
        else:
            content = []
            for item in part.content:
                if isinstance(item, str):
                    content.append(ChatCompletionContentPartTextParam(text=item, type='text'))
                elif isinstance(item, ImageUrl):
                    image_url = ImageURL(url=item.url)
                    content.append(ChatCompletionContentPartImageParam(image_url=image_url, type='image_url'))
                elif isinstance(item, BinaryContent):
                    base64_encoded = base64.b64encode(item.data).decode('utf-8')
                    if item.is_image:
                        image_url = ImageURL(url=f'data:{item.media_type};base64,{base64_encoded}')
                        content.append(ChatCompletionContentPartImageParam(image_url=image_url, type='image_url'))
                    elif item.is_audio:
                        audio = InputAudio(data=base64_encoded, format=item.audio_format)
                        content.append(ChatCompletionContentPartInputAudioParam(input_audio=audio, type='input_audio'))
                    else:  # pragma: no cover
                        raise RuntimeError(f'Unsupported binary content type: {item.media_type}')
                elif isinstance(item, AudioUrl):  # pragma: no cover
                    client = cached_async_http_client()
                    response = await client.get(item.url)
                    response.raise_for_status()
                    base64_encoded = base64.b64encode(response.content).decode('utf-8')
                    audio = InputAudio(data=base64_encoded, format=response.headers.get('content-type'))
                    content.append(ChatCompletionContentPartInputAudioParam(input_audio=audio, type='input_audio'))
                else:
                    assert_never(item)
        return chat.ChatCompletionUserMessageParam(role='user', content=content)
```

```
@dataclass(init=False)
class OpenAIModel(Model):
    """A model that uses the OpenAI API.

    Internally, this uses the [OpenAI Python client](https://github.com/openai/openai-python) to interact with the API.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    client: AsyncOpenAI = field(repr=False)
    system_prompt_role: OpenAISystemPromptRole | None = field(default=None)

    _model_name: OpenAIModelName = field(repr=False)
    _system: str | None = field(repr=False)

    @overload
    def __init__(
        self,
        model_name: OpenAIModelName,
        *,
        provider: Literal['openai', 'deepseek'] | Provider[AsyncOpenAI] = 'openai',
        system_prompt_role: OpenAISystemPromptRole | None = None,
        system: str | None = 'openai',
    ) -> None: ...

    @deprecated('Use the `provider` parameter instead of `base_url`, `api_key`, `openai_client` and `http_client`.')
    @overload
    def __init__(
        self,
        model_name: OpenAIModelName,
        *,
        provider: None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncHTTPClient | None = None,
        system_prompt_role: OpenAISystemPromptRole | None = None,
        system: str | None = 'openai',
    ) -> None: ...

    def __init__(
        self,
        model_name: OpenAIModelName,
        *,
        provider: Literal['openai', 'deepseek'] | Provider[AsyncOpenAI] | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncHTTPClient | None = None,
        system_prompt_role: OpenAISystemPromptRole | None = None,
        system: str | None = 'openai',
    ):
        """Initialize an OpenAI model.

        Args:
            model_name: The name of the OpenAI model to use. List of model names available
                [here](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7)
                (Unfortunately, despite being ask to do so, OpenAI do not provide `.inv` files for their API).
            provider: The provider to use. Defaults to `'openai'`.
            base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
                will be used if available. Otherwise, defaults to OpenAI's base url.
            api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
                will be used if available.
            openai_client: An existing
                [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
                client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
            system_prompt_role: The role to use for the system prompt message. If not provided, defaults to `'system'`.
                In the future, this may be inferred from the model name.
            system: The model provider used, defaults to `openai`. This is for observability purposes, you must
                customize the `base_url` and `api_key` to use a different provider.
        """
        self._model_name = model_name

        if provider is not None:
            if isinstance(provider, str):
                self.client = infer_provider(provider).client
            else:
                self.client = provider.client
        else:  # pragma: no cover
            # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
            # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
            if (
                api_key is None
                and 'OPENAI_API_KEY' not in os.environ
                and base_url is not None
                and openai_client is None
            ):
                api_key = 'api-key-not-set'

            if openai_client is not None:
                assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
                assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
                assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
                self.client = openai_client
            elif http_client is not None:
                self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=http_client)
            else:
                self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=cached_async_http_client())
        self.system_prompt_role = system_prompt_role
        self._system = system

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        check_allow_model_requests()
        response = await self._completions_create(
            messages, False, cast(OpenAIModelSettings, model_settings or {}), model_request_parameters
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
        response = await self._completions_create(
            messages, True, cast(OpenAIModelSettings, model_settings or {}), model_request_parameters
        )
        async with response:
            yield await self._process_streamed_response(response)

    @property
    def model_name(self) -> OpenAIModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    @overload
    async def _completions_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[True],
        model_settings: OpenAIModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncStream[ChatCompletionChunk]:
        pass

    @overload
    async def _completions_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[False],
        model_settings: OpenAIModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> chat.ChatCompletion:
        pass

    async def _completions_create(
        self,
        messages: list[ModelMessage],
        stream: bool,
        model_settings: OpenAIModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> chat.ChatCompletion | AsyncStream[ChatCompletionChunk]:
        tools = self._get_tools(model_request_parameters)

        # standalone function to make it easier to override
        if not tools:
            tool_choice: Literal['none', 'required', 'auto'] | None = None
        elif not model_request_parameters.allow_text_result:
            tool_choice = 'required'
        else:
            tool_choice = 'auto'

        openai_messages: list[chat.ChatCompletionMessageParam] = []
        for m in messages:
            async for msg in self._map_message(m):
                openai_messages.append(msg)

        try:
            return await self.client.chat.completions.create(
                model=self._model_name,
                messages=openai_messages,
                n=1,
                parallel_tool_calls=model_settings.get('parallel_tool_calls', NOT_GIVEN),
                tools=tools or NOT_GIVEN,
                tool_choice=tool_choice or NOT_GIVEN,
                stream=stream,
                stream_options={'include_usage': True} if stream else NOT_GIVEN,
                max_tokens=model_settings.get('max_tokens', NOT_GIVEN),
                temperature=model_settings.get('temperature', NOT_GIVEN),
                top_p=model_settings.get('top_p', NOT_GIVEN),
                timeout=model_settings.get('timeout', NOT_GIVEN),
                seed=model_settings.get('seed', NOT_GIVEN),
                presence_penalty=model_settings.get('presence_penalty', NOT_GIVEN),
                frequency_penalty=model_settings.get('frequency_penalty', NOT_GIVEN),
                logit_bias=model_settings.get('logit_bias', NOT_GIVEN),
                reasoning_effort=model_settings.get('openai_reasoning_effort', NOT_GIVEN),
            )
        except APIStatusError as e:
            if (status_code := e.status_code) >= 400:
                raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=e.body) from e
            raise

    def _process_response(self, response: chat.ChatCompletion) -> ModelResponse:
        """Process a non-streamed response, and prepare a message to return."""
        timestamp = datetime.fromtimestamp(response.created, tz=timezone.utc)
        choice = response.choices[0]
        items: list[ModelResponsePart] = []
        if choice.message.content is not None:
            items.append(TextPart(choice.message.content))
        if choice.message.tool_calls is not None:
            for c in choice.message.tool_calls:
                items.append(ToolCallPart(c.function.name, c.function.arguments, c.id))
        return ModelResponse(items, model_name=response.model, timestamp=timestamp)

    async def _process_streamed_response(self, response: AsyncStream[ChatCompletionChunk]) -> OpenAIStreamedResponse:
        """Process a streamed response, and prepare a streaming response to return."""
        peekable_response = _utils.PeekableAsyncStream(response)
        first_chunk = await peekable_response.peek()
        if isinstance(first_chunk, _utils.Unset):
            raise UnexpectedModelBehavior('Streamed response ended without content or tool calls')

        return OpenAIStreamedResponse(
            _model_name=self._model_name,
            _response=peekable_response,
            _timestamp=datetime.fromtimestamp(first_chunk.created, tz=timezone.utc),
        )

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[chat.ChatCompletionToolParam]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    async def _map_message(self, message: ModelMessage) -> AsyncIterable[chat.ChatCompletionMessageParam]:
        """Just maps a `pydantic_ai.Message` to a `openai.types.ChatCompletionMessageParam`."""
        if isinstance(message, ModelRequest):
            async for item in self._map_user_message(message):
                yield item
        elif isinstance(message, ModelResponse):
            texts: list[str] = []
            tool_calls: list[chat.ChatCompletionMessageToolCallParam] = []
            for item in message.parts:
                if isinstance(item, TextPart):
                    texts.append(item.content)
                elif isinstance(item, ToolCallPart):
                    tool_calls.append(self._map_tool_call(item))
                else:
                    assert_never(item)
            message_param = chat.ChatCompletionAssistantMessageParam(role='assistant')
            if texts:
                # Note: model responses from this model should only have one text item, so the following
                # shouldn't merge multiple texts into one unless you switch models between runs:
                message_param['content'] = '\n\n'.join(texts)
            if tool_calls:
                message_param['tool_calls'] = tool_calls
            yield message_param
        else:
            assert_never(message)

    @staticmethod
    def _map_tool_call(t: ToolCallPart) -> chat.ChatCompletionMessageToolCallParam:
        return chat.ChatCompletionMessageToolCallParam(
            id=_guard_tool_call_id(t=t, model_source='OpenAI'),
            type='function',
            function={'name': t.tool_name, 'arguments': t.args_as_json_str()},
        )

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> chat.ChatCompletionToolParam:
        return {
            'type': 'function',
            'function': {
                'name': f.name,
                'description': f.description,
                'parameters': f.parameters_json_schema,
            },
        }

    async def _map_user_message(self, message: ModelRequest) -> AsyncIterable[chat.ChatCompletionMessageParam]:
        for part in message.parts:
            if isinstance(part, SystemPromptPart):
                if self.system_prompt_role == 'developer':
                    yield chat.ChatCompletionDeveloperMessageParam(role='developer', content=part.content)
                elif self.system_prompt_role == 'user':
                    yield chat.ChatCompletionUserMessageParam(role='user', content=part.content)
                else:
                    yield chat.ChatCompletionSystemMessageParam(role='system', content=part.content)
            elif isinstance(part, UserPromptPart):
                yield await self._map_user_prompt(part)
            elif isinstance(part, ToolReturnPart):
                yield chat.ChatCompletionToolMessageParam(
                    role='tool',
                    tool_call_id=_guard_tool_call_id(t=part, model_source='OpenAI'),
                    content=part.model_response_str(),
                )
            elif isinstance(part, RetryPromptPart):
                if part.tool_name is None:
                    yield chat.ChatCompletionUserMessageParam(role='user', content=part.model_response())
                else:
                    yield chat.ChatCompletionToolMessageParam(
                        role='tool',
                        tool_call_id=_guard_tool_call_id(t=part, model_source='OpenAI'),
                        content=part.model_response(),
                    )
            else:
                assert_never(part)

    @staticmethod
    async def _map_user_prompt(part: UserPromptPart) -> chat.ChatCompletionUserMessageParam:
        content: str | list[ChatCompletionContentPartParam]
        if isinstance(part.content, str):
            content = part.content
        else:
            content = []
            for item in part.content:
                if isinstance(item, str):
                    content.append(ChatCompletionContentPartTextParam(text=item, type='text'))
                elif isinstance(item, ImageUrl):
                    image_url = ImageURL(url=item.url)
                    content.append(ChatCompletionContentPartImageParam(image_url=image_url, type='image_url'))
                elif isinstance(item, BinaryContent):
                    base64_encoded = base64.b64encode(item.data).decode('utf-8')
                    if item.is_image:
                        image_url = ImageURL(url=f'data:{item.media_type};base64,{base64_encoded}')
                        content.append(ChatCompletionContentPartImageParam(image_url=image_url, type='image_url'))
                    elif item.is_audio:
                        audio = InputAudio(data=base64_encoded, format=item.audio_format)
                        content.append(ChatCompletionContentPartInputAudioParam(input_audio=audio, type='input_audio'))
                    else:  # pragma: no cover
                        raise RuntimeError(f'Unsupported binary content type: {item.media_type}')
                elif isinstance(item, AudioUrl):  # pragma: no cover
                    client = cached_async_http_client()
                    response = await client.get(item.url)
                    response.raise_for_status()
                    base64_encoded = base64.b64encode(response.content).decode('utf-8')
                    audio = InputAudio(data=base64_encoded, format=response.headers.get('content-type'))
                    content.append(ChatCompletionContentPartInputAudioParam(input_audio=audio, type='input_audio'))
                else:
                    assert_never(item)
        return chat.ChatCompletionUserMessageParam(role='user', content=content)
```

#### __init__

```
__init__(
    model_name: OpenAIModelName,
    *,
    provider: (
        Literal["openai", "deepseek"]
        | Provider[AsyncOpenAI]
    ) = "openai",
    system_prompt_role: (
        OpenAISystemPromptRole | None
    ) = None,
    system: str | None = "openai"
) -> None
```

```
__init__(
    model_name: OpenAIModelName,
    *,
    provider: (
        Literal["openai", "deepseek"]
        | Provider[AsyncOpenAI]
    ) = "openai",
    system_prompt_role: (
        OpenAISystemPromptRole | None
    ) = None,
    system: str | None = "openai"
) -> None
```

[OpenAIModelName](https://ai.pydantic.dev#pydantic_ai.models.openai.OpenAIModelName)

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
__init__(
    model_name: OpenAIModelName,
    *,
    provider: None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncClient | None = None,
    system_prompt_role: (
        OpenAISystemPromptRole | None
    ) = None,
    system: str | None = "openai"
) -> None
```

```
__init__(
    model_name: OpenAIModelName,
    *,
    provider: None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncClient | None = None,
    system_prompt_role: (
        OpenAISystemPromptRole | None
    ) = None,
    system: str | None = "openai"
) -> None
```

[OpenAIModelName](https://ai.pydantic.dev#pydantic_ai.models.openai.OpenAIModelName)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
__init__(
    model_name: OpenAIModelName,
    *,
    provider: (
        Literal["openai", "deepseek"]
        | Provider[AsyncOpenAI]
        | None
    ) = None,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncClient | None = None,
    system_prompt_role: (
        OpenAISystemPromptRole | None
    ) = None,
    system: str | None = "openai"
)
```

```
__init__(
    model_name: OpenAIModelName,
    *,
    provider: (
        Literal["openai", "deepseek"]
        | Provider[AsyncOpenAI]
        | None
    ) = None,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncClient | None = None,
    system_prompt_role: (
        OpenAISystemPromptRole | None
    ) = None,
    system: str | None = "openai"
)
```

[OpenAIModelName](https://ai.pydantic.dev#pydantic_ai.models.openai.OpenAIModelName)

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Initialize an OpenAI model.

Parameters:

```
model_name
```

```
OpenAIModelName
```

[OpenAIModelName](https://ai.pydantic.dev#pydantic_ai.models.openai.OpenAIModelName)

The name of the OpenAI model to use. List of model names available
here
(Unfortunately, despite being ask to do so, OpenAI do not provide .inv files for their API).

```
.inv
```

```
provider
```

```
Literal['openai', 'deepseek'] | Provider[AsyncOpenAI] | None
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

The provider to use. Defaults to 'openai'.

```
'openai'
```

```
None
```

```
base_url
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The base url for the OpenAI requests. If not provided, the OPENAI_BASE_URL environment variable
will be used if available. Otherwise, defaults to OpenAI's base url.

```
OPENAI_BASE_URL
```

```
None
```

```
api_key
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The API key to use for authentication, if not provided, the OPENAI_API_KEY environment variable
will be used if available.

```
OPENAI_API_KEY
```

```
None
```

```
openai_client
```

```
AsyncOpenAI | None
```

An existing
AsyncOpenAI
client to use. If provided, base_url, api_key, and http_client must be None.

```
AsyncOpenAI
```

```
base_url
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
system_prompt_role
```

```
OpenAISystemPromptRole | None
```

The role to use for the system prompt message. If not provided, defaults to 'system'.
In the future, this may be inferred from the model name.

```
'system'
```

```
None
```

```
system
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The model provider used, defaults to openai. This is for observability purposes, you must
customize the base_url and api_key to use a different provider.

```
openai
```

```
base_url
```

```
api_key
```

```
'openai'
```

```
pydantic_ai_slim/pydantic_ai/models/openai.py
```

```
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
```

```
def __init__(
    self,
    model_name: OpenAIModelName,
    *,
    provider: Literal['openai', 'deepseek'] | Provider[AsyncOpenAI] | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncHTTPClient | None = None,
    system_prompt_role: OpenAISystemPromptRole | None = None,
    system: str | None = 'openai',
):
    """Initialize an OpenAI model.

    Args:
        model_name: The name of the OpenAI model to use. List of model names available
            [here](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7)
            (Unfortunately, despite being ask to do so, OpenAI do not provide `.inv` files for their API).
        provider: The provider to use. Defaults to `'openai'`.
        base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
            will be used if available. Otherwise, defaults to OpenAI's base url.
        api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
            will be used if available.
        openai_client: An existing
            [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
            client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        system_prompt_role: The role to use for the system prompt message. If not provided, defaults to `'system'`.
            In the future, this may be inferred from the model name.
        system: The model provider used, defaults to `openai`. This is for observability purposes, you must
            customize the `base_url` and `api_key` to use a different provider.
    """
    self._model_name = model_name

    if provider is not None:
        if isinstance(provider, str):
            self.client = infer_provider(provider).client
        else:
            self.client = provider.client
    else:  # pragma: no cover
        # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
        # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
        if (
            api_key is None
            and 'OPENAI_API_KEY' not in os.environ
            and base_url is not None
            and openai_client is None
        ):
            api_key = 'api-key-not-set'

        if openai_client is not None:
            assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
            assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
            assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
            self.client = openai_client
        elif http_client is not None:
            self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=http_client)
        else:
            self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=cached_async_http_client())
    self.system_prompt_role = system_prompt_role
    self._system = system
```

```
def __init__(
    self,
    model_name: OpenAIModelName,
    *,
    provider: Literal['openai', 'deepseek'] | Provider[AsyncOpenAI] | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncHTTPClient | None = None,
    system_prompt_role: OpenAISystemPromptRole | None = None,
    system: str | None = 'openai',
):
    """Initialize an OpenAI model.

    Args:
        model_name: The name of the OpenAI model to use. List of model names available
            [here](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7)
            (Unfortunately, despite being ask to do so, OpenAI do not provide `.inv` files for their API).
        provider: The provider to use. Defaults to `'openai'`.
        base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
            will be used if available. Otherwise, defaults to OpenAI's base url.
        api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
            will be used if available.
        openai_client: An existing
            [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
            client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        system_prompt_role: The role to use for the system prompt message. If not provided, defaults to `'system'`.
            In the future, this may be inferred from the model name.
        system: The model provider used, defaults to `openai`. This is for observability purposes, you must
            customize the `base_url` and `api_key` to use a different provider.
    """
    self._model_name = model_name

    if provider is not None:
        if isinstance(provider, str):
            self.client = infer_provider(provider).client
        else:
            self.client = provider.client
    else:  # pragma: no cover
        # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
        # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
        if (
            api_key is None
            and 'OPENAI_API_KEY' not in os.environ
            and base_url is not None
            and openai_client is None
        ):
            api_key = 'api-key-not-set'

        if openai_client is not None:
            assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
            assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
            assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
            self.client = openai_client
        elif http_client is not None:
            self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=http_client)
        else:
            self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, http_client=cached_async_http_client())
    self.system_prompt_role = system_prompt_role
    self._system = system
```

#### model_name

property

```
property
```

```
model_name: OpenAIModelName
```

```
model_name: OpenAIModelName
```

[OpenAIModelName](https://ai.pydantic.dev#pydantic_ai.models.openai.OpenAIModelName)

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

### OpenAIStreamedResponse

dataclass

```
dataclass
```

Bases: StreamedResponse

```
StreamedResponse
```

[StreamedResponse](https://ai.pydantic.dev/base/#pydantic_ai.models.StreamedResponse)

Implementation of StreamedResponse for OpenAI models.

```
StreamedResponse
```

```
pydantic_ai_slim/pydantic_ai/models/openai.py
```

```
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
```

```
@dataclass
class OpenAIStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for OpenAI models."""

    _model_name: OpenAIModelName
    _response: AsyncIterable[ChatCompletionChunk]
    _timestamp: datetime

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        async for chunk in self._response:
            self._usage += _map_usage(chunk)

            try:
                choice = chunk.choices[0]
            except IndexError:
                continue

            # Handle the text part of the response
            content = choice.delta.content
            if content is not None:
                yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=content)

            for dtc in choice.delta.tool_calls or []:
                maybe_event = self._parts_manager.handle_tool_call_delta(
                    vendor_part_id=dtc.index,
                    tool_name=dtc.function and dtc.function.name,
                    args=dtc.function and dtc.function.arguments,
                    tool_call_id=dtc.id,
                )
                if maybe_event is not None:
                    yield maybe_event

    @property
    def model_name(self) -> OpenAIModelName:
        """Get the model name of the response."""
        return self._model_name

    @property
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._timestamp
```

```
@dataclass
class OpenAIStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for OpenAI models."""

    _model_name: OpenAIModelName
    _response: AsyncIterable[ChatCompletionChunk]
    _timestamp: datetime

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        async for chunk in self._response:
            self._usage += _map_usage(chunk)

            try:
                choice = chunk.choices[0]
            except IndexError:
                continue

            # Handle the text part of the response
            content = choice.delta.content
            if content is not None:
                yield self._parts_manager.handle_text_delta(vendor_part_id='content', content=content)

            for dtc in choice.delta.tool_calls or []:
                maybe_event = self._parts_manager.handle_tool_call_delta(
                    vendor_part_id=dtc.index,
                    tool_name=dtc.function and dtc.function.name,
                    args=dtc.function and dtc.function.arguments,
                    tool_call_id=dtc.id,
                )
                if maybe_event is not None:
                    yield maybe_event

    @property
    def model_name(self) -> OpenAIModelName:
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
model_name: OpenAIModelName
```

```
model_name: OpenAIModelName
```

[OpenAIModelName](https://ai.pydantic.dev#pydantic_ai.models.openai.OpenAIModelName)

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

