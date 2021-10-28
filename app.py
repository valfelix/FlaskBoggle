from flask import Flask, request, render_template, session 
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
debug = DebugToolbarExtension

boggle_game = Boggle()


#  Flask this is where your routing logic should go.

@app.route('/')
def show_board():
    """ Render a page that shows the user the board. """
    return render_template('board.html')