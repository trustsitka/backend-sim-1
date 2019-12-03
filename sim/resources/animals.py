from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                fresh_jwt_required,
                                jwt_required)

from sim.server.animals import Animals

_animal_parser = reqparse.RequestParser()
_animal_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="animal name cannot be null"
)

_animal_parser.add_argument(
    "species",
    type=str,
    required=True,
    help="animal species cannot be null"
)


class AllAnimals(Resource):
    @jwt_required
    def get(self):
        animals = Animals.find_all_animals()
        if animals:
            return animals.jsonify({animals: [animals]})

        return {
                   "message": "animals not found!"
               }, 404


class Species(Resource):

    def get(self, species):
        animals = Animals.find_animal_by_species(species)
        if animals:
            return animals.jsonify({animals: [animals]})

        return {
                   "message": "species not found!"
               }, 404


class Animal(Resource):

    @jwt_required
    def get(self, id):
        animal = Animals.find_animal_by_id(id)
        if animal:
            return animal.json()

        return {
                   "message": "animal not found!"
               }, 404


class AddAnimal(Resource):
    def post(self):
        data = _animal_parser.parse_args()

        if Animals.find_animal_by_species_name(data["name"], data["species"]):
            return {
                       "message": "this animal already exists!"
                   }, 400

        animal = Animals(data["name"], data["species"])
        animal.save_to_db()
