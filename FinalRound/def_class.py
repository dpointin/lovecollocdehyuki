import random
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Video:
    def __init__(self, id, taille):
        self.id = id
        self.taille = taille
        self.serveurs = []
        self.requests = []

    def __str__(self):
        chaine = "*** Video {}".format(self.id)
        chaine += "\n serveur : "
        chaine += ", ".join(serveur.id for serveur in self.serveurs)
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
        taille = max_cap
        for v in self.videos:
            taille -= v.taille
        return taille


class EndPoint:
    def __init__(self, id, lat_dataServer, dico):
        self.lat_Server = lat_dataServer
        self.cacheServeurs = dico
        self.id = id

    def __str__(self):
        chaine = "*** End point {}".format(self.id)
        chaine += "\n latente : {}".format(self.lat_Server)
        chaine += "\n dict cache serveur / latence: "
        print self.cacheServeurs
        for cache_s in self.cacheServeurs:
            chaine += 'serv ' + str(cache_s.id) + ' lat ' + str(self.cacheServeurs[cache_s]) + ', '
        chaine += "\n"
        return chaine


class Request:
    def __init__(self, id, video, endPoint, nombre):
        self.nb = nombre
        self.endPoint = endPoint
        self.id = id
        self.video = video
        self.distanceActuelle = endPoint.lat_Server

    def __str__(self):
        chaine = "*** Request {}".format(self.id)
        chaine += "\n endpoint :" + str(self.endPoint.id)
        chaine += "\n video :" + str(self.video.id)
        chaine += "\n nb :" + str(self.nb)
        return chaine

    @property
    def size(self):
        return self.video.taille


class Probleme:
    def __init__(self, max_cap, cache_serveur, resquest, video, endpoints):
        self.max_cap = max_cap
        self.cache_servers = cache_serveur
        self.requests = resquest
        self.videos = video
        self.endpoints = endpoints

    def __str__(self):
        s = " **** PROBLEM \n"
        s += "MAX_CAP = " + str(self.max_cap) + "\n"
        s += "Serveurs" + "\n".join(str(s) for s in self.cache_servers) + "\n"
        s += "Requests" + "\n".join(str(s) for s in self.requests) + "\n"
        s += "Videos" + "\n".join(str(s) for s in self.videos) + "\n"
        s += "Endpoints" + "\n".join(str(s) for s in self.endpoints) + "\n"
        return s

    def updateDistanceActuelle(self, request, cache_server):
        if cache_server in request.endPoint.cacheServeurs:
            request.distanceActuelle = min(request.distanceActuelle, request.endPoint.cacheServeurs[cache_server])

    def distanceActuelle(self, request):
        distanceB = request.endPoint.lat_Server
        for cacheServeur, latence in request.endPoint.cacheServeurs.iteritems():
            if request.video in cacheServeur.videos:
                distanceB = min(distanceB, latence)
        return distanceB

    def bestcs(self, video):
        max = float('-inf')
        cmax = None
        for cash_center in self.valid_cs(video):
            somme = 0
            for r in video.requests:
                if cash_center in r.endPoint.cacheServeurs:
                    somme += r.nb * (r.distanceActuelle - r.endPoint.cacheServeurs[cash_center]) / video.taille
            if somme > max:
                max = somme
                cmax = cash_center
        return max, cmax

    def get_score(self):
        res_request = 0
        for request in self.requests:
            min_latency = request.endPoint.lat_Server
            for cache_server in self.cache_servers:
                if request.video in cache_server.videos and cache_server in request.endPoint.cacheServeurs:
                    min_latency = min(min_latency, request.endPoint.cacheServeurs[cache_server])
            res_request += (request.endPoint.lat_Server - min_latency) * request.nb * 1000
        return res_request / sum(r.nb for r in self.requests)

    def solution_naive(self):
        for request in sorted(self.requests, key=lambda x: x.nb, reverse=True):
            cache_servers = [c for c in request.endPoint.cacheServeurs if
                             c.free_size(self.max_cap) > request.size and request.video not in c.videos]
            cache_servers = sorted(cache_servers, key=lambda x: request.endPoint.cacheServeurs[x])
            if len(cache_servers) > 0:
                cache_servers[0].videos.append(request.video)

    def solution_2(self):
        while True:
            requests = sorted(self.requests, key=lambda x: self.distanceActuelle(x) * x.nb, reverse=True)
            for request in requests:
                cache_servers = [c for c in request.endPoint.cacheServeurs if
                                 c.free_size(self.max_cap) > request.size and request.video not in c.videos]
                cache_servers = sorted(cache_servers, key=lambda x: request.endPoint.cacheServeurs[x])
                if len(cache_servers) > 0:
                    cache_servers[0].videos.append(request.video)
                    break
            else:
                break

    def trouverRequete(self, video):
        return [request for request in self.requests if request.video.id == video.id]

    def valid_cs(self, video):
        return [cs for cs in self.cache_servers if cs.free_size(self.max_cap) > video.taille and video not in cs.videos]

    def solution_3(self):
        i = 0
        while True:
            random.shuffle(self.videos)
            video = sorted(self.videos[:100], key=lambda x: self.bestcs(x)[0], reverse=True)[0]
            cs = self.bestcs(video)[1]
            if cs is None:
                break
            if i % 50 == 0:
                logging.info("Adding video " + str(i))
            i += 1
            cs.videos.append(video)
            for request in video.requests:
                self.updateDistanceActuelle(request, cs)

    def output_sol(self):
        cache_servers_used = [c for c in self.cache_servers if len(c.videos) > 0]
        s = str(len(cache_servers_used)) + '\n'
        for c in cache_servers_used:
            s += str(c.id) + ' ' + ' '.join([str(v.id) for v in c.videos]) + '\n'
        return s
