'''
Created on May 17, 2019

@author: eker
'''
import sys
import warnings
import numpy as np
import time
from ema_workbench.connectors.vensim import VensimModel
from ema_workbench import (MultiprocessingEvaluator,
                           TimeSeriesOutcome, 
                           perform_experiments,
                           Policy,
                           RealParameter,
                           CategoricalParameter,
                           Constant, 
                           ema_logging, 
                           save_results)
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt





ema_logging.log_to_stderr(ema_logging.INFO)
ema_logging.log_to_stderr(ema_logging.DEBUG)

if __name__ == '__main__':
    directory = 'H:/MyDocuments/IIASA-Felix/Model files/Enhanced_Weathering/Winter1920/ema_run/'
    
    
    df_unc = pd.read_excel(directory+'EW_Framework.xlsx', sheet_name='Uncertainties')
    df_cat = pd.read_excel(directory+'EW_Framework.xlsx', sheet_name='Categoricals')
    df_out = pd.read_excel(directory+'EW_Framework.xlsx', sheet_name='Outcomes')


    vensimModel = VensimModel("ew", wd=directory, model_file=r'Felix3_v18_EW.vpm')
    
    #vensimModel.outcomes = [TimeSeriesOutcome(out) for out in df_out['Outcomes']]
    outs = ['Rock per ha agricultural land',
            'Rock per ha new forests',
            'Rock per ha coastal zone']
            #'Basalt application rate',
            #'Olivine application rate',
            #'Temperature Change from Preindustrial',
            #'Cumulative CO2 removal by weathering',
            #'Net CO2 emissions',
            #'Total Demand for Arable Land', 
            #'Agricultural N2O Emissions',
            #'Cumulative Cost of C Removal by EW',
            #'Cumulative basalt use',
            #'Cumulative olivine use']
    
    vensimModel.outcomes = [TimeSeriesOutcome(out) for out in outs]
    #vensimModel.outcomes = [TimeSeriesOutcome('Cumulative Cost of C Removal by EW')]
    
    vensimModel.uncertainties = [RealParameter(row['Uncertainty'], row['Lower'], row['Upper']) for index, row in df_unc.iterrows()
                                if not row['Source'].startswith('Managerial')]
    
    #vensimModel.constants = [Constant('Rock application area switch', 0)] # only cropland
    #vensimModel.constants = [Constant('Rock application area switch', 1), # only forest
    #vensimModel.constants = [Constant('Rock application area switch', 2), # only coast
    
    
    
    vensimModel.uncertainties += [#CategoricalParameter('Grain size switch', (50, 20, 10, 2)),
                                  #CategoricalParameter('Transition Scenario Switch', (1,2))]
                                  #CategoricalParameter('Rock application area switch', (0, 1, 2, 3)),
                                  CategoricalParameter('Goal Seeking Switch', (0,1))]
                                  
    vensimModel.constants = [Constant('Rock application area switch', 3), #all
                             #Constant('Goal Seeking Switch', 1),
                             Constant('Grain size switch', 50),
                             Constant('Transition Scenario Switch', 2)]
    
    ema_logging.log_to_stderr(ema_logging.INFO)
    
    area = {0 : "cropland",
            1: "forest",
            2: "coast",
            3: "all"}
    
    with MultiprocessingEvaluator(vensimModel, n_processes=8) as evaluator:

        results = evaluator.perform_experiments(10000, reporting_interval=1000)
        fn = '../results/EW_goal_nogoal_perha.tar.gz'
        save_results(results, fn)
    




