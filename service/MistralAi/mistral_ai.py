import os
from datetime import datetime

from asgiref.sync import sync_to_async
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]

N_MAX_ACTIVITIES = 4
N_MAX_STEPS = 4
MODEL_ENGINE = "mistral-large-latest"
MAX_TOKENS = 4096

client = MistralClient(api_key=api_key)


async def send_prompt(prompt):
    print(prompt)
    response = await sync_to_async(client.chat)(
        model=MODEL_ENGINE,
        response_format={"type": "json_object"},
        messages=prompt,
    )

    print('Mistral response:', response)
    print('Mistral response token count:', response.usage.total_tokens)
    print("####> Mistral ending at :", datetime.now().strftime("%H:%M:%S"))
    return response

async def prepare_prompt(user_prompt, system_prompt):
    """
        Function that sets the received user input as prompt before sending it to MistralAi
        Text has no indentation because it saves tokens and MistralAi isn't free...

        Args:
            system_prompt (str): system prompt used to tell MistralAi how to act
            user_prompt (str): user prompt used to tell MistralAi what the user wants
    """
    print("####> Mistral starting at :", datetime.now().strftime("%H:%M:%S"))
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt),
    ]

    return await send_prompt(messages)
