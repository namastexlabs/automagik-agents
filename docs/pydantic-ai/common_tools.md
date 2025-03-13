# Common Tools

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# Common Tools

PydanticAI ships with native tools that can be used to enhance your agent's capabilities.

## DuckDuckGo Search Tool

The DuckDuckGo search tool allows you to search the web for information. It is built on top of the
DuckDuckGo API.

### Installation

To use duckduckgo_search_tool, you need to install
pydantic-ai-slim with the duckduckgo optional group:

```
duckduckgo_search_tool
```

```
pydantic-ai-slim
```

```
duckduckgo
```

```
pip install 'pydantic-ai-slim[duckduckgo]'
```

```
pip install 'pydantic-ai-slim[duckduckgo]'
```

```
uv add 'pydantic-ai-slim[duckduckgo]'
```

```
uv add 'pydantic-ai-slim[duckduckgo]'
```

### Usage

Here's an example of how you can use the DuckDuckGo search tool with an agent:

```
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

agent = Agent(
    'openai:o3-mini',
    tools=[duckduckgo_search_tool()],
    system_prompt='Search DuckDuckGo for the given query and return the results.',
)

result = agent.run_sync(
    'Can you list the top five highest-grossing animated films of 2025?'
)
print(result.data)
"""
I looked into several sources on animated boxâoffice performance in 2025, and while detailed
rankings can shift as more money is tallied, multiple independent reports have already
highlighted a couple of recordâbreaking shows. For example:

â¢ Ne Zha 2 â News outlets (Variety, Wikipedia's "List of animated feature films of 2025", and others)
    have reported that this Chinese title not only became the highestâgrossing animated film of 2025
    but also broke records as the highestâgrossing nonâEnglish animated film ever. One article noted
    its run exceeded US$1.7 billion.
â¢ Inside Out 2 â According to data shared on Statista and in industry news, this Pixar sequel has been
    on pace to set new records (with some sources even noting it as the highestâgrossing animated film
    ever, as of January 2025).

Beyond those two, some entertainment trade sites (for example, a Just Jared article titled
"Top 10 Highest-Earning Animated Films at the Box Office Revealed") have begun listing a broader
topâ10. Although full consolidated figures can sometimes differ by source and are updated daily during
a boxâoffice run, many of the industry trackers have begun to single out five films as the biggest
earners so far in 2025.

Unfortunately, although multiple articles discuss the "top animated films" of 2025, there isn't yet a
single, universally accepted list with final numbers that names the complete top five. (Boxâoffice
rankings, especially midâyear, can be fluid as films continue to add to their totals.)

Based on what several sources note so far, the two undisputed leaders are:
1. Ne Zha 2
2. Inside Out 2

The remaining top spots (3â5) are reported by some outlets in their "Topâ10 Animated Films"
lists for 2025 but the titles and order can vary depending on the source and the exact cutâoff
date of the data. For the most upâtoâdate and detailed ranking (including the 3rd, 4th, and 5th
highestâgrossing films), I recommend checking resources like:
â¢ Wikipedia's "List of animated feature films of 2025" page
â¢ Boxâoffice tracking sites (such as Box Office Mojo or The Numbers)
â¢ Trade articles like the one on Just Jared

To summarize with what is clear from the current reporting:
1. Ne Zha 2
2. Inside Out 2
3â5. Other animated films (yet to be definitively finalized across all reporting outlets)

If you're looking for a final, consensus list of the top five, it may be best to wait until
the 2025 yearâend boxâoffice tallies are in or to consult a regularly updated entertainment industry source.

Would you like help finding a current source or additional details on where to look for the complete updated list?
"""
```

```
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

agent = Agent(
    'openai:o3-mini',
    tools=[duckduckgo_search_tool()],
    system_prompt='Search DuckDuckGo for the given query and return the results.',
)

result = agent.run_sync(
    'Can you list the top five highest-grossing animated films of 2025?'
)
print(result.data)
"""
I looked into several sources on animated boxâoffice performance in 2025, and while detailed
rankings can shift as more money is tallied, multiple independent reports have already
highlighted a couple of recordâbreaking shows. For example:

â¢ Ne Zha 2 â News outlets (Variety, Wikipedia's "List of animated feature films of 2025", and others)
    have reported that this Chinese title not only became the highestâgrossing animated film of 2025
    but also broke records as the highestâgrossing nonâEnglish animated film ever. One article noted
    its run exceeded US$1.7 billion.
â¢ Inside Out 2 â According to data shared on Statista and in industry news, this Pixar sequel has been
    on pace to set new records (with some sources even noting it as the highestâgrossing animated film
    ever, as of January 2025).

Beyond those two, some entertainment trade sites (for example, a Just Jared article titled
"Top 10 Highest-Earning Animated Films at the Box Office Revealed") have begun listing a broader
topâ10. Although full consolidated figures can sometimes differ by source and are updated daily during
a boxâoffice run, many of the industry trackers have begun to single out five films as the biggest
earners so far in 2025.

Unfortunately, although multiple articles discuss the "top animated films" of 2025, there isn't yet a
single, universally accepted list with final numbers that names the complete top five. (Boxâoffice
rankings, especially midâyear, can be fluid as films continue to add to their totals.)

Based on what several sources note so far, the two undisputed leaders are:
1. Ne Zha 2
2. Inside Out 2

The remaining top spots (3â5) are reported by some outlets in their "Topâ10 Animated Films"
lists for 2025 but the titles and order can vary depending on the source and the exact cutâoff
date of the data. For the most upâtoâdate and detailed ranking (including the 3rd, 4th, and 5th
highestâgrossing films), I recommend checking resources like:
â¢ Wikipedia's "List of animated feature films of 2025" page
â¢ Boxâoffice tracking sites (such as Box Office Mojo or The Numbers)
â¢ Trade articles like the one on Just Jared

To summarize with what is clear from the current reporting:
1. Ne Zha 2
2. Inside Out 2
3â5. Other animated films (yet to be definitively finalized across all reporting outlets)

If you're looking for a final, consensus list of the top five, it may be best to wait until
the 2025 yearâend boxâoffice tallies are in or to consult a regularly updated entertainment industry source.

Would you like help finding a current source or additional details on where to look for the complete updated list?
"""
```

## Tavily Search Tool

Info

Tavily is a paid service, but they have free credits to explore their product.

You need to sign up for an account and get an API key to use the Tavily search tool.

The Tavily search tool allows you to search the web for information. It is built on top of the Tavily API.

### Installation

To use tavily_search_tool, you need to install
pydantic-ai-slim with the tavily optional group:

```
tavily_search_tool
```

```
pydantic-ai-slim
```

```
tavily
```

```
pip install 'pydantic-ai-slim[tavily]'
```

```
pip install 'pydantic-ai-slim[tavily]'
```

```
uv add 'pydantic-ai-slim[tavily]'
```

```
uv add 'pydantic-ai-slim[tavily]'
```

### Usage

Here's an example of how you can use the Tavily search tool with an agent:

```
import os

from pydantic_ai.agent import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

api_key = os.getenv('TAVILY_API_KEY')
assert api_key is not None


agent = Agent(
    'openai:o3-mini',
    tools=[tavily_search_tool(api_key)],
    system_prompt='Search Tavily for the given query and return the results.',
)

result = agent.run_sync('Tell me the top news in the GenAI world, give me links.')
print(result.data)
"""
Here are some of the top recent news articles related to GenAI:

1. How CLEAR users can improve risk analysis with GenAI â Thomson Reuters
   Read more: https://legal.thomsonreuters.com/blog/how-clear-users-can-improve-risk-analysis-with-genai/
   (This article discusses how CLEAR's new GenAI-powered tool streamlines risk analysis by quickly summarizing key information from various public data sources.)

2. TELUS Digital Survey Reveals Enterprise Employees Are Entering Sensitive Data Into AI Assistants More Than You Think â FT.com
   Read more: https://markets.ft.com/data/announce/detail?dockey=600-202502260645BIZWIRE_USPRX____20250226_BW490609-1
   (This news piece highlights findings from a TELUS Digital survey showing that many enterprise employees use public GenAI tools and sometimes even enter sensitive data.)

3. The Essential Guide to Generative AI â Virtualization Review
   Read more: https://virtualizationreview.com/Whitepapers/2025/02/SNOWFLAKE-The-Essential-Guide-to-Generative-AI.aspx
   (This guide provides insights into how GenAI is revolutionizing enterprise strategies and productivity, with input from industry leaders.)

Feel free to click on the links to dive deeper into each story!
"""
```

```
import os

from pydantic_ai.agent import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

api_key = os.getenv('TAVILY_API_KEY')
assert api_key is not None


agent = Agent(
    'openai:o3-mini',
    tools=[tavily_search_tool(api_key)],
    system_prompt='Search Tavily for the given query and return the results.',
)

result = agent.run_sync('Tell me the top news in the GenAI world, give me links.')
print(result.data)
"""
Here are some of the top recent news articles related to GenAI:

1. How CLEAR users can improve risk analysis with GenAI â Thomson Reuters
   Read more: https://legal.thomsonreuters.com/blog/how-clear-users-can-improve-risk-analysis-with-genai/
   (This article discusses how CLEAR's new GenAI-powered tool streamlines risk analysis by quickly summarizing key information from various public data sources.)

2. TELUS Digital Survey Reveals Enterprise Employees Are Entering Sensitive Data Into AI Assistants More Than You Think â FT.com
   Read more: https://markets.ft.com/data/announce/detail?dockey=600-202502260645BIZWIRE_USPRX____20250226_BW490609-1
   (This news piece highlights findings from a TELUS Digital survey showing that many enterprise employees use public GenAI tools and sometimes even enter sensitive data.)

3. The Essential Guide to Generative AI â Virtualization Review
   Read more: https://virtualizationreview.com/Whitepapers/2025/02/SNOWFLAKE-The-Essential-Guide-to-Generative-AI.aspx
   (This guide provides insights into how GenAI is revolutionizing enterprise strategies and productivity, with input from industry leaders.)

Feel free to click on the links to dive deeper into each story!
"""
```

