class NotAPokemonException(Exception):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} is not a valid pokemon"


class NotAValidIndexException(Exception):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def __str__(self) -> str:
        return f"There is no valid pokemon with id {self.id}"


class NotAPokemonType(Exception):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} is not a valid pokemon type"
