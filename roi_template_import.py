import pandas as pd
import numpy as np

class RoiTemplateImport:


    def __init__(self, roi_template_path):
        self._roi_template_path = roi_template_path
        self.result = self.get_template_df()

    def get_template_df(self):
        template_df = pd.read_excel(self._roi_template_path, header=[0,1])
        static = template_df['static'].apply(RoiTemplateImport.get_coords_and_ranges, axis=1)
        dynamic = template_df['dynamic_event_options'].apply(RoiTemplateImport.get_coords_and_ranges, axis=1)
       
        template = pd.concat([static, dynamic, template_df['dynamic_roi_label']], 
                                axis=1, 
                                keys=['static','dynamic_event_options', 'dynamic_roi_label'])
        return template

    @staticmethod
    def get_coords_and_ranges(row):    
        if not isinstance(row.top_left_xy,str):
            return row
        br_xy, tl_xy = [tuple(map(int, coord.split(','))) for coord in [row.bottom_right_xy, row.top_left_xy]]
        row['bottom_right_x'] = br_xy[0]
        row['bottom_right_y'] = br_xy[1]

        row['top_left_x'] = tl_xy[0]
        row['top_left_y'] = tl_xy[1]
       
        return row