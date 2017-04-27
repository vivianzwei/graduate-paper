c_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
theta = [0.01,0.02,0.95,0.96]

plot_params_1 = {
	'type': 'of expect degree',
	'theta': 0.96,
	'c': [0.1,0.2,0.3,0.4],
	'meta': {
		# 下面可以添加任何相关信息，比如不同的文件名、保存路径，这些称为 meta data，元数据，不是用来计算的数据，作为一些函数的参数
		'picture_name': 'theta_0.96.png'
	}
}

plot_params_2 = {
	'type': 'varous level',
	'theta': [0.96,0.97.0.98],
	'c': 0.5,
	'meta': {
		# 下面可以添加任何相关信息，比如不同的文件名、保存路径，这些称为 meta data，元数据，不是用来计算的数据
		'picture_name': 'c_0.96.png'
	}
}

def plot(params,AvFailures3D,c_range,theta):
	if params['type'] == 'of expect degree':
		# 创建一个 n*60 的 array，每个 c 存一行;
		plot_data = np.zeros((len(params['c']),60))
		# enumerate 类可以在 for 循环中获取当前循环次数，也就是 index，从 0 开始; 开始对每个 c slice 数据
		for index,c in enumerate(params['c']):
			# 找到每个 c 在 c_range 中的 index
			index_in_c_range = c_range.index(c)
			index_in_theta = theta.index(params['theta'])
			plot_data[index] = AvFailures3D(:,index_in_theta,index_in_c_range)
		# 循环得到了所有的数据，下面就是对每一行进行绘图，自己弄去

	elif params['type'] == 'varous level':
		# 这个同样，只是把 c 和 theta 互换，自己写


plot(plot_params_1,AvFailures3D,c_range,theta)
plot(plot_params_2,AvFailures3D,c_range,theta)




