# Troubleshooting

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# Troubleshooting

Below are suggestions on how to fix some common errors you might encounter while using PydanticAI. If the issue you're experiencing is not listed below or addressed in the documentation, please feel free to ask in the Pydantic Slack or create an issue on GitHub.

## Jupyter Notebook Errors

### RuntimeError: This event loop is already running

```
RuntimeError: This event loop is already running
```

This error is caused by conflicts between the event loops in Jupyter notebook and PydanticAI's. One way to manage these conflicts is by using nest-asyncio. Namely, before you execute any agent runs, do the following:
import nest_asyncio

nest_asyncio.apply()

Note: This fix also applies to Google Colab.

```
nest-asyncio
```

```
import nest_asyncio

nest_asyncio.apply()
```

```
import nest_asyncio

nest_asyncio.apply()
```

## API Key Configuration

### UserError: API key must be provided or set in the [MODEL]_API_KEY environment variable

```
UserError: API key must be provided or set in the [MODEL]_API_KEY environment variable
```

If you're running into issues with setting the API key for your model, visit the Models page to learn more about how to set an environment variable and/or pass in an api_key argument.

```
api_key
```

## Monitoring HTTPX Requests

You can use custom httpx clients in your models in order to access specific requests, responses, and headers at runtime.

```
httpx
```

It's particularly helpful to use logfire's HTTPX integration to monitor the above.

```
logfire
```

