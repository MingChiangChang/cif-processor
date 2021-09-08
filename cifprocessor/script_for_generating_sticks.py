'''Simple example script for generating sticks.txt and names.txt'''
import glob
import os
from tqdm import tqdm
from pathlib import Path

from stick_generator import get_stick_dict_from_CIFs, write_out_sticks, resampling_sticks
from CIF_processor import simple_rename_cifs, rename_cifs


Q_range=(8,50)
home = Path.home()
dir_path = home / 'Desktop' / 'Data' / 'MnTiO-FeTiO' / 'DuncanModifiedFiles' / 'HandCurated_CIFS_MnTiO3-FeTiO3'
matsys = list(dir_path.glob('*'))
matsys = [os.path.basename(mat) for mat in matsys]

print(list(matsys))
#matsys = ['FeMnTiO', 'FeTiO', 'MnTiO3']
cif_dir_path = [dir_path / mat for mat in matsys]
full_cif_ls = []

for path in cif_dir_path:
    
    walk = os.walk(path)
    cif_ls = [] 
    for walk_obj in walk:
        cifs = glob.glob(walk_obj[0]+'/*.cif')
        if cifs:
            cif_ls += cifs 
    cif_ls = sorted(cif_ls)
    full_cif_ls += cif_ls

print(full_cif_ls)
full_cif_ls = rename_cifs(full_cif_ls)
new_ls = full_cif_ls

### If want to remove off-stoichio species, uncomment this snippet
#for cif in full_cif_ls:
#    cif_name = os.path.basename(cif)
#    if '.' not in cif_name[:cif_name.index('.cif')]:
#        new_ls.append(cif) 

#print(rename_cifs(full_cif_ls))


phase_dict = get_stick_dict_from_CIFs(new_ls)

#for key in tqdm(phase_dict, desc="Resampling sticks"):
#    phase_dict[key] = resampling_sticks(phase_dict[key], 5, Q_range, 1024, 20, 0.005)

write_out_sticks(phase_dict, dir_path, matsys[0])
