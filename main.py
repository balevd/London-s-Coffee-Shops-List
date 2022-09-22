from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from flask_bootstrap import Bootstrap
from requests import request

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __init__(self, name, map_url, img_url, location, seats, has_toilet, has_wifi, has_sockets, can_take_calls, coffee_price):
        self.name=name
        self.map_url = map_url
        self.img_url = img_url
        self.location = location
        self.seats = seats
        self.has_toilet = has_toilet
        self.has_wifi = has_wifi
        self.has_sockets = has_sockets
        self.can_take_calls = can_take_calls
        self.coffee_price = coffee_price
db.create_all()

class AddCafe(FlaskForm):

    cafe_name = StringField('Cafe Name: ')
    cafe_map_url = StringField('Cafe Map URL: ')
    cafe_img_url = StringField('Cafe img URL: ')
    cafe_location = StringField('Cafe Location: ')
    cafe_seats = StringField('Cafe Seat Availability: ')
    cafe_has_toilet = BooleanField()
    cafe_has_wifi = BooleanField()
    cafe_has_sockets = BooleanField()
    cafe_can_take_calls = BooleanField()
    cafe_coffee_price = StringField('Coffee Price: ')
    submit = SubmitField("Add Cafe")



@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)


@app.route("/add", methods=["GET","POST"])
def post_new_cafe():
    add_cafe = AddCafe()
    if add_cafe.validate_on_submit():
        new_cafe = Cafe(

            add_cafe.cafe_name.data,
            add_cafe.cafe_map_url.data,
            add_cafe.cafe_img_url.data,
            add_cafe.cafe_location.data,
            add_cafe.cafe_seats.data,
            add_cafe.cafe_has_toilet.data,
            add_cafe.cafe_has_wifi.data,
            add_cafe.cafe_has_sockets.data,
            add_cafe.cafe_can_take_calls.data,
            add_cafe.cafe_coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=add_cafe)

@app.route("/delete/<int:id>")
def delete_cafe(id):

    cafe = db.session.query(Cafe).get(id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)