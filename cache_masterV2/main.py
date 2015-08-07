#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import sys

import CLOCK, LRU, LFU, OPT, ARC, LIRS, RANDOM, kRANDOM_LRU, SkLRU

import random
from random import shuffle

from settings import * 
from plots import *

l = { "CLOCK": CLOCK,
      "LRU": LRU,
      "LFU": LFU,
      "OPT": OPT,
      "LIRS": LIRS,
      "RANDOM": RANDOM,
#      "kRANDOM_LRU": kRANDOM_LRU, #  handled differently
}


array_cache=[]


def rename_files():
    p = 1
    for x in os.listdir(traces):
        name = 'trace_'+str(p)
        os.rename(traces+x,traces+name)
        p+=1
    p = None


def inicialize_traces(character, position):
    dic_temporality.clear() 
    contador = 0
    n_lineas = 0
    trace_complete = []

    for x in os.listdir(traces):  #recorre la lista de los archivos de traces
        f = open(traces+x, "r")
        lines = f.readlines()
        n_lineas = n_lineas + sum(1 for line in lines) #obtiene el número de líneas del archivo        
        f.close()        
        for line in lines:        
            key = line.replace("\n", "").lstrip().split(" ")[position].split(character)[0]
            trace_complete.append(key)
            if not(dic_temporality.has_key(key)):
                dic_temporality[key] = {'first_position':contador, 'last_position':contador, 'amount':1}
            else:
                dic_temporality.get(key)['amount'] += 1
                dic_temporality.get(key)['last_position'] = contador
                if (dic_temporality.get(key)['amount'] > 2):
                    shuffle_array.append(key)
            contador +=1
    random.shuffle(shuffle_array)
    num_lines = n_lineas

    return trace_complete,num_lines

#Crea una lista con tamaños de cache aleatorios,
#tomando como rango mínimo el tamaño del archivo más pequeño
#y como rango máximo el tamaño del archivo más grande
def inicialize_cache():     
    min_file_size = 1
    max_file_size = 0
    n_array = 5      
    max_file_size = sum((1 for key, value in dic_temporality.items() if value['amount'] == 1))   
    for i in xrange(n_array):        
        array_cache.append(random.randint(min_file_size, max_file_size))
    array_cache.sort() 


def do_originals(trace_complete):
    for algn in algorithms_selected:
        k = None
        if algn.find("RANDOM_LRU") >= 0:
            algm = kRANDOM_LRU
            k = int(algn.replace("RANDOM_LRU_", ""))
        elif algn[0] == "S" and algn.find("LRU") > 0:
            algm = SkLRU
            k = int(algn[1:].replace("LRU", ""))
        elif algn not in l:
            print "Algorithm: %s does not exist" % algn
            exit()
        else:
            algm =  l[algn]

        folder = results+ str(algn)
        if not os.path.exists(folder):
            os.makedirs(folder)

        fo = open(folder+'/'+str(algn) + "_ORIGINAL.res","wb")

        
        for c in array_cache:
            
            alg = algm.alg(c, k=k)
            
            time1 = time.time()
            lc = 0

            

            for line in trace_complete:
                
                lc += 1
                ret = alg.get(line)
                if not ret:
                    alg.put(line, 1)
                #print 'stored: '
                #print alg.stored

            time2 = time.time()
            diff = time2-time1
            tp = lc / (0.0 + diff)
            hr = alg.hitcount / (0.0 + alg.count)
            fo.write( "%s %d %.4f %.2f\n" % (str(alg), c, 100.0*hr, tp));
        fo.close()

def range_hitrate_request():
    maxhit = 0
    maxtp = 0
    i = 0
    mimhit = 0
    mimtp = 0
    
    for fn in os.listdir(results):
        f = open(results+fn)
        lines= f.readlines()
        f.close()

        for line in lines:
            a, cache_size, val, time = line.replace("\n", "").split(" ")
            maxhit = max(maxhit, float(val))
            maxtp = max(maxtp, float(time))
            if i==0:
                minhit = float(val)
                mintp = float(time)
                i+=1
            minhit = min(minhit, float(val))
            mintp = min(mintp, float(time))


    maxhit += maxhit if minhit == 0 else minhit
    maxtp += maxtp if mintp == 0 else mintp
    minhit -= 20
    mintp -= 20

    return maxhit, maxtp, minhit, mintp

def range_cache():
    min_cache, max_cache = [array_cache[0], array_cache[-1]]
    return min_cache, max_cache


   
        
    

def do_shuffle(trace_complete, num_lines):    
        
    for algn in algorithms_selected:    #recorre lista de algoritmos        
        k = None
        if algn.find("RANDOM_LRU") >= 0:
            algm = kRANDOM_LRU
            k = int(algn.replace("RANDOM_LRU_", ""))
        elif algn[0] == "S" and algn.find("LRU") > 0:
            algm = SkLRU
            k = int(algn[1:].replace("LRU", ""))
        elif algn not in l:
            print "Algorithm: %s does not exist" % algn
            exit()
        else:
            algm =  l[algn]
            
        for j in xrange(len(slices)): #recorre arreglo de slices  
            n_slice = slices[j]

            folder = results+ str(algn)
            if not os.path.exists(folder):
                os.makedirs(folder)

            file_result = open(folder+'/'+str(algn) + "_K_" + str(slices[j])+".res","wb")

            for i in xrange(len(array_cache)):    #recorre lista de tamaños de cache
                c = int(array_cache[i])
                alg = algm.alg(c, k=k)        
                time1 = time.time()
                lc = 0

                if (num_lines < slices[j]):                                        
                    n_slice = 1
                contador = 0
                
                for q in xrange(n_slice): #divide el archivo en n partes
                    
                    if ((n_slice > 0) and (n_slice < num_lines)) :
                        if(contador == 0):                            
                            num = int(round(num_lines / n_slice,0))                            
                            max_num = num
                        else:                            
                            max_num = max_num + num 
                            if (q == n_slice - 1):
                                max_num = num_lines                        

                        arreglo_lineas = random.sample(range(contador, max_num), max_num-contador)
                        lista = range(contador, max_num)
                        random.shuffle(lista)
                        contador = max_num
                        for m in xrange(len(arreglo_lineas)):
                            #line = lines[arreglo_lineas[m]]
                            line = trace_complete[arreglo_lineas[m]]
                            lc += 1
                            ret = alg.get(line)
                            if not ret:
                                alg.put(line, 1)
            
                time2 = time.time()
                diff = time2-time1
                tp = 0
                if (diff > 0):
                    tp = lc / (0.0 + diff)
                hr = 0
                if(alg.count > 0):
                    hr = alg.hitcount / (0.0 + alg.count)            
                file_result.write(str(alg) + " " + str(c) + " " + str(100.0*hr) + " " + str(tp) + "\n")
                
        file_result.close()


 
#Función que genera un nuevo arreglo para calcular el temporality
def calculate_temporality(num_lines):    
    real_traces = []          
    indice = 0
    
    for q in xrange(num_lines):
        id = next((key for key, value in dic_temporality.items() if value['first_position'] == q), None)        
        if (id != None):            
            real_traces.append(id)
        else:
            id = next((key for key, value in dic_temporality.items() if value['last_position'] == q), None)            
            if (id != None):
                real_traces.append(id)
            else:                
                indice = random.randint(0, len(shuffle_array)-1)
                real_traces.append(shuffle_array.__getitem__(indice))
                shuffle_array.__delitem__(indice)                         
    return real_traces  


def do_temporality(trace_complete):
    for algn in algorithms_selected:
        k = None
        if algn.find("RANDOM_LRU") >= 0:
            algm = kRANDOM_LRU
            k = int(algn.replace("RANDOM_LRU_", ""))
        elif algn[0] == "S" and algn.find("LRU") > 0:
            algm = SkLRU
            k = int(algn[1:].replace("LRU", ""))
        elif algn not in l:
            print "Algorithm: %s does not exist" % algn
            exit()
        else:
            algm =  l[algn]

        folder = results+ str(algn)
        if not os.path.exists(folder):
            os.makedirs(folder)

        fo = open(folder+'/'+str(algn) + "_TEMPORAL.res","wb")

        for c in array_cache:
            
            alg = algm.alg(c, k=k)
            
            time1 = time.time()
            lc = 0
            

            for line in trace_complete:
                lc += 1
                ret = alg.get(line)
                if not ret:
                    alg.put(line, 1)
                    #print 'stored: '
                    #print alg.stored

            time2 = time.time()
            diff = time2-time1
            tp = lc / (0.0 + diff)
            hr = alg.hitcount / (0.0 + alg.count)
            fo.write( "%s %d %.4f %.2f\n" % (str(alg), c, 100.0*hr, tp));
        fo.close()


def range_hitrate_request_algorithm(algorithm):
    folder = results+algorithm+'/'
    maxhit = 0
    maxtp = 0
    i = 0
    mimhit = 0
    mimtp = 0
    
    for fn in os.listdir(folder):
        f = open(folder+fn)
        lines= f.readlines()
        f.close()

        for line in lines:
            a, cache_size, val, time = line.replace("\n", "").split(" ")
            maxhit = max(maxhit, float(val))
            maxtp = max(maxtp, float(time))
            if i==0:
                minhit = float(val)
                mintp = float(time)
                i+=1
            minhit = min(minhit, float(val))
            mintp = min(mintp, float(time))


    maxhit += maxhit if minhit == 0 else minhit
    maxtp += maxtp if mintp == 0 else mintp
    minhit -= 20
    mintp -= 20

    return maxhit, maxtp, minhit, mintp

if __name__ == "__main__":
    rename_files()
    print 'fin rename_files'

    trace_complete,num_lines = inicialize_traces("&",4)
    print 'fin de captura de los traces en un solo trace_complete'

    inicialize_cache()
    print 'fin inicialize_cache'

    do_originals(trace_complete)
    print 'fin do_originals'
    

    do_shuffle(trace_complete, num_lines)
    print 'fin do_shuffle'
#
    trace_complete = None
    #
    trace_complete1 = calculate_temporality(num_lines)
    do_temporality(trace_complete1)
    print 'fin do_temporality'
    trace_complete1 = None

    #real_traces = None
    shuffle_array = None
    dic_temporality.clear()
    #slices = None

    min_cache, max_cache = range_cache()

    for algorithm in algorithms_selected:
        maxhit, maxtp, minhit, mintp = range_hitrate_request_algorithm(algorithm)
        create_cache_hitrate_algorithm_gnu(minhit, maxhit, min_cache, max_cache, algorithm)
        plot_cache_vs_hitrate_algorithm(algorithm)

