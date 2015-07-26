#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import sys
import random
from random import shuffle
import itertools

import CLOCK, LRU, LFU, OPT, ARC, LIRS, RANDOM, kRANDOM_LRU, SkLRU

l = { "CLOCK": CLOCK,
      "LRU": LRU,
      "LFU": LFU,
      "OPT": OPT,
      "LIRS": LIRS,
      "ARC": ARC,
      "RANDOM": RANDOM,
      "kRANDOM_LRU": kRANDOM_LRU, #  handled differently
}

ls="LRU"
ss = []
#slices = [1, 4, 6]
#path = os.getcwd()+'/traces test/'
slices = [1, 2, 4, 30, 120]
path = os.getcwd()+'/traces/'

def rename_files():
    p = 1        
    for x in os.listdir(path):
        name = 'trace_'+str(p)
        os.rename(path+x,path+name)
        p+=1

def get_size_files():
    path_size = 0
    contador = 0    
    for the_path, dirs, files in os.walk(path):
        for fil in files:
            filename = os.path.join(the_path, fil)
            path_size += os.path.getsize(filename)
            contador +=1
    print "path_size: " +str((path_size/1024)/contador)
    return path_size
#Crea una lista con tamaños de cache aleatorios,
#tomando como rango mínimo el tamaño del archivo más pequeño
#y como rango máximo el tamaño del archivo más grande
def inicialize_cache(): 
    path_size = 0
    min_file_size = 0
    max_file_size = 0
    n_array = 2    
    for the_path, dirs, files in os.walk(path):
        for fil in files:
            filename = os.path.join(the_path, fil)
            path_size = os.path.getsize(filename)
            if(min_file_size == 0):
                min_file_size = path_size            
            if(path_size < min_file_size):
                min_file_size = path_size
            if(path_size > max_file_size):
                max_file_size = path_size            
    min_file_size = min_file_size/1024    
    max_file_size = max_file_size/1024    
    
    for i in xrange(n_array):        
        ss.append(random.randint(min_file_size, max_file_size))
    ss.sort()    
    
    
def fillspace(s):
    return s + " " * (20 - len(s))

def doitall():
    algn = ls
    
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
    #ss = [3, 6, 9]
    for i in xrange(len(ss)):    #recorre lista de tamaños de cache
        c = int(ss[i])        
        print " CACHE SIZE = " + str(ss[i])        
        for j in xrange(len(slices)): #recorre arreglo de slices
            alg = algm.alg(c, k=k)        
            time1 = time.time()
            lc = 0
            for x in os.listdir(path):  #recorre la lista de los archivos de traces
                f = open(path+x, "r")
                lines = f.readlines()
                alg.setup(lines)
                num_lines = sum(1 for line in lines) #obtiene el número de líneas del archivo
                f.close()
                print " leyendo archivo " + str(x) + " de " + str(num_lines) + " lineas, slice k = " + str(slices[j])                               
                contador = 0
                for k in xrange(slices[j]): #divide el archivo en n partes                    
                    if ((slices[j] > 0) and (slices[j] < num_lines)) :
                        if(contador == 0):                            
                            num = int(round(num_lines / slices[j],0))                            
                            max_num = num
                        else:                            
                            max_num = max_num + num 
                            if (k == slices[j] - 1):
                                max_num = num_lines                        
                        #print "contador: " + str(contador) + " max_num: " + str(max_num)                        
                        arreglo_lineas = random.sample(range(contador, max_num), max_num-contador)
                        lista = range(contador, max_num)
                        random.shuffle(lista)
                        #print "Reshuffled lista: " , lista
                        #print arreglo_lineas                        
                        contador = max_num
                        for m in xrange(len(arreglo_lineas)):
                            #print lines[arreglo_lineas[m]]
                            line = lines[arreglo_lineas[m]]
                            lc += 1
                            b = line.replace("\n", "").lstrip()
                            key = b.split(" ")[0]
                            #print 'key del trace: '+ str(key)
                            ret = alg.get(key)
                            if not ret:
                                alg.put(key, 1)
                            
        
            time2 = time.time()
            diff = time2-time1
            tp = lc / (0.0 + diff)
            hr = alg.hitcount / (0.0 + alg.count)
            print "hitcount: " +str(alg.hitcount)
            print "%s %d %.4f %.2f" % (str(alg), c, 100.0*hr, tp)
                #sys.stderr.write("%s with %d\tHit ratio: %.4f\tThroughput: %.2f (reqs/s)\n" % (fillspace(str(alg)), c, hr, tp))


if __name__ == "__main__":
    #rename_files()
    inicialize_cache()
    doitall()