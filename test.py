from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_homepage_start(self):
        """Test homepage loads"""

        with self.client:
            response = client.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="lead">Instructions:</p>', html)
            # need to test redirect
            
    def test_board(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/board')
            self.assertIn('board', session)
            self.assertIn(b'<p>Highest Score:</p>', response.data)
            self.assertIn(b'<p>Current Score:</p>', response.data)

    def test_check_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/board/check?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_word_not_found(self):
        """Test if real word is in board."""

        self.client.get('/board')
        response = self.client.get('/board/check?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_word(self):
        """Test word that is not real on the board."""

        self.client.get('/board')
        response = self.client.get(
            '/board/check?word=nnoottaawwoorrdd')
        self.assertEqual(response.json['result'], 'not-word')
    
    def test_show_score(self):
        """Test final score, highest score, and number of games being updated"""

        # self.client.get('/board/score')
        # response = self.client.get('/board/score')


