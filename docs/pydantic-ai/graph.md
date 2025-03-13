# Graphs

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# Graphs

Don't use a nail gun unless you need a nail gun

If PydanticAI agents are a hammer, and multi-agent workflows are a sledgehammer, then graphs are a nail gun:

* sure, nail guns look cooler than hammers
* but nail guns take a lot more setup than hammers
* and nail guns don't make you a better builder, they make you a builder with a nail gun
* Lastly, (and at the risk of torturing this metaphor), if you're a fan of medieval tools like mallets and untyped Python, you probably won't like nail guns or our approach to graphs. (But then again, if you're not a fan of type hints in Python, you've probably already bounced off PydanticAI to use one of the toy agent frameworks â good luck, and feel free to borrow my sledgehammer when you realize you need it)

In short, graphs are a powerful tool, but they're not the right tool for every job. Please consider other multi-agent approaches before proceeding.

If you're not confident a graph-based approach is a good idea, it might be unnecessary.

Graphs and finite state machines (FSMs) are a powerful abstraction to model, execute, control and visualize complex workflows.

Alongside PydanticAI, we've developed pydantic-graph â an async graph and state machine library for Python where nodes and edges are defined using type hints.

```
pydantic-graph
```

While this library is developed as part of PydanticAI; it has no dependency on pydantic-ai and can be considered as a pure graph-based state machine library. You may find it useful whether or not you're using PydanticAI or even building with GenAI.

```
pydantic-ai
```

pydantic-graph is designed for advanced users and makes heavy use of Python generics and type hints. It is not designed to be as beginner-friendly as PydanticAI.

```
pydantic-graph
```

Very Early beta

Graph support was introduced in v0.0.19 and is in a very early beta. The API is subject to change. The documentation is incomplete. The implementation is incomplete.

## Installation

pydantic-graph is a required dependency of pydantic-ai, and an optional dependency of pydantic-ai-slim, see installation instructions for more information. You can also install it directly:

```
pydantic-graph
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
pip install pydantic-graph
```

```
pip install pydantic-graph
```

```
uv add pydantic-graph
```

```
uv add pydantic-graph
```

## Graph Types

pydantic-graph is made up of a few key components:

```
pydantic-graph
```

### GraphRunContext

GraphRunContext â The context for the graph run, similar to PydanticAI's RunContext. This holds the state of the graph and dependencies and is passed to nodes when they're run.

```
GraphRunContext
```

```
RunContext
```

GraphRunContext is generic in the state type of the graph it's used in, StateT.

```
GraphRunContext
```

```
StateT
```

### End

End â return value to indicate the graph run should end.

```
End
```

End is generic in the graph return type of the graph it's used in, RunEndT.

```
End
```

```
RunEndT
```

### Nodes

Subclasses of BaseNode define nodes for execution in the graph.

```
BaseNode
```

Nodes, which are generally dataclasses, generally consist of:

```
dataclass
```

* fields containing any parameters required/optional when calling the node
* the business logic to execute the node, in the run method
* return annotations of the run method, which are read by pydantic-graph to determine the outgoing edges of the node

```
run
```

```
run
```

```
pydantic-graph
```

Nodes are generic in:

* state, which must have the same type as the state of graphs they're included in, StateT has a default of None, so if you're not using state you can omit this generic parameter, see stateful graphs for more information
* deps, which must have the same type as the deps of the graph they're included in, DepsT has a default of None, so if you're not using deps you can omit this generic parameter, see dependency injection for more information
* graph return type â this only applies if the node returns End. RunEndT has a default of Never so this generic parameter can be omitted if the node doesn't return End, but must be included if it does.

```
StateT
```

```
None
```

```
DepsT
```

```
None
```

```
End
```

```
RunEndT
```

```
End
```

Here's an example of a start or intermediate node in a graph â it can't end the run as it doesn't return End:

```
End
```

```
from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext


@dataclass
class MyNode(BaseNode[MyState]):  # (1)!
    foo: int  # (2)!

    async def run(
        self,
        ctx: GraphRunContext[MyState],  # (3)!
    ) -> AnotherNode:  # (4)!
        ...
        return AnotherNode()
```

```
from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext


@dataclass
class MyNode(BaseNode[MyState]):  # (1)!
    foo: int  # (2)!

    async def run(
        self,
        ctx: GraphRunContext[MyState],  # (3)!
    ) -> AnotherNode:  # (4)!
        ...
        return AnotherNode()
```

1. State in this example is MyState (not shown), hence BaseNode is parameterized with MyState. This node can't end the run, so the RunEndT generic parameter is omitted and defaults to Never.
2. MyNode is a dataclass and has a single field foo, an int.
3. The run method takes a GraphRunContext parameter, again parameterized with state MyState.
4. The return type of the run method is AnotherNode (not shown), this is used to determine the outgoing edges of the node.

```
MyState
```

```
BaseNode
```

```
MyState
```

```
RunEndT
```

```
Never
```

```
MyNode
```

```
foo
```

```
int
```

```
run
```

```
GraphRunContext
```

```
MyState
```

```
run
```

```
AnotherNode
```

We could extend MyNode to optionally end the run if foo is divisible by 5:

```
MyNode
```

```
foo
```

```
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext


@dataclass
class MyNode(BaseNode[MyState, None, int]):  # (1)!
    foo: int

    async def run(
        self,
        ctx: GraphRunContext[MyState],
    ) -> AnotherNode | End[int]:  # (2)!
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return AnotherNode()
```

```
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext


@dataclass
class MyNode(BaseNode[MyState, None, int]):  # (1)!
    foo: int

    async def run(
        self,
        ctx: GraphRunContext[MyState],
    ) -> AnotherNode | End[int]:  # (2)!
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return AnotherNode()
```

1. We parameterize the node with the return type (int in this case) as well as state. Because generic parameters are positional-only, we have to include None as the second parameter representing deps.
2. The return type of the run method is now a union of AnotherNode and End[int], this allows the node to end the run if foo is divisible by 5.

```
int
```

```
None
```

```
run
```

```
AnotherNode
```

```
End[int]
```

```
foo
```

### Graph

Graph â this is the execution graph itself, made up of a set of node classes (i.e., BaseNode subclasses).

```
Graph
```

```
BaseNode
```

Graph is generic in:

```
Graph
```

* state the state type of the graph, StateT
* deps the deps type of the graph, DepsT
* graph return type the return type of the graph run, RunEndT

```
StateT
```

```
DepsT
```

```
RunEndT
```

Here's an example of a simple graph:

```
from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class DivisibleBy5(BaseNode[None, None, int]):  # (1)!
    foo: int

    async def run(
        self,
        ctx: GraphRunContext,
    ) -> Increment | End[int]:
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return Increment(self.foo)


@dataclass
class Increment(BaseNode):  # (2)!
    foo: int

    async def run(self, ctx: GraphRunContext) -> DivisibleBy5:
        return DivisibleBy5(self.foo + 1)


fives_graph = Graph(nodes=[DivisibleBy5, Increment])  # (3)!
result = fives_graph.run_sync(DivisibleBy5(4))  # (4)!
print(result.output)
#> 5
# the full history is quite verbose (see below), so we'll just print the summary
print([item.data_snapshot() for item in result.history])
#> [DivisibleBy5(foo=4), Increment(foo=4), DivisibleBy5(foo=5), End(data=5)]
```

```
from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class DivisibleBy5(BaseNode[None, None, int]):  # (1)!
    foo: int

    async def run(
        self,
        ctx: GraphRunContext,
    ) -> Increment | End[int]:
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return Increment(self.foo)


@dataclass
class Increment(BaseNode):  # (2)!
    foo: int

    async def run(self, ctx: GraphRunContext) -> DivisibleBy5:
        return DivisibleBy5(self.foo + 1)


fives_graph = Graph(nodes=[DivisibleBy5, Increment])  # (3)!
result = fives_graph.run_sync(DivisibleBy5(4))  # (4)!
print(result.output)
#> 5
# the full history is quite verbose (see below), so we'll just print the summary
print([item.data_snapshot() for item in result.history])
#> [DivisibleBy5(foo=4), Increment(foo=4), DivisibleBy5(foo=5), End(data=5)]
```

1. The DivisibleBy5 node is parameterized with None for the state param and None for the deps param as this graph doesn't use state or deps, and int as it can end the run.
2. The Increment node doesn't return End, so the RunEndT generic parameter is omitted, state can also be omitted as the graph doesn't use state.
3. The graph is created with a sequence of nodes.
4. The graph is run synchronously with run_sync. The initial node is DivisibleBy5(4). Because the graph doesn't use external state or deps, we don't pass state or deps.

```
DivisibleBy5
```

```
None
```

```
None
```

```
int
```

```
Increment
```

```
End
```

```
RunEndT
```

```
run_sync
```

```
DivisibleBy5(4)
```

```
state
```

```
deps
```

(This example is complete, it can be run "as is" with Python 3.10+)

A mermaid diagram for this graph can be generated with the following code:

```
from graph_example import DivisibleBy5, fives_graph

fives_graph.mermaid_code(start_node=DivisibleBy5)
```

```
from graph_example import DivisibleBy5, fives_graph

fives_graph.mermaid_code(start_node=DivisibleBy5)
```

```
---
title: fives_graph
---
stateDiagram-v2
  [*] --> DivisibleBy5
  DivisibleBy5 --> Increment
  DivisibleBy5 --> [*]
  Increment --> DivisibleBy5
```

```
---
title: fives_graph
---
stateDiagram-v2
  [*] --> DivisibleBy5
  DivisibleBy5 --> Increment
  DivisibleBy5 --> [*]
  Increment --> DivisibleBy5
```

In order to visualize a graph within a jupyter-notebook, IPython.display needs to be used:

```
jupyter-notebook
```

```
IPython.display
```

```
from graph_example import DivisibleBy5, fives_graph
from IPython.display import Image, display

display(Image(fives_graph.mermaid_image(start_node=DivisibleBy5)))
```

```
from graph_example import DivisibleBy5, fives_graph
from IPython.display import Image, display

display(Image(fives_graph.mermaid_image(start_node=DivisibleBy5)))
```

## Stateful Graphs

The "state" concept in pydantic-graph provides an optional way to access and mutate an object (often a dataclass or Pydantic model) as nodes run in a graph. If you think of Graphs as a production line, then your state is the engine being passed along the line and built up by each node as the graph is run.

```
pydantic-graph
```

```
dataclass
```

In the future, we intend to extend pydantic-graph to provide state persistence with the state recorded after each node is run, see #695.

```
pydantic-graph
```

Here's an example of a graph which represents a vending machine where the user may insert coins and select a product to purchase.

```
from __future__ import annotations

from dataclasses import dataclass

from rich.prompt import Prompt

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class MachineState:  # (1)!
    user_balance: float = 0.0
    product: str | None = None


@dataclass
class InsertCoin(BaseNode[MachineState]):  # (3)!
    async def run(self, ctx: GraphRunContext[MachineState]) -> CoinsInserted:  # (16)!
        return CoinsInserted(float(Prompt.ask('Insert coins')))  # (4)!


@dataclass
class CoinsInserted(BaseNode[MachineState]):
    amount: float  # (5)!

    async def run(
        self, ctx: GraphRunContext[MachineState]
    ) -> SelectProduct | Purchase:  # (17)!
        ctx.state.user_balance += self.amount  # (6)!
        if ctx.state.product is not None:  # (7)!
            return Purchase(ctx.state.product)
        else:
            return SelectProduct()


@dataclass
class SelectProduct(BaseNode[MachineState]):
    async def run(self, ctx: GraphRunContext[MachineState]) -> Purchase:
        return Purchase(Prompt.ask('Select product'))


PRODUCT_PRICES = {  # (2)!
    'water': 1.25,
    'soda': 1.50,
    'crisps': 1.75,
    'chocolate': 2.00,
}


@dataclass
class Purchase(BaseNode[MachineState, None, None]):  # (18)!
    product: str

    async def run(
        self, ctx: GraphRunContext[MachineState]
    ) -> End | InsertCoin | SelectProduct:
        if price := PRODUCT_PRICES.get(self.product):  # (8)!
            ctx.state.product = self.product  # (9)!
            if ctx.state.user_balance >= price:  # (10)!
                ctx.state.user_balance -= price
                return End(None)
            else:
                diff = price - ctx.state.user_balance
                print(f'Not enough money for {self.product}, need {diff:0.2f} more')
                #> Not enough money for crisps, need 0.75 more
                return InsertCoin()  # (11)!
        else:
            print(f'No such product: {self.product}, try again')
            return SelectProduct()  # (12)!


vending_machine_graph = Graph(  # (13)!
    nodes=[InsertCoin, CoinsInserted, SelectProduct, Purchase]
)


async def main():
    state = MachineState()  # (14)!
    await vending_machine_graph.run(InsertCoin(), state=state)  # (15)!
    print(f'purchase successful item={state.product} change={state.user_balance:0.2f}')
    #> purchase successful item=crisps change=0.25
```

```
from __future__ import annotations

from dataclasses import dataclass

from rich.prompt import Prompt

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class MachineState:  # (1)!
    user_balance: float = 0.0
    product: str | None = None


@dataclass
class InsertCoin(BaseNode[MachineState]):  # (3)!
    async def run(self, ctx: GraphRunContext[MachineState]) -> CoinsInserted:  # (16)!
        return CoinsInserted(float(Prompt.ask('Insert coins')))  # (4)!


@dataclass
class CoinsInserted(BaseNode[MachineState]):
    amount: float  # (5)!

    async def run(
        self, ctx: GraphRunContext[MachineState]
    ) -> SelectProduct | Purchase:  # (17)!
        ctx.state.user_balance += self.amount  # (6)!
        if ctx.state.product is not None:  # (7)!
            return Purchase(ctx.state.product)
        else:
            return SelectProduct()


@dataclass
class SelectProduct(BaseNode[MachineState]):
    async def run(self, ctx: GraphRunContext[MachineState]) -> Purchase:
        return Purchase(Prompt.ask('Select product'))


PRODUCT_PRICES = {  # (2)!
    'water': 1.25,
    'soda': 1.50,
    'crisps': 1.75,
    'chocolate': 2.00,
}


@dataclass
class Purchase(BaseNode[MachineState, None, None]):  # (18)!
    product: str

    async def run(
        self, ctx: GraphRunContext[MachineState]
    ) -> End | InsertCoin | SelectProduct:
        if price := PRODUCT_PRICES.get(self.product):  # (8)!
            ctx.state.product = self.product  # (9)!
            if ctx.state.user_balance >= price:  # (10)!
                ctx.state.user_balance -= price
                return End(None)
            else:
                diff = price - ctx.state.user_balance
                print(f'Not enough money for {self.product}, need {diff:0.2f} more')
                #> Not enough money for crisps, need 0.75 more
                return InsertCoin()  # (11)!
        else:
            print(f'No such product: {self.product}, try again')
            return SelectProduct()  # (12)!


vending_machine_graph = Graph(  # (13)!
    nodes=[InsertCoin, CoinsInserted, SelectProduct, Purchase]
)


async def main():
    state = MachineState()  # (14)!
    await vending_machine_graph.run(InsertCoin(), state=state)  # (15)!
    print(f'purchase successful item={state.product} change={state.user_balance:0.2f}')
    #> purchase successful item=crisps change=0.25
```

1. The state of the vending machine is defined as a dataclass with the user's balance and the product they've selected, if any.
2. A dictionary of products mapped to prices.
3. The InsertCoin node, BaseNode is parameterized with MachineState as that's the state used in this graph.
4. The InsertCoin node prompts the user to insert coins. We keep things simple by just entering a monetary amount as a float. Before you start thinking this is a toy too since it's using rich's Prompt.ask within nodes, see below for how control flow can be managed when nodes require external input.
5. The CoinsInserted node; again this is a dataclass with one field amount.
6. Update the user's balance with the amount inserted.
7. If the user has already selected a product, go to Purchase, otherwise go to SelectProduct.
8. In the Purchase node, look up the price of the product if the user entered a valid product.
9. If the user did enter a valid product, set the product in the state so we don't revisit SelectProduct.
10. If the balance is enough to purchase the product, adjust the balance to reflect the purchase and return End to end the graph. We're not using the run return type, so we call End with None.
11. If the balance is insufficient, go to InsertCoin to prompt the user to insert more coins.
12. If the product is invalid, go to SelectProduct to prompt the user to select a product again.
13. The graph is created by passing a list of nodes to Graph. Order of nodes is not important, but it can affect how diagrams are displayed.
14. Initialize the state. This will be passed to the graph run and mutated as the graph runs.
15. Run the graph with the initial state. Since the graph can be run from any node, we must pass the start node â in this case, InsertCoin. Graph.run returns a GraphRunResult that provides the final data and a history of the run.
16. The return type of the node's run method is important as it is used to determine the outgoing edges of the node. This information in turn is used to render mermaid diagrams and is enforced at runtime to detect misbehavior as soon as possible.
17. The return type of CoinsInserted's run method is a union, meaning multiple outgoing edges are possible.
18. Unlike other nodes, Purchase can end the run, so the RunEndT generic parameter must be set. In this case it's None since the graph run return type is None.

```
InsertCoin
```

```
BaseNode
```

```
MachineState
```

```
InsertCoin
```

```
Prompt.ask
```

```
CoinsInserted
```

```
dataclass
```

```
amount
```

```
Purchase
```

```
SelectProduct
```

```
Purchase
```

```
SelectProduct
```

```
End
```

```
End
```

```
None
```

```
InsertCoin
```

```
SelectProduct
```

```
Graph
```

```
InsertCoin
```

```
Graph.run
```

```
GraphRunResult
```

```
run
```

```
CoinsInserted
```

```
run
```

```
Purchase
```

```
RunEndT
```

```
None
```

```
None
```

(This example is complete, it can be run "as is" with Python 3.10+ â you'll need to add asyncio.run(main()) to run main)

```
asyncio.run(main())
```

```
main
```

A mermaid diagram for this graph can be generated with the following code:

```
from vending_machine import InsertCoin, vending_machine_graph

vending_machine_graph.mermaid_code(start_node=InsertCoin)
```

```
from vending_machine import InsertCoin, vending_machine_graph

vending_machine_graph.mermaid_code(start_node=InsertCoin)
```

The diagram generated by the above code is:

```
---
title: vending_machine_graph
---
stateDiagram-v2
  [*] --> InsertCoin
  InsertCoin --> CoinsInserted
  CoinsInserted --> SelectProduct
  CoinsInserted --> Purchase
  SelectProduct --> Purchase
  Purchase --> InsertCoin
  Purchase --> SelectProduct
  Purchase --> [*]
```

```
---
title: vending_machine_graph
---
stateDiagram-v2
  [*] --> InsertCoin
  InsertCoin --> CoinsInserted
  CoinsInserted --> SelectProduct
  CoinsInserted --> Purchase
  SelectProduct --> Purchase
  Purchase --> InsertCoin
  Purchase --> SelectProduct
  Purchase --> [*]
```

See below for more information on generating diagrams.

## GenAI Example

So far we haven't shown an example of a Graph that actually uses PydanticAI or GenAI at all.

In this example, one agent generates a welcome email to a user and the other agent provides feedback on the email.

This graph has a very simple structure:

```
---
title: feedback_graph
---
stateDiagram-v2
  [*] --> WriteEmail
  WriteEmail --> Feedback
  Feedback --> WriteEmail
  Feedback --> [*]
```

```
---
title: feedback_graph
---
stateDiagram-v2
  [*] --> WriteEmail
  WriteEmail --> Feedback
  Feedback --> WriteEmail
  Feedback --> [*]
```

```
from __future__ import annotations as _annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, EmailStr

from pydantic_ai import Agent
from pydantic_ai.format_as_xml import format_as_xml
from pydantic_ai.messages import ModelMessage
from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class User:
    name: str
    email: EmailStr
    interests: list[str]


@dataclass
class Email:
    subject: str
    body: str


@dataclass
class State:
    user: User
    write_agent_messages: list[ModelMessage] = field(default_factory=list)


email_writer_agent = Agent(
    'google-vertex:gemini-1.5-pro',
    result_type=Email,
    system_prompt='Write a welcome email to our tech blog.',
)


@dataclass
class WriteEmail(BaseNode[State]):
    email_feedback: str | None = None

    async def run(self, ctx: GraphRunContext[State]) -> Feedback:
        if self.email_feedback:
            prompt = (
                f'Rewrite the email for the user:\n'
                f'{format_as_xml(ctx.state.user)}\n'
                f'Feedback: {self.email_feedback}'
            )
        else:
            prompt = (
                f'Write a welcome email for the user:\n'
                f'{format_as_xml(ctx.state.user)}'
            )

        result = await email_writer_agent.run(
            prompt,
            message_history=ctx.state.write_agent_messages,
        )
        ctx.state.write_agent_messages += result.all_messages()
        return Feedback(result.data)


class EmailRequiresWrite(BaseModel):
    feedback: str


class EmailOk(BaseModel):
    pass


feedback_agent = Agent[None, EmailRequiresWrite | EmailOk](
    'openai:gpt-4o',
    result_type=EmailRequiresWrite | EmailOk,  # type: ignore
    system_prompt=(
        'Review the email and provide feedback, email must reference the users specific interests.'
    ),
)


@dataclass
class Feedback(BaseNode[State, None, Email]):
    email: Email

    async def run(
        self,
        ctx: GraphRunContext[State],
    ) -> WriteEmail | End[Email]:
        prompt = format_as_xml({'user': ctx.state.user, 'email': self.email})
        result = await feedback_agent.run(prompt)
        if isinstance(result.data, EmailRequiresWrite):
            return WriteEmail(email_feedback=result.data.feedback)
        else:
            return End(self.email)


async def main():
    user = User(
        name='John Doe',
        email='john.joe@example.com',
        interests=['Haskel', 'Lisp', 'Fortran'],
    )
    state = State(user)
    feedback_graph = Graph(nodes=(WriteEmail, Feedback))
    result = await feedback_graph.run(WriteEmail(), state=state)
    print(result.output)
    """
    Email(
        subject='Welcome to our tech blog!',
        body='Hello John, Welcome to our tech blog! ...',
    )
    """
```

```
from __future__ import annotations as _annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, EmailStr

from pydantic_ai import Agent
from pydantic_ai.format_as_xml import format_as_xml
from pydantic_ai.messages import ModelMessage
from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class User:
    name: str
    email: EmailStr
    interests: list[str]


@dataclass
class Email:
    subject: str
    body: str


@dataclass
class State:
    user: User
    write_agent_messages: list[ModelMessage] = field(default_factory=list)


email_writer_agent = Agent(
    'google-vertex:gemini-1.5-pro',
    result_type=Email,
    system_prompt='Write a welcome email to our tech blog.',
)


@dataclass
class WriteEmail(BaseNode[State]):
    email_feedback: str | None = None

    async def run(self, ctx: GraphRunContext[State]) -> Feedback:
        if self.email_feedback:
            prompt = (
                f'Rewrite the email for the user:\n'
                f'{format_as_xml(ctx.state.user)}\n'
                f'Feedback: {self.email_feedback}'
            )
        else:
            prompt = (
                f'Write a welcome email for the user:\n'
                f'{format_as_xml(ctx.state.user)}'
            )

        result = await email_writer_agent.run(
            prompt,
            message_history=ctx.state.write_agent_messages,
        )
        ctx.state.write_agent_messages += result.all_messages()
        return Feedback(result.data)


class EmailRequiresWrite(BaseModel):
    feedback: str


class EmailOk(BaseModel):
    pass


feedback_agent = Agent[None, EmailRequiresWrite | EmailOk](
    'openai:gpt-4o',
    result_type=EmailRequiresWrite | EmailOk,  # type: ignore
    system_prompt=(
        'Review the email and provide feedback, email must reference the users specific interests.'
    ),
)


@dataclass
class Feedback(BaseNode[State, None, Email]):
    email: Email

    async def run(
        self,
        ctx: GraphRunContext[State],
    ) -> WriteEmail | End[Email]:
        prompt = format_as_xml({'user': ctx.state.user, 'email': self.email})
        result = await feedback_agent.run(prompt)
        if isinstance(result.data, EmailRequiresWrite):
            return WriteEmail(email_feedback=result.data.feedback)
        else:
            return End(self.email)


async def main():
    user = User(
        name='John Doe',
        email='john.joe@example.com',
        interests=['Haskel', 'Lisp', 'Fortran'],
    )
    state = State(user)
    feedback_graph = Graph(nodes=(WriteEmail, Feedback))
    result = await feedback_graph.run(WriteEmail(), state=state)
    print(result.output)
    """
    Email(
        subject='Welcome to our tech blog!',
        body='Hello John, Welcome to our tech blog! ...',
    )
    """
```

(This example is complete, it can be run "as is" with Python 3.10+ â you'll need to add asyncio.run(main()) to run main)

```
asyncio.run(main())
```

```
main
```

## Custom Control Flow

In many real-world applications, Graphs cannot run uninterrupted from start to finish â they might require external input, or run over an extended period of time such that a single process cannot execute the entire graph run from start to finish without interruption.

In these scenarios the next method can be used to run the graph one node at a time.

```
next
```

In this example, an AI asks the user a question, the user provides an answer, the AI evaluates the answer and ends if the user got it right or asks another question if they got it wrong.

```
ai_q_and_a_graph.py
```

```
question_graph
```

```
from __future__ import annotations as _annotations

from dataclasses import dataclass, field

from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from pydantic_ai import Agent
from pydantic_ai.format_as_xml import format_as_xml
from pydantic_ai.messages import ModelMessage

ask_agent = Agent('openai:gpt-4o', result_type=str)


@dataclass
class QuestionState:
    question: str | None = None
    ask_agent_messages: list[ModelMessage] = field(default_factory=list)
    evaluate_agent_messages: list[ModelMessage] = field(default_factory=list)


@dataclass
class Ask(BaseNode[QuestionState]):
    async def run(self, ctx: GraphRunContext[QuestionState]) -> Answer:
        result = await ask_agent.run(
            'Ask a simple question with a single correct answer.',
            message_history=ctx.state.ask_agent_messages,
        )
        ctx.state.ask_agent_messages += result.all_messages()
        ctx.state.question = result.data
        return Answer(result.data)


@dataclass
class Answer(BaseNode[QuestionState]):
    question: str
    answer: str | None = None

    async def run(self, ctx: GraphRunContext[QuestionState]) -> Evaluate:
        assert self.answer is not None
        return Evaluate(self.answer)


@dataclass
class EvaluationResult:
    correct: bool
    comment: str


evaluate_agent = Agent(
    'openai:gpt-4o',
    result_type=EvaluationResult,
    system_prompt='Given a question and answer, evaluate if the answer is correct.',
)


@dataclass
class Evaluate(BaseNode[QuestionState]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[QuestionState],
    ) -> End[str] | Reprimand:
        assert ctx.state.question is not None
        result = await evaluate_agent.run(
            format_as_xml({'question': ctx.state.question, 'answer': self.answer}),
            message_history=ctx.state.evaluate_agent_messages,
        )
        ctx.state.evaluate_agent_messages += result.all_messages()
        if result.data.correct:
            return End(result.data.comment)
        else:
            return Reprimand(result.data.comment)


@dataclass
class Reprimand(BaseNode[QuestionState]):
    comment: str

    async def run(self, ctx: GraphRunContext[QuestionState]) -> Ask:
        print(f'Comment: {self.comment}')
        ctx.state.question = None
        return Ask()


question_graph = Graph(nodes=(Ask, Answer, Evaluate, Reprimand))
```

```
from __future__ import annotations as _annotations

from dataclasses import dataclass, field

from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from pydantic_ai import Agent
from pydantic_ai.format_as_xml import format_as_xml
from pydantic_ai.messages import ModelMessage

ask_agent = Agent('openai:gpt-4o', result_type=str)


@dataclass
class QuestionState:
    question: str | None = None
    ask_agent_messages: list[ModelMessage] = field(default_factory=list)
    evaluate_agent_messages: list[ModelMessage] = field(default_factory=list)


@dataclass
class Ask(BaseNode[QuestionState]):
    async def run(self, ctx: GraphRunContext[QuestionState]) -> Answer:
        result = await ask_agent.run(
            'Ask a simple question with a single correct answer.',
            message_history=ctx.state.ask_agent_messages,
        )
        ctx.state.ask_agent_messages += result.all_messages()
        ctx.state.question = result.data
        return Answer(result.data)


@dataclass
class Answer(BaseNode[QuestionState]):
    question: str
    answer: str | None = None

    async def run(self, ctx: GraphRunContext[QuestionState]) -> Evaluate:
        assert self.answer is not None
        return Evaluate(self.answer)


@dataclass
class EvaluationResult:
    correct: bool
    comment: str


evaluate_agent = Agent(
    'openai:gpt-4o',
    result_type=EvaluationResult,
    system_prompt='Given a question and answer, evaluate if the answer is correct.',
)


@dataclass
class Evaluate(BaseNode[QuestionState]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[QuestionState],
    ) -> End[str] | Reprimand:
        assert ctx.state.question is not None
        result = await evaluate_agent.run(
            format_as_xml({'question': ctx.state.question, 'answer': self.answer}),
            message_history=ctx.state.evaluate_agent_messages,
        )
        ctx.state.evaluate_agent_messages += result.all_messages()
        if result.data.correct:
            return End(result.data.comment)
        else:
            return Reprimand(result.data.comment)


@dataclass
class Reprimand(BaseNode[QuestionState]):
    comment: str

    async def run(self, ctx: GraphRunContext[QuestionState]) -> Ask:
        print(f'Comment: {self.comment}')
        ctx.state.question = None
        return Ask()


question_graph = Graph(nodes=(Ask, Answer, Evaluate, Reprimand))
```

(This example is complete, it can be run "as is" with Python 3.10+)

```
from rich.prompt import Prompt

from pydantic_graph import End, HistoryStep

from ai_q_and_a_graph import Ask, question_graph, QuestionState, Answer


async def main():
    state = QuestionState()  # (1)!
    node = Ask()  # (2)!
    history: list[HistoryStep[QuestionState]] = []  # (3)!
    while True:
        node = await question_graph.next(node, history, state=state)  # (4)!
        if isinstance(node, Answer):
            node.answer = Prompt.ask(node.question)  # (5)!
        elif isinstance(node, End):  # (6)!
            print(f'Correct answer! {node.data}')
            #> Correct answer! Well done, 1 + 1 = 2
            print([e.data_snapshot() for e in history])
            """
            [
                Ask(),
                Answer(question='What is the capital of France?', answer='Vichy'),
                Evaluate(answer='Vichy'),
                Reprimand(comment='Vichy is no longer the capital of France.'),
                Ask(),
                Answer(question='what is 1 + 1?', answer='2'),
                Evaluate(answer='2'),
                End(data='Well done, 1 + 1 = 2'),
            ]
            """
            return
        # otherwise just continue
```

```
from rich.prompt import Prompt

from pydantic_graph import End, HistoryStep

from ai_q_and_a_graph import Ask, question_graph, QuestionState, Answer


async def main():
    state = QuestionState()  # (1)!
    node = Ask()  # (2)!
    history: list[HistoryStep[QuestionState]] = []  # (3)!
    while True:
        node = await question_graph.next(node, history, state=state)  # (4)!
        if isinstance(node, Answer):
            node.answer = Prompt.ask(node.question)  # (5)!
        elif isinstance(node, End):  # (6)!
            print(f'Correct answer! {node.data}')
            #> Correct answer! Well done, 1 + 1 = 2
            print([e.data_snapshot() for e in history])
            """
            [
                Ask(),
                Answer(question='What is the capital of France?', answer='Vichy'),
                Evaluate(answer='Vichy'),
                Reprimand(comment='Vichy is no longer the capital of France.'),
                Ask(),
                Answer(question='what is 1 + 1?', answer='2'),
                Evaluate(answer='2'),
                End(data='Well done, 1 + 1 = 2'),
            ]
            """
            return
        # otherwise just continue
```

1. Create the state object which will be mutated by next.
2. The start node is Ask but will be updated by next as the graph runs.
3. The history of the graph run is stored in a list of HistoryStep objects. Again next will update this list in place.
4. Run the graph one node at a time, updating the state, current node and history as the graph runs.
5. If the current node is an Answer node, prompt the user for an answer.
6. Since we're using next we have to manually check for an End and exit the loop if we get one.

```
next
```

```
Ask
```

```
next
```

```
HistoryStep
```

```
next
```

```
Answer
```

```
next
```

```
End
```

(This example is complete, it can be run "as is" with Python 3.10+ â you'll need to add asyncio.run(main()) to run main)

```
asyncio.run(main())
```

```
main
```

A mermaid diagram for this graph can be generated with the following code:

```
from ai_q_and_a_graph import Ask, question_graph

question_graph.mermaid_code(start_node=Ask)
```

```
from ai_q_and_a_graph import Ask, question_graph

question_graph.mermaid_code(start_node=Ask)
```

```
---
title: question_graph
---
stateDiagram-v2
  [*] --> Ask
  Ask --> Answer
  Answer --> Evaluate
  Evaluate --> Reprimand
  Evaluate --> [*]
  Reprimand --> Ask
```

```
---
title: question_graph
---
stateDiagram-v2
  [*] --> Ask
  Ask --> Answer
  Answer --> Evaluate
  Evaluate --> Reprimand
  Evaluate --> [*]
  Reprimand --> Ask
```

You maybe have noticed that although this example transfers control flow out of the graph run, we're still using rich's Prompt.ask to get user input, with the process hanging while we wait for the user to enter a response. For an example of genuine out-of-process control flow, see the question graph example.

```
Prompt.ask
```

## Iterating Over a Graph

### Using Graph.iter for async for iteration

```
Graph.iter
```

```
async for
```

Sometimes you want direct control or insight into each node as the graph executes. The easiest way to do that is with the Graph.iter method, which returns a context manager that yields a GraphRun object. The GraphRun is an async-iterable over the nodes of your graph, allowing you to record or modify them as they execute.

```
Graph.iter
```

```
GraphRun
```

```
GraphRun
```

Here's an example:

```
from __future__ import annotations as _annotations

from dataclasses import dataclass
from pydantic_graph import Graph, BaseNode, End, GraphRunContext


@dataclass
class CountDownState:
    counter: int


@dataclass
class CountDown(BaseNode[CountDownState]):
    async def run(self, ctx: GraphRunContext[CountDownState]) -> CountDown | End[int]:
        if ctx.state.counter <= 0:
            return End(ctx.state.counter)
        ctx.state.counter -= 1
        return CountDown()


count_down_graph = Graph(nodes=[CountDown])


async def main():
    state = CountDownState(counter=3)
    async with count_down_graph.iter(CountDown(), state=state) as run:  # (1)!
        async for node in run:  # (2)!
            print('Node:', node)
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: End(data=0)
    print('Final result:', run.result.output)  # (3)!
    #> Final result: 0
    print('History snapshots:', [step.data_snapshot() for step in run.history])
    """
    History snapshots:
    [CountDown(), CountDown(), CountDown(), CountDown(), End(data=0)]
    """
```

```
from __future__ import annotations as _annotations

from dataclasses import dataclass
from pydantic_graph import Graph, BaseNode, End, GraphRunContext


@dataclass
class CountDownState:
    counter: int


@dataclass
class CountDown(BaseNode[CountDownState]):
    async def run(self, ctx: GraphRunContext[CountDownState]) -> CountDown | End[int]:
        if ctx.state.counter <= 0:
            return End(ctx.state.counter)
        ctx.state.counter -= 1
        return CountDown()


count_down_graph = Graph(nodes=[CountDown])


async def main():
    state = CountDownState(counter=3)
    async with count_down_graph.iter(CountDown(), state=state) as run:  # (1)!
        async for node in run:  # (2)!
            print('Node:', node)
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: End(data=0)
    print('Final result:', run.result.output)  # (3)!
    #> Final result: 0
    print('History snapshots:', [step.data_snapshot() for step in run.history])
    """
    History snapshots:
    [CountDown(), CountDown(), CountDown(), CountDown(), End(data=0)]
    """
```

1. Graph.iter(...) returns a GraphRun.
2. Here, we step through each node as it is executed.
3. Once the graph returns an End, the loop ends, and run.final_result becomes a GraphRunResult containing the final outcome (0 here).

```
Graph.iter(...)
```

```
GraphRun
```

```
End
```

```
run.final_result
```

```
GraphRunResult
```

```
0
```

### Using GraphRun.next(node) manually

```
GraphRun.next(node)
```

Alternatively, you can drive iteration manually with the GraphRun.next method, which allows you to pass in whichever node you want to run next. You can modify or selectively skip nodes this way.

```
GraphRun.next
```

Below is a contrived example that stops whenever the counter is at 2, ignoring any node runs beyond that:

```
from pydantic_graph import End
from count_down import CountDown, CountDownState, count_down_graph


async def main():
    state = CountDownState(counter=5)
    async with count_down_graph.iter(CountDown(), state=state) as run:
        node = run.next_node  # (1)!
        while not isinstance(node, End):  # (2)!
            print('Node:', node)
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: CountDown()
            if state.counter == 2:
                break  # (3)!
            node = await run.next(node)  # (4)!

        print(run.result)  # (5)!
        #> None

        for step in run.history:  # (6)!
            print('History Step:', step.data_snapshot(), step.state)
            #> History Step: CountDown() CountDownState(counter=4)
            #> History Step: CountDown() CountDownState(counter=3)
            #> History Step: CountDown() CountDownState(counter=2)
```

```
from pydantic_graph import End
from count_down import CountDown, CountDownState, count_down_graph


async def main():
    state = CountDownState(counter=5)
    async with count_down_graph.iter(CountDown(), state=state) as run:
        node = run.next_node  # (1)!
        while not isinstance(node, End):  # (2)!
            print('Node:', node)
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: CountDown()
            #> Node: CountDown()
            if state.counter == 2:
                break  # (3)!
            node = await run.next(node)  # (4)!

        print(run.result)  # (5)!
        #> None

        for step in run.history:  # (6)!
            print('History Step:', step.data_snapshot(), step.state)
            #> History Step: CountDown() CountDownState(counter=4)
            #> History Step: CountDown() CountDownState(counter=3)
            #> History Step: CountDown() CountDownState(counter=2)
```

1. We start by grabbing the first node that will be run in the agent's graph.
2. The agent run is finished once an End node has been produced; instances of End cannot be passed to next.
3. If the user decides to stop early, we break out of the loop. The graph run won't have a real final result in that case (run.final_result remains None).
4. At each step, we call await run.next(node) to run it and get the next node (or an End).
5. Because we did not continue the run until it finished, the result is not set.
6. The run's history is still populated with the steps we executed so far.

```
End
```

```
End
```

```
next
```

```
run.final_result
```

```
None
```

```
await run.next(node)
```

```
End
```

```
result
```

## Dependency Injection

As with PydanticAI, pydantic-graph supports dependency injection via a generic parameter on Graph and BaseNode, and the GraphRunContext.deps field.

```
pydantic-graph
```

```
Graph
```

```
BaseNode
```

```
GraphRunContext.deps
```

As an example of dependency injection, let's modify the DivisibleBy5 example above to use a ProcessPoolExecutor to run the compute load in a separate process (this is a contrived example, ProcessPoolExecutor wouldn't actually improve performance in this example):

```
DivisibleBy5
```

```
ProcessPoolExecutor
```

```
ProcessPoolExecutor
```

```
from __future__ import annotations

import asyncio
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class GraphDeps:
    executor: ProcessPoolExecutor


@dataclass
class DivisibleBy5(BaseNode[None, GraphDeps, int]):
    foo: int

    async def run(
        self,
        ctx: GraphRunContext[None, GraphDeps],
    ) -> Increment | End[int]:
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return Increment(self.foo)


@dataclass
class Increment(BaseNode[None, GraphDeps]):
    foo: int

    async def run(self, ctx: GraphRunContext[None, GraphDeps]) -> DivisibleBy5:
        loop = asyncio.get_running_loop()
        compute_result = await loop.run_in_executor(
            ctx.deps.executor,
            self.compute,
        )
        return DivisibleBy5(compute_result)

    def compute(self) -> int:
        return self.foo + 1


fives_graph = Graph(nodes=[DivisibleBy5, Increment])


async def main():
    with ProcessPoolExecutor() as executor:
        deps = GraphDeps(executor)
        result = await fives_graph.run(DivisibleBy5(3), deps=deps)
    print(result.output)
    #> 5
    # the full history is quite verbose (see below), so we'll just print the summary
    print([item.data_snapshot() for item in result.history])
    """
    [
        DivisibleBy5(foo=3),
        Increment(foo=3),
        DivisibleBy5(foo=4),
        Increment(foo=4),
        DivisibleBy5(foo=5),
        End(data=5),
    ]
    """
```

```
from __future__ import annotations

import asyncio
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class GraphDeps:
    executor: ProcessPoolExecutor


@dataclass
class DivisibleBy5(BaseNode[None, GraphDeps, int]):
    foo: int

    async def run(
        self,
        ctx: GraphRunContext[None, GraphDeps],
    ) -> Increment | End[int]:
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return Increment(self.foo)


@dataclass
class Increment(BaseNode[None, GraphDeps]):
    foo: int

    async def run(self, ctx: GraphRunContext[None, GraphDeps]) -> DivisibleBy5:
        loop = asyncio.get_running_loop()
        compute_result = await loop.run_in_executor(
            ctx.deps.executor,
            self.compute,
        )
        return DivisibleBy5(compute_result)

    def compute(self) -> int:
        return self.foo + 1


fives_graph = Graph(nodes=[DivisibleBy5, Increment])


async def main():
    with ProcessPoolExecutor() as executor:
        deps = GraphDeps(executor)
        result = await fives_graph.run(DivisibleBy5(3), deps=deps)
    print(result.output)
    #> 5
    # the full history is quite verbose (see below), so we'll just print the summary
    print([item.data_snapshot() for item in result.history])
    """
    [
        DivisibleBy5(foo=3),
        Increment(foo=3),
        DivisibleBy5(foo=4),
        Increment(foo=4),
        DivisibleBy5(foo=5),
        End(data=5),
    ]
    """
```

(This example is complete, it can be run "as is" with Python 3.10+ â you'll need to add asyncio.run(main()) to run main)

```
asyncio.run(main())
```

```
main
```

## Mermaid Diagrams

Pydantic Graph can generate mermaid stateDiagram-v2 diagrams for graphs, as shown above.

```
stateDiagram-v2
```

These diagrams can be generated with:

* Graph.mermaid_code to generate the mermaid code for a graph
* Graph.mermaid_image to generate an image of the graph using mermaid.ink
* Graph.mermaid_save to generate an image of the graph using mermaid.ink and save it to a file

```
Graph.mermaid_code
```

```
Graph.mermaid_image
```

```
Graph.mermaid_save
```

Beyond the diagrams shown above, you can also customize mermaid diagrams with the following options:

* Edge allows you to apply a label to an edge
* BaseNode.docstring_notes and BaseNode.get_note allows you to add notes to nodes
* The highlighted_nodes parameter allows you to highlight specific node(s) in the diagram

```
Edge
```

```
BaseNode.docstring_notes
```

```
BaseNode.get_note
```

```
highlighted_nodes
```

Putting that together, we can edit the last ai_q_and_a_graph.py example to:

```
ai_q_and_a_graph.py
```

* add labels to some edges
* add a note to the Ask node
* highlight the Answer node
* save the diagram as a PNG image to file

```
Ask
```

```
Answer
```

```
PNG
```

```
...
from typing import Annotated

from pydantic_graph import BaseNode, End, Graph, GraphRunContext, Edge

...

@dataclass
class Ask(BaseNode[QuestionState]):
    """Generate question using GPT-4o."""
    docstring_notes = True
    async def run(
        self, ctx: GraphRunContext[QuestionState]
    ) -> Annotated[Answer, Edge(label='Ask the question')]:
        ...

...

@dataclass
class Evaluate(BaseNode[QuestionState]):
    answer: str

    async def run(
            self,
            ctx: GraphRunContext[QuestionState],
    ) -> Annotated[End[str], Edge(label='success')] | Reprimand:
        ...

...

question_graph.mermaid_save('image.png', highlighted_nodes=[Answer])
```

```
...
from typing import Annotated

from pydantic_graph import BaseNode, End, Graph, GraphRunContext, Edge

...

@dataclass
class Ask(BaseNode[QuestionState]):
    """Generate question using GPT-4o."""
    docstring_notes = True
    async def run(
        self, ctx: GraphRunContext[QuestionState]
    ) -> Annotated[Answer, Edge(label='Ask the question')]:
        ...

...

@dataclass
class Evaluate(BaseNode[QuestionState]):
    answer: str

    async def run(
            self,
            ctx: GraphRunContext[QuestionState],
    ) -> Annotated[End[str], Edge(label='success')] | Reprimand:
        ...

...

question_graph.mermaid_save('image.png', highlighted_nodes=[Answer])
```

(This example is not complete and cannot be run directly)

This would generate an image that looks like this:

```
---
title: question_graph
---
stateDiagram-v2
  Ask --> Answer: Ask the question
  note right of Ask
    Judge the answer.
    Decide on next step.
  end note
  Answer --> Evaluate
  Evaluate --> Reprimand
  Evaluate --> [*]: success
  Reprimand --> Ask

classDef highlighted fill:#fdff32
class Answer highlighted
```

```
---
title: question_graph
---
stateDiagram-v2
  Ask --> Answer: Ask the question
  note right of Ask
    Judge the answer.
    Decide on next step.
  end note
  Answer --> Evaluate
  Evaluate --> Reprimand
  Evaluate --> [*]: success
  Reprimand --> Ask

classDef highlighted fill:#fdff32
class Answer highlighted
```

### Setting Direction of the State Diagram

You can specify the direction of the state diagram using one of the following values:

* 'TB': Top to bottom, the diagram flows vertically from top to bottom.
* 'LR': Left to right, the diagram flows horizontally from left to right.
* 'RL': Right to left, the diagram flows horizontally from right to left.
* 'BT': Bottom to top, the diagram flows vertically from bottom to top.

```
'TB'
```

```
'LR'
```

```
'RL'
```

```
'BT'
```

Here is an example of how to do this using 'Left to Right' (LR) instead of the default 'Top to Bottom' (TB):
vending_machine_diagram.pyfrom vending_machine import InsertCoin, vending_machine_graph

vending_machine_graph.mermaid_code(start_node=InsertCoin, direction='LR')

```
from vending_machine import InsertCoin, vending_machine_graph

vending_machine_graph.mermaid_code(start_node=InsertCoin, direction='LR')
```

```
from vending_machine import InsertCoin, vending_machine_graph

vending_machine_graph.mermaid_code(start_node=InsertCoin, direction='LR')
```

```
---
title: vending_machine_graph
---
stateDiagram-v2
  direction LR
  [*] --> InsertCoin
  InsertCoin --> CoinsInserted
  CoinsInserted --> SelectProduct
  CoinsInserted --> Purchase
  SelectProduct --> Purchase
  Purchase --> InsertCoin
  Purchase --> SelectProduct
  Purchase --> [*]
```

```
---
title: vending_machine_graph
---
stateDiagram-v2
  direction LR
  [*] --> InsertCoin
  InsertCoin --> CoinsInserted
  CoinsInserted --> SelectProduct
  CoinsInserted --> Purchase
  SelectProduct --> Purchase
  Purchase --> InsertCoin
  Purchase --> SelectProduct
  Purchase --> [*]
```

