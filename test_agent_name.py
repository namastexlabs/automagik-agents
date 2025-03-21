from src.agents.simple.simple_agent.agent import SimpleAgent
import asyncio

async def test_name_response():
    agent = SimpleAgent({'model': 'openai:gpt-4o'})
    print('Agent initialized')
    response = await agent.run('What is your name?')
    print(f'Response: {response.text}')

asyncio.run(test_name_response()) 