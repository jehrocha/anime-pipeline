import psycopg

def insert_genre(genre_list):
    try:
        with psycopg.connect(dbname="anime", user="postgres") as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS genre(
                        genre_id SERIAL PRIMARY KEY,
                        genre VARCHAR(15) UNIQUE
                    );
                """)

                insert_query = """
                    INSERT INTO genre (genre)
                    VALUES (%s)
                    ON CONFLICT (genre) DO NOTHING; 
                """

                cur.executemany(insert_query, genre_list)
            conn.commit()

    except psycopg.Error as e:
        print("A database error occurred:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

def insert_anime_genre(anime_genre_list):
    try:
        with psycopg.connect(dbname="anime", user="postgres") as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS anime_genre(
                    anime_id INTEGER NOT NULL,
                    genre_id SMALLINT NOT NULL,
                    PRIMARY KEY(anime_id, genre_id),
                    FOREIGN KEY (anime_id) REFERENCES top_anime(anime_id) ON DELETE CASCADE,
                    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
                    );
                """)

                anime_genre_rows = []
                for anime in anime_genre_list:
                    anime_id = anime[0]
                    genre_name = anime[1]

                    cur.execute("SELECT genre_id FROM genre WHERE genre = %s;", (genre_name,))
                    result = cur.fetchone()[0]

                    if result:
                        genre_id = result
                        anime_genre_rows.append((anime_id, genre_id))
                    else:
                        print(f"Genre '{genre_name}' not found for Anime ID: {anime_id}.")

                cur.executemany("""
                    INSERT INTO anime_genre (anime_id, genre_id)
                    VALUES (%s, %s)
                    ON CONFLICT (anime_id, genre_id) DO NOTHING;
                """, anime_genre_rows)

            conn.commit()

    except psycopg.Error as e:
        print("A database error occurred:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

def insert_top_anime(top_anime_list):
    try:
        with psycopg.connect(dbname="anime", user="postgres") as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS top_100_anime(
                        anime_id INTEGER PRIMARY KEY UNIQUE,
                        title TEXT NOT NULL,
                        episodes SMALLINT CHECK (episodes >= 0),
                        status VARCHAR(20),
                        rank SMALLINT CHECK(rank >= 0)  ,
                        score NUMERIC(3,2) CHECK (score BETWEEN 0 AND 10),
                        members INTEGER CHECK (members >= 0),
                        year SMALLINT CHECK (year >= 1900)
                    )
                """
                            )

                insert_query = """
                    INSERT INTO top_100_anime (anime_id, title, episodes, status, rank, score, members, year)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (anime_id) DO NOTHING
                """

                cur.executemany(insert_query, top_anime_list)
            conn.commit()

    except psycopg.Error as e:
        print("A database error occurred:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

def insert_studio(studio_list):
    try:
        with psycopg.connect(dbname="anime", user="postgres") as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS studio (
                        studio_id SERIAL PRIMARY KEY,
                        studio_name VARCHAR(25) UNIQUE NOT NULL
                    );
                """)

                insert_query = """
                    INSERT INTO studio (studio_name)
                    VALUES (%s)
                    ON CONFLICT (studio_name) DO NOTHING;
                """

                cur.executemany(insert_query, studio_list)
            conn.commit()

    except psycopg.Error as e:
        print("A database error occurred:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

def insert_anime_studio(anime_studio_list):
    try:
        with psycopg.connect(dbname="anime", user="postgres") as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS anime_studio (
                        anime_id INTEGER,
                        studio_id SMALLINT,
                        PRIMARY KEY(anime_id, studio_id),
                        FOREIGN KEY (anime_id) REFERENCES top_anime(anime_id) ON DELETE CASCADE,
                        FOREIGN KEY (studio_id) REFERENCES studio(studio_id) ON DELETE CASCADE
                    );
                """)

                studio_rows = []
                
                for anime in anime_studio_list:
                    anime_id = anime[0]
                    studio_name = anime[1]

                    cur.execute("SELECT studio_id FROM studio WHERE studio_name = %s;", (studio_name,))
                    studio_id = cur.fetchone()[0]
                    studio_rows.append((anime_id, studio_id))

                cur.executemany("""
                     INSERT INTO anime_studio (anime_id, studio_id)
                     VALUES (%s, %s)
                     ON CONFLICT (anime_id, studio_id) DO NOTHING;
                """, studio_rows)

            conn.commit()

    except psycopg.Error as e:
        print("A database error occurred:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

