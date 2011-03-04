# Makefile template for erlang

.SUFFIXES: .erl .beam .yrl

.erl.beam:
	erlc -W $<

.yrl.erl:
	erlc -W $<


# Here is a list of erlang modules you want compiling
# If the modules don't fit onto one line add a \ 
# continuation character to the end of the line and 
# continue on the next line

# Edit the lines below
MODS = module1 module2


# The first target, and as such the default
all: compile

compile: ${MODS:%=%.beam} subdirs

special1.beam: special1.erl
	${ERL} -DDebug -W0 special1.erl

clean:
	rm -rf *.beam erl_crash.dump


