"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/api')
def nothing():
    return "hi"

@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    """Get data about all cupcakes."""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>', methods=["GET"])
def get_cupcake(id):
    """Get data for single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a cupcake with  flavor, size, rating and image data from the body of the request."""
    
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cake = Cupcake(flavor=flavor, rating=rating, size=size, image=image)
    db.session.add(new_cake)
    db.session.commit()

    return (jsonify(cupcake=new_cake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. Assume the entire cupcake obj will be passed to the backend."""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")







