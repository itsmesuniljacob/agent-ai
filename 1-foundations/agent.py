from agents import Agent, function_tool, Runner
from openai import OpenAI
import asyncio

client = OpenAI()


def get_current_weather(city: str) -> str:
    """Get the current weather for a given city"""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="weather_agent",
    instructions="Get weather for a given city in Haiku format",
    # tools=[function_tool(get_current_weather)],
    model="gpt-4o-mini",
)

async def main():
    result = await Runner.run(agent,"What's the weather in Tokyo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

