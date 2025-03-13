# pydantic_ai.common_tools

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.common_tools

```
pydantic_ai.common_tools
```

[](https://ai.pydantic.dev)

### duckduckgo_search_tool

```
duckduckgo_search_tool(
    duckduckgo_client: DDGS | None = None,
    max_results: int | None = None,
)
```

```
duckduckgo_search_tool(
    duckduckgo_client: DDGS | None = None,
    max_results: int | None = None,
)
```

[int](https://docs.python.org/3/library/functions.html#int)

Creates a DuckDuckGo search tool.

Parameters:

```
duckduckgo_client
```

```
DDGS | None
```

The DuckDuckGo search client.

```
None
```

```
max_results
```

```
int | None
```

[int](https://docs.python.org/3/library/functions.html#int)

The maximum number of results. If None, returns results only from the first response.

```
None
```

```
pydantic_ai_slim/pydantic_ai/common_tools/duckduckgo.py
```

```
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
```

```
def duckduckgo_search_tool(duckduckgo_client: DDGS | None = None, max_results: int | None = None):
    """Creates a DuckDuckGo search tool.

    Args:
        duckduckgo_client: The DuckDuckGo search client.
        max_results: The maximum number of results. If None, returns results only from the first response.
    """
    return Tool(
        DuckDuckGoSearchTool(client=duckduckgo_client or DDGS(), max_results=max_results).__call__,
        name='duckduckgo_search',
        description='Searches DuckDuckGo for the given query and returns the results.',
    )
```

```
def duckduckgo_search_tool(duckduckgo_client: DDGS | None = None, max_results: int | None = None):
    """Creates a DuckDuckGo search tool.

    Args:
        duckduckgo_client: The DuckDuckGo search client.
        max_results: The maximum number of results. If None, returns results only from the first response.
    """
    return Tool(
        DuckDuckGoSearchTool(client=duckduckgo_client or DDGS(), max_results=max_results).__call__,
        name='duckduckgo_search',
        description='Searches DuckDuckGo for the given query and returns the results.',
    )
```

[](https://ai.pydantic.dev)

### tavily_search_tool

```
tavily_search_tool(api_key: str)
```

```
tavily_search_tool(api_key: str)
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Creates a Tavily search tool.

Parameters:

```
api_key
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

The Tavily API key.

You can get one by signing up at https://app.tavily.com/home.

```
pydantic_ai_slim/pydantic_ai/common_tools/tavily.py
```

```
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
def tavily_search_tool(api_key: str):
    """Creates a Tavily search tool.

    Args:
        api_key: The Tavily API key.

            You can get one by signing up at [https://app.tavily.com/home](https://app.tavily.com/home).
    """
    return Tool(
        TavilySearchTool(client=AsyncTavilyClient(api_key)).__call__,
        name='tavily_search',
        description='Searches Tavily for the given query and returns the results.',
    )
```

```
def tavily_search_tool(api_key: str):
    """Creates a Tavily search tool.

    Args:
        api_key: The Tavily API key.

            You can get one by signing up at [https://app.tavily.com/home](https://app.tavily.com/home).
    """
    return Tool(
        TavilySearchTool(client=AsyncTavilyClient(api_key)).__call__,
        name='tavily_search',
        description='Searches Tavily for the given query and returns the results.',
    )
```

