/*
 * parser.c
 * https://www.gnu.org/software/libc/manual/html_node/Example-of-Getopt.html
 * https://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html
 * */

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int
main (int argc, char **argv)
{
  int verbose_flag = 1;
  int index;
  int c;

  opterr = 0;


  while ((c = getopt (argc, argv, "q")) != -1)
    switch (c)
      {
      case 'q':     // quiet
        verbose_flag = 0;
        break;
        
      /*  
      case 'c':
        cvalue = optarg;
        break;
      case '?':
        if (optopt == 'c')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      */
      default:
        abort ();
      }


  index = optind;

  printf ("verbose_flag = %d, index = %d\n",
          verbose_flag, index);

  for (index = optind; index < argc; index++)
    printf ("Non-option argument %s\n", argv[index]);
  return 0;
}
