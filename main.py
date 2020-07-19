from user_input import UserInput
from get_paths import GetPaths
import pandas as pd
from get_eye_movements import get_movements
from export import Export
import cProfile, pstats
from pstats import SortKey
from get_roi import GetROI
from pro_eye_test_tag import ProactiveEyeTestTag
from pro_eye_test_import import TestImportProactiveEyes
import numpy as np


def main(user_input):
    test_roi = pd.DataFrame()
    eye_movement_output_path = None
    
    if user_input._behavior_test_path:
        test_roi = get_roi(user_input)
    if user_input.eye_track_directory:
        eye_movement_output_path, movement_subjects_blocks = get_eye_movements(user_input)
        
    if user_input.bin_analysis:
        if not test_roi.empty and eye_movement_output_path:
            pass
    return

def get_roi(user_input):
    behavior_df = TestImportProactiveEyes(user_input.behavior_test_path).result
    test_response_tags = ProactiveEyeTestTag(behavior_df).result
    test_response_tags.rename('test_response_tags', inplace=True)

    if not user_input.roi_template_df.empty and user_input.roi_key_column_names:
        test_roi = GetROI(behavior_df
                        ,user_input.roi_template_df
                        ,user_input.roi_key_column_names).result


        output = test_roi.merge(test_response_tags, left_on='trial_id', right_index=True, how='left')
        file_name = 'test_roi'
    else:
        print('Specify roi_template_path and roi_key_column_names in user_input to excecute GetROI')

        output = pd.concat([behavior_df, test_response_tags], axis=1)
        file_name = 'test_behavior_tag'
    
    output_path = GetPaths.create_path(user_input.result_directory 
                            ,file_name
                            ,folder=user_input.output_folder_name)
    export = Export()
    export.store_data(df=output)
    export.export_stored_data(output_path)

    if file_name == 'test_roi':
        return output
    return None

def get_eye_movements(user_input):
    subject_eye_track_paths = GetPaths(user_input.eye_track_directory
                                ,target_path_type='.asc'
                                ,block_types=user_input.block_types).result
    output_path = GetPaths.create_path(user_input.result_directory 
                            ,'eye_movements'
                            ,folder=user_input.output_folder_name)
    print(subject_eye_track_paths)
    '''
    export = Export()
    subjects_blocks = []
    for subject_block in subject_eye_track_paths:       
        with open(subject_block.path) as f:
            eye_track_data = get_movements(f)
            export.store_data(df=eye_track_data, subject_block=subject_block[0:3])
            subjects_blocks.append(subject_block)
    export.export_stored_data(output_path)
    return output_path,subjects_blocks
    '''
    return 1,1

behavior_test_path = r'/Users/ninavergara/Desktop/proactive_eyes_test_behavior.xlsx'
roi_template_path  = r'/Users/ninavergara/Desktop/proactive_eyes_roi_template.xlsx'
res_path_windows = r'\\Users\\ninavergara\\Desktop'
eye_track_directory = r'/Users/ninavergara/Desktop/ProactiveEyes/Data/'

if __name__ == "__main__":
    #pr = cProfile.Profile() 
    #pr.enable()
    user_input = UserInput(result_directory=res_path_windows
                            ,eye_track_directory=eye_track_directory
                            ,behavior_test_path=behavior_test_path
                            ,roi_template_path=roi_template_path
                            ,roi_key_column_names= ['TargetX', 'LureX', 'TargetDistX', 'LureDistX']
                            ,output_folder_name='proactive_eyes_processed'
                            ,block_types='(E|R)')
    main(user_input)
    #pr.disable()
    #ps = pstats.Stats(pr)#.sort_stats(SortKey.CUMULATIVE)
    #ps.strip_dirs()
    #ps.sort_stats('cumulative')
    #ps.print_stats()    
   