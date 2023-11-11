from miniish.kernel import console


class Process:
    def __init__(self, name: str) -> None:
        self.name = name
        
    def init(self, args: list[str] = []) -> None:
        self.args = args
        pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        console.render()
        
    def load(self, path: str) -> bool:
        return False

    def save(self, path: str | None = None) -> bool:
        return False
    
    def __str__(self) -> str:
        return self.name
