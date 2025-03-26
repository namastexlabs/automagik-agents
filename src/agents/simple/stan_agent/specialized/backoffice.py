from pydantic_ai import Agent, RunContext
import logging

logger = logging.getLogger(__name__)

async def backoffice_agent(input_text: str) -> bool:
    roulette_agent = Agent(  
        'openai:gpt-4o',
        deps_type=int,
        result_type=str,
        system_prompt=(
            'Use the `roulette_wheel` function to see if the '
            'customer has won based on the number they provide.'
        ),
    )

    @roulette_agent.tool
    async def roulette_wheel(ctx: RunContext[int], square: int) -> str:  
        """check if the square is a winner"""
        return 'winner' if square == ctx.deps else 'loser'

    success_number = 18
    result = await roulette_agent.run(input_text, deps=success_number)
    
    logger.info(f"Specialized agent result: {result}")
    return result.data