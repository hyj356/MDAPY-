import mdapy as mp
from mdapy.potential import EAM
from ovito.io import import_file, export_file
from ovito.data import DataCollection
import glob
import numpy as np
import time
import re
import os

def compute_virial(item_list:tuple[str, EAM, list[str]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
  single_frame, EAM_potential, element_list = item_list
  # 导入轨迹文件, 这里我使用的格式是压缩文件, 如果同学们使用的是普通的dump文件, 要记得修改
  system = mp.System(single_frame, fmt='dump.gz')
  energy, force, virial = system.cal_energy_force_virial(potential=EAM_potential, elements_list=element_list)
  return (energy, force, virial)

def add_mass(data:DataCollection):
  mass = np.zeros(len(data.particles["Particle Identifier"]))
  for i, id in enumerate(data.particles["Particle Identifier"]):
    if id == 1:
      mass[i] = 63  # Cu的质量
    else:
      mass[i] = 92  # Nb的质量
  data.particles_.create_property(name="Mass", data=mass)
  return data


if __name__ == '__main__':
  # 1.设置轨迹文件的文件名模板
  filename = './dump/relaxing_*.dump.gz'
  # 检查文件夹是否存在
  if not os.path.exists('after_calculated'):
    os.makedirs('after_calculated')
  # 初始化计算环境
  mp.init("cpu")
  # 搜索符合条件的轨迹文件
  file_list = glob.glob(filename)
  # 对搜索到的文件按照帧数进行排序
  sorted_file_list = sorted(file_list, key=lambda x: int(re.search(r'\d+', x).group()))
  # 2.设置元素的符号列表
  element_list = ['Cu', 'Zr']
  # 3.导入eam势函数文件
  EAM_potential = mp.potential.EAM('./ZrCu_lammps.eam')
  # 设置输入参数
  item_list: list[tuple[str, EAM, list[str]]] = [(file, EAM_potential, element_list) for file in file_list]
  # 收取结果
  st = time.perf_counter()
  result = map(compute_virial, item_list)
  ed = time.perf_counter()
  print(f"Cost {ed-st} seconds.")
  # 导入文件
  pipeline = import_file(location=filename, input_format='lammps/dump')
  # 将计算出来的数据通过OVITO写入dump文件中
  for i, pe_force_virial in enumerate(result):
    data = pipeline.compute(frame=i)
    data = add_mass(data=data)
    # 4.这里我们将dump文件的输出地址改为另一个文件夹
    output_filename:str = data.attributes['SourceFile'].replace('dump', 'after_calculated')
    # 将计算出来的结果写入到对应的轨迹文件中
    data.particles_.create_property(name="pe", data=pe_force_virial[0])       # 单原子势能
    export_file(data, file=output_filename, columns=list(data.particles.keys()), format="lammps/dump")
  

