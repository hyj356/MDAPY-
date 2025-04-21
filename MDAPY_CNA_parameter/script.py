import mdapy as mp
import os
import glob
import time

def compute_CNP(filename:str):
  '''
  此函数用于计算并导出单帧轨迹中的单原子的CNP(Common_Neighbor_Parameter), 在一些典型的晶体结构中
  FCC : 0.0
  BCC : 0.0
  HCP : 4.4
  FCC (111) surface : 13.0
  FCC (100) surface : 26.5
  FCC dislocation core : 11.
  Isolated atom : 1000. (由mdapy赋予的默认数值)
  此外, 关于计算CNP需要提供的截断半径, 可以根据输入晶体按照如下公式进行计算, 设晶格常数为a:
  r_fcc: = 0.8536*a
  r_bcc: = 1.207*a
  设hcp的晶格常数为a和c, 且x = (c/a)/1.633
  r_hcp = 0.5*(1+sqrt((4+2*x**2)/3))*a
  '''
  # 导入文件
  system = mp.System(filename=filename, fmt='dump')
  # 输入晶体为Cu, 晶格常数为3.615, 晶体类型为FCC
  system.cal_common_neighbor_parameter(rc=0.8536*3.615)
  # 将结果文件写出到新的文件夹中
  output_file = filename.replace('./dump', './After_cal_CNP')
  # 导出结果
  system.write_dump(output_name=output_file)

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
  if not os.path.isdir('./After_cal_CNP'):
    os.mkdir('./After_cal_CNP')
  # 3.初始化MDAPY的计算环境
  mp.init("cpu")
  # 4.搜索需要进行处理的文件的名字构成的列表
  file_list = glob.glob(pathname=pattern)
  # 返回结果
  return file_list

if __name__ == "__main__":
  '''
  CNP参数对应的参考文献: https://doi.org/10.1016/j.cpc.2007.05.018, 
  <<Structural characterization of deformed crystals by analysis of common atomic neighborhood>>
  '''
  # 定义输入文件的名称模式
  filename = './dump/dump.NPT_*.xyz'
  # 获取所有符合条件的文件名称构成的列表
  file_list = check(filename)
  # 将所有文件名映射传递给compute_PTM进行计算
  st = time.perf_counter()
  list(map(compute_CNP, file_list))
  ed = time.perf_counter()
  print(f'Map: Cost {ed-st} seconds.')