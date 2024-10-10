import os
import subprocess
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
from rdkit.Chem import AllChem,  rdMolAlign
import rdkit.Chem as Chem
from rdkit.Chem import rdFMCS
from copy import deepcopy


def convert_pdbqt_to_mol2(input_file, output_file):
    cmd = ['obabel', '-ipdbqt', input_file, '-omol2', '-O', output_file]
    subprocess.run(cmd, check=True)

def pdbqt2mol2(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdbqt") and 'best_structure_run' in filename:
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, filename.replace(".pdbqt", ".mol2"))
            convert_pdbqt_to_mol2(input_path, output_path)

def calculate_rmsd_simple(mol1, mol2):
    conf1 = mol1.GetConformer()
    conf2 = mol2.GetConformer()
    coords1 = np.array([conf1.GetAtomPosition(i) for i in range(mol1.GetNumAtoms())])
    coords2 = np.array([conf2.GetAtomPosition(i) for i in range(mol2.GetNumAtoms())])
    diff = coords1 - coords2
    rmsd = np.sqrt(np.mean(np.sum(diff**2, axis=1)))
    return rmsd

def calculate_rmsd_matrix(conformers):
    num_conformers = len(conformers)
    rmsd_matrix = np.zeros((num_conformers, num_conformers))
    for i in range(num_conformers):
        print(i)
        for j in range(i + 1, num_conformers):
            rmsd = calculate_rmsd_simple(conformers[i],conformers[j])
            rmsd_matrix[i, j] = rmsd_matrix[j, i] = rmsd
    return rmsd_matrix
    
def calculate_rmsd_matrix_mol2(name):
    conformers = [Chem.MolFromMol2File(f'MD/dock/{name}/{name}_best_structure_run_{i}.mol2', removeHs=False, sanitize=False) for i in range(1,101)]
    rmsd_mat = calculate_rmsd_matrix(conformers)
    np.savetxt(f'MD/dock/{name}_rmsd_matrix.txt',rmsd_mat)

def cluster(name):
    rmsd_mat = np.loadtxt('MD/dock/' + name + '_rmsd_matrix.txt')
    Z = linkage(squareform(rmsd_mat), method='ward')

def cluster_and_find_representative(name, cutoff=30):
    rmsd_mat = np.loadtxt('MD/dock/' + name + '_rmsd_matrix.txt')
    Z = linkage(squareform(rmsd_mat), method='single')
    new_labels = [str(int(label) + 1) for label in range(rmsd_mat.shape[0])]
    plt.figure()
    dendrogram(Z, labels=new_labels)
    plt.title('Hierarchical Clustering of Conformers')
    plt.xlabel('Conformer index')
    plt.ylabel('RMSD')
    plt.tight_layout()
    plt.savefig('MD/dock/' +f'{name}.png', dpi=600)
    plt.close()

    Z = linkage(squareform(rmsd_mat), method='single')
    clusters = fcluster(Z, cutoff, criterion='distance') 
    print(clusters)
    unique_clusters = np.unique(clusters)
    max_cluster = max(unique_clusters, key=lambda x: np.sum(clusters == x))
    indices = np.where(clusters == max_cluster)[0]
    intra_cluster_rmsd = np.sum(rmsd_mat[indices][:, indices], axis=0)
    representative_idx = indices[np.argmin(intra_cluster_rmsd)]
    print(f"Cluster {max_cluster} is the largest with representative molecule at index {representative_idx+1}.")
    return representative_idx


# pdbqt2mol2('MD/dock/Fulvestrant')
pdbqt2mol2('MD/dock/Lsavuconazonium')
# pdbqt2mol2('MD/dock/Meropenem')
# pdbqt2mol2('MD/dock/Paliperidone')

# calculate_rmsd_matrix_mol2('Fulvestrant')
calculate_rmsd_matrix_mol2('Lsavuconazonium')
# calculate_rmsd_matrix_mol2('Meropenem')
# calculate_rmsd_matrix_mol2('Paliperidone')

# cluster('Fulvestrant')
# cluster('Lsavuconazonium')
# cluster('Meropenem')
# cluster('Paliperidone')



# cluster_and_find_representative('Fulvestrant',5) #46
cluster_and_find_representative('Lsavuconazonium',5) #89
# cluster_and_find_representative('Meropenem',0.5) #13 81
# cluster_and_find_representative('Paliperidone',0.5) #73



