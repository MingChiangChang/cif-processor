import glob
import os

from pymatgen.io.cif import CifParser
import pymatgen.analysis.diffraction.xrd as pm_xrd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# TODO: Talk directly to ICSD database

def rename_cifs(cif_ls):
    parser_ls = get_parser(cif_ls)
    chem_ls = []
     
    for parser in parser_ls:
        chem_ls.append(''.join(take_out_blanks(list(get_comp(parser)))))
    
    unique_chem = list(set(chem_ls))
    sg_ls = [get_space_group(parser) for parser in parser_ls]
    
    matching_ls = []
    for idx, chem in enumerate(chem_ls):
        matching_ls.append(str(chem_ls[:idx].count(chem)))
    new_cif_ls = []
    for idx, cif in enumerate(cif_ls):
        dirname = os.path.dirname(cif)
        os.chdir(dirname)
        new_name = dirname+'/'+chem_ls[idx]+'_'+matching_ls[idx]+'_'+sg_ls[idx]+'.cif'
        new_cif_ls.append(new_name)
        os.rename(cif, new_name)
    return new_cif_ls

def simple_rename_cifs(cif_ls):
    for cif in cif_ls:
        mat_name = os.path.basename(cif)
        new_name = '_'.join(mat_name.split('_')[:2]) + '.cif'
        os.rename(cif, os.path.dirname(cif)+'/' + new_name)

def get_parser(cif_ls):
    return [CifParser(cif) for cif in cif_ls]

def get_comp_from_file_name(filename):
    return os.path.basename(filename)[:os.path.basename(filename).index('_')]

# TODO: Do lattice comparison
def merge_space_group(path):
    parser_ls = get_parser(path)
    cif_ls = glob.glob(path+'*.cif')
    formula_ls = get_unique_formula(path)
    
    for formula in formula_ls:
        existing_sg = []
        for i in range(len(cif_ls)):
            sg = get_space_group_number(parser_ls[i])
            if get_comp_from_file_name(cif_ls[i]) == formula and sg not in existing_sg:
                existing_sg.append(sg)
            elif get_comp_from_file_name(cif_ls[i]) == formula and sg in existing_sg:
                os.remove(cif_ls[i])
                print(cif_ls[i] + ' removed.')

def get_unique_formula(path):
    cif_ls = glob.glob(path + '*.cif')
    
    formula_ls = []
    for cif in cif_ls:
        formula_ls.append(os.path.basename(cif)[:os.path.basename(cif).index('_')])
    
    return list(set(formula_ls))

def get_comp(parser):
    ICSD_name = list(parser.as_dict())[0]
    return parser.as_dict()[ICSD_name]['_chemical_formula_structural']

def off_stoichio(chemical_formula):
    return '.' in chemical_formula

def rm_off_stoichio(cif_path):
    '''
    Run rename_cif before this
    Input is list from glob.glob function
    '''
    file_ls = glob.glob(cif_path + '*.cif')
    for file_path in file_ls:
        formula = os.path.basename(file_path)
        formula = formula[:formula.index('.cif')]
        if off_stoichio(formula):
            os.remove(cif_path + formula+'.cif')
            print(formula + ' removed.')

def get_space_group(parser):
    ICSD_name = list(parser.as_dict())[0]
    try:
        sg_str =  parser.as_dict()[ICSD_name]['_space_group_name_H-M_alt']
    except KeyError:
        return ''
    sg_ls = list(sg_str)
    if '/' in sg_ls:
        sg_ls.remove('/')
    sg_ls = (''.join(sg_ls)).split(' ')
    sg_str = ''.join(sg_ls)
    print(sg_str)
    return sg_str  

def get_space_group_number(parser):
    ICSD_name = list(parser.as_dict())[0]
    return parser.as_dict()[ICSD_name]['_space_group_IT_number']

def title_process(title):
    '''Process molecular formula into latex-like form for plotting'''
    title = list(title)
    take_out_blanks(title)
    add_dollar_sign(title)
    title = add_brackets(title)
    return ''.join(title)

def take_out_blanks(title):
    for i in title:
        if i == ' ':
            title.remove(' ')
    return title 

def remove_parentheses(title):
    for i in title:
        if i=='(' or i==')':
            title.remove(i)
    return title

def add_dollar_sign(title):
    title.insert(0, '$')
    title.append('$')
    return title

def add_brackets(title):
    odd_brackets = False
    new_title = []
    for i in range(len(title)):
        if title[i].isnumeric() and not odd_brackets:
            new_title.append('_{')
            new_title.append(title[i])
            odd_brackets = True
        elif not title[i].isnumeric() and odd_brackets:
            new_title.append('}')
            new_title.append(title[i])
            odd_brackets = False
        elif i == len(title) and odd_brackets:
            new_title.append(title[i])
            title.append('}')
        else: 
            new_title.append(title[i])
    return new_title 
