import os
import string
import pandas as pd
import numpy as np
from filter_text import filter_text


def get_movements(raw_data):
    data_by_trial = filter_text(raw_data)
    movements = create_trial_df(data_by_trial)
    
    movements['start'] = movements.start_from_block_start - movements.trial_start
    movements['stop'] = movements.stop_from_block_start - movements.trial_start
    
    movements['duration'] = movements.stop - movements.start
    movements['count'] = movements.groupby('type').cumcount() + 1

    drop_columns = ['start_from_block_start', 
                    'stop_from_block_start', 
                    '_', 
                    'trial_start']
    movements.drop(drop_columns, axis=1, inplace=True)
    #print(movements)
    return movements


def create_trial_df(data_by_trial):
    data_by_trial.columns = ['type', 
                        'trial_start',
                        'start_from_block_start',  
                        'stop_from_block_start', 
                        'eprime_duration', 
                        'x', 
                        'y', 
                        '_',
                        'trial']

    movements = data_by_trial.groupby('trial').apply(get_trial_start).reset_index(drop=True)
    movements.set_index(['trial'], append=True, inplace=True, drop=True)
    movements.index.names = ['movement_id', 'Trial']

    return movements

def get_trial_start(trial_group):
    trial_group['trial_start'] = trial_group['trial_start'].replace('L', np.nan).ffill(axis=0)
    return trial_group.iloc[1:,]


        
        






