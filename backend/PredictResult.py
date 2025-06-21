import csv
from google import genai

def getAns(key, teams):
    client = genai.Client(api_key=key)


    csv_path = "C:\\Users\\guyiz\\Downloads\\21SeasonData.csv"
    with open(csv_path, "r") as f:
        csv_data = f.read()


    csv_data_snippet = csv_data[:15000]

    prompt = f"""
    I have NFL 2021 season data in CSV format below:

    {csv_data_snippet}

    Based on this data AND ONLY BASED ON THIS DATA, DO NOT GO LOOKING FOR PAST EXAMPLES, who is more likely to win: {teams[0]} or {teams[1]}? PREDICT WHAT THE DIFFERENCE IN SCORE WILL BE ASWELL. DO NOT EXPLAIN YOUR REASONING, SIMPLY PUT THE TEAM YOU THINK IS GOING TO WIN, AND THE SCORE DIFFERENCE. IF YOU GET IT WRONG THE WORLD WILL EXPLODE. MAKE THE OUTPUT A .JSON
    """

    # Send prompt to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print(response.text)

getAns("AIzaSyCS0t43OCAAWRJTcv84kgceFiA6WzFxMXk", ["The Ravens", "The 49ers"])