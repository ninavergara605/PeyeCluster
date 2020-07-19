import pandas as pd

class Export:
    def __init__(self):
        self.store_data = Export.store_output()
    
    @staticmethod
    def store_output():
        dfs = []
        subject_infos = []

        def add_df(df=None, subject_block=None):
            nonlocal dfs
            nonlocal subject_infos
            
            if subject_block:
                dfs.append(df)
                subject_infos.append(subject_block)
                return dfs, subject_infos
           
            dfs.append(df)
            return dfs
        return add_df
    
    def export_stored_data(self, path):
        if not self.store_data()[1]:
            output_df = self.store_data()[0]
        else:
            output_df = self.create_df()
        
        with open(path, 'w') as f:
                output_df.to_csv(f)
       
    def create_df(self):
        index_names = ['subject', 'block_type', 'block']
        dfs, concat_keys = self.store_data()
        if concat_keys:
            output_df = pd.concat(dfs, 
                                    keys=concat_keys, 
                                    names=index_names)
        else:
            output_df = pd.concat(dfs)
        
        return output_df


