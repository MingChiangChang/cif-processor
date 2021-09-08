import glob

from pymatgen.io.cif import CifParser

from CIF_processor import get_unique_formula

def main():
    return

def merge_cifs(paths, remove_path):
    chem_formulas = get_unique_formula(paths)
    for chem in chem_formulas:
        cifs = get_cifs_with_chem(chem)
        to_be_removed = []
        while(cifs):
            c = cifs.pop()
            for cif in cifs:
                if is_the_same_cif(c, cif):
                    to_be_removed.append(cif)
        move_to(to_be_removed, remove_path)

def get_cif_with_chem(chem):
    """
    Return cif files that fits the specified molecular formaula
    """
    return

def is_the_same_cif(ref_cif, cif):
    """
    Simplest implementation: 
    1. Same chemical formula and same space group means cifs are the same
    2. Fallback: If no space group information conpare lattice parameter 
    """

    if get_space_group(ref_cif) == get_space_group(cif):
        return True
    elif get_lattice_param(ref_cif)

    return

def move_to(to_be_removed, remove_path):
    if mot os.isdir(remove_path):
        os.mkdir(remove_path)
    for f in to_be_removed:
        os.rename(f, remove_path + os.path.basename(f))


if __name__ == '__main__':
    main() 
