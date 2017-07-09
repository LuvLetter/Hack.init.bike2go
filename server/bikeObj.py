#objects
class bike(object):
    def __init__(self,SSID,lng,lat):
        self.bikeId = (SSID//10000)
        self.encrypted = (SSID%10000)
        self.lng = lng
        self.lat = lat

    def __eq__(self,other):
        if(isinstance(self,bike)and isinstance(other,bike)):
            return self.bikeId == other.bikeId and self.encrypted==other.encrypted
        return False

    def __repr__(self):
        return self.bikeId
