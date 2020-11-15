class GameState:

    def __init__(self):
        self.current_player = None
        self.last_player = None
        self.current_card = None
        self.last_card = None
        self.cursor_marker = None
        self.last_life_value_lost = 0
        self.bot_thinking_time = 0