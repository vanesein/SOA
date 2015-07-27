import os

global algorithms_selected
global traces
global results
global cache_hitrate_gnu
global name_cache_hitrate_gnu
global cache_request_gnu
global name_cache_request_gnu


if not os.path.exists('results'):
    os.makedirs('results')

if not os.path.exists('results_slices'):
    os.makedirs('results_slices')

if not os.path.exists('graphics'):
    os.makedirs('graphics')

algorithms_selected = ["LRU", "RANDOM", "RANDOM_LRU_3", "S4LRU"]

traces = os.getcwd()+'/traces2/'

results = os.getcwd()+'/results/'

graphics = os.getcwd()+'/graphics/'

cache_hitrate_gnu = graphics+'/cache_hitrate.gnu'
name_cache_hitrate_gnu = 'cache_hitrate.gnu'

cache_request_gnu = graphics+'/cache_request.gnu'
name_cache_request_gnu = 'cache_request.gnu'

results_slices = os.getcwd()+'/results_slices/'

cache_hitrate_slices_gnu = graphics+'cache_hitrate_slices_'
