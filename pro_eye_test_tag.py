import pandas as pd
import itertools
import numpy as np
from collections import defaultdict
from functools import partial


class ProactiveEyeTestTag:
    def __init__(self, behavior_df):
        self._behavior_df = behavior_df
        self.result = behavior_df.apply(self.get_tags, axis=1)

    def get_tags(self, row):
        if np.isnan(row.Old_New_Resp):
            return 'BadResponse'
        
        elif row.Type == 'New':
            if row.Old_New_Resp == 1:
                return 'FA'
            elif row.Old_New_Resp == 2:          
                return 'CR'
        
        elif row.Old_New_Resp == 2:
            tag = ''.join([row.Type, '_Miss'])
            return tag
        elif np.isnan(row.FACE_R):
            return 'BadResponse'

        else:
            resp_roi = row[['TargResp', 'LureResp', 'TDistResp', 'LDistResp']]
            resp_col = resp_roi[resp_roi.isin([row.FACE_R])].index[0]
        
            if resp_col == 'TargResp':
                tag = ''.join([row.Type, '_Correct'])
            else:
                tag = ''.join([row.Type, '_', resp_col])
            return tag
    
