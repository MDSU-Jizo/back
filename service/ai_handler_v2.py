import asyncio
import aiocache

from asgiref.sync import sync_to_async

from contract.prompts import Prompts
from .MistralAi.mistral_ai import prepare_prompt as mistral_prompt
from .OpenAi.open_ai import prepare_prompt as openai_prompt

from interest.models import Interest
from type.models import Type

N_MAX_STEPS = 4


async def send_to_ai(user_inputs):
    user_prompt = _clean_prompt(await _user_prompt(user_inputs))
    system_prompt = _clean_prompt(_system_prompt(user_inputs))

    # Run both AI model requests concurrently
    mistral_response, openai_response = await asyncio.gather(
        mistral_prompt(user_prompt, system_prompt),
        openai_prompt(user_prompt, system_prompt)
    )

    return _choose_best_response(mistral_response, openai_response, user_inputs)


@aiocache.cached(ttl=600)  # Cache for 10 minutes
async def get_type_label(type_id):
    type_obj = await sync_to_async(Type.objects.get)(pk=type_id)
    return type_obj.label


@aiocache.cached(ttl=600)  # Cache for 10 minutes
async def get_interest_label(interest_id):
    interest_obj = await sync_to_async(Interest.objects.get)(pk=interest_id)
    return interest_obj.label


async def _user_prompt(user_inputs) -> str:
    user_inputs['types'] = await asyncio.gather(
        *[get_type_label(travel_type) for travel_type in user_inputs['types']]
    )

    user_inputs['interests'] = await asyncio.gather(
        *[get_interest_label(travel_interest) for travel_interest in user_inputs['interests']]
    )

    user_inputs.pop('user')
    return str(user_inputs)

def _system_prompt(user_inputs) -> str:
    language = "french" if user_inputs['language'] == "fr" else "english"
    language_prompt = f"The values should be in {language}."

    for n in range(N_MAX_STEPS):
        system_prompt = ""

        if (user_inputs.get('multiple_cities') is not None or False) or (
                user_inputs.get('starting_city') != user_inputs.get('ending_city')):
            if n == 1:
                system_prompt += Prompts.init_prompt + Prompts.first_step_prompt + language_prompt + Prompts.expected_json_starting_output
            elif n == N_MAX_STEPS:
                system_prompt += Prompts.last_step_prompt + Prompts.nth_step_prompt + language_prompt + Prompts.expected_json_nth_step_output
        else:
            system_prompt += Prompts.unique_city_prompt + language_prompt + Prompts.expected_json_starting_output

    return system_prompt


def _expected_json_format_prompt() -> str:
    return """
        ####
        Here is the expected JSON format:
        {{
          "country": "[Country]",
          "itinerary": [
            {{
              "city": "[City]",
              "latitude": "[Latitude]",
              "longitude": "[Longitude]",
              "duration": [Duration for this city],
              "todo": [
                {{
                  "name": "[Name of Attraction/Place/Restaurant]",
                  "latitude": "[Latitude]",
                  "longitude": "[Longitude]",
                  "category": "[Category]"
                }}
              ]
            }}
          ]
        }}
        ####
    """


def _clean_prompt(prompt: str) -> str:
    # Remove leading/trailing whitespaces and excessive internal whitespace
    lines = prompt.strip().split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    cleaned_prompt = ' '.join(cleaned_lines)
    return cleaned_prompt