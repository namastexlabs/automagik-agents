# Pydantic AI Framework Guide

## Core Concepts
- Define structured outputs with Pydantic models
- Create agents with `Agent(model_name, result_type=YourModel)`
- Tools are registered with `@agent.tool` decorator
- Dependencies are passed via `deps_type` and accessed through `ctx.deps`
- Error handling uses `ModelRetry` exception for LLM retry
- System prompts guide agent behavior (`system_prompt` parameter)
- Result validators ensure data quality (`@agent.result_validator`)

## Agent Creation Patterns
```python
# Basic type-aware agent
agent = Agent(
    'openai:gpt-4o',
    result_type=FlightDetails,
    system_prompt='Your instructions here',
    deps_type=Deps,
    instrument=True,  # Enable instrumentation
)

# Agent with union return types
agent = Agent[Deps, Success | Failure](
    'openai:gpt-4o',
    result_type=Success | Failure,  # type: ignore
    # Other parameters...
)
```

## Pydantic Model Patterns
```python
class WeatherResponse(BaseModel):
    temperature: float = Field(description='Temperature in Celsius')
    conditions: str = Field(description='Brief weather description')
    location: str = Field(description='Location queried')
    forecast: list[str] = Field(description='Short-term forecast')
```

## Tool Definition
```python
@agent.tool
async def get_weather(ctx: RunContext[Deps], location: str) -> dict:
    """Get weather information for a location.
    
    Args:
        ctx: The run context
        location: A city or region name
    """
    # Implementation...
    return weather_data
```

## Result Validation
```python
@agent.result_validator
async def validate_result(ctx: RunContext[Deps], result: Response) -> Response:
    # Validate and possibly transform result
    if errors:
        raise ModelRetry('Error message to guide the LLM')
    return result
```

## Usage & Message History
```python
# Create usage tracker and limits
usage = Usage()
usage_limits = UsageLimits(request_limit=10)

# Maintain conversation context
message_history = None
result = await agent.run(
    prompt,
    deps=deps,
    usage=usage,
    usage_limits=usage_limits,
    message_history=message_history,
)
# Update history for next interaction
message_history = result.all_messages()
```

## Running Examples
- Basic weather: `python -m examples.weather_agent`
- Question flow: `python -m examples.question_graph [continuous|cli|mermaid]`
- RAG demo: `python -m examples.rag [build|search]`
- SQL generation: `python -m examples.sql_gen`

## Best Practices
- Always document tools with detailed docstrings
- Use Field descriptions to guide LLM output
- Define clear validation rules using Pydantic validators
- Handle edge cases with union return types
- Use spans for tracing: `with logfire.span('action', params=params)`
- Set reasonable usage limits to control costs