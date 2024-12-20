from random import randrange

class Game:
    def __init__(self, player_1_name: str, player_2_name: str):
        self.players = []
        self.add_player(player_1_name)
        self.add_player(player_2_name)
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6
        
        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []
        
        self.current_player_index = 0
        self.is_getting_out_of_penalty_box = False
        
        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append(self.create_rock_question(i))
    
    def create_rock_question(self, index):
        return "Rock Question %s" % index
    
    def is_playable(self):
        return self.how_many_players >= 2
    
    def add_player(self, player_name):
        if len(self.players) >= 6:
            print("Too many players")
            return False

        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False
        
        print(f"{player_name} was added")
        print(f"It's player number {len(self.players)}")
        return True
    
    @property
    def how_many_players(self):
        return len(self.players)
    
    def roll(self, roll):
        current_player = self.players[self.current_player_index]
        print(f"{current_player} has rolled {roll}")
        
        if self.in_penalty_box[self.current_player_index]:
            if roll % 2 == 0:
                print(f"{current_player} is not getting out of the penalty box")
                return
            else:
                self.in_penalty_box[self.current_player_index] = False
            
        print(f"{self.players[self.current_player_index]} is getting out of the penalty box")
        self.places[self.current_player_index] = self.places[self.current_player_index] + roll
        if self.places[self.current_player_index] > 11:
            self.places[self.current_player_index] = self.places[self.current_player_index] - 12
        
        print(f"{self.players[self.current_player_index]} 's new location is {self.places[self.current_player_index]}")
        print(f"The category is {self._current_category}")
        self._ask_question()
    
    def _ask_question(self):
        if self._current_category == 'Pop':
            print(self.pop_questions.pop(0))
        if self._current_category == 'Science':
            print(self.science_questions.pop(0))
        if self._current_category == 'Sports':
            print(self.sports_questions.pop(0))
        if self._current_category == 'Rock':
            print(self.rock_questions.pop(0))
    
    @property
    def _current_category(self):
        places = ["Pop", "Science", "Sports", "Rock"]
        current_place_index = self.places[self.current_player_index] % len(places)
        return places[current_place_index]

    def was_correctly_answered(self):
        winner = True
        if not self.in_penalty_box[self.current_player_index]:
            print("Answer was correct!!!!")
            self.purses[self.current_player_index] += 1
            print(f"{self.players[self.current_player_index]} now has {self.purses[self.current_player_index]} Gold Coins.")
            winner = self._did_player_win()

        self.current_player_index += 1
        if self.current_player_index == len(self.players):
            self.current_player_index = 0
        
        return winner
    
    def wrong_answer(self):
        print("Question was incorrectly answered")
        print(f"{self.players[self.current_player_index]} was sent to the penalty box")
        self.in_penalty_box[self.current_player_index] = True
        
        self.current_player_index += 1
        if self.current_player_index == len(self.players):
            self.current_player_index = 0
        return True
    
    def _did_player_win(self):
        return not (self.purses[self.current_player_index] == 6)



if __name__ == '__main__':
    not_a_winner = False
    game = Game("Chet", "Pat")
    game.add_player('Sue')

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()
        
        if not not_a_winner:
            break
