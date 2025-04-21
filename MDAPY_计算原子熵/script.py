import mdapy as mp
import os
import glob
import time

def compute_entropy(filename:str):
  # 导入文件
  system = mp.System(filename=filename,fmt='dump')
  # 设置截断半径为5.0, σ为0.2, 单原子最大邻居数为80
  system.cal_atomic_entropy(rc=5.0, sigma=0.2, max_neigh=80)
  # 设置输出文件的名称
  output_file = filename.replace('./dump', './After_cal_entropy')
  # 输出文件
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
  if not os.path.isdir('./After_cal_entropy'):
    os.mkdir('./After_cal_entropy')
  # 3.初始化MDAPY的计算环境
  mp.init("cpu")
  # 4.搜索需要进行处理的文件的名字构成的列表
  file_list = glob.glob(pathname=pattern)
  # 返回结果
  return file_list

if __name__ == "__main__":
  # 定义输入文件的名称模式
  filename = './dump/dump.NPT_*.xyz'
  # 获取所有符合条件的文件名称构成的列表
  file_list = check(filename)
  # 调用for循环逐一处理
  # st = time.perf_counter()
  # for file in file_list:
  #   compute_entropy(file)
  # ed = time.perf_counter()
  # print(f'For loop: Cost {ed-st} seconds.')
  # 调用Map进行统一计算处理
  st = time.perf_counter()
  list(map(compute_entropy, file_list))
  ed = time.perf_counter()
  print(f'Map: Cost {ed-st} seconds.')
  # 如果在上述代码中, 先使用for循环进行统一处理, 在调用map, 那么就是map执行的更快
  # 反之, 就是for循环执行的更快
  

