from astropy.io import fits
import matplotlib.pyplot as plt
# C h a r g e r l e f i c h i e r FITS
data = fits.getdata('Tarantula\Tarantula_Nebula-halpha.fit')
# A f f i c h e r l ’ i m a g e
plt.imshow(data, cmap='gray')
plt.colorbar()
plt.show()