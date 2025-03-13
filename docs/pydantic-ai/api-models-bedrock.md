# pydantic_ai.models.bedrock

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.bedrock

```
pydantic_ai.models.bedrock
```

## Setup

For details on how to set up authentication with this model, see model configuration for Bedrock.

[](https://ai.pydantic.dev)

### LatestBedrockModelNames

module-attribute

```
module-attribute
```

```
LatestBedrockModelNames = Literal[
    "amazon.titan-tg1-large",
    "amazon.titan-text-lite-v1",
    "amazon.titan-text-express-v1",
    "us.amazon.nova-pro-v1:0",
    "us.amazon.nova-lite-v1:0",
    "us.amazon.nova-micro-v1:0",
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-3-5-haiku-20241022-v1:0",
    "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    "anthropic.claude-instant-v1",
    "anthropic.claude-v2:1",
    "anthropic.claude-v2",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "us.anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "us.anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "us.anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "us.anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-7-sonnet-20250219-v1:0",
    "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "cohere.command-text-v14",
    "cohere.command-r-v1:0",
    "cohere.command-r-plus-v1:0",
    "cohere.command-light-text-v14",
    "meta.llama3-8b-instruct-v1:0",
    "meta.llama3-70b-instruct-v1:0",
    "meta.llama3-1-8b-instruct-v1:0",
    "us.meta.llama3-1-8b-instruct-v1:0",
    "meta.llama3-1-70b-instruct-v1:0",
    "us.meta.llama3-1-70b-instruct-v1:0",
    "meta.llama3-1-405b-instruct-v1:0",
    "us.meta.llama3-2-11b-instruct-v1:0",
    "us.meta.llama3-2-90b-instruct-v1:0",
    "us.meta.llama3-2-1b-instruct-v1:0",
    "us.meta.llama3-2-3b-instruct-v1:0",
    "us.meta.llama3-3-70b-instruct-v1:0",
    "mistral.mistral-7b-instruct-v0:2",
    "mistral.mixtral-8x7b-instruct-v0:1",
    "mistral.mistral-large-2402-v1:0",
    "mistral.mistral-large-2407-v1:0",
]
```

```
LatestBedrockModelNames = Literal[
    "amazon.titan-tg1-large",
    "amazon.titan-text-lite-v1",
    "amazon.titan-text-express-v1",
    "us.amazon.nova-pro-v1:0",
    "us.amazon.nova-lite-v1:0",
    "us.amazon.nova-micro-v1:0",
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-3-5-haiku-20241022-v1:0",
    "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    "anthropic.claude-instant-v1",
    "anthropic.claude-v2:1",
    "anthropic.claude-v2",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "us.anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "us.anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "us.anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "us.anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-7-sonnet-20250219-v1:0",
    "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "cohere.command-text-v14",
    "cohere.command-r-v1:0",
    "cohere.command-r-plus-v1:0",
    "cohere.command-light-text-v14",
    "meta.llama3-8b-instruct-v1:0",
    "meta.llama3-70b-instruct-v1:0",
    "meta.llama3-1-8b-instruct-v1:0",
    "us.meta.llama3-1-8b-instruct-v1:0",
    "meta.llama3-1-70b-instruct-v1:0",
    "us.meta.llama3-1-70b-instruct-v1:0",
    "meta.llama3-1-405b-instruct-v1:0",
    "us.meta.llama3-2-11b-instruct-v1:0",
    "us.meta.llama3-2-90b-instruct-v1:0",
    "us.meta.llama3-2-1b-instruct-v1:0",
    "us.meta.llama3-2-3b-instruct-v1:0",
    "us.meta.llama3-3-70b-instruct-v1:0",
    "mistral.mistral-7b-instruct-v0:2",
    "mistral.mixtral-8x7b-instruct-v0:1",
    "mistral.mistral-large-2402-v1:0",
    "mistral.mistral-large-2407-v1:0",
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Latest Bedrock models.

### BedrockModelName

module-attribute

```
module-attribute
```

```
BedrockModelName = Union[str, LatestBedrockModelNames]
```

```
BedrockModelName = Union[str, LatestBedrockModelNames]
```

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[LatestBedrockModelNames](https://ai.pydantic.dev#pydantic_ai.models.bedrock.LatestBedrockModelNames)

Possible Bedrock model names.

Since Bedrock supports a variety of date-stamped models, we explicitly list the latest models but allow any name in the type hints.
See the Bedrock docs for a full list.

### BedrockConverseModel

dataclass

```
dataclass
```

Bases: Model

```
Model
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

A model that uses the Bedrock Converse API.

```
pydantic_ai_slim/pydantic_ai/models/bedrock.py
```

```
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
```

```
@dataclass(init=False)
class BedrockConverseModel(Model):
    """A model that uses the Bedrock Converse API."""

    client: BedrockRuntimeClient

    _model_name: BedrockModelName = field(repr=False)
    _system: str | None = field(default='bedrock', repr=False)

    @property
    def model_name(self) -> str:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider, ex: openai."""
        return self._system

    def __init__(
        self,
        model_name: BedrockModelName,
        *,
        provider: Literal['bedrock'] | Provider[BaseClient] = 'bedrock',
    ):
        """Initialize a Bedrock model.

        Args:
            model_name: The name of the model to use.
            model_name: The name of the Bedrock model to use. List of model names available
                [here](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html).
            provider: The provider to use. Defaults to `'bedrock'`.
        """
        self._model_name = model_name

        if isinstance(provider, str):
            self.client = infer_provider(provider).client
        else:
            self.client = cast('BedrockRuntimeClient', provider.client)

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[ToolTypeDef]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> ToolTypeDef:
        return {
            'toolSpec': {
                'name': f.name,
                'description': f.description,
                'inputSchema': {'json': f.parameters_json_schema},
            }
        }

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, result.Usage]:
        response = await self._messages_create(messages, False, model_settings, model_request_parameters)
        return await self._process_response(response)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        response = await self._messages_create(messages, True, model_settings, model_request_parameters)
        yield BedrockStreamedResponse(_model_name=self.model_name, _event_stream=response)

    async def _process_response(self, response: ConverseResponseTypeDef) -> tuple[ModelResponse, result.Usage]:
        items: list[ModelResponsePart] = []
        if message := response['output'].get('message'):
            for item in message['content']:
                if text := item.get('text'):
                    items.append(TextPart(content=text))
                else:
                    tool_use = item.get('toolUse')
                    assert tool_use is not None, f'Found a content that is not a text or tool use: {item}'
                    items.append(
                        ToolCallPart(
                            tool_name=tool_use['name'],
                            args=tool_use['input'],
                            tool_call_id=tool_use['toolUseId'],
                        ),
                    )
        usage = result.Usage(
            request_tokens=response['usage']['inputTokens'],
            response_tokens=response['usage']['outputTokens'],
            total_tokens=response['usage']['totalTokens'],
        )
        return ModelResponse(items, model_name=self.model_name), usage

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[True],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> EventStream[ConverseStreamOutputTypeDef]:
        pass

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[False],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> ConverseResponseTypeDef:
        pass

    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: bool,
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> ConverseResponseTypeDef | EventStream[ConverseStreamOutputTypeDef]:
        tools = self._get_tools(model_request_parameters)
        support_tools_choice = self.model_name.startswith(('anthropic', 'us.anthropic'))
        if not tools or not support_tools_choice:
            tool_choice: ToolChoiceTypeDef = {}
        elif not model_request_parameters.allow_text_result:
            tool_choice = {'any': {}}
        else:
            tool_choice = {'auto': {}}

        system_prompt, bedrock_messages = self._map_message(messages)
        inference_config = self._map_inference_config(model_settings)

        params = {
            'modelId': self.model_name,
            'messages': bedrock_messages,
            'system': [{'text': system_prompt}],
            'inferenceConfig': inference_config,
            **(
                {'toolConfig': {'tools': tools, **({'toolChoice': tool_choice} if tool_choice else {})}}
                if tools
                else {}
            ),
        }

        if stream:
            model_response = await anyio.to_thread.run_sync(functools.partial(self.client.converse_stream, **params))
            model_response = model_response['stream']
        else:
            model_response = await anyio.to_thread.run_sync(functools.partial(self.client.converse, **params))
        return model_response

    @staticmethod
    def _map_inference_config(
        model_settings: ModelSettings | None,
    ) -> InferenceConfigurationTypeDef:
        model_settings = model_settings or {}
        inference_config: InferenceConfigurationTypeDef = {}

        if max_tokens := model_settings.get('max_tokens'):
            inference_config['maxTokens'] = max_tokens
        if temperature := model_settings.get('temperature'):
            inference_config['temperature'] = temperature
        if top_p := model_settings.get('top_p'):
            inference_config['topP'] = top_p
        # TODO(Marcelo): This is not included in model_settings yet.
        # if stop_sequences := model_settings.get('stop_sequences'):
        #     inference_config['stopSequences'] = stop_sequences

        return inference_config

    def _map_message(self, messages: list[ModelMessage]) -> tuple[str, list[MessageUnionTypeDef]]:
        """Just maps a `pydantic_ai.Message` to the Bedrock `MessageUnionTypeDef`."""
        system_prompt: str = ''
        bedrock_messages: list[MessageUnionTypeDef] = []
        for m in messages:
            if isinstance(m, ModelRequest):
                for part in m.parts:
                    if isinstance(part, SystemPromptPart):
                        system_prompt += part.content
                    elif isinstance(part, UserPromptPart):
                        if isinstance(part.content, str):
                            bedrock_messages.append({'role': 'user', 'content': [{'text': part.content}]})
                        else:
                            raise NotImplementedError('User prompt can only be a string for now.')
                    elif isinstance(part, ToolReturnPart):
                        assert part.tool_call_id is not None
                        bedrock_messages.append(
                            {
                                'role': 'user',
                                'content': [
                                    {
                                        'toolResult': {
                                            'toolUseId': part.tool_call_id,
                                            'content': [{'text': part.model_response_str()}],
                                            'status': 'success',
                                        }
                                    }
                                ],
                            }
                        )
                    elif isinstance(part, RetryPromptPart):
                        # TODO(Marcelo): We need to add a test here.
                        if part.tool_name is None:  # pragma: no cover
                            bedrock_messages.append({'role': 'user', 'content': [{'text': part.model_response()}]})
                        else:
                            assert part.tool_call_id is not None
                            bedrock_messages.append(
                                {
                                    'role': 'user',
                                    'content': [
                                        {
                                            'toolResult': {
                                                'toolUseId': part.tool_call_id,
                                                'content': [{'text': part.model_response()}],
                                                'status': 'error',
                                            }
                                        }
                                    ],
                                }
                            )
            elif isinstance(m, ModelResponse):
                content: list[ContentBlockOutputTypeDef] = []
                for item in m.parts:
                    if isinstance(item, TextPart):
                        content.append({'text': item.content})
                    else:
                        assert isinstance(item, ToolCallPart)
                        content.append(self._map_tool_call(item))  # FIXME: MISSING key
                bedrock_messages.append({'role': 'assistant', 'content': content})
            else:
                assert_never(m)
        return system_prompt, bedrock_messages

    @staticmethod
    def _map_tool_call(t: ToolCallPart) -> ContentBlockOutputTypeDef:
        assert t.tool_call_id is not None
        return {
            'toolUse': {
                'toolUseId': t.tool_call_id,
                'name': t.tool_name,
                'input': t.args_as_dict(),
            }
        }
```

```
@dataclass(init=False)
class BedrockConverseModel(Model):
    """A model that uses the Bedrock Converse API."""

    client: BedrockRuntimeClient

    _model_name: BedrockModelName = field(repr=False)
    _system: str | None = field(default='bedrock', repr=False)

    @property
    def model_name(self) -> str:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider, ex: openai."""
        return self._system

    def __init__(
        self,
        model_name: BedrockModelName,
        *,
        provider: Literal['bedrock'] | Provider[BaseClient] = 'bedrock',
    ):
        """Initialize a Bedrock model.

        Args:
            model_name: The name of the model to use.
            model_name: The name of the Bedrock model to use. List of model names available
                [here](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html).
            provider: The provider to use. Defaults to `'bedrock'`.
        """
        self._model_name = model_name

        if isinstance(provider, str):
            self.client = infer_provider(provider).client
        else:
            self.client = cast('BedrockRuntimeClient', provider.client)

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> list[ToolTypeDef]:
        tools = [self._map_tool_definition(r) for r in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [self._map_tool_definition(r) for r in model_request_parameters.result_tools]
        return tools

    @staticmethod
    def _map_tool_definition(f: ToolDefinition) -> ToolTypeDef:
        return {
            'toolSpec': {
                'name': f.name,
                'description': f.description,
                'inputSchema': {'json': f.parameters_json_schema},
            }
        }

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, result.Usage]:
        response = await self._messages_create(messages, False, model_settings, model_request_parameters)
        return await self._process_response(response)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        response = await self._messages_create(messages, True, model_settings, model_request_parameters)
        yield BedrockStreamedResponse(_model_name=self.model_name, _event_stream=response)

    async def _process_response(self, response: ConverseResponseTypeDef) -> tuple[ModelResponse, result.Usage]:
        items: list[ModelResponsePart] = []
        if message := response['output'].get('message'):
            for item in message['content']:
                if text := item.get('text'):
                    items.append(TextPart(content=text))
                else:
                    tool_use = item.get('toolUse')
                    assert tool_use is not None, f'Found a content that is not a text or tool use: {item}'
                    items.append(
                        ToolCallPart(
                            tool_name=tool_use['name'],
                            args=tool_use['input'],
                            tool_call_id=tool_use['toolUseId'],
                        ),
                    )
        usage = result.Usage(
            request_tokens=response['usage']['inputTokens'],
            response_tokens=response['usage']['outputTokens'],
            total_tokens=response['usage']['totalTokens'],
        )
        return ModelResponse(items, model_name=self.model_name), usage

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[True],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> EventStream[ConverseStreamOutputTypeDef]:
        pass

    @overload
    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: Literal[False],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> ConverseResponseTypeDef:
        pass

    async def _messages_create(
        self,
        messages: list[ModelMessage],
        stream: bool,
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> ConverseResponseTypeDef | EventStream[ConverseStreamOutputTypeDef]:
        tools = self._get_tools(model_request_parameters)
        support_tools_choice = self.model_name.startswith(('anthropic', 'us.anthropic'))
        if not tools or not support_tools_choice:
            tool_choice: ToolChoiceTypeDef = {}
        elif not model_request_parameters.allow_text_result:
            tool_choice = {'any': {}}
        else:
            tool_choice = {'auto': {}}

        system_prompt, bedrock_messages = self._map_message(messages)
        inference_config = self._map_inference_config(model_settings)

        params = {
            'modelId': self.model_name,
            'messages': bedrock_messages,
            'system': [{'text': system_prompt}],
            'inferenceConfig': inference_config,
            **(
                {'toolConfig': {'tools': tools, **({'toolChoice': tool_choice} if tool_choice else {})}}
                if tools
                else {}
            ),
        }

        if stream:
            model_response = await anyio.to_thread.run_sync(functools.partial(self.client.converse_stream, **params))
            model_response = model_response['stream']
        else:
            model_response = await anyio.to_thread.run_sync(functools.partial(self.client.converse, **params))
        return model_response

    @staticmethod
    def _map_inference_config(
        model_settings: ModelSettings | None,
    ) -> InferenceConfigurationTypeDef:
        model_settings = model_settings or {}
        inference_config: InferenceConfigurationTypeDef = {}

        if max_tokens := model_settings.get('max_tokens'):
            inference_config['maxTokens'] = max_tokens
        if temperature := model_settings.get('temperature'):
            inference_config['temperature'] = temperature
        if top_p := model_settings.get('top_p'):
            inference_config['topP'] = top_p
        # TODO(Marcelo): This is not included in model_settings yet.
        # if stop_sequences := model_settings.get('stop_sequences'):
        #     inference_config['stopSequences'] = stop_sequences

        return inference_config

    def _map_message(self, messages: list[ModelMessage]) -> tuple[str, list[MessageUnionTypeDef]]:
        """Just maps a `pydantic_ai.Message` to the Bedrock `MessageUnionTypeDef`."""
        system_prompt: str = ''
        bedrock_messages: list[MessageUnionTypeDef] = []
        for m in messages:
            if isinstance(m, ModelRequest):
                for part in m.parts:
                    if isinstance(part, SystemPromptPart):
                        system_prompt += part.content
                    elif isinstance(part, UserPromptPart):
                        if isinstance(part.content, str):
                            bedrock_messages.append({'role': 'user', 'content': [{'text': part.content}]})
                        else:
                            raise NotImplementedError('User prompt can only be a string for now.')
                    elif isinstance(part, ToolReturnPart):
                        assert part.tool_call_id is not None
                        bedrock_messages.append(
                            {
                                'role': 'user',
                                'content': [
                                    {
                                        'toolResult': {
                                            'toolUseId': part.tool_call_id,
                                            'content': [{'text': part.model_response_str()}],
                                            'status': 'success',
                                        }
                                    }
                                ],
                            }
                        )
                    elif isinstance(part, RetryPromptPart):
                        # TODO(Marcelo): We need to add a test here.
                        if part.tool_name is None:  # pragma: no cover
                            bedrock_messages.append({'role': 'user', 'content': [{'text': part.model_response()}]})
                        else:
                            assert part.tool_call_id is not None
                            bedrock_messages.append(
                                {
                                    'role': 'user',
                                    'content': [
                                        {
                                            'toolResult': {
                                                'toolUseId': part.tool_call_id,
                                                'content': [{'text': part.model_response()}],
                                                'status': 'error',
                                            }
                                        }
                                    ],
                                }
                            )
            elif isinstance(m, ModelResponse):
                content: list[ContentBlockOutputTypeDef] = []
                for item in m.parts:
                    if isinstance(item, TextPart):
                        content.append({'text': item.content})
                    else:
                        assert isinstance(item, ToolCallPart)
                        content.append(self._map_tool_call(item))  # FIXME: MISSING key
                bedrock_messages.append({'role': 'assistant', 'content': content})
            else:
                assert_never(m)
        return system_prompt, bedrock_messages

    @staticmethod
    def _map_tool_call(t: ToolCallPart) -> ContentBlockOutputTypeDef:
        assert t.tool_call_id is not None
        return {
            'toolUse': {
                'toolUseId': t.tool_call_id,
                'name': t.tool_name,
                'input': t.args_as_dict(),
            }
        }
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

The system / model provider, ex: openai.

#### __init__

```
__init__(
    model_name: BedrockModelName,
    *,
    provider: (
        Literal["bedrock"] | Provider[BaseClient]
    ) = "bedrock"
)
```

```
__init__(
    model_name: BedrockModelName,
    *,
    provider: (
        Literal["bedrock"] | Provider[BaseClient]
    ) = "bedrock"
)
```

[BedrockModelName](https://ai.pydantic.dev#pydantic_ai.models.bedrock.BedrockModelName)

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

Initialize a Bedrock model.

Parameters:

```
model_name
```

```
BedrockModelName
```

[BedrockModelName](https://ai.pydantic.dev#pydantic_ai.models.bedrock.BedrockModelName)

The name of the model to use.

```
model_name
```

```
BedrockModelName
```

[BedrockModelName](https://ai.pydantic.dev#pydantic_ai.models.bedrock.BedrockModelName)

The name of the Bedrock model to use. List of model names available
here.

```
provider
```

```
Literal['bedrock'] | Provider[BaseClient]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

The provider to use. Defaults to 'bedrock'.

```
'bedrock'
```

```
'bedrock'
```

```
pydantic_ai_slim/pydantic_ai/models/bedrock.py
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
```

```
def __init__(
    self,
    model_name: BedrockModelName,
    *,
    provider: Literal['bedrock'] | Provider[BaseClient] = 'bedrock',
):
    """Initialize a Bedrock model.

    Args:
        model_name: The name of the model to use.
        model_name: The name of the Bedrock model to use. List of model names available
            [here](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html).
        provider: The provider to use. Defaults to `'bedrock'`.
    """
    self._model_name = model_name

    if isinstance(provider, str):
        self.client = infer_provider(provider).client
    else:
        self.client = cast('BedrockRuntimeClient', provider.client)
```

```
def __init__(
    self,
    model_name: BedrockModelName,
    *,
    provider: Literal['bedrock'] | Provider[BaseClient] = 'bedrock',
):
    """Initialize a Bedrock model.

    Args:
        model_name: The name of the model to use.
        model_name: The name of the Bedrock model to use. List of model names available
            [here](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html).
        provider: The provider to use. Defaults to `'bedrock'`.
    """
    self._model_name = model_name

    if isinstance(provider, str):
        self.client = infer_provider(provider).client
    else:
        self.client = cast('BedrockRuntimeClient', provider.client)
```

### BedrockStreamedResponse

dataclass

```
dataclass
```

Bases: StreamedResponse

```
StreamedResponse
```

[StreamedResponse](https://ai.pydantic.dev/base/#pydantic_ai.models.StreamedResponse)

Implementation of StreamedResponse for Bedrock models.

```
StreamedResponse
```

```
pydantic_ai_slim/pydantic_ai/models/bedrock.py
```

```
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
@dataclass
class BedrockStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for Bedrock models."""

    _model_name: BedrockModelName
    _event_stream: EventStream[ConverseStreamOutputTypeDef]
    _timestamp: datetime = field(default_factory=_utils.now_utc)

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        """Return an async iterator of [`ModelResponseStreamEvent`][pydantic_ai.messages.ModelResponseStreamEvent]s.

        This method should be implemented by subclasses to translate the vendor-specific stream of events into
        pydantic_ai-format events.
        """
        chunk: ConverseStreamOutputTypeDef
        tool_id: str | None = None
        async for chunk in _AsyncIteratorWrapper(self._event_stream):
            # TODO(Marcelo): Switch this to `match` when we drop Python 3.9 support.
            if 'messageStart' in chunk:
                continue
            if 'messageStop' in chunk:
                continue
            if 'metadata' in chunk:
                if 'usage' in chunk['metadata']:
                    self._usage += self._map_usage(chunk['metadata'])
                continue
            if 'contentBlockStart' in chunk:
                index = chunk['contentBlockStart']['contentBlockIndex']
                start = chunk['contentBlockStart']['start']
                if 'toolUse' in start:
                    tool_use_start = start['toolUse']
                    tool_id = tool_use_start['toolUseId']
                    tool_name = tool_use_start['name']
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=index,
                        tool_name=tool_name,
                        args=None,
                        tool_call_id=tool_id,
                    )
                    if maybe_event:
                        yield maybe_event
            if 'contentBlockDelta' in chunk:
                index = chunk['contentBlockDelta']['contentBlockIndex']
                delta = chunk['contentBlockDelta']['delta']
                if 'text' in delta:
                    yield self._parts_manager.handle_text_delta(vendor_part_id=index, content=delta['text'])
                if 'toolUse' in delta:
                    tool_use = delta['toolUse']
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=index,
                        tool_name=tool_use.get('name'),
                        args=tool_use.get('input'),
                        tool_call_id=tool_id,
                    )
                    if maybe_event:
                        yield maybe_event

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def model_name(self) -> str:
        """Get the model name of the response."""
        return self._model_name

    def _map_usage(self, metadata: ConverseStreamMetadataEventTypeDef) -> result.Usage:
        return result.Usage(
            request_tokens=metadata['usage']['inputTokens'],
            response_tokens=metadata['usage']['outputTokens'],
            total_tokens=metadata['usage']['totalTokens'],
        )
```

```
@dataclass
class BedrockStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for Bedrock models."""

    _model_name: BedrockModelName
    _event_stream: EventStream[ConverseStreamOutputTypeDef]
    _timestamp: datetime = field(default_factory=_utils.now_utc)

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        """Return an async iterator of [`ModelResponseStreamEvent`][pydantic_ai.messages.ModelResponseStreamEvent]s.

        This method should be implemented by subclasses to translate the vendor-specific stream of events into
        pydantic_ai-format events.
        """
        chunk: ConverseStreamOutputTypeDef
        tool_id: str | None = None
        async for chunk in _AsyncIteratorWrapper(self._event_stream):
            # TODO(Marcelo): Switch this to `match` when we drop Python 3.9 support.
            if 'messageStart' in chunk:
                continue
            if 'messageStop' in chunk:
                continue
            if 'metadata' in chunk:
                if 'usage' in chunk['metadata']:
                    self._usage += self._map_usage(chunk['metadata'])
                continue
            if 'contentBlockStart' in chunk:
                index = chunk['contentBlockStart']['contentBlockIndex']
                start = chunk['contentBlockStart']['start']
                if 'toolUse' in start:
                    tool_use_start = start['toolUse']
                    tool_id = tool_use_start['toolUseId']
                    tool_name = tool_use_start['name']
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=index,
                        tool_name=tool_name,
                        args=None,
                        tool_call_id=tool_id,
                    )
                    if maybe_event:
                        yield maybe_event
            if 'contentBlockDelta' in chunk:
                index = chunk['contentBlockDelta']['contentBlockIndex']
                delta = chunk['contentBlockDelta']['delta']
                if 'text' in delta:
                    yield self._parts_manager.handle_text_delta(vendor_part_id=index, content=delta['text'])
                if 'toolUse' in delta:
                    tool_use = delta['toolUse']
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=index,
                        tool_name=tool_use.get('name'),
                        args=tool_use.get('input'),
                        tool_call_id=tool_id,
                    )
                    if maybe_event:
                        yield maybe_event

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def model_name(self) -> str:
        """Get the model name of the response."""
        return self._model_name

    def _map_usage(self, metadata: ConverseStreamMetadataEventTypeDef) -> result.Usage:
        return result.Usage(
            request_tokens=metadata['usage']['inputTokens'],
            response_tokens=metadata['usage']['outputTokens'],
            total_tokens=metadata['usage']['totalTokens'],
        )
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

