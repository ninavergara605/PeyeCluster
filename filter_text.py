from collections import defaultdict
import pandas as pd

def filter_text(data):
    trial_no = 0
    converted_lines = []
    by_trial = []

    filter_by = ['START', 'EFIX', 'EBLINK']
    split_lines = [line.split() for line in data]
    
    for line in split_lines:
        if not line or line[0].isdigit():
            pass
        elif any(targ == line[0] for targ in filter_by):
            if line[0] == 'START':
                
                if converted_lines :
                    trial_df = pd.DataFrame(converted_lines).assign(trial=trial_no)
                    by_trial.append(trial_df)
                    converted_lines = []
                trial_no += 1
            
            filtered_line = string_to_num(line)
            converted_lines.append(filtered_line)

    trial_df = pd.DataFrame(converted_lines).assign(trial=trial_no)
    by_trial.append(trial_df)
    all_trials = pd.concat(by_trial, sort=True)
    return  all_trials
    

# Returns array of line values that are converted to ints/floats.
def string_to_num(line):
    number_line = []
    for string in line:
        current_number = []
    
        if string.isdigit():
            current_number = int(string)
        else:
            try:
                current_number = float(string)
            except ValueError:
                #keep string and append anyway
        
                current_number = string


        number_line.append(current_number)
    return number_line