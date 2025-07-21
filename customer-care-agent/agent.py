import random
from agents import Agent, function_tool, Runner
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import pandas as pd


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

df = pd.DataFrame(generate_watch_data(100))
# create a csv file with the dataframe
print(df.head())

