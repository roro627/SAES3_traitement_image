from astropy.io import fits
import matplotlib.pyplot as plt

# C h a r g e r l e f i c h i e r FITS
data = fits.getdata(r'downloads\hst_08726_03_wfpc2_total_wf_drz.fits')
# A f f i c h e r l ’ i m a g e
plt.imshow(data, cmap='gray')
plt.colorbar()
plt.show()