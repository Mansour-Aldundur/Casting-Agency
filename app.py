import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    # Endpoints

    @app.route('/')
    def hello():
        return 'Hello ! , welcome to the cating agency API'

    @app.route('/actors')
    def view_actors():
        try:
            actors = [actor.format for actor in Actor.query.all()]

            return jsonify({
                'success': True,
                'message': 'Actors successfully fetched',
                'actors': actors
            }), 200

        except Exception:
            abort(422)

    @app.route('/movies')
    def view_movies():
        try:
            movies = [movie.format for movie in Movie.query.all()]

            return jsonify({
                'success': True,
                'message': 'Movies successfully fetched',
                'movies': movies
            }), 200

        except Exception:
            abort(422)

    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        error = None

        if name is None or age is None or gender is None:
            error = 400
            abort(400)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            created_actor = Actor.query.filter_by(name=name).one_or_none()

            return jsonify({
                'success': True,
                'message': 'successfully added actor',
                'actor': created_actor.format
            }), 201

        except Exception:
            if error == 400:
                abort(400)
            abort(422)

    @app.route('/movies', methods=['POST'])
    def create_movie():
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        error = None

        if title is None or release_date is None:
            error = 400
            abort(400)

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            created_movie = Movie.query.filter_by(title=title).one_or_none()

            return jsonify({
                'success': True,
                'message': 'successfully added movie',
                'movie': created_movie.format
            }), 201

        except Exception:
            if error == 400:
                abort(400)
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    def update_actors(id):
        error = None

        try:
            body = request.get_json()

            actor = Actor.query.filter_by(id=id).one_or_none()

            if actor is None:
                error = 404
                abort(404)

            if not body:
                error = 400
                abort(400)

            actor.name = body.get('name', actor.name)
            actor.age = body.get('age', actor.age)
            actor.gender = body.get('gender', actor.gender)
            actor.update()

            return jsonify({
                'success': True,
                'message': 'successfully updated actor details',
                'actor': actor.format
            }), 200

        except Exception:
            if error == 404:
                abort(404)
            if error == 400:
                abort(400)
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    def update_movies(id):
        error = None

        try:
            body = request.get_json()

            movie = Movie.query.filter_by(id=id).one_or_none()

            if movie is None:
                error = 404
                abort(404)

            if not body:
                error = 400
                abort(400)

            movie.title = body.get('title', movie.title)
            movie.release_date = body.get('release_date', movie.release_date)
            movie.update()

            return jsonify({
                'success': True,
                'message': 'successfully updated movie details',
                'movie': movie.format
            }), 200

        except Exception:
            if error == 404:
                abort(404)
            if error == 400:
                abort(400)
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actors(id):
        error = None

        try:
            actor = Actor.query.filter_by(id=id).one_or_none()

            if actor is None:
                error = 404
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'message': 'successfully deleted actor',
                'deleted_id': actor.id
            }), 200

        except Exception:
            if error == 404:
                abort(404)
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movies(id):
        error = None

        try:
            movie = Movie.query.filter_by(id=id).one_or_none()

            if movie is None:
                error = 404
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'message': 'successfully deleted movie',
                'deleted_id': movie.id
            }), 200

        except Exception:
            if error == 404:
                abort(404)
            abort(422)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
