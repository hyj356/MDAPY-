import mdapy as mp
import numpy as np
import glob
import time
import os

def statistical_surface_defects(filename:str):
  '''
  调用MDAPY模块中的识别面缺陷算法统计ISF, ESF, TB原子的数量, 在该算法中
  0 = Non-hcp atoms (e.g. perfect fcc or disordered)
  1 = Indeterminate hcp-like (isolated hcp-like atoms, not forming a planar defect)
  2 = Intrinsic stacking fault (two adjacent hcp-like layers)
  3 = Coherent twin boundary (one hcp-like layer)
  4 = Multi-layer stacking fault (three or more adjacent hcp-like layers)
  5 = Extrinsic stacking fault
  经过处理之后的dump文件会多出一列名为'fault_types'的原子属性, 按照如上的列表查询并在ovito中
  进行适当处理即可可视化模型变形过程中出现的面缺陷
  '''
  # 导入读取dump文件
  system = mp.System(filename=filename, fmt='dump')
  # 识别面缺陷, 注意此函数基于ptm算法, 因此需要设置rmsd的阈值
  # 但是对于绝大多数情况来说, 默认阈值0.1已经足够
  system.cal_identify_SFs_TBs()
  # 获取结果
  fault_type = system.data['fault_types'].to_numpy()
  # 调用bincount可以及其方便的统计各种原子的数量
  count_of_fault = np.bincount(fault_type, minlength=6)
  # 定义输出文件的名字, 其实就是换一个文件夹
  if write_to_file:
    output_file = filename.replace('./dump', "./After_cal_planar-defect")
    # 将结果文件导出
    system.write_dump(output_name=output_file)
  return count_of_fault

def check(pattern:str)->list[str]:
  '''
  此函数用于检查运行参数与相关文件的状态, 并返回需要处理的文件的名称列表
  1.检查文件名是否符合规范
  2.创建文件夹存放计算完成之后的轨迹文件
  3.初始化MDAPY的计算环境
  4.搜索需要进行处理的文件的名字构成的列表
  '''
  # 1.检查文件名是否符合规范
  if not '*' in pattern:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 2.创建文件夹存放计算完成之后的轨迹文件
  if write_to_file:
    if not os.path.isdir('./After_cal_planar-defect'):
      os.mkdir('./After_cal_planar-defect')
  # 3.初始化MDAPY的计算环境
  mp.init("cpu")
  # 4.搜索需要进行处理的文件的名字构成的列表
  file_list = glob.glob(pathname=pattern)
  # 返回结果
  return file_list

if __name__ == "__main__":
  global write_to_file
  # 设置dump文件名字的模板
  filename = './dump/dump_*.shear'
  # 设置为False的话, 就不会写出新的dump文件, 仅对面缺陷原子数量进行统计
  write_to_file:bool = True
  # 获取轨迹文件名列表
  file_list = check(pattern=filename)
  # 将参数传入给statistical_surface_defects函数
  st = time.perf_counter()
  result = map(statistical_surface_defects, file_list)
  ed = time.perf_counter()
  print(f'Map function: Cost {ed-st} seconds.')
  # 将结果写入到txt文件中
  with open("Fault_count.txt", 'w') as fdata:
    fdata.write("#Frame Non-hcp isolated-hcp-like ISF Coherent_TB Multi-layer_SF ESF\n")
    for i, count in enumerate(result):
      fdata.write(f"{i} {count[0]} {count[1]} {count[2]} {count[3]} {count[4]} {count[5]}\n")