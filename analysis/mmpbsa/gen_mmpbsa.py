from pymol import cmd

def get_nearby_residues(pdb_file, output_file='mmpbsa.in', num_residues=728, ligand_resi='729', distance=8.0):
    # Load the PDB file
    cmd.load(pdb_file)
    
    # Select nearby residues around the ligand
    selection_name = "nearby_residues"
    cmd.select(selection_name, f"byres (resi {ligand_resi} around {distance}) and not resi {ligand_resi}")
    
    # Get the residue IDs of the nearby residues
    residues = []
    cmd.iterate(selection_name, "residues.append(resi)", space={'residues': residues})
    
    # Remove duplicates and sort the residues
    residues = sorted(int(i) for i in set(residues))
    residues = [str(i) for i in residues]
    print(residues)
    # Write the residues to a text file in one line
    nearby_residues=",".join(residues)
    with open(output_file, 'w') as f:
        f.write(
f"""&general             
    startframe=1, endframe=5000, interval=10,
    verbose = 1,
    ligand_mask = \':{ligand_resi}\',
    receptor_mask = \':1-{num_residues}\',
/    
&pb             
    inp=0, radiopt=0, 
    istrng=0.15,
/          
&decomp         
    idecomp=1,
    print_res=\'{nearby_residues}\',
    dec_verbose=1,
/\n""")
    
    print(f"Residue numbers saved to {output_file}")

# Example usage
get_nearby_residues(pdb_file="com_dry.pdb", output_file='mmpbsa.in', ligand_resi='729', distance=8.0)
"""
ante-MMPBSA.py -p com_solv.prmtop -c com.prmtop -r rec.prmtop -l lig.prmtop -s ':WAT,Na+,Cl-' -n ':729'
nohup MMPBSA.py -O -i mmpbsa.in -o MMPBSA.dat -sp com_solv.prmtop -cp com.prmtop -rp rec.prmtop -lp lig.prmtop -y ligamd_md.dcd &
"""

