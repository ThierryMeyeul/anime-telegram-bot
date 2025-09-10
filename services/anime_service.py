import requests
from deep_translator import GoogleTranslator

from config import API_URL


def get_random_quote():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()['data']
        quote_fr = GoogleTranslator(source='en', target='fr').translate(data['content'])
        quote_text = (
            f'💬 *Citation d’anime*\n\n'
            f'{quote_fr}\n\n'
            f'📺 *Anime :* {data['anime']['name']}\n'
            f'🧑 *Personnage :* {data['character']['name']} '
        )
        return quote_text