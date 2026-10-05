print("1: script started")
import pyvo
print("2: pyvo imported successfully")

ESO_TAP_URL = "https://archive.eso.org/tap_obs"

print("3: Creating TAPService object")
service = pyvo.dal.TAPService(ESO_TAP_URL)
print("4: TAPService object created successfully")
print(service)