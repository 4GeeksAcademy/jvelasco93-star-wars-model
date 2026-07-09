from app import app
from models import db, User, Planet, Character, Vehicle

with app.app_context():
    db.drop_all()
    db.create_all()

    # --- Users ---
    user1 = User(
        username="lskywalker",
        first_name="Luke",
        last_name="Skywalker",
        email="luke@jedi.com",
        password="force123",
    )
    user2 = User(
        username="darthvader",
        first_name="Anakin",
        last_name="Skywalker",
        email="vader@empire.com",
        password="dark123",
    )

    db.session.add_all([user1, user2])

    # --- Planets ---
    planets = [
        Planet(name="Tatooine", climate="arid", population=200000),
        Planet(name="Alderaan", climate="temperate", population=2000000000),
        Planet(name="Hoth", climate="frozen", population=None),
        Planet(name="Endor", climate="forest", population=30000000),
        Planet(name="Dagobah", climate="swamp", population=None),
    ]
    db.session.add_all(planets)

    # --- Characters ---
    characters = [
        Character(
            name="Luke Skywalker",
            hair_color="blond",
            eye_color="blue",
            birth_year="19BBY",
        ),
        Character(
            name="Leia Organa",
            hair_color="brown",
            eye_color="brown",
            birth_year="19BBY",
        ),
        Character(
            name="Darth Vader",
            hair_color="none",
            eye_color="yellow",
            birth_year="41BBY",
        ),
        Character(
            name="Han Solo",
            hair_color="brown",
            eye_color="brown",
            birth_year="29BBY",
        ),
        Character(
            name="Chewbacca",
            hair_color="brown",
            eye_color="blue",
            birth_year="200BBY",
        ),
    ]
    db.session.add_all(characters)

    # --- Vehicles ---
    vehicles = [
        Vehicle(name="Millennium Falcon", model="YT-1300", passengers=6),
        Vehicle(name="X-wing", model="T-65", passengers=1),
        Vehicle(name="TIE Fighter", model="TIE/ln", passengers=1),
        Vehicle(name="Star Destroyer", model="Imperial I", passengers=37000),
        Vehicle(name="Landspeeder", model="X-34", passengers=2),
    ]
    db.session.add_all(vehicles)

    # --- Favorites ---
    user1.favorite_planets.append(planets[0])  # Tatooine
    user1.favorite_planets.append(planets[1])  # Alderaan
    user1.favorite_characters.append(characters[0])  # Luke
    user1.favorite_vehicles.append(vehicles[0])  # Falcon

    user2.favorite_planets.append(planets[2])  # Hoth
    user2.favorite_characters.append(characters[2])  # Vader
    user2.favorite_vehicles.append(vehicles[2])  # TIE Fighter

    db.session.commit()
    print("Seed completado ✅")
