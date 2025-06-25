from extract.extract_genre import extract_genre, extract_anime_genre
from extract.extract_studio import extract_studio, extract_anime_studios
from extract.extract_top_anime import extract_top_anime
from load.load_to_postgres import insert_genre, insert_anime_genre, insert_anime_studio, insert_studio, insert_top_anime

genre_list = extract_genre()
insert_genre(genre_list)

anime_genre_list = extract_anime_genre()
insert_anime_genre(anime_genre_list)

studio_list = extract_studio()
insert_studio(studio_list)

anime_studio_list = extract_anime_studios()
insert_anime_studio(anime_studio_list)

top_anime_list = extract_top_anime()
insert_top_anime(top_anime_list)
