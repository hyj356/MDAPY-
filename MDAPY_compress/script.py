import mdapy as mda
import os
import multiprocessing as mul
import time

def compress_dump_file(filename:str, step:int, frames:int, thread:int):
  # 创建一个新文件夹存放压缩之后的轨迹文件
  if not os.path.exists("Compressed"):
    os.makedirs("Compressed")
  # 检查文件名是否符合要求
  if not '*' in filename:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 构建文件名列表
  file_list = [filename.replace('*', str(i*step)) for i in range(frames)]
  # 构建输出文件名列表, 确保输出的压缩文件在我们新建立的文件夹里面
  output_file_list = [file.replace('./dump', './Compressed')+'.gz' for file in file_list]
  # 初始化mda的计算环境
  mda.init('cpu')
  # 开始压缩
  for file, output_file in zip(file_list, output_file_list):
    # 如果不想要原来的轨迹文件, 可以在下面的函数调用中加入一个inplace=True, 这样新生成的
    # 压缩轨迹文件就可以替代掉对应的轨迹文件了
    mda.pigz.compress_file(source_file=file, output_file=output_file,
                            compresslevel=9, workers=thread)
  
  

if __name__ == "__main__":
  filename:str = './dump/dump_*.shear'  # 轨迹文件的文件名模板
  step:int = 500  # 相邻两帧轨迹文件间隔500步
  frames:int = 41 # 一共有多少帧文件
  threads:int = mul.cpu_count()
  print(f"There are total {threads} threads in your computer.")
  st = time.time()
  compress_dump_file(filename=filename, step=step, frames=frames, thread=threads)
  ed = time.time()
  print(f"It took a total of {ed-st} seconds to compress the track file.")