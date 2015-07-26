import sim

l="RANDOM"
#ss="5 30 50 70 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500"
ss="5 30 50 70 100 200"
t= true
def waitfunc {
	set +e
	pidlist=$1
	print "waiting for $pidlist"
	while t
	do
		alldone=true
		for pid in $pidlist
		do
			[[ `ps|grep $pid` ]] && alldone=false && break
		done
		$alldone && break
		sleep 0.1s
	done
	set -e
	echo "done waiting"
}