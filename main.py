from http.client import HTTPException
from logging import exception, error

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
#from sqlalchemy.sql.functions import random
import random

# Initialize Flask application
app = Flask(__name__)

# --- Database Configuration ---
# Define the base class for SQLAlchemy ORM
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    """
        Model representing a Cafe in the database.
        Attributes:
            id (int): Primary key of the cafe.
            name (str): Name of the cafe.
            map_url (str): Google Maps URL of the cafe.
            img_url (str): Image URL of the cafe.
            location (str): Location of the cafe.
            seats (str): Available seating information.
            has_toilet (bool): Whether the cafe has a toilet.
            has_wifi (bool): Whether the cafe has Wi-Fi.
            has_sockets (bool): Whether the cafe has power sockets.
            can_take_calls (bool): Whether calls can be taken at the cafe.
            coffee_price (str): Price of coffee at the cafe.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dict = {}
        # loop through each column in the data record
        for column in self.__table__.columns:
            # create new dictionary entry
            # where key is the name of column
            # and the value is the value of column
            dict[column.name]=getattr(self,column.name)
        return  dict


# Create all tables in the database
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route("/")
def home():
    """
        Render the home page.
        Returns:
            HTML: Rendered home page template.
     """
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def random_choice():
   """
       Fetch a random cafe from the database.
       Returns:
           JSON: A random cafe's details in JSON format.
    """
   all_cafe = db.session.execute(db.select(Cafe)).scalars().all()
   random_cafe = random.choice(all_cafe)
   # Simply convert the random cafe data record to a dictionary of key-value pairs
   return  jsonify(cafe=random_cafe.to_dict())


# HTTP GET - Read Record
@app.route("/all",methods=["GET"])
def get_all():
    """
       Fetch all cafes from the database.
       Returns:
           JSON: A list of all cafes in JSON format.
       """
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    cafe_list = []
    for cafe in all_cafes:

        cafe_list.append(cafe.to_dict())
    return jsonify(cafe_list)

@app.route("/search",methods=["GET"])
def search():
    """
       Search for cafes by location.
       Query Parameters:
           loc (str): The location to search for.
       Returns:
           JSON: Cafes in the specified location or an error message.
       """
    query_location = request.args.get("loc")
    cafe_list = []
    cafes_at_location = db.session.execute(db.select(Cafe).where(Cafe.location==query_location)).scalars().all()
    if cafes_at_location:
        for cafe in cafes_at_location:
            cafe_list.append(cafe.to_dict())
        return jsonify(cafe_list)

    else:
        return jsonify(error={"Not Found":"Sorry, We don't have cafe at this location."}),404



# HTTP POST - Create Record
@app.route("/add",methods=["GET","POST"])
def add():

    """
    Add a new cafe to the database.
    Query Parameters:
        Various: Details about the new cafe.
    Returns:
        JSON: Success message or error message.
    """
        
    new_cafe = Cafe(

        name = request.args.get("name"),
        map_url = request.args.get("map_url"),
        img_url = request.args.get("img_url"),
        location = request.args.get("location"),
        seats = request.args.get("seats"),
        has_toilet =request.args.get("has_toilet")=='true',
        has_wifi = request.args.get("has_wifi")=='true',
        has_sockets = request.args.get("has_sockets")=='true',
        can_take_calls = request.args.get("can_take_call")=='true',
        coffee_price = request.args.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response = {"Success":"Successfully added to the new cafe."}),201



# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>",methods=["PATCH"])
def update_price(cafe_id):
    """
       Update the coffee price of a specific cafe.
       Query Parameters:
           coffee_price (str): The new coffee price.
       Path Parameters:
           cafe_id (int): The ID of the cafe to update.
       Returns:
           JSON: Success or error message.
       """
    cafe = db.session.get(Cafe,cafe_id)
    if cafe:
        cafe.coffee_price = request.args.get("coffee_price") # new coffee price entered on the url
        db.session.commit()
        return jsonify(response = {"Success":"Successfully Updates the price."})
    else:
        return jsonify(response = {"error": "Sorry  a cafe with that Id not found in the database"}),404

#
# # HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>",methods=["DELETE"])
def delete_cafe(cafe_id):
    """
       Delete a cafe from the database securely using an API key.
       Query Parameters:
           api-key (str): The API key for authentication.
       Path Parameters:
           cafe_id (int): The ID of the cafe to delete.
       Returns:
           JSON: Success or error message.
       """
    api_key = request.args.get("api-key")
    print(api_key)
    if api_key == "TopSecretAPIKey":
       cafe = db.session.get(Cafe,cafe_id)
       if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"Success":"Cafe has been deleted Successfully!!"}),200

       else:
            return jsonify(error ={"error" :" The Cafe with given id was not found in the database."}),404
    else:
        return jsonify(error={"Forbidden":"Sorry,that's not allowed. Make sure you have the correct api_key."}),403

# Run the application (for development purposes only)
if __name__ == '__main__':
    app.run(debug=True)
