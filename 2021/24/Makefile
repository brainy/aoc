COPT = -O3 -DNDEBUG
# COPT = -g -O0

all: solve

solve: execute.c solve.c Makefile
	clang -std=c99 -Wall $(COPT) -o '$@' solve.c

execute.c: compile.py input.txt
	@./compile.py 'input.txt' > 'temp.$@'
	@if cmp -s 'temp.$@' '$@'; then                 \
	    rm -f 'temp.$@';                            \
	else                                            \
	    echo "./compile.py 'input.txt' > '$@'";     \
	    mv 'temp.$@' '$@';                          \
	fi
