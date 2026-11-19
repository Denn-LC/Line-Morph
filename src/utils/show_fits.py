from pathlib import Path

import matplotlib.pyplot as plt
from astropy.visualization import ZScaleInterval
from ccdproc import CCDData

# func to show fits, path required, title optional cmap below
# Ha (H-alpha) : Reds_r
# R (Red) : Reds_r
# B (Blue) : Blues_r
# V (Visual) : Greens_r
# Any filter : Gray (default)
def show_fits(path, title = None, cmap = "gray"):
    path = Path(path)
    image = CCDData.read(path, unit = "adu")
    low, high = ZScaleInterval().get_limits(image.data)

    fig, ax = plt.subplots()
    pixels = ax.imshow(
        image.data, cmap = cmap, origin = "lower", vmin = low, vmax = high
    )
    ax.set_title(title or path.stem)
    fig.colorbar(pixels, ax=ax, label="ADU")
    plt.show()