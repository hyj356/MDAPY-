import numpy as np
import matplotlib.pyplot as plt
import mdapy as mp
from mdapy import pltset, cm2inch
import json

def compute_eos(filename:str, lattice:str, element:str, parameter:tuple[float, float, float, float]):
  '''
  此函数用于计算单晶在各个晶格常数下的平均内聚能
  filename: eam/alloy格式的势函数文件
  lattice: 目前仅支持FCC, BCC, HCP三种晶格类型, 且默认HCP晶格中c/a = 1.63333
  parameter: 4个参数分别是缩放比例的下限, 缩放比例的上限, 相邻缩放比例之间的间隔, 和晶格常数
  '''
  # 初始化计算环境为cpu并行, 这个计算量不大, cpu并行即可解决
  mp.init('cpu')
  low, high, step = parameter[0], parameter[1], parameter[2]
  eos = []
  lattice_constant = parameter[-1]
  x, y, z = 3, 3, 3
  # 构建一个标准取向下的3x3x3的FCC单晶
  FCC = mp.LatticeMaker(lattice_constant, lattice, x, y, z) 
  FCC.compute()
  # 读取一个eam/alloy格式的势函数文件, 目前仅支持eam/alloy格式
  potential = mp.EAM(filename) 
  # 开始循环计算以获取EOS曲线上的数据
  for scale in np.arange(low, high, step): 
      energy, _, _ = potential.compute(FCC.pos*scale, FCC.box*scale, [element], np.ones(FCC.pos.shape[0], dtype=np.int32))
      eos.append([scale*lattice_constant, energy.mean()])
  # 转一下格式, 把list转成numpy的一维数组
  eos = np.array(eos)
  return eos

def plot_eos(eos_curve:np.ndarray, save_to_file:bool):
  '''
  此函数用于将计算获得的EOS数据点绘制成EOS曲线并保存,
  '''
  # 调整绘图设置
  pltset()
  fig = plt.figure(figsize=(cm2inch(10), cm2inch(7)), dpi=150)
  plt.subplots_adjust(bottom=0.18, top=0.92, left=0.2, right=0.98)
  # 绘制EOS曲线
  plt.plot(eos_curve[:,0], eos_curve[:,1], 'o-')
  # 从EOS曲线中获取最小值, 就是对应元素的内聚能
  e_coh = eos_curve[:,1].min()
  # 利用最小值的索引找到对应的晶格常数, 即为平衡晶格常数
  a_equi = eos_curve[np.argmin(eos_curve[:, 1]), 0]
  # 将EOS曲线上的最低点单独绘制出来
  plt.plot([a_equi], [e_coh], 'o', mfc='white')
  # 标题使用了Latex语法, 在两个美元符号$之间的语句即为Latex语句
  plt.title(r'$\mathregular{E_{Coh}}$ : %.2f eV, a : %.2f $\mathregular{\AA}$' % (e_coh, a_equi), fontsize=10)
  plt.xlim(eos_curve[0,0]-0.2, eos_curve[-1,0]+0.2)
  plt.xlabel("a ($\mathregular{\AA}$)")
  plt.ylabel(r"PE (eV/atom)")
  ax = plt.gca()
  # 如果要保存图片的话就导出来
  if save_to_file:
    plt.savefig('eos.png', dpi=600, bbox_inches='tight', transparent=True)
  # 展示曲线
  plt.show()

def main():
  with open("./parameter.json", 'r') as f:
    data = json.load(f)
  # 设置eam/alloy格式的势函数文件
  eam_file = data['eam_file']
  # 设置晶格类型
  lat_type = data['lattice_type']
  # 设置晶格常数
  lattice = data['lattice_constant']
  # 设置缩放范围和单步步长
  low, high, step = data['low'], data['high'], data['step']
  # 获取元素符号
  element = data["element"]
  # 获取是否需要写出文件
  save_figure = data['save_figure']
  # 计算EOS曲线上的数据点
  EOS = compute_eos(filename=eam_file, lattice=lat_type, 
                    element=element, parameter=(low, high, step, lattice))
  # 绘制EOS曲线
  plot_eos(eos_curve=EOS, save_to_file=save_figure)

if __name__ == "__main__":
  main()
  print("------------------All done!------------------")
  
