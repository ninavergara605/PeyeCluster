import pandas as pd
from collections import defaultdict
import numpy as np
from excel_import_3FND import BehaviorTestImport

class TestTag3FND:

    def __init__(self, behav_df):
        self._behav_df = behav_df
        self._conditions = ['Same', 'Similar', 'New']
        self._correct_roi_response = {'Same': 
                                    {12: 'targ_resp', 24: 'targ_resp'}, 
                                'Similar': 
                                    {12: 'new_resp', 24: 'targ_resp'}, 
                                'New':
                                    {12: 'new_resp', 24: 'new_resp'}}
        self._response_columns = ['targ_resp', 'lure_resp', 'new_resp']
        self.result = self.get_behavior()

    def get_behavior(self):
        #copy input df to preserve the original and minimize instance calls
        behavior_test = self._behav_df.copy()

        inc_scene_tags = TestTag3FND.get_tags('miss'
                                                ,arr_1=self._conditions 
                                                ,arr_2=self._conditions
                                                )
        inc_roi_tags = TestTag3FND.get_tags('inc'
                                                ,arr_1=self._conditions
                                                ,arr_2=self._response_columns
                                                )
        corr_roi_tags = TestTag3FND.get_tags('correct', arr_1=self._conditions)

        scene_resp_tag_df = behavior_test.groupby(['condition', 'scene_resp']).apply(
                                                                                TestTag3FND.tag_inc_scene_resp
                                                                                ,inc_scene_tags)
        roi_resp_tag_df = scene_resp_tag_df[scene_resp_tag_df['behavior_tag'].isnull()].copy()
        roi_resp_tag_df = roi_resp_tag_df.apply(TestTag3FND.tag_roi_resp
                                                    , axis=1
                                                    , args=(self._correct_roi_response
                                                                ,corr_roi_tags
                                                                ,inc_roi_tags))
        tagged_df = scene_resp_tag_df.combine_first(roi_resp_tag_df)
        return tagged_df['behavior_tag']
    @staticmethod
    def tag_roi_resp(row, corr_responses, corr_tags, inc_tags):
        response_columns = ['targ_resp', 'lure_resp', 'new_resp']
        roi_columns = row[response_columns]

        test_response, cond, time = row[['face_resp', 'condition', 'time_condition']].values
        corr_roi_name = corr_responses[cond][time]
        
        roi_resp_name = roi_columns.index[roi_columns.isin([test_response])][0]
        if roi_resp_name:
            if corr_roi_name == roi_resp_name:
                tag = corr_tags[cond]
            else:
                tag = inc_tags[cond][roi_resp_name]
        else:
            tag = 'BadResp'
        
        row['behavior_tag'] = tag
        return row
       
    @staticmethod
    def tag_inc_scene_resp(group, inc_scene_tags):
        correct_responses = {1:'Same', 2:'Similar', 3:'New'}
        condition, scene_response = group.name

        if not isinstance(scene_response, int):    
            group['behavior_tag'] = 'BadResp'
            return group
        
        resp_cond = correct_responses.get(scene_response)
        if resp_cond:
            if resp_cond != condition:
                tag = inc_scene_tags[condition][resp_cond]
            else:
                tag = np.nan
        else:
            tag='BadResp'
        group['behavior_tag'] = tag
        return group

    @staticmethod
    def get_tags( _str, arr_1=None, arr_2=None):
        if arr_2:
            tags = [((i, j), ''.join([i,'_', _str,'_',j])) 
                                                    for i in arr_1
                                                        for j in arr_2]
            tag_dict = defaultdict(dict)
            for (i, j), tag in tags:
                tag_dict[i][j] = tag
        else:
            tags = [(i, ''.join([i, '_',_str])) for i in arr_1]
            tag_dict = {}
            for i, tag in tags:
                tag_dict[i] = tag
        return tag_dict




behavior_test = r'/Users/ninavergara/Desktop/3FaceNightDay/Data/3FaceNightDayBehaviorUpdated.xlsx'

behavior_df = BehaviorTestImport(behavior_test).result
TestTag3FND(behavior_df)