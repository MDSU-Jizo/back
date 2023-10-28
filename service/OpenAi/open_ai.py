import os
import openai
import tiktoken

openai.organization = "org-saALfuKO0neOjgs0kVOo628C"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

N_MAX_ACTIVITIES = 4
N_MAX_STEPS = 4
# MODEL_ENGINE = "babbage-002"
MODEL_ENGINE = "text-davinci-003"
# MODEL_ENGINE = "gpt-3.5-turbo"
MAX_TOKENS = 1100


def token_count(prompt) -> int:
    encoding = tiktoken.encoding_for_model(MODEL_ENGINE)
    return len(encoding.encode(prompt))


def send_prompt(prompt):
    response = openai.Completion.create(
        model=MODEL_ENGINE,
        prompt=prompt,
        max_tokens=MAX_TOKENS,
        n=1,
        stop="####",
        temperature=0.0,
    )

    print('response:', response.choices[0].text)
    return response


def prepare_prompt(user_inputs):
    """
        Function that sets the received user input as prompt before sending in to OpenAI
        Text has no indentation because it saves 19 tokens and OpenAI isn't free...

        Args:
            user_inputs (dict): Dict of every user inputs
    """
    prompt = """Generate a personalized JSON travel itinerary based on user inputs
The JSON should include details on the country
the duration of the trip
and a breakdown of the itinerary with locations to visit"""

    prompt += str(user_inputs)

    if not user_inputs['steps']:
        prompt += f"Generate the JSON itinerary with {N_MAX_STEPS} steps"

    prompt += f"""
Each step should include {N_MAX_ACTIVITIES} activities or points of interest If 'Multiple Cities' is set to 'True' 
The itinerary must include steps with different cities 
must start at the 'starting City'
The 'endingCity' must be the last step 
The itinerary should align with the user's interests 
and if 'Traveling with Children' is set to 'True' 
add a few kid-friendly activities
Ensure no repeated visits to the same place and suggest a national restaurant at least once a day
Also, provide latitude and longitude for every place to visit
Only return the JSON
expected JSON format:
{{
  "country": "[Country]",
  "itinerary": [
    {{
      "city": "[City]",
      "duration": [Duration for this city],
      "todo": [
        {{
          "name": "[Name of Attraction/Place/Restaurant]",
          "longitude": "[Longitude]",
          "latitude": "[Latitude]",
          "category": "[Category]"
        }}
      ]
    }}
  ]
}}"""

    print(prompt)
    print('User prompt token count:', token_count(prompt))
    return send_prompt(prompt)
