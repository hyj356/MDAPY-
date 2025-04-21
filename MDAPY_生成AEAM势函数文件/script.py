import mdapy as mp
mp.init('cpu')
mp.EAMAverage(filename="NiCoCr.lammps.eam", 
                          concentration=[1/3, 1/3, 1/3],
                          output_name="NiCoCr.lammps.AEAM") # Generate the EAMAverage class.
mp.EAMAverage(filename="AlCu.eam.alloy", 
                          concentration=[0.5, 0.5],
                          output_name="AlCu.aeam.alloy") # Generate the EAMAverage class.