import requests
import random
def generate_paragraph():
    """Generate 4 to 8 random sentences using a api"""
    number_of_sentence = random.randint(1, 3)
    url = f'http://metaphorpsum.com/sentences/{number_of_sentence}?'
    response =requests.get(url=url)
    return response.text

    
