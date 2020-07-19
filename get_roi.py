from collections import defaultdict
import pandas as pd
import numpy as np

class GetROI:
    def __init__(self, behavior_test, roi_template, key_column_names):       
        self._key_column_names = key_column_names
        self._test_behavior = behavior_test
        self._roi_template = roi_template
        self.result = self.get_roi()

    def get_roi(self):
        result_df = self.create_result_df()
        #reindexes dynamic labels for filling result_df with labeled columns
        static_df = self._roi_template['static'].set_index('lookup_keys', drop=True)
        result_df = result_df.combine_first(static_df) #Adds static info to result df
        
        #reindexes dynamic labels for filling result_df with labeled columns
        dynamic_label_df = self._roi_template['dynamic_roi_label'].set_index('dynamic_event_column', drop=True)
        dynamic_label_df.index.names = ['lookup_keys']
        result_df = result_df.combine_first(dynamic_label_df) #adds dynamic label columns to result df
        
        
        behavior_test_dynamic_keys = self._test_behavior[self._key_column_names].stack()
        result_df['event_key'] = np.nan
        result_df['event_key'] = result_df['event_key'].combine_first(behavior_test_dynamic_keys)
        
        dynamic_event_options = self._roi_template['dynamic_event_options'].set_index('key', drop=True).to_dict('index')
        for key, value in dynamic_event_options.items():
            result_df.loc[result_df.event_key == key,:] = result_df.loc[result_df.event_key == key,:].fillna(value)
        
        result_df.set_index('roi_label', append=True,inplace=True)
        del result_df['event_key']
        result_df = result_df.droplevel('lookup_keys', axis=0)
        
        return result_df

    def create_result_df(self):
        columns = self._roi_template['static'].columns
        
        roi_index = self._key_column_names.copy()
        static_index = self.get_static_index()
        roi_index.extend(static_index)
        
        index = pd.MultiIndex.from_product([self._test_behavior.index, roi_index], names=['trial_id', 'lookup_keys'])
        df = pd.DataFrame(index=index, columns=columns)

        return df

    def get_static_index(self):
        static_index_range = range(len(self._roi_template['static'])-1) #exclude headers 
        static_index = [''.join(['static_', str(x)]) for x in static_index_range] #create index names for final df

        #add index to static df for merging
        self._roi_template.loc[static_index_range,('static','lookup_keys')] = static_index
        self._roi_template.sort_index(axis=1, level=0, inplace=True)

        return static_index
