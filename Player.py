class Player:
    def __init__(self, rfid, name, wins, defeats, draws):
        self.rfid = rfid
        self.name = name
        self.wins = wins
        self.defeats = defeats
        self.draws = draws

    def __str__(self) -> str:
        return f'RFID: {self.rfid}\n' \
               f'Name: {self.name}\n' \
               f'Wins: {self.wins}\n' \
               f'Defeats: {self.defeats}\n' \
               f'Draws: {self.draws}\n'
