from flask import Flask, url_for, request, render_template, jsonify, abort, make_response, redirect, flash
from pymongo import MongoClient
from mongoflask import MongoJSONEncoder, ObjectIdConverter
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from functools import wraps
import json
from config import Config

def create_app():
  app = Flask(__name__)
  app.secret_key = 'fyndMovieTask'
  app.json_encoder = MongoJSONEncoder
  app.url_map.converters['objectid'] = ObjectIdConverter

  client = MongoClient(Config.MONGO_URI)
  db = client.get_database('MoviesList')
  # app.config["MONGODB_SETTINGS"] = {'db': "MoviesList",
  # 'host': "mongodb+srv://mohitkadyan:fyndMohit@cluster0.qwdnpfl.mongodb.net/MoviesList?retryWrites=true&w=majority"}
  # db = MongoEngine(app)
  AllMovies = db.Movies
  # print(AllMovies.count_documents({}))

  login = LoginManager()
  login.init_app(app)
  login.login_view = 'index'

  @login.user_loader
  def load_user(username):
      u = users.find_one({"email": username})
      if not u:
          return None
      return User(username=u['email'], role=u['role'], id=u['_id'])

  class User:
    def __init__(self, id, username, role):
      self._id = id
      self.username = username
      self.role = role

    @staticmethod
    def is_authenticated():
      return True

    @staticmethod
    def is_active():
      return True

    @staticmethod
    def is_anonymous():
      return False
      
    def get_id(self):
        return self.username

  ### custom wrap to determine role access  ### 
  def roles_required(*role_names):
    def decorator(original_route):
      @wraps(original_route)
      def decorated_route(*args, **kwargs):
        if not current_user.is_authenticated:
          print('The user is not authenticated.')
          return redirect(url_for('login'))
        
        print(current_user.role)
        print(role_names)
        if not current_user.role in role_names:
          print('The user does not have this role.')
          return redirect(url_for('login'))
        else:
          print('The user is in this role.')
          return original_route(*args, **kwargs)
      return decorated_route
    return decorator

  @app.route('/login', methods=['GET', 'POST'])
  def login():
    if current_user.is_authenticated:
      return redirect(url_for('home'))

    if request.method == 'POST':
      user = users.find_one({"email": request.form['username']})
      if user and user['password'] == request.form['password']:
        user_obj = User(username=user['email'], role=user['role'], id=user['_id'])
        login_user(user_obj)
        flash("Logged in successfully!", category='success')
        return redirect(url_for('home'))

      flash("Wrong username or password!", category='error')
    return render_template('login.html')

  @app.route('/logout', methods=['GET', 'POST'])
  @login_required
  def logout():
      logout_user()
      flash('You have successfully logged out.', 'success')
      return redirect(url_for('index'))

  # Login Page Route
  @app.route("/")
  def index():
    return render_template("login.html")

  @app.route("/home")
  @login_required
  def home():
    return render_template("home.html")

  # Entry point of our API
  # Returns a list of all movies
  @app.route("/api/movies", methods=["GET"])
  @login_required
  def get_movies():
    movies=list(AllMovies.find())
    return jsonify({'movies': movies})

  # Get movie by id
  @app.route("/api/movies/<objectid:id>", methods=["GET"])
  @login_required
  @roles_required('admin')
  def get_movie(id):
    data = AllMovies.find_one({'_id': id})
    if not data :
      abort(404)
    return jsonify({'movie': data})

  # Add new movie
  @app.route("/api/movies/add", methods=["POST"])
  @login_required
  @roles_required('admin')
  def add_movie():
    movie_details = json.loads(request.form['movie_details'])
    print("hello")
    print(movie_details)
    if not movie_details or not 'name' in movie_details:
      abort(400)
    movie = {
      'name': movie_details['name'],
      'imdb_score': movie_details.get('imdb_score', ''),
      'director': movie_details.get('director', ''),
      'genre': movie_details.get('genre', ''),
      '99popularity': movie_details.get('99popularity', '')
    }
    # movies.append(movie)
    AllMovies.insert_one(movie)
    return jsonify({'movie': movie})

  # Update existing movie
  @app.route('/api/movies/<objectid:id>', methods=['PUT'])
  @login_required
  @roles_required('admin')
  def update_movie(id):
    data = AllMovies.find_one({'_id' : id})
    if not data :
      abort(404)
    if not request.json:
      abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
      abort(400)
    new_updates = request.json
    AllMovies.update_one({'_id': id},{'$set': new_updates})
    return jsonify({'movie': AllMovies.find_one({'_id': id})})

  # Delete movie
  @app.route('/api/movies/<objectid:id>', methods=['DELETE'])
  @login_required
  @roles_required('admin')
  def delete_movie(id):
    data = AllMovies.find_one({'_id': id})
    if not data :
        abort(404)
    AllMovies.delete_one({'_id': id})
    return jsonify({'result': True})

  @app.route('/api/movies/searchMovie',methods=['POST'])
  @login_required
  def search_movie_by_name():
    movie_name_contains = request.form['movie_name']
    print(movie_name_contains)
    searched_movies = list(AllMovies.find({'name': { '$regex' : "(?i){}(?-i)".format(movie_name_contains) }}))
    if not searched_movies:
      abort(404)
    return jsonify({'movies': searched_movies})

  # Handle 404 errors
  @app.errorhandler(404)
  def not_found(error):
    return make_response(jsonify({'error': 'Could not find that movie'}), 404)  

  # Handle 400 errors
  @app.errorhandler(400)
  def bad_request_error(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)  

  users = db.Users
  roles = db.Roles

  def add_role(role_name):
    role_data = {
      'role_name': role_name
    }
    return roles.insert_one(role_data)

  def add_user(first_name, last_name, email, password, role):
    user_data = {
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'password': password,
      'role': role
    }
    return users.insert_one(user_data)

  def initialize_User_Role():
    # add roles
    admin = add_role('admin')
    user = add_role('user')
    # add users
    akash = add_user('Akash', 'Gupta', 'akash@gupta.com', 'abc123', 'user')
    mohit = add_user('Mohit', 'Kadyan', 'mohit@kadyan.com', 'abc456', 'admin')

  return app
# initialize_User_Role()
# if __name__ == '__main__':
#   app.run(debug=True)
  
    