import os
from rdkit import Chem
from rdkit.Chem import AllChem


def gaussianLog2xyz(logfile, xyzfile):
    with open(logfile, 'r') as file:
        lines = file.readlines()
    atoms = []
    start_reading_coord = False
    start_reading_atom = False
    for line in lines:
        if 'Mulliken charges:' in line:
            if atoms:
                continue
            start_reading_atom = True
            atoms = []
        if 'Sum of Mulliken charges' in line:
            start_reading_atom = False
        if start_reading_atom:
            if len(line.split()) > 2:
                atoms.append(line.split()[1].strip())

        
        if 'Standard orientation:' in line:
            start_reading_coord = True
            coords = [] 
        if 'Rotational constants' in line:
            start_reading_coord=False
        if start_reading_coord:
            if '---------------------------------------------------------------------' in line:
                if coords: 
                    continue
            parts = line.split()
            if len(parts) == 6 and parts[0].isdigit():
                x, y, z = parts[3], parts[4], parts[5]
                x = f"{float(x):15.5f}"
                y = f"{float(y):15.5f}"
                z = f"{float(z):15.5f}"
                coords.append(f"{x}{y}{z}")
                
    with open(xyzfile, 'w') as file:
        file.write(f"{len(atoms)}\n")
        file.write("Generated from Gaussian log file\n")
        lines = [atoms[i]+'  '+coords[i] for i in range(len(atoms))]
        file.write("\n".join(lines))

def mol2gjf_by_obabel(obabel_path, g16_path, gaussian_dir, task_name, mem, nproc,):
    input_mol2_path = gaussian_dir+'/'+task_name+'.mol2'
    output_gjf_path = gaussian_dir+'/'+task_name+'.gjf'
    os.system(f'{obabel_path} {input_mol2_path} -O {output_gjf_path}')
    # mol = Chem.MolFromMol2File(input_mol2_path)
    # formal_charge = Chem.GetFormalCharge(mol)
    with open(output_gjf_path, 'r') as f:
        lines = f.readlines()
        lines = lines[5:]
    with open(output_gjf_path, 'w') as f:
        f.write(f'%chk={gaussian_dir}/{task_name}.chk\n%mem={mem}\n%nprocshared={nproc}\nopt B3LYP/6-31G(d) freq\n\n{task_name}\n\n')
        for line in lines:
            f.write(line)

def run_gaussian(obabel_path, g16_path, gaussian_dir, task_name):
    input_gjf_path = gaussian_dir+'/'+task_name+'.gjf'
    output_log_path = gaussian_dir+'/'+task_name+'.log'
    out_mol2_path = gaussian_dir+'/'+task_name+'_opt.mol2'

    os.system(f'f{g16_path} <{input_gjf_path} >{output_log_path}')
    output_xyz_path = gaussian_dir+'/'+task_name+'_opt.xyz'
    gaussianLog2xyz(output_log_path, output_xyz_path)
    os.system(f'f{obabel_path} -ixyz {output_xyz_path} -omol2 -O {out_mol2_path}')


