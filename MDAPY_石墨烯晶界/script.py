import mdapy as mp
import numpy as np
mp.init("cpu")
box = np.array([[0.0, 200.0], [0.0, 200.0], [0.0, 200.0]]) # Generate a box.
polycry = mp.CreatePolycrystalline(
              box, 20, 3.615, "FCC", add_graphene=True, randomseed=16516,
              output_name="graphene_poly.lmp") # Initilize a Poly class.
polycry.compute() # Generate a graphene/metal structure with 20 grains.