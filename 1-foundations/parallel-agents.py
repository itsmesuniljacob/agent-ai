from agents import Agent, function_tool, Runner, trace
from openai import OpenAI
import asyncio

client = OpenAI()


def get_current_weather(city: str) -> str:
    """Get the current weather for a given city"""
    return f"The weather in {city} is sunny"

agent_1 = Agent(
    name="haiku_weather_agent",
    instructions="Get weather for a given city in Haiku format",
    tools=[function_tool(get_current_weather)],
    model="gpt-4o-mini",
)

agent_2 = Agent(
    name="weather_agent",
    instructions="Get weather for a given city",
    tools=[function_tool(get_current_weather)],
    model="gpt-4o-mini",
)

agent_3 = Agent(
    name="weather_agent",
    instructions="Get weather for a given city in Celsius",
    tools=[function_tool(get_current_weather)],
    model="gpt-4o-mini",
)

message = "What's the weather in Tokyo?"

async def main():
    with trace("Parallel weather report with multiple Agents"):
        results = await asyncio.gather(
            Runner.run(agent_1, message),
            Runner.run(agent_2, message),
            Runner.run(agent_3, message),
        )

    outputs = [result.final_output for result in results]
    for output in outputs:
        print(output + "\n\n")

if __name__ == "__main__":
    asyncio.run(main())
