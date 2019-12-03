import argparse
import logging
import json
import re

from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from flask_jwt_extended import jwt_required, fresh_jwt_required

from . import db
from ..common.config import load_config


class BaseJSONHandler(BaseHTTPRequestHandler):
    """BaseJSONHandler

    This handler class manages incoming POST requests and returns JSON-formatted dictionaries.
    Subclasses are intended to implement the path handlers and associated execution methods.
    """
    def do_POST(self):
        try:
            handler = self.get_handler_for_path(self.path)
            if handler is None:
                self.send_error(404)
            else:
                response_object = handler()
                self._send_json_response(response_object)
        except Exception:
            logging.exception('Uncaught exception')
            self.send_error(500)

    def get_handler_for_path(self, path):
        """get_handler_for_path

        Should be implemented by subclasses.
        Returns:
            Callable if found, None otherwise.
        """
        raise NotImplementedError()

    def _send_json_response(self, json_object):
        response_content = json.dumps(json_object).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response_content))
        self.end_headers()
        self.wfile.write(response_content)


class RequestHandler(BaseJSONHandler):

    """RequestHandler

    Implements path handlers for the server.
    """

    urlPath = []
    ANIMALID = 2
    ANIMALNAME = 3
    ANIMALSPECIES = 2

    def splitInputPath(self, path):
        return Path(path).parts

    def get_handler_for_path(self, path):
        self.urlPath = self.splitInputPath(path)
        print("urlpath: ", self.urlPath)
        if path.startswith("/add/"): return self._handle_add_request
        if path.startswith("/animal/"): return self._handle_id_request
        if path.startswith("/species/"): return self._handle_species_request

        handlers = {
            '/status': self._handle_status_request,
            '/animals': self._handle_animals_request,
        }
        return handlers.get(path)

    # default - return server status
    def _handle_status_request(self):
        print('in handle status')
        return {'status': 'ok'}

    # return all animals
    # format /animals
    def _handle_animals_request(self):
        print('in handle animals')
        session = self.server.database.create_session()
        try:
            animals = session.query(db.Animal).all()
            return {'animals': [a.as_dict() for a in animals]}
        finally:
            session.close()

    # return single animal by id
    # format animal/<id>
    def _handle_id_request(self):
        session = self.server.database.create_session()
        try:
            animal = session.query(db.Animal).filter(db.Animal.id == self.urlPath[self.ANIMALID])
            return {'animal': [a.as_dict() for a in animal]}
        finally:
            session.close()

    # return single animal by species
    # case matters
    # format <species>/<value>
    def _handle_species_request(self):
        session = self.server.database.create_session()
        try:
            animal = session.query(db.Animal).filter(db.Animal.species == self.urlPath[self.ANIMALSPECIES])
            return {'animal': [a.as_dict() for a in animal]}
        finally:
            session.close()

    # return added animal or existing match
    # case and order matter
    # format add/<species>/<name>
    def _handle_add_request(self):
        session = self.server.database.create_session()
        try:

            # does this specific animal already exist?
            animal = session.query(db.Animal).filter(db.Animal.species == self.urlPath[self.ANIMALSPECIES],
                        db.Animal.name == self.urlPath[self.ANIMALNAME]).first()
            print("animal: ", animal)
            if not animal:
                animal = db.Animal()
                animal.species = self.urlPath[self.ANIMALSPECIES]
                animal.name = self.urlPath[self.ANIMALNAME]
                animal.id = None
                session.add(animal)
                session.commit()
                session.refresh(animal)
                return {'newly added animal': [animal.as_dict()]}

            return {'animal already exists': [animal.as_dict()]}
        finally:
            session.close()


class Server(HTTPServer):
    def __init__(self, config):
        super().__init__(
            (config['hostname'], config['port']),
            RequestHandler,
        )
        self.config = config
        self.database = db.Database(config)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Simulation server starting...')
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='simulation.cfg')
    args = parser.parse_args()

    httpd = Server(load_config(args.config))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
