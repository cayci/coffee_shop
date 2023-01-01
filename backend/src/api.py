import os
import traceback
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from pprint import pprint
from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks():
    drinks=Drink.query.order_by(Drink.title).all()
    formatted_drinks=[]
    for drink in drinks:
        formatted_drinks.append(drink.short())
    return jsonify({
        "success":True,
        "drinks": formatted_drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    
    drinks=Drink.query.order_by(Drink.title).all()
    formatted_drinks=[]
    for drink in drinks:
        formatted_drinks.append(drink.long())
    return jsonify({
        "success":True,
        "drinks": formatted_drinks
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    body = request.get_json()
    title = body.get('title')
    recipe = json.dumps(body.get('recipe'))
    new_drink = Drink(title=title, recipe=recipe)
    try:
        db.session.add(new_drink)
        db.session.commit()
    
        return jsonify({
            "success": True,
            "drinks": new_drink.long()
        })
    except Exception as err:
        print(traceback.format_exc())
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    try:
        drink_for_deletion = Drink.query.filter_by(id=drink_id).all()
        if len(drink_for_deletion) == 1:
            drink_for_deletion[0].delete()
            db.session.commit()
            return jsonify({
                "success":True,
                "delete": drink_id
            })
        else:
            abort(404)
    except:
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    try:
        drink_for_update = Drink.query.filter_by(id=drink_id).all()
        if len(drink_for_update) == 1:
            body=request.get_json()
            title = body.get("title")
            recipe = body.get("recipe")
            if title is not None: 
                drink_for_update[0].title = title
            if recipe is not None:
                drink_for_update[0].recipe = json.dumps(recipe)
            db.session.commit()
            return jsonify({
                "success":True,
                "updated":drink_id
            })
        else:
            abort(404)
    except Exception as err:
        print(traceback.format_exc())
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401