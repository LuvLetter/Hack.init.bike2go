#objects
class bike(object):
    def __init__(self,bikeId,n,e,d,status,lng,lat):
        self.bikeId = bikeId
        self.n = n
        self.e = e
        self.d = d
        self.status = status
        self.lng = lng
        self.lat = lat

    def __eq__(self,other):
        if(isinstance(self,bike)and isinstance(other,bike)):
            return self.bikeId == other.bikeId
        return False

    def __repr__(self):
        return self.bikeId

