#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
from cycler import cycler

def readIntensity(photoName, plotName, lamp, surface):
    """
        photoName: image name of data to process
        plotName: image name of where to save data to
        lamp: lamp type (showed on the resulting graph)
        surface: surface color (showed on the resulting graph)
        RETURNS
        np.ndarray
    """
    photo = iio.imread(photoName)
    background = photo[425:825, 800:1100, 0:3].swapaxes(0, 1)  # Cut the pic and 90def clockwise rotation.
    
    cut = photo[425:825, 800:1100, 0:3].swapaxes(0, 1)

    # HANDLE INCORRECT IMAGES:
    # If rgb of pixel is less than (15, 15, 15), then rgb = (0, 0, 0)
    with np.nditer(cut, op_flags=['readwrite']) as it:
      for x in it:
        if x < 25:
          x[...] = 0

    rgb = np.mean(cut, axis=(0))

    luma = 0.2989 * rgb[:, 0] + 0.5866 * rgb[:, 1] + 0.1144 * rgb[:, 2]

    # Set rc 'axes' to prop_cycle, now the property 'color' will cycle through 'r', 'g', 'b'
    plt.rc('axes', prop_cycle=( cycler('color', ['r', 'g', 'b']) ) )

    fig, ax = plt.subplots(figsize=(10, 5), dpi=200)

    ax.set_title(f'Интенсивность отражённого излучения\n {lamp} / {surface}')
    ax.set_xlabel('Относительный номер пикселя')
    ax.set_ylabel('Яркость')

    ax.grid('--')
    ax.plot(rgb, label=['r', 'g', 'b'])
    ax.plot(luma, 'w', label='I')
    ax.legend()
    
    ax.imshow(background, origin='lower')
    
    plt.savefig(plotName)

    return luma
