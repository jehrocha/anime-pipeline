import requests
import psycopg
import time

def extract_genre():
    genre_list = []
    url = "https://api.jikan.moe/v4/genres/anime"
    filters = ["genres", "explicit_genres"]

    for filter in filters:
        response = requests.get(url, params={"filter": filter})

        if response.status_code == 200:

            data = response.json()
            genre = data.get("data")

            for genre in genre:
                name = genre.get("name")
                genre_list.append((name,))
    
    print("Successfully extracted all genres")
    return genre_list

def extract_anime_genre(page = 1, count = 1):
    anime_genre = []
    base_url = "https://api.jikan.moe/v4/top/anime"

    while count < 100:
        response = requests.get(f"{base_url}", params={"page": page, "type": "tv", "filter": "bypopularity", "sfw": "true"})

        if response.status_code != 200:
            print("Stopped at page", page)
            break

        data = response.json()
        anime_page = data.get("data", [])

        if not anime_page:
            print(f"No data found on page {page}. Ending fetch.")
            break

        for anime in anime_page:

            anime_id = anime.get("mal_id")
            genres = anime.get("genres")

            for genre in genres:
                genre_name = genre.get("name")
                anime_genre.append((anime_id, genre_name))

            count += 1

        print(f"Page {page} done, total titles so far: {len(anime_genre)}")
        page += 1
        time.sleep(1)

    return anime_genre




