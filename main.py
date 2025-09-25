from flask import Flask, render_template, session, request, jsonify
import db

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/', methods=['GET'])
def index():
    games = db.select()
    return render_template('index.html', games=games)


@app.route('/game/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    game = db.select_game(game_id)
    return render_template('game_detail.html', game=game)


@app.route('/auth/sign-in', methods=['POST'])
def auth():
    if request.method == "POST":
        info = request.get_json()
        session['username'] = info.get('username')
    return jsonify({"username_session": session.get('username')})


if __name__ == '__main__':
    db.init_db(db.Base)
    app.run(port=8000, debug=True)
