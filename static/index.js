'use strict';

class BoggleGame {
    constructor(secs = 60) {
        this.words = new Set();
        this.score = 0;

        this.secs = secs
        this.showTimer();

        /* every 1000 msec, "tick" */
        this.timer = setInterval(this.tick.bind(this), 1000);
    }

    /* Update message in DOM */
    displayMsg(msg) {
        $('#messages').text(msg);
        console.log(msg)
    }

    /* show word in list of words */
    showWord(word) {
        $(".words").append($('<li>', { text: word }));
    }

    /* Update timer in DOM */
    showTimer() {
        $("#countdown").text(this.secs);
    }

    /* Tick: Handle a second passing in game and freeze form when timer reaches 0 seconds */
    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            document.getElementById("word").disabled = true;
            document.getElementById("word-button").disabled = true;
            await this.scoreGame
        }
    }

    async scoreGame() {
        const resp = await axios.post("/board/score", { score: this.score });
        if (resp.data.brokeRecord) {
          this.displayMsg(`New record: ${this.score}`);
        } else {
          this.displayMsg(`Final score: ${this.score}`);
        }
    }

    /* When the user submits the form, send the guess to your server. The page should not refresh when the user submits the form. */
    async checkWord(event) {
        event.preventDefault();
        /* Using jQuery, take the form value and using axios, make an AJAX request to send it to the server. */ 
        const word = $("input#word").val().toLowerCase();
        const resp = await axios.get(`${window.origin}/board/check`, { params: { word } } );
        console.log(resp)

        if (resp.data.result === "ok") {
            if (this.words.has(word)){
                this.displayMsg("Word already entered");
                console.log('this words has word already')

            } else {
                /* Score for word = length. If a valid word is guessed, add its score to the total and display the current score as it changes. */
                this.words.add(word);
                this.score += word.length;
                $('#total').text(`${this.score}`);
                this.showWord(word);
                this.displayMsg("You got it!");
                console.log('this word added to words')
            }

        } else if (resp.data.result === "not-on-board") {
            this.displayMsg("Sorry, word not on board");
            console.log('resp.data.result not on board')

        } else {
            this.displayMsg("Hmm, word not recognized");
            console.log('resp.data.result not a word')
        }
        $('input#word').val('');
    }
};

/* instantiate boggle game class */
const boggleGame = new BoggleGame();

/* Event listener for user submitting word form */
$('#word-submit-form').on('submit', async function(event){
    await boggleGame.checkWord(event);
    console.log('form submitted')
});
