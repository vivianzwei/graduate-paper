#!/usr/bin/python3 
import numpy as np
from numpy import *

n = 100 #企业的数量n设为100
iterations = 100 #因此每组参数值的迭代次数也为100

c_range = list(map(lambda x: x/10 , range(1,10,1)))
# c - 交叉持有的组织的比例。
theta_range = list(map(lambda x: x/100 , range(80,100,1)))
# theta - 组织的初始值的分数
d_range = list(map(lambda x: x/3 , range(1,61,1)))
# d - 组织的预期程度（拥有交叉拥有权的其他组织的预期数量以及持有组织的其他组织的预期数量）


AvFailures = np.empty((len(d_range),len(theta_range) * len(c_range)))
# 存储d、theta和c

AvSomeFailures = np.empty((len(d_range),len(theta_range) * len(c_range)))
# 对一些破产的迭代部分进行计数

AvFailures3d = np.empty((len(d_range),len(theta_range),len(c_range)))
AvSomeFailures3d = np.empty((len(d_range),len(theta_range),len(c_range)))
# 这些是上述数组的3维版本

c_counter = 0
# 交叉持有的组织的比例增加的计数器

for c in c_range:
	c_counter = c_counter + 1
	theta_counter = 0
	# 接下来我们遍历θ的值

	for theta in theta_range:
		theta_counter = theta_counter + 1
		d_counter = 0

		# 然后我们循环d
		for d in d_range:
			d_counter = d_counter + 1

			# 我们将此变量设置为零。对于当前参数，它们将记录至少一个组织失败的迭代次数以及所有迭代中的失败总数。
			SomeFailures = 0 #一些组织首次破产的计数器，初始值为0
			TotFailures = 0 #破产的组织数量，初始值为0

			for k in range(1, iterations + 1):
				# 生成一个具有n个顶点和期望度d的随机图，自链接被禁止;
				# 首先，我们生成一个均匀（0,1）随机变量组成的n乘n矩阵。 
				# 然后，如果相关联的随机数低于阈值，则定义阈值t并生成从i到j的链接。 
				# 最后，我们通过将对角线设置为零来删除自链接。
				# 将x从一个逻辑类型转换为数字。
				U = np.random.rand(n, n)
				t = np.divide(d, (n - 1))
				G = np.multiply(np.ones((n, n)) - np.identity(n), (U < t).astype(float))

				# 接下来我们找到能实现的G的列求和; 列求和为0的被替换为1（这样，在下一次计算中，我们不会将零除以零）
				colSumG = np.sum(G, axis=0)
				colSumG = colSumG + (colSumG == 0).astype(float)

				# 现在我们得到随机的列L - 我们使其他组织为给定的组织中的交叉持有者
				L = np.dot(G, (np.diag(np.divide(1, colSumG))))

				# 现在我们可以创建交叉矩阵。
				# 我们向外部股东提供每个组织的1-c份额，并将每个组织的剩余份额平均分配给各个持有者。
				# 这里的交叉持有矩阵不同于文章中定义的矩阵，因为它包括外部投资者持有的股票，即它对应于论文中的C +帽C.
				C = np.multiply(c, L) + np.multiply((1 - c), np.identity(n))

				# 我们现在使用在本文中导出的方程找到关联的A矩阵。这里方程的差异是由于C的定义不同。
				hatC = np.multiply(C, np.identity(n))
				A = np.dot(hatC, np.matrix(np.identity(n) - C + hatC).I)
				# 现在我们找到初始值并设置相对于这些的破产阈值。
				# 假设没有组织失败并由A * ones（n，1）给出初始值，因为每个组织持有一个值为1的单一专有资产。

				underlinev = np.multiply(np.dot(A, np.ones((n, 1))), theta)

				# 选择一个组织的资产，并将其值降为0，即破产。
				# 然后计算新的组织价值，看看是否有人破产。
				# 重复这个过程，直到没有新的组织破产。
				# 失败的组织的基础资产价值为零。 
				# 换句话说，银行成本消耗所有的标的资产价值。把银行的存款成本，如基础资产，根据A矩阵分配给组织。 
				# 我们把破产的组织的资产1的值设置为0。

				Dold = np.ones((n, 1))
				# 这是初始相关资产值的向量
				D = np.copy(Dold)
				D[0, 0] = 0
				# 将组织1的基础资产价值设置为零的

				# 下面的循环是计算最小故障集的算法
				while (1 - np.allclose(D, Dold)):
				# 继续循环，直到向量D和Dold相等，这意味着没有新的组织破产
					v = np.dot(A, D)
					# 这些是最近基础资产价值减少后的组织的当前价值
					Dold = D
					D = np.multiply(D, (v > underlinev).astype(float))
					# 对于价值已经低于失败阈值的任何组织，其底层资产值设置为零

				# 对于当前迭代，记录破产的数量
				numberOfFailures = np.sum((v <= underlinev).astype(float), axis=0)
				# 将这些值添加到当前参数值的所有迭代中到目前为止的破产总数。
				TotFailures = TotFailures + numberOfFailures
				# 记录至少有一个组织破产的迭代次数。
				SomeFailures = SomeFailures + (numberOfFailures > 0).astype(float)

			x = np.multiply((c_counter - 1) , len(theta_range)) + theta_counter
			# 每次迭代的平均破产数
			AvFailures[d_counter - 1, x - 1] = np.divide(TotFailures, iterations)
			AvFailures3d[d_counter - 1, theta_counter - 1, c_counter - 1] = np.divide(TotFailures, iterations)
			# 什么部分的迭代至少有一个失败
			AvSomeFailures[d_counter - 1, x - 1] = np.divide(SomeFailures, iterations)
			AvSomeFailures3d[d_counter - 1, theta_counter -1, c_counter - 1] = np.divide(SomeFailures, iterations)

print('len(d_range):',len(d_range)) # len(d_range):60
print('len(theta_range):',len(theta_range)) # len(theta_range):20
print('len(c_range):',len(c_range)) # len(c_range):9

np.savetxt('AvFailures.txt', AvFailures)
AvFailures3d1d = np.reshape(AvFailures3d,(1,len(d_range)*len(theta_range)*len(c_range)))
np.savetxt('AvFailures3d1d.txt', AvFailures3d1d)
np.savetxt('AvSomeFailures.txt', AvSomeFailures)
AvSomeFailures3d1d = np.reshape(AvSomeFailures3d,(1,len(d_range)*len(theta_range)*len(c_range)))
np.savetxt('AvSomeFailures3d1d.txt', AvSomeFailures3d1d)

