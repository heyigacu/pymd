
import numpy as np
import re



def read_mdinfo(mdinfo_path=''):
    """
    continuous common MD
    """
    with open(mdinfo_path, 'r') as file:
        for line in file:
            if "Completed" in line:
                parts = line.split('|')
                num_total_steps = int(parts[1].split(':')[1].strip())
                num_completed_steps = int(parts[2].split()[1].strip())
                num_remain_steps= int(parts[3].split(':')[1].strip())
                return num_remain_steps, num_completed_steps, num_total_steps


        
frame_stepsize = 50000
num_remain_steps, num_completed_steps, num_total_steps = read_mdinfo('mdinfo')
num_total_steps = 250000000
num_remain_steps = num_total_steps - num_completed_steps
num_remian_frames = np.ceil(num_remain_steps/frame_stepsize)
print(f"##################### change value of nstlim to {int(num_remian_frames*frame_stepsize)} in your_md.in ######################")




