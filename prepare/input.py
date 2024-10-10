from rdkit import Chem
from rdkit.Chem import AllChem

def smiles2mol2_MMFF(smiles="",
                save_path=''):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol)
    w = Chem.SDWriter(save_path)
    w.write(mol)
    w.close()




