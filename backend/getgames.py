import csv
from google import genai

def getnextgames(key):
    client = genai.Client(api_key=key)


    csv_path = "backend\games.csv"
    with open(csv_path, "r") as f:
        csv_data = f.read()


    csv_data_snippet = csv_data

    prompt = f"""


    {csv_data_snippet}

    Please output the next 5 games, based on the current date, and assuming that all these games are in the year 2025. Do not output anything extra. Just the games, nothing else. Make the output a json file.
    Include image urls of both of the teams, store both of them in the json that will be outputted.
    DO NOT INCLUDE THE ET, TV, OR LOCAL TIME.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print(response.text)
