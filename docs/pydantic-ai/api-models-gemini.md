# pydantic_ai.models.gemini

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.gemini

```
pydantic_ai.models.gemini
```

Custom interface to the generativelanguage.googleapis.com API using
HTTPX and Pydantic.

```
generativelanguage.googleapis.com
```

The Google SDK for interacting with the generativelanguage.googleapis.com API
google-generativeai reads like it was written by a
Java developer who thought they knew everything about OOP, spent 30 minutes trying to learn Python,
gave up and decided to build the library to prove how horrible Python is. It also doesn't use httpx for HTTP requests,
and tries to implement tool calling itself, but doesn't use Pydantic or equivalent for validation.

```
generativelanguage.googleapis.com
```

```
google-generativeai
```

We therefore implement support for the API directly.

Despite these shortcomings, the Gemini model is actually quite powerful and very fast.

## Setup

For details on how to set up authentication with this model, see model configuration for Gemini.

[](https://ai.pydantic.dev)

### LatestGeminiModelNames

module-attribute

```
module-attribute
```

```
LatestGeminiModelNames = Literal[
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-exp-1206",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-2.0-pro-exp-02-05",
]
```

```
LatestGeminiModelNames = Literal[
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-exp-1206",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-2.0-pro-exp-02-05",
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Latest Gemini models.

### GeminiModelName

module-attribute

```
module-attribute
```

```
GeminiModelName = Union[str, LatestGeminiModelNames]
```

```
GeminiModelName = Union[str, LatestGeminiModelNames]
```

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[LatestGeminiModelNames](https://ai.pydantic.dev#pydantic_ai.models.gemini.LatestGeminiModelNames)

Possible Gemini model names.

Since Gemini supports a variety of date-stamped models, we explicitly list the latest models but
allow any name in the type hints.
See the Gemini API docs for a full list.

### GeminiModelSettings

Bases: ModelSettings

```
ModelSettings
```

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

Settings used for a Gemini model request.

```
pydantic_ai_slim/pydantic_ai/models/gemini.py
```

```
71
72
73
74
```

```
class GeminiModelSettings(ModelSettings):
    """Settings used for a Gemini model request."""

    gemini_safety_settings: list[GeminiSafetySettings]
```

```
class GeminiModelSettings(ModelSettings):
    """Settings used for a Gemini model request."""

    gemini_safety_settings: list[GeminiSafetySettings]
```

### GeminiModel

dataclass

```
dataclass
```

Bases: Model

```
Model
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

A model that uses Gemini via generativelanguage.googleapis.com API.

```
generativelanguage.googleapis.com
```

This is implemented from scratch rather than using a dedicated SDK, good API documentation is
available here.

Apart from __init__, all methods are private or match those of the base class.

```
__init__
```

```
pydantic_ai_slim/pydantic_ai/models/gemini.py
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
```

```
@dataclass(init=False)
class GeminiModel(Model):
    """A model that uses Gemini via `generativelanguage.googleapis.com` API.

    This is implemented from scratch rather than using a dedicated SDK, good API documentation is
    available [here](https://ai.google.dev/api).

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    client: AsyncHTTPClient = field(repr=False)

    _model_name: GeminiModelName = field(repr=False)
    _provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] | None = field(repr=False)
    _auth: AuthProtocol | None = field(repr=False)
    _url: str | None = field(repr=False)
    _system: str | None = field(default='google-gla', repr=False)

    @overload
    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] = 'google-gla',
    ) -> None: ...

    @deprecated('Use the `provider` argument instead of the `api_key`, `http_client`, and `url_template` arguments.')
    @overload
    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        provider: None = None,
        api_key: str | None = None,
        http_client: AsyncHTTPClient | None = None,
        url_template: str = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:',
    ) -> None: ...

    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] | None = None,
        api_key: str | None = None,
        http_client: AsyncHTTPClient | None = None,
        url_template: str = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:',
    ):
        """Initialize a Gemini model.

        Args:
            model_name: The name of the model to use.
            provider: The provider to use for the model.
            api_key: The API key to use for authentication, if not provided, the `GEMINI_API_KEY` environment variable
                will be used if available.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
            url_template: The URL template to use for making requests, you shouldn't need to change this,
                docs [here](https://ai.google.dev/gemini-api/docs/quickstart?lang=rest#make-first-request),
                `model` is substituted with the model name, and `function` is added to the end of the URL.
        """
        self._model_name = model_name
        self._provider = provider

        if provider is not None:
            if isinstance(provider, str):
                self._system = provider
                self.client = infer_provider(provider).client
            else:
                self._system = provider.name
                self.client = provider.client
        else:
            if api_key is None:
                if env_api_key := os.getenv('GEMINI_API_KEY'):
                    api_key = env_api_key
                else:
                    raise UserError('API key must be provided or set in the GEMINI_API_KEY environment variable')
            self.client = http_client or cached_async_http_client()
            self._auth = ApiKeyAuth(api_key)
            self._url = url_template.format(model=model_name)

    @property
    def auth(self) -> AuthProtocol:
        assert self._auth is not None, 'Auth not initialized'
        return self._auth

    @property
    def url(self) -> str:
        assert self._url is not None, 'URL not initialized'
        return self._url

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        check_allow_model_requests()
        async with self._make_request(
            messages, False, cast(GeminiModelSettings, model_settings or {}), model_request_parameters
        ) as http_response:
            response = _gemini_response_ta.validate_json(await http_response.aread())
        return self._process_response(response), _metadata_as_usage(response)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        check_allow_model_requests()
        async with self._make_request(
            messages, True, cast(GeminiModelSettings, model_settings or {}), model_request_parameters
        ) as http_response:
            yield await self._process_streamed_response(http_response)

    @property
    def model_name(self) -> GeminiModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> _GeminiTools | None:
        tools = [_function_from_abstract_tool(t) for t in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [_function_from_abstract_tool(t) for t in model_request_parameters.result_tools]
        return _GeminiTools(function_declarations=tools) if tools else None

    def _get_tool_config(
        self, model_request_parameters: ModelRequestParameters, tools: _GeminiTools | None
    ) -> _GeminiToolConfig | None:
        if model_request_parameters.allow_text_result:
            return None
        elif tools:
            return _tool_config([t['name'] for t in tools['function_declarations']])
        else:
            return _tool_config([])

    @asynccontextmanager
    async def _make_request(
        self,
        messages: list[ModelMessage],
        streamed: bool,
        model_settings: GeminiModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[HTTPResponse]:
        tools = self._get_tools(model_request_parameters)
        tool_config = self._get_tool_config(model_request_parameters, tools)
        sys_prompt_parts, contents = await self._message_to_gemini_content(messages)

        request_data = _GeminiRequest(contents=contents)
        if sys_prompt_parts:
            request_data['system_instruction'] = _GeminiTextContent(role='user', parts=sys_prompt_parts)
        if tools is not None:
            request_data['tools'] = tools
        if tool_config is not None:
            request_data['tool_config'] = tool_config

        generation_config: _GeminiGenerationConfig = {}
        if model_settings:
            if (max_tokens := model_settings.get('max_tokens')) is not None:
                generation_config['max_output_tokens'] = max_tokens
            if (temperature := model_settings.get('temperature')) is not None:
                generation_config['temperature'] = temperature
            if (top_p := model_settings.get('top_p')) is not None:
                generation_config['top_p'] = top_p
            if (presence_penalty := model_settings.get('presence_penalty')) is not None:
                generation_config['presence_penalty'] = presence_penalty
            if (frequency_penalty := model_settings.get('frequency_penalty')) is not None:
                generation_config['frequency_penalty'] = frequency_penalty
            if (gemini_safety_settings := model_settings.get('gemini_safety_settings')) != []:
                request_data['safety_settings'] = gemini_safety_settings
        if generation_config:
            request_data['generation_config'] = generation_config

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': get_user_agent(),
        }
        if self._provider is None:  # pragma: no cover
            url = self.url + ('streamGenerateContent' if streamed else 'generateContent')
            headers.update(await self.auth.headers())
        else:
            url = f'/{self._model_name}:{"streamGenerateContent" if streamed else "generateContent"}'

        request_json = _gemini_request_ta.dump_json(request_data, by_alias=True)

        async with self.client.stream(
            'POST',
            url,
            content=request_json,
            headers=headers,
            timeout=model_settings.get('timeout', USE_CLIENT_DEFAULT),
        ) as r:
            if (status_code := r.status_code) != 200:
                await r.aread()
                if status_code >= 400:
                    raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=r.text)
                raise UnexpectedModelBehavior(f'Unexpected response from gemini {status_code}', r.text)
            yield r

    def _process_response(self, response: _GeminiResponse) -> ModelResponse:
        if len(response['candidates']) != 1:
            raise UnexpectedModelBehavior('Expected exactly one candidate in Gemini response')
        if 'content' not in response['candidates'][0]:
            if response['candidates'][0].get('finish_reason') == 'SAFETY':
                raise UnexpectedModelBehavior('Safety settings triggered', str(response))
            else:
                raise UnexpectedModelBehavior('Content field missing from Gemini response', str(response))
        parts = response['candidates'][0]['content']['parts']
        return _process_response_from_parts(parts, model_name=response.get('model_version', self._model_name))

    async def _process_streamed_response(self, http_response: HTTPResponse) -> StreamedResponse:
        """Process a streamed response, and prepare a streaming response to return."""
        aiter_bytes = http_response.aiter_bytes()
        start_response: _GeminiResponse | None = None
        content = bytearray()

        async for chunk in aiter_bytes:
            content.extend(chunk)
            responses = _gemini_streamed_response_ta.validate_json(
                _ensure_decodeable(content),
                experimental_allow_partial='trailing-strings',
            )
            if responses:
                last = responses[-1]
                if last['candidates'] and last['candidates'][0].get('content', {}).get('parts'):
                    start_response = last
                    break

        if start_response is None:
            raise UnexpectedModelBehavior('Streamed response ended without content or tool calls')

        return GeminiStreamedResponse(_model_name=self._model_name, _content=content, _stream=aiter_bytes)

    @classmethod
    async def _message_to_gemini_content(
        cls, messages: list[ModelMessage]
    ) -> tuple[list[_GeminiTextPart], list[_GeminiContent]]:
        sys_prompt_parts: list[_GeminiTextPart] = []
        contents: list[_GeminiContent] = []
        for m in messages:
            if isinstance(m, ModelRequest):
                message_parts: list[_GeminiPartUnion] = []

                for part in m.parts:
                    if isinstance(part, SystemPromptPart):
                        sys_prompt_parts.append(_GeminiTextPart(text=part.content))
                    elif isinstance(part, UserPromptPart):
                        message_parts.extend(await cls._map_user_prompt(part))
                    elif isinstance(part, ToolReturnPart):
                        message_parts.append(_response_part_from_response(part.tool_name, part.model_response_object()))
                    elif isinstance(part, RetryPromptPart):
                        if part.tool_name is None:
                            message_parts.append(_GeminiTextPart(text=part.model_response()))
                        else:
                            response = {'call_error': part.model_response()}
                            message_parts.append(_response_part_from_response(part.tool_name, response))
                    else:
                        assert_never(part)

                if message_parts:
                    contents.append(_GeminiContent(role='user', parts=message_parts))
            elif isinstance(m, ModelResponse):
                contents.append(_content_model_response(m))
            else:
                assert_never(m)

        return sys_prompt_parts, contents

    @staticmethod
    async def _map_user_prompt(part: UserPromptPart) -> list[_GeminiPartUnion]:
        if isinstance(part.content, str):
            return [{'text': part.content}]
        else:
            content: list[_GeminiPartUnion] = []
            for item in part.content:
                if isinstance(item, str):
                    content.append({'text': item})
                elif isinstance(item, BinaryContent):
                    base64_encoded = base64.b64encode(item.data).decode('utf-8')
                    content.append(
                        _GeminiInlineDataPart(inline_data={'data': base64_encoded, 'mime_type': item.media_type})
                    )
                elif isinstance(item, (AudioUrl, ImageUrl)):
                    try:
                        content.append(
                            _GeminiFileDataPart(file_data={'file_uri': item.url, 'mime_type': item.media_type})
                        )
                    except ValueError:
                        # Download the file if can't find the mime type.
                        client = cached_async_http_client()
                        response = await client.get(item.url, follow_redirects=True)
                        response.raise_for_status()
                        base64_encoded = base64.b64encode(response.content).decode('utf-8')
                        content.append(
                            _GeminiInlineDataPart(
                                inline_data={'data': base64_encoded, 'mime_type': response.headers['Content-Type']}
                            )
                        )
                else:
                    assert_never(item)
        return content
```

```
@dataclass(init=False)
class GeminiModel(Model):
    """A model that uses Gemini via `generativelanguage.googleapis.com` API.

    This is implemented from scratch rather than using a dedicated SDK, good API documentation is
    available [here](https://ai.google.dev/api).

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    client: AsyncHTTPClient = field(repr=False)

    _model_name: GeminiModelName = field(repr=False)
    _provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] | None = field(repr=False)
    _auth: AuthProtocol | None = field(repr=False)
    _url: str | None = field(repr=False)
    _system: str | None = field(default='google-gla', repr=False)

    @overload
    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] = 'google-gla',
    ) -> None: ...

    @deprecated('Use the `provider` argument instead of the `api_key`, `http_client`, and `url_template` arguments.')
    @overload
    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        provider: None = None,
        api_key: str | None = None,
        http_client: AsyncHTTPClient | None = None,
        url_template: str = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:',
    ) -> None: ...

    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] | None = None,
        api_key: str | None = None,
        http_client: AsyncHTTPClient | None = None,
        url_template: str = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:',
    ):
        """Initialize a Gemini model.

        Args:
            model_name: The name of the model to use.
            provider: The provider to use for the model.
            api_key: The API key to use for authentication, if not provided, the `GEMINI_API_KEY` environment variable
                will be used if available.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
            url_template: The URL template to use for making requests, you shouldn't need to change this,
                docs [here](https://ai.google.dev/gemini-api/docs/quickstart?lang=rest#make-first-request),
                `model` is substituted with the model name, and `function` is added to the end of the URL.
        """
        self._model_name = model_name
        self._provider = provider

        if provider is not None:
            if isinstance(provider, str):
                self._system = provider
                self.client = infer_provider(provider).client
            else:
                self._system = provider.name
                self.client = provider.client
        else:
            if api_key is None:
                if env_api_key := os.getenv('GEMINI_API_KEY'):
                    api_key = env_api_key
                else:
                    raise UserError('API key must be provided or set in the GEMINI_API_KEY environment variable')
            self.client = http_client or cached_async_http_client()
            self._auth = ApiKeyAuth(api_key)
            self._url = url_template.format(model=model_name)

    @property
    def auth(self) -> AuthProtocol:
        assert self._auth is not None, 'Auth not initialized'
        return self._auth

    @property
    def url(self) -> str:
        assert self._url is not None, 'URL not initialized'
        return self._url

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        check_allow_model_requests()
        async with self._make_request(
            messages, False, cast(GeminiModelSettings, model_settings or {}), model_request_parameters
        ) as http_response:
            response = _gemini_response_ta.validate_json(await http_response.aread())
        return self._process_response(response), _metadata_as_usage(response)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        check_allow_model_requests()
        async with self._make_request(
            messages, True, cast(GeminiModelSettings, model_settings or {}), model_request_parameters
        ) as http_response:
            yield await self._process_streamed_response(http_response)

    @property
    def model_name(self) -> GeminiModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system

    def _get_tools(self, model_request_parameters: ModelRequestParameters) -> _GeminiTools | None:
        tools = [_function_from_abstract_tool(t) for t in model_request_parameters.function_tools]
        if model_request_parameters.result_tools:
            tools += [_function_from_abstract_tool(t) for t in model_request_parameters.result_tools]
        return _GeminiTools(function_declarations=tools) if tools else None

    def _get_tool_config(
        self, model_request_parameters: ModelRequestParameters, tools: _GeminiTools | None
    ) -> _GeminiToolConfig | None:
        if model_request_parameters.allow_text_result:
            return None
        elif tools:
            return _tool_config([t['name'] for t in tools['function_declarations']])
        else:
            return _tool_config([])

    @asynccontextmanager
    async def _make_request(
        self,
        messages: list[ModelMessage],
        streamed: bool,
        model_settings: GeminiModelSettings,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[HTTPResponse]:
        tools = self._get_tools(model_request_parameters)
        tool_config = self._get_tool_config(model_request_parameters, tools)
        sys_prompt_parts, contents = await self._message_to_gemini_content(messages)

        request_data = _GeminiRequest(contents=contents)
        if sys_prompt_parts:
            request_data['system_instruction'] = _GeminiTextContent(role='user', parts=sys_prompt_parts)
        if tools is not None:
            request_data['tools'] = tools
        if tool_config is not None:
            request_data['tool_config'] = tool_config

        generation_config: _GeminiGenerationConfig = {}
        if model_settings:
            if (max_tokens := model_settings.get('max_tokens')) is not None:
                generation_config['max_output_tokens'] = max_tokens
            if (temperature := model_settings.get('temperature')) is not None:
                generation_config['temperature'] = temperature
            if (top_p := model_settings.get('top_p')) is not None:
                generation_config['top_p'] = top_p
            if (presence_penalty := model_settings.get('presence_penalty')) is not None:
                generation_config['presence_penalty'] = presence_penalty
            if (frequency_penalty := model_settings.get('frequency_penalty')) is not None:
                generation_config['frequency_penalty'] = frequency_penalty
            if (gemini_safety_settings := model_settings.get('gemini_safety_settings')) != []:
                request_data['safety_settings'] = gemini_safety_settings
        if generation_config:
            request_data['generation_config'] = generation_config

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': get_user_agent(),
        }
        if self._provider is None:  # pragma: no cover
            url = self.url + ('streamGenerateContent' if streamed else 'generateContent')
            headers.update(await self.auth.headers())
        else:
            url = f'/{self._model_name}:{"streamGenerateContent" if streamed else "generateContent"}'

        request_json = _gemini_request_ta.dump_json(request_data, by_alias=True)

        async with self.client.stream(
            'POST',
            url,
            content=request_json,
            headers=headers,
            timeout=model_settings.get('timeout', USE_CLIENT_DEFAULT),
        ) as r:
            if (status_code := r.status_code) != 200:
                await r.aread()
                if status_code >= 400:
                    raise ModelHTTPError(status_code=status_code, model_name=self.model_name, body=r.text)
                raise UnexpectedModelBehavior(f'Unexpected response from gemini {status_code}', r.text)
            yield r

    def _process_response(self, response: _GeminiResponse) -> ModelResponse:
        if len(response['candidates']) != 1:
            raise UnexpectedModelBehavior('Expected exactly one candidate in Gemini response')
        if 'content' not in response['candidates'][0]:
            if response['candidates'][0].get('finish_reason') == 'SAFETY':
                raise UnexpectedModelBehavior('Safety settings triggered', str(response))
            else:
                raise UnexpectedModelBehavior('Content field missing from Gemini response', str(response))
        parts = response['candidates'][0]['content']['parts']
        return _process_response_from_parts(parts, model_name=response.get('model_version', self._model_name))

    async def _process_streamed_response(self, http_response: HTTPResponse) -> StreamedResponse:
        """Process a streamed response, and prepare a streaming response to return."""
        aiter_bytes = http_response.aiter_bytes()
        start_response: _GeminiResponse | None = None
        content = bytearray()

        async for chunk in aiter_bytes:
            content.extend(chunk)
            responses = _gemini_streamed_response_ta.validate_json(
                _ensure_decodeable(content),
                experimental_allow_partial='trailing-strings',
            )
            if responses:
                last = responses[-1]
                if last['candidates'] and last['candidates'][0].get('content', {}).get('parts'):
                    start_response = last
                    break

        if start_response is None:
            raise UnexpectedModelBehavior('Streamed response ended without content or tool calls')

        return GeminiStreamedResponse(_model_name=self._model_name, _content=content, _stream=aiter_bytes)

    @classmethod
    async def _message_to_gemini_content(
        cls, messages: list[ModelMessage]
    ) -> tuple[list[_GeminiTextPart], list[_GeminiContent]]:
        sys_prompt_parts: list[_GeminiTextPart] = []
        contents: list[_GeminiContent] = []
        for m in messages:
            if isinstance(m, ModelRequest):
                message_parts: list[_GeminiPartUnion] = []

                for part in m.parts:
                    if isinstance(part, SystemPromptPart):
                        sys_prompt_parts.append(_GeminiTextPart(text=part.content))
                    elif isinstance(part, UserPromptPart):
                        message_parts.extend(await cls._map_user_prompt(part))
                    elif isinstance(part, ToolReturnPart):
                        message_parts.append(_response_part_from_response(part.tool_name, part.model_response_object()))
                    elif isinstance(part, RetryPromptPart):
                        if part.tool_name is None:
                            message_parts.append(_GeminiTextPart(text=part.model_response()))
                        else:
                            response = {'call_error': part.model_response()}
                            message_parts.append(_response_part_from_response(part.tool_name, response))
                    else:
                        assert_never(part)

                if message_parts:
                    contents.append(_GeminiContent(role='user', parts=message_parts))
            elif isinstance(m, ModelResponse):
                contents.append(_content_model_response(m))
            else:
                assert_never(m)

        return sys_prompt_parts, contents

    @staticmethod
    async def _map_user_prompt(part: UserPromptPart) -> list[_GeminiPartUnion]:
        if isinstance(part.content, str):
            return [{'text': part.content}]
        else:
            content: list[_GeminiPartUnion] = []
            for item in part.content:
                if isinstance(item, str):
                    content.append({'text': item})
                elif isinstance(item, BinaryContent):
                    base64_encoded = base64.b64encode(item.data).decode('utf-8')
                    content.append(
                        _GeminiInlineDataPart(inline_data={'data': base64_encoded, 'mime_type': item.media_type})
                    )
                elif isinstance(item, (AudioUrl, ImageUrl)):
                    try:
                        content.append(
                            _GeminiFileDataPart(file_data={'file_uri': item.url, 'mime_type': item.media_type})
                        )
                    except ValueError:
                        # Download the file if can't find the mime type.
                        client = cached_async_http_client()
                        response = await client.get(item.url, follow_redirects=True)
                        response.raise_for_status()
                        base64_encoded = base64.b64encode(response.content).decode('utf-8')
                        content.append(
                            _GeminiInlineDataPart(
                                inline_data={'data': base64_encoded, 'mime_type': response.headers['Content-Type']}
                            )
                        )
                else:
                    assert_never(item)
        return content
```

#### __init__

```
__init__(
    model_name: GeminiModelName,
    *,
    provider: (
        Literal["google-gla", "google-vertex"]
        | Provider[AsyncClient]
    ) = "google-gla"
) -> None
```

```
__init__(
    model_name: GeminiModelName,
    *,
    provider: (
        Literal["google-gla", "google-vertex"]
        | Provider[AsyncClient]
    ) = "google-gla"
) -> None
```

[GeminiModelName](https://ai.pydantic.dev#pydantic_ai.models.gemini.GeminiModelName)

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

```
__init__(
    model_name: GeminiModelName,
    *,
    provider: None = None,
    api_key: str | None = None,
    http_client: AsyncClient | None = None,
    url_template: str = "https://generativelanguage.googleapis.com/v1beta/models/{model}:"
) -> None
```

```
__init__(
    model_name: GeminiModelName,
    *,
    provider: None = None,
    api_key: str | None = None,
    http_client: AsyncClient | None = None,
    url_template: str = "https://generativelanguage.googleapis.com/v1beta/models/{model}:"
) -> None
```

[GeminiModelName](https://ai.pydantic.dev#pydantic_ai.models.gemini.GeminiModelName)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
__init__(
    model_name: GeminiModelName,
    *,
    provider: (
        Literal["google-gla", "google-vertex"]
        | Provider[AsyncClient]
        | None
    ) = None,
    api_key: str | None = None,
    http_client: AsyncClient | None = None,
    url_template: str = "https://generativelanguage.googleapis.com/v1beta/models/{model}:"
)
```

```
__init__(
    model_name: GeminiModelName,
    *,
    provider: (
        Literal["google-gla", "google-vertex"]
        | Provider[AsyncClient]
        | None
    ) = None,
    api_key: str | None = None,
    http_client: AsyncClient | None = None,
    url_template: str = "https://generativelanguage.googleapis.com/v1beta/models/{model}:"
)
```

[GeminiModelName](https://ai.pydantic.dev#pydantic_ai.models.gemini.GeminiModelName)

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Initialize a Gemini model.

Parameters:

```
model_name
```

```
GeminiModelName
```

[GeminiModelName](https://ai.pydantic.dev#pydantic_ai.models.gemini.GeminiModelName)

The name of the model to use.

```
provider
```

```
Literal['google-gla', 'google-vertex'] | Provider[AsyncClient] | None
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[Provider](https://ai.pydantic.dev/providers/#pydantic_ai.providers.Provider)

The provider to use for the model.

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

The API key to use for authentication, if not provided, the GEMINI_API_KEY environment variable
will be used if available.

```
GEMINI_API_KEY
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
url_template
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The URL template to use for making requests, you shouldn't need to change this,
docs here,
model is substituted with the model name, and function is added to the end of the URL.

```
model
```

```
function
```

```
'https://generativelanguage.googleapis.com/v1beta/models/{model}:'
```

```
pydantic_ai_slim/pydantic_ai/models/gemini.py
```

```
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
```

```
def __init__(
    self,
    model_name: GeminiModelName,
    *,
    provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] | None = None,
    api_key: str | None = None,
    http_client: AsyncHTTPClient | None = None,
    url_template: str = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:',
):
    """Initialize a Gemini model.

    Args:
        model_name: The name of the model to use.
        provider: The provider to use for the model.
        api_key: The API key to use for authentication, if not provided, the `GEMINI_API_KEY` environment variable
            will be used if available.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        url_template: The URL template to use for making requests, you shouldn't need to change this,
            docs [here](https://ai.google.dev/gemini-api/docs/quickstart?lang=rest#make-first-request),
            `model` is substituted with the model name, and `function` is added to the end of the URL.
    """
    self._model_name = model_name
    self._provider = provider

    if provider is not None:
        if isinstance(provider, str):
            self._system = provider
            self.client = infer_provider(provider).client
        else:
            self._system = provider.name
            self.client = provider.client
    else:
        if api_key is None:
            if env_api_key := os.getenv('GEMINI_API_KEY'):
                api_key = env_api_key
            else:
                raise UserError('API key must be provided or set in the GEMINI_API_KEY environment variable')
        self.client = http_client or cached_async_http_client()
        self._auth = ApiKeyAuth(api_key)
        self._url = url_template.format(model=model_name)
```

```
def __init__(
    self,
    model_name: GeminiModelName,
    *,
    provider: Literal['google-gla', 'google-vertex'] | Provider[AsyncHTTPClient] | None = None,
    api_key: str | None = None,
    http_client: AsyncHTTPClient | None = None,
    url_template: str = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:',
):
    """Initialize a Gemini model.

    Args:
        model_name: The name of the model to use.
        provider: The provider to use for the model.
        api_key: The API key to use for authentication, if not provided, the `GEMINI_API_KEY` environment variable
            will be used if available.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        url_template: The URL template to use for making requests, you shouldn't need to change this,
            docs [here](https://ai.google.dev/gemini-api/docs/quickstart?lang=rest#make-first-request),
            `model` is substituted with the model name, and `function` is added to the end of the URL.
    """
    self._model_name = model_name
    self._provider = provider

    if provider is not None:
        if isinstance(provider, str):
            self._system = provider
            self.client = infer_provider(provider).client
        else:
            self._system = provider.name
            self.client = provider.client
    else:
        if api_key is None:
            if env_api_key := os.getenv('GEMINI_API_KEY'):
                api_key = env_api_key
            else:
                raise UserError('API key must be provided or set in the GEMINI_API_KEY environment variable')
        self.client = http_client or cached_async_http_client()
        self._auth = ApiKeyAuth(api_key)
        self._url = url_template.format(model=model_name)
```

#### model_name

property

```
property
```

```
model_name: GeminiModelName
```

```
model_name: GeminiModelName
```

[GeminiModelName](https://ai.pydantic.dev#pydantic_ai.models.gemini.GeminiModelName)

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

### AuthProtocol

Bases: Protocol

```
Protocol
```

[Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)

Abstract definition for Gemini authentication.

```
pydantic_ai_slim/pydantic_ai/models/gemini.py
```

```
385
386
387
388
```

```
class AuthProtocol(Protocol):
    """Abstract definition for Gemini authentication."""

    async def headers(self) -> dict[str, str]: ...
```

```
class AuthProtocol(Protocol):
    """Abstract definition for Gemini authentication."""

    async def headers(self) -> dict[str, str]: ...
```

### ApiKeyAuth

dataclass

```
dataclass
```

Authentication using an API key for the X-Goog-Api-Key header.

```
X-Goog-Api-Key
```

```
pydantic_ai_slim/pydantic_ai/models/gemini.py
```

```
391
392
393
394
395
396
397
398
399
```

```
@dataclass
class ApiKeyAuth:
    """Authentication using an API key for the `X-Goog-Api-Key` header."""

    api_key: str

    async def headers(self) -> dict[str, str]:
        # https://cloud.google.com/docs/authentication/api-keys-use#using-with-rest
        return {'X-Goog-Api-Key': self.api_key}
```

```
@dataclass
class ApiKeyAuth:
    """Authentication using an API key for the `X-Goog-Api-Key` header."""

    api_key: str

    async def headers(self) -> dict[str, str]:
        # https://cloud.google.com/docs/authentication/api-keys-use#using-with-rest
        return {'X-Goog-Api-Key': self.api_key}
```

### GeminiStreamedResponse

dataclass

```
dataclass
```

Bases: StreamedResponse

```
StreamedResponse
```

[StreamedResponse](https://ai.pydantic.dev/base/#pydantic_ai.models.StreamedResponse)

Implementation of StreamedResponse for the Gemini model.

```
StreamedResponse
```

```
pydantic_ai_slim/pydantic_ai/models/gemini.py
```

```
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
```

```
@dataclass
class GeminiStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for the Gemini model."""

    _model_name: GeminiModelName
    _content: bytearray
    _stream: AsyncIterator[bytes]
    _timestamp: datetime = field(default_factory=_utils.now_utc, init=False)

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        async for gemini_response in self._get_gemini_responses():
            candidate = gemini_response['candidates'][0]
            if 'content' not in candidate:
                raise UnexpectedModelBehavior('Streamed response has no content field')
            gemini_part: _GeminiPartUnion
            for gemini_part in candidate['content']['parts']:
                if 'text' in gemini_part:
                    # Using vendor_part_id=None means we can produce multiple text parts if their deltas are sprinkled
                    # amongst the tool call deltas
                    yield self._parts_manager.handle_text_delta(vendor_part_id=None, content=gemini_part['text'])

                elif 'function_call' in gemini_part:
                    # Here, we assume all function_call parts are complete and don't have deltas.
                    # We do this by assigning a unique randomly generated "vendor_part_id".
                    # We need to confirm whether this is actually true, but if it isn't, we can still handle it properly
                    # it would just be a bit more complicated. And we'd need to confirm the intended semantics.
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=uuid4(),
                        tool_name=gemini_part['function_call']['name'],
                        args=gemini_part['function_call']['args'],
                        tool_call_id=None,
                    )
                    if maybe_event is not None:
                        yield maybe_event
                else:
                    assert 'function_response' in gemini_part, f'Unexpected part: {gemini_part}'

    async def _get_gemini_responses(self) -> AsyncIterator[_GeminiResponse]:
        # This method exists to ensure we only yield completed items, so we don't need to worry about
        # partial gemini responses, which would make everything more complicated

        gemini_responses: list[_GeminiResponse] = []
        current_gemini_response_index = 0
        # Right now, there are some circumstances where we will have information that could be yielded sooner than it is
        # But changing that would make things a lot more complicated.
        async for chunk in self._stream:
            self._content.extend(chunk)

            gemini_responses = _gemini_streamed_response_ta.validate_json(
                _ensure_decodeable(self._content),
                experimental_allow_partial='trailing-strings',
            )

            # The idea: yield only up to the latest response, which might still be partial.
            # Note that if the latest response is complete, we could yield it immediately, but there's not a good
            # allow_partial API to determine if the last item in the list is complete.
            responses_to_yield = gemini_responses[:-1]
            for r in responses_to_yield[current_gemini_response_index:]:
                current_gemini_response_index += 1
                self._usage += _metadata_as_usage(r)
                yield r

        # Now yield the final response, which should be complete
        if gemini_responses:
            r = gemini_responses[-1]
            self._usage += _metadata_as_usage(r)
            yield r

    @property
    def model_name(self) -> GeminiModelName:
        """Get the model name of the response."""
        return self._model_name

    @property
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._timestamp
```

```
@dataclass
class GeminiStreamedResponse(StreamedResponse):
    """Implementation of `StreamedResponse` for the Gemini model."""

    _model_name: GeminiModelName
    _content: bytearray
    _stream: AsyncIterator[bytes]
    _timestamp: datetime = field(default_factory=_utils.now_utc, init=False)

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        async for gemini_response in self._get_gemini_responses():
            candidate = gemini_response['candidates'][0]
            if 'content' not in candidate:
                raise UnexpectedModelBehavior('Streamed response has no content field')
            gemini_part: _GeminiPartUnion
            for gemini_part in candidate['content']['parts']:
                if 'text' in gemini_part:
                    # Using vendor_part_id=None means we can produce multiple text parts if their deltas are sprinkled
                    # amongst the tool call deltas
                    yield self._parts_manager.handle_text_delta(vendor_part_id=None, content=gemini_part['text'])

                elif 'function_call' in gemini_part:
                    # Here, we assume all function_call parts are complete and don't have deltas.
                    # We do this by assigning a unique randomly generated "vendor_part_id".
                    # We need to confirm whether this is actually true, but if it isn't, we can still handle it properly
                    # it would just be a bit more complicated. And we'd need to confirm the intended semantics.
                    maybe_event = self._parts_manager.handle_tool_call_delta(
                        vendor_part_id=uuid4(),
                        tool_name=gemini_part['function_call']['name'],
                        args=gemini_part['function_call']['args'],
                        tool_call_id=None,
                    )
                    if maybe_event is not None:
                        yield maybe_event
                else:
                    assert 'function_response' in gemini_part, f'Unexpected part: {gemini_part}'

    async def _get_gemini_responses(self) -> AsyncIterator[_GeminiResponse]:
        # This method exists to ensure we only yield completed items, so we don't need to worry about
        # partial gemini responses, which would make everything more complicated

        gemini_responses: list[_GeminiResponse] = []
        current_gemini_response_index = 0
        # Right now, there are some circumstances where we will have information that could be yielded sooner than it is
        # But changing that would make things a lot more complicated.
        async for chunk in self._stream:
            self._content.extend(chunk)

            gemini_responses = _gemini_streamed_response_ta.validate_json(
                _ensure_decodeable(self._content),
                experimental_allow_partial='trailing-strings',
            )

            # The idea: yield only up to the latest response, which might still be partial.
            # Note that if the latest response is complete, we could yield it immediately, but there's not a good
            # allow_partial API to determine if the last item in the list is complete.
            responses_to_yield = gemini_responses[:-1]
            for r in responses_to_yield[current_gemini_response_index:]:
                current_gemini_response_index += 1
                self._usage += _metadata_as_usage(r)
                yield r

        # Now yield the final response, which should be complete
        if gemini_responses:
            r = gemini_responses[-1]
            self._usage += _metadata_as_usage(r)
            yield r

    @property
    def model_name(self) -> GeminiModelName:
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
model_name: GeminiModelName
```

```
model_name: GeminiModelName
```

[GeminiModelName](https://ai.pydantic.dev#pydantic_ai.models.gemini.GeminiModelName)

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

### GeminiSafetySettings

Bases: TypedDict

```
TypedDict
```

[TypedDict](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypedDict)

Safety settings options for Gemini model request.

See Gemini API docs for safety category and threshold descriptions.
For an example on how to use GeminiSafetySettings, see here.

```
GeminiSafetySettings
```

```
pydantic_ai_slim/pydantic_ai/models/gemini.py
```

```
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
```

```
class GeminiSafetySettings(TypedDict):
    """Safety settings options for Gemini model request.

    See [Gemini API docs](https://ai.google.dev/gemini-api/docs/safety-settings) for safety category and threshold descriptions.
    For an example on how to use `GeminiSafetySettings`, see [here](../../agents.md#model-specific-settings).
    """

    category: Literal[
        'HARM_CATEGORY_UNSPECIFIED',
        'HARM_CATEGORY_HARASSMENT',
        'HARM_CATEGORY_HATE_SPEECH',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'HARM_CATEGORY_DANGEROUS_CONTENT',
        'HARM_CATEGORY_CIVIC_INTEGRITY',
    ]
    """
    Safety settings category.
    """

    threshold: Literal[
        'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
        'BLOCK_LOW_AND_ABOVE',
        'BLOCK_MEDIUM_AND_ABOVE',
        'BLOCK_ONLY_HIGH',
        'BLOCK_NONE',
        'OFF',
    ]
    """
    Safety settings threshold.
    """
```

```
class GeminiSafetySettings(TypedDict):
    """Safety settings options for Gemini model request.

    See [Gemini API docs](https://ai.google.dev/gemini-api/docs/safety-settings) for safety category and threshold descriptions.
    For an example on how to use `GeminiSafetySettings`, see [here](../../agents.md#model-specific-settings).
    """

    category: Literal[
        'HARM_CATEGORY_UNSPECIFIED',
        'HARM_CATEGORY_HARASSMENT',
        'HARM_CATEGORY_HATE_SPEECH',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'HARM_CATEGORY_DANGEROUS_CONTENT',
        'HARM_CATEGORY_CIVIC_INTEGRITY',
    ]
    """
    Safety settings category.
    """

    threshold: Literal[
        'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
        'BLOCK_LOW_AND_ABOVE',
        'BLOCK_MEDIUM_AND_ABOVE',
        'BLOCK_ONLY_HIGH',
        'BLOCK_NONE',
        'OFF',
    ]
    """
    Safety settings threshold.
    """
```

#### category

instance-attribute

```
instance-attribute
```

```
category: Literal[
    "HARM_CATEGORY_UNSPECIFIED",
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
    "HARM_CATEGORY_CIVIC_INTEGRITY",
]
```

```
category: Literal[
    "HARM_CATEGORY_UNSPECIFIED",
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
    "HARM_CATEGORY_CIVIC_INTEGRITY",
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Safety settings category.

#### threshold

instance-attribute

```
instance-attribute
```

```
threshold: Literal[
    "HARM_BLOCK_THRESHOLD_UNSPECIFIED",
    "BLOCK_LOW_AND_ABOVE",
    "BLOCK_MEDIUM_AND_ABOVE",
    "BLOCK_ONLY_HIGH",
    "BLOCK_NONE",
    "OFF",
]
```

```
threshold: Literal[
    "HARM_BLOCK_THRESHOLD_UNSPECIFIED",
    "BLOCK_LOW_AND_ABOVE",
    "BLOCK_MEDIUM_AND_ABOVE",
    "BLOCK_ONLY_HIGH",
    "BLOCK_NONE",
    "OFF",
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Safety settings threshold.

