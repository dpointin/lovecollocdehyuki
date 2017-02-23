class Video:
    def __init__(self, id, taille):
        self.id = id
        self.taille = taille
        self.serveurs = []


    def __str__(self):
        chaine="video {}".format(id)
        return chaine

class CacheServeur:
    def __init__(self, id):
        self.videos = []
        self.id = id


class EndPoint:
    def __init__(self, id, lat_dataServer, dico):
        self.lat_Server = lat_dataServer
        self.cacheServeur = dico
        self.id = id


class Request:
    def __init__(self, id, Video, endPoint, nombre):
        self.nb = nombre
        self.endPoint = endPoint
        self.id = id
        self.video = video
