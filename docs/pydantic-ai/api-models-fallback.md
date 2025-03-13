# pydantic_ai.models.fallback

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.models.fallback

[](https://ai.pydantic.dev)

### FallbackModel

dataclass

```
dataclass
```

Bases: Model

```
Model
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

A model that uses one or more fallback models upon failure.

Apart from __init__, all methods are private or match those of the base class.

```
__init__
```

```
pydantic_ai_slim/pydantic_ai/models/fallback.py
```

```
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
```

```
@dataclass(init=False)
class FallbackModel(Model):
    """A model that uses one or more fallback models upon failure.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    models: list[Model]

    _model_name: str = field(repr=False)
    _fallback_on: Callable[[Exception], bool]

    def __init__(
        self,
        default_model: Model | KnownModelName,
        *fallback_models: Model | KnownModelName,
        fallback_on: Callable[[Exception], bool] | tuple[type[Exception], ...] = (ModelHTTPError,),
    ):
        """Initialize a fallback model instance.

        Args:
            default_model: The name or instance of the default model to use.
            fallback_models: The names or instances of the fallback models to use upon failure.
            fallback_on: A callable or tuple of exceptions that should trigger a fallback.
        """
        self.models = [infer_model(default_model), *[infer_model(m) for m in fallback_models]]
        self._model_name = f'FallBackModel[{", ".join(model.model_name for model in self.models)}]'

        if isinstance(fallback_on, tuple):
            self._fallback_on = _default_fallback_condition_factory(fallback_on)
        else:
            self._fallback_on = fallback_on

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, Usage]:
        """Try each model in sequence until one succeeds.

        In case of failure, raise a FallbackExceptionGroup with all exceptions.
        """
        exceptions: list[Exception] = []

        for model in self.models:
            try:
                return await model.request(messages, model_settings, model_request_parameters)
            except Exception as exc:
                if self._fallback_on(exc):
                    exceptions.append(exc)
                    continue
                raise exc

        raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        """Try each model in sequence until one succeeds."""
        exceptions: list[Exception] = []

        for model in self.models:
            async with AsyncExitStack() as stack:
                try:
                    response = await stack.enter_async_context(
                        model.request_stream(messages, model_settings, model_request_parameters)
                    )
                except Exception as exc:
                    if self._fallback_on(exc):
                        exceptions.append(exc)
                        continue
                    raise exc
                yield response
                return

        raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)

    @property
    def model_name(self) -> str:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider, n/a for fallback models."""
        return None
```

```
@dataclass(init=False)
class FallbackModel(Model):
    """A model that uses one or more fallback models upon failure.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    models: list[Model]

    _model_name: str = field(repr=False)
    _fallback_on: Callable[[Exception], bool]

    def __init__(
        self,
        default_model: Model | KnownModelName,
        *fallback_models: Model | KnownModelName,
        fallback_on: Callable[[Exception], bool] | tuple[type[Exception], ...] = (ModelHTTPError,),
    ):
        """Initialize a fallback model instance.

        Args:
            default_model: The name or instance of the default model to use.
            fallback_models: The names or instances of the fallback models to use upon failure.
            fallback_on: A callable or tuple of exceptions that should trigger a fallback.
        """
        self.models = [infer_model(default_model), *[infer_model(m) for m in fallback_models]]
        self._model_name = f'FallBackModel[{", ".join(model.model_name for model in self.models)}]'

        if isinstance(fallback_on, tuple):
            self._fallback_on = _default_fallback_condition_factory(fallback_on)
        else:
            self._fallback_on = fallback_on

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> tuple[ModelResponse, Usage]:
        """Try each model in sequence until one succeeds.

        In case of failure, raise a FallbackExceptionGroup with all exceptions.
        """
        exceptions: list[Exception] = []

        for model in self.models:
            try:
                return await model.request(messages, model_settings, model_request_parameters)
            except Exception as exc:
                if self._fallback_on(exc):
                    exceptions.append(exc)
                    continue
                raise exc

        raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> AsyncIterator[StreamedResponse]:
        """Try each model in sequence until one succeeds."""
        exceptions: list[Exception] = []

        for model in self.models:
            async with AsyncExitStack() as stack:
                try:
                    response = await stack.enter_async_context(
                        model.request_stream(messages, model_settings, model_request_parameters)
                    )
                except Exception as exc:
                    if self._fallback_on(exc):
                        exceptions.append(exc)
                        continue
                    raise exc
                yield response
                return

        raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)

    @property
    def model_name(self) -> str:
        """The model name."""
        return self._model_name

    @property
    def system(self) -> str | None:
        """The system / model provider, n/a for fallback models."""
        return None
```

#### __init__

```
__init__(
    default_model: Model | KnownModelName,
    *fallback_models: Model | KnownModelName,
    fallback_on: (
        Callable[[Exception], bool]
        | tuple[type[Exception], ...]
    ) = (ModelHTTPError,)
)
```

```
__init__(
    default_model: Model | KnownModelName,
    *fallback_models: Model | KnownModelName,
    fallback_on: (
        Callable[[Exception], bool]
        | tuple[type[Exception], ...]
    ) = (ModelHTTPError,)
)
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/base/#pydantic_ai.models.KnownModelName)

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/base/#pydantic_ai.models.KnownModelName)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[Exception](https://docs.python.org/3/library/exceptions.html#Exception)

[bool](https://docs.python.org/3/library/functions.html#bool)

[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

[type](https://docs.python.org/3/library/functions.html#type)

[Exception](https://docs.python.org/3/library/exceptions.html#Exception)

[ModelHTTPError](https://ai.pydantic.dev/exceptions/#pydantic_ai.exceptions.ModelHTTPError)

Initialize a fallback model instance.

Parameters:

```
default_model
```

```
Model | KnownModelName
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/base/#pydantic_ai.models.KnownModelName)

The name or instance of the default model to use.

```
fallback_models
```

```
Model | KnownModelName
```

[Model](https://ai.pydantic.dev/base/#pydantic_ai.models.Model)

[KnownModelName](https://ai.pydantic.dev/base/#pydantic_ai.models.KnownModelName)

The names or instances of the fallback models to use upon failure.

```
()
```

```
fallback_on
```

```
Callable[[Exception], bool] | tuple[type[Exception], ...]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[Exception](https://docs.python.org/3/library/exceptions.html#Exception)

[bool](https://docs.python.org/3/library/functions.html#bool)

[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

[type](https://docs.python.org/3/library/functions.html#type)

[Exception](https://docs.python.org/3/library/exceptions.html#Exception)

A callable or tuple of exceptions that should trigger a fallback.

```
(ModelHTTPError,)
```

[ModelHTTPError](https://ai.pydantic.dev/exceptions/#pydantic_ai.exceptions.ModelHTTPError)

```
pydantic_ai_slim/pydantic_ai/models/fallback.py
```

```
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
```

```
def __init__(
    self,
    default_model: Model | KnownModelName,
    *fallback_models: Model | KnownModelName,
    fallback_on: Callable[[Exception], bool] | tuple[type[Exception], ...] = (ModelHTTPError,),
):
    """Initialize a fallback model instance.

    Args:
        default_model: The name or instance of the default model to use.
        fallback_models: The names or instances of the fallback models to use upon failure.
        fallback_on: A callable or tuple of exceptions that should trigger a fallback.
    """
    self.models = [infer_model(default_model), *[infer_model(m) for m in fallback_models]]
    self._model_name = f'FallBackModel[{", ".join(model.model_name for model in self.models)}]'

    if isinstance(fallback_on, tuple):
        self._fallback_on = _default_fallback_condition_factory(fallback_on)
    else:
        self._fallback_on = fallback_on
```

```
def __init__(
    self,
    default_model: Model | KnownModelName,
    *fallback_models: Model | KnownModelName,
    fallback_on: Callable[[Exception], bool] | tuple[type[Exception], ...] = (ModelHTTPError,),
):
    """Initialize a fallback model instance.

    Args:
        default_model: The name or instance of the default model to use.
        fallback_models: The names or instances of the fallback models to use upon failure.
        fallback_on: A callable or tuple of exceptions that should trigger a fallback.
    """
    self.models = [infer_model(default_model), *[infer_model(m) for m in fallback_models]]
    self._model_name = f'FallBackModel[{", ".join(model.model_name for model in self.models)}]'

    if isinstance(fallback_on, tuple):
        self._fallback_on = _default_fallback_condition_factory(fallback_on)
    else:
        self._fallback_on = fallback_on
```

#### request

async

```
async
```

```
request(
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> tuple[ModelResponse, Usage]
```

```
request(
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> tuple[ModelResponse, Usage]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[ModelRequestParameters](https://ai.pydantic.dev/base/#pydantic_ai.models.ModelRequestParameters)

[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

[ModelResponse](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelResponse)

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Try each model in sequence until one succeeds.

In case of failure, raise a FallbackExceptionGroup with all exceptions.

```
pydantic_ai_slim/pydantic_ai/models/fallback.py
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
```

```
async def request(
    self,
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> tuple[ModelResponse, Usage]:
    """Try each model in sequence until one succeeds.

    In case of failure, raise a FallbackExceptionGroup with all exceptions.
    """
    exceptions: list[Exception] = []

    for model in self.models:
        try:
            return await model.request(messages, model_settings, model_request_parameters)
        except Exception as exc:
            if self._fallback_on(exc):
                exceptions.append(exc)
                continue
            raise exc

    raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)
```

```
async def request(
    self,
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> tuple[ModelResponse, Usage]:
    """Try each model in sequence until one succeeds.

    In case of failure, raise a FallbackExceptionGroup with all exceptions.
    """
    exceptions: list[Exception] = []

    for model in self.models:
        try:
            return await model.request(messages, model_settings, model_request_parameters)
        except Exception as exc:
            if self._fallback_on(exc):
                exceptions.append(exc)
                continue
            raise exc

    raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)
```

#### request_stream

async

```
async
```

```
request_stream(
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> AsyncIterator[StreamedResponse]
```

```
request_stream(
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> AsyncIterator[StreamedResponse]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[ModelSettings](https://ai.pydantic.dev/settings/#pydantic_ai.settings.ModelSettings)

[ModelRequestParameters](https://ai.pydantic.dev/base/#pydantic_ai.models.ModelRequestParameters)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[StreamedResponse](https://ai.pydantic.dev/base/#pydantic_ai.models.StreamedResponse)

Try each model in sequence until one succeeds.

```
pydantic_ai_slim/pydantic_ai/models/fallback.py
```

```
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
```

```
@asynccontextmanager
async def request_stream(
    self,
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> AsyncIterator[StreamedResponse]:
    """Try each model in sequence until one succeeds."""
    exceptions: list[Exception] = []

    for model in self.models:
        async with AsyncExitStack() as stack:
            try:
                response = await stack.enter_async_context(
                    model.request_stream(messages, model_settings, model_request_parameters)
                )
            except Exception as exc:
                if self._fallback_on(exc):
                    exceptions.append(exc)
                    continue
                raise exc
            yield response
            return

    raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)
```

```
@asynccontextmanager
async def request_stream(
    self,
    messages: list[ModelMessage],
    model_settings: ModelSettings | None,
    model_request_parameters: ModelRequestParameters,
) -> AsyncIterator[StreamedResponse]:
    """Try each model in sequence until one succeeds."""
    exceptions: list[Exception] = []

    for model in self.models:
        async with AsyncExitStack() as stack:
            try:
                response = await stack.enter_async_context(
                    model.request_stream(messages, model_settings, model_request_parameters)
                )
            except Exception as exc:
                if self._fallback_on(exc):
                    exceptions.append(exc)
                    continue
                raise exc
            yield response
            return

    raise FallbackExceptionGroup('All models from FallbackModel failed', exceptions)
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

The system / model provider, n/a for fallback models.

