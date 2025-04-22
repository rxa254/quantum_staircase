"""Export helpers using matplotlib."""
import matplotlib.pyplot as plt
import numpy as np

def save_image(arr, outfile, panel_size_m, resolution_mm):
    dpi = 1000 / resolution_mm  # 1 mm per pixel ⇒ 1000 mm per metre
    figsize = (panel_size_m, panel_size_m)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.imshow(arr, extent=[0, panel_size_m, 0, panel_size_m], origin="lower")
    ax.set_axis_off()
    fig.savefig(outfile, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
