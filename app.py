from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

#  initial setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]
debug = DebugToolbarExtension(app)

boggle_game = Boggle()
words = set(boggle_game.words)

@app.route('/')
def start():
    """ Render an initial page. """
    return render_template('index.html')

# Generate a board on the backend using a function from the boggle.py file and send that to Jinja template.
@app.route('/board')
def show_board():
    """ Render a page that displays the board. """
    board = boggle_game.make_board()
    session['board'] = board
    print(session['board'])
    highest = session.get("highest", 0)
    totalgames = session.get("totalgames", 0)
    return render_template('board.html', board=board, highest=highest, totalgames=totalgames)

# Take the form value and check if it is a valid word in the dictionary using the words variable
# Make sure that the word is valid on the board using the check_valid_word function
@app.route("/board/check")
def check_word():
    """ Check for valid word in the board with Boggle method. """

    word = request.args["word"] # get word from form
    board = session["board"] # get board from saved session
    response = boggle_game.check_valid_word(board, word)

    # Since AJAX request was made to server, respond with JSON using the jsonify function from Flask
    return jsonify({'result': response})


@app.route("/board/score", methods=["POST"])
def show_score():
    """Receive score, update number of games, update high score if appropriate."""

    score = request.json["score"]
    highest = session.get("highest", 0)
    totalgames = session.get("totalgames", 0)

    session['totalgames'] = totalgames + 1
    session['highest'] = max(score, highest)

    print(highest)
    return jsonify(brokeRecord = score > highest)

