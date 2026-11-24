from utils.normalize import normalize, save_normalized_spectrum

star_id = "hen3-938"
product_id = "ADP.2024-02-29T08:05:55.704"
corrected_path = f"data/processed/{star_id}/{product_id}_corrected.fits"

spectrum = normalize(corrected_path)
save_normalized_spectrum(spectrum, star_id, product_id, corrected_path)