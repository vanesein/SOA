import os

global algorithms_selected
global slices
global traces
global results
global cache_hitrate_gnu
global name_cache_hitrate_gnu
global cache_request_gnu
global name_cache_request_gnu

global real_traces
global shuffle_array
global dic_temporality

if not os.path.exists('results'):
    os.makedirs('results')

if not os.path.exists('graphics'):
    os.makedirs('graphics')

algorithms_selected = ["LRU", "RANDOM", "RANDOM_LRU_3", "S4LRU"]

slices = [1]

traces = os.getcwd()+'/traces3/'

results = os.getcwd()+'/results/'

graphics = os.getcwd()+'/graphics/'

cache_hitrate_gnu = graphics+'/cache_hitrate.gnu'
name_cache_hitrate_gnu = 'cache_hitrate.gnu'

cache_request_gnu = graphics+'/cache_request.gnu'
name_cache_request_gnu = 'cache_request.gnu'

results_slices = os.getcwd()+'/results_slices/'

cache_hitrate_slices_gnu = graphics+'cache_hitrate_slices_'


real_traces = []
shuffle_array = []
dic_temporality = dict()