# Loop on pairs (video, cache server) and update scores for the pairs

import logging
import sys
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

MAX_CAPACITY = 0


class Video:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.servers = []
        self.requests = []


class Server:
    def __init__(self, id):
        self.videos = []
        self.id = id

    @property
    def remaining_capacity(self):
        return MAX_CAPACITY - sum(video.size for video in self.videos)


class Endpoint:
    def __init__(self, id, latency, d_server_latency):
        self.latency = latency
        self.d_server_latency = d_server_latency
        self.id = id


class Request:
    def __init__(self, id, video, endpoint, n_videos):
        self.n_videos = n_videos
        self.endpoint = endpoint
        self.id = id
        self.video = video
        self.current_latency = self.endpoint.latency


class ChoiceStructure:
    """
    Structure defining the impact of adding a video to a server
    """
    def __init__(self, video, server):
        self.video = video
        self.server = server
        self.score = 0
        self._set_score()

    def _set_score(self):
        # Returns the score increase that we will get if we add the video to the server
        score = 0
        for request in self.video.requests:
            score += request.n_videos * \
                     max(0, request.current_latency - request.endpoint.d_server_latency.get(self.server, float('+inf'))) \
                     / self.video.size
        self.score = score * 1000


class Problem:
    def __init__(self, max_cap, servers, requests, videos, endpoints):
        global MAX_CAPACITY
        MAX_CAPACITY = max_cap
        self.servers = servers
        self.requests = requests
        self.videos = videos
        self.endpoints = endpoints
        self.result_list = []
        self.knapsack_list = []

    def update_request_latencies(self, added_video, server_impacted):
        for request in added_video.requests:
            request.current_latency = min(request.current_latency,
                                          request.endpoint.d_server_latency.get(server_impacted, float('+inf')))

    def greedy_sol(self, server):
        self.knapsack_list.sort(key=lambda c: c.score, reverse=True)
        for choice in self.knapsack_list:
            if choice.video.size < server.remaining_capacity:
                server.videos.append(choice.video)
                self.update_request_latencies(choice.video,server)

    def solve(self):
        for server in self.servers:
            logging.info("Server number "+str(server.id))
            self.knapsack_list = [ChoiceStructure(video, server) for video in self.videos]
            self.greedy_sol(server)

    def output(self):
        used_servers = [c for c in self.servers if len(c.videos) > 0]
        s = str(len(used_servers)) + '\n'
        for c in used_servers:
            s += str(c.id) + ' ' + ' '.join([str(v.id) for v in c.videos]) + '\n'
        return s


def read_input(filename):
    with open(filename, 'r') as f:
        n_videos, n_endpoints, n_requests, n_cache_servers, cap = map(int, f.readline().strip().split())
        videos = [Video(i, t) for i, t in enumerate(map(int, f.readline().strip().split()))]
        cache_servers = [Server(i) for i in range(n_cache_servers)]
        endpoints = []
        for i in xrange(n_endpoints):
            cache_servers_e = {}
            lat_server, n_cache_servers_by_endpoint = map(int, f.readline().strip().split())
            for _ in xrange(n_cache_servers_by_endpoint):
                cache_server_index, latency = map(int, f.readline().strip().split())
                cache_servers_e[cache_servers[cache_server_index]] = latency
            endpoints.append(Endpoint(i, lat_server, cache_servers_e))
        requests = []
        for i in xrange(n_requests):
            i_video, i_endpoint, n = map(int, f.readline().strip().split())
            requests.append(Request(i, videos[i_video], endpoints[i_endpoint], n))
            videos[i_video].requests.append(requests[i])
    return Problem(cap, cache_servers, requests, videos, endpoints)


if __name__ == '__main__':
    for filename in ["me_at_the_zoo", "trending_today", "videos_worth_spreading", "kittens"]:
        logging.info('*' * 10 + ' ' + filename + ' ' + '*' * 10)
        infile = os.path.join('input', filename) + '.in'
        outfile = os.path.join('greedy_sol', filename) + '.out'
        problem = read_input(infile)
        problem.solve()
        output_file = open(outfile, 'w+')
        output_file.write(problem.output())
        output_file.close()
