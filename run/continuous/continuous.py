
import numpy as np
import re

def cmd_continuous(mdinfo_path=''):
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

def read_gamdlog(gamdlog_path, num_completed_steps=5000000):
    """
    continuous GaMD
    """
    with open(gamdlog_path, 'r') as f:
        lines = f.readlines()
        num_gamdlog_outs = len(lines) - 3
        gamdlog_stepsize = int(lines[3].split()[0])
        num_gamd_steps = num_gamdlog_outs*gamdlog_stepsize
    num_gamdlog_short = int((num_completed_steps- num_gamd_steps)/gamdlog_stepsize)
    return num_gamdlog_short, gamdlog_stepsize


def generate_interpolated_lines_formatted(start_str, end_str, n):
    def split_with_spaces(s):
        return re.findall(r'\s+|\S+', s)
    start_parts = split_with_spaces(start_str)
    end_parts = split_with_spaces(end_str)
    num_indices = [i for i, part in enumerate(start_parts) if not part.isspace()]
    start_nums_str = [start_parts[i] for i in num_indices]
    end_nums_str = [end_parts[i] for i in num_indices]
    if len(start_nums_str) != len(end_nums_str):
        raise ValueError("起始和末尾数据行的数值数量必须相同。")
    num_columns = len(start_nums_str)
    formats = []
    for col in range(num_columns):
        start_num = start_nums_str[col]
        end_num = end_nums_str[col]
        def count_decimal(s):
            if '.' in s:
                return len(s.split('.')[-1])
            else:
                return 0
        decimals_start = count_decimal(start_num)
        decimals_end = count_decimal(end_num)
        decimals = max(decimals_start, decimals_end)
        width_start = len(start_num)
        width_end = len(end_num)
        width = max(width_start, width_end)
        fmt = f"{{:>{width}.{decimals}f}}"
        formats.append(fmt)
    start_vals = list(map(float, start_nums_str))
    end_vals = list(map(float, end_nums_str))
    start_array = np.array(start_vals)
    end_array = np.array(end_vals)
    interpolated_lines = []
    for i in range(1, n + 1):
        factor = i / (n + 1)
        interp_array = start_array + factor * (end_array - start_array)
        formatted_nums = [formats[col].format(interp_array[col]) for col in range(num_columns)]
        new_parts = start_parts.copy()
        for idx, col in enumerate(num_indices):
            new_parts[col] = formatted_nums[idx]
        interp_str = ''.join(new_parts)
        interpolated_lines.append(interp_str)
    
    return interpolated_lines


def update_second_column(data, start_value, step_size):
    updated_data = []
    current_value = start_value
    for line in data:
        match = re.match(r'^(\S+\s+)(\S+)(\s+.*)$', line)
        if match:
            prefix, original_number, suffix = match.groups()
            decimal_match = re.match(r'^(\d+)\.(\d+)$', original_number)
            if decimal_match:
                integer_part, decimal_part = decimal_match.groups()
                decimal_length = len(decimal_part)
                new_number = f"{current_value:.{decimal_length}f}"
            else:
                new_number = f"{current_value}"
            new_line = f"{prefix}{new_number}{suffix}"
            updated_data.append(new_line)
            current_value += step_size
        else:
            updated_data.append(line)
    
    return updated_data


def concat_gamd_log(num_gamdlog_short=10, num_remain_steps=10, gamdlog_stepsize=50000, concat_gamdlog_path='gamd_concat.log', backup_gamdlog_path='gamd_backup.log', new_gamdlog_path='gamd_backup.log'):
    total_lines = []
    with open(backup_gamdlog_path, 'r') as f:
        backup_lines = f.readlines()
        total_lines+=backup_lines
        start_line = backup_lines[-1]

    with open(new_gamdlog_path, 'r') as f:
        new_lines = f.readlines()
        end_line = new_lines[3]

    generate_lines = generate_interpolated_lines_formatted(start_line, end_line, num_gamdlog_short)
    total_lines+=generate_lines

    start_value = float(generate_lines[-1].split()[1])
    new_lines = update_second_column(new_lines, start_value, gamdlog_stepsize)
    total_lines+=new_lines[3:(4+int(num_remain_steps/gamdlog_stepsize))]
    
    with open(concat_gamdlog_path,'w') as f:
        for line in total_lines:
            f.write(line)



def write_in_connect_trajectory(file, remain_frame):
    remain_frame = int(remain_frame)
    with open(file,'w') as f:
        f.write(
f"""     
parm nowat.prmtop 
trajin nowat_pre.dcd 
trajin nowat_next.dcd 1 {remain_frame} 1
autoimage
trajout nowat.dcd 
run
quit
""")
        
frame_stepsize = 50000
num_remain_steps, num_completed_steps, num_total_steps = cmd_continuous('mdinfo_backup')
num_total_steps = 250000000
num_remain_steps = num_total_steps - num_completed_steps
num_remian_frames = np.ceil(num_remain_steps/frame_stepsize)


print(f"##################### change value of nstlim to {int(num_remian_frames*frame_stepsize)} in your_md.in ######################")

num_gamdlog_short,gamdlog_stepsize = read_gamdlog('gamd_backup.log', num_completed_steps=num_completed_steps)
concat_gamd_log(num_gamdlog_short=num_gamdlog_short, num_remain_steps=num_remain_steps, gamdlog_stepsize=gamdlog_stepsize, 
                concat_gamdlog_path='gamd_concat.log', backup_gamdlog_path='gamd_backup.log', new_gamdlog_path='gamd.log')
write_in_connect_trajectory('connect.in',num_remian_frames)
"""
cpptrak -i nowat_pre.in
cpptrak -i nowat_next.in
cpptrak -i connect.in
"""


