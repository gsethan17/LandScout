import pandas as pd
def get_district_code(name=None):
    df = pd.read_csv('statutory_administrative_district_code.txt', sep='\t')

    level_ = {}
    for l in range(1, 6, 1):
        level_[l] = [i for i, x in enumerate(df[df.columns[1]].values) if len(x.split(' ')) == l]
    
    exist = sorted(df[df.columns[2]].unique())[0]
    
    if name != None:
        code = None
        for i in level_[len(name.split(" "))]:
            if df.loc[i, df.columns[1]] == name:
                if df.loc[i, df.columns[2]] == exist:
                    code = df.loc[i, df.columns[0]]
    else:
        code = []
        for i in level_[2]:
            if df.loc[i, df.columns[2]] == exist:
                code.append(df.loc[i, df.columns[0]])
                
    return code

def get_district_name(code):
    df = pd.read_csv('statutory_administrative_district_code.txt', sep='\t')
    exist = sorted(df[df.columns[2]].unique())[0]
    name_no_spaces = ''
    
    name = df[(df[df.columns[0]] == int(code)) & (df[df.columns[2]] == exist)][df.columns[1]].values[0]
    
    for name in name.split(' '):
        name_no_spaces += name + '_'
    
    return name_no_spaces[:-1]

import os
import shutil
def build_exe(file_path, necessary_files=[]):
    
    # check previous log
    dir_ = os.path.dirname(file_path)
    is_build = os.path.isdir(os.path.join(dir_, "build"))
    is_dist = os.path.isdir(os.path.join(dir_, "dist"))
    spec_path = os.path.join(dir_, os.path.splitext(os.path.basename(file_path))[0] + ".spec")
    is_spec = os.path.isfile(spec_path)
    
    if is_build or is_dist or is_spec:
        if input("이전 실행 내역이 존재합니다. 삭제하고 계속할까요? (y/n): ").lower() != 'y':
            return -1
    if is_build:
        shutil.rmtree(os.path.join(dir_, "build"))
    if is_dist:
        shutil.rmtree(os.path.join(dir_, "dist"))
    if is_spec:
        os.remove(spec_path)
        
        
    os.system(f"pyinstaller {file_path} -n LandScout")
    
    for file_ in necessary_files:
        from_file = os.path.join(os.path.dirname(file_path), file_)
        to_file = os.path.join(dir_, "dist", "LandScout", file_)
        shutil.copyfile(from_file, to_file)
    
    
if __name__ == "__main__":
    code = '2920000000'
    name = get_district_name(code=code)
    print(name)
    