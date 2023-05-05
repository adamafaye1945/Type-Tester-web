import requests
import random
def generate_paragraph():
    """Generate 4 to 8 random sentences using a api"""
    # Define the endpoint URL and parameters
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'titles': 'Cold_War',
        'format': 'json'
    }

    # Make the GET request
    response = requests.get(url, params=params)

    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    first_five_sentences = page['extract'].split('\n')[0:5]
    return first_five_sentences[random.randint(0,2)]