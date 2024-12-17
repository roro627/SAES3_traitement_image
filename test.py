def test():
    i = 0
    i = yield i + 1  # Première valeur renvoyée
    i = yield i + 1  # Deuxième valeur renvoyée
    i = yield i + 1  # Troisième valeur renvoyée
    if i is None:
        i = 0
    yield i + 1  # Quatrième valeur renvoyée

gen = test()
print(next(gen))  # Démarre le générateur et renvoie 1
print(gen.send(2))  # Envoie 2 au générateur, i devient 2, renvoie 3 (2 + 1)
print(gen.send(10))  # Envoie 10 au générateur, i devient 10, renvoie 11 (10 + 1)
print(gen.send(None))  # Envoie None, i devient 0, renvoie 1 (0 + 1)





# from astropy.io import fits
# import matplotlib.pyplot as plt
# # C h a r g e r l e f i c h i e r FITS
# data = fits.getdata('Sirius_data.fits')
# # A f f i c h e r l ’ i m a g e
# plt.imshow(data, cmap='gray')
# plt.colorbar()
# plt.show()