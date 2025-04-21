import mdapy as mp
import os
import multiprocessing as mul
import time
import glob

def compress_dump_file(filename:str):
  # 构建输出文件名, 确保输出的压缩文件在我们新建立的文件夹里面
  output_file:str = filename.replace('./dump', './Compressed')+'.gz' 
  # 如果不想要原来的轨迹文件, 可以在下面的函数调用中加入一个inplace=True, 这样新生成的
  # 压缩轨迹文件就可以替代掉对应的轨迹文件了
  mp.pigz.compress_file(source_file=filename, output_file=output_file,
                          compresslevel=9, workers=1)
  
def check(pattern:str):
  '''
  此函数用于开始mdapy计算前的准备和检查工作
  1.创建一个新文件夹存放压缩之后的轨迹文件
  2.检查文件名是否符合要求
  3.初始化mdapy计算的环境
  4.获取需要进行压缩的文件名列表
  '''
  # 1.创建一个新文件夹存放压缩之后的轨迹文件
  if not os.path.exists("Compressed"):
    os.makedirs("Compressed")
  # 2.检查文件名是否符合要求
  if not '*' in pattern:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 3.初始化mdapy计算的环境
  mp.init('cpu')
  # 4.获取需要进行压缩的文件名列表
  file_list = glob.glob(pathname=pattern)
  # 返回结果
  return file_list

if __name__ == "__main__":
  filename:str = './dump/dump_*.shear'  # 轨迹文件的文件名模板
  file_list = check(pattern=filename)   # 获取需要进行处理的dump文件的名称
  threads:int = mul.cpu_count()         # 获取当前CPU的最大线程数量
  print(f"There are total {threads} threads in your computer.")
  # 开始计算并进行压缩文件
  st = time.time()
  # 这里只使用一半的CPU核数进行并行, 因为计算量本身就不大, 核数太多反而会拖慢速度
  with mul.Pool(processes=threads//2) as pool:
    pool.map(compress_dump_file, file_list)
  ed = time.time()
  print(f"It took a total of {ed-st} seconds to compress the track file.")