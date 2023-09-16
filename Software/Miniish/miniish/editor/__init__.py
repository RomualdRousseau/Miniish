import pyco
import pyco.sys

from miniish.kernel.process import Process
from miniish.kernel.scheduler import pause
from miniish.constants import COLOR_STAT_BG, COLOR_MAIN_BG
from miniish.editor.widgets.component import Component
from miniish.editor.widgets.widgets import Button, ButtonGroup
from miniish.editor.code import CodeEditor
from miniish.editor.map import MapEditor
from miniish.editor.music import MusicEditor
from miniish.editor.sound import SoundEditor
from miniish.editor.sprite import SpriteEditor

TABS: list[Component] = [
    CodeEditor(),
    SpriteEditor(),
    MapEditor(),
    SoundEditor(),
    MusicEditor(),
]


class Editor(Process):
    """The Editor."""

    def __init__(self) -> None:
        self.tabs = ButtonGroup(
            -1,
            (128 - len(TABS) * 8, 0),
            [
                Button(i, (0, 0), (i * 2, i * 2 + 1), self._switch_app)
                for i in range(len(TABS))
            ],
            False,
            [0],
        )
        self.tab_curr = TABS[0]
        self.initialized = False

    def init(self, args: list[str] = []) -> None:
        if self.initialized:
            return
        for tab in TABS:
            tab.init_ui()
        self.initialized = True

    def update(self) -> None:
        self.tabs.update()
        if not self.tab_curr.update():
            pause()

    def draw(self) -> None:
        pyco.rectfill((0, 0, 128, 8), COLOR_STAT_BG)
        pyco.rectfill((0, 8, 128, 113), COLOR_MAIN_BG)
        pyco.rectfill((0, 121, 128, 7), COLOR_STAT_BG)
        self.tabs.draw()
        self.tab_curr.draw()

    def load(self, path: str | None = None) -> bool:
        self.init()
        for tab in TABS:
            tab.load()
        return True

    def save(self, path: str | None = None) -> None:
        for tab in TABS:
            tab.save()

    def _switch_app(self, button: Button) -> None:
        self.tab_curr = TABS[button.id]
        pyco.flush()
