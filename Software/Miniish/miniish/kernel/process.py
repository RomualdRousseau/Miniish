from miniish.kernel import console


class Process:
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
