class GameStats():

    def __init__(self):

        # Current amount of currency (Rockaroos?)
        self.rock_currency = 0
        
        # Producers currently owned
        self.snorckyjr_count = 1
        self.hork_count = 0
        self.pork_count = 0
        self.gork_count = 0
        self.snorck_count = 0

        # Producer multipliers
        self.snorckyjr_mult = 1.0
        self.hork_mult = 1.0
        self.pork_mult = 1.0
        self.gork_mult = 1.0
        self.snorck_mult = 1.0

        # Player statistics
        self.manual_clicks = 0
        self.active_time_played = 0
        self.total_time_played = 0
        self.upgrades_bought = 0
