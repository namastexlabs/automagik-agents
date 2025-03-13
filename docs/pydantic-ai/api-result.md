# pydantic_ai.result

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.result

```
pydantic_ai.result
```

[](https://ai.pydantic.dev)

### ResultDataT

module-attribute

```
module-attribute
```

```
ResultDataT = TypeVar(
    "ResultDataT", default=str, covariant=True
)
```

```
ResultDataT = TypeVar(
    "ResultDataT", default=str, covariant=True
)
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Covariant type variable for the result data type of a run.

### StreamedRunResult

dataclass

```
dataclass
```

Bases: Generic[AgentDepsT, ResultDataT]

```
Generic[AgentDepsT, ResultDataT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[AgentDepsT](https://ai.pydantic.dev/tools/#pydantic_ai.tools.AgentDepsT)

[ResultDataT](https://ai.pydantic.dev#pydantic_ai.result.ResultDataT)

Result of a streamed run that returns structured data via a tool call.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
```

```
@dataclass
class StreamedRunResult(Generic[AgentDepsT, ResultDataT]):
    """Result of a streamed run that returns structured data via a tool call."""

    _all_messages: list[_messages.ModelMessage]
    _new_message_index: int

    _usage_limits: UsageLimits | None
    _stream_response: models.StreamedResponse
    _result_schema: _result.ResultSchema[ResultDataT] | None
    _run_ctx: RunContext[AgentDepsT]
    _result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]]
    _result_tool_name: str | None
    _on_complete: Callable[[], Awaitable[None]]

    _initial_run_ctx_usage: Usage = field(init=False)
    is_complete: bool = field(default=False, init=False)
    """Whether the stream has all been received.

    This is set to `True` when one of
    [`stream`][pydantic_ai.result.StreamedRunResult.stream],
    [`stream_text`][pydantic_ai.result.StreamedRunResult.stream_text],
    [`stream_structured`][pydantic_ai.result.StreamedRunResult.stream_structured] or
    [`get_data`][pydantic_ai.result.StreamedRunResult.get_data] completes.
    """

    def __post_init__(self):
        self._initial_run_ctx_usage = copy(self._run_ctx.usage)

    def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return the history of _messages.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of messages.
        """
        # this is a method to be consistent with the other methods
        if result_tool_return_content is not None:
            raise NotImplementedError('Setting result tool return content is not supported for this result type.')
        return self._all_messages

    def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return all messages from [`all_messages`][pydantic_ai.result.StreamedRunResult.all_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.all_messages(result_tool_return_content=result_tool_return_content)
        )

    def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return new messages associated with this run.

        Messages from older runs are excluded.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of new messages.
        """
        return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]

    def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return new messages from [`new_messages`][pydantic_ai.result.StreamedRunResult.new_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the new messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.new_messages(result_tool_return_content=result_tool_return_content)
        )

    async def stream(self, *, debounce_by: float | None = 0.1) -> AsyncIterator[ResultDataT]:
        """Stream the response as an async iterable.

        The pydantic validator for structured data will be called in
        [partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
        on each iteration.

        Args:
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.

        Returns:
            An async iterable of the response data.
        """
        async for structured_message, is_last in self.stream_structured(debounce_by=debounce_by):
            result = await self.validate_structured_result(structured_message, allow_partial=not is_last)
            yield result

    async def stream_text(self, *, delta: bool = False, debounce_by: float | None = 0.1) -> AsyncIterator[str]:
        """Stream the text result as an async iterable.

        !!! note
            Result validators will NOT be called on the text result if `delta=True`.

        Args:
            delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
                up to the current point.
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.
        """
        if self._result_schema and not self._result_schema.allow_text_result:
            raise exceptions.UserError('stream_text() can only be used with text responses')

        if delta:
            async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
                yield text
        else:
            async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
                combined_validated_text = await self._validate_text_result(text)
                yield combined_validated_text
        await self._marked_completed(self._stream_response.get())

    async def stream_structured(
        self, *, debounce_by: float | None = 0.1
    ) -> AsyncIterator[tuple[_messages.ModelResponse, bool]]:
        """Stream the response as an async iterable of Structured LLM Messages.

        Args:
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.

        Returns:
            An async iterable of the structured response message and whether that is the last message.
        """
        # if the message currently has any parts with content, yield before streaming
        msg = self._stream_response.get()
        for part in msg.parts:
            if part.has_content():
                yield msg, False
                break

        async for msg in self._stream_response_structured(debounce_by=debounce_by):
            yield msg, False

        msg = self._stream_response.get()
        yield msg, True

        await self._marked_completed(msg)

    async def get_data(self) -> ResultDataT:
        """Stream the whole response, validate and return it."""
        usage_checking_stream = _get_usage_checking_stream_response(
            self._stream_response, self._usage_limits, self.usage
        )

        async for _ in usage_checking_stream:
            pass
        message = self._stream_response.get()
        await self._marked_completed(message)
        return await self.validate_structured_result(message)

    def usage(self) -> Usage:
        """Return the usage of the whole run.

        !!! note
            This won't return the full usage until the stream is finished.
        """
        return self._initial_run_ctx_usage + self._stream_response.usage()

    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._stream_response.timestamp

    async def validate_structured_result(
        self, message: _messages.ModelResponse, *, allow_partial: bool = False
    ) -> ResultDataT:
        """Validate a structured result message."""
        if self._result_schema is not None and self._result_tool_name is not None:
            match = self._result_schema.find_named_tool(message.parts, self._result_tool_name)
            if match is None:
                raise exceptions.UnexpectedModelBehavior(
                    f'Invalid response, unable to find tool: {self._result_schema.tool_names()}'
                )

            call, result_tool = match
            result_data = result_tool.validate(call, allow_partial=allow_partial, wrap_validation_errors=False)

            for validator in self._result_validators:
                result_data = await validator.validate(result_data, call, self._run_ctx)
            return result_data
        else:
            text = '\n\n'.join(x.content for x in message.parts if isinstance(x, _messages.TextPart))
            for validator in self._result_validators:
                text = await validator.validate(
                    text,
                    None,
                    self._run_ctx,
                )
            # Since there is no result tool, we can assume that str is compatible with ResultDataT
            return cast(ResultDataT, text)

    async def _validate_text_result(self, text: str) -> str:
        for validator in self._result_validators:
            text = await validator.validate(
                text,
                None,
                self._run_ctx,
            )
        return text

    async def _marked_completed(self, message: _messages.ModelResponse) -> None:
        self.is_complete = True
        self._all_messages.append(message)
        await self._on_complete()

    async def _stream_response_structured(
        self, *, debounce_by: float | None = 0.1
    ) -> AsyncIterator[_messages.ModelResponse]:
        async with _utils.group_by_temporal(self._stream_response, debounce_by) as group_iter:
            async for _items in group_iter:
                yield self._stream_response.get()

    async def _stream_response_text(
        self, *, delta: bool = False, debounce_by: float | None = 0.1
    ) -> AsyncIterator[str]:
        """Stream the response as an async iterable of text."""

        # Define a "merged" version of the iterator that will yield items that have already been retrieved
        # and items that we receive while streaming. We define a dedicated async iterator for this so we can
        # pass the combined stream to the group_by_temporal function within `_stream_text_deltas` below.
        async def _stream_text_deltas_ungrouped() -> AsyncIterator[tuple[str, int]]:
            # yields tuples of (text_content, part_index)
            # we don't currently make use of the part_index, but in principle this may be useful
            # so we retain it here for now to make possible future refactors simpler
            msg = self._stream_response.get()
            for i, part in enumerate(msg.parts):
                if isinstance(part, _messages.TextPart) and part.content:
                    yield part.content, i

            async for event in self._stream_response:
                if (
                    isinstance(event, _messages.PartStartEvent)
                    and isinstance(event.part, _messages.TextPart)
                    and event.part.content
                ):
                    yield event.part.content, event.index
                elif (
                    isinstance(event, _messages.PartDeltaEvent)
                    and isinstance(event.delta, _messages.TextPartDelta)
                    and event.delta.content_delta
                ):
                    yield event.delta.content_delta, event.index

        async def _stream_text_deltas() -> AsyncIterator[str]:
            async with _utils.group_by_temporal(_stream_text_deltas_ungrouped(), debounce_by) as group_iter:
                async for items in group_iter:
                    # Note: we are currently just dropping the part index on the group here
                    yield ''.join([content for content, _ in items])

        if delta:
            async for text in _stream_text_deltas():
                yield text
        else:
            # a quick benchmark shows it's faster to build up a string with concat when we're
            # yielding at each step
            deltas: list[str] = []
            async for text in _stream_text_deltas():
                deltas.append(text)
                yield ''.join(deltas)
```

```
@dataclass
class StreamedRunResult(Generic[AgentDepsT, ResultDataT]):
    """Result of a streamed run that returns structured data via a tool call."""

    _all_messages: list[_messages.ModelMessage]
    _new_message_index: int

    _usage_limits: UsageLimits | None
    _stream_response: models.StreamedResponse
    _result_schema: _result.ResultSchema[ResultDataT] | None
    _run_ctx: RunContext[AgentDepsT]
    _result_validators: list[_result.ResultValidator[AgentDepsT, ResultDataT]]
    _result_tool_name: str | None
    _on_complete: Callable[[], Awaitable[None]]

    _initial_run_ctx_usage: Usage = field(init=False)
    is_complete: bool = field(default=False, init=False)
    """Whether the stream has all been received.

    This is set to `True` when one of
    [`stream`][pydantic_ai.result.StreamedRunResult.stream],
    [`stream_text`][pydantic_ai.result.StreamedRunResult.stream_text],
    [`stream_structured`][pydantic_ai.result.StreamedRunResult.stream_structured] or
    [`get_data`][pydantic_ai.result.StreamedRunResult.get_data] completes.
    """

    def __post_init__(self):
        self._initial_run_ctx_usage = copy(self._run_ctx.usage)

    def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return the history of _messages.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of messages.
        """
        # this is a method to be consistent with the other methods
        if result_tool_return_content is not None:
            raise NotImplementedError('Setting result tool return content is not supported for this result type.')
        return self._all_messages

    def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return all messages from [`all_messages`][pydantic_ai.result.StreamedRunResult.all_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.all_messages(result_tool_return_content=result_tool_return_content)
        )

    def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
        """Return new messages associated with this run.

        Messages from older runs are excluded.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            List of new messages.
        """
        return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]

    def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
        """Return new messages from [`new_messages`][pydantic_ai.result.StreamedRunResult.new_messages] as JSON bytes.

        Args:
            result_tool_return_content: The return content of the tool call to set in the last message.
                This provides a convenient way to modify the content of the result tool call if you want to continue
                the conversation and want to set the response to the result tool call. If `None`, the last message will
                not be modified.

        Returns:
            JSON bytes representing the new messages.
        """
        return _messages.ModelMessagesTypeAdapter.dump_json(
            self.new_messages(result_tool_return_content=result_tool_return_content)
        )

    async def stream(self, *, debounce_by: float | None = 0.1) -> AsyncIterator[ResultDataT]:
        """Stream the response as an async iterable.

        The pydantic validator for structured data will be called in
        [partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
        on each iteration.

        Args:
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.

        Returns:
            An async iterable of the response data.
        """
        async for structured_message, is_last in self.stream_structured(debounce_by=debounce_by):
            result = await self.validate_structured_result(structured_message, allow_partial=not is_last)
            yield result

    async def stream_text(self, *, delta: bool = False, debounce_by: float | None = 0.1) -> AsyncIterator[str]:
        """Stream the text result as an async iterable.

        !!! note
            Result validators will NOT be called on the text result if `delta=True`.

        Args:
            delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
                up to the current point.
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.
        """
        if self._result_schema and not self._result_schema.allow_text_result:
            raise exceptions.UserError('stream_text() can only be used with text responses')

        if delta:
            async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
                yield text
        else:
            async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
                combined_validated_text = await self._validate_text_result(text)
                yield combined_validated_text
        await self._marked_completed(self._stream_response.get())

    async def stream_structured(
        self, *, debounce_by: float | None = 0.1
    ) -> AsyncIterator[tuple[_messages.ModelResponse, bool]]:
        """Stream the response as an async iterable of Structured LLM Messages.

        Args:
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.

        Returns:
            An async iterable of the structured response message and whether that is the last message.
        """
        # if the message currently has any parts with content, yield before streaming
        msg = self._stream_response.get()
        for part in msg.parts:
            if part.has_content():
                yield msg, False
                break

        async for msg in self._stream_response_structured(debounce_by=debounce_by):
            yield msg, False

        msg = self._stream_response.get()
        yield msg, True

        await self._marked_completed(msg)

    async def get_data(self) -> ResultDataT:
        """Stream the whole response, validate and return it."""
        usage_checking_stream = _get_usage_checking_stream_response(
            self._stream_response, self._usage_limits, self.usage
        )

        async for _ in usage_checking_stream:
            pass
        message = self._stream_response.get()
        await self._marked_completed(message)
        return await self.validate_structured_result(message)

    def usage(self) -> Usage:
        """Return the usage of the whole run.

        !!! note
            This won't return the full usage until the stream is finished.
        """
        return self._initial_run_ctx_usage + self._stream_response.usage()

    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._stream_response.timestamp

    async def validate_structured_result(
        self, message: _messages.ModelResponse, *, allow_partial: bool = False
    ) -> ResultDataT:
        """Validate a structured result message."""
        if self._result_schema is not None and self._result_tool_name is not None:
            match = self._result_schema.find_named_tool(message.parts, self._result_tool_name)
            if match is None:
                raise exceptions.UnexpectedModelBehavior(
                    f'Invalid response, unable to find tool: {self._result_schema.tool_names()}'
                )

            call, result_tool = match
            result_data = result_tool.validate(call, allow_partial=allow_partial, wrap_validation_errors=False)

            for validator in self._result_validators:
                result_data = await validator.validate(result_data, call, self._run_ctx)
            return result_data
        else:
            text = '\n\n'.join(x.content for x in message.parts if isinstance(x, _messages.TextPart))
            for validator in self._result_validators:
                text = await validator.validate(
                    text,
                    None,
                    self._run_ctx,
                )
            # Since there is no result tool, we can assume that str is compatible with ResultDataT
            return cast(ResultDataT, text)

    async def _validate_text_result(self, text: str) -> str:
        for validator in self._result_validators:
            text = await validator.validate(
                text,
                None,
                self._run_ctx,
            )
        return text

    async def _marked_completed(self, message: _messages.ModelResponse) -> None:
        self.is_complete = True
        self._all_messages.append(message)
        await self._on_complete()

    async def _stream_response_structured(
        self, *, debounce_by: float | None = 0.1
    ) -> AsyncIterator[_messages.ModelResponse]:
        async with _utils.group_by_temporal(self._stream_response, debounce_by) as group_iter:
            async for _items in group_iter:
                yield self._stream_response.get()

    async def _stream_response_text(
        self, *, delta: bool = False, debounce_by: float | None = 0.1
    ) -> AsyncIterator[str]:
        """Stream the response as an async iterable of text."""

        # Define a "merged" version of the iterator that will yield items that have already been retrieved
        # and items that we receive while streaming. We define a dedicated async iterator for this so we can
        # pass the combined stream to the group_by_temporal function within `_stream_text_deltas` below.
        async def _stream_text_deltas_ungrouped() -> AsyncIterator[tuple[str, int]]:
            # yields tuples of (text_content, part_index)
            # we don't currently make use of the part_index, but in principle this may be useful
            # so we retain it here for now to make possible future refactors simpler
            msg = self._stream_response.get()
            for i, part in enumerate(msg.parts):
                if isinstance(part, _messages.TextPart) and part.content:
                    yield part.content, i

            async for event in self._stream_response:
                if (
                    isinstance(event, _messages.PartStartEvent)
                    and isinstance(event.part, _messages.TextPart)
                    and event.part.content
                ):
                    yield event.part.content, event.index
                elif (
                    isinstance(event, _messages.PartDeltaEvent)
                    and isinstance(event.delta, _messages.TextPartDelta)
                    and event.delta.content_delta
                ):
                    yield event.delta.content_delta, event.index

        async def _stream_text_deltas() -> AsyncIterator[str]:
            async with _utils.group_by_temporal(_stream_text_deltas_ungrouped(), debounce_by) as group_iter:
                async for items in group_iter:
                    # Note: we are currently just dropping the part index on the group here
                    yield ''.join([content for content, _ in items])

        if delta:
            async for text in _stream_text_deltas():
                yield text
        else:
            # a quick benchmark shows it's faster to build up a string with concat when we're
            # yielding at each step
            deltas: list[str] = []
            async for text in _stream_text_deltas():
                deltas.append(text)
                yield ''.join(deltas)
```

#### is_complete

class-attribute
instance-attribute

```
class-attribute
```

```
instance-attribute
```

```
is_complete: bool = field(default=False, init=False)
```

```
is_complete: bool = field(default=False, init=False)
```

[bool](https://docs.python.org/3/library/functions.html#bool)

[field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field)

Whether the stream has all been received.

This is set to True when one of
stream,
stream_text,
stream_structured or
get_data completes.

```
True
```

```
stream
```

```
stream_text
```

```
stream_structured
```

```
get_data
```

#### all_messages

```
all_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

```
all_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

Return the history of _messages.

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
list[ModelMessage]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

List of messages.

```
pydantic_ai_slim/pydantic_ai/result.py
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
```

```
def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return the history of _messages.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of messages.
    """
    # this is a method to be consistent with the other methods
    if result_tool_return_content is not None:
        raise NotImplementedError('Setting result tool return content is not supported for this result type.')
    return self._all_messages
```

```
def all_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return the history of _messages.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of messages.
    """
    # this is a method to be consistent with the other methods
    if result_tool_return_content is not None:
        raise NotImplementedError('Setting result tool return content is not supported for this result type.')
    return self._all_messages
```

#### all_messages_json

```
all_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

```
all_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

Return all messages from all_messages as JSON bytes.

```
all_messages
```

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
bytes
```

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

JSON bytes representing the messages.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
```

```
def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return all messages from [`all_messages`][pydantic_ai.result.StreamedRunResult.all_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.all_messages(result_tool_return_content=result_tool_return_content)
    )
```

```
def all_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return all messages from [`all_messages`][pydantic_ai.result.StreamedRunResult.all_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.all_messages(result_tool_return_content=result_tool_return_content)
    )
```

#### new_messages

```
new_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

```
new_messages(
    *, result_tool_return_content: str | None = None
) -> list[ModelMessage]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

Return new messages associated with this run.

Messages from older runs are excluded.

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
list[ModelMessage]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[ModelMessage](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelMessage)

List of new messages.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
```

```
def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return new messages associated with this run.

    Messages from older runs are excluded.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of new messages.
    """
    return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]
```

```
def new_messages(self, *, result_tool_return_content: str | None = None) -> list[_messages.ModelMessage]:
    """Return new messages associated with this run.

    Messages from older runs are excluded.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        List of new messages.
    """
    return self.all_messages(result_tool_return_content=result_tool_return_content)[self._new_message_index :]
```

#### new_messages_json

```
new_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

```
new_messages_json(
    *, result_tool_return_content: str | None = None
) -> bytes
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

Return new messages from new_messages as JSON bytes.

```
new_messages
```

Parameters:

```
result_tool_return_content
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The return content of the tool call to set in the last message.
This provides a convenient way to modify the content of the result tool call if you want to continue
the conversation and want to set the response to the result tool call. If None, the last message will
not be modified.

```
None
```

```
None
```

Returns:

```
bytes
```

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

JSON bytes representing the new messages.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return new messages from [`new_messages`][pydantic_ai.result.StreamedRunResult.new_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the new messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.new_messages(result_tool_return_content=result_tool_return_content)
    )
```

```
def new_messages_json(self, *, result_tool_return_content: str | None = None) -> bytes:
    """Return new messages from [`new_messages`][pydantic_ai.result.StreamedRunResult.new_messages] as JSON bytes.

    Args:
        result_tool_return_content: The return content of the tool call to set in the last message.
            This provides a convenient way to modify the content of the result tool call if you want to continue
            the conversation and want to set the response to the result tool call. If `None`, the last message will
            not be modified.

    Returns:
        JSON bytes representing the new messages.
    """
    return _messages.ModelMessagesTypeAdapter.dump_json(
        self.new_messages(result_tool_return_content=result_tool_return_content)
    )
```

#### stream

async

```
async
```

```
stream(
    *, debounce_by: float | None = 0.1
) -> AsyncIterator[ResultDataT]
```

```
stream(
    *, debounce_by: float | None = 0.1
) -> AsyncIterator[ResultDataT]
```

[float](https://docs.python.org/3/library/functions.html#float)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[ResultDataT](https://ai.pydantic.dev#pydantic_ai.result.ResultDataT)

Stream the response as an async iterable.

The pydantic validator for structured data will be called in
partial mode
on each iteration.

Parameters:

```
debounce_by
```

```
float | None
```

[float](https://docs.python.org/3/library/functions.html#float)

by how much (if at all) to debounce/group the response chunks by. None means no debouncing.
Debouncing is particularly important for long structured responses to reduce the overhead of
performing validation as each token is received.

```
None
```

```
0.1
```

Returns:

```
AsyncIterator[ResultDataT]
```

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[ResultDataT](https://ai.pydantic.dev#pydantic_ai.result.ResultDataT)

An async iterable of the response data.

```
pydantic_ai_slim/pydantic_ai/result.py
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
```

```
async def stream(self, *, debounce_by: float | None = 0.1) -> AsyncIterator[ResultDataT]:
    """Stream the response as an async iterable.

    The pydantic validator for structured data will be called in
    [partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
    on each iteration.

    Args:
        debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
            Debouncing is particularly important for long structured responses to reduce the overhead of
            performing validation as each token is received.

    Returns:
        An async iterable of the response data.
    """
    async for structured_message, is_last in self.stream_structured(debounce_by=debounce_by):
        result = await self.validate_structured_result(structured_message, allow_partial=not is_last)
        yield result
```

```
async def stream(self, *, debounce_by: float | None = 0.1) -> AsyncIterator[ResultDataT]:
    """Stream the response as an async iterable.

    The pydantic validator for structured data will be called in
    [partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
    on each iteration.

    Args:
        debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
            Debouncing is particularly important for long structured responses to reduce the overhead of
            performing validation as each token is received.

    Returns:
        An async iterable of the response data.
    """
    async for structured_message, is_last in self.stream_structured(debounce_by=debounce_by):
        result = await self.validate_structured_result(structured_message, allow_partial=not is_last)
        yield result
```

#### stream_text

async

```
async
```

```
stream_text(
    *, delta: bool = False, debounce_by: float | None = 0.1
) -> AsyncIterator[str]
```

```
stream_text(
    *, delta: bool = False, debounce_by: float | None = 0.1
) -> AsyncIterator[str]
```

[bool](https://docs.python.org/3/library/functions.html#bool)

[float](https://docs.python.org/3/library/functions.html#float)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Stream the text result as an async iterable.

Note

Result validators will NOT be called on the text result if delta=True.

```
delta=True
```

Parameters:

```
delta
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

if True, yield each chunk of text as it is received, if False (default), yield the full text
up to the current point.

```
True
```

```
False
```

```
False
```

```
debounce_by
```

```
float | None
```

[float](https://docs.python.org/3/library/functions.html#float)

by how much (if at all) to debounce/group the response chunks by. None means no debouncing.
Debouncing is particularly important for long structured responses to reduce the overhead of
performing validation as each token is received.

```
None
```

```
0.1
```

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
```

```
async def stream_text(self, *, delta: bool = False, debounce_by: float | None = 0.1) -> AsyncIterator[str]:
    """Stream the text result as an async iterable.

    !!! note
        Result validators will NOT be called on the text result if `delta=True`.

    Args:
        delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
            up to the current point.
        debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
            Debouncing is particularly important for long structured responses to reduce the overhead of
            performing validation as each token is received.
    """
    if self._result_schema and not self._result_schema.allow_text_result:
        raise exceptions.UserError('stream_text() can only be used with text responses')

    if delta:
        async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
            yield text
    else:
        async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
            combined_validated_text = await self._validate_text_result(text)
            yield combined_validated_text
    await self._marked_completed(self._stream_response.get())
```

```
async def stream_text(self, *, delta: bool = False, debounce_by: float | None = 0.1) -> AsyncIterator[str]:
    """Stream the text result as an async iterable.

    !!! note
        Result validators will NOT be called on the text result if `delta=True`.

    Args:
        delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
            up to the current point.
        debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
            Debouncing is particularly important for long structured responses to reduce the overhead of
            performing validation as each token is received.
    """
    if self._result_schema and not self._result_schema.allow_text_result:
        raise exceptions.UserError('stream_text() can only be used with text responses')

    if delta:
        async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
            yield text
    else:
        async for text in self._stream_response_text(delta=delta, debounce_by=debounce_by):
            combined_validated_text = await self._validate_text_result(text)
            yield combined_validated_text
    await self._marked_completed(self._stream_response.get())
```

#### stream_structured

async

```
async
```

```
stream_structured(
    *, debounce_by: float | None = 0.1
) -> AsyncIterator[tuple[ModelResponse, bool]]
```

```
stream_structured(
    *, debounce_by: float | None = 0.1
) -> AsyncIterator[tuple[ModelResponse, bool]]
```

[float](https://docs.python.org/3/library/functions.html#float)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

[ModelResponse](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelResponse)

[bool](https://docs.python.org/3/library/functions.html#bool)

Stream the response as an async iterable of Structured LLM Messages.

Parameters:

```
debounce_by
```

```
float | None
```

[float](https://docs.python.org/3/library/functions.html#float)

by how much (if at all) to debounce/group the response chunks by. None means no debouncing.
Debouncing is particularly important for long structured responses to reduce the overhead of
performing validation as each token is received.

```
None
```

```
0.1
```

Returns:

```
AsyncIterator[tuple[ModelResponse, bool]]
```

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

[ModelResponse](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelResponse)

[bool](https://docs.python.org/3/library/functions.html#bool)

An async iterable of the structured response message and whether that is the last message.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
```

```
async def stream_structured(
    self, *, debounce_by: float | None = 0.1
) -> AsyncIterator[tuple[_messages.ModelResponse, bool]]:
    """Stream the response as an async iterable of Structured LLM Messages.

    Args:
        debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
            Debouncing is particularly important for long structured responses to reduce the overhead of
            performing validation as each token is received.

    Returns:
        An async iterable of the structured response message and whether that is the last message.
    """
    # if the message currently has any parts with content, yield before streaming
    msg = self._stream_response.get()
    for part in msg.parts:
        if part.has_content():
            yield msg, False
            break

    async for msg in self._stream_response_structured(debounce_by=debounce_by):
        yield msg, False

    msg = self._stream_response.get()
    yield msg, True

    await self._marked_completed(msg)
```

```
async def stream_structured(
    self, *, debounce_by: float | None = 0.1
) -> AsyncIterator[tuple[_messages.ModelResponse, bool]]:
    """Stream the response as an async iterable of Structured LLM Messages.

    Args:
        debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
            Debouncing is particularly important for long structured responses to reduce the overhead of
            performing validation as each token is received.

    Returns:
        An async iterable of the structured response message and whether that is the last message.
    """
    # if the message currently has any parts with content, yield before streaming
    msg = self._stream_response.get()
    for part in msg.parts:
        if part.has_content():
            yield msg, False
            break

    async for msg in self._stream_response_structured(debounce_by=debounce_by):
        yield msg, False

    msg = self._stream_response.get()
    yield msg, True

    await self._marked_completed(msg)
```

#### get_data

async

```
async
```

```
get_data() -> ResultDataT
```

```
get_data() -> ResultDataT
```

[ResultDataT](https://ai.pydantic.dev#pydantic_ai.result.ResultDataT)

Stream the whole response, validate and return it.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
```

```
async def get_data(self) -> ResultDataT:
    """Stream the whole response, validate and return it."""
    usage_checking_stream = _get_usage_checking_stream_response(
        self._stream_response, self._usage_limits, self.usage
    )

    async for _ in usage_checking_stream:
        pass
    message = self._stream_response.get()
    await self._marked_completed(message)
    return await self.validate_structured_result(message)
```

```
async def get_data(self) -> ResultDataT:
    """Stream the whole response, validate and return it."""
    usage_checking_stream = _get_usage_checking_stream_response(
        self._stream_response, self._usage_limits, self.usage
    )

    async for _ in usage_checking_stream:
        pass
    message = self._stream_response.get()
    await self._marked_completed(message)
    return await self.validate_structured_result(message)
```

#### usage

```
usage() -> Usage
```

```
usage() -> Usage
```

[Usage](https://ai.pydantic.dev/usage/#pydantic_ai.usage.Usage)

Return the usage of the whole run.

Note

This won't return the full usage until the stream is finished.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
351
352
353
354
355
356
357
```

```
def usage(self) -> Usage:
    """Return the usage of the whole run.

    !!! note
        This won't return the full usage until the stream is finished.
    """
    return self._initial_run_ctx_usage + self._stream_response.usage()
```

```
def usage(self) -> Usage:
    """Return the usage of the whole run.

    !!! note
        This won't return the full usage until the stream is finished.
    """
    return self._initial_run_ctx_usage + self._stream_response.usage()
```

#### timestamp

```
timestamp() -> datetime
```

```
timestamp() -> datetime
```

[datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime)

Get the timestamp of the response.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
359
360
361
```

```
def timestamp(self) -> datetime:
    """Get the timestamp of the response."""
    return self._stream_response.timestamp
```

```
def timestamp(self) -> datetime:
    """Get the timestamp of the response."""
    return self._stream_response.timestamp
```

#### validate_structured_result

async

```
async
```

```
validate_structured_result(
    message: ModelResponse, *, allow_partial: bool = False
) -> ResultDataT
```

```
validate_structured_result(
    message: ModelResponse, *, allow_partial: bool = False
) -> ResultDataT
```

[ModelResponse](https://ai.pydantic.dev/messages/#pydantic_ai.messages.ModelResponse)

[bool](https://docs.python.org/3/library/functions.html#bool)

[ResultDataT](https://ai.pydantic.dev#pydantic_ai.result.ResultDataT)

Validate a structured result message.

```
pydantic_ai_slim/pydantic_ai/result.py
```

```
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
```

```
async def validate_structured_result(
    self, message: _messages.ModelResponse, *, allow_partial: bool = False
) -> ResultDataT:
    """Validate a structured result message."""
    if self._result_schema is not None and self._result_tool_name is not None:
        match = self._result_schema.find_named_tool(message.parts, self._result_tool_name)
        if match is None:
            raise exceptions.UnexpectedModelBehavior(
                f'Invalid response, unable to find tool: {self._result_schema.tool_names()}'
            )

        call, result_tool = match
        result_data = result_tool.validate(call, allow_partial=allow_partial, wrap_validation_errors=False)

        for validator in self._result_validators:
            result_data = await validator.validate(result_data, call, self._run_ctx)
        return result_data
    else:
        text = '\n\n'.join(x.content for x in message.parts if isinstance(x, _messages.TextPart))
        for validator in self._result_validators:
            text = await validator.validate(
                text,
                None,
                self._run_ctx,
            )
        # Since there is no result tool, we can assume that str is compatible with ResultDataT
        return cast(ResultDataT, text)
```

```
async def validate_structured_result(
    self, message: _messages.ModelResponse, *, allow_partial: bool = False
) -> ResultDataT:
    """Validate a structured result message."""
    if self._result_schema is not None and self._result_tool_name is not None:
        match = self._result_schema.find_named_tool(message.parts, self._result_tool_name)
        if match is None:
            raise exceptions.UnexpectedModelBehavior(
                f'Invalid response, unable to find tool: {self._result_schema.tool_names()}'
            )

        call, result_tool = match
        result_data = result_tool.validate(call, allow_partial=allow_partial, wrap_validation_errors=False)

        for validator in self._result_validators:
            result_data = await validator.validate(result_data, call, self._run_ctx)
        return result_data
    else:
        text = '\n\n'.join(x.content for x in message.parts if isinstance(x, _messages.TextPart))
        for validator in self._result_validators:
            text = await validator.validate(
                text,
                None,
                self._run_ctx,
            )
        # Since there is no result tool, we can assume that str is compatible with ResultDataT
        return cast(ResultDataT, text)
```

