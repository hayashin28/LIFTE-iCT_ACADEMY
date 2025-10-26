import geocoder

# Get current location
def getCurrentLocation():
    g = geocoder.ip('me')
    return g.latlng


location = getCurrentLocation()
print(f"Current location: {location}")