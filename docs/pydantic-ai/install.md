# Installation

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# Installation

PydanticAI is available on PyPI as pydantic-ai so installation is as simple as:

```
pydantic-ai
```

```
pip install pydantic-ai
```

```
pip install pydantic-ai
```

```
uv add pydantic-ai
```

```
uv add pydantic-ai
```

(Requires Python 3.9+)

This installs the pydantic_ai package, core dependencies, and libraries required to use all the models
included in PydanticAI. If you want to use a specific model, you can install the "slim" version of PydanticAI.

```
pydantic_ai
```

## Use with Pydantic Logfire

PydanticAI has an excellent (but completely optional) integration with Pydantic Logfire to help you view and understand agent runs.

To use Logfire with PydanticAI, install pydantic-ai or pydantic-ai-slim with the logfire optional group:

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
logfire
```

```
pip install 'pydantic-ai[logfire]'
```

```
pip install 'pydantic-ai[logfire]'
```

```
uv add 'pydantic-ai[logfire]'
```

```
uv add 'pydantic-ai[logfire]'
```

From there, follow the Logfire setup docs to configure Logfire.

## Running Examples

We distribute the pydantic_ai_examples directory as a separate PyPI package (pydantic-ai-examples) to make examples extremely easy to customize and run.

```
pydantic_ai_examples
```

```
pydantic-ai-examples
```

To install examples, use the examples optional group:

```
examples
```

```
pip install 'pydantic-ai[examples]'
```

```
pip install 'pydantic-ai[examples]'
```

```
uv add 'pydantic-ai[examples]'
```

```
uv add 'pydantic-ai[examples]'
```

To run the examples, follow instructions in the examples docs.

## Slim Install

If you know which model you're going to use and want to avoid installing superfluous packages, you can use the pydantic-ai-slim package.
For example, if you're using just OpenAIModel, you would run:

```
pydantic-ai-slim
```

```
OpenAIModel
```

```
pip install 'pydantic-ai-slim[openai]'
```

```
pip install 'pydantic-ai-slim[openai]'
```

```
uv add 'pydantic-ai-slim[openai]'
```

```
uv add 'pydantic-ai-slim[openai]'
```

pydantic-ai-slim has the following optional groups:

```
pydantic-ai-slim
```

* logfire â installs logfire PyPI â
* openai â installs openai PyPI â
* vertexai â installs google-auth PyPI â and requests PyPI â
* anthropic â installs anthropic PyPI â
* groq â installs groq PyPI â
* mistral â installs mistralai PyPI â
* cohere - installs cohere PyPI â
* duckduckgo - installs duckduckgo-search PyPI â
* tavily - installs tavily-python PyPI â

```
logfire
```

```
logfire
```

```
openai
```

```
openai
```

```
vertexai
```

```
google-auth
```

```
requests
```

```
anthropic
```

```
anthropic
```

```
groq
```

```
groq
```

```
mistral
```

```
mistralai
```

```
cohere
```

```
cohere
```

```
duckduckgo
```

```
duckduckgo-search
```

```
tavily
```

```
tavily-python
```

See the models documentation for information on which optional dependencies are required for each model.

You can also install dependencies for multiple models and use cases, for example:

```
pip install 'pydantic-ai-slim[openai,vertexai,logfire]'
```

```
pip install 'pydantic-ai-slim[openai,vertexai,logfire]'
```

```
uv add 'pydantic-ai-slim[openai,vertexai,logfire]'
```

```
uv add 'pydantic-ai-slim[openai,vertexai,logfire]'
```

