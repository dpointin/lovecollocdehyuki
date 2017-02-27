from def_class import *


def read_input(filename):
    with open(filename, 'r') as f:
        n_videos, n_endpoints, n_requests, n_cache_servers, MAX_CAPACITY = map(int, f.readline().strip().split())
        videos = [Video(i, t) for i, t in enumerate(map(int, f.readline().strip().split()))]
        cache_servers = [CacheServeur(i) for i in range(n_cache_servers)]
        endpoints = []
        for i in xrange(n_endpoints):
            cache_servers_e = {}
            lat_server, n_cache_servers_by_endpoint = map(int, f.readline().strip().split())
            for _ in xrange(n_cache_servers_by_endpoint):
                cache_server_index,latency = map(int, f.readline().strip().split())
                cache_servers_e[cache_servers[cache_server_index]] = latency
            endpoints.append(EndPoint(i, lat_server, cache_servers_e))
        requests = []
        for i in xrange(n_requests):
            i_video, i_endpoint, n = map(int, f.readline().strip().split())
            requests.append(Request(i, videos[i_video], endpoints[i_endpoint], n))
            videos[i_video].requests.append(requests[i])
    return Probleme(MAX_CAPACITY, cache_servers, requests, videos, endpoints)
