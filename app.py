import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import Actor, Movie, setup_db, db_drop_and_create_all
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    '''
  After_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    ''' ACTORS ROUTES '''
    ''' GET all /actors'''

    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors(jwt):
        try:
            query = Actor.query.all()

            if not query:
                abort(404)

            return jsonify({
                'status': 200,
                'success': True,
                'actors': [i.format() for i in query],
                'total_actors': len(query)
            })
        except BaseException:
            abort(500)

    ''' POST /actors'''

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actor")
    def post_actors(jwt):
        try:
            body = request.get_json()
            if not body:
                abort(400)

            actor = Actor(
                name=body['name'],
                age=body['age'],
                gender=body['gender'])
            actor.insert()
            query = Actor.query.all()

            return jsonify({
                'status': 201,
                'success': True,
                'actor': actor.format(),
                'total_actors': len(query)
            })
        except BaseException:
            abort(400)

    ''' DELETE /actors'''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actors(jwt, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if actor_id is None:
                abort(404)
            else:
                actor.delete()
                query = Actor.query.all()

                return jsonify({
                    'status': 200,
                    'success': True,
                    'deleted': actor_id,
                    'total_actors': len(query)
                })
        except BaseException:
            abort(422)

    ''' PATCH /actors'''

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def patch_actors(jwt, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()
            if actor_id is None:
                abort(404)
            else:
                body = request.get_json()
                if not body:
                    abort(400)

                actor.name = body['name']
                actor.age = body['age']
                actor.gender = body['gender']
                actor.update()

                query = Actor.query.all()

                return jsonify({
                    'status': 200,
                    'success': True,
                    'updated': actor.format(),
                    'total_actors': len(query)
                })
        except BaseException:
            abort(422)

    ''' MOVIES ROUTES '''
    ''' GET all /actors'''

    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies(jwt):
        try:
            query = Movie.query.all()

            if not query:
                abort(404)

            return jsonify({
                'status': 200,
                'success': True,
                'movies': [i.format() for i in query],
                'total_movies': len(query)
            })
        except BaseException:
            abort(500)

    ''' POST /movies'''

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movie")
    def post_movies(jwt):
        try:
            body = request.get_json()
            if not body:
                abort(400)

            movie = Movie(
                title=body['title'],
                release_date=body['release_date'])
            movie.insert()
            query = Movie.query.all()

            return jsonify({
                'status': 201,
                'success': True,
                'movie': movie.format(),
                'total_movies': len(query)
            })
        except BaseException:
            abort(400)

    ''' DELETE /movies'''

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movies(jwt, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()

            if movie_id is None:
                abort(404)
            else:
                movie.delete()
                query = Movie.query.all()

                return jsonify({
                    'status': 200,
                    'success': True,
                    'deleted': movie_id,
                    'total_movies': len(query)
                })
        except BaseException:
            abort(422)

    ''' PATCH /actors'''

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movies")
    def patch_movies(jwt, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()
            if movie_id is None:
                abort(404)
            else:
                body = request.get_json()
                if not body:
                    abort(400)

                movie.title = body['title']
                movie.release_date = body['release_date']
                movie.update()

                query = Movie.query.all()

                return jsonify({
                    'status': 200,
                    'success': True,
                    'updated': movie.format(),
                    'total_movies': len(query)
                })
        except BaseException:
            abort(422)

        '''
  Create error handlers for all expected errors
  '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request",
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized",
        }), 401

    @app.errorhandler(403)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden",
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found",
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed",
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity",
        }), 422

    @app.errorhandler(500)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server error",
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
