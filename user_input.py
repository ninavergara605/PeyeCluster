import pandas as pd
from get_paths import GetPaths
from roi_template_import import RoiTemplateImport
class UserInput:

    def __init__(self 
        ,result_directory=None
        ,roi_template_path=None
        ,behavior_test_path=None
        ,eye_track_directory=None
        ,bin_analysis=False
        ,roi_template_df=pd.DataFrame()
        ,show_nonmatching_data=True
        ,roi_key_column_names=None
        ,output_folder_name = 'processed_data'
        ,block_types=None):
        
        self._result_directory = GetPaths.normalize_path(result_directory)
        self._roi_template_path = GetPaths.normalize_path(roi_template_path)
        self._behavior_test_path = GetPaths.normalize_path(behavior_test_path)
        self._eye_track_directory = GetPaths.normalize_path(eye_track_directory)
        self._bin_analysis = bin_analysis
        self._roi_template_df = roi_template_df
        self._show_nonmatching_data = show_nonmatching_data
        self._roi_key_column_names = roi_key_column_names
        self._output_folder_name = output_folder_name
        self._block_types = block_types

    @property
    def result_directory(self):
        return self._result_directory
    
    @result_directory.setter
    def result_directory(self, value):
        self._result_directory = GetPaths.normalize_path(value)

    @property
    def roi_template_path(self):
            return self._roi_template_path

    @roi_template_path.setter
    def roi_template_path(self, value):
        self._roi_template_path = GetPaths.normalize_path(value)
    
    @property
    def roi_template_df(self):
        if self._roi_template_df.empty:
                self._roi_template_df = RoiTemplateImport(self._roi_template_path).result
        return self._roi_template_df

    @property
    def behavior_test_path(self):
            return self._behavior_test_path

    @behavior_test_path.setter
    def behavior_test_path(self, value):
        self._behavior_test_path = GetPaths.normalize_path(value)

    @property
    def eye_track_directory(self):
            return self._eye_track_directory
      
    @eye_track_directory.setter
    def eye_track_directory(self, value):
        self._eye_track_directory = GetPaths.normalize_path(value)

    @property
    def bin_analysis(self):
            return self._bin_analysis
    
    @bin_analysis.setter
    def bin_analysis(self, value):
        self._bin_analysis = value

    @property
    def show_nonmatching_data(self):
            return self._show_nonmatching_data
       
    @show_nonmatching_data.setter
    def show_nonmatching_data(self, value):
        self._show_nonmatching_data = value

    @property
    def roi_key_column_names(self):
            return self._roi_key_column_names
       
    @roi_key_column_names.setter
    def roi_key_column_names(self, value):
        self._roi_key_column_names = value
    
    @property
    def output_folder_name(self):
            return self._output_folder_name
       
    @output_folder_name.setter
    def output_folder_name(self, value):
        self._output_folder_name = value


    @property
    def block_types(self):
            return self._block_types
       
    @block_types.setter
    def block_types(self, value):
        self._block_types = value