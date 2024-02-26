from flask import Flask, render_template, request

app = Flask(__name__)

class Game:
    def __init__(self, no_players):
        self.no_players = no_players
        self.elements = {
            "Machali": 1,
            "Pani Main": 2,
            "Chapak": 3
        }
        self.stack = []
        self.turn = 1
        self.score = 0

    def set_elements(self, turn=1):
        for j in self.elements.keys():
            for _ in range(1, turn + 1):
                self.stack.append(j)

    def get_elements(self, turn=1):
        return self.stack

    def set_board(self):
        self.set_elements(self.turn)
        while True:
            for i in range(1, self.no_players + 1):
                choice = request.form.get(f"player_{i}_choice")
                element = self.stack.pop(0)
                if element != choice:
                    return self.kill_game(i)
                if not self.stack:
                    self.turn += 1
                    self.set_elements(self.turn)
            self.score += 1

    def kill_game(self, loser_number):
        return f"Game ender loser is {loser_number}, score is {self.score}"

    def show_queue(self):
        return self.stack

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        # Get the number of players from the form
        no_players = int(request.form.get('no_players'))
        # Create an instance of the game with the user-provided number of players
        game_instance = Game(no_players=no_players)
        # Execute the game logic based on the form submission
        result = game_instance.set_board()
        return render_template('result.html', result=result)

    # Display the form to input the number of players
    return render_template('play.html')

if __name__ == '__main__':
    app.run(debug=True)

