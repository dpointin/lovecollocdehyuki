from def_class import *

MAX_CAPACITY = 0
cache_servers = []
endpoints = []
requests = []
videos = []

def read_input(filename):
    global MAX_CAPACITY,cache_servers,requests,videos,endpoints
    with open(filename, 'r') as f:
        n_videos, n_endpoints, n_requests, n_cache_servers, MAX_CAPACITY = map(int, f.readline().strip().split())
        videos = [Video(i, int(f.readline())) for i in xrange(n_videos)]
        cache_servers = [CacheServeur(i) for i in range(n_cache_servers)]
        for i in xrange(n_endpoints):
            e = EndPoint(i)
            e.lat_Server, n_cache_servers_by_endpoint = map(int, f.readline().strip().split())
            for _ in xrange(n_cache_servers_by_endpoint):
                cache_server_index = int(f.readline())
                latency = int(f.readline())
                e.cacheServers[cache_servers[cache_server_index]] = latency
        for i in xrange(n_requests):
            i_video, i_endpoint, n = map(int, f.readline().strip().split())
            requests.append(Request(i, videos[i_video], endpoints[i_endpoint], n))
