import re
from pathlib import Path, PureWindowsPath
from collections import namedtuple


class GetPaths:
    
    
    def __init__(self, directory, target_path_type = '.asc', block_types=None):
        self._directory = directory
        self._target_path_type = target_path_type
        self._block_types = block_types
        
        self.result = self.get_paths_from_directory()
   
    def get_paths_from_directory(self):
        paths=[]
        if self._target_path_type:
            search_pattern = ''.join(['**/*', self._target_path_type])
            
        else:
            search_pattern = '**/*'
        #if self._directory.is_dir():
            #print('is_dir')
        for folder in self._directory.iterdir():
            match_paths = list(folder.glob(search_pattern))
            print(match_paths)
            if match_paths:
                paths.extend(match_paths)  
        #else:
        #    return self._directory
        #print('hi')
        if self._block_types:
            print('hi')
            labeled_paths = GetPaths.label_by_subject(paths, self._block_types)
            return labeled_paths

        return paths

    @staticmethod
    def label_by_subject(paths, split_by):
        Subject = namedtuple('Subject', ['subject', 'block_type', 'block', 'path'])
        labeled_paths = []
        for path in paths:
            name = path.stem
            
            subject, block_type, block = re.split(split_by, name)
            print(subject, block_type, block)
            subject_info = Subject(subject, block_type, block, path)
            labeled_paths.append(subject_info)
           
        return labeled_paths 

    @staticmethod
    def normalize_path(path):
        if path:
            if '\\' in path:
                windows_path = PureWindowsPath(path)
                normalized = Path(windows_path.as_posix())
            else:
                normalized = Path(path)
            return normalized
        else:
            return None

    '''
    Creates a path from directory and file name inputs.
    Any folder that does not exist is made into a directory.
    '''
    @staticmethod
    def create_path(directory, file_name, extension='.csv', folder='processed_data'):        

        folder_path = directory / folder
        if not folder_path.is_dir():
            folder_path.mkdir(parents=True)
        
        file_path = folder_path / file_name 
        path_with_extension = file_path.with_suffix(extension)
        return path_with_extension