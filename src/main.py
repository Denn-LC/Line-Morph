import matplotlib.pyplot as plt

from utils.normalize import normalize, plot_normalization

spectrum = normalize(
    "data/processed/reflex/hen3-938/NIR/reflex_end_products/"
    "molecfit/XSHOOTER/2026-11-12T16:52:25/"
    "ADP.2024-02-29T08:05:55.704/Hen_3-938_SCIENCE_TELLURIC_CORR.fits"
)

fig = plot_normalization(spectrum, title="Hen 3-938 · He I 1083 nm")
fig.savefig("figures/hei_1083_normalized.png")
plt.show()