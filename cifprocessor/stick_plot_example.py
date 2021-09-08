import numpy as np
from pymatgen.io.cif import CifParser
import pymatgen.analysis.diffraction.xrd as pm_xrd
import glob
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from CIF_processor import * 

mat_sys = 'BTO'
path = '/Users/mingchiang/Desktop/Code/data/CIF/{}/CIF/'.format(mat_sys)
rename_cif(path)
cif_ls = glob.glob((path + '*.cif').format(mat_sys))
out_path = '/Users/mingchiang/Desktop/Code/data/CIF/{}/XRD/'.format(mat_sys)

Phases = dict()
for cif in cif_ls:
    parser = CifParser(cif)
    #name = get_comp(parser)
    file_name = os.path.basename(cif)
    name = file_name[:file_name.index('.cif')]
    print(name)
    try:
        structure = parser.get_structures()[0]
    except:
        print('Something wrong with {} for getting structures'.format(name))
        continue
    Phases[name] = {}
    stickpattern = pm_xrd.XRDCalculator().get_pattern(structure=structure, two_theta_range=None).as_dict()
    Q = 4*np.pi/0.15406*np.sin(np.deg2rad(stickpattern['x']/2))
    I = stickpattern['y']/max(stickpattern['y'])


    Phases[name]['Qs'] = Q[Q<45]
    Phases[name]['Is'] = I[Q<45]
    color = ['rebeccapurple','forestgreen','goldenrod','fuchsia','dodgerblue','c','crimson','chartreuse']
    patches = []
for kdx, name in enumerate(list(Phases)):
    #patches.append(mpatches.Patch(color=color[kdx],label=name+' line '+str(kdx)))
    #plotting sticks
    for jdx in np.arange(len(Phases[name]['Qs'])):
#       print(jdx,val)
        q = Phases[name]['Qs'][jdx]
        i = np.log10(Phases[name]['Is'][jdx]+1)
        plt.plot([q,q],[i,0],c='r',label = name+' line '+str(jdx),linewidth=2,alpha=0.6)
        #adds a legend to the stickpatterns showing which phases are which
    try:
        plt.title(title_process(name[:list(name).index('_')]))
        plt.xlim([8,45])
        plt.xlabel('$Q (nm^{-1})$')
        plt.ylabel('Relative Intensity (a.u.)')
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        plt.savefig(fname=out_path+name+'.png')
        #plt.show()
        plt.clf()
    except:
        print('Something wrong with {}'.format(name))
