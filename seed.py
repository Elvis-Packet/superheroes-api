import sqlite3
from faker import Faker

fake = Faker()

def create_schema(cursor):
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS superheroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city_id INTEGER NOT NULL,
        FOREIGN KEY (city_id) REFERENCES cities (id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        superpower TEXT NOT NULL,
        superhero_id INTEGER NOT NULL,
        FOREIGN KEY (superhero_id) REFERENCES superheroes (id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS powers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hero_powers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hero_id INTEGER NOT NULL,
        power_id INTEGER NOT NULL,
        FOREIGN KEY (hero_id) REFERENCES heroes (id),
        FOREIGN KEY (power_id) REFERENCES powers (id)
    )
    ''')

def seed_data(cursor):
    # Seed Cities
    cities = []
    for _ in range(5):
        city_name = fake.city()
        cursor.execute('INSERT INTO cities (name) VALUES (?)', (city_name,))
        cities.append(cursor.lastrowid)

    # Seed Superheroes
    superheroes = []
    for _ in range(10):
        superhero_name = fake.name()
        city_id = fake.random_element(cities)
        cursor.execute('INSERT INTO superheroes (name, city_id) VALUES (?, ?)', (superhero_name, city_id))
        superheroes.append(cursor.lastrowid)

    # Seed Heroes
    heroes = []
    for _ in range(100):
        hero_name = fake.name()
        superpower = fake.word()
        superhero_id = fake.random_element(superheroes)
        cursor.execute('INSERT INTO heroes (name, superpower, superhero_id) VALUES (?, ?, ?)', (hero_name, superpower, superhero_id))
        heroes.append(cursor.lastrowid)

    # Seed Powers
    powers = []
    for _ in range(100):
        power_name = fake.word()
        description = fake.text(max_nb_chars=50)
        cursor.execute('INSERT INTO powers (name, description) VALUES (?, ?)', (power_name, description))
        powers.append(cursor.lastrowid)

    # Seed HeroPowers
    for _ in range(150):
        hero_id = fake.random_element(heroes)
        power_id = fake.random_element(powers)
        cursor.execute('INSERT INTO hero_powers (hero_id, power_id) VALUES (?, ?)', (hero_id, power_id))

def main():
    try:
        conn = sqlite3.connect('superhero.db')
        cursor = conn.cursor()

        # Ensure schema is created
        create_schema(cursor)

        # Clear existing data
        cursor.execute('DELETE FROM hero_powers')
        cursor.execute('DELETE FROM powers')
        cursor.execute('DELETE FROM heroes')
        cursor.execute('DELETE FROM superheroes')
        cursor.execute('DELETE FROM cities')

        # Seed data
        seed_data(cursor)

        conn.commit()
        print("Database seeded successfully!")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
