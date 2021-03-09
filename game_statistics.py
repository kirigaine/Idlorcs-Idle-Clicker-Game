class GameStats():
    def __init__(self):
        # Currency counts
        self.rock_count = 0
        self.wood_count = 0
        self.gold_count = 0
        self.food_count = 0
        
        # Unit counts
        self.rockminer_count = 0
        self.lumberjack_count = 0
        self.farmer_count = 0
        self.goldminer_count = 0

        # Poulation counts
        self.population_current = 0
        self.population_limit = 10

        # Gameplay statistics
        self.total_clicks = 0

    def can_buy_unit(self):
        """Returns whether or not purchase of an additional unit would surpass population limit"""
        if self.get_current_population() < self.population_limit:
            return True
        return False

    def get_current_population(self):
        """Returns the summation of all units"""
        total_population = 0
        total_population += self.rockminer_count
        total_population += self.lumberjack_count
        total_population += self.farmer_count
        total_population += self.goldminer_count
        return total_population