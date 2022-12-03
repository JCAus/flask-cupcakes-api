"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template, flash, redirect
from forms import Add_Cupcake_Form, Edit_Cupcake_Form
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/')
def index_page():
    """Renders template that shows all cupcakes - JS frontend"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/add-cupcake', methods=["GET", "POST"])
def add_cupcake_page():
    """Renders a form to add a cupcake"""
    form = Add_Cupcake_Form()
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data

        cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
        db.session.add(cupcake)
        db.session.commit()
        flash(f"{cupcake.flavor} cupcake successfully added.")
        return redirect('/')
    else:
        return render_template('add_cupcake.html', form=form)

@app.route('/cupcakes/<int:cupcake_id>')
def show_cupcake(cupcake_id):
    """Show a specific cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return render_template("cupcake_profile.html", cupcake=cupcake)

@app.route('/cupcakes/<int:cupcake_id>/edit-cupcake', methods=["GET", "POST"])
def edit_cupcake(cupcake_id):
    """Renders a form to edit a cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    form = Edit_Cupcake_Form(obj=cupcake)

    if form.validate_on_submit():
        cupcake.image = form.image.data
        cupcake.size = form.size.data
        cupcake.rating= form.rating.data
        db.session.commit()
        flash(f"{cupcake.flavor} cupcake has been successfully updated.")
        return redirect('/')
    else:
        return render_template("edit_cupcake.html", form=form, cupcake=cupcake)

@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_todo():
    """Creates a new cupcake and returns its JSON"""
    new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a cupcake and responds with JSON of that cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_todo(id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")  