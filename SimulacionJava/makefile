JC = javac
JCR = java

.SUFFIXES: .java .class
.java.class:
	$(JC) $*.java

CLASSES = \
	DiscreteEventSimulation.java \
	Event.java \
	EventHandler.java \
	EventHeap.java \
	Machine.java \
	Repairman.java \
	Simulation.java \
	User.java 

TXT_FILES = \
	trace_java.txt \

default: classes exec-tests

classes: $(CLASSES:.java=.class)

clean:
	$(RM) *.class *~

exec-tests: classes
	set -e; \
	for file in $(TXT_FILES); do $(JCR) DiscreteEventSimulation $$file; done;


.PHONY: default clean classes exec-tests

