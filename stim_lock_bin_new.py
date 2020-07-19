import pandas as pd
import numpy as np


class GetMovementRoi:

    def __init__(self, eye_movements, roi):
        self._eye_movements = eye_movements
        self._roi = roi
        self.result = self.get_movement_roi()

    def get_movement_roi(self):
        roi_x_bins = pd.IntervalIndex.from_tuples(self._roi['x_range'])
        roi_y_bins = pd.IntervalIndex.from_tuples(self._roi['y_range'])
    
        y_in_range = self.in_range(self._eye_movements['y'].values, roi_y_bins)
        x_in_range = self.in_range(self._eye_movements['x'].values, roi_x_bins)
        in_coord_range = self.intersection(y_in_range, x_in_range)
        
        movements_roi = []
        for movement_id, in_range in enumerate(in_coord_range, 1):
            movement_roi = self._roi[in_range]
            if not movement_roi.empty:
                movement_roi = movement_roi.assign(movement_id=movement_id)
                movements_roi.append(movement_roi)
        
        movements_roi = pd.concat(movements_roi)
        movements_roi = pd.merge(movements_roi, self._eye_movements, 
                left_on='movement_id', 
                right_on='fixation', 
                suffixes=('_roi', '_movement'))
        
        time_constrained_movements = movements_roi.apply(self.constrain_movement_time, axis = 1)
        time_constrained_movements.dropna(inplace=True)
        result_columns = time_constrained_movements[['trial', 
                                                    'roi', 
                                                    'movement_id',
                                                    'constrained_start',
                                                    'constrained_stop' ]]
        return result_columns

    def constrain_movement_time(self, row):
        if row.start_movement > row.stop_roi or row.stop_movement < row.start_roi:
            row['constrained_start'] = np.nan
            row['constrained_stop'] = np.nan
            return row
        if row.start_movement > row.start_roi:
            row['constrained_start'] = row.start_movement
        else:
            row['constrained_start'] = row.start_roi
        if row.stop_movement > row.stop_roi:
            row['constrained_stop'] = row.stop_roi
        else:
            row['constrained_stop'] = row.stop_movement
        return row

    def in_range(self, x_arr, bins):
        is_in_range = [[x in _bin for _bin in bins] for x in x_arr]
        return is_in_range
    
    def intersection(self, i, j):
        is_intersect = [[(k == True)&(l == True) for k, l in zip(m,n)] for m, n in zip(i, j)]
        return is_intersect