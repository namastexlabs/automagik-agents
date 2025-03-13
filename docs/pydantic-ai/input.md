# Image and Audio Input

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# Image and Audio Input

Some LLMs are now capable of understanding both audio and image content.

## Image Input

Info

Some models do not support image input. Please check the model's documentation to confirm whether it supports image input.

If you have a direct URL for the image, you can use ImageUrl:

```
ImageUrl
```

```
from pydantic_ai import Agent, ImageUrl

agent = Agent(model='openai:gpt-4o')
result = agent.run_sync(
    [
        'What company is this logo from?',
        ImageUrl(url='https://iili.io/3Hs4FMg.png'),
    ]
)
print(result.data)
#> This is the logo for Pydantic, a data validation and settings management library in Python.
```

```
from pydantic_ai import Agent, ImageUrl

agent = Agent(model='openai:gpt-4o')
result = agent.run_sync(
    [
        'What company is this logo from?',
        ImageUrl(url='https://iili.io/3Hs4FMg.png'),
    ]
)
print(result.data)
#> This is the logo for Pydantic, a data validation and settings management library in Python.
```

If you have the image locally, you can also use BinaryContent:

```
BinaryContent
```

```
import httpx

from pydantic_ai import Agent, BinaryContent

image_response = httpx.get('https://iili.io/3Hs4FMg.png')  # Pydantic logo

agent = Agent(model='openai:gpt-4o')
result = agent.run_sync(
    [
        'What company is this logo from?',
        BinaryContent(data=image_response.content, media_type='image/png'),  # (1)!
    ]
)
print(result.data)
#> This is the logo for Pydantic, a data validation and settings management library in Python.
```

```
import httpx

from pydantic_ai import Agent, BinaryContent

image_response = httpx.get('https://iili.io/3Hs4FMg.png')  # Pydantic logo

agent = Agent(model='openai:gpt-4o')
result = agent.run_sync(
    [
        'What company is this logo from?',
        BinaryContent(data=image_response.content, media_type='image/png'),  # (1)!
    ]
)
print(result.data)
#> This is the logo for Pydantic, a data validation and settings management library in Python.
```

1. To ensure the example is runnable we download this image from the web, but you can also use Path().read_bytes() to read a local file's contents.

```
Path().read_bytes()
```

## Audio Input

Info

Some models do not support audio input. Please check the model's documentation to confirm whether it supports audio input.

You can provide audio input using either AudioUrl or BinaryContent. The process is analogous to the examples above.

```
AudioUrl
```

```
BinaryContent
```

