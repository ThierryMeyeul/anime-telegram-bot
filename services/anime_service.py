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


def get_anime_random():
    url = "https://api.jikan.moe/v4/random/anime"
    for _ in range(10):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()["data"]
            anime_type = data.get('type', '').lower()
            if anime_type in ['tv', 'movie']:
                titles = [t["title"] for t in data.get("titles", [])]
                title_str = " / ".join(titles)
                trailer_url = data.get("trailer", {}).get("url")
                trailer_img = data.get("trailer", {}).get("images", {}).get("image_url")

                anime_info = {
                    "Titre(s)": title_str,
                    "Type": data.get("type", "N/A"),
                    "Episodes": data.get("episodes", "N/A"),
                    "Durée": data.get("duration", "N/A"),
                    "Statut": data.get("status", "N/A"),
                    "Date de sortie": data.get("aired", {}).get("string", "N/A"),
                    "Genres": ", ".join([g["name"] for g in data.get("genres", [])]),
                    "Synopsis": data.get("synopsis", "Pas de synopsis disponible."),
                    "URL MAL": data.get("url"),
                    "Image": data.get("images", {}).get("jpg", {}).get("large_image_url"),
                    "Trailer": trailer_url,
                    "Trailer_img": trailer_img
                }
                anime_info['Synopsis'] = GoogleTranslator(source='en', target='fr').translate(anime_info['Synopsis'])
                max_length = 600
                if len(anime_info['Synopsis']) > max_length:
                    anime_info['Synopsis'] = anime_info['Synopsis'][:max_length].rsplit(" ", 1)[0] + '...'
                result = (
                    f"🎬 **{anime_info['Titre(s)']}**\n"
                    f"📺 Type : {anime_info['Type']}\n"
                    f"🎞️ Episodes : {anime_info['Episodes']} ({anime_info['Durée']})\n"
                    f"📡 Statut : {anime_info['Statut']}\n"
                    f"📅 Diffusion : {anime_info['Date de sortie']}\n"
                    f"🏷️ Genres : {anime_info['Genres']}\n\n"
                    f"📝 Synopsis : {anime_info['Synopsis']}\n\n"
                    f"🔗 [Voir sur MyAnimeList]({anime_info['URL MAL']})"
                )

                if anime_info["Trailer"]:
                    result += f"\n\n🎬 [Trailer]({anime_info['Trailer']})"
                elif anime_info["Trailer_img"]:
                    result += f"\n\n🎬 Trailer preview : {anime_info['Trailer_img']}"

                return anime_info['Image'], result
        else:
            print(f"❌ Erreur API : {response.status_code}")
    return None