N_MAX_ACTIVITIES = 4
N_MAX_STEPS = 4

class Prompts:

    init_prompt = """
        Forget every previous prompt.
        You are an expert in travels of all kind.
        Generate a personalized travel itinerary based on user inputs for a backpacking trip. 
        Your task is to craft an itinerary tailored to the user's preferences, 
        including the duration of the trip for each step, locations to visit, and points of interest.
        The itinerary should align with the user's interests. 
        If 'with_children' is set to 'True', include kid-friendly activities; 
        otherwise, exclude them.
        Avoid repeated visits to the same place and suggest a national restaurant at least once a day.
        Avoid repeated visits to the same place and suggest a national restaurant at least once a day.
        Provide latitude and longitude in decimal degrees for each place to visit, with latitude first followed by longitude.
        Do not provide any explanations or notes.
        The response must be in JSON format.
    """

    unique_city_prompt = f"""
        The itinerary should only cover this unique city
        Ensure that the itinerary includes at least {N_MAX_STEPS} steps around the 'starting_city', 
        each containing a minimum of {N_MAX_ACTIVITIES} activities.
    """

    first_step_prompt = f"""
        This step should contain a minimum of {N_MAX_ACTIVITIES} activities or points of interest.
        Ensure a minimum of {N_MAX_ACTIVITIES} activities close to this city that fit the trip's duration.
    """

    nth_step_prompt = f"""
        This step should contain a minimum of {N_MAX_ACTIVITIES} activities or points of interest.
        Ensure a minimum of {N_MAX_ACTIVITIES} activities close to this city that fit the trip's duration.
    """

    last_step_prompt = f"""
        This step should contain a minimum of {N_MAX_ACTIVITIES} activities or points of interest.
        Ensure a minimum of {N_MAX_ACTIVITIES} activities close to this city that fit the trip's duration.
    """

    expected_json_starting_output = """
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

    expected_json_nth_step_output = """
        ####
            Here is the expected JSON format:
            {{
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