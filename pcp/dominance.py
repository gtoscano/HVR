"""
dominance.py
@todo: compare is working, but it would be great if we could implement the PISA's dominance version
"""

from pylab import *

A_DOM_B       =  1;
A_IS_DOM_BY_B = -1;
A_EQUALS_TO_B =  0;
NON_DOMINATED = -2;


dom_flags = {
    1:  "A\\_DOM\\_B",
    -1: "A\\_IS\\_DOM\\_BY\\_B",
    0:  "A\\_EQUALS\\_TO\\_B" ,
    -2: "NON\\_DOMINATED",
    }
    


def compare_min(a, b, cnstr_a, cnstr_b):
    if cnstr_a < 0 and cnstr_b < 0:
        if cnstr_b > cnstr_a:
            return A_IS_DOM_BY_B
        elif cnstr_a > cnstr_b:
            return A_DOM_B
        else:
            return NON_DOMINATED
    elif cnstr_a >= 0 and cnstr_b < 0:
        return A_DOM_B
    elif cnstr_a < 0 and cnstr_b >= 0:

        return A_IS_DOM_BY_B
    
    m = a.shape[0]
    
    flag_diff = False               # we assume that a and b are different
    flag_dominance = None;          # dominance flag
    flag_aux = None;                # auxilar flag
    
    
    for i in range(m):
        
        if (a[i] == b[i]):
            continue                        # same i-th objective, it has no sense to compare

        elif (a[i] < b[i]):
            flag_aux = A_DOM_B
            flag_diff = True                # the i-th objetive of both a and b is different
            break                                # that is, a and b are different objective vectors
     
        else:
            flag_aux = A_IS_DOM_BY_B
            flag_diff = True                # the i-th objetive of both a and b is different
            break                                # that is, a and b are different objective vectors
     
    if not flag_diff:
        return A_EQUALS_TO_B
        
    
    for i in range(m):
        
        if (a[i] == b[i]):
            continue                        # same i-th objective, it has no sense to compare
        #else:
        #    flag_diff = True                # the i-th objetive of both a and b is different
                                            # that is, a and b are different objective vectors
        
        if (a[i] < b[i]):
            flag_dominance = A_DOM_B
        else:
            flag_dominance = A_IS_DOM_BY_B
            
        #if (i == 0):
        #    flag_aux = flag_dominance;
        #    continue
        
        
        if (flag_aux != flag_dominance):
            return NON_DOMINATED            # there was a change in dominantion, thus, a and b are non dominated
    

    #if (flag_diff == False):
    #    flag_dominance = A_EQUALS_TO_B      # a and b are the same vector    
    
    return flag_dominance





def compare_max(a, b, cnst_a=0, cnst_b=0):
    if cnstr_a < 0 and cnstr_b < 0:
        if cnstr_a < cnstr_b:
            return A_IS_DOM_BY_B
        elif cnstr_b < cnstr_a:
            return A_DOM_B
    elif cnstr_a == 0 and cnstr_b < 0:
        return A_DOM_B
    elif cnstr_a < 0 and cnstr_b == 0:
        return A_IS_DOM_BY_B    
    
    m = a.shape[0]
    
    flag_diff = False               # we assume that a and b are different
    flag_dominance = None;          # dominance flag
    flag_aux = None;                # auxilar flag
    
    
    for i in range(m):
        
        if (a[i] == b[i]):
            continue                        # same i-th objective, it has no sense to compare

        elif (a[i] > b[i]):
            flag_aux = A_DOM_B
            flag_diff = True                # the i-th objetive of both a and b is different
            break                                # that is, a and b are different objective vectors
     
        else:
            flag_aux = A_IS_DOM_BY_B
            flag_diff = True                # the i-th objetive of both a and b is different
            break                                # that is, a and b are different objective vectors
     
    if not flag_diff:
        return A_EQUALS_TO_B
        
    
    for i in range(m):
        
        if (a[i] == b[i]):
            continue                        # same i-th objective, it has no sense to compare
        #else:
        #    flag_diff = True                # the i-th objetive of both a and b is different
                                            # that is, a and b are different objective vectors
        
        if (a[i] > b[i]):
            flag_dominance = A_DOM_B
        else:
            flag_dominance = A_IS_DOM_BY_B
            
        #if (i == 0):
        #    flag_aux = flag_dominance;
        #    continue
        
        
        if (flag_aux != flag_dominance):
            return NON_DOMINATED            # there was a change in dominantion, thus, a and b are non dominated
    

    #if (flag_diff == False):
    #    flag_dominance = A_EQUALS_TO_B      # a and b are the same vector    
    
    return flag_dominance

