'''
Created on May 14, 2020

@author: eker
'''
from ema_workbench import (TimeSeriesOutcome, 
                           perform_experiments,
                           RealParameter, 
                           CategoricalParameter,
                           ema_logging, 
                           save_results,
                          load_results)
import ema_workbench.analysis.prim as prim
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#ema_logging.log_to_stderr()

results = load_results('../results/EW_explore_Managerial_vNPP_2.tar.gz')
exp, out = results
logical_index = [exp['Transition Scenario Switch'] == 2]
x = exp[logical_index]
print(x.shape)
data = out['Temperature Change from Preindustrial'][logical_index]

#ref_results = ref_experiments, ref_outcomes
y = data[:,-100]<=1.5
print(y.shape)
print(y.sum())
#prim_obj = prim.setup_prim(ref_results, classify, threshold=0.8, threshold_type=1)
prim_obj = prim.Prim(x, y, threshold=0.8)
box_1 = prim_obj.find_box()
sns.set_style("white")
box_1.show_tradeoff()
plt.savefig('../results/prim_tradeoff.png', dpi=300, bbox_inches='tight')
box_1.inspect(11, 'graph')
plt.savefig('../results/prim_box11.png', dpi=300, bbox_inches='tight')
box_1.inspect(21, 'graph')
plt.savefig('../results/prim_box21.png', dpi=300, bbox_inches='tight')
plt.show()