class Video:
    def __init__(self, taille):
        self.taille = taille
        self.serveurs=[]

class CacheServeur:
    def __init__(self, id):
        self.videos=[]
        self.id=id

class EndPoint:
    def __init__(self, id, lat_dataServer, dico):
        self.lat_Server=lat_dataServer
        self.cacheServeur=dico
        self.id=id

class Request:
    def __init__(self, id, idEndPoint, nombre):
        self.nb=nombre
        self.idEndPoint=idEndPoint
        self.id=id

