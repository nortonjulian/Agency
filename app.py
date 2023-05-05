from flask import Flask, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = "secret"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """List all pets"""
    # available_pets = Pet.query.filter_by(available=True).all()
    # unavailable_pets = Pet.query.filter_by(available=False).all()
    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Add a pet"""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        species = form.species.data
        photo_url = form.photo_url.data
        notes = form.photo_url.data
        new_pet = Pet(name=name, age=age, species=species, photo_url=photo_url, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added!")
        return redirect("pet_list.html")
    else:
        return render_template("add_pet_form.html")

@app.route("/<int:pid>", methods=["GET","POST"])
def edit_pet(pid):
    """Edit Pet"""

    pet = Pet.query.get_or_404(pid)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        flash(f"Pet {pid} updated!")
        return redirect("pet_list.html")
    else:
        return render_template("pet_edit.html", form=form, pet=pet)
