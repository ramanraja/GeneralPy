# some utility functions (test them well !)

def normalise(in_pix):  
    minval = min(in_pix)    
    maxval = max(in_pix)  
    out_pix = [(x-minval) / (maxval-minval) for x in in_pix]
    return (out_pix)
        
        
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def map_value(x, in_min, in_max, out_min, out_max):
    if (x < in_min) : x = in_min  # Rajaraman's change to avoid negatives
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
      
 