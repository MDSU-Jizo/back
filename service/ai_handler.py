import asyncio
import datetime
import aiocache
import json

from asgiref.sync import sync_to_async
from .MistralAi.mistral_ai import prepare_prompt as mistral_prompt
from .OpenAi.open_ai import prepare_prompt as openai_prompt

from type.models import Type
from interest.models import Interest

N_MAX_ACTIVITIES = 4
N_MAX_STEPS = 4


async def send_to_ai(user_inputs) -> str:
    user_prompt = _clean_prompt(await _user_prompt(user_inputs))
    system_prompt = _clean_prompt(_system_prompt(user_inputs))

    # Run both AI model requests concurrently
    mistral_response, openai_response = await asyncio.gather(
        mistral_prompt(user_prompt, system_prompt),
        openai_prompt(user_prompt, system_prompt)
    )

    return _choose_best_response(mistral_response, openai_response, user_inputs)


def _choose_best_response(mistral_response, openai_response, user_inputs) -> str:
    # Parse responses
    mistral_data = json.loads(mistral_response.choices[0].message.content)
    openai_data = json.loads(openai_response.choices[0].message.content)

    # Validate responses
    mistral_score = _validate_response(mistral_data, user_inputs)
    openai_score = _validate_response(openai_data, user_inputs)

    print('mistral_score =>', mistral_score)
    print('openai_score =>', openai_score)

    # Choose the best response based on score
    if mistral_score < openai_score:
        return openai_response.choices[0].message.content
    else:
        return mistral_response.choices[0].message.content


def _validate_response(response, user_inputs) -> int:
    score = 0
    total_duration = 0

    start_date = datetime.datetime.strptime(user_inputs['start_date'], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(user_inputs['end_date'], "%Y-%m-%d")
    user_travel_duration = (end_date - start_date).days

    # Validate number of steps and activities
    if len(response['itinerary']) == N_MAX_STEPS:
        score += 1
    for step in response['itinerary']:
        if len(step['todo']) == N_MAX_ACTIVITIES:
            score += 1

    # Validate coherence
    if response['itinerary'][0]['city'].lower() == user_inputs['starting_city'].lower():
        score += 1
    if response['itinerary'][-1]['city'].lower() == user_inputs['ending_city'].lower():
        score += 1

    # Validate no duplicate activities
    activities = set()
    for step in response['itinerary']:
        for activity in step['todo']:
            if activity['name'] in activities:
                score -= 1
            else:
                activities.add(activity['name'])

    # Validate user preferences
    for step in response['itinerary']:
        for activity in step['todo']:
            if activity['category'] not in user_inputs['interests']:
                score -= 1

    # Validate trip duration
    for step in response['itinerary']:
        total_duration += step['duration']

    if total_duration == user_travel_duration:
        score += 1
    else:
        score -= 1

    return score


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

    system_prompt = f"""
        Forget every previous prompt.
        You are an expert in travels of all kind.
        Generate a personalized travel itinerary based on user inputs for a backpacking trip. 
        Your task is to craft an itinerary tailored to the user's preferences, 
        including the duration of the trip for each step, 
        locations to visit, and points of interest. Each step should contain a minimum of {N_MAX_ACTIVITIES} activities or points of interest.
        If 'multiple_cities' is set to 'True' or it has an 'ending_city' different from 'starting_city', the itinerary should cover multiple cities; 
        otherwise, focus on the 'starting_city'. 
        Ensure a minimum of {N_MAX_STEPS} steps and/or {N_MAX_ACTIVITIES} activities close to the starting city that fit the trip's duration. 
        The itinerary must start at the 'starting_city' and end at the 'ending_city', 
        unless 'ending_city' is not specified, in which case the last step must be the same as the starting city.
        If 'multiple_cities' is not set to 'True', 
        ensure that the itinerary includes at least {N_MAX_STEPS} steps around the 'starting_city', 
        each containing a minimum of {N_MAX_ACTIVITIES} activities.
        The itinerary should align with the user's interests. 
        If 'with_children' is set to 'True', include kid-friendly activities; 
        otherwise, exclude them.
        Avoid repeated visits to the same place and suggest a national restaurant at least once a day.
        Provide latitude and longitude in decimal degrees for each place to visit, with latitude first followed by longitude. 
        The values should be in {language}.
        Do not provide any explanations or notes.
    """

    if user_inputs.get('steps') is None:
        system_prompt += f" Generate the JSON itinerary with a minimum of {N_MAX_STEPS} steps"

    system_prompt += _expected_json_format_prompt()

    return system_prompt


def _clean_prompt(prompt: str) -> str:
    # Remove leading/trailing whitespaces and excessive internal whitespace
    lines = prompt.strip().split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    cleaned_prompt = ' '.join(cleaned_lines)
    return cleaned_prompt