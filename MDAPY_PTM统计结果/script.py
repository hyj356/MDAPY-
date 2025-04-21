import mdapy as mp
import numpy as np
import glob
import time

def compute_PTM(filename:str):
  # 导入文件
  system = mp.System(filename=filename, fmt='dump')
  # 默认只识别fcc,hcp,bcc类型的原子
  system.cal_polyhedral_template_matching(structure = "fcc-hcp-bcc")
  # 获取结果
  struct_type = system.data['structure_types'].to_numpy()
  # 返回结果, 只识别fcc,hcp,bcc类型, 加上other, 一共4种晶体类型
  return np.bincount(struct_type, minlength=4)

def check(pattern:str)->list[str]:
  '''
  此函数用于检查运行参数与相关文件的状态, 并返回需要处理的文件的名称列表
  1.检查文件名是否符合规范
  2.初始化MDAPY的计算环境
  3.搜索需要进行处理的文件的名字构成的列表
  '''
  # 1.检查文件名是否符合规范
  if not '*' in pattern:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 2.初始化MDAPY的计算环境
  mp.init("cpu")
  # 3.搜索需要进行处理的文件的名字构成的列表
  file_list = glob.glob(pathname=pattern)
  # 返回结果
  return file_list

if __name__ == "__main__":
  # 定义输入文件的名称模式
  filename = './dump/dump.NPT_*.xyz'
  # 获取所有符合条件的文件名称构成的列表
  file_list = check(filename)
  # 将所有文件名映射传递给compute_PTM进行计算
  st = time.perf_counter()
  result = map(compute_PTM, file_list)
  ed = time.perf_counter()
  print(f'Map: Cost {ed-st} seconds.')
  # 将结果写入到txt文件中
  with open("Structure_count.txt", 'w') as fdata:
    fdata.write("#Frame Other FCC HCP BCC\n")
    for i, count in enumerate(result):
      fdata.write(f"{i} {count[0]} {count[1]} {count[2]} {count[3]}\n")