# pydantic_ai.providers

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.providers

```
pydantic_ai.providers
```

[](https://ai.pydantic.dev)

Bases: ABC, Generic[InterfaceClient]

```
ABC
```

[ABC](https://docs.python.org/3/library/abc.html#abc.ABC)

```
Generic[InterfaceClient]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

Abstract class for a provider.

The provider is in charge of providing an authenticated client to the API.

Each provider only supports a specific interface. A interface can be supported by multiple providers.

For example, the OpenAIModel interface can be supported by the OpenAIProvider and the DeepSeekProvider.

```
pydantic_ai_slim/pydantic_ai/providers/__init__.py
```

```
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
```

```
class Provider(ABC, Generic[InterfaceClient]):
    """Abstract class for a provider.

    The provider is in charge of providing an authenticated client to the API.

    Each provider only supports a specific interface. A interface can be supported by multiple providers.

    For example, the OpenAIModel interface can be supported by the OpenAIProvider and the DeepSeekProvider.
    """

    _client: InterfaceClient

    @property
    @abstractmethod
    def name(self) -> str:
        """The provider name."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def base_url(self) -> str:
        """The base URL for the provider API."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def client(self) -> InterfaceClient:
        """The client for the provider."""
        raise NotImplementedError()
```

```
class Provider(ABC, Generic[InterfaceClient]):
    """Abstract class for a provider.

    The provider is in charge of providing an authenticated client to the API.

    Each provider only supports a specific interface. A interface can be supported by multiple providers.

    For example, the OpenAIModel interface can be supported by the OpenAIProvider and the DeepSeekProvider.
    """

    _client: InterfaceClient

    @property
    @abstractmethod
    def name(self) -> str:
        """The provider name."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def base_url(self) -> str:
        """The base URL for the provider API."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def client(self) -> InterfaceClient:
        """The client for the provider."""
        raise NotImplementedError()
```

### name

abstractmethod
property

```
abstractmethod
```

```
property
```

```
name: str
```

```
name: str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The provider name.

### base_url

abstractmethod
property

```
abstractmethod
```

```
property
```

```
base_url: str
```

```
base_url: str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The base URL for the provider API.

### client

abstractmethod
property

```
abstractmethod
```

```
property
```

```
client: InterfaceClient
```

```
client: InterfaceClient
```

The client for the provider.

[](https://ai.pydantic.dev)

### GoogleVertexProvider

Bases: Provider[AsyncClient]

```
Provider[AsyncClient]
```

[Provider](https://ai.pydantic.dev#pydantic_ai.providers.Provider)

Provider for Vertex AI API.

```
pydantic_ai_slim/pydantic_ai/providers/google_vertex.py
```

```
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
```

```
class GoogleVertexProvider(Provider[httpx.AsyncClient]):
    """Provider for Vertex AI API."""

    @property
    def name(self) -> str:
        return 'google-vertex'

    @property
    def base_url(self) -> str:
        return (
            f'https://{self.region}-aiplatform.googleapis.com/v1'
            f'/projects/{self.project_id}'
            f'/locations/{self.region}'
            f'/publishers/{self.model_publisher}/models/'
        )

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    def __init__(
        self,
        service_account_file: Path | str | None = None,
        project_id: str | None = None,
        region: VertexAiRegion = 'us-central1',
        model_publisher: str = 'google',
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Create a new Vertex AI provider.

        Args:
            service_account_file: Path to a service account file.
                If not provided, the default environment credentials will be used.
            project_id: The project ID to use, if not provided it will be taken from the credentials.
            region: The region to make requests to.
            model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
                and from trial and error it seems non-google models don't work with the `generateContent` and
                `streamGenerateContent` functions, hence only `google` is currently supported.
                Please create an issue or PR if you know how to use other publishers.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._client = http_client or cached_async_http_client()
        self.service_account_file = service_account_file
        self.project_id = project_id
        self.region = region
        self.model_publisher = model_publisher

        self._client.auth = _VertexAIAuth(service_account_file, project_id, region)
        self._client.base_url = self.base_url
```

```
class GoogleVertexProvider(Provider[httpx.AsyncClient]):
    """Provider for Vertex AI API."""

    @property
    def name(self) -> str:
        return 'google-vertex'

    @property
    def base_url(self) -> str:
        return (
            f'https://{self.region}-aiplatform.googleapis.com/v1'
            f'/projects/{self.project_id}'
            f'/locations/{self.region}'
            f'/publishers/{self.model_publisher}/models/'
        )

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    def __init__(
        self,
        service_account_file: Path | str | None = None,
        project_id: str | None = None,
        region: VertexAiRegion = 'us-central1',
        model_publisher: str = 'google',
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Create a new Vertex AI provider.

        Args:
            service_account_file: Path to a service account file.
                If not provided, the default environment credentials will be used.
            project_id: The project ID to use, if not provided it will be taken from the credentials.
            region: The region to make requests to.
            model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
                and from trial and error it seems non-google models don't work with the `generateContent` and
                `streamGenerateContent` functions, hence only `google` is currently supported.
                Please create an issue or PR if you know how to use other publishers.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._client = http_client or cached_async_http_client()
        self.service_account_file = service_account_file
        self.project_id = project_id
        self.region = region
        self.model_publisher = model_publisher

        self._client.auth = _VertexAIAuth(service_account_file, project_id, region)
        self._client.base_url = self.base_url
```

#### __init__

```
__init__(
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = "us-central1",
    model_publisher: str = "google",
    http_client: AsyncClient | None = None,
) -> None
```

```
__init__(
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = "us-central1",
    model_publisher: str = "google",
    http_client: AsyncClient | None = None,
) -> None
```

[Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Create a new Vertex AI provider.

Parameters:

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

The region to make requests to.

```
'us-central1'
```

```
model_publisher
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

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
pydantic_ai_slim/pydantic_ai/providers/google_vertex.py
```

```
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
```

```
def __init__(
    self,
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = 'us-central1',
    model_publisher: str = 'google',
    http_client: httpx.AsyncClient | None = None,
) -> None:
    """Create a new Vertex AI provider.

    Args:
        service_account_file: Path to a service account file.
            If not provided, the default environment credentials will be used.
        project_id: The project ID to use, if not provided it will be taken from the credentials.
        region: The region to make requests to.
        model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
            and from trial and error it seems non-google models don't work with the `generateContent` and
            `streamGenerateContent` functions, hence only `google` is currently supported.
            Please create an issue or PR if you know how to use other publishers.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._client = http_client or cached_async_http_client()
    self.service_account_file = service_account_file
    self.project_id = project_id
    self.region = region
    self.model_publisher = model_publisher

    self._client.auth = _VertexAIAuth(service_account_file, project_id, region)
    self._client.base_url = self.base_url
```

```
def __init__(
    self,
    service_account_file: Path | str | None = None,
    project_id: str | None = None,
    region: VertexAiRegion = 'us-central1',
    model_publisher: str = 'google',
    http_client: httpx.AsyncClient | None = None,
) -> None:
    """Create a new Vertex AI provider.

    Args:
        service_account_file: Path to a service account file.
            If not provided, the default environment credentials will be used.
        project_id: The project ID to use, if not provided it will be taken from the credentials.
        region: The region to make requests to.
        model_publisher: The model publisher to use, I couldn't find a good list of available publishers,
            and from trial and error it seems non-google models don't work with the `generateContent` and
            `streamGenerateContent` functions, hence only `google` is currently supported.
            Please create an issue or PR if you know how to use other publishers.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._client = http_client or cached_async_http_client()
    self.service_account_file = service_account_file
    self.project_id = project_id
    self.region = region
    self.model_publisher = model_publisher

    self._client.auth = _VertexAIAuth(service_account_file, project_id, region)
    self._client.base_url = self.base_url
```

[](https://ai.pydantic.dev)

### OpenAIProvider

Bases: Provider[AsyncOpenAI]

```
Provider[AsyncOpenAI]
```

[Provider](https://ai.pydantic.dev#pydantic_ai.providers.Provider)

Provider for OpenAI API.

```
pydantic_ai_slim/pydantic_ai/providers/openai.py
```

```
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
68
69
70
71
72
```

```
class OpenAIProvider(Provider[AsyncOpenAI]):
    """Provider for OpenAI API."""

    @property
    def name(self) -> str:
        return 'openai'  # pragma: no cover

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Create a new OpenAI provider.

        Args:
            base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
                will be used if available. Otherwise, defaults to OpenAI's base url.
            api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
                will be used if available.
            openai_client: An existing
                [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
                client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._base_url = base_url or 'https://api.openai.com/v1'
        # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
        # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
        if api_key is None and 'OPENAI_API_KEY' not in os.environ and openai_client is None:
            api_key = 'api-key-not-set'

        if openai_client is not None:
            assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
            assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
            assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
            self._client = openai_client
        elif http_client is not None:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=http_client)
        else:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=cached_async_http_client())
```

```
class OpenAIProvider(Provider[AsyncOpenAI]):
    """Provider for OpenAI API."""

    @property
    def name(self) -> str:
        return 'openai'  # pragma: no cover

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Create a new OpenAI provider.

        Args:
            base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
                will be used if available. Otherwise, defaults to OpenAI's base url.
            api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
                will be used if available.
            openai_client: An existing
                [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
                client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._base_url = base_url or 'https://api.openai.com/v1'
        # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
        # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
        if api_key is None and 'OPENAI_API_KEY' not in os.environ and openai_client is None:
            api_key = 'api-key-not-set'

        if openai_client is not None:
            assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
            assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
            assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
            self._client = openai_client
        elif http_client is not None:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=http_client)
        else:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=cached_async_http_client())
```

#### __init__

```
__init__(
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncClient | None = None,
) -> None
```

```
__init__(
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: AsyncClient | None = None,
) -> None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Create a new OpenAI provider.

Parameters:

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
pydantic_ai_slim/pydantic_ai/providers/openai.py
```

```
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
```

```
def __init__(
    self,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> None:
    """Create a new OpenAI provider.

    Args:
        base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
            will be used if available. Otherwise, defaults to OpenAI's base url.
        api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
            will be used if available.
        openai_client: An existing
            [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
            client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._base_url = base_url or 'https://api.openai.com/v1'
    # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
    # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
    if api_key is None and 'OPENAI_API_KEY' not in os.environ and openai_client is None:
        api_key = 'api-key-not-set'

    if openai_client is not None:
        assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
        assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
        assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
        self._client = openai_client
    elif http_client is not None:
        self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=http_client)
    else:
        self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=cached_async_http_client())
```

```
def __init__(
    self,
    base_url: str | None = None,
    api_key: str | None = None,
    openai_client: AsyncOpenAI | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> None:
    """Create a new OpenAI provider.

    Args:
        base_url: The base url for the OpenAI requests. If not provided, the `OPENAI_BASE_URL` environment variable
            will be used if available. Otherwise, defaults to OpenAI's base url.
        api_key: The API key to use for authentication, if not provided, the `OPENAI_API_KEY` environment variable
            will be used if available.
        openai_client: An existing
            [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
            client to use. If provided, `base_url`, `api_key`, and `http_client` must be `None`.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
    """
    self._base_url = base_url or 'https://api.openai.com/v1'
    # This is a workaround for the OpenAI client requiring an API key, whilst locally served,
    # openai compatible models do not always need an API key, but a placeholder (non-empty) key is required.
    if api_key is None and 'OPENAI_API_KEY' not in os.environ and openai_client is None:
        api_key = 'api-key-not-set'

    if openai_client is not None:
        assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
        assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
        assert api_key is None, 'Cannot provide both `openai_client` and `api_key`'
        self._client = openai_client
    elif http_client is not None:
        self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=http_client)
    else:
        self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=cached_async_http_client())
```

[](https://ai.pydantic.dev)

### DeepSeekProvider

Bases: Provider[AsyncOpenAI]

```
Provider[AsyncOpenAI]
```

[Provider](https://ai.pydantic.dev#pydantic_ai.providers.Provider)

Provider for DeepSeek API.

```
pydantic_ai_slim/pydantic_ai/providers/deepseek.py
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
68
```

```
class DeepSeekProvider(Provider[AsyncOpenAI]):
    """Provider for DeepSeek API."""

    @property
    def name(self) -> str:
        return 'deepseek'

    @property
    def base_url(self) -> str:
        return 'https://api.deepseek.com'

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, *, api_key: str) -> None: ...

    @overload
    def __init__(self, *, api_key: str, http_client: AsyncHTTPClient) -> None: ...

    @overload
    def __init__(self, *, openai_client: AsyncOpenAI | None = None) -> None: ...

    def __init__(
        self,
        *,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncHTTPClient | None = None,
    ) -> None:
        api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if api_key is None and openai_client is None:
            raise ValueError(
                'Set the `DEEPSEEK_API_KEY` environment variable or pass it via `DeepSeekProvider(api_key=...)`'
                'to use the DeepSeek provider.'
            )

        if openai_client is not None:
            self._client = openai_client
        elif http_client is not None:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=http_client)
        else:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=cached_async_http_client())
```

```
class DeepSeekProvider(Provider[AsyncOpenAI]):
    """Provider for DeepSeek API."""

    @property
    def name(self) -> str:
        return 'deepseek'

    @property
    def base_url(self) -> str:
        return 'https://api.deepseek.com'

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, *, api_key: str) -> None: ...

    @overload
    def __init__(self, *, api_key: str, http_client: AsyncHTTPClient) -> None: ...

    @overload
    def __init__(self, *, openai_client: AsyncOpenAI | None = None) -> None: ...

    def __init__(
        self,
        *,
        api_key: str | None = None,
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncHTTPClient | None = None,
    ) -> None:
        api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if api_key is None and openai_client is None:
            raise ValueError(
                'Set the `DEEPSEEK_API_KEY` environment variable or pass it via `DeepSeekProvider(api_key=...)`'
                'to use the DeepSeek provider.'
            )

        if openai_client is not None:
            self._client = openai_client
        elif http_client is not None:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=http_client)
        else:
            self._client = AsyncOpenAI(base_url=self.base_url, api_key=api_key, http_client=cached_async_http_client())
```

[](https://ai.pydantic.dev)

### BedrockProvider

Bases: Provider[BaseClient]

```
Provider[BaseClient]
```

[Provider](https://ai.pydantic.dev#pydantic_ai.providers.Provider)

Provider for AWS Bedrock.

```
pydantic_ai_slim/pydantic_ai/providers/bedrock.py
```

```
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
68
69
70
71
72
73
74
75
76
```

```
class BedrockProvider(Provider[BaseClient]):
    """Provider for AWS Bedrock."""

    @property
    def name(self) -> str:
        return 'bedrock'

    @property
    def base_url(self) -> str:
        return self._client.meta.endpoint_url

    @property
    def client(self) -> BaseClient:
        return self._client

    @overload
    def __init__(self, *, bedrock_client: BaseClient) -> None: ...

    @overload
    def __init__(
        self,
        *,
        region_name: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
    ) -> None: ...

    def __init__(
        self,
        *,
        bedrock_client: BaseClient | None = None,
        region_name: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
    ) -> None:
        """Initialize the Bedrock provider.

        Args:
            bedrock_client: A boto3 client for Bedrock Runtime. If provided, other arguments are ignored.
            region_name: The AWS region name.
            aws_access_key_id: The AWS access key ID.
            aws_secret_access_key: The AWS secret access key.
            aws_session_token: The AWS session token.
        """
        if bedrock_client is not None:
            self._client = bedrock_client
        else:
            try:
                self._client = boto3.client(  # type: ignore[reportUnknownMemberType]
                    'bedrock-runtime',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    aws_session_token=aws_session_token,
                    region_name=region_name,
                )
            except NoRegionError as exc:  # pragma: no cover
                raise ValueError('You must provide a `region_name` or a boto3 client for Bedrock Runtime.') from exc
```

```
class BedrockProvider(Provider[BaseClient]):
    """Provider for AWS Bedrock."""

    @property
    def name(self) -> str:
        return 'bedrock'

    @property
    def base_url(self) -> str:
        return self._client.meta.endpoint_url

    @property
    def client(self) -> BaseClient:
        return self._client

    @overload
    def __init__(self, *, bedrock_client: BaseClient) -> None: ...

    @overload
    def __init__(
        self,
        *,
        region_name: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
    ) -> None: ...

    def __init__(
        self,
        *,
        bedrock_client: BaseClient | None = None,
        region_name: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
    ) -> None:
        """Initialize the Bedrock provider.

        Args:
            bedrock_client: A boto3 client for Bedrock Runtime. If provided, other arguments are ignored.
            region_name: The AWS region name.
            aws_access_key_id: The AWS access key ID.
            aws_secret_access_key: The AWS secret access key.
            aws_session_token: The AWS session token.
        """
        if bedrock_client is not None:
            self._client = bedrock_client
        else:
            try:
                self._client = boto3.client(  # type: ignore[reportUnknownMemberType]
                    'bedrock-runtime',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    aws_session_token=aws_session_token,
                    region_name=region_name,
                )
            except NoRegionError as exc:  # pragma: no cover
                raise ValueError('You must provide a `region_name` or a boto3 client for Bedrock Runtime.') from exc
```

#### __init__

```
__init__(*, bedrock_client: BaseClient) -> None
```

```
__init__(*, bedrock_client: BaseClient) -> None
```

```
__init__(
    *,
    region_name: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    aws_session_token: str | None = None
) -> None
```

```
__init__(
    *,
    region_name: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    aws_session_token: str | None = None
) -> None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

```
__init__(
    *,
    bedrock_client: BaseClient | None = None,
    region_name: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    aws_session_token: str | None = None
) -> None
```

```
__init__(
    *,
    bedrock_client: BaseClient | None = None,
    region_name: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    aws_session_token: str | None = None
) -> None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Initialize the Bedrock provider.

Parameters:

```
bedrock_client
```

```
BaseClient | None
```

A boto3 client for Bedrock Runtime. If provided, other arguments are ignored.

```
None
```

```
region_name
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The AWS region name.

```
None
```

```
aws_access_key_id
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The AWS access key ID.

```
None
```

```
aws_secret_access_key
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The AWS secret access key.

```
None
```

```
aws_session_token
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The AWS session token.

```
None
```

```
pydantic_ai_slim/pydantic_ai/providers/bedrock.py
```

```
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
```

```
def __init__(
    self,
    *,
    bedrock_client: BaseClient | None = None,
    region_name: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    aws_session_token: str | None = None,
) -> None:
    """Initialize the Bedrock provider.

    Args:
        bedrock_client: A boto3 client for Bedrock Runtime. If provided, other arguments are ignored.
        region_name: The AWS region name.
        aws_access_key_id: The AWS access key ID.
        aws_secret_access_key: The AWS secret access key.
        aws_session_token: The AWS session token.
    """
    if bedrock_client is not None:
        self._client = bedrock_client
    else:
        try:
            self._client = boto3.client(  # type: ignore[reportUnknownMemberType]
                'bedrock-runtime',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                region_name=region_name,
            )
        except NoRegionError as exc:  # pragma: no cover
            raise ValueError('You must provide a `region_name` or a boto3 client for Bedrock Runtime.') from exc
```

```
def __init__(
    self,
    *,
    bedrock_client: BaseClient | None = None,
    region_name: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    aws_session_token: str | None = None,
) -> None:
    """Initialize the Bedrock provider.

    Args:
        bedrock_client: A boto3 client for Bedrock Runtime. If provided, other arguments are ignored.
        region_name: The AWS region name.
        aws_access_key_id: The AWS access key ID.
        aws_secret_access_key: The AWS secret access key.
        aws_session_token: The AWS session token.
    """
    if bedrock_client is not None:
        self._client = bedrock_client
    else:
        try:
            self._client = boto3.client(  # type: ignore[reportUnknownMemberType]
                'bedrock-runtime',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                region_name=region_name,
            )
        except NoRegionError as exc:  # pragma: no cover
            raise ValueError('You must provide a `region_name` or a boto3 client for Bedrock Runtime.') from exc
```

