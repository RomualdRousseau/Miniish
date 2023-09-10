from miniish.kernel import console


class Process:
    def init(self, args: list[str] = []) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        console.render()
