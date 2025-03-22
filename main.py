import chainlit as cl
from dotenv import load_dotenv
import os
import google.generativeai as genai
from typing import Optional, Dict

load_dotenv()

genai_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key = genai_api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token : str,
  row_user_data: Dict[str,str],
  default_user: cl.User,
) -> Optional[cl.User]:
  """
  Handle the oAuth callback from authentication providers (GitHub or Google)
  Return the user object if authentication is successful
  """
  print(f"Provider: {provider_id}")
  print(f"Row user data: {row_user_data}")
  
  # You can add custom logic here based on the provider
  if provider_id == "github":
    # Custom handling for GitHub authentication
    print(f"GitHub user authenticated: {row_user_data.get('login', 'Unknown')}")
  elif provider_id == "google":
    # Custom handling for Google authentication
    print(f"Google user authenticated: {row_user_data.get('email', 'Unknown')}")
  
  return default_user

@cl.on_chat_start
async def handle_chat_start():
  
  cl.user_session.set("history", [])

  await cl.Message(content = "Hello!How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
  
  history = cl.user_session.get("history")

  history.append({"role": "user" , "content":message.content})

  formatted_history = []
  for msg in history:
    role = "user" if msg["role"] == "user" else "model"

    formatted_history.append({"role": role, "parts":[{"text":msg["content"]}]})

  response = model.generate_content(formatted_history)

  response_text = response.text if hasattr(response, "text") else ""

  history.append({"role":"assistant", "content":response_text})

  cl.user_session.set("history", history)

  await cl.Message(content = response_text).send()