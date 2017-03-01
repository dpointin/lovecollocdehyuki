# Loop on pairs (video, cache server) and update scores for the pairs

import logging
import sys
import os
import functools

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

MAX_CAPACITY = 0


class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return self.func(*args)

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)


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
                     max(0, request.current_latency - request.endpoint.d_server_latency.get(self.server, float('+inf')))
        self.score = score


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

    """
    def knapsack(self):
        # Return the value of the most valuable subsequence of the first i
        # elements in items whose weights sum to no more than j.
        @memoized
        def best_value(max_obj_id, max_cap):
            if max_obj_id == 0: return 0
            choice = self.knapsack_list[max_obj_id - 1]
            if choice.video.size > max_cap:
                return best_value(max_obj_id - 1, max_cap)
            else:
                return max(best_value(max_obj_id - 1, max_cap),
                           best_value(max_obj_id - 1, max_cap - choice.video.size) + choice.score)

        max_cap = MAX_CAPACITY
        result = []
        for max_obj_id in xrange(len(self.knapsack_list), 0, -1):
            if best_value(max_obj_id, max_cap) != best_value(max_obj_id - 1, max_cap):
                result.append(self.knapsack_list[max_obj_id - 1])
                max_cap -= self.knapsack_list[max_obj_id - 1].score
        for choice in result:
            choice.server.videos.append(choice.video)
            self.update_request_latencies(choice.video, choice.server)
    """

    def knapsack_iterative(self):
        best_values = [[0] * (MAX_CAPACITY + 1) for _ in xrange(len(self.knapsack_list) + 1)]

        for i, choice in enumerate(self.knapsack_list):
            for capacity in xrange(MAX_CAPACITY + 1):
                if choice.video.size > capacity:
                    best_values[i + 1][capacity] = best_values[i][capacity]
                else:
                    best_values[i + 1][capacity] = max(best_values[i][capacity],
                                                       best_values[i][capacity - choice.video.size] + choice.score)

        result = []
        j = MAX_CAPACITY
        for i in xrange(len(self.knapsack_list), 0, -1):
            if best_values[i][j] != best_values[i - 1][j]:
                result.append(self.knapsack_list[i - 1])
                j -= self.knapsack_list[i - 1].video.size
            i -= 1
        for choice in result:
            choice.server.videos.append(choice.video)
            self.update_request_latencies(choice.video, choice.server)

    def solve(self):
        # increase recursion depth to avoid
        sys.setrecursionlimit(10000)
        for server in self.servers:
            logging.info("Server number " + str(server.id))
            self.knapsack_list = [ChoiceStructure(video, server) for video in self.videos]
            self.knapsack_iterative()

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
        outfile = os.path.join('knapsack', filename) + '.out'
        problem = read_input(infile)
        problem.solve()
        output_file = open(outfile, 'w+')
        output_file.write(problem.output())
        output_file.close()
