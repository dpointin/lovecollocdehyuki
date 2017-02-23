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

        def __str__(self):
            chaine = "CacheServeur {}".format(id)
            return chaine


class EndPoint:
    def __init__(self, id, lat_dataServer, dico):
        self.lat_Server = lat_dataServer
        self.cacheServeur = dico
        self.id = id

    def __str__(self):
        chaine = "End point {}".format(id)
        return chaine


class Request:
    def __init__(self, id, video, endPoint, nombre):
        self.nb = nombre
        self.endPoint = endPoint
        self.id = id
        self.video = video

    def __str__(self):
        chaine = "Request {}".format(id)
        return chaine

class Probleme:
    def __init__(self, max_cap, cache_serveur, resquest, video, endpoints):
        self.max_cap=max_cap
        self.cache_servers=cache_serveur
        self.requests=resquest
        self.videos=video
        self.endpoints=endpoints

    def __str__(self):
        s = "MAX_CAP = "+self.max_cap+"\n"
        s += "Serveurs" +"\n".join(str(s) for s in self.cache_servers)+"\n"
        s += "Requests" +"\n".join(str(s) for s in self.requests)+"\n"
        s += "Videos" +"\n".join(str(s) for s in self.videos)+"\n"
        s += "Endpoints" +"\n".join(str(s) for s in self.endpoints)+"\n"
        return s