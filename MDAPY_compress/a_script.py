import mdapy as mp
import glob
import re
import os
import time

def compress_file(filename:str):
  # 创建一个新文件夹存放压缩之后的轨迹文件
  if not os.path.exists("Compressed"):
    os.makedirs("Compressed")
  # 检查文件名是否符合要求
  if not '*' in filename:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 获取符合条件的文件名列表
  file_list = glob.glob(filename)
  # 对其进行排序, 这一步其实非必须, 因为乱序执行也完全不影响
  file_list = sorted(file_list, key=extract_number)
  # 开始计时
  st = time.time()
  # 开始压缩文件
  for file in file_list:
    system = mp.System(filename=file, fmt='dump')
    system.write_dump(output_name=file.replace('./dump', './Compressed')+'.gz', compress=True)
  # 结束计时
  ed = time.time()
  print(f"It took a total of {ed-st} seconds to compress the track file.")


def extract_number(filename:str)->int:
  '''
  此函数用于从形如"./dump/dump_500.shear"中将数字500提取出来, 此外需要使用者保证文件名字中,
  最后一个数字对应的是轨迹文件的帧数
  '''
  number = re.findall(r"\d+", filename)
  return int(number[-1])

if __name__ == '__main__':
  '''
  该脚本是使用mdapy进行压缩轨迹文件的另一种写法, 但是不推荐使用该方法, 经过实测发现速度确实不如并行压缩的脚本
  并且在压缩过程中会丢失掉原子类型的信息, 即dump里面的element关键字对应的信息会丢失
  '''
  # 设置轨迹文件名模板
  filename = './dump/dump_*.shear'
  # 压缩轨迹文件
  compress_file(filename=filename)