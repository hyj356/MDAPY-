import mdapy as mp

if __name__ == "__main__":
  mp.init("cpu")
  system = mp.System(filename="./CoCuFeNiPd-4M.txt", fmt='lmp')
  # 设置截断半径和最大邻居数量, CoCuFeNiPd高熵合金的晶格常数为3.6埃
  # 这里需要乘以一个系数, 系数的选择详见文件夹内的png文件
  system.cal_warren_cowley_parameter(rc=0.8536*3.6, max_neigh=30)
  # 指明当前data文件中的几种原子的元素类型
  fig, ax = system.WarrenCowleyParameter.plot(['Co', 'Cu', 'Fe', 'Ni', 'Pd'])
  # 保存图片
  fig.savefig("WCP.png", dpi=600)