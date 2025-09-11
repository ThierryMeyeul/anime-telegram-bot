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
            f"📺 *Anime :* {data['anime']['name']}\n"
            f"🧑 *Personnage :* {data['character']['name']} "
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


def get_waifu_random():
    url = 'https://api.waifu.im/search'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('images'):
            waifu = data['images'][0]
            image_url = waifu['url']
            source = waifu.get('source', 'inconnue')
            if source.find('reddit') != -1:
                source = 'inconnue'

            character_name = waifu.get('character', {}).get('name') if waifu.get('character') else None
            anime_name = waifu.get("character", {}).get("anime") if waifu.get("character") else None
            description_waifu = ''
            tags = waifu.get('tags', [])
            if tags:
                if tags[0]['name'] != 'waifu':
                    character_name = tags[0]['name']
                    description_waifu = tags[0]['description']
                    description_waifu = GoogleTranslator(source='en', target='fr').translate(description_waifu)

            caption = f"🌸 <b>Waifu Random</b>\n\n"
            if character_name:
                caption += f"🧑 <b>Personnage :</b> {character_name}\n"
            if anime_name:
                caption += f"📺 <b>Anime/Jeu :</b> {anime_name}\n"
            if description_waifu:
                caption += f"ℹ️ <b>Description :</b> {description_waifu}\n"
            caption += f"🔗 <b>Source :</b> {source}"

            return image_url, caption