'''Functions to visualize sticks'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def visualize_Q(Qs, Is, Q_range, title=None, save=False, path=None):
    fig, axs = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(15)
    axs.scatter(Qs, Is, c='none', s=0.5)
    for Q, I in zip(Qs, Is):
        rect = mpatches.Rectangle((Q,0), 0.2, I, linewidth=6, edgecolor='r',
                                   facecolor='r', alpha=0.5)
        axs.add_patch(rect)
    plt.xlim(Q_range[0], Q_range[1])
    plt.ylim(0,1)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.xlabel('Q ($nm^{-1}$)', fontsize=24)
    plt.ylabel('Relative Intensity', fontsize=24)
    if title is not None:
        plt.title(title, fontsize=24)
    plt.tight_layout()
    if save:
        plt.savefig(path + title + '.png')
    else:
        plt.show()


if __name__ == '__main__':
    mat = 'BTO' 
    path = f'/home/mingchiang/Desktop/Data/MnTiO-FeTiO/DuncanModifiedFiles/MnFeTiO3_all/'
    with open(path + 'sticks.txt','r') as f:
        sticks = f.read().split('\n')
    with open(path + 'names.txt', 'r') as f:
        names = f.read().split('\n')
    sticks.remove('')
    names.remove('')
    for name in names:
        name = name[name.index('=')+1:]
    Qs = []
    Is = []
    for idx, stick in enumerate(sticks):
        stick = stick[stick.index('=')+1:]
        if idx%2 == 0:
            Qs.append([float(s) for s in stick.split(',')])
        else:
            Is.append([float(s) for s in stick.split(',')])
    for Q, I, name in zip(Qs, Is, names):
        visualize_Q(Q, I, (9, 65), name[name.index('=')+1:], save=True, path=path)
