# pydantic_ai.models.vertexai

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.vertexai

```
pydantic_ai.models.vertexai
```

Deprecated

The VertexAIModel is deprecated. You can use the
GoogleVertexProvider to authenticate with the Vertex AI API
and then use the GeminiModel to use the Gemini API.

```
VertexAIModel
```

```
GoogleVertexProvider
```

```
GeminiModel
```

Custom interface to the *-aiplatform.googleapis.com API for Gemini models.

```
*-aiplatform.googleapis.com
```

This model inherits from GeminiModel with just the URL and auth method
changed, it relies on the VertexAI
generateContent
and
streamGenerateContent
function endpoints
having the same schemas as the equivalent Gemini endpoints.

```
GeminiModel
```

```
generateContent
```

```
streamGenerateContent
```

## Setup

For details on how to set up authentication with this model as well as a comparison with the generativelanguage.googleapis.com API used by GeminiModel,
see model configuration for Gemini via VertexAI.

```
generativelanguage.googleapis.com
```

```
GeminiModel
```

## Example Usage

With the default google project already configured in your environment using "application default credentials":

```
from pydantic_ai import Agent
from pydantic_ai.models.vertexai import VertexAIModel

model = VertexAIModel('gemini-1.5-flash')  # (1)!
agent = Agent(model)
result = agent.run_sync('Tell me a joke.')
print(result.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.
```

```
from pydantic_ai import Agent
from pydantic_ai.models.vertexai import VertexAIModel

model = VertexAIModel('gemini-1.5-flash')  # (1)!
agent = Agent(model)
result = agent.run_sync('Tell me a joke.')
print(result.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.
```

1. The VertexAIModel is deprecated, you should use the GeminiModel
   with the GoogleVertexProvider instead.

```
VertexAIModel
```

```
GeminiModel
```

```
GoogleVertexProvider
```

Or using a service account JSON file:

```
from pydantic_ai import Agent
from pydantic_ai.models.vertexai import VertexAIModel

model = VertexAIModel(  # (1)!
    'gemini-1.5-flash',
    service_account_file='path/to/service-account.json',
)
agent = Agent(model)
result = agent.run_sync('Tell me a joke.')
print(result.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.
```

```
from pydantic_ai import Agent
from pydantic_ai.models.vertexai import VertexAIModel

model = VertexAIModel(  # (1)!
    'gemini-1.5-flash',
    service_account_file='path/to/service-account.json',
)
agent = Agent(model)
result = agent.run_sync('Tell me a joke.')
print(result.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.
```

1. The VertexAIModel is deprecated, you should use the GeminiModel
   with the GoogleVertexProvider instead.

```
VertexAIModel
```

```
GeminiModel
```

```
GoogleVertexProvider
```

[](https://ai.pydantic.dev)

### VERTEX_AI_URL_TEMPLATE

module-attribute

```
module-attribute
```

```
VERTEX_AI_URL_TEMPLATE = "https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/{model_publisher}/models/{model}:"
```

```
VERTEX_AI_URL_TEMPLATE = "https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/{model_publisher}/models/{model}:"
```

URL template for Vertex AI.

See
generateContent docs
and
streamGenerateContent docs
for more information.

```
generateContent
```

```
streamGenerateContent
```

The template is used thus:

* region is substituted with the region argument,
  see available regions
* model_publisher is substituted with the model_publisher argument
* model is substituted with the model_name argument
* project_id is substituted with the project_id from auth/credentials
* function (generateContent or streamGenerateContent) is added to the end of the URL

```
region
```

```
region
```

```
model_publisher
```

```
model_publisher
```

```
model
```

```
model_name
```

```
project_id
```

```
project_id
```

```
function
```

```
generateContent
```

```
streamGenerateContent
```

### VertexAIModel

dataclass

```
dataclass
```

Bases: GeminiModel

```
GeminiModel
```

[GeminiModel](https://ai.pydantic.dev/gemini/#pydantic_ai.models.gemini.GeminiModel)

A model that uses Gemini via the *-aiplatform.googleapis.com VertexAI API.

```
*-aiplatform.googleapis.com
```

```
pydantic_ai_slim/pydantic_ai/models/vertexai.py
```

```
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
```

```
@deprecated('Please use `GeminiModel(provider=GoogleVertexProvider(...))` instead.')
@dataclass(init=False)
class VertexAIModel(GeminiModel):
    """A model that uses Gemini via the `*-aiplatform.googleapis.com` VertexAI API."""

    service_account_file: Path | str | None
    project_id: str | None
    region: VertexAiRegion
    model_publisher: Literal['google']
    url_template: str

    _model_name: GeminiModelName = field(repr=False)
    _system: str | None = field(default='google-vertex', repr=False)

    # TODO __init__ can be removed once we drop 3.9 and we can set kw_only correctly on the dataclass
    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        service_account_file: Path | str | None = None,
        project_id: str | None = None,
        region: VertexAiRegion = 'us-central1',
        model_publisher: Literal['google'] = 'google',
        http_client: AsyncHTTPClient | None = None,
        url_template: str = VERTEX_AI_URL_TEMPLATE,
    ):
        """Initialize a Vertex AI Gemini model.

        Args:
            model_name: The name of the model to use. I couldn't find a list of supported Google models, in VertexAI
                so for now this uses the same models as the [Gemini model][pydantic_ai.models.gemini.GeminiModel].
            service_account_file: Path to a service account file.
                If not provided, the default environment credentials will be used.
            project_id: The project ID to use, if not provided it will be taken from the credentials.
            region: The region to make requests to.
            model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
                and from trial and error it seems non-google models don't work with the `generateContent` and
                `streamGenerateContent` functions, hence only `google` is currently supported.
                Please create an issue or PR if you know how to use other publishers.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
            url_template: URL template for Vertex AI, see
                [`VERTEX_AI_URL_TEMPLATE` docs][pydantic_ai.models.vertexai.VERTEX_AI_URL_TEMPLATE]
                for more information.
        """
        self._model_name = model_name
        self.service_account_file = service_account_file
        self.project_id = project_id
        self.region = region
        self.model_publisher = model_publisher
        self.client = http_client or cached_async_http_client()
        self.url_template = url_template

        self._auth = None
        self._url = None
        warnings.warn(
            'VertexAIModel is deprecated, please use `GeminiModel(provider=GoogleVertexProvider(...))` instead.',
            DeprecationWarning,
        )
        self._provider = None

    async def ainit(self) -> None:
        """Initialize the model, setting the URL and auth.

        This will raise an error if authentication fails.
        """
        if self._url is not None and self._auth is not None:
            return

        if self.service_account_file is not None:
            creds: BaseCredentials | ServiceAccountCredentials = _creds_from_file(self.service_account_file)
            assert creds.project_id is None or isinstance(creds.project_id, str)
            creds_project_id: str | None = creds.project_id
            creds_source = 'service account file'
        else:
            creds, creds_project_id = await _async_google_auth()
            creds_source = '`google.auth.default()`'

        if self.project_id is None:
            if creds_project_id is None:
                raise UserError(f'No project_id provided and none found in {creds_source}')
            project_id = creds_project_id
        else:
            project_id = self.project_id

        self._url = self.url_template.format(
            region=self.region,
            project_id=project_id,
            model_publisher=self.model_publisher,
            model=self._model_name,
        )
        self._auth = BearerTokenAuth(creds)

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        await self.ainit()
        return await super().request(messages, model_settings, model_request_parameters)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        await self.ainit()
        async with super().request_stream(messages, model_settings, model_request_parameters) as value:
            yield value

    @property
    def model_name(self) -> GeminiModelName:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider."""
        return self._system
```

```
@deprecated('Please use `GeminiModel(provider=GoogleVertexProvider(...))` instead.')
@dataclass(init=False)
class VertexAIModel(GeminiModel):
    """A model that uses Gemini via the `*-aiplatform.googleapis.com` VertexAI API."""

    service_account_file: Path | str | None
    project_id: str | None
    region: VertexAiRegion
    model_publisher: Literal['google']
    url_template: str

    _model_name: GeminiModelName = field(repr=False)
    _system: str | None = field(default='google-vertex', repr=False)

    # TODO __init__ can be removed once we drop 3.9 and we can set kw_only correctly on the dataclass
    def __init__(
        self,
        model_name: GeminiModelName,
        *,
        service_account_file: Path | str | None = None,
        project_id: str | None = None,
        region: VertexAiRegion = 'us-central1',
        model_publisher: Literal['google'] = 'google',
        http_client: AsyncHTTPClient | None = None,
        url_template: str = VERTEX_AI_URL_TEMPLATE,
    ):
        """Initialize a Vertex AI Gemini model.

        Args:
            model_name: The name of the model to use. I couldn't find a list of supported Google models, in VertexAI
                so for now this uses the same models as the [Gemini model][pydantic_ai.models.gemini.GeminiModel].
            service_account_file: Path to a service account file.
                If not provided, the default environment credentials will be used.
            project_id: The project ID to use, if not provided it will be taken from the credentials.
            region: The region to make requests to.
            model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
                and from trial and error it seems non-google models don't work with the `generateContent` and
                `streamGenerateContent` functions, hence only `google` is currently supported.
                Please create an issue or PR if you know how to use other publishers.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
            url_template: URL template for Vertex AI, see
                [`VERTEX_AI_URL_TEMPLATE` docs][pydantic_ai.models.vertexai.VERTEX_AI_URL_TEMPLATE]
                for more information.
        """
        self._model_name = model_name
        self.service_account_file = service_account_file
        self.project_id = project_id
        self.region = region
        self.model_publisher = model_publisher
        self.client = http_client or cached_async_http_client()
        self.url_template = url_template

        self._auth = None
        self._url = None
        warnings.warn(
            'VertexAIModel is deprecated, please use `GeminiModel(provider=GoogleVertexProvider(...))` instead.',
            DeprecationWarning,
        )
        self._provider = None

    async def ainit(self) -> None:
        """Initialize the model, setting the URL and auth.

        This will raise an error if authentication fails.
        """
        if self._url is not None and self._auth is not None:
            return

        if self.service_account_file is not None:
            creds: BaseCredentials | ServiceAccountCredentials = _creds_from_file(self.service_account_file)
            assert creds.project_id is None or isinstance(creds.project_id, str)
            creds_project_id: str | None = creds.project_id
            creds_source = 'service account file'
        else:
            creds, creds_project_id = await _async_google_auth()
            creds_source = '`google.auth.default()`'

        if self.project_id is None:
            if creds_project_id is None:
                raise UserError(f'No project_id provided and none found in {creds_source}')
            project_id = creds_project_id
        else:
            project_id = self.project_id

        self._url = self.url_template.format(
            region=self.region,
            project_id=project_id,
            model_publisher=self.model_publisher,
            model=self._model_name,
        )
        self._auth = BearerTokenAuth(creds)

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, usage.Usage]:
        await self.ainit()
        return await super().request(messages, model_settings, model_request_parameters)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        await self.ainit()
        async with super().request_stream(messages, model_settings, model_request_parameters) as value:
            yield value

    @property
    def model_name(self) -> GeminiModelName:
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
    model_name: GeminiModelName,
    *,
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = "us-central1",
    model_publisher: Literal["google"] = "google",
    http_client: AsyncClient | None = None,
    url_template: str = VERTEX_AI_URL_TEMPLATE
)
```

```
__init__(
    model_name: GeminiModelName,
    *,
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = "us-central1",
    model_publisher: Literal["google"] = "google",
    http_client: AsyncClient | None = None,
    url_template: str = VERTEX_AI_URL_TEMPLATE
)
```

[GeminiModelName](https://ai.pydantic.dev/gemini/#pydantic_ai.models.gemini.GeminiModelName)

[Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[VertexAiRegion](https://ai.pydantic.dev#pydantic_ai.models.vertexai.VertexAiRegion)

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[VERTEX_AI_URL_TEMPLATE](https://ai.pydantic.dev#pydantic_ai.models.vertexai.VERTEX_AI_URL_TEMPLATE)

Initialize a Vertex AI Gemini model.

Parameters:

```
model_name
```

```
GeminiModelName
```

[GeminiModelName](https://ai.pydantic.dev/gemini/#pydantic_ai.models.gemini.GeminiModelName)

The name of the model to use. I couldn't find a list of supported Google models, in VertexAI
so for now this uses the same models as the Gemini model.

```
service_account_file
```

```
Path | str | None
```

[Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Path to a service account file.
If not provided, the default environment credentials will be used.

```
None
```

```
project_id
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The project ID to use, if not provided it will be taken from the credentials.

```
None
```

```
region
```

```
VertexAiRegion
```

[VertexAiRegion](https://ai.pydantic.dev#pydantic_ai.models.vertexai.VertexAiRegion)

The region to make requests to.

```
'us-central1'
```

```
model_publisher
```

```
Literal['google']
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

The model publisher to use, I couldn't find a good list of available publishers,
and from trial and error it seems non-google models don't work with the generateContent and
streamGenerateContent functions, hence only google is currently supported.
Please create an issue or PR if you know how to use other publishers.

```
generateContent
```

```
streamGenerateContent
```

```
google
```

```
'google'
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

URL template for Vertex AI, see
VERTEX_AI_URL_TEMPLATE docs
for more information.

```
VERTEX_AI_URL_TEMPLATE
```

```
VERTEX_AI_URL_TEMPLATE
```

[VERTEX_AI_URL_TEMPLATE](https://ai.pydantic.dev#pydantic_ai.models.vertexai.VERTEX_AI_URL_TEMPLATE)

```
pydantic_ai_slim/pydantic_ai/models/vertexai.py
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
```

```
def __init__(
    self,
    model_name: GeminiModelName,
    *,
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = 'us-central1',
    model_publisher: Literal['google'] = 'google',
    http_client: AsyncHTTPClient | None = None,
    url_template: str = VERTEX_AI_URL_TEMPLATE,
):
    """Initialize a Vertex AI Gemini model.

    Args:
        model_name: The name of the model to use. I couldn't find a list of supported Google models, in VertexAI
            so for now this uses the same models as the [Gemini model][pydantic_ai.models.gemini.GeminiModel].
        service_account_file: Path to a service account file.
            If not provided, the default environment credentials will be used.
        project_id: The project ID to use, if not provided it will be taken from the credentials.
        region: The region to make requests to.
        model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
            and from trial and error it seems non-google models don't work with the `generateContent` and
            `streamGenerateContent` functions, hence only `google` is currently supported.
            Please create an issue or PR if you know how to use other publishers.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        url_template: URL template for Vertex AI, see
            [`VERTEX_AI_URL_TEMPLATE` docs][pydantic_ai.models.vertexai.VERTEX_AI_URL_TEMPLATE]
            for more information.
    """
    self._model_name = model_name
    self.service_account_file = service_account_file
    self.project_id = project_id
    self.region = region
    self.model_publisher = model_publisher
    self.client = http_client or cached_async_http_client()
    self.url_template = url_template

    self._auth = None
    self._url = None
    warnings.warn(
        'VertexAIModel is deprecated, please use `GeminiModel(provider=GoogleVertexProvider(...))` instead.',
        DeprecationWarning,
    )
    self._provider = None
```

```
def __init__(
    self,
    model_name: GeminiModelName,
    *,
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = 'us-central1',
    model_publisher: Literal['google'] = 'google',
    http_client: AsyncHTTPClient | None = None,
    url_template: str = VERTEX_AI_URL_TEMPLATE,
):
    """Initialize a Vertex AI Gemini model.

    Args:
        model_name: The name of the model to use. I couldn't find a list of supported Google models, in VertexAI
            so for now this uses the same models as the [Gemini model][pydantic_ai.models.gemini.GeminiModel].
        service_account_file: Path to a service account file.
            If not provided, the default environment credentials will be used.
        project_id: The project ID to use, if not provided it will be taken from the credentials.
        region: The region to make requests to.
        model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
            and from trial and error it seems non-google models don't work with the `generateContent` and
            `streamGenerateContent` functions, hence only `google` is currently supported.
            Please create an issue or PR if you know how to use other publishers.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        url_template: URL template for Vertex AI, see
            [`VERTEX_AI_URL_TEMPLATE` docs][pydantic_ai.models.vertexai.VERTEX_AI_URL_TEMPLATE]
            for more information.
    """
    self._model_name = model_name
    self.service_account_file = service_account_file
    self.project_id = project_id
    self.region = region
    self.model_publisher = model_publisher
    self.client = http_client or cached_async_http_client()
    self.url_template = url_template

    self._auth = None
    self._url = None
    warnings.warn(
        'VertexAIModel is deprecated, please use `GeminiModel(provider=GoogleVertexProvider(...))` instead.',
        DeprecationWarning,
    )
    self._provider = None
```

#### ainit

async

```
async
```

```
ainit() -> None
```

```
ainit() -> None
```

Initialize the model, setting the URL and auth.

This will raise an error if authentication fails.

```
pydantic_ai_slim/pydantic_ai/models/vertexai.py
```

```
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
```

```
async def ainit(self) -> None:
    """Initialize the model, setting the URL and auth.

    This will raise an error if authentication fails.
    """
    if self._url is not None and self._auth is not None:
        return

    if self.service_account_file is not None:
        creds: BaseCredentials | ServiceAccountCredentials = _creds_from_file(self.service_account_file)
        assert creds.project_id is None or isinstance(creds.project_id, str)
        creds_project_id: str | None = creds.project_id
        creds_source = 'service account file'
    else:
        creds, creds_project_id = await _async_google_auth()
        creds_source = '`google.auth.default()`'

    if self.project_id is None:
        if creds_project_id is None:
            raise UserError(f'No project_id provided and none found in {creds_source}')
        project_id = creds_project_id
    else:
        project_id = self.project_id

    self._url = self.url_template.format(
        region=self.region,
        project_id=project_id,
        model_publisher=self.model_publisher,
        model=self._model_name,
    )
    self._auth = BearerTokenAuth(creds)
```

```
async def ainit(self) -> None:
    """Initialize the model, setting the URL and auth.

    This will raise an error if authentication fails.
    """
    if self._url is not None and self._auth is not None:
        return

    if self.service_account_file is not None:
        creds: BaseCredentials | ServiceAccountCredentials = _creds_from_file(self.service_account_file)
        assert creds.project_id is None or isinstance(creds.project_id, str)
        creds_project_id: str | None = creds.project_id
        creds_source = 'service account file'
    else:
        creds, creds_project_id = await _async_google_auth()
        creds_source = '`google.auth.default()`'

    if self.project_id is None:
        if creds_project_id is None:
            raise UserError(f'No project_id provided and none found in {creds_source}')
        project_id = creds_project_id
    else:
        project_id = self.project_id

    self._url = self.url_template.format(
        region=self.region,
        project_id=project_id,
        model_publisher=self.model_publisher,
        model=self._model_name,
    )
    self._auth = BearerTokenAuth(creds)
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

[GeminiModelName](https://ai.pydantic.dev/gemini/#pydantic_ai.models.gemini.GeminiModelName)

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

### BearerTokenAuth

dataclass

```
dataclass
```

Authentication using a bearer token generated by google-auth.

```
pydantic_ai_slim/pydantic_ai/models/vertexai.py
```

```
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
```

```
@dataclass
class BearerTokenAuth:
    """Authentication using a bearer token generated by google-auth."""

    credentials: BaseCredentials | ServiceAccountCredentials
    token_created: datetime | None = field(default=None, init=False)

    async def headers(self) -> dict[str, str]:
        if self.credentials.token is None or self._token_expired():
            await run_in_executor(self._refresh_token)
            self.token_created = datetime.now()
        return {'Authorization': f'Bearer {self.credentials.token}'}

    def _token_expired(self) -> bool:
        if self.token_created is None:
            return True
        else:
            return (datetime.now() - self.token_created) > MAX_TOKEN_AGE

    def _refresh_token(self) -> str:
        self.credentials.refresh(Request())
        assert isinstance(self.credentials.token, str), f'Expected token to be a string, got {self.credentials.token}'
        return self.credentials.token
```

```
@dataclass
class BearerTokenAuth:
    """Authentication using a bearer token generated by google-auth."""

    credentials: BaseCredentials | ServiceAccountCredentials
    token_created: datetime | None = field(default=None, init=False)

    async def headers(self) -> dict[str, str]:
        if self.credentials.token is None or self._token_expired():
            await run_in_executor(self._refresh_token)
            self.token_created = datetime.now()
        return {'Authorization': f'Bearer {self.credentials.token}'}

    def _token_expired(self) -> bool:
        if self.token_created is None:
            return True
        else:
            return (datetime.now() - self.token_created) > MAX_TOKEN_AGE

    def _refresh_token(self) -> str:
        self.credentials.refresh(Request())
        assert isinstance(self.credentials.token, str), f'Expected token to be a string, got {self.credentials.token}'
        return self.credentials.token
```

### VertexAiRegion

module-attribute

```
module-attribute
```

```
VertexAiRegion = Literal[
    "asia-east1",
    "asia-east2",
    "asia-northeast1",
    "asia-northeast3",
    "asia-south1",
    "asia-southeast1",
    "australia-southeast1",
    "europe-central2",
    "europe-north1",
    "europe-southwest1",
    "europe-west1",
    "europe-west2",
    "europe-west3",
    "europe-west4",
    "europe-west6",
    "europe-west8",
    "europe-west9",
    "me-central1",
    "me-central2",
    "me-west1",
    "northamerica-northeast1",
    "southamerica-east1",
    "us-central1",
    "us-east1",
    "us-east4",
    "us-east5",
    "us-south1",
    "us-west1",
    "us-west4",
]
```

```
VertexAiRegion = Literal[
    "asia-east1",
    "asia-east2",
    "asia-northeast1",
    "asia-northeast3",
    "asia-south1",
    "asia-southeast1",
    "australia-southeast1",
    "europe-central2",
    "europe-north1",
    "europe-southwest1",
    "europe-west1",
    "europe-west2",
    "europe-west3",
    "europe-west4",
    "europe-west6",
    "europe-west8",
    "europe-west9",
    "me-central1",
    "me-central2",
    "me-west1",
    "northamerica-northeast1",
    "southamerica-east1",
    "us-central1",
    "us-east1",
    "us-east4",
    "us-east5",
    "us-south1",
    "us-west1",
    "us-west4",
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Regions available for Vertex AI.

More details here.

