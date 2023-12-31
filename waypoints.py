class Campsite:
    def __init__(
        self, 
        name, 
        address, 
        city, 
        state, 
        zip, 
        latitude,
        longitude,
        phone,
        website,
        amenities,
        notes
    ):
        self.name  = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.latitude = latitude
        self.longitude = longitude
        self.phone = phone
        self.website = website
        self.amenities = amenities
        self.notes = notes