import Gnuplot
from os import system, remove

import matplotlib.pyplot as plt

from settings import * 


def create_cache_hitrate_gnu(minhit, maxhit, min_cache, max_cache):
    fo = open(cache_hitrate_gnu, "wb")
    fo.write(  "set term pngcairo\n")
    fo.write(  "set key right top\n")
    fo.write(  "set xlabel \"Cache size (items)\"\n")
    fo.write(  "set style data linespoints\n")
    fo.write(  "set ylabel \"Hit ratio [%]\"\n")
    fo.write(  "set output \"graphics/cache_hitrate.png\"\n")
    fo.write(  "set title \"Trace: Cache vs HitRate\"\n")
    fo.write(  "set xrange ["+str(min_cache)+":"+str(max_cache)+"]\n")
    fo.write(  "set yrange ["+str(minhit)+":"+str(maxhit)+"]\n")

    a = "plot "
    notfirst = ""
    p = 1

    for alg in algorithms_selected:
        if p == len (algorithms_selected):
            notfirst = notfirst + "\"results/"+alg+".res\" using 2:3  title \""+alg+"\" "
        else:
            notfirst = notfirst + "\"results/"+alg+".res\" using 2:3  title \""+alg+"\" , "
        p+=1

    a = a + notfirst
    fo.write( a )
    fo.close()

def plot_cache_vs_hitrate():
    system('gnuplot ' + cache_hitrate_gnu)
    remove(cache_hitrate_gnu)


def create_cache_request_gnu(mintp, maxtp, min_cache, max_cache):
    
    fo = open(cache_request_gnu, "wb")
    fo.write(  "set term pngcairo\n")
    fo.write(  "set key right top\n")
    fo.write(  "set xlabel \"Cache size (items)\"\n")
    fo.write(  "set style data linespoints\n")
    fo.write(  "set ylabel \"Throughput [requests/s]\"\n")
    fo.write(  "set output \"graphics/cache_request.png\"\n")
    fo.write(  "set title \"Trace: Cache vs Throughput [requests/s]\"\n")
    fo.write(  "set xrange ["+str(min_cache)+":"+str(max_cache)+"]\n")
    fo.write(  "set yrange ["+str(mintp)+":"+str(maxtp)+"]\n")
    
    a = "plot "
    notfirst = ""
    p = 1

    for alg in algorithms_selected:
        if p == len (algorithms_selected):
            notfirst = notfirst + "\"results/"+alg+".res\" using 2:4  title \""+alg+"\" "
        else:
            notfirst = notfirst + "\"results/"+alg+".res\" using 2:4  title \""+alg+"\" , "
        p+=1

    a = a + notfirst
    fo.write( a )
    fo.close()

def plot_cache_vs_request():
    system('gnuplot ' + cache_request_gnu)
    remove(cache_request_gnu)



def create_cache_hitrate_slice_gnu(minhit, maxhit, min_cache, max_cache, slices, algorithm):
    folder = results_slices+algorithm+'/'
    results_file = algorithm+'_K_'

    file_name_gnu = cache_hitrate_slices_gnu+algorithm+'.gnu'
    file_name_png = cache_hitrate_slices_gnu+algorithm+'.png'

    fo = open(file_name_gnu, "wb")
    fo.write(  "set term pngcairo\n")
    fo.write(  "set key right top\n")
    fo.write(  "set xlabel \"Cache size (items)\"\n")
    fo.write(  "set style data linespoints\n")
    fo.write(  "set ylabel \"Hit ratio [%]\"\n")
    fo.write(  "set output \""+file_name_png+"\"\n")
    fo.write(  "set title \"Trace: Cache vs HitRate "+algorithm+"\"\n")
    fo.write(  "set xrange ["+str(min_cache)+":"+str(max_cache)+"]\n")
    fo.write(  "set yrange ["+str(minhit)+":"+str(maxhit)+"]\n")
    
    a = "plot "
    notfirst = ""
    p = 1

    for k in slices:
        if p == len (slices):
            notfirst = notfirst + "\""+folder+results_file+str(k)+".res\" using 2:3  title \"Shuffling, K = "+str(k)+"\" "
        else:
            notfirst = notfirst + "\""+folder+results_file+str(k)+".res\" using 2:3  title \"Shuffling, K = "+str(k)+"\" , "
        p+=1

    a = a + notfirst
    fo.write( a )
    fo.close()

def plot_cache_vs_hitrate_slices(algorithm):
    file_name_gnu = cache_hitrate_slices_gnu+algorithm+'.gnu'

    system('gnuplot ' + file_name_gnu)
    remove(file_name_gnu)


