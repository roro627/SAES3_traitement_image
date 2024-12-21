from astropy.io import fits
import matplotlib.pyplot as plt

# C h a r g e r l e f i c h i e r FITS
data = fits.getdata(r'downloads\jw01558-o005_t001_nircam_clear-f212n_i2d.fits')
# A f f i c h e r l ’ i m a g e
plt.imshow(data, cmap='gray')
plt.colorbar()
plt.show()