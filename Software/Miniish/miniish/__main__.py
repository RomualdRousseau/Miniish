from miniish.terminal import Terminal
from miniish.kernel import scheduler


if __name__ == "__main__":
    scheduler.start(Terminal())
