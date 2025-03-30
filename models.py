from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()  # Define the SQLAlchemy database instance

class Superhero(db.Model, SerializerMixin):
    __tablename__ = 'superheroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    power = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship("City", back_populates="superheroes")
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class City(db.Model, SerializerMixin):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    superheroes = db.relationship("Superhero", back_populates="city")

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    super_name = db.Column(db.String, index=True)
    hero_powers = db.relationship("HeroPower", back_populates="hero")

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String, nullable=False)
    hero_powers = db.relationship("HeroPower", back_populates="power")

    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return value

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="hero_powers")

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return value