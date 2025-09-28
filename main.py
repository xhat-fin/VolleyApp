from flask import Flask, render_template, session, request, jsonify, redirect, url_for
import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'


@app.route('/', methods=['GET'])
def index():
    if not session.get('username'):
        return redirect(url_for('auth'), code=301)
    try:
        games = db.select()
    except Exception as e:
        print(e)
        games = []
    return render_template('index.html', games=games)


@app.route('/game/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    if not session.get('username'):
        return redirect(url_for('auth'), code=301)
    try:
        game = db.select_game(game_id)
    except Exception as e:
        print(e)
        game = {"massage_error": "Произошла ошибка, попробуйте позже"}
    return render_template('game_detail.html', game=game)


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            password_hash = generate_password_hash(password)
            db.create_players(username, password_hash)
        return redirect(url_for('auth'), code=301)

    return render_template('register.html')


@app.route('/auth/sign-in', methods=['GET', 'POST'])
def auth():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.select_user(username)
        if user and check_password_hash(user.get('password_hash'), password):
            session['username'] = username
            session['datetime_session'] = datetime.now() + timedelta(days=1)
            return redirect(url_for('index'))
    return render_template('auth.html')


@app.route('/create', methods=['GET', 'POST'])
def create_game():
    if not session.get('username'):
        return redirect(url_for('auth'), code=301)
    if request.method == 'POST':
        title_game = request.form.get('title_game')
        description = request.form.get('description')
        need_players = request.form.get('need_players')
        db.insert_game(title_game=title_game, description=description, need_players=need_players)
        return redirect(url_for('index'))
    return render_template('CreateGame.html')


@app.route('/update/<int:game_id>', methods=['GET', 'POST'])
def update_game(game_id):
    if not session.get('username'):
        return redirect(url_for('auth'), code=301)
    if request.method == 'POST':
        new_title_game = request.form.get('new_title_game')
        new_description = request.form.get('new_description')
        new_need_players = request.form.get('new_need_players')
        db.update_game(game_id, new_title_game, new_description, new_need_players)
        return redirect(url_for('get_game_by_id', game_id=game_id))
    game = db.select_game(game_id)
    return render_template('UpdateGame.html', game=game)

@app.route('/exit', methods=['GET'])
def exit_app():
    session.clear()
    return redirect(url_for('auth'))



if __name__ == '__main__':
    db.init_db(db.Base)
    app.run(port=8000, debug=True)
