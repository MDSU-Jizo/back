import os
import tiktoken
import openai
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


def send_prompt(prompt):
    response = openai.chat.completions.create(
        model=MODEL_ENGINE,
        messages=prompt,
        max_tokens=MAX_TOKENS,
        response_format={"type": "json_object"},
        n=1,
        stop="####",
        temperature=1.0,
    )

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
    system_prompt = """
    You are an expert in backpacking travels and travels in general
    Generate a personalized travel itinerary based on user inputs
    the itinerary should include the duration of the trip for each step
    and a breakdown of the itinerary with locations to visit
    """

    system_prompt += f"""
    Each step should include {N_MAX_ACTIVITIES} activities or points of interest If 'Multiple Cities' is set to 'True' else only return an itinerary about the 'starting City' and activities near it
    The itinerary must include steps with different cities and must start at the 'starting City' and the 'endingCity' must be the last step
    If no 'starting City' sets the last step must be the same as the 'starting City'
    The itinerary should align with the user's interests and if the user has set 'Traveling with Children' to 'True' add a few kid-friendly activities else don't
    Ensure no repeated visits to the same place and suggest a national restaurant at least once a day
    Also, provide latitude and longitude in decimal degrees for every place to visit
    latitude must come first then longitude
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

    if not user_inputs['steps']:
        system_prompt += f" Generate the JSON itinerary with {N_MAX_STEPS} steps"

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
    #used_tokens = token_count(prompt) # TODO: update method to count tokens
    #print('User prompt token count:', used_tokens)
    return send_prompt(prompt)
