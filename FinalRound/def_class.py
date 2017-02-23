class Video:
    def __init__(self, id, taille):
        self.id = id
        self.taille = taille
        self.serveurs = []


    def __str__(self):
        chaine="*** Video {}".format(self.id)
        chaine+="\n serveur : "
        chaine+=", ".join(serveur.id for serveur in self.serveurs)
        return chaine

class CacheServeur:
    def __init__(self, id):
        self.videos = []
        self.id = id

    def __str__(self):
        chaine = "*** CacheServeur {}".format(self.id)
        chaine += "\n videos : "
        chaine += ", ".join(video.id for video in self.videos)
        return chaine

    def free_size(self, max_cap):
        taille=max_cap
        for v in self.videos:
            taille-=v.taille
        return taille


class EndPoint:
    def __init__(self, id, lat_dataServer, dico):
        self.lat_Server = lat_dataServer
        self.cacheServeur = dico
        self.id = id

    def __str__(self):
        chaine = "*** End point {}".format(self.id)
        chaine += "\n latente : {}".format(self.lat_Server)
        chaine += "\n dict cache serveur / latence: "
        print self.cacheServeur
        for cache_s in self.cacheServeur :
            chaine += 'serv '+str(cache_s.id)+' lat '+str(self.cacheServeur[cache_s])+', '
        chaine += "\n"
        return chaine


class Request:
    def __init__(self, id, video, endPoint, nombre):
        self.nb = nombre
        self.endPoint = endPoint
        self.id = id
        self.video = video

    def __str__(self):
        chaine = "*** Request {}".format(self.id)
        chaine+="\n endpoint :" +str(self.endPoint.id)
        chaine += "\n video :" + str(self.video.id)
        chaine += "\n nb :" + str(self.nb)
        return chaine

    @property
    def size(self):
        return self.nombre*self.video.taille

class Probleme:
    def __init__(self, max_cap, cache_serveur, resquest, video, endpoints):
        self.max_cap=max_cap
        self.cache_servers=cache_serveur
        self.requests=resquest
        self.videos=video
        self.endpoints=endpoints

    def __str__(self):
        s = " **** PROBLEM \n"
        s += "MAX_CAP = "+str(self.max_cap)+"\n"
        s += "Serveurs" +"\n".join(str(s) for s in self.cache_servers)+"\n"
        s += "Requests" +"\n".join(str(s) for s in self.requests)+"\n"
        s += "Videos" +"\n".join(str(s) for s in self.videos)+"\n"
        s += "Endpoints" +"\n".join(str(s) for s in self.endpoints)+"\n"
        return s