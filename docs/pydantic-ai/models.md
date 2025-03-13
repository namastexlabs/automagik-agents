# Models

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# Models

PydanticAI is Model-agnostic and has built in support for the following model providers:

* OpenAI
* Anthropic
* Gemini via two different APIs: Generative Language API and VertexAI API
* Ollama
* Groq
* Mistral
* Cohere
* Bedrock

See OpenAI-compatible models for more examples on how to use models such as OpenRouter, and Grok (xAI) that support the OpenAI SDK.

You can also add support for other models.

PydanticAI also comes with TestModel and FunctionModel for testing and development.

```
TestModel
```

```
FunctionModel
```

To use each model provider, you need to configure your local environment and make sure you have the right packages installed.

## Models, Interfaces, and Providers

PydanticAI uses a few key terms to describe how it interacts with different LLMs:

* Model: This refers to the specific LLM model you want to handle your requests (e.g., gpt-4o, claude-3-5-sonnet-latest,
    gemini-1.5-flash). It's the "brain" that processes your prompts and generates responses.  You specify the
    Model as a parameter to the Interface.
* Interface: This refers to a PydanticAI class used to make requests following a specific LLM API
    (generally by wrapping a vendor-provided SDK, like the openai python SDK). These classes implement a
    vendor-SDK-agnostic API, ensuring a single PydanticAI agent is portable to different LLM vendors without
    any other code changes just by swapping out the Interface it uses. Currently, interface classes are named
    roughly in the format <VendorSdk>Model, for example, we have OpenAIModel, AnthropicModel, GeminiModel,
    etc. These Model classes will soon be renamed to <VendorSdk>Interface to reflect this terminology better.
* Provider: This refers to Interface-specific classes which handle the authentication and connections to an LLM vendor.
    Passing a non-default Provider as a parameter to an Interface is how you can ensure that your agent will make
    requests to a specific endpoint, or make use of a specific approach to authentication (e.g., you can use Vertex-specific
    auth with the GeminiModel by way of the VertexProvider). In particular, this is how you can make use of an AI gateway,
    or an LLM vendor that offers API compatibility with the vendor SDK used by an existing interface (such as OpenAIModel).

```
gpt-4o
```

```
claude-3-5-sonnet-latest
```

```
gemini-1.5-flash
```

```
openai
```

```
<VendorSdk>Model
```

```
OpenAIModel
```

```
AnthropicModel
```

```
GeminiModel
```

```
Model
```

```
<VendorSdk>Interface
```

```
GeminiModel
```

```
VertexProvider
```

```
OpenAIModel
```

In short, you select a model, PydanticAI uses the appropriate interface class, and the provider handles the
connection and authentication to the underlying service.

## OpenAI

### Install

To use OpenAI models, you need to either install pydantic-ai, or install pydantic-ai-slim with the openai optional group:

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
openai
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

### Configuration

To use OpenAIModel through their main API, go to platform.openai.com and follow your nose until you find the place to generate an API key.

```
OpenAIModel
```

### Environment variable

Once you have the API key, you can set it as an environment variable:

```
export OPENAI_API_KEY='your-api-key'
```

```
export OPENAI_API_KEY='your-api-key'
```

You can then use OpenAIModel by name:

```
OpenAIModel
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')
...
```

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')
...
```

Or initialise the model directly with just the model name:

openai_model_init.pyfrom pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel('gpt-4o')
agent = Agent(model)
...

By default, the OpenAIModel uses the OpenAIProvider
with the base_url set to https://api.openai.com/v1.

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel('gpt-4o')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel('gpt-4o')
agent = Agent(model)
...
```

```
OpenAIModel
```

```
OpenAIProvider
```

```
base_url
```

```
https://api.openai.com/v1
```

### provider argument

```
provider
```

You can provide a custom Provider via the provider argument:

```
Provider
```

```
provider
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel('gpt-4o', provider=OpenAIProvider(api_key='your-api-key'))
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel('gpt-4o', provider=OpenAIProvider(api_key='your-api-key'))
agent = Agent(model)
...
```

### Custom OpenAI Client

OpenAIProvider also accepts a custom AsyncOpenAI client via the
openai_client parameter, so you can customise the
organization, project, base_url etc. as defined in the OpenAI API docs.

```
OpenAIProvider
```

```
AsyncOpenAI
```

```
openai_client
```

```
organization
```

```
project
```

```
base_url
```

You could also use the AsyncAzureOpenAI
client to use the Azure OpenAI API.

```
AsyncAzureOpenAI
```

```
from openai import AsyncAzureOpenAI

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

client = AsyncAzureOpenAI(
    azure_endpoint='...',
    api_version='2024-07-01-preview',
    api_key='your-api-key',
)

model = OpenAIModel(
    'gpt-4o',
    provider=OpenAIProvider(openai_client=client),
)
agent = Agent(model)
...
```

```
from openai import AsyncAzureOpenAI

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

client = AsyncAzureOpenAI(
    azure_endpoint='...',
    api_version='2024-07-01-preview',
    api_key='your-api-key',
)

model = OpenAIModel(
    'gpt-4o',
    provider=OpenAIProvider(openai_client=client),
)
agent = Agent(model)
...
```

## Anthropic

### Install

To use AnthropicModel models, you need to either install pydantic-ai, or install pydantic-ai-slim with the anthropic optional group:

```
AnthropicModel
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
anthropic
```

```
pip install 'pydantic-ai-slim[anthropic]'
```

```
pip install 'pydantic-ai-slim[anthropic]'
```

```
uv add 'pydantic-ai-slim[anthropic]'
```

```
uv add 'pydantic-ai-slim[anthropic]'
```

### Configuration

To use Anthropic through their API, go to console.anthropic.com/settings/keys to generate an API key.

AnthropicModelName contains a list of available Anthropic models.

```
AnthropicModelName
```

### Environment variable

Once you have the API key, you can set it as an environment variable:

```
export ANTHROPIC_API_KEY='your-api-key'
```

```
export ANTHROPIC_API_KEY='your-api-key'
```

You can then use AnthropicModel by name:

```
AnthropicModel
```

```
from pydantic_ai import Agent

agent = Agent('anthropic:claude-3-5-sonnet-latest')
...
```

```
from pydantic_ai import Agent

agent = Agent('anthropic:claude-3-5-sonnet-latest')
...
```

Or initialise the model directly with just the model name:

```
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel

model = AnthropicModel('claude-3-5-sonnet-latest')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel

model = AnthropicModel('claude-3-5-sonnet-latest')
agent = Agent(model)
...
```

### api_key argument

```
api_key
```

If you don't want to or can't set the environment variable, you can pass it at runtime via the api_key argument:

```
api_key
```

```
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel

model = AnthropicModel('claude-3-5-sonnet-latest', api_key='your-api-key')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel

model = AnthropicModel('claude-3-5-sonnet-latest', api_key='your-api-key')
agent = Agent(model)
...
```

## Gemini

### Install

To use GeminiModel models, you just need to install pydantic-ai or pydantic-ai-slim, no extra dependencies are required.

```
GeminiModel
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

### Configuration

GeminiModel let's you use the Google's Gemini models through their Generative Language API, generativelanguage.googleapis.com.

```
GeminiModel
```

```
generativelanguage.googleapis.com
```

GeminiModelName contains a list of available Gemini models that can be used through this interface.

```
GeminiModelName
```

To use GeminiModel, go to aistudio.google.com and select "Create API key".

```
GeminiModel
```

### Environment variable

Once you have the API key, you can set it as an environment variable:

```
export GEMINI_API_KEY=your-api-key
```

```
export GEMINI_API_KEY=your-api-key
```

You can then use GeminiModel by name:

```
GeminiModel
```

```
from pydantic_ai import Agent

agent = Agent('google-gla:gemini-2.0-flash')
...
```

```
from pydantic_ai import Agent

agent = Agent('google-gla:gemini-2.0-flash')
...
```

Note

The google-gla provider prefix represents the Google Generative Language API for GeminiModels.
google-vertex is used with Vertex AI.

```
google-gla
```

```
GeminiModel
```

```
google-vertex
```

Or initialise the model directly with just the model name and provider:

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

model = GeminiModel('gemini-2.0-flash', provider='google-gla')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

model = GeminiModel('gemini-2.0-flash', provider='google-gla')
agent = Agent(model)
...
```

### provider argument

```
provider
```

You can provide a custom Provider via the provider argument:

```
Provider
```

```
provider
```

gemini_model_provider.pyfrom pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleGLAProvider(api_key='your-api-key')
)
agent = Agent(model)
...

You can also customize the GoogleGLAProvider with a custom http_client:
gemini_model_custom_provider.pyfrom httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

custom_http_client = AsyncClient(timeout=30)
model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key='your-api-key', http_client=custom_http_client),
)
agent = Agent(model)
...

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleGLAProvider(api_key='your-api-key')
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleGLAProvider(api_key='your-api-key')
)
agent = Agent(model)
...
```

```
GoogleGLAProvider
```

```
http_client
```

```
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

custom_http_client = AsyncClient(timeout=30)
model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key='your-api-key', http_client=custom_http_client),
)
agent = Agent(model)
...
```

```
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

custom_http_client = AsyncClient(timeout=30)
model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key='your-api-key', http_client=custom_http_client),
)
agent = Agent(model)
...
```

## Gemini via VertexAI

If you are an enterprise user, you should use the google-vertex provider with GeminiModel which uses the *-aiplatform.googleapis.com API.

```
google-vertex
```

```
GeminiModel
```

```
*-aiplatform.googleapis.com
```

GeminiModelName contains a list of available Gemini models that can be used through this interface.

```
GeminiModelName
```

### Install

To use the google-vertex provider with GeminiModel, you need to either install
pydantic-ai, or install pydantic-ai-slim with the vertexai optional group:

```
google-vertex
```

```
GeminiModel
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
vertexai
```

```
pip install 'pydantic-ai-slim[vertexai]'
```

```
pip install 'pydantic-ai-slim[vertexai]'
```

```
uv add 'pydantic-ai-slim[vertexai]'
```

```
uv add 'pydantic-ai-slim[vertexai]'
```

### Configuration

This interface has a number of advantages over generativelanguage.googleapis.com documented above:

```
generativelanguage.googleapis.com
```

1. The VertexAI API comes with more enterprise readiness guarantees.
2. You can
   purchase provisioned throughput
   with VertexAI to guarantee capacity.
3. If you're running PydanticAI inside GCP, you don't need to set up authentication, it should "just work".
4. You can decide which region to use, which might be important from a regulatory perspective,
   and might improve latency.

The big disadvantage is that for local development you may need to create and configure a "service account", which I've found extremely painful to get right in the past.

Whichever way you authenticate, you'll need to have VertexAI enabled in your GCP account.

### Application default credentials

Luckily if you're running PydanticAI inside GCP, or you have the gcloud CLI installed and configured, you should be able to use VertexAIModel without any additional setup.

```
gcloud
```

```
VertexAIModel
```

To use VertexAIModel, with application default credentials configured (e.g. with gcloud), you can simply use:

```
VertexAIModel
```

```
gcloud
```

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

model = GeminiModel('gemini-2.0-flash', provider='google-vertex')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

model = GeminiModel('gemini-2.0-flash', provider='google-vertex')
agent = Agent(model)
...
```

Internally this uses google.auth.default() from the google-auth package to obtain credentials.

```
google.auth.default()
```

```
google-auth
```

Won't fail until agent.run()

```
agent.run()
```

Because google.auth.default() requires network requests and can be slow, it's not run until you call agent.run().

```
google.auth.default()
```

```
agent.run()
```

You may also need to pass the project_id argument to GoogleVertexProvider if application default credentials don't set a project, if you pass project_id and it conflicts with the project set by application default credentials, an error is raised.

```
project_id
```

```
GoogleVertexProvider
```

```
project_id
```

### Service account

If instead of application default credentials, you want to authenticate with a service account, you'll need to create a service account, add it to your GCP project (note: AFAIK this step is necessary even if you created the service account within the project), give that service account the "Vertex AI Service Agent" role, and download the service account JSON file.

Once you have the JSON file, you can use it thus:

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleVertexProvider(service_account_file='path/to/service-account.json'),
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleVertexProvider(service_account_file='path/to/service-account.json'),
)
agent = Agent(model)
...
```

### Customising region

Whichever way you authenticate, you can specify which region requests will be sent to via the region argument.

```
region
```

Using a region close to your application can improve latency and might be important from a regulatory perspective.

vertexai_region.pyfrom pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleVertexProvider(region='asia-east1')
)
agent = Agent(model)
...

You can also customize the GoogleVertexProvider with a custom http_client:
vertexai_custom_provider.pyfrom httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

custom_http_client = AsyncClient(timeout=30)
model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleVertexProvider(region='asia-east1', http_client=custom_http_client),
)
agent = Agent(model)
...

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleVertexProvider(region='asia-east1')
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleVertexProvider(region='asia-east1')
)
agent = Agent(model)
...
```

```
GoogleVertexProvider
```

```
http_client
```

```
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

custom_http_client = AsyncClient(timeout=30)
model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleVertexProvider(region='asia-east1', http_client=custom_http_client),
)
agent = Agent(model)
...
```

```
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

custom_http_client = AsyncClient(timeout=30)
model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleVertexProvider(region='asia-east1', http_client=custom_http_client),
)
agent = Agent(model)
...
```

## Groq

### Install

To use GroqModel, you need to either install pydantic-ai, or install pydantic-ai-slim with the groq optional group:

```
GroqModel
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
groq
```

```
pip install 'pydantic-ai-slim[groq]'
```

```
pip install 'pydantic-ai-slim[groq]'
```

```
uv add 'pydantic-ai-slim[groq]'
```

```
uv add 'pydantic-ai-slim[groq]'
```

### Configuration

To use Groq through their API, go to console.groq.com/keys and follow your nose until you find the place to generate an API key.

GroqModelName contains a list of available Groq models.

```
GroqModelName
```

### Environment variable

Once you have the API key, you can set it as an environment variable:

```
export GROQ_API_KEY='your-api-key'
```

```
export GROQ_API_KEY='your-api-key'
```

You can then use GroqModel by name:

```
GroqModel
```

```
from pydantic_ai import Agent

agent = Agent('groq:llama-3.3-70b-versatile')
...
```

```
from pydantic_ai import Agent

agent = Agent('groq:llama-3.3-70b-versatile')
...
```

Or initialise the model directly with just the model name:

```
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

model = GroqModel('llama-3.3-70b-versatile')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

model = GroqModel('llama-3.3-70b-versatile')
agent = Agent(model)
...
```

### api_key argument

```
api_key
```

If you don't want to or can't set the environment variable, you can pass it at runtime via the api_key argument:

```
api_key
```

```
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

model = GroqModel('llama-3.3-70b-versatile', api_key='your-api-key')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

model = GroqModel('llama-3.3-70b-versatile', api_key='your-api-key')
agent = Agent(model)
...
```

## Mistral

### Install

To use MistralModel, you need to either install pydantic-ai, or install pydantic-ai-slim with the mistral optional group:

```
MistralModel
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
mistral
```

```
pip install 'pydantic-ai-slim[mistral]'
```

```
pip install 'pydantic-ai-slim[mistral]'
```

```
uv add 'pydantic-ai-slim[mistral]'
```

```
uv add 'pydantic-ai-slim[mistral]'
```

### Configuration

To use Mistral through their API, go to console.mistral.ai/api-keys/ and follow your nose until you find the place to generate an API key.

MistralModelName contains a list of the most popular Mistral models.

```
MistralModelName
```

### Environment variable

Once you have the API key, you can set it as an environment variable:

```
export MISTRAL_API_KEY='your-api-key'
```

```
export MISTRAL_API_KEY='your-api-key'
```

You can then use MistralModel by name:

```
MistralModel
```

```
from pydantic_ai import Agent

agent = Agent('mistral:mistral-large-latest')
...
```

```
from pydantic_ai import Agent

agent = Agent('mistral:mistral-large-latest')
...
```

Or initialise the model directly with just the model name:

```
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

model = MistralModel('mistral-small-latest')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

model = MistralModel('mistral-small-latest')
agent = Agent(model)
...
```

### api_key argument

```
api_key
```

If you don't want to or can't set the environment variable, you can pass it at runtime via the api_key argument:

```
api_key
```

```
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

model = MistralModel('mistral-small-latest', api_key='your-api-key')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

model = MistralModel('mistral-small-latest', api_key='your-api-key')
agent = Agent(model)
...
```

## Cohere

### Install

To use CohereModel, you need to either install pydantic-ai, or install pydantic-ai-slim with the cohere optional group:

```
CohereModel
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
cohere
```

```
pip install 'pydantic-ai-slim[cohere]'
```

```
pip install 'pydantic-ai-slim[cohere]'
```

```
uv add 'pydantic-ai-slim[cohere]'
```

```
uv add 'pydantic-ai-slim[cohere]'
```

### Configuration

To use Cohere through their API, go to dashboard.cohere.com/api-keys and follow your nose until you find the place to generate an API key.

CohereModelName contains a list of the most popular Cohere models.

```
CohereModelName
```

### Environment variable

Once you have the API key, you can set it as an environment variable:

```
export CO_API_KEY='your-api-key'
```

```
export CO_API_KEY='your-api-key'
```

You can then use CohereModel by name:

```
CohereModel
```

```
from pydantic_ai import Agent

agent = Agent('cohere:command')
...
```

```
from pydantic_ai import Agent

agent = Agent('cohere:command')
...
```

Or initialise the model directly with just the model name:

```
from pydantic_ai import Agent
from pydantic_ai.models.cohere import CohereModel

model = CohereModel('command', api_key='your-api-key')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.cohere import CohereModel

model = CohereModel('command', api_key='your-api-key')
agent = Agent(model)
...
```

### api_key argument

```
api_key
```

If you don't want to or can't set the environment variable, you can pass it at runtime via the api_key argument:

```
api_key
```

```
from pydantic_ai import Agent
from pydantic_ai.models.cohere import CohereModel

model = CohereModel('command', api_key='your-api-key')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.cohere import CohereModel

model = CohereModel('command', api_key='your-api-key')
agent = Agent(model)
...
```

## Bedrock

### Install

To use BedrockConverseModel, you need to either install pydantic-ai, or install pydantic-ai-slim with the bedrock optional group:

```
BedrockConverseModel
```

```
pydantic-ai
```

```
pydantic-ai-slim
```

```
bedrock
```

```
pip install 'pydantic-ai-slim[bedrock]'
```

```
pip install 'pydantic-ai-slim[bedrock]'
```

```
uv add 'pydantic-ai-slim[bedrock]'
```

```
uv add 'pydantic-ai-slim[bedrock]'
```

### Configuration

To use AWS Bedrock, you'll need an AWS account with Bedrock enabled and appropriate credentials. You can use either AWS credentials directly or a pre-configured boto3 client.

BedrockModelName contains a list of available Bedrock models, including models from Anthropic, Amazon, Cohere, Meta, and Mistral.

```
BedrockModelName
```

### Environment variables

You can set your AWS credentials as environment variables:

```
export AWS_ACCESS_KEY_ID='your-access-key'
export AWS_SECRET_ACCESS_KEY='your-secret-key'
export AWS_REGION='us-east-1'  # or your preferred region
```

```
export AWS_ACCESS_KEY_ID='your-access-key'
export AWS_SECRET_ACCESS_KEY='your-secret-key'
export AWS_REGION='us-east-1'  # or your preferred region
```

You can then use BedrockConverseModel by name:

```
BedrockConverseModel
```

```
from pydantic_ai import Agent

agent = Agent('bedrock:anthropic.claude-3-sonnet-20240229-v1:0')
...
```

```
from pydantic_ai import Agent

agent = Agent('bedrock:anthropic.claude-3-sonnet-20240229-v1:0')
...
```

Or initialize the model directly with just the model name:

```
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel

model = BedrockConverseModel('anthropic.claude-3-sonnet-20240229-v1:0')
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel

model = BedrockConverseModel('anthropic.claude-3-sonnet-20240229-v1:0')
agent = Agent(model)
...
```

### provider argument

```
provider
```

You can provide a custom BedrockProvider via the provider argument. This is useful when you want to specify credentials directly or use a custom boto3 client:

```
BedrockProvider
```

```
provider
```

```
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

# Using AWS credentials directly
model = BedrockConverseModel(
    'anthropic.claude-3-sonnet-20240229-v1:0',
    provider=BedrockProvider(
        region_name='us-east-1',
        aws_access_key_id='your-access-key',
        aws_secret_access_key='your-secret-key',
    ),
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

# Using AWS credentials directly
model = BedrockConverseModel(
    'anthropic.claude-3-sonnet-20240229-v1:0',
    provider=BedrockProvider(
        region_name='us-east-1',
        aws_access_key_id='your-access-key',
        aws_secret_access_key='your-secret-key',
    ),
)
agent = Agent(model)
...
```

You can also pass a pre-configured boto3 client:

```
import boto3

from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

# Using a pre-configured boto3 client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
model = BedrockConverseModel(
    'anthropic.claude-3-sonnet-20240229-v1:0',
    provider=BedrockProvider(bedrock_client=bedrock_client),
)
agent = Agent(model)
...
```

```
import boto3

from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

# Using a pre-configured boto3 client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
model = BedrockConverseModel(
    'anthropic.claude-3-sonnet-20240229-v1:0',
    provider=BedrockProvider(bedrock_client=bedrock_client),
)
agent = Agent(model)
...
```

## OpenAI-compatible Models

Many of the models are compatible with OpenAI API, and thus can be used with OpenAIModel in PydanticAI.
Before getting started, check the OpenAI section for installation and configuration instructions.

```
OpenAIModel
```

To use another OpenAI-compatible API, you can make use of the base_url
and api_key arguments from OpenAIProvider:

```
base_url
```

```
api_key
```

```
OpenAIProvider
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'model_name',
    provider=OpenAIProvider(
        base_url='https://<openai-compatible-api-endpoint>.com', api_key='your-api-key'
    ),
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'model_name',
    provider=OpenAIProvider(
        base_url='https://<openai-compatible-api-endpoint>.com', api_key='your-api-key'
    ),
)
agent = Agent(model)
...
```

You can also use the provider argument with a custom provider class like the DeepSeekProvider:

```
provider
```

```
DeepSeekProvider
```

deepseek_model_init_provider_class.pyfrom pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(api_key='your-deepseek-api-key'),
)
agent = Agent(model)
...

You can also customize any provider with a custom http_client:
deepseek_model_init_provider_custom.pyfrom httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

custom_http_client = AsyncClient(timeout=30)
model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(
        api_key='your-deepseek-api-key', http_client=custom_http_client
    ),
)
agent = Agent(model)
...

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(api_key='your-deepseek-api-key'),
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(api_key='your-deepseek-api-key'),
)
agent = Agent(model)
...
```

```
http_client
```

```
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

custom_http_client = AsyncClient(timeout=30)
model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(
        api_key='your-deepseek-api-key', http_client=custom_http_client
    ),
)
agent = Agent(model)
...
```

```
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

custom_http_client = AsyncClient(timeout=30)
model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(
        api_key='your-deepseek-api-key', http_client=custom_http_client
    ),
)
agent = Agent(model)
...
```

### Ollama

To use Ollama, you must first download the Ollama client, and then download a model using the Ollama model library.

You must also ensure the Ollama server is running when trying to make requests to it. For more information, please see the Ollama documentation.

#### Example local usage

With ollama installed, you can run the server with the model you want to use:

```
ollama
```

```
ollama run llama3.2
```

```
ollama run llama3.2
```

(this will pull the llama3.2 model if you don't already have it downloaded)

```
llama3.2
```

Then run your code, here's a minimal example:

```
from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


class CityLocation(BaseModel):
    city: str
    country: str


ollama_model = OpenAIModel(
    model_name='llama3.2', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)
agent = Agent(ollama_model, result_type=CityLocation)

result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
```

```
from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


class CityLocation(BaseModel):
    city: str
    country: str


ollama_model = OpenAIModel(
    model_name='llama3.2', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)
agent = Agent(ollama_model, result_type=CityLocation)

result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
```

#### Example using a remote server

```
from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

ollama_model = OpenAIModel(
    model_name='qwen2.5-coder:7b',  # (1)!
    provider=OpenAIProvider(base_url='http://192.168.1.74:11434/v1'),  # (2)!
)


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent(model=ollama_model, result_type=CityLocation)

result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
```

```
from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

ollama_model = OpenAIModel(
    model_name='qwen2.5-coder:7b',  # (1)!
    provider=OpenAIProvider(base_url='http://192.168.1.74:11434/v1'),  # (2)!
)


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent(model=ollama_model, result_type=CityLocation)

result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
```

1. The name of the model running on the remote server
2. The url of the remote server

### OpenRouter

To use OpenRouter, first create an API key at openrouter.ai/keys.

Once you have the API key, you can use it with the OpenAIProvider:

```
OpenAIProvider
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'anthropic/claude-3.5-sonnet',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1', api_key='your-openrouter-api-key'
    ),
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'anthropic/claude-3.5-sonnet',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1', api_key='your-openrouter-api-key'
    ),
)
agent = Agent(model)
...
```

### Grok (xAI)

Go to xAI API Console and create an API key.
Once you have the API key, you can use it with the OpenAIProvider:

```
OpenAIProvider
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'grok-2-1212',
    provider=OpenAIProvider(base_url='https://api.x.ai/v1', api_key='your-xai-api-key'),
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'grok-2-1212',
    provider=OpenAIProvider(base_url='https://api.x.ai/v1', api_key='your-xai-api-key'),
)
agent = Agent(model)
...
```

### Perplexity

Follow the Perplexity getting started
guide to create an API key. Then, you can query the Perplexity API with the following:

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'sonar-pro',
    provider=OpenAIProvider(
        base_url='https://api.perplexity.ai', api_key='your-perplexity-api-key'
    ),
)
agent = Agent(model)
...
```

```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'sonar-pro',
    provider=OpenAIProvider(
        base_url='https://api.perplexity.ai', api_key='your-perplexity-api-key'
    ),
)
agent = Agent(model)
...
```

## Implementing Custom Models

To implement support for models not already supported, you will need to subclass the Model abstract base class.

```
Model
```

For streaming, you'll also need to implement the following abstract base class:

* StreamedResponse

```
StreamedResponse
```

The best place to start is to review the source code for existing implementations, e.g. OpenAIModel.

```
OpenAIModel
```

For details on when we'll accept contributions adding new models to PydanticAI, see the contributing guidelines.

## Fallback

You can use FallbackModel to attempt multiple models
in sequence until one returns a successful result. Under the hood, PydanticAI automatically switches
from one model to the next if the current model returns a 4xx or 5xx status code.

```
FallbackModel
```

In the following example, the agent first makes a request to the OpenAI model (which fails due to an invalid API key),
and then falls back to the Anthropic model.

```
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIModel

openai_model = OpenAIModel('gpt-4o', api_key='not-valid')
anthropic_model = AnthropicModel('claude-3-5-sonnet-latest')
fallback_model = FallbackModel(openai_model, anthropic_model)

agent = Agent(fallback_model)
response = agent.run_sync('What is the capital of France?')
print(response.data)
#> Paris

print(response.all_messages())
"""
[
    ModelRequest(
        parts=[
            UserPromptPart(
                content='What is the capital of France?',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            )
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[TextPart(content='Paris', part_kind='text')],
        model_name='claude-3-5-sonnet-latest',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
]
"""
```

```
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIModel

openai_model = OpenAIModel('gpt-4o', api_key='not-valid')
anthropic_model = AnthropicModel('claude-3-5-sonnet-latest')
fallback_model = FallbackModel(openai_model, anthropic_model)

agent = Agent(fallback_model)
response = agent.run_sync('What is the capital of France?')
print(response.data)
#> Paris

print(response.all_messages())
"""
[
    ModelRequest(
        parts=[
            UserPromptPart(
                content='What is the capital of France?',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            )
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[TextPart(content='Paris', part_kind='text')],
        model_name='claude-3-5-sonnet-latest',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
]
"""
```

The ModelResponse message above indicates in the model_name field that the result was returned by the Anthropic model, which is the second model specified in the FallbackModel.

```
ModelResponse
```

```
model_name
```

```
FallbackModel
```

Note

Each model's options should be configured individually. For example, base_url, api_key, and custom clients should be set on each model itself, not on the FallbackModel.

```
base_url
```

```
api_key
```

```
FallbackModel
```

In this next example, we demonstrate the exception-handling capabilities of FallbackModel.
If all models fail, a FallbackExceptionGroup is raised, which
contains all the exceptions encountered during the run execution.

```
FallbackModel
```

```
FallbackExceptionGroup
```

```
run
```

```
from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIModel

openai_model = OpenAIModel('gpt-4o', api_key='not-valid')
anthropic_model = AnthropicModel('claude-3-5-sonnet-latest', api_key='not-valid')
fallback_model = FallbackModel(openai_model, anthropic_model)

agent = Agent(fallback_model)
try:
    response = agent.run_sync('What is the capital of France?')
except* ModelHTTPError as exc_group:
    for exc in exc_group.exceptions:
        print(exc)
```

```
from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIModel

openai_model = OpenAIModel('gpt-4o', api_key='not-valid')
anthropic_model = AnthropicModel('claude-3-5-sonnet-latest', api_key='not-valid')
fallback_model = FallbackModel(openai_model, anthropic_model)

agent = Agent(fallback_model)
try:
    response = agent.run_sync('What is the capital of France?')
except* ModelHTTPError as exc_group:
    for exc in exc_group.exceptions:
        print(exc)
```

Since except* is only supported
in Python 3.11+, we use the exceptiongroup backport
package for earlier Python versions:

```
except*
```

```
exceptiongroup
```

```
from exceptiongroup import catch

from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIModel


def model_status_error_handler(exc_group: BaseExceptionGroup) -> None:
    for exc in exc_group.exceptions:
        print(exc)


openai_model = OpenAIModel('gpt-4o', api_key='not-valid')
anthropic_model = AnthropicModel('claude-3-5-sonnet-latest', api_key='not-valid')
fallback_model = FallbackModel(openai_model, anthropic_model)

agent = Agent(fallback_model)
with catch({ModelHTTPError: model_status_error_handler}):
    response = agent.run_sync('What is the capital of France?')
```

```
from exceptiongroup import catch

from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIModel


def model_status_error_handler(exc_group: BaseExceptionGroup) -> None:
    for exc in exc_group.exceptions:
        print(exc)


openai_model = OpenAIModel('gpt-4o', api_key='not-valid')
anthropic_model = AnthropicModel('claude-3-5-sonnet-latest', api_key='not-valid')
fallback_model = FallbackModel(openai_model, anthropic_model)

agent = Agent(fallback_model)
with catch({ModelHTTPError: model_status_error_handler}):
    response = agent.run_sync('What is the capital of France?')
```

By default, the FallbackModel only moves on to the next model if the current model raises a
ModelHTTPError. You can customize this behavior by
passing a custom fallback_on argument to the FallbackModel constructor.

```
FallbackModel
```

```
ModelHTTPError
```

```
fallback_on
```

```
FallbackModel
```

