import MDAnalysis as mda
from MDAnalysis.analysis.distances import distance_array
import numpy as np


u = mda.Universe('nvt.tpr', 'trj2.xtc')


index_A = 0  
index_B = 10  
atom_A = u.atoms[index_A]
atom_B = u.atoms[index_B]


times = []
distances = []


for ts in u.trajectory:

    time = ts.time

    pos_A = atom_A.position
    pos_B = atom_B.position

    distance = distance_array(pos_A, pos_B, box=u.dimensions)[0][0]

    times.append(time)
    distances.append(distance)


with open('atom_distances.txt', 'w') as f:
    for time, distance in zip(times, distances):
        f.write(f"{time} {distance}\n")

