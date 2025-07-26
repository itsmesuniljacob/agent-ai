import random
from agents import Agent, function_tool, Runner, RunContextWrapper, trace, handoff, RunConfig
from pydantic import BaseModel, Field
from openai import OpenAI
from openai.types.responses import (
    ResponseCreatedEvent,
    ResponseTextDeltaEvent,
    ResponseContentPartDoneEvent
)
from dotenv import load_dotenv
import asyncio, json, time
import pandas as pd
import streamlit as st
import strip_markdown as smd


load_dotenv(override=True)

client = OpenAI()

brands = [
    "Rolex", "Omega", "Tag Heuer", "Patek Philippe", "Audemars Piguet", 
    "Breitling", "Cartier", "Hublot", "IWC Schaffhausen", "Tissot"
]

movement_types = [
    "Automatic", "Manual", "Quartz", "Smart Hybrid"
]

genders = [
    "Men", "Women", "Unisex"
]

availability_status = [
    "In Stock", "Limited Edition", "Pre-Order", "Out of Stock"
]

watch_styles = [
    "Diver", "Dress", "Chronograph", "Aviator", "Skeleton", "Field", "Luxury Sports"
]

materials = [
    "Stainless Steel", "Titanium", "Ceramic", "Gold", "Platinum", "Carbon Fiber"
]

seasons = [
    "All Season", "Summer", "Winter", "Formal Occasions", "Adventure"
]

launch_years = list(range(1980, 2025))

adjectives = [
    "Regal", "Eternal", "Phantom", "Majestic", "Celestial",
    "Stealth", "Vanguard", "Pristine", "Obsidian", "Aurora"
]

design_keywords = [
    "Heritage", "Pulse", "Voyager", "Infinity", "Horizon",
    "Legacy", "Aero", "Chronos", "Nebula", "Titan"
]

# I want to generate watch data with the above data, also add price and description. The output should be a json object with the following keys: brand, movement_type, gender, availability, watch_style, material, season, launch_year, adjective, design_keyword, price, description.
# create dataframe with 100 rows and store in products.csv
import pandas as pd
df = pd.DataFrame(columns=["brand", "movement_type", "gender", "availability", "watch_style", "material", "season", "launch_year", "adjective", "design_keyword", "price", "description"])

def generate_watch_data(n):
    data = []
    for i in range(n):
        brand = random.choice(brands)
        movement_type = random.choice(movement_types)
        gender = random.choice(genders)
        availability = random.choice(availability_status)
        watch_style = random.choice(watch_styles)
        material = random.choice(materials)
        season = random.choice(seasons) 
        launch_year = random.choice(launch_years)
        adjective = random.choice(adjectives)
        design_keyword = random.choice(design_keywords)
        price = random.randint(1000, 10000)
        description = f"This is a {brand} {watch_style} watch with a {movement_type} movement. It is {adjective} and {design_keyword}. It is made of {material} and is available in {season}. It was launched in {launch_year}. It is {availability}."
        data.append({
            "brand": brand,
            "movement_type": movement_type,
            "gender": gender,
            "availability": availability,
            "watch_style": watch_style,
            "material": material,
            "season": season,
            "launch_year": launch_year,
            "adjective": adjective,
            "design_keyword": design_keyword,
            "price": price,
            "description": description
        })
    return data

df = pd.DataFrame(generate_watch_data(10))
# create a csv file with the dataframe
print(df.head())
df.to_csv('products-01.csv', index=False)

class QueryGeneratorOutput(BaseModel):
    query: str = Field(description="A valid pandas expression that can be used to query the data.")


# a function that takes a pandas expression and executes it and returns the result, if result is an error, return the error message
def execute_query(query: str):
    print(f"Executing query: {query}")
    try:
        result = eval(query, {'df': df})
        if isinstance(result, pd.Series):
            result = result.to_dict()
        elif isinstance(result, pd.DataFrame):
            result = result.to_dict(orient='records')
        if not result:
            return "No products found matching your criteria."
        # Format results as a readable list
        if isinstance(result, dict):
            # Single result (Series)
            result = [result]
        output = ["\nHere are the matching watches:\n"]
        for i, item in enumerate(result[:5]):  # Show only first 5 results
            output.append(
                f"{i+1}. {item['brand']} {item['watch_style']} ({item['launch_year']})\n"
                f"   Price: ${item['price']}\n"
                f"   Movement: {item['movement_type']}, Gender: {item['gender']}\n"
                f"   Material: {item['material']}, Season: {item['season']}\n"
                f"   Availability: {item['availability']}\n"
                f"   Description: {item['description']}\n"
            )
        if len(result) > 5:
            output.append(f"...and {len(result)-5} more results.\n")
        return "\n".join(output)
    except Exception as e:
        return str(e)

def data_query_agent_handoff(ctx: RunContextWrapper[None]):
    print('Handing off to data query agent')


query_execution_agent = Agent(
    name="query_execution_agent_v1",
    model="gpt-4o-mini",
    instructions=(
        "You are a helpful assistant that executes a pandas expression using the `execute_query` tool and return the results."
        "You should return the results in a human readable format. In a concise and convincing way."
    ),
    tools=[execute_query]
)

# Query Generator Agent
query_generator_agent = Agent(
    name="query_generator_agent_v1",
    model="gpt-4o-mini",
    instructions=(
        "You are a helpful assistant that can answer questions related to business data."
        f"Seeing the refined query, {df.columns} and {df.head()}, you generate a pandas expression to query the data."
    ),
    output_type=QueryGeneratorOutput,
    handoffs=[query_execution_agent],
)

# Query Refiner Agent
query_refiner_agent = Agent(
    name="query_refiner_agent_v1",
    model="gpt-4o-mini",
    instructions=(
        "You are a helpful assistant that can refine queries to be more specific and accurate."
        "If user asks for best seller or for random suggestions, search for perfumes with maximum rating."
        "You receive a query and generate a refined query in plain english that another agent will use to generate a pandas expression."
        "The query should be concise and to the point, and should not include any instructions or explanations."
    ),
    handoffs=[query_generator_agent],
)


data_query_agent = Agent(
    name="data_query_agent_v1",
    handoffs=[query_refiner_agent],
)

root_agent = Agent(
    name="Root Agent",
    instructions=(
      "You are a friendly and talkative assistant representing WatchCompany, a premium watch brand known for its exquisite collection of watches. "
        "Introduce yourself as WatchCompany's brand representative and share our passion for creating unique, high-quality watches. "
        "Engage users warmly, answer general questions, and encourage them to ask about our watches, collections, or anything related to the WatchCompany brand. "
        "If the user asks about watches and products and list or some information, delegate the query to `data_query_agent`. "    ),
    model="gpt-4o-mini",
    handoffs=[
        handoff(data_query_agent,on_handoff=data_query_agent_handoff)
        ]
)

async def main():
    user_msg =  input("User: ")
    agent = root_agent
    inputs: list[str] = [{"content": user_msg, "role": "user"}]
    while True:
        with trace("WatchCompany Customer Care Agent"):
            runner = Runner()
            result = runner.run_streamed(root_agent, input=inputs)
        async for chunk in result.stream_events():
            if chunk.type == "raw_response_event":
                event = chunk.data
                if isinstance(event, ResponseCreatedEvent):
                    agent_name = result.last_agent.name
                    print(f"🏃 Starting `{agent_name}` \n")
                    print("-" * 50, end="", flush=True)
                if isinstance(chunk, ResponseTextDeltaEvent):
                    print(chunk.delta, end="", flush=True)
                elif isinstance(chunk, ResponseContentPartDoneEvent):
                    print("\n")
        answer = result.final_output
        print("Assistant: "+f"\n{answer}\n")
 
        inputs = result.to_input_list()
        print()

        user_msg = input("User: \n")

        inputs.append({"content": user_msg, "role": "user"})

        # if there is no input from user for a minute   
        if not user_msg:
            time.sleep(60)
            if not user_msg:
                break

        if user_msg.lower() in ["exit", "bye"]:
            break

if __name__ == "__main__":
    asyncio.run(main())