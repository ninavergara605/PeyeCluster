import pandas as pd


class TestImportProactiveEyes:

    def __init__(self, behavior_path):    
        self._behavior_path = behavior_path
        self.result = self.format_df(behavior_path)
       
    def format_df(self, behavior_path):
        df = pd.read_excel(behavior_path)
        df = df.groupby(['ExperimentName']).apply(TestImportProactiveEyes.get_block) 
        
        not_null_columns = ['TargResp'
                        ,'LureResp'
                        ,'TDistResp'
                        ,'LDistResp'
                        ,'Type'
                        ,'TargetX'
                        ,'LureX'
                        ,'TargetDistX'
                        ,'LureDistX']
        filtered_df = df.dropna(subset=not_null_columns)
        return filtered_df

    @staticmethod
    def get_block(group):
        experiment_name = group.name
        block = experiment_name.split()[-1]  #filters to 'test#'
        
        group['block_type'] = 'T'
        group['block'] = block
        return group

    @staticmethod
    def chunk_by_subj_block(df):   
        groups = df.groupby(['subject', 'block_type', 'block'])
        return groups