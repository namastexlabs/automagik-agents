# pydantic_graph

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_graph

```
pydantic_graph
```

[](https://ai.pydantic.dev)

### Graph

dataclass

```
dataclass
```

Bases: Generic[StateT, DepsT, RunEndT]

```
Generic[StateT, DepsT, RunEndT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

Definition of a graph.

In pydantic-graph, a graph is a collection of nodes that can be run in sequence. The nodes define
their outgoing edges â e.g. which nodes may be run next, and thereby the structure of the graph.

```
pydantic-graph
```

Here's a very simple example of a graph which increments a number by 1, but makes sure the number is never
42 at the end.

never_42.pyfrom __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext

@dataclass
class MyState:
    number: int

@dataclass
class Increment(BaseNode[MyState]):
    async def run(self, ctx: GraphRunContext) -> Check42:
        ctx.state.number += 1
        return Check42()

@dataclass
class Check42(BaseNode[MyState, None, int]):
    async def run(self, ctx: GraphRunContext) -> Increment | End[int]:
        if ctx.state.number == 42:
            return Increment()
        else:
            return End(ctx.state.number)

never_42_graph = Graph(nodes=(Increment, Check42))

(This example is complete, it can be run "as is")

```
from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext

@dataclass
class MyState:
    number: int

@dataclass
class Increment(BaseNode[MyState]):
    async def run(self, ctx: GraphRunContext) -> Check42:
        ctx.state.number += 1
        return Check42()

@dataclass
class Check42(BaseNode[MyState, None, int]):
    async def run(self, ctx: GraphRunContext) -> Increment | End[int]:
        if ctx.state.number == 42:
            return Increment()
        else:
            return End(ctx.state.number)

never_42_graph = Graph(nodes=(Increment, Check42))
```

```
from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext

@dataclass
class MyState:
    number: int

@dataclass
class Increment(BaseNode[MyState]):
    async def run(self, ctx: GraphRunContext) -> Check42:
        ctx.state.number += 1
        return Check42()

@dataclass
class Check42(BaseNode[MyState, None, int]):
    async def run(self, ctx: GraphRunContext) -> Increment | End[int]:
        if ctx.state.number == 42:
            return Increment()
        else:
            return End(ctx.state.number)

never_42_graph = Graph(nodes=(Increment, Check42))
```

See run For an example of running graph, and
mermaid_code for an example of generating a mermaid diagram
from the graph.

```
run
```

```
mermaid_code
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
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
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
```

```
@dataclass(init=False)
class Graph(Generic[StateT, DepsT, RunEndT]):
    """Definition of a graph.

    In `pydantic-graph`, a graph is a collection of nodes that can be run in sequence. The nodes define
    their outgoing edges â e.g. which nodes may be run next, and thereby the structure of the graph.

    Here's a very simple example of a graph which increments a number by 1, but makes sure the number is never
    42 at the end.

    ```py {title="never_42.py" noqa="I001" py="3.10"}
    from __future__ import annotations

    from dataclasses import dataclass

    from pydantic_graph import BaseNode, End, Graph, GraphRunContext

    @dataclass
    class MyState:
        number: int

    @dataclass
    class Increment(BaseNode[MyState]):
        async def run(self, ctx: GraphRunContext) -> Check42:
            ctx.state.number += 1
            return Check42()

    @dataclass
    class Check42(BaseNode[MyState, None, int]):
        async def run(self, ctx: GraphRunContext) -> Increment | End[int]:
            if ctx.state.number == 42:
                return Increment()
            else:
                return End(ctx.state.number)

    never_42_graph = Graph(nodes=(Increment, Check42))
    ```
    _(This example is complete, it can be run "as is")_

    See [`run`][pydantic_graph.graph.Graph.run] For an example of running graph, and
    [`mermaid_code`][pydantic_graph.graph.Graph.mermaid_code] for an example of generating a mermaid diagram
    from the graph.
    """

    name: str | None
    node_defs: dict[str, NodeDef[StateT, DepsT, RunEndT]]
    snapshot_state: Callable[[StateT], StateT]
    _state_type: type[StateT] | _utils.Unset = field(repr=False)
    _run_end_type: type[RunEndT] | _utils.Unset = field(repr=False)
    _auto_instrument: bool = field(repr=False)

    def __init__(
        self,
        *,
        nodes: Sequence[type[BaseNode[StateT, DepsT, RunEndT]]],
        name: str | None = None,
        state_type: type[StateT] | _utils.Unset = _utils.UNSET,
        run_end_type: type[RunEndT] | _utils.Unset = _utils.UNSET,
        snapshot_state: Callable[[StateT], StateT] = deep_copy_state,
        auto_instrument: bool = True,
    ):
        """Create a graph from a sequence of nodes.

        Args:
            nodes: The nodes which make up the graph, nodes need to be unique and all be generic in the same
                state type.
            name: Optional name for the graph, if not provided the name will be inferred from the calling frame
                on the first call to a graph method.
            state_type: The type of the state for the graph, this can generally be inferred from `nodes`.
            run_end_type: The type of the result of running the graph, this can generally be inferred from `nodes`.
            snapshot_state: A function to snapshot the state of the graph, this is used in
                [`NodeStep`][pydantic_graph.state.NodeStep] and [`EndStep`][pydantic_graph.state.EndStep] to record
                the state before each step.
            auto_instrument: Whether to create a span for the graph run and the execution of each node's run method.
        """
        self.name = name
        self._state_type = state_type
        self._run_end_type = run_end_type
        self._auto_instrument = auto_instrument
        self.snapshot_state = snapshot_state

        parent_namespace = _utils.get_parent_namespace(inspect.currentframe())
        self.node_defs: dict[str, NodeDef[StateT, DepsT, RunEndT]] = {}
        for node in nodes:
            self._register_node(node, parent_namespace)

        self._validate_edges()

    async def run(
        self: Graph[StateT, DepsT, T],
        start_node: BaseNode[StateT, DepsT, T],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
        span: LogfireSpan | None = None,
    ) -> GraphRunResult[StateT, T]:
        """Run the graph from a starting node until it ends.

        Args:
            start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
                you need to provide the starting node.
            state: The initial state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.
            span: The span to use for the graph run. If not provided, a span will be created depending on the value of
                the `_auto_instrument` field.

        Returns:
            A `GraphRunResult` containing information about the run, including its final result.

        Here's an example of running the graph from [above][pydantic_graph.graph.Graph]:

        ```py {title="run_never_42.py" noqa="I001" py="3.10"}
        from never_42 import Increment, MyState, never_42_graph

        async def main():
            state = MyState(1)
            graph_run_result = await never_42_graph.run(Increment(), state=state)
            print(state)
            #> MyState(number=2)
            print(len(graph_run_result.history))
            #> 3

            state = MyState(41)
            graph_run_result = await never_42_graph.run(Increment(), state=state)
            print(state)
            #> MyState(number=43)
            print(len(graph_run_result.history))
            #> 5
        ```
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())

        async with self.iter(start_node, state=state, deps=deps, infer_name=infer_name, span=span) as graph_run:
            async for _node in graph_run:
                pass

        final_result = graph_run.result
        assert final_result is not None, 'GraphRun should have a final result'
        return final_result

    @asynccontextmanager
    async def iter(
        self: Graph[StateT, DepsT, T],
        start_node: BaseNode[StateT, DepsT, T],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
        span: AbstractContextManager[Any] | None = None,
    ) -> AsyncIterator[GraphRun[StateT, DepsT, T]]:
        """A contextmanager which can be used to iterate over the graph's nodes as they are executed.

        This method returns a `GraphRun` object which can be used to async-iterate over the nodes of this `Graph` as
        they are executed. This is the API to use if you want to record or interact with the nodes as the graph
        execution unfolds.

        The `GraphRun` can also be used to manually drive the graph execution by calling
        [`GraphRun.next`][pydantic_graph.graph.GraphRun.next].

        The `GraphRun` provides access to the full run history, state, deps, and the final result of the run once
        it has completed.

        For more details, see the API documentation of [`GraphRun`][pydantic_graph.graph.GraphRun].

        Args:
            start_node: the first node to run. Since the graph definition doesn't define the entry point in the graph,
                you need to provide the starting node.
            state: The initial state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.
            span: The span to use for the graph run. If not provided, a new span will be created.

        Yields:
            A GraphRun that can be async iterated over to drive the graph to completion.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())

        if self._auto_instrument and span is None:
            span = logfire_api.span('run graph {graph.name}', graph=self)

        with ExitStack() as stack:
            if span is not None:
                stack.enter_context(span)
            yield GraphRun[StateT, DepsT, T](
                self,
                start_node,
                history=[],
                state=state,
                deps=deps,
                auto_instrument=self._auto_instrument,
            )

    def run_sync(
        self: Graph[StateT, DepsT, T],
        start_node: BaseNode[StateT, DepsT, T],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
    ) -> GraphRunResult[StateT, T]:
        """Synchronously run the graph.

        This is a convenience method that wraps [`self.run`][pydantic_graph.Graph.run] with `loop.run_until_complete(...)`.
        You therefore can't use this method inside async code or if there's an active event loop.

        Args:
            start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
                you need to provide the starting node.
            state: The initial state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.

        Returns:
            The result type from ending the run and the history of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        return _utils.get_event_loop().run_until_complete(
            self.run(start_node, state=state, deps=deps, infer_name=False)
        )

    async def next(
        self: Graph[StateT, DepsT, T],
        node: BaseNode[StateT, DepsT, T],
        history: list[HistoryStep[StateT, T]],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
    ) -> BaseNode[StateT, DepsT, Any] | End[T]:
        """Run a node in the graph and return the next node to run.

        Args:
            node: The node to run.
            history: The history of the graph run so far. NOTE: this will be mutated to add the new step.
            state: The current state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.

        Returns:
            The next node to run or [`End`][pydantic_graph.nodes.End] if the graph has finished.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())

        if isinstance(node, End):
            # While technically this is not compatible with the documented method signature, it's an easy mistake to
            # make, and we should eagerly provide a more helpful error message than you'd get otherwise.
            raise exceptions.GraphRuntimeError(f'Cannot call `next` with an `End` node: {node!r}.')

        node_id = node.get_id()
        if node_id not in self.node_defs:
            raise exceptions.GraphRuntimeError(f'Node `{node}` is not in the graph.')

        with ExitStack() as stack:
            if self._auto_instrument:
                stack.enter_context(_logfire.span('run node {node_id}', node_id=node_id, node=node))
            ctx = GraphRunContext(state, deps)
            start_ts = _utils.now_utc()
            start = perf_counter()
            next_node = await node.run(ctx)
            duration = perf_counter() - start

        history.append(
            NodeStep(state=state, node=node, start_ts=start_ts, duration=duration, snapshot_state=self.snapshot_state)
        )

        if isinstance(next_node, End):
            history.append(EndStep(result=next_node))
        elif not isinstance(next_node, BaseNode):
            if TYPE_CHECKING:
                typing_extensions.assert_never(next_node)
            else:
                raise exceptions.GraphRuntimeError(
                    f'Invalid node return type: `{type(next_node).__name__}`. Expected `BaseNode` or `End`.'
                )

        return next_node

    def dump_history(
        self: Graph[StateT, DepsT, T], history: list[HistoryStep[StateT, T]], *, indent: int | None = None
    ) -> bytes:
        """Dump the history of a graph run as JSON.

        Args:
            history: The history of the graph run.
            indent: The number of spaces to indent the JSON.

        Returns:
            The JSON representation of the history.
        """
        return self.history_type_adapter.dump_json(history, indent=indent)

    def load_history(self, json_bytes: str | bytes | bytearray) -> list[HistoryStep[StateT, RunEndT]]:
        """Load the history of a graph run from JSON.

        Args:
            json_bytes: The JSON representation of the history.

        Returns:
            The history of the graph run.
        """
        return self.history_type_adapter.validate_json(json_bytes)

    @cached_property
    def history_type_adapter(self) -> pydantic.TypeAdapter[list[HistoryStep[StateT, RunEndT]]]:
        nodes = [node_def.node for node_def in self.node_defs.values()]
        state_t = self._get_state_type()
        end_t = self._get_run_end_type()
        token = nodes_schema_var.set(nodes)
        try:
            ta = pydantic.TypeAdapter(list[Annotated[HistoryStep[state_t, end_t], pydantic.Discriminator('kind')]])
        finally:
            nodes_schema_var.reset(token)
        return ta

    def mermaid_code(
        self,
        *,
        start_node: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
        title: str | None | typing_extensions.Literal[False] = None,
        edge_labels: bool = True,
        notes: bool = True,
        highlighted_nodes: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
        highlight_css: str = mermaid.DEFAULT_HIGHLIGHT_CSS,
        infer_name: bool = True,
        direction: mermaid.StateDiagramDirection | None = None,
    ) -> str:
        """Generate a diagram representing the graph as [mermaid](https://mermaid.js.org/) diagram.

        This method calls [`pydantic_graph.mermaid.generate_code`][pydantic_graph.mermaid.generate_code].

        Args:
            start_node: The node or nodes which can start the graph.
            title: The title of the diagram, use `False` to not include a title.
            edge_labels: Whether to include edge labels.
            notes: Whether to include notes on each node.
            highlighted_nodes: Optional node or nodes to highlight.
            highlight_css: The CSS to use for highlighting nodes.
            infer_name: Whether to infer the graph name from the calling frame.
            direction: The direction of flow.

        Returns:
            The mermaid code for the graph, which can then be rendered as a diagram.

        Here's an example of generating a diagram for the graph from [above][pydantic_graph.graph.Graph]:

        ```py {title="mermaid_never_42.py" py="3.10"}
        from never_42 import Increment, never_42_graph

        print(never_42_graph.mermaid_code(start_node=Increment))
        '''
        ---
        title: never_42_graph
        ---
        stateDiagram-v2
          [*] --> Increment
          Increment --> Check42
          Check42 --> Increment
          Check42 --> [*]
        '''
        ```

        The rendered diagram will look like this:

        ```mermaid
        ---
        title: never_42_graph
        ---
        stateDiagram-v2
          [*] --> Increment
          Increment --> Check42
          Check42 --> Increment
          Check42 --> [*]
        ```
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        if title is None and self.name:
            title = self.name
        return mermaid.generate_code(
            self,
            start_node=start_node,
            highlighted_nodes=highlighted_nodes,
            highlight_css=highlight_css,
            title=title or None,
            edge_labels=edge_labels,
            notes=notes,
            direction=direction,
        )

    def mermaid_image(
        self, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
    ) -> bytes:
        """Generate a diagram representing the graph as an image.

        The format and diagram can be customized using `kwargs`,
        see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

        !!! note "Uses external service"
            This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
            is a free service not affiliated with Pydantic.

        Args:
            infer_name: Whether to infer the graph name from the calling frame.
            **kwargs: Additional arguments to pass to `mermaid.request_image`.

        Returns:
            The image bytes.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        if 'title' not in kwargs and self.name:
            kwargs['title'] = self.name
        return mermaid.request_image(self, **kwargs)

    def mermaid_save(
        self, path: Path | str, /, *, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
    ) -> None:
        """Generate a diagram representing the graph and save it as an image.

        The format and diagram can be customized using `kwargs`,
        see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

        !!! note "Uses external service"
            This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
            is a free service not affiliated with Pydantic.

        Args:
            path: The path to save the image to.
            infer_name: Whether to infer the graph name from the calling frame.
            **kwargs: Additional arguments to pass to `mermaid.save_image`.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        if 'title' not in kwargs and self.name:
            kwargs['title'] = self.name
        mermaid.save_image(path, self, **kwargs)

    def _get_state_type(self) -> type[StateT]:
        if _utils.is_set(self._state_type):
            return self._state_type

        for node_def in self.node_defs.values():
            for base in typing_extensions.get_original_bases(node_def.node):
                if typing_extensions.get_origin(base) is BaseNode:
                    args = typing_extensions.get_args(base)
                    if args:
                        return args[0]
                    # break the inner (bases) loop
                    break
        # state defaults to None, so use that if we can't infer it
        return type(None)  # pyright: ignore[reportReturnType]

    def _get_run_end_type(self) -> type[RunEndT]:
        if _utils.is_set(self._run_end_type):
            return self._run_end_type

        for node_def in self.node_defs.values():
            for base in typing_extensions.get_original_bases(node_def.node):
                if typing_extensions.get_origin(base) is BaseNode:
                    args = typing_extensions.get_args(base)
                    if len(args) == 3:
                        t = args[2]
                        if not typing_objects.is_never(t):
                            return t
                    # break the inner (bases) loop
                    break
        raise exceptions.GraphSetupError('Could not infer run end type from nodes, please set `run_end_type`.')

    def _register_node(
        self: Graph[StateT, DepsT, T],
        node: type[BaseNode[StateT, DepsT, T]],
        parent_namespace: dict[str, Any] | None,
    ) -> None:
        node_id = node.get_id()
        if existing_node := self.node_defs.get(node_id):
            raise exceptions.GraphSetupError(
                f'Node ID `{node_id}` is not unique â found on {existing_node.node} and {node}'
            )
        else:
            self.node_defs[node_id] = node.get_node_def(parent_namespace)

    def _validate_edges(self):
        known_node_ids = self.node_defs.keys()
        bad_edges: dict[str, list[str]] = {}

        for node_id, node_def in self.node_defs.items():
            for edge in node_def.next_node_edges.keys():
                if edge not in known_node_ids:
                    bad_edges.setdefault(edge, []).append(f'`{node_id}`')

        if bad_edges:
            bad_edges_list = [f'`{k}` is referenced by {_utils.comma_and(v)}' for k, v in bad_edges.items()]
            if len(bad_edges_list) == 1:
                raise exceptions.GraphSetupError(f'{bad_edges_list[0]} but not included in the graph.')
            else:
                b = '\n'.join(f' {be}' for be in bad_edges_list)
                raise exceptions.GraphSetupError(
                    f'Nodes are referenced in the graph but not included in the graph:\n{b}'
                )

    def _infer_name(self, function_frame: types.FrameType | None) -> None:
        """Infer the agent name from the call frame.

        Usage should be `self._infer_name(inspect.currentframe())`.

        Copied from `Agent`.
        """
        assert self.name is None, 'Name already set'
        if function_frame is not None and (parent_frame := function_frame.f_back):  # pragma: no branch
            for name, item in parent_frame.f_locals.items():
                if item is self:
                    self.name = name
                    return
            if parent_frame.f_locals != parent_frame.f_globals:
                # if we couldn't find the agent in locals and globals are a different dict, try globals
                for name, item in parent_frame.f_globals.items():
                    if item is self:
                        self.name = name
                        return
```

```
@dataclass(init=False)
class Graph(Generic[StateT, DepsT, RunEndT]):
    """Definition of a graph.

    In `pydantic-graph`, a graph is a collection of nodes that can be run in sequence. The nodes define
    their outgoing edges â e.g. which nodes may be run next, and thereby the structure of the graph.

    Here's a very simple example of a graph which increments a number by 1, but makes sure the number is never
    42 at the end.

    ```py {title="never_42.py" noqa="I001" py="3.10"}
    from __future__ import annotations

    from dataclasses import dataclass

    from pydantic_graph import BaseNode, End, Graph, GraphRunContext

    @dataclass
    class MyState:
        number: int

    @dataclass
    class Increment(BaseNode[MyState]):
        async def run(self, ctx: GraphRunContext) -> Check42:
            ctx.state.number += 1
            return Check42()

    @dataclass
    class Check42(BaseNode[MyState, None, int]):
        async def run(self, ctx: GraphRunContext) -> Increment | End[int]:
            if ctx.state.number == 42:
                return Increment()
            else:
                return End(ctx.state.number)

    never_42_graph = Graph(nodes=(Increment, Check42))
    ```
    _(This example is complete, it can be run "as is")_

    See [`run`][pydantic_graph.graph.Graph.run] For an example of running graph, and
    [`mermaid_code`][pydantic_graph.graph.Graph.mermaid_code] for an example of generating a mermaid diagram
    from the graph.
    """

    name: str | None
    node_defs: dict[str, NodeDef[StateT, DepsT, RunEndT]]
    snapshot_state: Callable[[StateT], StateT]
    _state_type: type[StateT] | _utils.Unset = field(repr=False)
    _run_end_type: type[RunEndT] | _utils.Unset = field(repr=False)
    _auto_instrument: bool = field(repr=False)

    def __init__(
        self,
        *,
        nodes: Sequence[type[BaseNode[StateT, DepsT, RunEndT]]],
        name: str | None = None,
        state_type: type[StateT] | _utils.Unset = _utils.UNSET,
        run_end_type: type[RunEndT] | _utils.Unset = _utils.UNSET,
        snapshot_state: Callable[[StateT], StateT] = deep_copy_state,
        auto_instrument: bool = True,
    ):
        """Create a graph from a sequence of nodes.

        Args:
            nodes: The nodes which make up the graph, nodes need to be unique and all be generic in the same
                state type.
            name: Optional name for the graph, if not provided the name will be inferred from the calling frame
                on the first call to a graph method.
            state_type: The type of the state for the graph, this can generally be inferred from `nodes`.
            run_end_type: The type of the result of running the graph, this can generally be inferred from `nodes`.
            snapshot_state: A function to snapshot the state of the graph, this is used in
                [`NodeStep`][pydantic_graph.state.NodeStep] and [`EndStep`][pydantic_graph.state.EndStep] to record
                the state before each step.
            auto_instrument: Whether to create a span for the graph run and the execution of each node's run method.
        """
        self.name = name
        self._state_type = state_type
        self._run_end_type = run_end_type
        self._auto_instrument = auto_instrument
        self.snapshot_state = snapshot_state

        parent_namespace = _utils.get_parent_namespace(inspect.currentframe())
        self.node_defs: dict[str, NodeDef[StateT, DepsT, RunEndT]] = {}
        for node in nodes:
            self._register_node(node, parent_namespace)

        self._validate_edges()

    async def run(
        self: Graph[StateT, DepsT, T],
        start_node: BaseNode[StateT, DepsT, T],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
        span: LogfireSpan | None = None,
    ) -> GraphRunResult[StateT, T]:
        """Run the graph from a starting node until it ends.

        Args:
            start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
                you need to provide the starting node.
            state: The initial state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.
            span: The span to use for the graph run. If not provided, a span will be created depending on the value of
                the `_auto_instrument` field.

        Returns:
            A `GraphRunResult` containing information about the run, including its final result.

        Here's an example of running the graph from [above][pydantic_graph.graph.Graph]:

        ```py {title="run_never_42.py" noqa="I001" py="3.10"}
        from never_42 import Increment, MyState, never_42_graph

        async def main():
            state = MyState(1)
            graph_run_result = await never_42_graph.run(Increment(), state=state)
            print(state)
            #> MyState(number=2)
            print(len(graph_run_result.history))
            #> 3

            state = MyState(41)
            graph_run_result = await never_42_graph.run(Increment(), state=state)
            print(state)
            #> MyState(number=43)
            print(len(graph_run_result.history))
            #> 5
        ```
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())

        async with self.iter(start_node, state=state, deps=deps, infer_name=infer_name, span=span) as graph_run:
            async for _node in graph_run:
                pass

        final_result = graph_run.result
        assert final_result is not None, 'GraphRun should have a final result'
        return final_result

    @asynccontextmanager
    async def iter(
        self: Graph[StateT, DepsT, T],
        start_node: BaseNode[StateT, DepsT, T],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
        span: AbstractContextManager[Any] | None = None,
    ) -> AsyncIterator[GraphRun[StateT, DepsT, T]]:
        """A contextmanager which can be used to iterate over the graph's nodes as they are executed.

        This method returns a `GraphRun` object which can be used to async-iterate over the nodes of this `Graph` as
        they are executed. This is the API to use if you want to record or interact with the nodes as the graph
        execution unfolds.

        The `GraphRun` can also be used to manually drive the graph execution by calling
        [`GraphRun.next`][pydantic_graph.graph.GraphRun.next].

        The `GraphRun` provides access to the full run history, state, deps, and the final result of the run once
        it has completed.

        For more details, see the API documentation of [`GraphRun`][pydantic_graph.graph.GraphRun].

        Args:
            start_node: the first node to run. Since the graph definition doesn't define the entry point in the graph,
                you need to provide the starting node.
            state: The initial state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.
            span: The span to use for the graph run. If not provided, a new span will be created.

        Yields:
            A GraphRun that can be async iterated over to drive the graph to completion.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())

        if self._auto_instrument and span is None:
            span = logfire_api.span('run graph {graph.name}', graph=self)

        with ExitStack() as stack:
            if span is not None:
                stack.enter_context(span)
            yield GraphRun[StateT, DepsT, T](
                self,
                start_node,
                history=[],
                state=state,
                deps=deps,
                auto_instrument=self._auto_instrument,
            )

    def run_sync(
        self: Graph[StateT, DepsT, T],
        start_node: BaseNode[StateT, DepsT, T],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
    ) -> GraphRunResult[StateT, T]:
        """Synchronously run the graph.

        This is a convenience method that wraps [`self.run`][pydantic_graph.Graph.run] with `loop.run_until_complete(...)`.
        You therefore can't use this method inside async code or if there's an active event loop.

        Args:
            start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
                you need to provide the starting node.
            state: The initial state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.

        Returns:
            The result type from ending the run and the history of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        return _utils.get_event_loop().run_until_complete(
            self.run(start_node, state=state, deps=deps, infer_name=False)
        )

    async def next(
        self: Graph[StateT, DepsT, T],
        node: BaseNode[StateT, DepsT, T],
        history: list[HistoryStep[StateT, T]],
        *,
        state: StateT = None,
        deps: DepsT = None,
        infer_name: bool = True,
    ) -> BaseNode[StateT, DepsT, Any] | End[T]:
        """Run a node in the graph and return the next node to run.

        Args:
            node: The node to run.
            history: The history of the graph run so far. NOTE: this will be mutated to add the new step.
            state: The current state of the graph.
            deps: The dependencies of the graph.
            infer_name: Whether to infer the graph name from the calling frame.

        Returns:
            The next node to run or [`End`][pydantic_graph.nodes.End] if the graph has finished.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())

        if isinstance(node, End):
            # While technically this is not compatible with the documented method signature, it's an easy mistake to
            # make, and we should eagerly provide a more helpful error message than you'd get otherwise.
            raise exceptions.GraphRuntimeError(f'Cannot call `next` with an `End` node: {node!r}.')

        node_id = node.get_id()
        if node_id not in self.node_defs:
            raise exceptions.GraphRuntimeError(f'Node `{node}` is not in the graph.')

        with ExitStack() as stack:
            if self._auto_instrument:
                stack.enter_context(_logfire.span('run node {node_id}', node_id=node_id, node=node))
            ctx = GraphRunContext(state, deps)
            start_ts = _utils.now_utc()
            start = perf_counter()
            next_node = await node.run(ctx)
            duration = perf_counter() - start

        history.append(
            NodeStep(state=state, node=node, start_ts=start_ts, duration=duration, snapshot_state=self.snapshot_state)
        )

        if isinstance(next_node, End):
            history.append(EndStep(result=next_node))
        elif not isinstance(next_node, BaseNode):
            if TYPE_CHECKING:
                typing_extensions.assert_never(next_node)
            else:
                raise exceptions.GraphRuntimeError(
                    f'Invalid node return type: `{type(next_node).__name__}`. Expected `BaseNode` or `End`.'
                )

        return next_node

    def dump_history(
        self: Graph[StateT, DepsT, T], history: list[HistoryStep[StateT, T]], *, indent: int | None = None
    ) -> bytes:
        """Dump the history of a graph run as JSON.

        Args:
            history: The history of the graph run.
            indent: The number of spaces to indent the JSON.

        Returns:
            The JSON representation of the history.
        """
        return self.history_type_adapter.dump_json(history, indent=indent)

    def load_history(self, json_bytes: str | bytes | bytearray) -> list[HistoryStep[StateT, RunEndT]]:
        """Load the history of a graph run from JSON.

        Args:
            json_bytes: The JSON representation of the history.

        Returns:
            The history of the graph run.
        """
        return self.history_type_adapter.validate_json(json_bytes)

    @cached_property
    def history_type_adapter(self) -> pydantic.TypeAdapter[list[HistoryStep[StateT, RunEndT]]]:
        nodes = [node_def.node for node_def in self.node_defs.values()]
        state_t = self._get_state_type()
        end_t = self._get_run_end_type()
        token = nodes_schema_var.set(nodes)
        try:
            ta = pydantic.TypeAdapter(list[Annotated[HistoryStep[state_t, end_t], pydantic.Discriminator('kind')]])
        finally:
            nodes_schema_var.reset(token)
        return ta

    def mermaid_code(
        self,
        *,
        start_node: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
        title: str | None | typing_extensions.Literal[False] = None,
        edge_labels: bool = True,
        notes: bool = True,
        highlighted_nodes: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
        highlight_css: str = mermaid.DEFAULT_HIGHLIGHT_CSS,
        infer_name: bool = True,
        direction: mermaid.StateDiagramDirection | None = None,
    ) -> str:
        """Generate a diagram representing the graph as [mermaid](https://mermaid.js.org/) diagram.

        This method calls [`pydantic_graph.mermaid.generate_code`][pydantic_graph.mermaid.generate_code].

        Args:
            start_node: The node or nodes which can start the graph.
            title: The title of the diagram, use `False` to not include a title.
            edge_labels: Whether to include edge labels.
            notes: Whether to include notes on each node.
            highlighted_nodes: Optional node or nodes to highlight.
            highlight_css: The CSS to use for highlighting nodes.
            infer_name: Whether to infer the graph name from the calling frame.
            direction: The direction of flow.

        Returns:
            The mermaid code for the graph, which can then be rendered as a diagram.

        Here's an example of generating a diagram for the graph from [above][pydantic_graph.graph.Graph]:

        ```py {title="mermaid_never_42.py" py="3.10"}
        from never_42 import Increment, never_42_graph

        print(never_42_graph.mermaid_code(start_node=Increment))
        '''
        ---
        title: never_42_graph
        ---
        stateDiagram-v2
          [*] --> Increment
          Increment --> Check42
          Check42 --> Increment
          Check42 --> [*]
        '''
        ```

        The rendered diagram will look like this:

        ```mermaid
        ---
        title: never_42_graph
        ---
        stateDiagram-v2
          [*] --> Increment
          Increment --> Check42
          Check42 --> Increment
          Check42 --> [*]
        ```
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        if title is None and self.name:
            title = self.name
        return mermaid.generate_code(
            self,
            start_node=start_node,
            highlighted_nodes=highlighted_nodes,
            highlight_css=highlight_css,
            title=title or None,
            edge_labels=edge_labels,
            notes=notes,
            direction=direction,
        )

    def mermaid_image(
        self, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
    ) -> bytes:
        """Generate a diagram representing the graph as an image.

        The format and diagram can be customized using `kwargs`,
        see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

        !!! note "Uses external service"
            This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
            is a free service not affiliated with Pydantic.

        Args:
            infer_name: Whether to infer the graph name from the calling frame.
            **kwargs: Additional arguments to pass to `mermaid.request_image`.

        Returns:
            The image bytes.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        if 'title' not in kwargs and self.name:
            kwargs['title'] = self.name
        return mermaid.request_image(self, **kwargs)

    def mermaid_save(
        self, path: Path | str, /, *, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
    ) -> None:
        """Generate a diagram representing the graph and save it as an image.

        The format and diagram can be customized using `kwargs`,
        see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

        !!! note "Uses external service"
            This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
            is a free service not affiliated with Pydantic.

        Args:
            path: The path to save the image to.
            infer_name: Whether to infer the graph name from the calling frame.
            **kwargs: Additional arguments to pass to `mermaid.save_image`.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        if 'title' not in kwargs and self.name:
            kwargs['title'] = self.name
        mermaid.save_image(path, self, **kwargs)

    def _get_state_type(self) -> type[StateT]:
        if _utils.is_set(self._state_type):
            return self._state_type

        for node_def in self.node_defs.values():
            for base in typing_extensions.get_original_bases(node_def.node):
                if typing_extensions.get_origin(base) is BaseNode:
                    args = typing_extensions.get_args(base)
                    if args:
                        return args[0]
                    # break the inner (bases) loop
                    break
        # state defaults to None, so use that if we can't infer it
        return type(None)  # pyright: ignore[reportReturnType]

    def _get_run_end_type(self) -> type[RunEndT]:
        if _utils.is_set(self._run_end_type):
            return self._run_end_type

        for node_def in self.node_defs.values():
            for base in typing_extensions.get_original_bases(node_def.node):
                if typing_extensions.get_origin(base) is BaseNode:
                    args = typing_extensions.get_args(base)
                    if len(args) == 3:
                        t = args[2]
                        if not typing_objects.is_never(t):
                            return t
                    # break the inner (bases) loop
                    break
        raise exceptions.GraphSetupError('Could not infer run end type from nodes, please set `run_end_type`.')

    def _register_node(
        self: Graph[StateT, DepsT, T],
        node: type[BaseNode[StateT, DepsT, T]],
        parent_namespace: dict[str, Any] | None,
    ) -> None:
        node_id = node.get_id()
        if existing_node := self.node_defs.get(node_id):
            raise exceptions.GraphSetupError(
                f'Node ID `{node_id}` is not unique â found on {existing_node.node} and {node}'
            )
        else:
            self.node_defs[node_id] = node.get_node_def(parent_namespace)

    def _validate_edges(self):
        known_node_ids = self.node_defs.keys()
        bad_edges: dict[str, list[str]] = {}

        for node_id, node_def in self.node_defs.items():
            for edge in node_def.next_node_edges.keys():
                if edge not in known_node_ids:
                    bad_edges.setdefault(edge, []).append(f'`{node_id}`')

        if bad_edges:
            bad_edges_list = [f'`{k}` is referenced by {_utils.comma_and(v)}' for k, v in bad_edges.items()]
            if len(bad_edges_list) == 1:
                raise exceptions.GraphSetupError(f'{bad_edges_list[0]} but not included in the graph.')
            else:
                b = '\n'.join(f' {be}' for be in bad_edges_list)
                raise exceptions.GraphSetupError(
                    f'Nodes are referenced in the graph but not included in the graph:\n{b}'
                )

    def _infer_name(self, function_frame: types.FrameType | None) -> None:
        """Infer the agent name from the call frame.

        Usage should be `self._infer_name(inspect.currentframe())`.

        Copied from `Agent`.
        """
        assert self.name is None, 'Name already set'
        if function_frame is not None and (parent_frame := function_frame.f_back):  # pragma: no branch
            for name, item in parent_frame.f_locals.items():
                if item is self:
                    self.name = name
                    return
            if parent_frame.f_locals != parent_frame.f_globals:
                # if we couldn't find the agent in locals and globals are a different dict, try globals
                for name, item in parent_frame.f_globals.items():
                    if item is self:
                        self.name = name
                        return
```

#### __init__

```
__init__(
    *,
    nodes: Sequence[type[BaseNode[StateT, DepsT, RunEndT]]],
    name: str | None = None,
    state_type: type[StateT] | Unset = UNSET,
    run_end_type: type[RunEndT] | Unset = UNSET,
    snapshot_state: Callable[
        [StateT], StateT
    ] = deep_copy_state,
    auto_instrument: bool = True
)
```

```
__init__(
    *,
    nodes: Sequence[type[BaseNode[StateT, DepsT, RunEndT]]],
    name: str | None = None,
    state_type: type[StateT] | Unset = UNSET,
    run_end_type: type[RunEndT] | Unset = UNSET,
    snapshot_state: Callable[
        [StateT], StateT
    ] = deep_copy_state,
    auto_instrument: bool = True
)
```

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[type](https://docs.python.org/3/library/functions.html#type)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[type](https://docs.python.org/3/library/functions.html#type)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[deep_copy_state](https://ai.pydantic.dev/state/#pydantic_graph.state.deep_copy_state)

[bool](https://docs.python.org/3/library/functions.html#bool)

Create a graph from a sequence of nodes.

Parameters:

```
nodes
```

```
Sequence[type[BaseNode[StateT, DepsT, RunEndT]]]
```

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[type](https://docs.python.org/3/library/functions.html#type)

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The nodes which make up the graph, nodes need to be unique and all be generic in the same
state type.

```
name
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Optional name for the graph, if not provided the name will be inferred from the calling frame
on the first call to a graph method.

```
None
```

```
state_type
```

```
type[StateT] | Unset
```

[type](https://docs.python.org/3/library/functions.html#type)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The type of the state for the graph, this can generally be inferred from nodes.

```
nodes
```

```
UNSET
```

```
run_end_type
```

```
type[RunEndT] | Unset
```

[type](https://docs.python.org/3/library/functions.html#type)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The type of the result of running the graph, this can generally be inferred from nodes.

```
nodes
```

```
UNSET
```

```
snapshot_state
```

```
Callable[[StateT], StateT]
```

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

A function to snapshot the state of the graph, this is used in
NodeStep and EndStep to record
the state before each step.

```
NodeStep
```

```
EndStep
```

```
deep_copy_state
```

[deep_copy_state](https://ai.pydantic.dev/state/#pydantic_graph.state.deep_copy_state)

```
auto_instrument
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to create a span for the graph run and the execution of each node's run method.

```
True
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
def __init__(
    self,
    *,
    nodes: Sequence[type[BaseNode[StateT, DepsT, RunEndT]]],
    name: str | None = None,
    state_type: type[StateT] | _utils.Unset = _utils.UNSET,
    run_end_type: type[RunEndT] | _utils.Unset = _utils.UNSET,
    snapshot_state: Callable[[StateT], StateT] = deep_copy_state,
    auto_instrument: bool = True,
):
    """Create a graph from a sequence of nodes.

    Args:
        nodes: The nodes which make up the graph, nodes need to be unique and all be generic in the same
            state type.
        name: Optional name for the graph, if not provided the name will be inferred from the calling frame
            on the first call to a graph method.
        state_type: The type of the state for the graph, this can generally be inferred from `nodes`.
        run_end_type: The type of the result of running the graph, this can generally be inferred from `nodes`.
        snapshot_state: A function to snapshot the state of the graph, this is used in
            [`NodeStep`][pydantic_graph.state.NodeStep] and [`EndStep`][pydantic_graph.state.EndStep] to record
            the state before each step.
        auto_instrument: Whether to create a span for the graph run and the execution of each node's run method.
    """
    self.name = name
    self._state_type = state_type
    self._run_end_type = run_end_type
    self._auto_instrument = auto_instrument
    self.snapshot_state = snapshot_state

    parent_namespace = _utils.get_parent_namespace(inspect.currentframe())
    self.node_defs: dict[str, NodeDef[StateT, DepsT, RunEndT]] = {}
    for node in nodes:
        self._register_node(node, parent_namespace)

    self._validate_edges()
```

```
def __init__(
    self,
    *,
    nodes: Sequence[type[BaseNode[StateT, DepsT, RunEndT]]],
    name: str | None = None,
    state_type: type[StateT] | _utils.Unset = _utils.UNSET,
    run_end_type: type[RunEndT] | _utils.Unset = _utils.UNSET,
    snapshot_state: Callable[[StateT], StateT] = deep_copy_state,
    auto_instrument: bool = True,
):
    """Create a graph from a sequence of nodes.

    Args:
        nodes: The nodes which make up the graph, nodes need to be unique and all be generic in the same
            state type.
        name: Optional name for the graph, if not provided the name will be inferred from the calling frame
            on the first call to a graph method.
        state_type: The type of the state for the graph, this can generally be inferred from `nodes`.
        run_end_type: The type of the result of running the graph, this can generally be inferred from `nodes`.
        snapshot_state: A function to snapshot the state of the graph, this is used in
            [`NodeStep`][pydantic_graph.state.NodeStep] and [`EndStep`][pydantic_graph.state.EndStep] to record
            the state before each step.
        auto_instrument: Whether to create a span for the graph run and the execution of each node's run method.
    """
    self.name = name
    self._state_type = state_type
    self._run_end_type = run_end_type
    self._auto_instrument = auto_instrument
    self.snapshot_state = snapshot_state

    parent_namespace = _utils.get_parent_namespace(inspect.currentframe())
    self.node_defs: dict[str, NodeDef[StateT, DepsT, RunEndT]] = {}
    for node in nodes:
        self._register_node(node, parent_namespace)

    self._validate_edges()
```

#### run

async

```
async
```

```
run(
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: LogfireSpan | None = None
) -> GraphRunResult[StateT, T]
```

```
run(
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: LogfireSpan | None = None
) -> GraphRunResult[StateT, T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

[GraphRunResult](https://ai.pydantic.dev#pydantic_graph.graph.GraphRunResult)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

Run the graph from a starting node until it ends.

Parameters:

```
start_node
```

```
BaseNode[StateT, DepsT, T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

the first node to run, since the graph definition doesn't define the entry point in the graph,
you need to provide the starting node.

```
state
```

```
StateT
```

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The initial state of the graph.

```
None
```

```
deps
```

```
DepsT
```

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

The dependencies of the graph.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to infer the graph name from the calling frame.

```
True
```

```
span
```

```
LogfireSpan | None
```

The span to use for the graph run. If not provided, a span will be created depending on the value of
the _auto_instrument field.

```
_auto_instrument
```

```
None
```

Returns:

```
GraphRunResult[StateT, T]
```

[GraphRunResult](https://ai.pydantic.dev#pydantic_graph.graph.GraphRunResult)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

A GraphRunResult containing information about the run, including its final result.

```
GraphRunResult
```

Here's an example of running the graph from above:

```
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(1)
    graph_run_result = await never_42_graph.run(Increment(), state=state)
    print(state)
    #> MyState(number=2)
    print(len(graph_run_result.history))
    #> 3

    state = MyState(41)
    graph_run_result = await never_42_graph.run(Increment(), state=state)
    print(state)
    #> MyState(number=43)
    print(len(graph_run_result.history))
    #> 5
```

```
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(1)
    graph_run_result = await never_42_graph.run(Increment(), state=state)
    print(state)
    #> MyState(number=2)
    print(len(graph_run_result.history))
    #> 3

    state = MyState(41)
    graph_run_result = await never_42_graph.run(Increment(), state=state)
    print(state)
    #> MyState(number=43)
    print(len(graph_run_result.history))
    #> 5
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
async def run(
    self: Graph[StateT, DepsT, T],
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: LogfireSpan | None = None,
) -> GraphRunResult[StateT, T]:
    """Run the graph from a starting node until it ends.

    Args:
        start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
            you need to provide the starting node.
        state: The initial state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.
        span: The span to use for the graph run. If not provided, a span will be created depending on the value of
            the `_auto_instrument` field.

    Returns:
        A `GraphRunResult` containing information about the run, including its final result.

    Here's an example of running the graph from [above][pydantic_graph.graph.Graph]:

    ```py {title="run_never_42.py" noqa="I001" py="3.10"}
    from never_42 import Increment, MyState, never_42_graph

    async def main():
        state = MyState(1)
        graph_run_result = await never_42_graph.run(Increment(), state=state)
        print(state)
        #> MyState(number=2)
        print(len(graph_run_result.history))
        #> 3

        state = MyState(41)
        graph_run_result = await never_42_graph.run(Increment(), state=state)
        print(state)
        #> MyState(number=43)
        print(len(graph_run_result.history))
        #> 5
    ```
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())

    async with self.iter(start_node, state=state, deps=deps, infer_name=infer_name, span=span) as graph_run:
        async for _node in graph_run:
            pass

    final_result = graph_run.result
    assert final_result is not None, 'GraphRun should have a final result'
    return final_result
```

```
async def run(
    self: Graph[StateT, DepsT, T],
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: LogfireSpan | None = None,
) -> GraphRunResult[StateT, T]:
    """Run the graph from a starting node until it ends.

    Args:
        start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
            you need to provide the starting node.
        state: The initial state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.
        span: The span to use for the graph run. If not provided, a span will be created depending on the value of
            the `_auto_instrument` field.

    Returns:
        A `GraphRunResult` containing information about the run, including its final result.

    Here's an example of running the graph from [above][pydantic_graph.graph.Graph]:

    ```py {title="run_never_42.py" noqa="I001" py="3.10"}
    from never_42 import Increment, MyState, never_42_graph

    async def main():
        state = MyState(1)
        graph_run_result = await never_42_graph.run(Increment(), state=state)
        print(state)
        #> MyState(number=2)
        print(len(graph_run_result.history))
        #> 3

        state = MyState(41)
        graph_run_result = await never_42_graph.run(Increment(), state=state)
        print(state)
        #> MyState(number=43)
        print(len(graph_run_result.history))
        #> 5
    ```
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())

    async with self.iter(start_node, state=state, deps=deps, infer_name=infer_name, span=span) as graph_run:
        async for _node in graph_run:
            pass

    final_result = graph_run.result
    assert final_result is not None, 'GraphRun should have a final result'
    return final_result
```

#### iter

async

```
async
```

```
iter(
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: AbstractContextManager[Any] | None = None
) -> AsyncIterator[GraphRun[StateT, DepsT, T]]
```

```
iter(
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: AbstractContextManager[Any] | None = None
) -> AsyncIterator[GraphRun[StateT, DepsT, T]]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

[AbstractContextManager](https://docs.python.org/3/library/contextlib.html#contextlib.AbstractContextManager)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[GraphRun](https://ai.pydantic.dev#pydantic_graph.graph.GraphRun)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

A contextmanager which can be used to iterate over the graph's nodes as they are executed.

This method returns a GraphRun object which can be used to async-iterate over the nodes of this Graph as
they are executed. This is the API to use if you want to record or interact with the nodes as the graph
execution unfolds.

```
GraphRun
```

```
Graph
```

The GraphRun can also be used to manually drive the graph execution by calling
GraphRun.next.

```
GraphRun
```

```
GraphRun.next
```

The GraphRun provides access to the full run history, state, deps, and the final result of the run once
it has completed.

```
GraphRun
```

For more details, see the API documentation of GraphRun.

```
GraphRun
```

Parameters:

```
start_node
```

```
BaseNode[StateT, DepsT, T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

the first node to run. Since the graph definition doesn't define the entry point in the graph,
you need to provide the starting node.

```
state
```

```
StateT
```

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The initial state of the graph.

```
None
```

```
deps
```

```
DepsT
```

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

The dependencies of the graph.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to infer the graph name from the calling frame.

```
True
```

```
span
```

```
AbstractContextManager[Any] | None
```

[AbstractContextManager](https://docs.python.org/3/library/contextlib.html#contextlib.AbstractContextManager)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

The span to use for the graph run. If not provided, a new span will be created.

```
None
```

Yields:

```
AsyncIterator[GraphRun[StateT, DepsT, T]]
```

[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator)

[GraphRun](https://ai.pydantic.dev#pydantic_graph.graph.GraphRun)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

A GraphRun that can be async iterated over to drive the graph to completion.

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
@asynccontextmanager
async def iter(
    self: Graph[StateT, DepsT, T],
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: AbstractContextManager[Any] | None = None,
) -> AsyncIterator[GraphRun[StateT, DepsT, T]]:
    """A contextmanager which can be used to iterate over the graph's nodes as they are executed.

    This method returns a `GraphRun` object which can be used to async-iterate over the nodes of this `Graph` as
    they are executed. This is the API to use if you want to record or interact with the nodes as the graph
    execution unfolds.

    The `GraphRun` can also be used to manually drive the graph execution by calling
    [`GraphRun.next`][pydantic_graph.graph.GraphRun.next].

    The `GraphRun` provides access to the full run history, state, deps, and the final result of the run once
    it has completed.

    For more details, see the API documentation of [`GraphRun`][pydantic_graph.graph.GraphRun].

    Args:
        start_node: the first node to run. Since the graph definition doesn't define the entry point in the graph,
            you need to provide the starting node.
        state: The initial state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.
        span: The span to use for the graph run. If not provided, a new span will be created.

    Yields:
        A GraphRun that can be async iterated over to drive the graph to completion.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())

    if self._auto_instrument and span is None:
        span = logfire_api.span('run graph {graph.name}', graph=self)

    with ExitStack() as stack:
        if span is not None:
            stack.enter_context(span)
        yield GraphRun[StateT, DepsT, T](
            self,
            start_node,
            history=[],
            state=state,
            deps=deps,
            auto_instrument=self._auto_instrument,
        )
```

```
@asynccontextmanager
async def iter(
    self: Graph[StateT, DepsT, T],
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
    span: AbstractContextManager[Any] | None = None,
) -> AsyncIterator[GraphRun[StateT, DepsT, T]]:
    """A contextmanager which can be used to iterate over the graph's nodes as they are executed.

    This method returns a `GraphRun` object which can be used to async-iterate over the nodes of this `Graph` as
    they are executed. This is the API to use if you want to record or interact with the nodes as the graph
    execution unfolds.

    The `GraphRun` can also be used to manually drive the graph execution by calling
    [`GraphRun.next`][pydantic_graph.graph.GraphRun.next].

    The `GraphRun` provides access to the full run history, state, deps, and the final result of the run once
    it has completed.

    For more details, see the API documentation of [`GraphRun`][pydantic_graph.graph.GraphRun].

    Args:
        start_node: the first node to run. Since the graph definition doesn't define the entry point in the graph,
            you need to provide the starting node.
        state: The initial state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.
        span: The span to use for the graph run. If not provided, a new span will be created.

    Yields:
        A GraphRun that can be async iterated over to drive the graph to completion.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())

    if self._auto_instrument and span is None:
        span = logfire_api.span('run graph {graph.name}', graph=self)

    with ExitStack() as stack:
        if span is not None:
            stack.enter_context(span)
        yield GraphRun[StateT, DepsT, T](
            self,
            start_node,
            history=[],
            state=state,
            deps=deps,
            auto_instrument=self._auto_instrument,
        )
```

#### run_sync

```
run_sync(
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True
) -> GraphRunResult[StateT, T]
```

```
run_sync(
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True
) -> GraphRunResult[StateT, T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

[GraphRunResult](https://ai.pydantic.dev#pydantic_graph.graph.GraphRunResult)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

Synchronously run the graph.

This is a convenience method that wraps self.run with loop.run_until_complete(...).
You therefore can't use this method inside async code or if there's an active event loop.

```
self.run
```

```
loop.run_until_complete(...)
```

Parameters:

```
start_node
```

```
BaseNode[StateT, DepsT, T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

the first node to run, since the graph definition doesn't define the entry point in the graph,
you need to provide the starting node.

```
state
```

```
StateT
```

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The initial state of the graph.

```
None
```

```
deps
```

```
DepsT
```

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

The dependencies of the graph.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to infer the graph name from the calling frame.

```
True
```

Returns:

```
GraphRunResult[StateT, T]
```

[GraphRunResult](https://ai.pydantic.dev#pydantic_graph.graph.GraphRunResult)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The result type from ending the run and the history of the run.

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
def run_sync(
    self: Graph[StateT, DepsT, T],
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
) -> GraphRunResult[StateT, T]:
    """Synchronously run the graph.

    This is a convenience method that wraps [`self.run`][pydantic_graph.Graph.run] with `loop.run_until_complete(...)`.
    You therefore can't use this method inside async code or if there's an active event loop.

    Args:
        start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
            you need to provide the starting node.
        state: The initial state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.

    Returns:
        The result type from ending the run and the history of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    return _utils.get_event_loop().run_until_complete(
        self.run(start_node, state=state, deps=deps, infer_name=False)
    )
```

```
def run_sync(
    self: Graph[StateT, DepsT, T],
    start_node: BaseNode[StateT, DepsT, T],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
) -> GraphRunResult[StateT, T]:
    """Synchronously run the graph.

    This is a convenience method that wraps [`self.run`][pydantic_graph.Graph.run] with `loop.run_until_complete(...)`.
    You therefore can't use this method inside async code or if there's an active event loop.

    Args:
        start_node: the first node to run, since the graph definition doesn't define the entry point in the graph,
            you need to provide the starting node.
        state: The initial state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.

    Returns:
        The result type from ending the run and the history of the run.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    return _utils.get_event_loop().run_until_complete(
        self.run(start_node, state=state, deps=deps, infer_name=False)
    )
```

#### next

async

```
async
```

```
next(
    node: BaseNode[StateT, DepsT, T],
    history: list[HistoryStep[StateT, T]],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True
) -> BaseNode[StateT, DepsT, Any] | End[T]
```

```
next(
    node: BaseNode[StateT, DepsT, T],
    history: list[HistoryStep[StateT, T]],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True
) -> BaseNode[StateT, DepsT, Any] | End[T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

[End](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.End)

Run a node in the graph and return the next node to run.

Parameters:

```
node
```

```
BaseNode[StateT, DepsT, T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

The node to run.

```
history
```

```
list[HistoryStep[StateT, T]]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The history of the graph run so far. NOTE: this will be mutated to add the new step.

```
state
```

```
StateT
```

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The current state of the graph.

```
None
```

```
deps
```

```
DepsT
```

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

The dependencies of the graph.

```
None
```

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to infer the graph name from the calling frame.

```
True
```

Returns:

```
BaseNode[StateT, DepsT, Any] | End[T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

[End](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.End)

The next node to run or End if the graph has finished.

```
End
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
async def next(
    self: Graph[StateT, DepsT, T],
    node: BaseNode[StateT, DepsT, T],
    history: list[HistoryStep[StateT, T]],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
) -> BaseNode[StateT, DepsT, Any] | End[T]:
    """Run a node in the graph and return the next node to run.

    Args:
        node: The node to run.
        history: The history of the graph run so far. NOTE: this will be mutated to add the new step.
        state: The current state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.

    Returns:
        The next node to run or [`End`][pydantic_graph.nodes.End] if the graph has finished.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())

    if isinstance(node, End):
        # While technically this is not compatible with the documented method signature, it's an easy mistake to
        # make, and we should eagerly provide a more helpful error message than you'd get otherwise.
        raise exceptions.GraphRuntimeError(f'Cannot call `next` with an `End` node: {node!r}.')

    node_id = node.get_id()
    if node_id not in self.node_defs:
        raise exceptions.GraphRuntimeError(f'Node `{node}` is not in the graph.')

    with ExitStack() as stack:
        if self._auto_instrument:
            stack.enter_context(_logfire.span('run node {node_id}', node_id=node_id, node=node))
        ctx = GraphRunContext(state, deps)
        start_ts = _utils.now_utc()
        start = perf_counter()
        next_node = await node.run(ctx)
        duration = perf_counter() - start

    history.append(
        NodeStep(state=state, node=node, start_ts=start_ts, duration=duration, snapshot_state=self.snapshot_state)
    )

    if isinstance(next_node, End):
        history.append(EndStep(result=next_node))
    elif not isinstance(next_node, BaseNode):
        if TYPE_CHECKING:
            typing_extensions.assert_never(next_node)
        else:
            raise exceptions.GraphRuntimeError(
                f'Invalid node return type: `{type(next_node).__name__}`. Expected `BaseNode` or `End`.'
            )

    return next_node
```

```
async def next(
    self: Graph[StateT, DepsT, T],
    node: BaseNode[StateT, DepsT, T],
    history: list[HistoryStep[StateT, T]],
    *,
    state: StateT = None,
    deps: DepsT = None,
    infer_name: bool = True,
) -> BaseNode[StateT, DepsT, Any] | End[T]:
    """Run a node in the graph and return the next node to run.

    Args:
        node: The node to run.
        history: The history of the graph run so far. NOTE: this will be mutated to add the new step.
        state: The current state of the graph.
        deps: The dependencies of the graph.
        infer_name: Whether to infer the graph name from the calling frame.

    Returns:
        The next node to run or [`End`][pydantic_graph.nodes.End] if the graph has finished.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())

    if isinstance(node, End):
        # While technically this is not compatible with the documented method signature, it's an easy mistake to
        # make, and we should eagerly provide a more helpful error message than you'd get otherwise.
        raise exceptions.GraphRuntimeError(f'Cannot call `next` with an `End` node: {node!r}.')

    node_id = node.get_id()
    if node_id not in self.node_defs:
        raise exceptions.GraphRuntimeError(f'Node `{node}` is not in the graph.')

    with ExitStack() as stack:
        if self._auto_instrument:
            stack.enter_context(_logfire.span('run node {node_id}', node_id=node_id, node=node))
        ctx = GraphRunContext(state, deps)
        start_ts = _utils.now_utc()
        start = perf_counter()
        next_node = await node.run(ctx)
        duration = perf_counter() - start

    history.append(
        NodeStep(state=state, node=node, start_ts=start_ts, duration=duration, snapshot_state=self.snapshot_state)
    )

    if isinstance(next_node, End):
        history.append(EndStep(result=next_node))
    elif not isinstance(next_node, BaseNode):
        if TYPE_CHECKING:
            typing_extensions.assert_never(next_node)
        else:
            raise exceptions.GraphRuntimeError(
                f'Invalid node return type: `{type(next_node).__name__}`. Expected `BaseNode` or `End`.'
            )

    return next_node
```

#### dump_history

```
dump_history(
    history: list[HistoryStep[StateT, T]],
    *,
    indent: int | None = None
) -> bytes
```

```
dump_history(
    history: list[HistoryStep[StateT, T]],
    *,
    indent: int | None = None
) -> bytes
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[int](https://docs.python.org/3/library/functions.html#int)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

Dump the history of a graph run as JSON.

Parameters:

```
history
```

```
list[HistoryStep[StateT, T]]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

The history of the graph run.

```
indent
```

```
int | None
```

[int](https://docs.python.org/3/library/functions.html#int)

The number of spaces to indent the JSON.

```
None
```

Returns:

```
bytes
```

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

The JSON representation of the history.

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
def dump_history(
    self: Graph[StateT, DepsT, T], history: list[HistoryStep[StateT, T]], *, indent: int | None = None
) -> bytes:
    """Dump the history of a graph run as JSON.

    Args:
        history: The history of the graph run.
        indent: The number of spaces to indent the JSON.

    Returns:
        The JSON representation of the history.
    """
    return self.history_type_adapter.dump_json(history, indent=indent)
```

```
def dump_history(
    self: Graph[StateT, DepsT, T], history: list[HistoryStep[StateT, T]], *, indent: int | None = None
) -> bytes:
    """Dump the history of a graph run as JSON.

    Args:
        history: The history of the graph run.
        indent: The number of spaces to indent the JSON.

    Returns:
        The JSON representation of the history.
    """
    return self.history_type_adapter.dump_json(history, indent=indent)
```

#### load_history

```
load_history(
    json_bytes: str | bytes | bytearray,
) -> list[HistoryStep[StateT, RunEndT]]
```

```
load_history(
    json_bytes: str | bytes | bytearray,
) -> list[HistoryStep[StateT, RunEndT]]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

[bytearray](https://docs.python.org/3/library/stdtypes.html#bytearray)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

Load the history of a graph run from JSON.

Parameters:

```
json_bytes
```

```
str | bytes | bytearray
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

[bytearray](https://docs.python.org/3/library/stdtypes.html#bytearray)

The JSON representation of the history.

Returns:

```
list[HistoryStep[StateT, RunEndT]]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The history of the graph run.

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
def load_history(self, json_bytes: str | bytes | bytearray) -> list[HistoryStep[StateT, RunEndT]]:
    """Load the history of a graph run from JSON.

    Args:
        json_bytes: The JSON representation of the history.

    Returns:
        The history of the graph run.
    """
    return self.history_type_adapter.validate_json(json_bytes)
```

```
def load_history(self, json_bytes: str | bytes | bytearray) -> list[HistoryStep[StateT, RunEndT]]:
    """Load the history of a graph run from JSON.

    Args:
        json_bytes: The JSON representation of the history.

    Returns:
        The history of the graph run.
    """
    return self.history_type_adapter.validate_json(json_bytes)
```

#### mermaid_code

```
mermaid_code(
    *,
    start_node: (
        Sequence[NodeIdent] | NodeIdent | None
    ) = None,
    title: str | None | Literal[False] = None,
    edge_labels: bool = True,
    notes: bool = True,
    highlighted_nodes: (
        Sequence[NodeIdent] | NodeIdent | None
    ) = None,
    highlight_css: str = DEFAULT_HIGHLIGHT_CSS,
    infer_name: bool = True,
    direction: StateDiagramDirection | None = None
) -> str
```

```
mermaid_code(
    *,
    start_node: (
        Sequence[NodeIdent] | NodeIdent | None
    ) = None,
    title: str | None | Literal[False] = None,
    edge_labels: bool = True,
    notes: bool = True,
    highlighted_nodes: (
        Sequence[NodeIdent] | NodeIdent | None
    ) = None,
    highlight_css: str = DEFAULT_HIGHLIGHT_CSS,
    infer_name: bool = True,
    direction: StateDiagramDirection | None = None
) -> str
```

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Literal](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Literal)

[bool](https://docs.python.org/3/library/functions.html#bool)

[bool](https://docs.python.org/3/library/functions.html#bool)

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[DEFAULT_HIGHLIGHT_CSS](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.DEFAULT_HIGHLIGHT_CSS)

[bool](https://docs.python.org/3/library/functions.html#bool)

[StateDiagramDirection](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.StateDiagramDirection)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Generate a diagram representing the graph as mermaid diagram.

This method calls pydantic_graph.mermaid.generate_code.

```
pydantic_graph.mermaid.generate_code
```

Parameters:

```
start_node
```

```
Sequence[NodeIdent] | NodeIdent | None
```

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

The node or nodes which can start the graph.

```
None
```

```
title
```

```
str | None | Literal[False]
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

[Literal](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Literal)

The title of the diagram, use False to not include a title.

```
False
```

```
None
```

```
edge_labels
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to include edge labels.

```
True
```

```
notes
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to include notes on each node.

```
True
```

```
highlighted_nodes
```

```
Sequence[NodeIdent] | NodeIdent | None
```

[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

[NodeIdent](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.NodeIdent)

Optional node or nodes to highlight.

```
None
```

```
highlight_css
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The CSS to use for highlighting nodes.

```
DEFAULT_HIGHLIGHT_CSS
```

[DEFAULT_HIGHLIGHT_CSS](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.DEFAULT_HIGHLIGHT_CSS)

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to infer the graph name from the calling frame.

```
True
```

```
direction
```

```
StateDiagramDirection | None
```

[StateDiagramDirection](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.StateDiagramDirection)

The direction of flow.

```
None
```

Returns:

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The mermaid code for the graph, which can then be rendered as a diagram.

Here's an example of generating a diagram for the graph from above:

```
from never_42 import Increment, never_42_graph

print(never_42_graph.mermaid_code(start_node=Increment))
'''
---
title: never_42_graph
---
stateDiagram-v2
  [*] --> Increment
  Increment --> Check42
  Check42 --> Increment
  Check42 --> [*]
'''
```

```
from never_42 import Increment, never_42_graph

print(never_42_graph.mermaid_code(start_node=Increment))
'''
---
title: never_42_graph
---
stateDiagram-v2
  [*] --> Increment
  Increment --> Check42
  Check42 --> Increment
  Check42 --> [*]
'''
```

The rendered diagram will look like this:

```
---
title: never_42_graph
---
stateDiagram-v2
  [*] --> Increment
  Increment --> Check42
  Check42 --> Increment
  Check42 --> [*]
```

```
---
title: never_42_graph
---
stateDiagram-v2
  [*] --> Increment
  Increment --> Check42
  Check42 --> Increment
  Check42 --> [*]
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
def mermaid_code(
    self,
    *,
    start_node: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
    title: str | None | typing_extensions.Literal[False] = None,
    edge_labels: bool = True,
    notes: bool = True,
    highlighted_nodes: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
    highlight_css: str = mermaid.DEFAULT_HIGHLIGHT_CSS,
    infer_name: bool = True,
    direction: mermaid.StateDiagramDirection | None = None,
) -> str:
    """Generate a diagram representing the graph as [mermaid](https://mermaid.js.org/) diagram.

    This method calls [`pydantic_graph.mermaid.generate_code`][pydantic_graph.mermaid.generate_code].

    Args:
        start_node: The node or nodes which can start the graph.
        title: The title of the diagram, use `False` to not include a title.
        edge_labels: Whether to include edge labels.
        notes: Whether to include notes on each node.
        highlighted_nodes: Optional node or nodes to highlight.
        highlight_css: The CSS to use for highlighting nodes.
        infer_name: Whether to infer the graph name from the calling frame.
        direction: The direction of flow.

    Returns:
        The mermaid code for the graph, which can then be rendered as a diagram.

    Here's an example of generating a diagram for the graph from [above][pydantic_graph.graph.Graph]:

    ```py {title="mermaid_never_42.py" py="3.10"}
    from never_42 import Increment, never_42_graph

    print(never_42_graph.mermaid_code(start_node=Increment))
    '''
    ---
    title: never_42_graph
    ---
    stateDiagram-v2
      [*] --> Increment
      Increment --> Check42
      Check42 --> Increment
      Check42 --> [*]
    '''
    ```

    The rendered diagram will look like this:

    ```mermaid
    ---
    title: never_42_graph
    ---
    stateDiagram-v2
      [*] --> Increment
      Increment --> Check42
      Check42 --> Increment
      Check42 --> [*]
    ```
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    if title is None and self.name:
        title = self.name
    return mermaid.generate_code(
        self,
        start_node=start_node,
        highlighted_nodes=highlighted_nodes,
        highlight_css=highlight_css,
        title=title or None,
        edge_labels=edge_labels,
        notes=notes,
        direction=direction,
    )
```

```
def mermaid_code(
    self,
    *,
    start_node: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
    title: str | None | typing_extensions.Literal[False] = None,
    edge_labels: bool = True,
    notes: bool = True,
    highlighted_nodes: Sequence[mermaid.NodeIdent] | mermaid.NodeIdent | None = None,
    highlight_css: str = mermaid.DEFAULT_HIGHLIGHT_CSS,
    infer_name: bool = True,
    direction: mermaid.StateDiagramDirection | None = None,
) -> str:
    """Generate a diagram representing the graph as [mermaid](https://mermaid.js.org/) diagram.

    This method calls [`pydantic_graph.mermaid.generate_code`][pydantic_graph.mermaid.generate_code].

    Args:
        start_node: The node or nodes which can start the graph.
        title: The title of the diagram, use `False` to not include a title.
        edge_labels: Whether to include edge labels.
        notes: Whether to include notes on each node.
        highlighted_nodes: Optional node or nodes to highlight.
        highlight_css: The CSS to use for highlighting nodes.
        infer_name: Whether to infer the graph name from the calling frame.
        direction: The direction of flow.

    Returns:
        The mermaid code for the graph, which can then be rendered as a diagram.

    Here's an example of generating a diagram for the graph from [above][pydantic_graph.graph.Graph]:

    ```py {title="mermaid_never_42.py" py="3.10"}
    from never_42 import Increment, never_42_graph

    print(never_42_graph.mermaid_code(start_node=Increment))
    '''
    ---
    title: never_42_graph
    ---
    stateDiagram-v2
      [*] --> Increment
      Increment --> Check42
      Check42 --> Increment
      Check42 --> [*]
    '''
    ```

    The rendered diagram will look like this:

    ```mermaid
    ---
    title: never_42_graph
    ---
    stateDiagram-v2
      [*] --> Increment
      Increment --> Check42
      Check42 --> Increment
      Check42 --> [*]
    ```
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    if title is None and self.name:
        title = self.name
    return mermaid.generate_code(
        self,
        start_node=start_node,
        highlighted_nodes=highlighted_nodes,
        highlight_css=highlight_css,
        title=title or None,
        edge_labels=edge_labels,
        notes=notes,
        direction=direction,
    )
```

#### mermaid_image

```
mermaid_image(
    infer_name: bool = True, **kwargs: Unpack[MermaidConfig]
) -> bytes
```

```
mermaid_image(
    infer_name: bool = True, **kwargs: Unpack[MermaidConfig]
) -> bytes
```

[bool](https://docs.python.org/3/library/functions.html#bool)

[Unpack](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Unpack)

[MermaidConfig](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.MermaidConfig)

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

Generate a diagram representing the graph as an image.

The format and diagram can be customized using kwargs,
see pydantic_graph.mermaid.MermaidConfig.

```
kwargs
```

```
pydantic_graph.mermaid.MermaidConfig
```

Uses external service

This method makes a request to mermaid.ink to render the image, mermaid.ink
is a free service not affiliated with Pydantic.

```
mermaid.ink
```

Parameters:

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to infer the graph name from the calling frame.

```
True
```

```
**kwargs
```

```
Unpack[MermaidConfig]
```

[Unpack](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Unpack)

[MermaidConfig](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.MermaidConfig)

Additional arguments to pass to mermaid.request_image.

```
mermaid.request_image
```

```
{}
```

Returns:

```
bytes
```

[bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

The image bytes.

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
def mermaid_image(
    self, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
) -> bytes:
    """Generate a diagram representing the graph as an image.

    The format and diagram can be customized using `kwargs`,
    see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

    !!! note "Uses external service"
        This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
        is a free service not affiliated with Pydantic.

    Args:
        infer_name: Whether to infer the graph name from the calling frame.
        **kwargs: Additional arguments to pass to `mermaid.request_image`.

    Returns:
        The image bytes.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    if 'title' not in kwargs and self.name:
        kwargs['title'] = self.name
    return mermaid.request_image(self, **kwargs)
```

```
def mermaid_image(
    self, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
) -> bytes:
    """Generate a diagram representing the graph as an image.

    The format and diagram can be customized using `kwargs`,
    see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

    !!! note "Uses external service"
        This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
        is a free service not affiliated with Pydantic.

    Args:
        infer_name: Whether to infer the graph name from the calling frame.
        **kwargs: Additional arguments to pass to `mermaid.request_image`.

    Returns:
        The image bytes.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    if 'title' not in kwargs and self.name:
        kwargs['title'] = self.name
    return mermaid.request_image(self, **kwargs)
```

#### mermaid_save

```
mermaid_save(
    path: Path | str,
    /,
    *,
    infer_name: bool = True,
    **kwargs: Unpack[MermaidConfig],
) -> None
```

```
mermaid_save(
    path: Path | str,
    /,
    *,
    infer_name: bool = True,
    **kwargs: Unpack[MermaidConfig],
) -> None
```

[Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bool](https://docs.python.org/3/library/functions.html#bool)

[Unpack](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Unpack)

[MermaidConfig](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.MermaidConfig)

Generate a diagram representing the graph and save it as an image.

The format and diagram can be customized using kwargs,
see pydantic_graph.mermaid.MermaidConfig.

```
kwargs
```

```
pydantic_graph.mermaid.MermaidConfig
```

Uses external service

This method makes a request to mermaid.ink to render the image, mermaid.ink
is a free service not affiliated with Pydantic.

```
mermaid.ink
```

Parameters:

```
path
```

```
Path | str
```

[Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)

[str](https://docs.python.org/3/library/stdtypes.html#str)

The path to save the image to.

```
infer_name
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to infer the graph name from the calling frame.

```
True
```

```
**kwargs
```

```
Unpack[MermaidConfig]
```

[Unpack](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Unpack)

[MermaidConfig](https://ai.pydantic.dev/mermaid/#pydantic_graph.mermaid.MermaidConfig)

Additional arguments to pass to mermaid.save_image.

```
mermaid.save_image
```

```
{}
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
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
```

```
def mermaid_save(
    self, path: Path | str, /, *, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
) -> None:
    """Generate a diagram representing the graph and save it as an image.

    The format and diagram can be customized using `kwargs`,
    see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

    !!! note "Uses external service"
        This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
        is a free service not affiliated with Pydantic.

    Args:
        path: The path to save the image to.
        infer_name: Whether to infer the graph name from the calling frame.
        **kwargs: Additional arguments to pass to `mermaid.save_image`.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    if 'title' not in kwargs and self.name:
        kwargs['title'] = self.name
    mermaid.save_image(path, self, **kwargs)
```

```
def mermaid_save(
    self, path: Path | str, /, *, infer_name: bool = True, **kwargs: typing_extensions.Unpack[mermaid.MermaidConfig]
) -> None:
    """Generate a diagram representing the graph and save it as an image.

    The format and diagram can be customized using `kwargs`,
    see [`pydantic_graph.mermaid.MermaidConfig`][pydantic_graph.mermaid.MermaidConfig].

    !!! note "Uses external service"
        This method makes a request to [mermaid.ink](https://mermaid.ink) to render the image, `mermaid.ink`
        is a free service not affiliated with Pydantic.

    Args:
        path: The path to save the image to.
        infer_name: Whether to infer the graph name from the calling frame.
        **kwargs: Additional arguments to pass to `mermaid.save_image`.
    """
    if infer_name and self.name is None:
        self._infer_name(inspect.currentframe())
    if 'title' not in kwargs and self.name:
        kwargs['title'] = self.name
    mermaid.save_image(path, self, **kwargs)
```

### GraphRun

Bases: Generic[StateT, DepsT, RunEndT]

```
Generic[StateT, DepsT, RunEndT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

A stateful, async-iterable run of a Graph.

```
Graph
```

You typically get a GraphRun instance from calling
async with [my_graph.iter(...)][pydantic_graph.graph.Graph.iter] as graph_run:. That gives you the ability to iterate
through nodes as they run, either by async for iteration or by repeatedly calling .next(...).

```
GraphRun
```

```
async with [my_graph.iter(...)][pydantic_graph.graph.Graph.iter] as graph_run:
```

```
async for
```

```
.next(...)
```

Here's an example of iterating over the graph from above:
iter_never_42.pyfrom copy import deepcopy
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(1)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
        async for node in graph_run:
            node_states.append((node, deepcopy(graph_run.state)))
        print(node_states)
        '''
        [
            (Increment(), MyState(number=1)),
            (Check42(), MyState(number=2)),
            (End(data=2), MyState(number=2)),
        ]
        '''

    state = MyState(41)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
        async for node in graph_run:
            node_states.append((node, deepcopy(graph_run.state)))
        print(node_states)
        '''
        [
            (Increment(), MyState(number=41)),
            (Check42(), MyState(number=42)),
            (Increment(), MyState(number=42)),
            (Check42(), MyState(number=43)),
            (End(data=43), MyState(number=43)),
        ]
        '''

```
from copy import deepcopy
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(1)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
        async for node in graph_run:
            node_states.append((node, deepcopy(graph_run.state)))
        print(node_states)
        '''
        [
            (Increment(), MyState(number=1)),
            (Check42(), MyState(number=2)),
            (End(data=2), MyState(number=2)),
        ]
        '''

    state = MyState(41)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
        async for node in graph_run:
            node_states.append((node, deepcopy(graph_run.state)))
        print(node_states)
        '''
        [
            (Increment(), MyState(number=41)),
            (Check42(), MyState(number=42)),
            (Increment(), MyState(number=42)),
            (Check42(), MyState(number=43)),
            (End(data=43), MyState(number=43)),
        ]
        '''
```

```
from copy import deepcopy
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(1)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
        async for node in graph_run:
            node_states.append((node, deepcopy(graph_run.state)))
        print(node_states)
        '''
        [
            (Increment(), MyState(number=1)),
            (Check42(), MyState(number=2)),
            (End(data=2), MyState(number=2)),
        ]
        '''

    state = MyState(41)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
        async for node in graph_run:
            node_states.append((node, deepcopy(graph_run.state)))
        print(node_states)
        '''
        [
            (Increment(), MyState(number=41)),
            (Check42(), MyState(number=42)),
            (Increment(), MyState(number=42)),
            (Check42(), MyState(number=43)),
            (End(data=43), MyState(number=43)),
        ]
        '''
```

See the GraphRun.next documentation for an example of how to manually
drive the graph run.

```
GraphRun.next
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
```

```
class GraphRun(Generic[StateT, DepsT, RunEndT]):
    """A stateful, async-iterable run of a [`Graph`][pydantic_graph.graph.Graph].

    You typically get a `GraphRun` instance from calling
    `async with [my_graph.iter(...)][pydantic_graph.graph.Graph.iter] as graph_run:`. That gives you the ability to iterate
    through nodes as they run, either by `async for` iteration or by repeatedly calling `.next(...)`.

    Here's an example of iterating over the graph from [above][pydantic_graph.graph.Graph]:
    ```py {title="iter_never_42.py" noqa="I001" py="3.10"}
    from copy import deepcopy
    from never_42 import Increment, MyState, never_42_graph

    async def main():
        state = MyState(1)
        async with never_42_graph.iter(Increment(), state=state) as graph_run:
            node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
            async for node in graph_run:
                node_states.append((node, deepcopy(graph_run.state)))
            print(node_states)
            '''
            [
                (Increment(), MyState(number=1)),
                (Check42(), MyState(number=2)),
                (End(data=2), MyState(number=2)),
            ]
            '''

        state = MyState(41)
        async with never_42_graph.iter(Increment(), state=state) as graph_run:
            node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
            async for node in graph_run:
                node_states.append((node, deepcopy(graph_run.state)))
            print(node_states)
            '''
            [
                (Increment(), MyState(number=41)),
                (Check42(), MyState(number=42)),
                (Increment(), MyState(number=42)),
                (Check42(), MyState(number=43)),
                (End(data=43), MyState(number=43)),
            ]
            '''
    ```

    See the [`GraphRun.next` documentation][pydantic_graph.graph.GraphRun.next] for an example of how to manually
    drive the graph run.
    """

    def __init__(
        self,
        graph: Graph[StateT, DepsT, RunEndT],
        start_node: BaseNode[StateT, DepsT, RunEndT],
        *,
        history: list[HistoryStep[StateT, RunEndT]],
        state: StateT,
        deps: DepsT,
        auto_instrument: bool,
    ):
        """Create a new run for a given graph, starting at the specified node.

        Typically, you'll use [`Graph.iter`][pydantic_graph.graph.Graph.iter] rather than calling this directly.

        Args:
            graph: The [`Graph`][pydantic_graph.graph.Graph] to run.
            start_node: The node where execution will begin.
            history: A list of [`HistoryStep`][pydantic_graph.state.HistoryStep] objects that describe
                each step of the run. Usually starts empty; can be populated if resuming.
            state: A shared state object or primitive (like a counter, dataclass, etc.) that is available
                to all nodes via `ctx.state`.
            deps: Optional dependencies that each node can access via `ctx.deps`, e.g. database connections,
                configuration, or logging clients.
            auto_instrument: Whether to automatically create instrumentation spans during the run.
        """
        self.graph = graph
        self.history = history
        self.state = state
        self.deps = deps
        self._auto_instrument = auto_instrument

        self._next_node: BaseNode[StateT, DepsT, RunEndT] | End[RunEndT] = start_node

    @property
    def next_node(self) -> BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]:
        """The next node that will be run in the graph.

        This is the next node that will be used during async iteration, or if a node is not passed to `self.next(...)`.
        """
        return self._next_node

    @property
    def result(self) -> GraphRunResult[StateT, RunEndT] | None:
        """The final result of the graph run if the run is completed, otherwise `None`."""
        if not isinstance(self._next_node, End):
            return None  # The GraphRun has not finished running
        return GraphRunResult(
            self._next_node.data,
            state=self.state,
            history=self.history,
        )

    async def next(
        self: GraphRun[StateT, DepsT, T], node: BaseNode[StateT, DepsT, T] | None = None
    ) -> BaseNode[StateT, DepsT, T] | End[T]:
        """Manually drive the graph run by passing in the node you want to run next.

        This lets you inspect or mutate the node before continuing execution, or skip certain nodes
        under dynamic conditions. The graph run should stop when you return an [`End`][pydantic_graph.nodes.End] node.

        Here's an example of using `next` to drive the graph from [above][pydantic_graph.graph.Graph]:
        ```py {title="next_never_42.py" noqa="I001" py="3.10"}
        from copy import deepcopy
        from pydantic_graph import End
        from never_42 import Increment, MyState, never_42_graph

        async def main():
            state = MyState(48)
            async with never_42_graph.iter(Increment(), state=state) as graph_run:
                next_node = graph_run.next_node  # start with the first node
                node_states = [(next_node, deepcopy(graph_run.state))]

                while not isinstance(next_node, End):
                    if graph_run.state.number == 50:
                        graph_run.state.number = 42
                    next_node = await graph_run.next(next_node)
                    node_states.append((next_node, deepcopy(graph_run.state)))

                print(node_states)
                '''
                [
                    (Increment(), MyState(number=48)),
                    (Check42(), MyState(number=49)),
                    (End(data=49), MyState(number=49)),
                ]
                '''
        ```

        Args:
            node: The node to run next in the graph. If not specified, uses `self.next_node`, which is initialized to
                the `start_node` of the run and updated each time a new node is returned.

        Returns:
            The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
            the run has completed.
        """
        if node is None:
            if isinstance(self._next_node, End):
                # Note: we could alternatively just return `self._next_node` here, but it's easier to start with an
                # error and relax the behavior later, than vice versa.
                raise exceptions.GraphRuntimeError('This graph run has already ended.')
            node = self._next_node

        history = self.history
        state = self.state
        deps = self.deps

        self._next_node = await self.graph.next(node, history, state=state, deps=deps, infer_name=False)

        return self._next_node

    def __aiter__(self) -> AsyncIterator[BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]]:
        return self

    async def __anext__(self) -> BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]:
        """Use the last returned node as the input to `Graph.next`."""
        if isinstance(self._next_node, End):
            raise StopAsyncIteration
        return await self.next(self._next_node)

    def __repr__(self) -> str:
        return f'<GraphRun name={self.graph.name or "<unnamed>"} step={len(self.history) + 1}>'
```

```
class GraphRun(Generic[StateT, DepsT, RunEndT]):
    """A stateful, async-iterable run of a [`Graph`][pydantic_graph.graph.Graph].

    You typically get a `GraphRun` instance from calling
    `async with [my_graph.iter(...)][pydantic_graph.graph.Graph.iter] as graph_run:`. That gives you the ability to iterate
    through nodes as they run, either by `async for` iteration or by repeatedly calling `.next(...)`.

    Here's an example of iterating over the graph from [above][pydantic_graph.graph.Graph]:
    ```py {title="iter_never_42.py" noqa="I001" py="3.10"}
    from copy import deepcopy
    from never_42 import Increment, MyState, never_42_graph

    async def main():
        state = MyState(1)
        async with never_42_graph.iter(Increment(), state=state) as graph_run:
            node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
            async for node in graph_run:
                node_states.append((node, deepcopy(graph_run.state)))
            print(node_states)
            '''
            [
                (Increment(), MyState(number=1)),
                (Check42(), MyState(number=2)),
                (End(data=2), MyState(number=2)),
            ]
            '''

        state = MyState(41)
        async with never_42_graph.iter(Increment(), state=state) as graph_run:
            node_states = [(graph_run.next_node, deepcopy(graph_run.state))]
            async for node in graph_run:
                node_states.append((node, deepcopy(graph_run.state)))
            print(node_states)
            '''
            [
                (Increment(), MyState(number=41)),
                (Check42(), MyState(number=42)),
                (Increment(), MyState(number=42)),
                (Check42(), MyState(number=43)),
                (End(data=43), MyState(number=43)),
            ]
            '''
    ```

    See the [`GraphRun.next` documentation][pydantic_graph.graph.GraphRun.next] for an example of how to manually
    drive the graph run.
    """

    def __init__(
        self,
        graph: Graph[StateT, DepsT, RunEndT],
        start_node: BaseNode[StateT, DepsT, RunEndT],
        *,
        history: list[HistoryStep[StateT, RunEndT]],
        state: StateT,
        deps: DepsT,
        auto_instrument: bool,
    ):
        """Create a new run for a given graph, starting at the specified node.

        Typically, you'll use [`Graph.iter`][pydantic_graph.graph.Graph.iter] rather than calling this directly.

        Args:
            graph: The [`Graph`][pydantic_graph.graph.Graph] to run.
            start_node: The node where execution will begin.
            history: A list of [`HistoryStep`][pydantic_graph.state.HistoryStep] objects that describe
                each step of the run. Usually starts empty; can be populated if resuming.
            state: A shared state object or primitive (like a counter, dataclass, etc.) that is available
                to all nodes via `ctx.state`.
            deps: Optional dependencies that each node can access via `ctx.deps`, e.g. database connections,
                configuration, or logging clients.
            auto_instrument: Whether to automatically create instrumentation spans during the run.
        """
        self.graph = graph
        self.history = history
        self.state = state
        self.deps = deps
        self._auto_instrument = auto_instrument

        self._next_node: BaseNode[StateT, DepsT, RunEndT] | End[RunEndT] = start_node

    @property
    def next_node(self) -> BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]:
        """The next node that will be run in the graph.

        This is the next node that will be used during async iteration, or if a node is not passed to `self.next(...)`.
        """
        return self._next_node

    @property
    def result(self) -> GraphRunResult[StateT, RunEndT] | None:
        """The final result of the graph run if the run is completed, otherwise `None`."""
        if not isinstance(self._next_node, End):
            return None  # The GraphRun has not finished running
        return GraphRunResult(
            self._next_node.data,
            state=self.state,
            history=self.history,
        )

    async def next(
        self: GraphRun[StateT, DepsT, T], node: BaseNode[StateT, DepsT, T] | None = None
    ) -> BaseNode[StateT, DepsT, T] | End[T]:
        """Manually drive the graph run by passing in the node you want to run next.

        This lets you inspect or mutate the node before continuing execution, or skip certain nodes
        under dynamic conditions. The graph run should stop when you return an [`End`][pydantic_graph.nodes.End] node.

        Here's an example of using `next` to drive the graph from [above][pydantic_graph.graph.Graph]:
        ```py {title="next_never_42.py" noqa="I001" py="3.10"}
        from copy import deepcopy
        from pydantic_graph import End
        from never_42 import Increment, MyState, never_42_graph

        async def main():
            state = MyState(48)
            async with never_42_graph.iter(Increment(), state=state) as graph_run:
                next_node = graph_run.next_node  # start with the first node
                node_states = [(next_node, deepcopy(graph_run.state))]

                while not isinstance(next_node, End):
                    if graph_run.state.number == 50:
                        graph_run.state.number = 42
                    next_node = await graph_run.next(next_node)
                    node_states.append((next_node, deepcopy(graph_run.state)))

                print(node_states)
                '''
                [
                    (Increment(), MyState(number=48)),
                    (Check42(), MyState(number=49)),
                    (End(data=49), MyState(number=49)),
                ]
                '''
        ```

        Args:
            node: The node to run next in the graph. If not specified, uses `self.next_node`, which is initialized to
                the `start_node` of the run and updated each time a new node is returned.

        Returns:
            The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
            the run has completed.
        """
        if node is None:
            if isinstance(self._next_node, End):
                # Note: we could alternatively just return `self._next_node` here, but it's easier to start with an
                # error and relax the behavior later, than vice versa.
                raise exceptions.GraphRuntimeError('This graph run has already ended.')
            node = self._next_node

        history = self.history
        state = self.state
        deps = self.deps

        self._next_node = await self.graph.next(node, history, state=state, deps=deps, infer_name=False)

        return self._next_node

    def __aiter__(self) -> AsyncIterator[BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]]:
        return self

    async def __anext__(self) -> BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]:
        """Use the last returned node as the input to `Graph.next`."""
        if isinstance(self._next_node, End):
            raise StopAsyncIteration
        return await self.next(self._next_node)

    def __repr__(self) -> str:
        return f'<GraphRun name={self.graph.name or "<unnamed>"} step={len(self.history) + 1}>'
```

#### __init__

```
__init__(
    graph: Graph[StateT, DepsT, RunEndT],
    start_node: BaseNode[StateT, DepsT, RunEndT],
    *,
    history: list[HistoryStep[StateT, RunEndT]],
    state: StateT,
    deps: DepsT,
    auto_instrument: bool
)
```

```
__init__(
    graph: Graph[StateT, DepsT, RunEndT],
    start_node: BaseNode[StateT, DepsT, RunEndT],
    *,
    history: list[HistoryStep[StateT, RunEndT]],
    state: StateT,
    deps: DepsT,
    auto_instrument: bool
)
```

[Graph](https://ai.pydantic.dev#pydantic_graph.graph.Graph)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[bool](https://docs.python.org/3/library/functions.html#bool)

Create a new run for a given graph, starting at the specified node.

Typically, you'll use Graph.iter rather than calling this directly.

```
Graph.iter
```

Parameters:

```
graph
```

```
Graph[StateT, DepsT, RunEndT]
```

[Graph](https://ai.pydantic.dev#pydantic_graph.graph.Graph)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The Graph to run.

```
Graph
```

```
start_node
```

```
BaseNode[StateT, DepsT, RunEndT]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The node where execution will begin.

```
history
```

```
list[HistoryStep[StateT, RunEndT]]
```

[list](https://docs.python.org/3/library/stdtypes.html#list)

[HistoryStep](https://ai.pydantic.dev/state/#pydantic_graph.state.HistoryStep)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

A list of HistoryStep objects that describe
each step of the run. Usually starts empty; can be populated if resuming.

```
HistoryStep
```

```
state
```

```
StateT
```

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

A shared state object or primitive (like a counter, dataclass, etc.) that is available
to all nodes via ctx.state.

```
ctx.state
```

```
deps
```

```
DepsT
```

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

Optional dependencies that each node can access via ctx.deps, e.g. database connections,
configuration, or logging clients.

```
ctx.deps
```

```
auto_instrument
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to automatically create instrumentation spans during the run.

```
pydantic_graph/pydantic_graph/graph.py
```

```
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
```

```
def __init__(
    self,
    graph: Graph[StateT, DepsT, RunEndT],
    start_node: BaseNode[StateT, DepsT, RunEndT],
    *,
    history: list[HistoryStep[StateT, RunEndT]],
    state: StateT,
    deps: DepsT,
    auto_instrument: bool,
):
    """Create a new run for a given graph, starting at the specified node.

    Typically, you'll use [`Graph.iter`][pydantic_graph.graph.Graph.iter] rather than calling this directly.

    Args:
        graph: The [`Graph`][pydantic_graph.graph.Graph] to run.
        start_node: The node where execution will begin.
        history: A list of [`HistoryStep`][pydantic_graph.state.HistoryStep] objects that describe
            each step of the run. Usually starts empty; can be populated if resuming.
        state: A shared state object or primitive (like a counter, dataclass, etc.) that is available
            to all nodes via `ctx.state`.
        deps: Optional dependencies that each node can access via `ctx.deps`, e.g. database connections,
            configuration, or logging clients.
        auto_instrument: Whether to automatically create instrumentation spans during the run.
    """
    self.graph = graph
    self.history = history
    self.state = state
    self.deps = deps
    self._auto_instrument = auto_instrument

    self._next_node: BaseNode[StateT, DepsT, RunEndT] | End[RunEndT] = start_node
```

```
def __init__(
    self,
    graph: Graph[StateT, DepsT, RunEndT],
    start_node: BaseNode[StateT, DepsT, RunEndT],
    *,
    history: list[HistoryStep[StateT, RunEndT]],
    state: StateT,
    deps: DepsT,
    auto_instrument: bool,
):
    """Create a new run for a given graph, starting at the specified node.

    Typically, you'll use [`Graph.iter`][pydantic_graph.graph.Graph.iter] rather than calling this directly.

    Args:
        graph: The [`Graph`][pydantic_graph.graph.Graph] to run.
        start_node: The node where execution will begin.
        history: A list of [`HistoryStep`][pydantic_graph.state.HistoryStep] objects that describe
            each step of the run. Usually starts empty; can be populated if resuming.
        state: A shared state object or primitive (like a counter, dataclass, etc.) that is available
            to all nodes via `ctx.state`.
        deps: Optional dependencies that each node can access via `ctx.deps`, e.g. database connections,
            configuration, or logging clients.
        auto_instrument: Whether to automatically create instrumentation spans during the run.
    """
    self.graph = graph
    self.history = history
    self.state = state
    self.deps = deps
    self._auto_instrument = auto_instrument

    self._next_node: BaseNode[StateT, DepsT, RunEndT] | End[RunEndT] = start_node
```

#### next_node

property

```
property
```

```
next_node: BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]
```

```
next_node: BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

[End](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.End)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The next node that will be run in the graph.

This is the next node that will be used during async iteration, or if a node is not passed to self.next(...).

```
self.next(...)
```

#### result

property

```
property
```

```
result: GraphRunResult[StateT, RunEndT] | None
```

```
result: GraphRunResult[StateT, RunEndT] | None
```

[GraphRunResult](https://ai.pydantic.dev#pydantic_graph.graph.GraphRunResult)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The final result of the graph run if the run is completed, otherwise None.

```
None
```

#### next

async

```
async
```

```
next(
    node: BaseNode[StateT, DepsT, T] | None = None,
) -> BaseNode[StateT, DepsT, T] | End[T]
```

```
next(
    node: BaseNode[StateT, DepsT, T] | None = None,
) -> BaseNode[StateT, DepsT, T] | End[T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[End](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.End)

Manually drive the graph run by passing in the node you want to run next.

This lets you inspect or mutate the node before continuing execution, or skip certain nodes
under dynamic conditions. The graph run should stop when you return an End node.

```
End
```

Here's an example of using next to drive the graph from above:
next_never_42.pyfrom copy import deepcopy
from pydantic_graph import End
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(48)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        next_node = graph_run.next_node  # start with the first node
        node_states = [(next_node, deepcopy(graph_run.state))]

        while not isinstance(next_node, End):
            if graph_run.state.number == 50:
                graph_run.state.number = 42
            next_node = await graph_run.next(next_node)
            node_states.append((next_node, deepcopy(graph_run.state)))

        print(node_states)
        '''
        [
            (Increment(), MyState(number=48)),
            (Check42(), MyState(number=49)),
            (End(data=49), MyState(number=49)),
        ]
        '''

```
next
```

```
from copy import deepcopy
from pydantic_graph import End
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(48)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        next_node = graph_run.next_node  # start with the first node
        node_states = [(next_node, deepcopy(graph_run.state))]

        while not isinstance(next_node, End):
            if graph_run.state.number == 50:
                graph_run.state.number = 42
            next_node = await graph_run.next(next_node)
            node_states.append((next_node, deepcopy(graph_run.state)))

        print(node_states)
        '''
        [
            (Increment(), MyState(number=48)),
            (Check42(), MyState(number=49)),
            (End(data=49), MyState(number=49)),
        ]
        '''
```

```
from copy import deepcopy
from pydantic_graph import End
from never_42 import Increment, MyState, never_42_graph

async def main():
    state = MyState(48)
    async with never_42_graph.iter(Increment(), state=state) as graph_run:
        next_node = graph_run.next_node  # start with the first node
        node_states = [(next_node, deepcopy(graph_run.state))]

        while not isinstance(next_node, End):
            if graph_run.state.number == 50:
                graph_run.state.number = 42
            next_node = await graph_run.next(next_node)
            node_states.append((next_node, deepcopy(graph_run.state)))

        print(node_states)
        '''
        [
            (Increment(), MyState(number=48)),
            (Check42(), MyState(number=49)),
            (End(data=49), MyState(number=49)),
        ]
        '''
```

Parameters:

```
node
```

```
BaseNode[StateT, DepsT, T] | None
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

The node to run next in the graph. If not specified, uses self.next_node, which is initialized to
the start_node of the run and updated each time a new node is returned.

```
self.next_node
```

```
start_node
```

```
None
```

Returns:

```
BaseNode[StateT, DepsT, T] | End[T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[End](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.End)

The next node returned by the graph logic, or an End node if

```
End
```

```
BaseNode[StateT, DepsT, T] | End[T]
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[End](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.End)

the run has completed.

```
pydantic_graph/pydantic_graph/graph.py
```

```
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
```

```
async def next(
    self: GraphRun[StateT, DepsT, T], node: BaseNode[StateT, DepsT, T] | None = None
) -> BaseNode[StateT, DepsT, T] | End[T]:
    """Manually drive the graph run by passing in the node you want to run next.

    This lets you inspect or mutate the node before continuing execution, or skip certain nodes
    under dynamic conditions. The graph run should stop when you return an [`End`][pydantic_graph.nodes.End] node.

    Here's an example of using `next` to drive the graph from [above][pydantic_graph.graph.Graph]:
    ```py {title="next_never_42.py" noqa="I001" py="3.10"}
    from copy import deepcopy
    from pydantic_graph import End
    from never_42 import Increment, MyState, never_42_graph

    async def main():
        state = MyState(48)
        async with never_42_graph.iter(Increment(), state=state) as graph_run:
            next_node = graph_run.next_node  # start with the first node
            node_states = [(next_node, deepcopy(graph_run.state))]

            while not isinstance(next_node, End):
                if graph_run.state.number == 50:
                    graph_run.state.number = 42
                next_node = await graph_run.next(next_node)
                node_states.append((next_node, deepcopy(graph_run.state)))

            print(node_states)
            '''
            [
                (Increment(), MyState(number=48)),
                (Check42(), MyState(number=49)),
                (End(data=49), MyState(number=49)),
            ]
            '''
    ```

    Args:
        node: The node to run next in the graph. If not specified, uses `self.next_node`, which is initialized to
            the `start_node` of the run and updated each time a new node is returned.

    Returns:
        The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
        the run has completed.
    """
    if node is None:
        if isinstance(self._next_node, End):
            # Note: we could alternatively just return `self._next_node` here, but it's easier to start with an
            # error and relax the behavior later, than vice versa.
            raise exceptions.GraphRuntimeError('This graph run has already ended.')
        node = self._next_node

    history = self.history
    state = self.state
    deps = self.deps

    self._next_node = await self.graph.next(node, history, state=state, deps=deps, infer_name=False)

    return self._next_node
```

```
async def next(
    self: GraphRun[StateT, DepsT, T], node: BaseNode[StateT, DepsT, T] | None = None
) -> BaseNode[StateT, DepsT, T] | End[T]:
    """Manually drive the graph run by passing in the node you want to run next.

    This lets you inspect or mutate the node before continuing execution, or skip certain nodes
    under dynamic conditions. The graph run should stop when you return an [`End`][pydantic_graph.nodes.End] node.

    Here's an example of using `next` to drive the graph from [above][pydantic_graph.graph.Graph]:
    ```py {title="next_never_42.py" noqa="I001" py="3.10"}
    from copy import deepcopy
    from pydantic_graph import End
    from never_42 import Increment, MyState, never_42_graph

    async def main():
        state = MyState(48)
        async with never_42_graph.iter(Increment(), state=state) as graph_run:
            next_node = graph_run.next_node  # start with the first node
            node_states = [(next_node, deepcopy(graph_run.state))]

            while not isinstance(next_node, End):
                if graph_run.state.number == 50:
                    graph_run.state.number = 42
                next_node = await graph_run.next(next_node)
                node_states.append((next_node, deepcopy(graph_run.state)))

            print(node_states)
            '''
            [
                (Increment(), MyState(number=48)),
                (Check42(), MyState(number=49)),
                (End(data=49), MyState(number=49)),
            ]
            '''
    ```

    Args:
        node: The node to run next in the graph. If not specified, uses `self.next_node`, which is initialized to
            the `start_node` of the run and updated each time a new node is returned.

    Returns:
        The next node returned by the graph logic, or an [`End`][pydantic_graph.nodes.End] node if
        the run has completed.
    """
    if node is None:
        if isinstance(self._next_node, End):
            # Note: we could alternatively just return `self._next_node` here, but it's easier to start with an
            # error and relax the behavior later, than vice versa.
            raise exceptions.GraphRuntimeError('This graph run has already ended.')
        node = self._next_node

    history = self.history
    state = self.state
    deps = self.deps

    self._next_node = await self.graph.next(node, history, state=state, deps=deps, infer_name=False)

    return self._next_node
```

#### __anext__

async

```
async
```

```
__anext__() -> (
    BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]
)
```

```
__anext__() -> (
    BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]
)
```

[BaseNode](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.BaseNode)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[DepsT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.DepsT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

[End](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.End)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

Use the last returned node as the input to Graph.next.

```
Graph.next
```

```
pydantic_graph/pydantic_graph/graph.py
```

```
730
731
732
733
734
```

```
async def __anext__(self) -> BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]:
    """Use the last returned node as the input to `Graph.next`."""
    if isinstance(self._next_node, End):
        raise StopAsyncIteration
    return await self.next(self._next_node)
```

```
async def __anext__(self) -> BaseNode[StateT, DepsT, RunEndT] | End[RunEndT]:
    """Use the last returned node as the input to `Graph.next`."""
    if isinstance(self._next_node, End):
        raise StopAsyncIteration
    return await self.next(self._next_node)
```

### GraphRunResult

dataclass

```
dataclass
```

Bases: Generic[StateT, RunEndT]

```
Generic[StateT, RunEndT]
```

[Generic](https://docs.python.org/3/library/typing.html#typing.Generic)

[StateT](https://ai.pydantic.dev/state/#pydantic_graph.state.StateT)

[RunEndT](https://ai.pydantic.dev/nodes/#pydantic_graph.nodes.RunEndT)

The final result of running a graph.

```
pydantic_graph/pydantic_graph/graph.py
```

```
740
741
742
743
744
745
746
```

```
@dataclass
class GraphRunResult(Generic[StateT, RunEndT]):
    """The final result of running a graph."""

    output: RunEndT
    state: StateT
    history: list[HistoryStep[StateT, RunEndT]] = field(repr=False)
```

```
@dataclass
class GraphRunResult(Generic[StateT, RunEndT]):
    """The final result of running a graph."""

    output: RunEndT
    state: StateT
    history: list[HistoryStep[StateT, RunEndT]] = field(repr=False)
```

