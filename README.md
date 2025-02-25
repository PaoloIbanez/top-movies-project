# My Top 10 Movies

## Description
"My Top 10 Movies" is a dynamic web application developed using Flask, WTForms, SQLite, and SQLAlchemy. It allows users to compile a personalized list of their top 10 favorite movies, including features to add reviews, ratings, and fetch movie details automatically through The Movie Database (TMDb) API. The app is designed with a responsive and modern UI using Bootstrap-Flask.

## Features
- **Add Movies:** Users can search and add movies via The Movie Database API.
- **Movie Management:** Create, read, update, and delete movies in the personalized list.
- **Ratings and Reviews:** Provide reviews and rate movies directly from the app.
- **API Integration:** Automatically fetch movie data such as title, year, description, and image.
- **Mobile-Responsive Design:** Styled with Bootstrap-Flask for an optimal experience on both desktop and mobile devices.
- **Dynamic Ranking:** Automatically ranks movies based on user ratings.

## Technologies and Tools Used
- **Frontend:** HTML, CSS, Bootstrap-Flask
- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **API Integration:** The Movie Database (TMDb) API
- **Validation:** WTForms for form handling
- **Version Control:** Git & GitHub

## Installation and Setup

### Prerequisites
- Python (>= 3.8)
- Git

### Instructions

1. **Clone the Repository:**
```bash
git clone <repository_url>
cd top-movies-project
```

2. **Create a Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate # On Windows use: .venv\Scripts\activate
```

3. **Install Required Packages:**
```bash
pip install -r requirements.txt
```

4. **Initialize the Database:**
```bash
python
>>> from main import db
>>> db.create_all()
>>> exit()
```

5. **Run the Application:**
```bash
flask run
```

6. **Access the App:**
Open your browser and go to `http://127.0.0.1:5000`

## How to Use
- **Add Movies:** Search for a movie title and select the correct option from the API results.
- **Edit Ratings and Reviews:** Update the movie details to reflect your opinions.
- **Delete Movies:** Remove movies from your list as desired.
- **Dynamic Ranking:** Movies are automatically ranked based on your ratings.

## Future Improvements
- Add user authentication to allow personalized movie lists.
- Enhance search functionality with auto-complete.
- Introduce a community rating feature to see average ratings from all users.

## License
This project is licensed under the MIT License.

## Author
Built by Paolo Ibanez Medina

