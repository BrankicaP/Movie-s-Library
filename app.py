from flask import Flask, render_template, request, session, redirect, url_for
import flask_bootstrap
import flask
from flask_mysqldb import MySQL
import yaml
import time
import hashlib

app=Flask(__name__)
app.config['SECRET_KEY']='Brankicaaa'
flask_bootstrap.Bootstrap(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

list_of_category=["action", "thriller", "comedy", "horror", "drama"]

admin_username='admin'
admin_password="admin123"
admin1=hashlib.md5(admin_password.encode())
admin123=admin1.hexdigest()

#*********************** MOVIES **************************************
cur=mysql.connection.cursor()
c = cur.execute("SELECT * from Movie")
if c==0:
    cur.execute("INSERT INTO Movie(MovieName,year,image,language,imdb,category) VALUES (%s,%s,%s,%s,%s,%s)",
                    ['Mrtav Ladan', '2019', 'https://m.media-amazon.com/images/M/MV5BMTk5NDc0MjU3Nl5BMl5BanBnXkFtZTcwNDc3NTU3OQ@@._V1_.jpg', 'srpski',
            9.60, 'comedy, action'])
    cur.execute("INSERT INTO Movie(MovieName,year,image,language,imdb,category) VALUES (%s,%s,%s,%s,%s,%s)",
                    ['Barbie', '2023', 'https://upload.wikimedia.org/wikipedia/en/0/0b/Barbie_2023_poster.jpg', 'engleski', 5.40, 'comedy, drama'])
    cur.execute("INSERT INTO Movie(MovieName,year,image,language,imdb,category) VALUES (%s,%s,%s,%s,%s,%s)",
                    ['Pod zvijezdama Pariza', '2020', 'https://www.cineplexxpalas.ba/images/2023/06/21/_spmedia_thumbs/Pod-zvezdama-400x593.jpg', 'francuski', 8.50, 'comedy, action, drama'])
    cur.execute("INSERT INTO Movie(MovieName,year,image,language,imdb,category) VALUES (%s,%s,%s,%s,%s,%s)",
                    ['Anna', '2019', 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Anna_film_poster.jpg/220px-Anna_film_poster.jpg', 'engleski',8.70, 'action, thriller'])
    cur.execute("INSERT INTO Movie(MovieName,year,image,language,imdb,category) VALUES (%s,%s,%s,%s,%s,%s)",
                    ['Pakleni provod', '2023', 'https://www.cineplexxpalas.ba/images/2023/06/29/_spmedia_thumbs/Joy-ride-400x593.jpg', 'engleski', 7.80, 'comedy, action'])
    mysql.connection.comit()
    cur.close()

@app.route('/login/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if session.get('username') is None:
            cur = mysql.connection.cursor()
            username = request.form.get('username')
            passw = request.form.get('password')
            passw1 = hashlib.md5(passw.encode())
            password = passw1.hexdigest()
            if cur.execute("SELECT * from User where username = %s and password = %s", [username, password]) > 0:
                user = cur.fetchone()
                # print(user)
                session['login'] = True
                session['username'] = user[3]
                session['firstname'] = user[1]
                session['lastname'] = user[2]
                session['email']=user[4]
                session['password']=user[5]
                mysql.connection.commit()
                cur.execute("UPDATE User SET active = 1 WHERE username = %s ", [username])
                mysql.connection.commit()
                movies=[]
                result_value = cur.execute("SELECT * from Movie")
                if result_value > 0:
                   movies = cur.fetchall()
                   return render_template("home.html", movies=movies)
                if session['username']==admin_username and session['password']==admin123:
                    return render_template("home1.html", movies=movies)
                else:
                    return render_template("home.html")
            else:
                flask.flash('Invalid username and password!', 'danger')
                return render_template('login.html')
        else:
            cur = mysql.connection.cursor()
            movies=[]
            result_value = cur.execute("SELECT * from Movie")
            if result_value > 0:
                movies = cur.fetchall()
                return render_template("home.html", movies=movies)
            if session['username'] == admin_username and session['password'] == admin123:
                return render_template("home1.html", movies=movies)
            else:
                return render_template("home.html")
    else:
        if session.get('username') is not None:
            cur = mysql.connection.cursor()
            result_value = cur.execute("SELECT * from Movie")
            movies=[]
            if result_value > 0:
                movies = cur.fetchall()
            if session['username']==admin_username and session['password']==admin123:
                return render_template("home1.html", movies=movies)
            else:
                return render_template("home.html", movies=movies)
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route('/logout/')
def logout():
    if session.get('username') is not None:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE User SET active = 0 WHERE username = %s ", [session['username']])
        mysql.connection.commit()
        session.pop('username')
        return render_template('index.html')
    else:
        return render_template('index.html')
@app.route('/')
def home():
    if session.get('username') is None:
        return render_template("index.html")
    else:
        cur = mysql.connection.cursor()
        movies=[]
        result_value = cur.execute("SELECT * from Movie")
        if result_value > 0:
            movies = cur.fetchall()
        if session['username'] == admin_username and session['password'] == admin123:
            return render_template("home1.html", movies=movies, list=list_of_category)
        else:
            return render_template("home.html", movies=movies, list=list_of_category)
        return render_template("home.html")

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form.get('username')
        passw = request.form.get('password')
        passw1=hashlib.md5(passw.encode())
        password=passw1.hexdigest()
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        gender = request.form.get('gender')
        passw_confirm = request.form.get('passwordConfirm')
        passw1_confirm=hashlib.md5(passw_confirm.encode())
        password_confirm=passw1_confirm.hexdigest()
        if password == password_confirm:
            if (cur.execute("SELECT * from User where username = %s", [username]) == 0) and len(username) >= 5:
                if cur.execute("SELECT * from User where email = %s", [email]) == 0:
                    cur.execute("INSERT INTO User(firstname,lastname,username,email,password,gender) VALUES (%s,%s,%s,%s,%s,%s)",
                                [firstname, lastname, username, email, password, gender])
                    mysql.connection.commit()
                    cur.close()
                    flask.flash('Registration successful! Please login.', 'success')
                    return redirect(url_for('index'))
                else:
                    flask.flash('Email exists!', 'danger')
                    return render_template("registration.html")
            else:
                flask.flash('Username exists!', 'danger')
                return render_template("registration.html")
        else:
            flask.flash('Password error!', 'danger')
            return render_template("registration.html")
    return render_template("registration.html")


@app.route('/movie/<string:name>')
def movie(name):
    if session.get('username') is None:
        return render_template("index.html")
    else:
        cur = mysql.connection.cursor()
        result_value = cur.execute("SELECT * from Movie WHERE MovieName = %s ", [name])
        if result_value > 0:
            m = cur.fetchone()
            return render_template("movie.html", movie=m)
        return render_template("home.html")

@app.route('/movie/rate/<string:name>')
def rate(name):
    if session.get('username') is None:
        return render_template("index.html")
    else:
        cur = mysql.connection.cursor()
        u = cur.execute("SELECT * from user")
        if u > 0:
            user = cur.fetchall()
        m = cur.execute("SELECT * from Movie")
        if m > 0:
            movie = cur.fetchall()
        for m in movie:
            if m[1]==name:
                id_Movie=m[0]
        rates = []
        rate=cur.execute("SELECT * from Rates WHERE Movie_IdMovie=%s ", [id_Movie])
        if rate>0:
            rates=cur.fetchall()
        reviews = []
        review=cur.execute("SELECT * from Reviews WHERE Movie_IdMovie=%s ", [id_Movie])
        if review>0:
            reviews=cur.fetchall()
        return render_template("movie&rate&review.html", name=name, rates=rates, reviews=reviews, users=user, movies=movie)


@app.route('/movie/', methods=['GET', 'POST'])
def create_movie():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        name = request.form.get('name')
        year = request.form.get('year')
        image = request.form.get('image')
        language = request.form.get('language')
        imdb = request.form.get('imdb')
        category = request.form.get('category')
        cur.execute("INSERT INTO Movie(MovieName,year,image,language,imdb,category) VALUES (%s,%s,%s,%s,%s,%s)", [name, year, image, language,imdb,category])
        mysql.connection.commit()
        flask.flash('Movie created!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template("createMovie.html")

@app.route('/movie/category/<int:id>')
def category(id):
    if session.get('username') is None:
        return render_template("index.html")
    else:
        cur=mysql.connection.cursor()
        c = cur.execute("SELECT * from Moviecategory")
        if c==0:
            for i in list_of_category:
                cur.execute("INSERT INTO Moviecategory(CategoryMovie) VALUES (%s)", [i])
                mysql.connection.commit()
        c=cur.execute("SELECT * from Moviecategory")
        cat=cur.fetchall()
        movie=[]
        m = cur.execute("SELECT * from movie")
        if m > 0:
            movie = cur.fetchall()
        for m in movie:
            categoryMovie=m[6].split(",")
            movieId_Movie = m[0]
            for category in categoryMovie:
                if category in list_of_category:
                    movieCategory_IdCategoryMovie=list_of_category.index(category)+1
                    cur.execute("INSERT INTO Movie_has_moviecategory(Movie_IdMovie, MovieCategory_IdCategoryMovie) VALUES (%s,%s)", [movieId_Movie,movieCategory_IdCategoryMovie])
                    mysql.connection.commit()
        result_value = cur.execute("SELECT * from Movie_has_moviecategory WHERE MovieCategory_IdCategoryMovie=%s ", [id])
        if result_value > 0:
            category = cur.fetchall()
        categoriesMovies=[]
        for c in category:
            cMovies=cur.execute("SELECT * from Movie WHERE MovieId=%s", [c[0]])
        categoriesMovies=cur.fetchall()
        cur.close()
        return render_template('category.html', list= list_of_category, category=categoriesMovies )

@app.route('/movie/<string:name>/',methods=['GET', 'POST'])
def create_rate(name):
    if session.get('username') is None:
        return render_template("index.html")
    else:
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            rate = request.form.get('rate')
            review = request.form.get('review')
            timeReview = time.asctime()
            username=session.get('username')
            password=session.get('password')
            u=cur.execute("SELECT * from user")
            if u > 0:
                user = cur.fetchall()
                for i in user:
                    if i[3]==str(username) and i[5]==str(password):
                        user_IdUser = i[0]
            m=cur.execute("SELECT * from movie")
            if m > 0:
                movie = cur.fetchall()
                for i in movie:
                    if i[1] == name:
                        movie_IdMovie = i[0]
            rates = []
            if rate:
                cur.execute("INSERT INTO Rates(Rate,User_IdUser,Movie_IdMovie) VALUES (%s, %s, %s)", [rate,user_IdUser,movie_IdMovie])
            mysql.connection.commit()
            for movieRate in movie:
                if movieRate[1] == name:
                    result_value1 = cur.execute("SELECT * from Rates WHERE Movie_IdMovie=%s", [movieRate[0]])
                    if result_value1 > 0:
                        rates = cur.fetchall()
            reviews = []
            if review:
                cur.execute(
                "INSERT INTO Reviews(TimeReview,ContentReview,User_IdUser,Movie_IdMovie) VALUES (%s,%s, %s, %s)",
                [timeReview, review, user_IdUser, movie_IdMovie])
            mysql.connection.commit()
            for movieRate in movie:
                if movieRate[1] == name:
                    result_value2 = cur.execute("SELECT * from Reviews WHERE Movie_IdMovie=%s", [movieRate[0]])
                    if result_value2 > 0:
                        reviews = cur.fetchall()
            return render_template("rate.html",name=name, rates=rates, reviews=reviews, users=user, movies=movie)
            cur.close()
            flask.flash('Movie rated!', 'success')
            return redirect(url_for('movie/<string:name>'))
        return render_template('movie.html')


@app.errorhandler(404)
def invalid_route(e):
    return render_template("404.html")
