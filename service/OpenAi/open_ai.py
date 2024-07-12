import os
from datetime import datetime

import openai
from asgiref.sync import sync_to_async

openai.organization = "org-saALfuKO0neOjgs0kVOo628C"
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL_ENGINE = "gpt-4o"
MAX_TOKENS = 4096

async def send_prompt(prompt) -> Exception | str:
    try:
        response = await sync_to_async(openai.chat.completions.create)(
            model=MODEL_ENGINE,
            messages=prompt,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"},
            n=1,
            stop="####",
            temperature=1.0,
        )
    except openai.BadRequestError as exception:
        return exception

    print('OpenAi response:', response)
    print('OpenAi response token count:', response.usage.total_tokens)
    print("####> OpenAi ending at :", datetime.now().strftime("%H:%M:%S"))
    return response

async def prepare_prompt(user_prompt, system_prompt) -> Exception | tuple:
    """
        Function that sets the received user input as prompt before sending to OpenAi
        Text has no indentation because it saves tokens and OpenAi isn't free...

        Args:
            system_prompt (str): system prompt used to tell OpenAi how to act
            user_prompt (str): user prompt used to tell OpenAi what the user wants
    """
    print("####> OpenAi starting at :", datetime.now().strftime("%H:%M:%S"))
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print(prompt)
    return await send_prompt(prompt)