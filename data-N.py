#!/usr/bin/python3 
import numpy as np
from numpy import *
from pprint import pprint

theta_range = list(map(lambda x: x/100 , range(80,100,1)))
n = 6
# GDP (亿美元)    France  Germany Greece	 Italy	Netherlands	  UK
gdp_08 = matrix([[29235],[37469],[3546],[23919],[9313],[27917]])
gdp_16 = matrix([[24883],[34949],[1960],[18525],[7699],[26500]])

names = array(['France','Germany','Greece','Italy','Netherlands','UK'])

normalizing_value = gdp_16[2]
gdp_08_normalized = gdp_08/normalizing_value
gdp_16_normalized = gdp_16/normalizing_value

fraction_gdp_loss = np.divide((gdp_08-gdp_16),gdp_08)

x = matrix([0,171757,684,43231,91963,144499,157155,0,1854,182129,164576,154957,1637,25785,0,584,1207,4652,294355,86722,223,0,28539,27705,104547,118119,180,18857,0,127375,220532,389793,9698,46473,98610,0])
C_raw_transposed = np.reshape(x,(6,6))

C_raw = np.transpose(C_raw_transposed)

c = 0.33
colsumC_raw = np.sum(C_raw, axis=0)
C = np.dot(np.dot(c,C_raw),np.diagflat(np.divide(1,colsumC_raw)))

Chat = np.dot((1-c),np.identity(n))

A = np.dot(Chat,np.matrix(np.identity(n) - C).I)

p = gdp_16_normalized

for theta in theta_range:
	v_threshold = np.dot(theta,np.dot(A,gdp_08_normalized))

	pcurrent = np.copy(p)

	wave = 0
	all_failure_indicator = np.zeros((n,1))

	while (wave == 0) or (1-((new_failed_countries).size == 0)):
		wave = wave + 1
		new_failure_indicator = np.multiply((np.dot(A,pcurrent) < v_threshold).astype(float),(all_failure_indicator == 0).astype(float))
		all_failure_indicator = np.maximum(all_failure_indicator,new_failure_indicator)
		pcurrent = pcurrent - np.divide(np.multiply(new_failure_indicator,v_threshold),2)
		new_failed_countries = np.where(new_failure_indicator == 1)[0]
		new_failed_names = names[new_failed_countries]

		if (1-np.all(new_failed_countries == 0)):
			print('Theta:',str(theta),'Wave', str(wave),'failures are: ')
			pprint(new_failed_names.tolist())

