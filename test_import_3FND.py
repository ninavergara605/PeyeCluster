import pandas as pd
import re


class BehaviorTestImport:

    def __init__(self, behavior_path):    
        self._behavior_path = behavior_path
        self.result = self.format_df(behavior_path)
       
    def format_df(self, behavior_path):
        df = pd.read_excel(behavior_path)
        df.rename(columns = {'picturetrial.RESP': 'scene_resp', 
                            'pictureTrial3.RESP':'face_resp'}, 
                            inplace = True)
        
        df.columns = BehaviorTestImport.camel_to_snake(df.columns)
        df = df.groupby(['experiment_name']).apply(BehaviorTestImport.get_block) 
        
        not_null_columns = ['targ_resp', 'lure_resp', 'new_resp', 'scene_resp', 'face_resp']
        filtered_df = df.dropna(subset=not_null_columns)
        
        return filtered_df
    
    @staticmethod
    def camel_to_snake(name_arr):
        converted = []
        for name in name_arr:
            new = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
            converted.append(new)
        return converted

    @staticmethod
    def get_block(group):
        experiment_name = group.name
        block_str = experiment_name.split('-')[-1]  #filters to 'test#'
        
        block_type, block_number = re.split('(\d+)', block_str)[0:2] #split by letters and numbers
        group['block_type'] = block_type[0] 
        group['block'] = block_number
        return group

    @staticmethod
    def chunk_by_subj_block(df):   
        groups = df.groupby(['subject', 'block_type', 'block'])
        return groups
                