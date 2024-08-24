from rdkit import Chem
from rdkit.Chem import AllChem

def smiles2mol2(smiles="[H]C(C)(OC(=O)N(C)C1=C(COC(=O)CNC)C=CC=N1)[N+]1=CN(C[C@](O)(C2=C(F)C=CC(F)=C2)[C@@]([H])(C)C2=NC(=CS2)C2=CC=C(C=C2)C#N)N=C1",
                savename='Lsavuconazonium'):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol)
    w = Chem.SDWriter(f'{savename}.mol')
    w.write(mol)
    w.close()

#https://go.drugbank.com/drugs/DB06636
smiles2mol2(smiles="[H]C(C)(OC(=O)N(C)C1=C(COC(=O)CNC)C=CC=N1)[N+]1=CN(C[C@](O)(C2=C(F)C=CC(F)=C2)[C@@]([H])(C)C2=NC(=CS2)C2=CC=C(C=C2)C#N)N=C1", 
            savename='Lsavuconazonium')
#https://go.drugbank.com/drugs/DB01267
smiles2mol2(smiles="CC1=C(CCN2CCC(CC2)C2=NOC3=C2C=CC(F)=C3)C(=O)N2CCCC(O)C2=N1",
            savename='Paliperidone')
#https://go.drugbank.com/drugs/DB00947
smiles2mol2(smiles='[H][C@@]12CC[C@H](O)[C@@]1(C)CC[C@]1([H])C3=CC=C(O)C=C3C[C@@H](CCCCCCCCCS(=O)CCCC(F)(F)C(F)(F)F)[C@@]21[H]',
            savename='Fulvestrant')
#https://go.drugbank.com/drugs/DB00760
smiles2mol2(smiles='[H][C@]1([C@@H](C)O)C(=O)N2C(C(O)=O)=C(S[C@@H]3CN[C@@H](C3)C(=O)N(C)C)[C@H](C)[C@]12[H]',
            savename='Meropenem')




