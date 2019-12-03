from sim.server.db import db


class Animals(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    def __init__(self, name, species):
        self.name = name
        self.species = species

    def json(self):
        return {
                   'id': self.id,
                   'name': self.name,
                   'species': self.species
               }, 200

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_animal_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_animal_by_species(cls, species):
        return cls.query.filter_by(species=species)

    @classmethod
    def find_animal_by_species_name(cls, species, name):
        return cls.query.filter_by(species=species, name= name)

    @classmethod
    def find_all_animals(cls):
        return cls.query.all()