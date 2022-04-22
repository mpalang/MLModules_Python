# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 09:29:24 2022

@author: work
"""

import numpy as np

# data= np.loadtxt(r'C:\Users\work\Messdaten\U21_TA\20220421_Berkefeld\08_perp_rot\raw\08_Co_c3_perp_rot_transient_fc_avg_cc_cut.dat'.replace('\\','/'))
data= np.loadtxt(r'C:\Users\work\Messdaten\U21_TA\20220421_Berkefeld\07_parallel_rot\raw\07_Co_c3_parallel_rot_transient_fc_avg_cc_cut.dat'.replace('\\','/'))

# data_c=data[59:,1:]

# data_c=np.column_stack((data[59:,0],data_c))

# data_c=np.vstack((data[0,:],data_c))

data_c = data
data_c[1:,1:] = data_c[1:,1:]*(-1)

np.savetxt(r'C:\Users\work\Messdaten\U21_TA\20220421_Berkefeld\07_parallel_rot\raw\07_Co_c3_parallel_rot_transient_fc_avg_cc_cut.dat'.replace('\\','/'), data_c, delimiter='\t', fmt='%1.8f')
# 