from miniish.kernel import console

class Process:
    def __init__(self, name: str) -> None:
        self.name = name
        self.pid = 0
        self.args = []
        self.status = 'r'
        
    def spawn(self, args: list[str] = []) -> None:
        self.args = args if len(args) > 0 else [self.name]
        self.init(args)
        
    def init(self, args: list[str] = []) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        console.render()
        
    def load(self, path: str) -> bool:
        return False

    def save(self, path: str | None = None) -> bool:
        return False

