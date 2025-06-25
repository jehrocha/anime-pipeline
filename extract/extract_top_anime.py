import requests
import time
import psycopg

def extract_top_anime(page = 1):
    top_anime = []
    base_url = "https://api.jikan.moe/v4/top/anime"

    while len(top_anime) < 100:
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
            if len(top_anime) >= 100:
                break

            anime_id = anime.get("mal_id")
            title = anime.get("title_english") or anime.get("title")
            episodes = anime.get("episodes") or 0
            status = anime.get("status")
            year = anime.get("year")
            rank = anime.get("rank")
            score = anime.get("score")
            members = anime.get("members")

            top_anime.append((anime_id, title, episodes, status, rank, score, members, year))

        print(f"Page {page} done, total titles so far: {len(top_anime)}")
        page += 1
        time.sleep(1)

    return top_anime



