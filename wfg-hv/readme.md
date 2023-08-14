# About this repository

This repository contains our fork of the WFG (Walking Fish Group) algorithm [Bradstreet10] to compute the hypervolume indicator.

The implementation in C was obtained from [here](http://www.wfg.csse.uwa.edu.au/hypervolume/). We use the version 1.15. The reader is referred to [Bradstreet10] for more details.

## Compile

In [Bradstreet10], the authors suggest to use `gcc -O3 -march=nocona -funroll-all-loops` for compilation, but such an option do not appear in `makefile`.  Instead, we compile `wfg.c` as follows:

```
make march=nocona clean; make march=nocona
```

----

**Note**: The following error could be displayed:

```
$ make march=nocona clean; make march=nocona

rm -f wfg *.o 
rm -rf *.dSYM
gcc -std=c99 -Wall  -O3  -march=nocona -c read.c
gcc -std=c99 -Wall  -O3  -march=nocona -o wfg wfg.c read.o 
wfg.c: In function ‘main’:
wfg.c:553:24: warning: implicit declaration of function ‘getopt’ [-Wimplicit-function-declaration]
     while ((argument = getopt(argc, argv, "q")) != -1)
                        ^
wfg.c:566:17: error: ‘optind’ undeclared (first use in this function)
     arg_index = optind;         // acts as an offset
                 ^
wfg.c:566:17: note: each undeclared identifier is reported only once for each function it appears in
makefile:20: recipe for target 'wfg' failed
make: *** [wfg] Error 1
```

In order to fix it, you need to change `makefile` to use `getopt`. Replace this line:

```
CC = gcc -std=c99 -Wall  $(OPT)
```

for this line:

```
CC = gcc -Wall  $(OPT)
```

Then, compile again:

```
make march=nocona clean; make march=nocona
```

----

**Note for `chronos`**: These changes are needed to compile `wfg.c` in `chronos`:

1. Edit `makefile` to use `-std=c99` to allow loops like `for (int i=0; ...)`:

```
# makefile
CC = gcc -std=c99 -Wall  $(OPT)
```

2. Include `getopt.h` in `wfg.c`:

```
// wfg.c
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>  # add this one
```

----



## Add `wfg_hypervolume` to `PATH`

Add the following snippet at the bottom of `~/.bashrc`:

```
# wfg
WFG_PATH="$HOME/wfg_hypervolume"

PATH=${WFG_PATH}:${PATH}
export PATH
```

Now, `wfg` will be available as a command:

```
$ wfg

verbose flag: 1, arg_index: 1, argc: 1, ind_filename: 1, ind_ref_vect: 2
filename: (null)
ref point:
File (null) could not be opened
```


## Usage

The input file must follow this format:

```
# 
0.598 0.737 0.131 0.916 6.745
0.263 0.740 0.449 0.753 6.964
0.109 8.483 0.199 0.302 8.872
#
```
where:

- objective values are separated by spaces
- one point (objective vector) per line
- fronts are separated by `#` (otherwise, a `segfault` will arise)
- all fronts use the same reference point, therefore all points in all fronts must have the same number of objectives. 


## Example

```
$ wfg pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
```

This is the output:

```
verbose flag: 1, arg_index: 1, argc: 10, ind_filename: 1, ind_ref_vect: 2
filename: pop_sample.txt
ref point:
0, 1.10 
1, 1.10 
2, 1.10 
3, 1.10 
4, 1.10 
5, 1.10 
6, 1.10 
7, 1.10 
# fronts: 1
# maxm: 2137
# maxn: 8
1.714551 0.799851
Time: 0.371660 (s)
Total time = 0.371660 (s)
```

You can use `-q` to ignore additional info:

```
$ wfg -q pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
```

This is the output:

```
1.714551 0.799851
```



## Modifications

We made two modifications to `wfg.c` to avoid printing warning messages and normalize the hypervolume. 

1. **Do not print times**. This is the output of the original implementation:

   ```
   hv(1) = 0.0297853976
   Time: 7.996000 (s)
   Total time = 7.996000 (s)
   ```

   We have added a parameter `-q` (for quiet) to reduce the amount of information as output to:

   ```
   0.0297853976
   ```

2. **Normalize output**. The *raw* hypervolume value is normalized following the considerations in [Cheng16].   Now, the output contains two values: the raw and normalized hypervolume values, respectively:

   ```
   0.029785 0.007130
   ```

3. **Handle of empty pop** Suppose the input pop looks like this:


  ```
  #
  #
  ```

  Then, call `wfg` as follows:

  ```
  wfg -q empty_pop.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
  ```

  This is the output:

  ```
  0 0
  ```


## Updates

- **21/may/2018**  `rev 6` is in `chronos`. Also, it has been compiled.
- **8/july/2018** `rev 9` replaces `exit(1)` by `exit(0)` to avoid errors when calling `wfg` within python with `subprocess.check_output`.
- **10/dec/2018** `changeset 11:dbcb089e92cc ` `wfg.c` and `makefile` were reverted to the original version of the `WFG` group because our modified version has some issues according to `valgrind`. Use the following approach to test `wfg` using `valgrind`:

```
cd ~/wfg_hypervolume
make march=nocona clean; make march=nocona
valgrind --tool=memcheck --leak-check=full -v --show-leak-kinds=all ./wfg pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
```

This *is the output of the original version*

```
File pop_sample.txt could not be opened
==3764== 
==3764== HEAP SUMMARY:
==3764==     in use at exit: 16 bytes in 1 blocks
==3764==   total heap usage: 2 allocs, 1 frees, 568 bytes allocated
==3764== 
==3764== Searching for pointers to 1 not-freed blocks
==3764== Checked 62,816 bytes
==3764== 
==3764== 16 bytes in 1 blocks are still reachable in loss record 1 of 1
==3764==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==3764==    by 0x402E67: readFile (in /home/auraham/Desktop/WFG_1.15/wfg)
==3764==    by 0x4008A5: main (in /home/auraham/Desktop/WFG_1.15/wfg)
==3764== 
==3764== LEAK SUMMARY:
==3764==    definitely lost: 0 bytes in 0 blocks
==3764==    indirectly lost: 0 bytes in 0 blocks
==3764==      possibly lost: 0 bytes in 0 blocks
==3764==    still reachable: 16 bytes in 1 blocks
==3764==         suppressed: 0 bytes in 0 blocks
==3764== 
==3764== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
==3764== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

Notice the first line:

```
File pop_sample.txt could not be opened
```

For that reason, there is no memory leaks. The reason of that error is because `pop_sample.txt` is not in the `WFG_1.15` directory. After copying such a file, this is the output:

```
cd ~/Desktop/WFG_1.15$ 
./wfg pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
hv(1) = 1.7145510555
Time: 0.331279 (s)
Total time = 0.331279 (s)
```

```
valgrind --tool=memcheck --leak-check=full -v --show-leak-kinds=all ./wfg pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
```

```
==3913== Invalid write of size 4
==3913==    at 0x4017FD: makeDominatedBit (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==    by 0x402BF7: hv (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==    by 0x4028DA: hv (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==    by 0x4028DA: hv (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==    by 0x4028DA: hv (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==    by 0x4028DA: hv (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==    by 0x4028DA: hv (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==    by 0x400CD2: main (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913==  Address 0x66b1fec is 4 bytes before a block of size 8,548 alloc'd
==3913==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==3913==    by 0x400A35: main (in /home/auraham/Desktop/WFG_1.15/wfg)
==3913== 
==3913== ERROR SUMMARY: 19463 errors from 4 contexts (suppressed: 0 from 0)
```

**tl;dr** the original version has memory leaks.

- **10/dec/2018** `changeset: 13:bfda5955484d` `wfg.c` and `makefile` were restored to `rev 3e08` via these commands:

```
hg revert --rev 3e08 wfg.c
hg revert --rev 3e08 makefile
```

We evaluated this revision using these commands:

```
cd ~/wfg_hypervolume
make march=nocona clean; make march=nocona
valgrind --tool=memcheck --leak-check=full -v --show-leak-kinds=all ./wfg pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
```

This is the output:

```
==4997== 11014 errors in context 3 of 4:
==4997== Invalid write of size 4
==4997==    at 0x401ACD: makeDominatedBit (in /home/auraham/wfg_hypervolume/wfg)
==4997==    by 0x402EC7: hv (in /home/auraham/wfg_hypervolume/wfg)
==4997==    by 0x402BAA: hv (in /home/auraham/wfg_hypervolume/wfg)
==4997==    by 0x402BAA: hv (in /home/auraham/wfg_hypervolume/wfg)
==4997==    by 0x402BAA: hv (in /home/auraham/wfg_hypervolume/wfg)
==4997==    by 0x402BAA: hv (in /home/auraham/wfg_hypervolume/wfg)
==4997==    by 0x402BAA: hv (in /home/auraham/wfg_hypervolume/wfg)
==4997==    by 0x400ED3: main (in /home/auraham/wfg_hypervolume/wfg)
==4997==  Address 0x66b24bc is 4 bytes before a block of size 8,548 alloc'd
==4997==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==4997==    by 0x400BD0: main (in /home/auraham/wfg_hypervolume/wfg)
==4997== 
==4997== ERROR SUMMARY: 19463 errors from 4 contexts (suppressed: 0 from 0)
```

The number of errors, `19463`, is the same as in the previous revision. That is, our modification are not causing additional memory errors (I guess!).

- **10/dec/2018** `changeset: 16:aeb893c818f2` This version defines each component of the reference point as `r=1+1/H` [Ishibuchi18] when the user employs `0` as reference point. Example:

```
cd ~/wfg_hypervolume
./wfg -q pop_sample.txt 0 0 0 0 0 0 0 0
9.507890 0.951863
```

Also, you can use a given reference point (only if each component is greater or equal to 1):

```
cd ~/wfg_hypervolume
./wfg -q pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1
1.714551 0.799851
```

Finally, this is the `valgrind` test:

```
valgrind --tool=memcheck --leak-check=full -v --show-leak-kinds=all ./wfg pop_sample.txt 0 0 0 0 0 0 0 0 

...
==6212== ERROR SUMMARY: 19463 errors from 4 contexts (suppressed: 0 from 0)
```

```
valgrind --tool=memcheck --leak-check=full -v --show-leak-kinds=all ./wfg pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1

...
==6265== ERROR SUMMARY: 19463 errors from 4 contexts (suppressed: 0 from 0)
```

- **11/dec/2018** `changeset 20:201142fd82f4` We found this error message when compiling in `udon4`:

```
wfg.c: In function ‘main’:
wfg.c:749:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
     if (verbose_flag)
     ^~
wfg.c:752:2: note: ...this statement, but the latter is misleadingly indented as if it is guarded by the ‘if’
  return 0;
  ^~~~~~
```

We added `{` and `}` to remove the previous error message:

```
if (verbose_flag) {
        printf("Total time = %f (s)\n", totaltime);
}

return 0;
```



## References

- [Cheng16] *A Reference Vector Guided Evolutionary Algorithm for Many-Objective Optimization*.
- [Bradstreet10] *A Fast Many-objective Hypervolume Algorithm using Iterated Incremental Calculations*.
- [Ishibuchi18] *How to Specify a Reference Point in Hypervolume Calculation for Fair Performance Comparison*.