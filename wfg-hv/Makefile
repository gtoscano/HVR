EXE = wfg
OBJ = read.o 
OPT = -O3 

# use this line in chronos
#CC = gcc -std=c99 -Wall  $(OPT)

# use this line for getopt
CC = gcc -Wall -O3 -march=native

$(EXE): $(OBJ) wfg.c
	$(CC) -o wfg wfg.c $(OBJ)

%.o: %.c
	$(CC) -c $<

clean: 
	rm -f wfg *.o 
	rm -rf *.dSYM
