import random

DEFAULT_DICT = {}
POINTS_FOR_WIN = 1
POINTS_FOR_TIE = 0
POINTS_FOR_LOSS = -1
POINTS_FOR_POSSIBLE = 0
TRAINING_ROUNDS = 100000

# The following class TicTacToe is standard and widely available
# on the Internet with unknown source and attribution.
class TicTacToe:

    def __init__(self):
      self.board = []
    
    def create_board(self):
      self.board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                    
    def random_first_player(self):
      return random.randint(0, 1)
      
    def player_spot_available_ifso_take(self, spot, player):
      if self.board[int(spot)] == "X" or self.board[int(spot)] == "O":
        return False
      else:
        self.board[int(spot)] = player
        return True
    def has_player_won(self, player):
      board = self.board
      # First checking horizontal wins
      if board[0] == player and board[1] == player and board[2] == player:
        return True
      elif board[3] == player and board[4] == player and board[5] == player:
        return True
      elif board[6] == player and board[7] == player and board[8] == player:
        return True
      # Checking vertical wins
      elif board[0] == player and board[3] == player and board[6] == player:
        return True
      elif board[1] == player and board[4] == player and board[7] == player:
        return True
      elif board[2] == player and board[5] == player and board[8] == player:
        return True
      # Checking diagonal wins
      elif board[0] == player and board[4] == player and board[8] == player:
        return True
      elif board[2] == player and board[4] == player and board[6] == player:
        return True
      else:
        return False
    
    def is_tie(self):
      for i in range(len(self.board)):
        if self.board[i] != "O" and self.board[i] != "X":
          return False
      return True

    def is_game_over(self):
        if self.is_tie() or self.has_player_won('X') or self.has_player_won('O'):
            return True
        return False
    
    def switch_turn(self, player):
      return 'X' if player == 'O' else 'O'
    
    def show_board(self):
      board = []
      for i in self.board:
        board.append(str(i))
      viewing_row1 = board[:3]
      viewing_row2 = board[3:6]
      viewing_row3 = board[6:]
      row1 = ' '.join(viewing_row1)
      row2 = ' '.join(viewing_row2)
      row3 = ' '.join(viewing_row3)
      print(row1)
      print(row2)
      print(row3)
    
    def start(self):
      self.create_board()
      player = 'X' if self.random_first_player() == 1 else 'O'
      while self.is_tie() == False:
        print("Player", player, "Turn")
        self.show_board()
        while True:
          try:
            spot = int(input("Enter number to go to that spot: "))
            possible = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            assert spot in possible
            self.player_spot_available_ifso_take(spot, player)
            break
          except:
            continue
        if self.has_player_won(player):
          print("Player", player, "Won")
          self.show_board()
          return
        player = self.switch_turn(player)
      if self.has_player_won(player):
        print("Player", player, "Won")
        self.show_board()
        return
      else:
        print("Match drawn.")
        self.show_board()

class AIGameHuman(TicTacToe):
    def __init__(self):
      self.board = []
    def start(self, **kwargs):
      dictionary = kwargs.get("dictionary", {})
      state_list = []
      action_list = []
      possible_actions_list = []
      self.create_board()
      ai_player = 'X' if self.random_first_player() == 1 else 'O'
      human_player = 'O' if ai_player == 'X' else 'X'
      print("You are ", human_player)
      print("The AI is ", ai_player)
      whose_turn = ai_player if ai_player == "X" else human_player
      self.show_board()
      while self.is_tie() == False:
        print("Player ", whose_turn, "Turn")
        if whose_turn == human_player:
          spot = int(input("Enter number: "))
          self.player_spot_available_ifso_take(spot, human_player)
          self.show_board()
        if self.is_tie() == True:
          print("Match drawn.")
          break
        elif whose_turn == ai_player:
          state = tuple(self.board) # Testing
          state_list.append(state)
          action = self.ai_choice(dictionary, state)
          action_list.append(action)
          possible_actions = self.get_possible(state)
          possible_actions_list.append(tuple(possible_actions))
          self.player_spot_available_ifso_take(action, ai_player)
          self.show_board()
        if self.is_tie() == True:
          print("Match drawn.")
          break
        if self.has_player_won(ai_player):
          print("AI Player Won.")
          self.show_board() # Add result append to dictionary here
          for some_index in range(len(state_list)):
            self.append_dictionary(dictionary, state_list[some_index], action_list[some_index], POINTS_FOR_WIN)
            for other_index in range(len(possible_actions_list[some_index])):
              self.append_dictionary(dictionary, state_list[some_index], possible_actions_list[some_index][other_index], POINTS_FOR_POSSIBLE)
          return dictionary
        elif self.has_player_won(human_player):
          print("Human Player Won.")
          self.show_board() # Add result append to dictionary here
          for some_index in range(len(state_list)):
            self.append_dictionary(dictionary, state_list[some_index], action_list[some_index], POINTS_FOR_LOSS)
            for other_index in range(len(possible_actions_list[some_index])):
              self.append_dictionary(dictionary, state_list[some_index], possible_actions_list[some_index][other_index], POINTS_FOR_POSSIBLE)
          return dictionary
        whose_turn = self.switch_turn(whose_turn)
      else:
        print("Match drawn.")
    def append_dictionary(self, dictionary, state, action, result):
      """ Appends to a dictionary of format { state : { action : result (that occurred) }} """
      if dictionary.get(state) == None:
        dictionary[state] = {}
        dictionary[state].update({ action : result})
        return
      else:
        if dictionary[state].get(action) == None:
          dictionary[state].update({ action : result })
          return
        else:
          the = dictionary[state].get(action)
          result += the
          dictionary[state].update({ action : result})
          return
    def ai_choice(self, dictionary, state):
      possible = self.get_possible(state)
      if state in dictionary:
        detail_dict = dictionary[state]
        key_list = list(detail_dict.keys())
        val_list = list(detail_dict.values())
        maximum = max(val_list)
        max_index = val_list.index(maximum)
        action = key_list[max_index]
        return action
      else:
        action = random.choice(possible)
        return action
    def get_possible(self, state):
      possible = []
      for i in state:
        if i != "X" and i != "O":
          possible.append(i)
      return possible

class AIGame(AIGameHuman):
    def __init__(self):
      self.board = []
      self.ai_player = 'X' if self.random_first_player() == 1 else 'O'
      self.other_ai_player = 'O' if self.ai_player == 'X' else 'X'
    def start(self, **kwargs):
        dictionary = kwargs.get("dictionary", DEFAULT_DICT)
        state_list = []
        action_list = []
        possible_actions_list = []
        self.create_board()
        ai_player = self.ai_player
        other_ai_player = self.other_ai_player
        whose_turn = ai_player if ai_player == "X" else other_ai_player
        while True:
            if self.is_game_over() == True:
                break;
            if whose_turn == other_ai_player:
                state = tuple(self.board)
                state_list.append(state)
                action = self.ai_choice(dictionary, state, other_ai_player)
                action_list.append(action)
                possible_actions = self.get_possible(state)
                possible_actions_list.append(tuple(possible_actions))
                self.player_spot_available_ifso_take(action, other_ai_player)
            if self.is_game_over() == True:
                break
            if whose_turn == ai_player:
                state = tuple(self.board)
                state_list.append(state)
                action = self.ai_choice(dictionary, state, ai_player)
                action_list.append(action)
                possible_actions = self.get_possible(state)
                possible_actions_list.append(tuple(possible_actions))
                self.player_spot_available_ifso_take(action, ai_player)
            whose_turn = self.switch_turn(whose_turn)
        if self.has_player_won(ai_player):
            for some_index in range(len(state_list)):
                self.append_dictionary(dictionary, state_list[some_index], action_list[some_index], POINTS_FOR_WIN)
                for other_index in range(len(possible_actions_list[some_index])):
                    self.append_dictionary(dictionary, state_list[some_index], possible_actions_list[some_index][other_index], POINTS_FOR_POSSIBLE)
            return dictionary
        elif self.has_player_won(other_ai_player):
            for some_index in range(len(state_list)):
                self.append_dictionary(dictionary, state_list[some_index], action_list[some_index], POINTS_FOR_LOSS)
                for other_index in range(len(possible_actions_list[some_index])):
                    self.append_dictionary(dictionary, state_list[some_index], possible_actions_list[some_index][other_index], POINTS_FOR_POSSIBLE)
            return dictionary
        elif self.is_tie() == True:
            for some_index in range(len(state_list)):
                self.append_dictionary(dictionary, state_list[some_index], action_list[some_index], POINTS_FOR_TIE)
                for other_index in range(len(possible_actions_list[some_index])):
                    self.append_dictionary(dictionary, state_list[some_index], possible_actions_list[some_index][other_index], POINTS_FOR_POSSIBLE)
            return dictionary
    def ai_choice(self, dictionary, state, player):
      possible = self.get_possible(state)
      if state in dictionary and player == self.ai_player:
        detail_dict = dictionary[state]
        key_list = list(detail_dict.keys())
        val_list = list(detail_dict.values())
        choice_list = []
        for i in range(len(val_list)):
          it = val_list[i]
          has = key_list[i]
          choice = [has] * it
          choice_list.append(choice)
        the = random.choice(choice_list)
        if len(the) != 0:
            action = the[0]
        else:
            action = random.choice(possible)
        return action
      elif state in dictionary and player == self.other_ai_player:
        action = random.choice(possible)
        return action
      else:
        action = random.choice(possible)
        return action


def train(times):
  game = AIGame()
  the = game.start()
  for i in range(times):
    the = game.start(dictionary = the) 
  return the

model = train(TRAINING_ROUNDS)
game = AIGameHuman()
it = game.start(dictionary = model)
