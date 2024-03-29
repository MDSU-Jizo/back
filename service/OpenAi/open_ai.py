import os
import tiktoken
import openai
from openai.types.chat.chat_completion import ChatCompletion

from type.models import Type
from interest.models import Interest

openai.organization = "org-saALfuKO0neOjgs0kVOo628C"
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.Model.list()

N_MAX_ACTIVITIES = 4
N_MAX_STEPS = 4
# MODEL_ENGINE = "babbage-002"
MODEL_ENGINE = "gpt-3.5-turbo-0125"
# MODEL_ENGINE = "gpt-3.5-turbo"
MAX_TOKENS = 4096


def token_count(prompt) -> int: # TODO: update method to count tokens
    encoding = tiktoken.encoding_for_model(MODEL_ENGINE)
    return len(encoding.encode(prompt))


def send_prompt(prompt, used_tokens) -> Exception | ChatCompletion:
    try:
        response = openai.chat.completions.create(
            model=MODEL_ENGINE,
            messages=prompt,
            max_tokens=MAX_TOKENS - used_tokens,
            response_format={"type": "json_object"},
            n=1,
            stop="####",
            temperature=1.0,
        )

    except openai.BadRequestError as exception:
        return exception

    print('response:', response.choices[0].message.content)
    print('response token count:', response.usage.total_tokens)
    return response


def prepare_prompt(user_inputs):
    """
        Function that sets the received user input as prompt before sending in to OpenAI
        Text has no indentation because it saves 19 tokens and OpenAI isn't free...

        Args:
            user_inputs (dict): Dict of every user inputs
    """
    language = "french" if user_inputs['language'] == "fr" else "english"

    system_prompt = f"""
Generate a personalized travel itinerary based on user inputs for a backpacking trip. 
Your task is to craft an itinerary tailored to the user's preferences, 
including the duration of the trip for each step, 
locations to visit, and points of interest. Each step should contain a minimum of {N_MAX_ACTIVITIES} activities or points of interest.
If 'multiple_cities' is set to 'True', the itinerary should cover multiple cities; 
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
"""

    if user_inputs.get('steps') is None:
        system_prompt += f" Generate the JSON itinerary with a minimum of {N_MAX_STEPS} steps"

    system_prompt += """
expected JSON format:
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
"""

    tmp_types = []
    for travel_type in user_inputs['types']:
        tmp_types.append(Type.objects.get(pk=travel_type).label)
    user_inputs['types'] = tmp_types

    tmp_interests = []
    for travel_interest in user_inputs['interests']:
        tmp_interests.append(Interest.objects.get(pk=travel_interest).label)
    user_inputs['interests'] = tmp_interests
    user_inputs.pop('user')

    user_prompt = str(user_inputs)

    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # prompt += """
    #  Ensure the correct order of latitude and longitude in the generated coordinates.
    # . Ensure to ONLY return the stringified JSON
    # """

    print(prompt)
    system_tokens = token_count(prompt[0]['content']) # TODO: update method to count tokens
    user_tokens = token_count(prompt[0]['content']) # TODO: update method to count tokens
    print('System prompt token count:', system_tokens)
    print('User prompt token count:', user_tokens)
    return send_prompt(prompt, system_tokens + user_tokens)
