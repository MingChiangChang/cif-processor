''' Testing script '''
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import gaussian
import os
import glob
from tqdm import tqdm

from gaussian_mix_fit import gaussian_mix_fit
from peak_fitting import peak_fitting
from stick_generator import get_stick_dict_from_CIFs, resampling_sticks, write_out_sticks
from visualize import visualize_Q

#test_data = np.zeros(1000)
#DATA_WIDTH = 300
#intensity = (1, 0.4, 0.3)
#position = (200, 450, 780)
#
#peak = gaussian(DATA_WIDTH, std=20)
#w = int(DATA_WIDTH/2)
#for i, p in zip(intensity, position):
#    test_data[p-w:p+w] += i*peak
#plt.plot(test_data)
#plt.show()
#peak_ls = peak_fitting(test_data, max_peak=3,
#                       min_improv=0.1)
#print(peak_ls)
# unittest: assertTrue(norm(fitted_intenisty-intensity)/len(intensity)<0.01)

cif_dir_path = '/home/ming-chiang/Desktop/Code/CIF_processor/data/BTO/'

walk = os.walk(cif_dir_path)

cif_ls = []

for walk_obj in walk:
    cifs = glob.glob(walk_obj[0]+'/*.cif')
    if cifs:
        cif_ls += cifs

print(cif_ls)

#simple_rename_cifs(cif_ls)
Q_range = (8, 65)

phase_dict = get_stick_dict_from_CIFs(cif_ls)

for key in tqdm(phase_dict, desc="Resampling sticks"):
#    visualize_Q(phase_dict[key]['Qs'], phase_dict[key]['Is'], Q_range, title=f'{key} before')
    phase_dict[key] = resampling_sticks(phase_dict[key], 5, Q_range, 1024, 20, 0.005)
#    visualize_Q(phase_dict[key]['Qs'], phase_dict[key]['Is'], Q_range, title=f'{key} after')

write_out_sticks(phase_dict, cif_dir_path)
