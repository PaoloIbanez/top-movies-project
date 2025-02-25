from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap5(app)

API_KEY = "2e10226845d1dd58783cd86d18059c46"  # Replace with your TMDB API key

# -------------------- Database Setup -------------------- #
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

# -------------------- WTForms -------------------- #
class RateMovieForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 e.g. 7.5", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

# -------------------- Routes -------------------- #
@app.route("/")
def home():
    # Order by title, just to see them in alphabetical order
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars().all()
    # Debug print to verify data
    for movie in all_movies:
        print(movie.id, movie.title, movie.year, movie.rating, movie.ranking, movie.review, movie.img_url)
    return render_template("index.html", movies=all_movies)

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        # Fetch matching movies from TMDB
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": API_KEY, "query": movie_title}
        )
        data = response.json()["results"]
        return render_template("select.html", movies=data)
    return render_template("add.html", form=form)

@app.route("/add_selected/<int:movie_id>")
def add_selected(movie_id):
    # Get movie details
    movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(movie_api_url, params={"api_key": API_KEY})
    data = response.json()

    # Create a new Movie with partial details
    new_movie = Movie(
        title=data["title"],
        year=int(data["release_date"].split("-")[0]),
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
        rating=0.0,
        ranking=0,
        review="No review yet."
    )
    db.session.add(new_movie)
    db.session.commit()

    # Redirect to edit the rating and review
    return redirect(url_for("edit", id=new_movie.id))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()

    if form.validate_on_submit():
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", movie=movie_to_update, form=form)

@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
