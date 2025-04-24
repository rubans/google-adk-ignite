from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

from .prompts import return_instructions_ee
from google.adk.tools import load_artifacts

from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional

import os
# --- 1. Define the Callback Function ---
def validate_if_file_is_uploaded(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Check if user has uploaded the file.
    If not then skip the agent's execution.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id

    print(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"\[Callback] checking uploaded file: {callback_context.user_content.parts}")
    
    is_file_uploaded_in_user_ctx = ""
    for part in callback_context.user_content.parts:
        if part.inline_data and getattr(part.inline_data, 'mime_type', None):
            is_file_uploaded_in_user_ctx = False
        else:
            is_file_uploaded_in_user_ctx = True
            
    if is_file_uploaded_in_user_ctx is False:
        print(f"\n[Callback] mime/type found: Proceeding with agent {agent_name}.")
        # Return None to allow the LlmAgent's normal execution
        return None
    else:
        print(f"\nCallback] Not Found mime_type: Skipping agent {agent_name}.")
        callback_context.state['financial_entities'] = None # Setting this explicitly so another agent can check this state
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} Please upload the file.")],
            role="model" # Assign model role to the overriding response
        )

root_agent = Agent(
    model=os.getenv("DEFAULT_MODEL"),
    name="entity_extractor_agent",
    instruction=return_instructions_ee(),
    # before_agent_callback=validate_if_file_is_uploaded,
    tools=[load_artifacts]
)
