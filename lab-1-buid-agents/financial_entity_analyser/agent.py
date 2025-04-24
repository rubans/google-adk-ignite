import os

from datetime import date
from google.genai import types
from google.adk.agents import Agent
from google.genai import types
from .sub_agents import entity_extractor_agent, stock_analyst_agent

from .prompts import return_instructions_root

date_today = date.today()

    
root_agent = Agent(
    model=os.getenv("DEFAULT_MODEL"),
    name="entity_analysis_multiagent",
    instruction=return_instructions_root(),
    global_instruction=(
        f"""
        You are a Senior Financial Analyst Multi Agent System.
        Todays date: {date_today}
        """
    ),
    sub_agents=[entity_extractor_agent],
    tools=[
        stock_analyst_agent
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
