# Pydantic-AI v0.0.25 Update

## Issue

The project was using pydantic-ai v0.0.24, but v0.0.25 introduced a breaking change in the agent result API.

According to the [release notes](https://github.com/pydantic/pydantic-ai/releases/tag/v0.0.25), the v0.0.25 update included:

- Add `GraphRun` object to make use of `next` more ergonomic
- Various other changes and improvements

## Changes Made

1. Updated the `base_agent.py` file to use the new API:
   - Changed from using the `_all_messages` attribute to calling the `all_messages()` method.

2. Updated the dependency in `pyproject.toml` to specify minimum version as 0.0.25.

## Testing

The fix was tested with a simple agent query and confirmed working in the test_fix.py script. 