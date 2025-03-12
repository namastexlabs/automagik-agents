# pydantic_ai.tools

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.tools

```
pydantic_ai.tools
```

[](https://ai.pydantic.dev)

### AgentDepsT

module-attribute

```
module-attribute
```

```
AgentDepsT = TypeVar(
    "AgentDepsT", default=None, contravariant=True
)
```

```
AgentDepsT = TypeVar(
    "AgentDepsT", default=None, contravariant=True
)
```

Type variable for agent dependencies.

### RunContext

dataclass

```
dataclass
```

Bases: Generic[AgentDepsT]

```
Generic[AgentDepsT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

Information about the current call.

```
pydantic_ai_slim/pydantic_ai/tools.py
```

```
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
```

```
@dataclasses.dataclass
class RunContext(Generic[AgentDepsT]):
    """Information about the current call."""

    deps: AgentDepsT
    """Dependencies for the agent."""
    model: models.Model
    """The model used in this run."""
    usage: Usage
    """LLM usage associated with the run."""
    prompt: str | Sequence[_messages.UserContent]
    """The original user prompt passed to the run."""
    messages: list[_messages.ModelMessage] = field(default_factory=list)
    """Messages exchanged in the conversation so far."""
    tool_call_id: str | None = None
    """The ID of the tool call."""
    tool_name: str | None = None
    """Name of the tool being called."""
    retry: int = 0
    """Number of retries so far."""
    run_step: int = 0
    """The current step in the run."""

    def replace_with(
        self, retry: int | None = None, tool_name: str | None | _utils.Unset = _utils.UNSET
    ) -> RunContext[AgentDepsT]:
        # Create a new `RunContext` a new `retry` value and `tool_name`.
        kwargs = {}
        if retry is not None:
            kwargs['retry'] = retry
        if tool_name is not _utils.UNSET:
            kwargs['tool_name'] = tool_name
        return dataclasses.replace(self, **kwargs)
```

```
@dataclasses.dataclass
class RunContext(Generic[AgentDepsT]):
    """Information about the current call."""

    deps: AgentDepsT
    """Dependencies for the agent."""
    model: models.Model
    """The model used in this run."""
    usage: Usage
    """LLM usage associated with the run."""
    prompt: str | Sequence[_messages.UserContent]
    """The original user prompt passed to the run."""
    messages: list[_messages.ModelMessage] = field(default_factory=list)
    """Messages exchanged in the conversation so far."""
    tool_call_id: str | None = None
    """The ID of the tool call."""
    tool_name: str | None = None
    """Name of the tool being called."""
    retry: int = 0
    """Number of retries so far."""
    run_step: int = 0
    """The current step in the run."""

    def replace_with(
        self, retry: int | None = None, tool_name: str | None | _utils.Unset = _utils.UNSET
    ) -> RunContext[AgentDepsT]:
        # Create a new `RunContext` a new `retry` value and `tool_name`.
        kwargs = {}
        if retry is not None:
            kwargs['retry'] = retry
        if tool_name is not _utils.UNSET:
            kwargs['tool_name'] = tool_name
        return dataclasses.replace(self, **kwargs)
```

#### deps

instance-attribute

```
instance-attribute
```

```
deps: AgentDepsT
```

```
deps: AgentDepsT
```

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

Dependencies for the agent.

#### model

instance-attribute

```
instance-attribute
```

```
model: Model
```

```
model: Model
```

[Model](https://ai.pydantic.dev/models/base/#pydantic_ai.models.Model)

The model used in this run.

#### usage

instance-attribute

```
instance-attribute
```

```
usage: Usage
```

```
usage: Usage
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

LLM usage associated with the run.

#### prompt

instance-attribute

```
instance-attribute
```

```
prompt: str | Sequence[UserContent]
```

```
prompt: str | Sequence[UserContent]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

The original user prompt passed to the run.

#### messages

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
messages: list[ModelMessage] = field(default_factory=list)
```

```
messages: list[ModelMessage] = field(default_factory=list)
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

[field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field)

[list](https://docs.python.org/3/library/stdtypes.html#list)

Messages exchanged in the conversation so far.

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

The ID of the tool call.

#### tool_name

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
tool_name: str | None = None
```

```
tool_name: str | None = None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Name of the tool being called.

#### retry

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
retry: int = 0
```

```
retry: int = 0
```

[int](https://docs.python.org/3/library/functions.html#int)

Number of retries so far.

#### run_step

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
run_step: int = 0
```

```
run_step: int = 0
```

[int](https://docs.python.org/3/library/functions.html#int)

The current step in the run.

### ToolParams

module-attribute

```
module-attribute
```

```
ToolParams = ParamSpec('ToolParams', default=...)
```

```
ToolParams = ParamSpec('ToolParams', default=...)
```

[ParamSpec](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.ParamSpec)

Retrieval function param spec.

### SystemPromptFunc

module-attribute

```
module-attribute
```

```
SystemPromptFunc = Union[
    Callable[[RunContext[AgentDepsT]], str],
    Callable[[RunContext[AgentDepsT]], Awaitable[str]],
    Callable[[], str],
    Callable[[], Awaitable[str]],
]
```

```
SystemPromptFunc = Union[
    Callable[[RunContext[AgentDepsT]], str],
    Callable[[RunContext[AgentDepsT]], Awaitable[str]],
    Callable[[], str],
    Callable[[], Awaitable[str]],
]
```

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[RunContext](https://ai.pydantic.dev#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable)

[str](https://docs.python.org/3/library/stdtypes.html#str)

A function that may or maybe not take RunContext as an argument, and may or may not be async.

```
RunContext
```

Usage SystemPromptFunc[AgentDepsT].

```
SystemPromptFunc[AgentDepsT]
```

### ToolFuncContext

module-attribute

```
module-attribute
```

```
ToolFuncContext = Callable[
    Concatenate[RunContext[AgentDepsT], ToolParams], Any
]
```

```
ToolFuncContext = Callable[
    Concatenate[RunContext[AgentDepsT], ToolParams], Any
]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[Concatenate](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Concatenate)

[RunContext](https://ai.pydantic.dev#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev#pydantic_ai.tools.ToolParams)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

A tool function that takes RunContext as the first argument.

```
RunContext
```

Usage ToolContextFunc[AgentDepsT, ToolParams].

```
ToolContextFunc[AgentDepsT, ToolParams]
```

### ToolFuncPlain

module-attribute

```
module-attribute
```

```
ToolFuncPlain = Callable[ToolParams, Any]
```

```
ToolFuncPlain = Callable[ToolParams, Any]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[ToolParams](https://ai.pydantic.dev#pydantic_ai.tools.ToolParams)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

A tool function that does not take RunContext as the first argument.

```
RunContext
```

Usage ToolPlainFunc[ToolParams].

```
ToolPlainFunc[ToolParams]
```

### ToolFuncEither

module-attribute

```
module-attribute
```

```
ToolFuncEither = Union[
    ToolFuncContext[AgentDepsT, ToolParams],
    ToolFuncPlain[ToolParams],
]
```

```
ToolFuncEither = Union[
    ToolFuncContext[AgentDepsT, ToolParams],
    ToolFuncPlain[ToolParams],
]
```

[Union](https://docs.python.org/3/library/typing.html#typing.Union)

[ToolFuncContext](https://ai.pydantic.dev#pydantic_ai.tools.ToolFuncContext)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[ToolParams](https://ai.pydantic.dev#pydantic_ai.tools.ToolParams)

[ToolFuncPlain](https://ai.pydantic.dev#pydantic_ai.tools.ToolFuncPlain)

[ToolParams](https://ai.pydantic.dev#pydantic_ai.tools.ToolParams)

Either kind of tool function.

This is just a union of ToolFuncContext and
ToolFuncPlain.

```
ToolFuncContext
```

```
ToolFuncPlain
```

Usage ToolFuncEither[AgentDepsT, ToolParams].

```
ToolFuncEither[AgentDepsT, ToolParams]
```

### ToolPrepareFunc

module-attribute

```
module-attribute
```

```
ToolPrepareFunc: TypeAlias = (
    "Callable[[RunContext[AgentDepsT], ToolDefinition], Awaitable[ToolDefinition | None]]"
)
```

```
ToolPrepareFunc: TypeAlias = (
    "Callable[[RunContext[AgentDepsT], ToolDefinition], Awaitable[ToolDefinition | None]]"
)
```

[TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias)

Definition of a function that can prepare a tool definition at call time.

See tool docs for more information.

Example â here only_if_42 is valid as a ToolPrepareFunc:

```
only_if_42
```

```
ToolPrepareFunc
```

```
from typing import Union

from pydantic_ai import RunContext, Tool
from pydantic_ai.tools import ToolDefinition

async def only_if_42(
    ctx: RunContext[int], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps == 42:
        return tool_def

def hitchhiker(ctx: RunContext[int], answer: str) -> str:
    return f'{ctx.deps} {answer}'

hitchhiker = Tool(hitchhiker, prepare=only_if_42)
```

```
from typing import Union

from pydantic_ai import RunContext, Tool
from pydantic_ai.tools import ToolDefinition

async def only_if_42(
    ctx: RunContext[int], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps == 42:
        return tool_def

def hitchhiker(ctx: RunContext[int], answer: str) -> str:
    return f'{ctx.deps} {answer}'

hitchhiker = Tool(hitchhiker, prepare=only_if_42)
```

Usage ToolPrepareFunc[AgentDepsT].

```
ToolPrepareFunc[AgentDepsT]
```

### DocstringFormat

module-attribute

```
module-attribute
```

```
DocstringFormat = Literal[
    "google", "numpy", "sphinx", "auto"
]
```

```
DocstringFormat = Literal[
    "google", "numpy", "sphinx", "auto"
]
```

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

Supported docstring formats.

* 'google' â Google-style docstrings.
* 'numpy' â Numpy-style docstrings.
* 'sphinx' â Sphinx-style docstrings.
* 'auto' â Automatically infer the format based on the structure of the docstring.

```
'google'
```

```
'numpy'
```

```
'sphinx'
```

```
'auto'
```

### Tool

dataclass

```
dataclass
```

Bases: Generic[AgentDepsT]

```
Generic[AgentDepsT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

A tool function for an agent.

```
pydantic_ai_slim/pydantic_ai/tools.py
```

```
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
```

```
@dataclass(init=False)
class Tool(Generic[AgentDepsT]):
    """A tool function for an agent."""

    function: ToolFuncEither[AgentDepsT]
    takes_ctx: bool
    max_retries: int | None
    name: str
    description: str
    prepare: ToolPrepareFunc[AgentDepsT] | None
    docstring_format: DocstringFormat
    require_parameter_descriptions: bool
    _is_async: bool = field(init=False)
    _single_arg_name: str | None = field(init=False)
    _positional_fields: list[str] = field(init=False)
    _var_positional_field: str | None = field(init=False)
    _validator: SchemaValidator = field(init=False, repr=False)
    _parameters_json_schema: ObjectJsonSchema = field(init=False)

    # TODO: Move this state off the Tool class, which is otherwise stateless.
    #   This should be tracked inside a specific agent run, not the tool.
    current_retry: int = field(default=0, init=False)

    def __init__(
        self,
        function: ToolFuncEither[AgentDepsT],
        *,
        takes_ctx: bool | None = None,
        max_retries: int | None = None,
        name: str | None = None,
        description: str | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ):
        """Create a new tool instance.

        Example usage:

        ```python {noqa="I001"}
        from pydantic_ai import Agent, RunContext, Tool

        async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
            return f'{ctx.deps} {x} {y}'

        agent = Agent('test', tools=[Tool(my_tool)])
        ```

        or with a custom prepare method:

        ```python {noqa="I001"}
        from typing import Union

        from pydantic_ai import Agent, RunContext, Tool
        from pydantic_ai.tools import ToolDefinition

        async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
            return f'{ctx.deps} {x} {y}'

        async def prep_my_tool(
            ctx: RunContext[int], tool_def: ToolDefinition
        ) -> Union[ToolDefinition, None]:
            # only register the tool if `deps == 42`
            if ctx.deps == 42:
                return tool_def

        agent = Agent('test', tools=[Tool(my_tool, prepare=prep_my_tool)])
        ```


        Args:
            function: The Python function to call as the tool.
            takes_ctx: Whether the function takes a [`RunContext`][pydantic_ai.tools.RunContext] first argument,
                this is inferred if unset.
            max_retries: Maximum number of retries allowed for this tool, set to the agent default if `None`.
            name: Name of the tool, inferred from the function if `None`.
            description: Description of the tool, inferred from the function if `None`.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
                Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
            require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
        """
        if takes_ctx is None:
            takes_ctx = _pydantic.takes_ctx(function)

        f = _pydantic.function_schema(function, takes_ctx, docstring_format, require_parameter_descriptions)
        self.function = function
        self.takes_ctx = takes_ctx
        self.max_retries = max_retries
        self.name = name or function.__name__
        self.description = description or f['description']
        self.prepare = prepare
        self.docstring_format = docstring_format
        self.require_parameter_descriptions = require_parameter_descriptions
        self._is_async = inspect.iscoroutinefunction(self.function)
        self._single_arg_name = f['single_arg_name']
        self._positional_fields = f['positional_fields']
        self._var_positional_field = f['var_positional_field']
        self._validator = f['validator']
        self._parameters_json_schema = f['json_schema']

    async def prepare_tool_def(self, ctx: RunContext[AgentDepsT]) -> ToolDefinition | None:
        """Get the tool definition.

        By default, this method creates a tool definition, then either returns it, or calls `self.prepare`
        if it's set.

        Returns:
            return a `ToolDefinition` or `None` if the tools should not be registered for this run.
        """
        tool_def = ToolDefinition(
            name=self.name,
            description=self.description,
            parameters_json_schema=self._parameters_json_schema,
        )
        if self.prepare is not None:
            return await self.prepare(ctx, tool_def)
        else:
            return tool_def

    async def run(
        self, message: _messages.ToolCallPart, run_context: RunContext[AgentDepsT]
    ) -> _messages.ToolReturnPart | _messages.RetryPromptPart:
        """Run the tool function asynchronously."""
        try:
            if isinstance(message.args, str):
                args_dict = self._validator.validate_json(message.args)
            else:
                args_dict = self._validator.validate_python(message.args)
        except ValidationError as e:
            return self._on_error(e, message)

        args, kwargs = self._call_args(args_dict, message, run_context)
        try:
            if self._is_async:
                function = cast(Callable[[Any], Awaitable[str]], self.function)
                response_content = await function(*args, **kwargs)
            else:
                function = cast(Callable[[Any], str], self.function)
                response_content = await _utils.run_in_executor(function, *args, **kwargs)
        except ModelRetry as e:
            return self._on_error(e, message)

        self.current_retry = 0
        return _messages.ToolReturnPart(
            tool_name=message.tool_name,
            content=response_content,
            tool_call_id=message.tool_call_id,
        )

    def _call_args(
        self,
        args_dict: dict[str, Any],
        message: _messages.ToolCallPart,
        run_context: RunContext[AgentDepsT],
    ) -> tuple[list[Any], dict[str, Any]]:
        if self._single_arg_name:
            args_dict = {self._single_arg_name: args_dict}

        ctx = dataclasses.replace(
            run_context,
            retry=self.current_retry,
            tool_name=message.tool_name,
            tool_call_id=message.tool_call_id,
        )
        args = [ctx] if self.takes_ctx else []
        for positional_field in self._positional_fields:
            args.append(args_dict.pop(positional_field))
        if self._var_positional_field:
            args.extend(args_dict.pop(self._var_positional_field))

        return args, args_dict

    def _on_error(
        self, exc: ValidationError | ModelRetry, call_message: _messages.ToolCallPart
    ) -> _messages.RetryPromptPart:
        self.current_retry += 1
        if self.max_retries is None or self.current_retry > self.max_retries:
            raise UnexpectedModelBehavior(f'Tool exceeded max retries count of {self.max_retries}') from exc
        else:
            if isinstance(exc, ValidationError):
                content = exc.errors(include_url=False)
            else:
                content = exc.message
            return _messages.RetryPromptPart(
                tool_name=call_message.tool_name,
                content=content,
                tool_call_id=call_message.tool_call_id,
            )
```

```
@dataclass(init=False)
class Tool(Generic[AgentDepsT]):
    """A tool function for an agent."""

    function: ToolFuncEither[AgentDepsT]
    takes_ctx: bool
    max_retries: int | None
    name: str
    description: str
    prepare: ToolPrepareFunc[AgentDepsT] | None
    docstring_format: DocstringFormat
    require_parameter_descriptions: bool
    _is_async: bool = field(init=False)
    _single_arg_name: str | None = field(init=False)
    _positional_fields: list[str] = field(init=False)
    _var_positional_field: str | None = field(init=False)
    _validator: SchemaValidator = field(init=False, repr=False)
    _parameters_json_schema: ObjectJsonSchema = field(init=False)

    # TODO: Move this state off the Tool class, which is otherwise stateless.
    #   This should be tracked inside a specific agent run, not the tool.
    current_retry: int = field(default=0, init=False)

    def __init__(
        self,
        function: ToolFuncEither[AgentDepsT],
        *,
        takes_ctx: bool | None = None,
        max_retries: int | None = None,
        name: str | None = None,
        description: str | None = None,
        prepare: ToolPrepareFunc[AgentDepsT] | None = None,
        docstring_format: DocstringFormat = 'auto',
        require_parameter_descriptions: bool = False,
    ):
        """Create a new tool instance.

        Example usage:

        ```python {noqa="I001"}
        from pydantic_ai import Agent, RunContext, Tool

        async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
            return f'{ctx.deps} {x} {y}'

        agent = Agent('test', tools=[Tool(my_tool)])
        ```

        or with a custom prepare method:

        ```python {noqa="I001"}
        from typing import Union

        from pydantic_ai import Agent, RunContext, Tool
        from pydantic_ai.tools import ToolDefinition

        async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
            return f'{ctx.deps} {x} {y}'

        async def prep_my_tool(
            ctx: RunContext[int], tool_def: ToolDefinition
        ) -> Union[ToolDefinition, None]:
            # only register the tool if `deps == 42`
            if ctx.deps == 42:
                return tool_def

        agent = Agent('test', tools=[Tool(my_tool, prepare=prep_my_tool)])
        ```


        Args:
            function: The Python function to call as the tool.
            takes_ctx: Whether the function takes a [`RunContext`][pydantic_ai.tools.RunContext] first argument,
                this is inferred if unset.
            max_retries: Maximum number of retries allowed for this tool, set to the agent default if `None`.
            name: Name of the tool, inferred from the function if `None`.
            description: Description of the tool, inferred from the function if `None`.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
                Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
            require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
        """
        if takes_ctx is None:
            takes_ctx = _pydantic.takes_ctx(function)

        f = _pydantic.function_schema(function, takes_ctx, docstring_format, require_parameter_descriptions)
        self.function = function
        self.takes_ctx = takes_ctx
        self.max_retries = max_retries
        self.name = name or function.__name__
        self.description = description or f['description']
        self.prepare = prepare
        self.docstring_format = docstring_format
        self.require_parameter_descriptions = require_parameter_descriptions
        self._is_async = inspect.iscoroutinefunction(self.function)
        self._single_arg_name = f['single_arg_name']
        self._positional_fields = f['positional_fields']
        self._var_positional_field = f['var_positional_field']
        self._validator = f['validator']
        self._parameters_json_schema = f['json_schema']

    async def prepare_tool_def(self, ctx: RunContext[AgentDepsT]) -> ToolDefinition | None:
        """Get the tool definition.

        By default, this method creates a tool definition, then either returns it, or calls `self.prepare`
        if it's set.

        Returns:
            return a `ToolDefinition` or `None` if the tools should not be registered for this run.
        """
        tool_def = ToolDefinition(
            name=self.name,
            description=self.description,
            parameters_json_schema=self._parameters_json_schema,
        )
        if self.prepare is not None:
            return await self.prepare(ctx, tool_def)
        else:
            return tool_def

    async def run(
        self, message: _messages.ToolCallPart, run_context: RunContext[AgentDepsT]
    ) -> _messages.ToolReturnPart | _messages.RetryPromptPart:
        """Run the tool function asynchronously."""
        try:
            if isinstance(message.args, str):
                args_dict = self._validator.validate_json(message.args)
            else:
                args_dict = self._validator.validate_python(message.args)
        except ValidationError as e:
            return self._on_error(e, message)

        args, kwargs = self._call_args(args_dict, message, run_context)
        try:
            if self._is_async:
                function = cast(Callable[[Any], Awaitable[str]], self.function)
                response_content = await function(*args, **kwargs)
            else:
                function = cast(Callable[[Any], str], self.function)
                response_content = await _utils.run_in_executor(function, *args, **kwargs)
        except ModelRetry as e:
            return self._on_error(e, message)

        self.current_retry = 0
        return _messages.ToolReturnPart(
            tool_name=message.tool_name,
            content=response_content,
            tool_call_id=message.tool_call_id,
        )

    def _call_args(
        self,
        args_dict: dict[str, Any],
        message: _messages.ToolCallPart,
        run_context: RunContext[AgentDepsT],
    ) -> tuple[list[Any], dict[str, Any]]:
        if self._single_arg_name:
            args_dict = {self._single_arg_name: args_dict}

        ctx = dataclasses.replace(
            run_context,
            retry=self.current_retry,
            tool_name=message.tool_name,
            tool_call_id=message.tool_call_id,
        )
        args = [ctx] if self.takes_ctx else []
        for positional_field in self._positional_fields:
            args.append(args_dict.pop(positional_field))
        if self._var_positional_field:
            args.extend(args_dict.pop(self._var_positional_field))

        return args, args_dict

    def _on_error(
        self, exc: ValidationError | ModelRetry, call_message: _messages.ToolCallPart
    ) -> _messages.RetryPromptPart:
        self.current_retry += 1
        if self.max_retries is None or self.current_retry > self.max_retries:
            raise UnexpectedModelBehavior(f'Tool exceeded max retries count of {self.max_retries}') from exc
        else:
            if isinstance(exc, ValidationError):
                content = exc.errors(include_url=False)
            else:
                content = exc.message
            return _messages.RetryPromptPart(
                tool_name=call_message.tool_name,
                content=content,
                tool_call_id=call_message.tool_call_id,
            )
```

#### __init__

```
__init__(
    function: ToolFuncEither[AgentDepsT],
    *,
    takes_ctx: bool | None = None,
    max_retries: int | None = None,
    name: str | None = None,
    description: str | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False
)
```

```
__init__(
    function: ToolFuncEither[AgentDepsT],
    *,
    takes_ctx: bool | None = None,
    max_retries: int | None = None,
    name: str | None = None,
    description: str | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = "auto",
    require_parameter_descriptions: bool = False
)
```

[ToolFuncEither](https://ai.pydantic.dev#pydantic_ai.tools.ToolFuncEither)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

[int](https://docs.python.org/3/library/functions.html#int)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[ToolPrepareFunc](https://ai.pydantic.dev#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[DocstringFormat](https://ai.pydantic.dev#pydantic_ai.tools.DocstringFormat)

[bool](https://docs.python.org/3/library/functions.html#bool)

Create a new tool instance.

Example usage:

```
from pydantic_ai import Agent, RunContext, Tool

async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
    return f'{ctx.deps} {x} {y}'

agent = Agent('test', tools=[Tool(my_tool)])
```

```
from pydantic_ai import Agent, RunContext, Tool

async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
    return f'{ctx.deps} {x} {y}'

agent = Agent('test', tools=[Tool(my_tool)])
```

or with a custom prepare method:

```
from typing import Union

from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.tools import ToolDefinition

async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
    return f'{ctx.deps} {x} {y}'

async def prep_my_tool(
    ctx: RunContext[int], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    # only register the tool if `deps == 42`
    if ctx.deps == 42:
        return tool_def

agent = Agent('test', tools=[Tool(my_tool, prepare=prep_my_tool)])
```

```
from typing import Union

from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.tools import ToolDefinition

async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
    return f'{ctx.deps} {x} {y}'

async def prep_my_tool(
    ctx: RunContext[int], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    # only register the tool if `deps == 42`
    if ctx.deps == 42:
        return tool_def

agent = Agent('test', tools=[Tool(my_tool, prepare=prep_my_tool)])
```

Parameters:

```
function
```

```
ToolFuncEither[AgentDepsT]
```

[ToolFuncEither](https://ai.pydantic.dev#pydantic_ai.tools.ToolFuncEither)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

The Python function to call as the tool.

```
takes_ctx
```

```
bool | None
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether the function takes a RunContext first argument,
this is inferred if unset.

```
RunContext
```

```
None
```

```
max_retries
```

```
int | None
```

[int](https://docs.python.org/3/library/functions.html#int)

Maximum number of retries allowed for this tool, set to the agent default if None.

```
None
```

```
None
```

```
name
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Name of the tool, inferred from the function if None.

```
None
```

```
None
```

```
description
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Description of the tool, inferred from the function if None.

```
None
```

```
None
```

```
prepare
```

```
ToolPrepareFunc[AgentDepsT] | None
```

[ToolPrepareFunc](https://ai.pydantic.dev#pydantic_ai.tools.ToolPrepareFunc)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

custom method to prepare the tool definition for each step, return None to omit this
tool from a given step. This is useful if you want to customise a tool at call time,
or omit it completely from a step. See ToolPrepareFunc.

```
None
```

```
ToolPrepareFunc
```

```
None
```

```
docstring_format
```

```
DocstringFormat
```

[DocstringFormat](https://ai.pydantic.dev#pydantic_ai.tools.DocstringFormat)

The format of the docstring, see DocstringFormat.
Defaults to 'auto', such that the format is inferred from the structure of the docstring.

```
DocstringFormat
```

```
'auto'
```

```
'auto'
```

```
require_parameter_descriptions
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

If True, raise an error if a parameter description is missing. Defaults to False.

```
False
```

```
pydantic_ai_slim/pydantic_ai/tools.py
```

```
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
```

```
def __init__(
    self,
    function: ToolFuncEither[AgentDepsT],
    *,
    takes_ctx: bool | None = None,
    max_retries: int | None = None,
    name: str | None = None,
    description: str | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = 'auto',
    require_parameter_descriptions: bool = False,
):
    """Create a new tool instance.

    Example usage:

    ```python {noqa="I001"}
    from pydantic_ai import Agent, RunContext, Tool

    async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
        return f'{ctx.deps} {x} {y}'

    agent = Agent('test', tools=[Tool(my_tool)])
    ```

    or with a custom prepare method:

    ```python {noqa="I001"}
    from typing import Union

    from pydantic_ai import Agent, RunContext, Tool
    from pydantic_ai.tools import ToolDefinition

    async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
        return f'{ctx.deps} {x} {y}'

    async def prep_my_tool(
        ctx: RunContext[int], tool_def: ToolDefinition
    ) -> Union[ToolDefinition, None]:
        # only register the tool if `deps == 42`
        if ctx.deps == 42:
            return tool_def

    agent = Agent('test', tools=[Tool(my_tool, prepare=prep_my_tool)])
    ```


    Args:
        function: The Python function to call as the tool.
        takes_ctx: Whether the function takes a [`RunContext`][pydantic_ai.tools.RunContext] first argument,
            this is inferred if unset.
        max_retries: Maximum number of retries allowed for this tool, set to the agent default if `None`.
        name: Name of the tool, inferred from the function if `None`.
        description: Description of the tool, inferred from the function if `None`.
        prepare: custom method to prepare the tool definition for each step, return `None` to omit this
            tool from a given step. This is useful if you want to customise a tool at call time,
            or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
            Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
        require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    """
    if takes_ctx is None:
        takes_ctx = _pydantic.takes_ctx(function)

    f = _pydantic.function_schema(function, takes_ctx, docstring_format, require_parameter_descriptions)
    self.function = function
    self.takes_ctx = takes_ctx
    self.max_retries = max_retries
    self.name = name or function.__name__
    self.description = description or f['description']
    self.prepare = prepare
    self.docstring_format = docstring_format
    self.require_parameter_descriptions = require_parameter_descriptions
    self._is_async = inspect.iscoroutinefunction(self.function)
    self._single_arg_name = f['single_arg_name']
    self._positional_fields = f['positional_fields']
    self._var_positional_field = f['var_positional_field']
    self._validator = f['validator']
    self._parameters_json_schema = f['json_schema']
```

```
def __init__(
    self,
    function: ToolFuncEither[AgentDepsT],
    *,
    takes_ctx: bool | None = None,
    max_retries: int | None = None,
    name: str | None = None,
    description: str | None = None,
    prepare: ToolPrepareFunc[AgentDepsT] | None = None,
    docstring_format: DocstringFormat = 'auto',
    require_parameter_descriptions: bool = False,
):
    """Create a new tool instance.

    Example usage:

    ```python {noqa="I001"}
    from pydantic_ai import Agent, RunContext, Tool

    async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
        return f'{ctx.deps} {x} {y}'

    agent = Agent('test', tools=[Tool(my_tool)])
    ```

    or with a custom prepare method:

    ```python {noqa="I001"}
    from typing import Union

    from pydantic_ai import Agent, RunContext, Tool
    from pydantic_ai.tools import ToolDefinition

    async def my_tool(ctx: RunContext[int], x: int, y: int) -> str:
        return f'{ctx.deps} {x} {y}'

    async def prep_my_tool(
        ctx: RunContext[int], tool_def: ToolDefinition
    ) -> Union[ToolDefinition, None]:
        # only register the tool if `deps == 42`
        if ctx.deps == 42:
            return tool_def

    agent = Agent('test', tools=[Tool(my_tool, prepare=prep_my_tool)])
    ```


    Args:
        function: The Python function to call as the tool.
        takes_ctx: Whether the function takes a [`RunContext`][pydantic_ai.tools.RunContext] first argument,
            this is inferred if unset.
        max_retries: Maximum number of retries allowed for this tool, set to the agent default if `None`.
        name: Name of the tool, inferred from the function if `None`.
        description: Description of the tool, inferred from the function if `None`.
        prepare: custom method to prepare the tool definition for each step, return `None` to omit this
            tool from a given step. This is useful if you want to customise a tool at call time,
            or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
            Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
        require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    """
    if takes_ctx is None:
        takes_ctx = _pydantic.takes_ctx(function)

    f = _pydantic.function_schema(function, takes_ctx, docstring_format, require_parameter_descriptions)
    self.function = function
    self.takes_ctx = takes_ctx
    self.max_retries = max_retries
    self.name = name or function.__name__
    self.description = description or f['description']
    self.prepare = prepare
    self.docstring_format = docstring_format
    self.require_parameter_descriptions = require_parameter_descriptions
    self._is_async = inspect.iscoroutinefunction(self.function)
    self._single_arg_name = f['single_arg_name']
    self._positional_fields = f['positional_fields']
    self._var_positional_field = f['var_positional_field']
    self._validator = f['validator']
    self._parameters_json_schema = f['json_schema']
```

#### prepare_tool_def

async

```
async
```

```
prepare_tool_def(
    ctx: RunContext[AgentDepsT],
) -> ToolDefinition | None
```

```
prepare_tool_def(
    ctx: RunContext[AgentDepsT],
) -> ToolDefinition | None
```

[RunContext](https://ai.pydantic.dev#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[ToolDefinition](https://ai.pydantic.dev#pydantic_ai.tools.ToolDefinition)

Get the tool definition.

By default, this method creates a tool definition, then either returns it, or calls self.prepare
if it's set.

```
self.prepare
```

Returns:

```
ToolDefinition | None
```

[ToolDefinition](https://ai.pydantic.dev#pydantic_ai.tools.ToolDefinition)

return a ToolDefinition or None if the tools should not be registered for this run.

```
ToolDefinition
```

```
None
```

```
pydantic_ai_slim/pydantic_ai/tools.py
```

```
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
```

```
async def prepare_tool_def(self, ctx: RunContext[AgentDepsT]) -> ToolDefinition | None:
    """Get the tool definition.

    By default, this method creates a tool definition, then either returns it, or calls `self.prepare`
    if it's set.

    Returns:
        return a `ToolDefinition` or `None` if the tools should not be registered for this run.
    """
    tool_def = ToolDefinition(
        name=self.name,
        description=self.description,
        parameters_json_schema=self._parameters_json_schema,
    )
    if self.prepare is not None:
        return await self.prepare(ctx, tool_def)
    else:
        return tool_def
```

```
async def prepare_tool_def(self, ctx: RunContext[AgentDepsT]) -> ToolDefinition | None:
    """Get the tool definition.

    By default, this method creates a tool definition, then either returns it, or calls `self.prepare`
    if it's set.

    Returns:
        return a `ToolDefinition` or `None` if the tools should not be registered for this run.
    """
    tool_def = ToolDefinition(
        name=self.name,
        description=self.description,
        parameters_json_schema=self._parameters_json_schema,
    )
    if self.prepare is not None:
        return await self.prepare(ctx, tool_def)
    else:
        return tool_def
```

#### run

async

```
async
```

```
run(
    message: ToolCallPart,
    run_context: RunContext[AgentDepsT],
) -> ToolReturnPart | RetryPromptPart
```

```
run(
    message: ToolCallPart,
    run_context: RunContext[AgentDepsT],
) -> ToolReturnPart | RetryPromptPart
```

[ToolCallPart](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ToolCallPart)

[RunContext](https://ai.pydantic.dev#pydantic_ai.tools.RunContext)

[AgentDepsT](https://ai.pydantic.dev#pydantic_ai.tools.AgentDepsT)

[ToolReturnPart](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ToolReturnPart)

[RetryPromptPart](https://ai.pydantic.dev/messages/#pydantic_ai.messages.RetryPromptPart)

Run the tool function asynchronously.

```
pydantic_ai_slim/pydantic_ai/tools.py
```

```
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
```

```
async def run(
    self, message: _messages.ToolCallPart, run_context: RunContext[AgentDepsT]
) -> _messages.ToolReturnPart | _messages.RetryPromptPart:
    """Run the tool function asynchronously."""
    try:
        if isinstance(message.args, str):
            args_dict = self._validator.validate_json(message.args)
        else:
            args_dict = self._validator.validate_python(message.args)
    except ValidationError as e:
        return self._on_error(e, message)

    args, kwargs = self._call_args(args_dict, message, run_context)
    try:
        if self._is_async:
            function = cast(Callable[[Any], Awaitable[str]], self.function)
            response_content = await function(*args, **kwargs)
        else:
            function = cast(Callable[[Any], str], self.function)
            response_content = await _utils.run_in_executor(function, *args, **kwargs)
    except ModelRetry as e:
        return self._on_error(e, message)

    self.current_retry = 0
    return _messages.ToolReturnPart(
        tool_name=message.tool_name,
        content=response_content,
        tool_call_id=message.tool_call_id,
    )
```

```
async def run(
    self, message: _messages.ToolCallPart, run_context: RunContext[AgentDepsT]
) -> _messages.ToolReturnPart | _messages.RetryPromptPart:
    """Run the tool function asynchronously."""
    try:
        if isinstance(message.args, str):
            args_dict = self._validator.validate_json(message.args)
        else:
            args_dict = self._validator.validate_python(message.args)
    except ValidationError as e:
        return self._on_error(e, message)

    args, kwargs = self._call_args(args_dict, message, run_context)
    try:
        if self._is_async:
            function = cast(Callable[[Any], Awaitable[str]], self.function)
            response_content = await function(*args, **kwargs)
        else:
            function = cast(Callable[[Any], str], self.function)
            response_content = await _utils.run_in_executor(function, *args, **kwargs)
    except ModelRetry as e:
        return self._on_error(e, message)

    self.current_retry = 0
    return _messages.ToolReturnPart(
        tool_name=message.tool_name,
        content=response_content,
        tool_call_id=message.tool_call_id,
    )
```

### ObjectJsonSchema

module-attribute

```
module-attribute
```

```
ObjectJsonSchema: TypeAlias = dict[str, Any]
```

```
ObjectJsonSchema: TypeAlias = dict[str, Any]
```

[TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias)

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

Type representing JSON schema of an object, e.g. where "type": "object".

```
"type": "object"
```

This type is used to define tools parameters (aka arguments) in ToolDefinition.

With PEP-728 this should be a TypedDict with type: Literal['object'], and extra_parts=Any

```
type: Literal['object']
```

```
extra_parts=Any
```

### ToolDefinition

dataclass

```
dataclass
```

Definition of a tool passed to a model.

This is used for both function tools result tools.

```
pydantic_ai_slim/pydantic_ai/tools.py
```

```
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
```

```
@dataclass
class ToolDefinition:
    """Definition of a tool passed to a model.

    This is used for both function tools result tools.
    """

    name: str
    """The name of the tool."""

    description: str
    """The description of the tool."""

    parameters_json_schema: ObjectJsonSchema
    """The JSON schema for the tool's parameters."""

    outer_typed_dict_key: str | None = None
    """The key in the outer [TypedDict] that wraps a result tool.

    This will only be set for result tools which don't have an `object` JSON schema.
    """
```

```
@dataclass
class ToolDefinition:
    """Definition of a tool passed to a model.

    This is used for both function tools result tools.
    """

    name: str
    """The name of the tool."""

    description: str
    """The description of the tool."""

    parameters_json_schema: ObjectJsonSchema
    """The JSON schema for the tool's parameters."""

    outer_typed_dict_key: str | None = None
    """The key in the outer [TypedDict] that wraps a result tool.

    This will only be set for result tools which don't have an `object` JSON schema.
    """
```

#### name

instance-attribute

```
instance-attribute
```

```
name: str
```

```
name: str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The name of the tool.

#### description

instance-attribute

```
instance-attribute
```

```
description: str
```

```
description: str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The description of the tool.

#### parameters_json_schema

instance-attribute

```
instance-attribute
```

```
parameters_json_schema: ObjectJsonSchema
```

```
parameters_json_schema: ObjectJsonSchema
```

[ObjectJsonSchema](https://ai.pydantic.dev#pydantic_ai.tools.ObjectJsonSchema)

The JSON schema for the tool's parameters.

#### outer_typed_dict_key

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
outer_typed_dict_key: str | None = None
```

```
outer_typed_dict_key: str | None = None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The key in the outer [TypedDict] that wraps a result tool.

This will only be set for result tools which don't have an object JSON schema.

```
object
```

