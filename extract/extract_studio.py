import requests
import psycopg
import time

def extract_studio(page = 1, count = 1):
    studio_list = []
    base_url = "https://api.jikan.moe/v4/top/anime"

    while count < 100:
        response = requests.get(f"{base_url}", params ={"page" : page, "type" : "tv", "filter" : "bypopularity", "sfw" : "true"})

        if response.status_code != 200:
            print("Stopped at page", page)
            break
        
        data = response.json()
        anime_page = data.get("data", [])

        if not anime_page:
            print(f"No data found on page {page}. Ending fetch.")
            break

        for anime in anime_page:
            studios = anime.get("studios")

            for studio in studios:
                name = studio.get("name")

                if (name,) not in studio_list:
                    studio_list.append((name,))
            count += 1

        page += 1
        time.sleep(1)

    print("Successfully extracted all studios")
    return studio_list

def extract_anime_studios(page = 1, count = 1):

    anime_studio = []
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
            studios = anime.get("studios")

            for studio in studios:
                studio_name = studio.get("name")
                anime_studio.append((anime_id, studio_name))

            count += 1

        print(f"Page {page} done, total titles so far: {len(anime_studio)}")
        page += 1
        time.sleep(1)

    return anime_studio



    