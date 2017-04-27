import numpy as np
from numpy import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)


AvFailures3d1d = np.loadtxt('AvFailures3d1d.txt')
AvFailures3d = np.reshape(AvFailures3d1d,(60,20,9))
# (len(d_range),len(theta_range),len(c_range))
AvSomeFailures3d1d = np.loadtxt('AvSomeFailures3d1d.txt')
AvSomeFailures3d = np.reshape(AvSomeFailures3d1d,(60,20,9))
# (len(d_range),len(theta_range),len(c_range))

c_range = list(map(lambda x: x/10 , range(1,10,1)))
theta_range = list(map(lambda x: x/100 , range(80,100,1)))
d_range = list(map(lambda x: x/3 , range(1,61,1)))


plot_params_1 = {
	'type': 'of expect degree',
	'theta': 0.93,
	'c': [0.2,0.4,0.6,0.8],
	'meta': {
		# 下面可以添加任何相关信息，比如不同的文件名、保存路径，这些称为 meta data，元数据，不是用来计算的数据，作为一些函数的参数
		'picture_name': 'theta_0.93.png'
	}
}

plot_params_2 = {
	'type': 'varous level',
	'theta': [0.91,0.93,0.95,0.97],
	'c': 0.5,
	'meta': {
		# 下面可以添加任何相关信息，比如不同的文件名、保存路径，这些称为 meta data，元数据，不是用来计算的数据
		'picture_name': 'c_0.5.png'
	}
}

def plot(params,AvFailures3d,c_range,theta_range):
	if params['type'] == 'of expect degree':
		# 创建一个 n*60 的 array，每个 c 存一行;
		plot_data = np.zeros((len(params['c']),60))
		# enumerate 类可以在 for 循环中获取当前循环次数，也就是 index，从 0 开始; 开始对每个 c slice 数据
		for index,c in enumerate(params['c']):
			# 找到每个 c 在 c_range 中的 index
			index_in_c_range = c_range.index(c)
			index_in_theta = theta_range.index(params['theta'])
			plot_data[index] = AvFailures3d[:,index_in_theta,index_in_c_range]
		# 循环得到了所有的数据，下面就是对每一行进行绘图，自己弄去
		plt.style.use('ggplot') # bmh、ggplot、dark_background、fivethirtyeight、grayscale
		plt.figure(figsize=(10,5))
		plt.title("theta=0.93,n=100,不同c")
		plt.xlabel("d")
		#plt.xticks(d_range,['0.3', '2.3', '4.3', '6.3', '8.3', '10.3', '12.3', '14.3', '16.3', '18.3'],rotation=60)
		plt.ylabel("AvFailures")
		plt.yticks(np.arange(0,101,20), ['0','20','40','60','80','100'], rotation=0)
		plt.plot(d_range,plot_data[0,0:60],'-',label="c=0.2")
		plt.plot(d_range,plot_data[1,0:60],'-',color='r',label="c=0.4")
		plt.plot(d_range,plot_data[2,0:60],'-',color='y',label="c=0.6")
		plt.plot(d_range,plot_data[3,0:60],'-',color='b',label="c=0.8")
		plt.legend()
		plt.grid(True)
		plt.savefig('differentC.eps')

	elif params['type'] == 'varous level':
		plot_data = np.zeros((len(params['theta']),60))
		for index,theta in enumerate(params['theta']):
			index_in_c = c_range.index(params['c'])
			index_in_theta_range = theta_range.index(theta)
			plot_data[index] = AvFailures3d[:,index_in_theta_range,index_in_c]
		plt.style.use('ggplot') # # bmh、ggplot、dark_background、fivethirtyeight、grayscale
		plt.figure(figsize=(10,5))
		plt.title("c=0.5,n=100,不同theta")
		plt.xlabel("d")
		#plt.xticks(np.arange(0.3,21,2), ['0.3', '2.3', '4.3', '6.3', '8.3', '10.3', '12.3', '14.3', '16.3', '18.3'] ,rotation=60)
		plt.ylabel("AvFailures")
		plt.yticks(np.arange(0,101,20), ['0','20','40','60','80','100'], rotation=0)
		plt.plot(d_range,plot_data[0,0:60],'-',label="theta=0.91")
		plt.plot(d_range,plot_data[1,0:60],'-',color='r',label="theta=0.93")
		plt.plot(d_range,plot_data[2,0:60],'-',color='y',label="theta=0.95")
		plt.plot(d_range,plot_data[3,0:60],'-',color='b',label="theta=0.97")
		plt.legend()
		plt.grid(True)
		plt.savefig('differentTheta.eps')

plot(plot_params_1,AvFailures3d,c_range,theta_range)
plot(plot_params_2,AvFailures3d,c_range,theta_range)


