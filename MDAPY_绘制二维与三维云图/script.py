import mdapy as mp

# 注意必须要显式的指明运行平台, 否则会报错
mp.init('cpu')
# 导入文件
system = mp.System(filename='./relaxing_50000.dump.gz',fmt='dump.gz')
# 查看文件中存在哪些粒子属性
# print(system.data.columns)
# 将单原子势能进行二维空间的平均化, 建议截断半径至少大于一个晶格常数
system.spatial_binning(direction='xy', vbin='c_pe',wbin=4.0,operation='mean')
fig, ax = system.Binning.plot(value_label='Average_potential_energy')
# 查看二维数组坐标
# print(system.Binning.coor)
# 保存图片
fig.savefig("Two_dimension.png", dpi=600)
# 将单原子势能进行二维空间的平均化
system.spatial_binning(direction='xyz', vbin='c_pe',wbin=4.0,operation='mean')
fig, ax = system.Binning.plot(value_label='Average_potential_energy')
# 查看三维数组坐标
print(system.Binning.coor)
# 保存图片
fig.savefig("Three_dimension.png", dpi=600)