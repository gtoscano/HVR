- [ ] copy source from `stability_pop_indicator`
- [ ] compare against `scalar_forms`
- [ ] add `readme.md`
- [ ] add documentation about how to add `wfg_hypervolume` to `path` in your `.bashrc`
- [ ] update `hv.sh` to remove the modification of `PATH`











# #

```c
OBJECTIVE get_ref_point_def_value(int m_objs) {
    
    OBJECTIVE def_value = 0;
    OBJECTIVE h = 0;
    
    if (m_objs == 3)	h = 12;
    if (m_objs == 4)	h = 7;
    if (m_objs == 5)	h = 6;
    if (m_objs == 6)	h = 4;
    if (m_objs == 7)	h = 4;
    if (m_objs == 8)	h = 3;
    if (m_objs == 10)	h = 3;
    else {
    	printf("There is not a default value for h for m=%d objectives", m_objs);
    	exit(0);
   }
    
    def_value = 1 + (1/h);
   	
   	return def_value;
}
```



```c

// define reference vector

// @add
// this function returns 1 + 1/H according to maxn (m_objs)
// OBJECTIVE == double
OBJECTIVE def_value = get_ref_point_def_value(maxn);

for (int i = ind_ref_vect; i < argc; i++) {
	ref.objectives[i - ind_ref_vect] = atof(argv[i]);
      
	// added to define a default reference point
    if (ref.objectives[i - ind_ref_vec] < 0)
        ref.objectives[i - ind_ref_vect] = def_value;

    // added for normalizing hv [Cheng16]
	total_volume *= ref.objectives[i - ind_ref_vect]; 
}


// added
if (verbose_flag) {
    printf ("ref point:\n");
        
    for (int counter=arg_index+1, id=0; counter<argc; counter++, id++)
            printf("%d, %.2f \n", id, ref.objectives[counter]);
}
```





