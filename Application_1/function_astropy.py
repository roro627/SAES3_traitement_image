from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, img_as_float, img_as_ubyte

def apply_color_filter(image, r_scale=30, g_scale=30, b_scale=30):
    red = image * r_scale
    green = image * g_scale
    blue = image * b_scale

    rgb_image = np.stack([red, green, blue], axis=-1)
    
    rgb_image = np.clip(rgb_image, 0, 1)

    return rgb_image

def main() -> None:

    # Test

    with fits.open('Tarantula\Tarantula_Nebula-halpha.fit') as hdul:
        header = hdul[0].header

        print(repr(header))

        image_data = hdul[0].data

        print(image_data)

        image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))
        rgb_image = apply_color_filter(image_data)

        plt.imshow(image_data, cmap='grey')
        plt.colorbar()
        plt.show()

    return 

if __name__ == "__main__":
    main()






    