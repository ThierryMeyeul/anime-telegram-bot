from datetime import datetime, timedelta

import requests
from deep_translator import GoogleTranslator

from config import API_URL


DAYS_FR = {
    "monday": "Lundi",
    "tuesday": "Mardi",
    "wednesday": "Mercredi",
    "thursday": "Jeudi",
    "friday": "Vendredi",
    "saturday": "Samedi",
    "sunday": "Dimanche"
}


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


def get_weekly_schedule():
    schedule = {}
    days = list(DAYS_FR.keys())
    today = datetime.today()

    for i, day in enumerate(days):
        date = (today + timedelta(days = (i - today.weekday()) % 7)).strftime('%d/%m/%Y')
        url = f"https://api.jikan.moe/v4/schedules/{day}"
        response = requests.get(url)
        anime_list = []
        if response.status_code == 200:
            data = response.json().get('data', [])

            for anime in data:
                title = anime.get('title')
                anime_list.append(f"• {title}")
        schedule[f"{DAYS_FR[day]} ({date})"] = anime_list if anime_list else ["Aucun anime prévu."]

    return schedule