# Generate ligand: SMILES to RDKit to ASE Atoms object

from rdkit import Chem
from rdkit.Chem import AllChem
from ase import Atoms
from ase.io import write
from typing import Tuple


def generate_ligand(smiles: str) -> Tuple[Atoms, Chem.Mol]:
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    AllChem.UFFOptimizeMolecule(mol)
    
    conformer = mol.GetConformer()
    atoms = []
    positions = []
    
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        atoms.append(symbol)
    
    for i in range(mol.GetNumAtoms()):
        pos = conformer.GetAtomPosition(i)
        positions.append([pos.x, pos.y, pos.z])
    
    atoms_obj = Atoms(atoms, positions=positions)
    filename = "".join(atoms_obj.get_chemical_symbols()) + ".xyz"
    write(filename, atoms_obj)
    
    return atoms_obj, mol
