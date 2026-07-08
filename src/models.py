from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

db = SQLAlchemy()

favorites_characters_table = db.Table(
    "favorites_characters",
    db.Column("user_id", ForeignKey("user.id"), primary_key=True),
    db.Column("character_id", ForeignKey("characters.id"), primary_key=True),
)

favorites_planets_table = db.Table(
    "favorites_planets",
    db.Column("user_id", ForeignKey("user.id"), primary_key=True),
    db.Column("planet_id", ForeignKey("planets.id"), primary_key=True),
)

favorites_vehicles_table = db.Table(
    "favorites_vehicles",
    db.Column("user_id", ForeignKey("user.id"), primary_key=True),
    db.Column("vehicle_id", ForeignKey("vehicles.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(256), nullable=False)

    favorite_characters: Mapped[list["Character"]] = relationship(
        secondary=favorites_characters_table,
        back_populates="favorited_by"
    )

    favorite_planets: Mapped[list["Planet"]] = relationship(
        secondary=favorites_planets_table,
        back_populates="favorited_by"
    )

    favorite_vehicles: Mapped[list["Vehicle"]] = relationship(
        secondary=favorites_vehicles_table,
        back_populates="favorited_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }


class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[Optional[int]] = mapped_column(nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(
        secondary=favorites_planets_table,
        back_populates="favorite_planets"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
        }


class Character(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    hair_color: Mapped[str] = mapped_column(String(50), nullable=False)
    eye_color: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    birth_year: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )

    favorited_by: Mapped[list["User"]] = relationship(
        secondary=favorites_characters_table,
        back_populates="favorite_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
        }


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    model: Mapped[str] = mapped_column(
        String(120), nullable=False
    )
    passengers: Mapped[Optional[int]] = mapped_column(nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(
        secondary=favorites_vehicles_table,
        back_populates="favorite_vehicles"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers,
        }
