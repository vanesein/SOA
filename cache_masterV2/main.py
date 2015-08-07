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

#ss=[5, 30, 50, 70, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
ss=[]


def rename_files():
    p = 1
    for x in os.listdir(traces):
        name = 'trace_'+str(p)
        os.rename(traces+x,traces+name)
        p+=1


#Función que lee las líneas del archivo indicando la posición del id y un el caracter de separación en caso de existir
def get_file_column_from_file(character, position, lines):
    for line in lines:        
        key = line.replace("\n", "").lstrip().split(" ")[position].split(character)[0]
        real_traces.append(key)



def do_originals(character, position):
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

        for c in ss:
            
            alg = algm.alg(c, k=k)
            
            time1 = time.time()
            lc = 0

            for x in os.listdir(traces):
                f = open(traces+x, "r")
                lines = f.readlines()
                #alg.setup(lines)
                f.close()
                
                get_file_column_from_file(character, position, lines)

                for line in real_traces:
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
    min_cache, max_cache = [ss[0], ss[-1]]
    return min_cache, max_cache


#Crea una lista con tamaños de cache aleatorios,
#tomando como rango mínimo el tamaño del archivo más pequeño
#y como rango máximo el tamaño del archivo más grande
def inicialize_cache(): 
    path_size = 0
    min_file_size = 0
    max_file_size = 0
    n_array = 5    
    for the_path, dirs, files in os.walk(traces):
        for fil in files:
            filename = os.path.join(the_path, fil)
            path_size = os.path.getsize(filename)
            if(min_file_size == 0):
                min_file_size = path_size            
            if(path_size < min_file_size):
                min_file_size = path_size
            if(path_size > max_file_size):
                max_file_size = path_size   
        if (path_size > 1024):
            min_file_size = min_file_size/1024    
            max_file_size = max_file_size/1024    
                
    for i in xrange(n_array):        
        ss.append(random.randint(min_file_size, max_file_size))
    ss.sort()    
        
    

def do_shuffle(character, position):    
        
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

            for i in xrange(len(ss)):    #recorre lista de tamaños de cache
                c = int(ss[i])
                alg = algm.alg(c, k=k)        
                time1 = time.time()
                lc = 0
                #print " CACHE SIZE = " + str(ss[i])        
                
                for x in os.listdir(traces):  #recorre la lista de los archivos de traces
                    f = open(traces+x, "r")
                    lines = f.readlines()

                    get_file_column_from_file(character, position, lines)

                    #alg.setup(lines)
                    #num_lines = sum(1 for line in lines) #obtiene el número de líneas del archivo

                    num_lines = sum(1 for line in real_traces) #obtiene el número de líneas del archivo

                    f.close()
                    
                    

                    #print " leyendo archivo " + str(x) + " de " + str(num_lines) + " lineas, slice k = " + str(slices[j])   
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
                                line = real_traces[arreglo_lineas[m]]
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
                #print "hitcount: " +str(alg.hitcount)
                #print "%s %d %.4f %.2f" % (str(alg), c, 100.0*hr, tp)
                file_result.write(str(alg) + " " + str(c) + " " + str(100.0*hr) + " " + str(tp) + "\n")
                
        file_result.close()


 
#Función que genera un nuevo arreglo para calcular el temporality
def calculate_temporality(character, position):
    dic_temporality.clear()
    shuffle_array = []
    contador = 0
    num_lines = 0
    for x in os.listdir(traces):  #recorre la lista de los archivos de traces
        f = open(traces+x, "r")
        lines = f.readlines()
        num_lines = num_lines + sum(1 for line in lines) #obtiene el número de líneas del archivo
        f.close()        
        for line in lines:        
            key = line.replace("\n", "").lstrip().split(" ")[position].split(character)[0]
            if not(dic_temporality.has_key(key)):
                dic_temporality[key] = {'first_position':contador, 'last_position':contador, 'amount':1}
            else:
                dic_temporality.get(key)['amount'] += 1
                dic_temporality.get(key)['last_position'] = contador
                if (dic_temporality.get(key)['amount'] > 2):
                    shuffle_array.append(key)
            contador +=1    
    
    random.shuffle(shuffle_array)        
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


def do_temporality():
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

        for c in ss:
            
            alg = algm.alg(c, k=k)
            
            time1 = time.time()
            lc = 0

            for line in real_traces:
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

    inicialize_cache()
    print 'fin inicialize_cache'

    real_traces = []
    do_originals("&",4)
    print 'fin do_originals'

    real_traces = []
    do_shuffle("&",4)
    print 'fin do_shuffle'

    real_traces = []
    calculate_temporality("&",4)
    do_temporality()
    print 'fin do_temporality'

#
    min_cache, max_cache = range_cache()

##    create_cache_request_gnu(mintp, maxtp, min_cache, max_cache)
##    plot_cache_vs_request()

    for algorithm in algorithms_selected:
        maxhit, maxtp, minhit, mintp = range_hitrate_request_algorithm(algorithm)
        create_cache_hitrate_algorithm_gnu(minhit, maxhit, min_cache, max_cache, algorithm)
        plot_cache_vs_hitrate_algorithm(algorithm)