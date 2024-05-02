class GameStats:
    #tracks stats

    def __init__(self,ai_game):
        #initialize the stats
        self.settings = ai_game.settings
        self.reset_stats()
        self.aliens_killed = 0
        self.level = 1
        

        #start game in active state
        self.game_active = True

    def reset_stats(self):
        #initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit