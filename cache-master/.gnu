set term pngcairo
set xlabel "Cache size (items)"
set style data linespoints

set ylabel "Throughput [requests/s]"
set output "results/cache_request_tp.png"
set title "Trace: cache_request"
set xrange [0:16+50]
set yrange [0:119382.465]
plot "results/LRU.res" using 2:4  title "LRU"  , "results/RANDOM.res" using 2:4  title "RANDOM"  , "results/RANDOM_LRU_3.res" using 2:4  title "RANDOM_LRU_3"  , "results/S4LRU.res" using 2:4  title "S4LRU" 