import sys

import miniish.pyco.sys as psys
import miniish.sketch as sketch


def _main():
    psys.set_callbacks(
            sketch._init, 
            sketch._update, 
            sketch._draw
            )
    psys.run()


if __name__ == "__main__":
    sys.exit(_main())
