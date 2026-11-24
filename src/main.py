import matplotlib.pyplot as plt

from utils.normalize import normalize, plot_normalization

spectrum = normalize(
    "data/processed/hen3-938/ADP.2024-02-29T08:05:55.704_corrected.fits"
)

fig = plot_normalization(spectrum, title="Hen 3-938 · He I 1083 nm")
fig.savefig("figures/hei_1083_normalized.png")
plt.show()