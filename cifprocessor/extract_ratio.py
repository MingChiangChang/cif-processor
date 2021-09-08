import glob
from pymatgen.io.cif import CifParser
import os 
from CIF_processor import get_comp, get_space_group
import numpy as np
from collections import OrderedDict

compounds = OrderedDict()

elements = ['Ti', 'O']
mat_sys = ''.join(elements)
path = '/home/ming-chiang/Desktop/Code/CIF_processor/data/{}/CIF/'.format(mat_sys)

cif_ls = glob.glob('/home/ming-chiang/Desktop/Code/CIF_processor/data/{}/CIF/*.cif'.format(mat_sys))

stoichio = np.zeros((len(cif_ls), len(elements)))
mol_names = []
space_group_num = []
for i in range(len(cif_ls)):
    parser = CifParser(cif_ls[i])
    file_name = os.path.basename(cif_ls[i])
    name = get_comp(parser)
    full_name = file_name[:file_name.index('.cif')]
    compound = {}
    compound['name'] = full_name 
    #space_group_num.append(get_space_group(parser))
    compound['space_group'] = get_space_group(parser)
    #mol_names.append(name)
    name = list(name)
    name.append(' ')
    name = ''.join(name)
    try:
        structure = parser.get_structures()[0]
    except:
        print('Something wrong with {} for getting structures'.format(name))
        continue


    try:
        for j in range(len(elements)):
            if j != len(elements)-1:
                num = name[name.index(elements[j])+len(elements[j]):name.index(elements[j+1])]
                if num.isspace() :
                    #stoichio[i][j]=1
                    compound[elements[j]]=1
                else:
                    #stoichio[i][j]=float(num)
                    compound[elements[j]]=float(num)
            else:
                num = name[name.index(elements[j])+len(elements[j]):]
                if num == ' ' or num =='\n' or None:
                    #stoichio[i][j]=1
                    compound[elements[j]]=1
                else:
                    #stoichio[i][j]=float(num)
                    compound[elements[j]]=float(num)
        name = get_comp(parser)
        compound['id'] = i
        compounds[full_name] = compound
        mol_names.append(full_name)
    except:
        print('There is error prcoessing {} stoichiometric ratio'.format(name))
    
# Selecting condition
indep_id = []
for i in range(len(mol_names)):
    #if stoichio[i][1] == 2*stoichio[i][0]-1 and stoichio[i][0]>1:
    #    print(mol_names[i], stoichio[i], space_group_num[i])
    name = mol_names[i]
    if compounds[name]['O']== 2*compounds[name]['Ti']-1 and compounds[name]['Ti']>1:
        print(compounds[name], compounds[name]['space_group'])
        indep_id.append(compounds[name]['id'])

print(len(indep_id))


