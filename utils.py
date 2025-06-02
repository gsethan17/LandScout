import pandas as pd
def get_district_code(name=None):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'config', 'statutory_administrative_district_code.txt'), sep='\t')

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
                
    return int(code)

def get_district_name(code):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'config', 'statutory_administrative_district_code.txt'), sep='\t')
    exist = sorted(df[df.columns[2]].unique())[0]
    name_no_spaces = ''
    
    name = df[(df[df.columns[0]] == int(code)) & (df[df.columns[2]] == exist)][df.columns[1]].values[0]
    
    for name in name.split(' '):
        name_no_spaces += name + '_'
    
    return name_no_spaces[:-1]

from config_base import param_name
def check_district_code(params):
    # if user provides the name of interested district,
    if len(params["cortarName"]) > 0 :
        district_names = params["cortarName"]
        district_codes = []
        for name in district_names:
            code = get_district_code(name)
            if code == None:
                raise NameError("[E] 행정구역 이름 또는 띄어쓰기를 확인하세요.: {}".format(name))
            district_codes.append(str(code))
    # otherwise, the search will cover the entire country,
    else:
        raise ValueError("[E] config_user.txt 파일 내 탐색 지역을 1개 이상 작성하세요.")
        
    print("")
    print("[I] 아래 조건으로 탐색합니다.")
    print("[I] 탐색 구역: ")
    for name in district_names:
        print("\t- {}".format(name))
    for k, v in params.items():
        if k == "cortarName":
            continue
        try:
            print("[I] {}:".format(param_name[k]))
            for sub_ in v:
                try:
                    print("\t- {}".format(param_name[sub_]))
                except:
                    print("\t- {}".format(sub_))
        except:
            if v[0] == 'True':
                print("[I] 추가 기능 : {}".format(k))
    print("")
    return True, district_codes

def get_district_dict():
    
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'config', 'statutory_administrative_district_code.txt'), sep='\t')
    
    num_dong = df.법정동명.apply(lambda x: len(x.split(' '))).copy()
    idx_is_exist = df[df['폐지여부'] == '존재'].index
    
    idx_dong_1level = num_dong[num_dong == 1].index
    idx_dong_1level = idx_dong_1level.intersection(idx_is_exist)
    dong_1level = df.법정동명[idx_dong_1level].to_list()
    
    district_dict = {k:{} for k in dong_1level}
    
    idx_dong_2level = num_dong[num_dong == 2].index
    idx_dong_2level = idx_dong_2level.intersection(idx_is_exist)
    for dong_1_2 in df.법정동명[idx_dong_2level].to_list():
        dong1, dong2 = dong_1_2.split(' ')
        
        district_dict[dong1][dong2] = []
    
    
    idx_dong_3level = num_dong[num_dong == 3].index
    idx_dong_3level = idx_dong_3level.intersection(idx_is_exist)
    for dong_1_2_3 in df.법정동명[idx_dong_3level].to_list():
        dong1, dong2, dong3 = dong_1_2_3.split(' ')
        
        district_dict[dong1][dong2].append(dong3)
        
    return district_dict
    
        

import os
import shutil
def build_exe(file_path):
    
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
    
    from_dir = os.path.join(os.path.dirname(file_path), "config")
    to_dir = os.path.join(dir_, "dist", "LandScout", "_internal", "config")
    shutil.copytree(from_dir, to_dir)
    
from config_base import param_name
def get_txt_config(path):
    config = {}
    key = None
    
    with open(path, 'r', encoding='UTF8') as file:
        for line in file:
            line = line.strip() # remove blank
            
            # ignore commend or black line
            if line.startswith("#") or not line:
                continue
            
            if line.startswith(">"):
                key = line.split(">")[-1].strip()
                config[key] = []
            else:
                value = line.strip()
                # convert hangul value to key code
                for param_k, param_v in param_name.items():
                    if param_v == value:
                        value = param_k
                        
                config[key].append(value)
                
    return config

def get_application_key():
    app_key = {}
    with open(os.path.join(os.path.dirname(__file__), "config", "application_key.txt"), encoding='UTF8') as file:
        for line in file:
            line = line.strip() # remove blank
            
            # ignore commend or black line
            if line.startswith("#") or not line:
                continue
            
            key, value = line.split("=", 1)
            if not value:
                raise ValueError("[E] application_key.txt 파일에 client_id 및 client_secret을 확인하세요.")
            
            app_key[key.strip()] = value.strip()
    
    return app_key

import time
def terminate():
    print("Terminate in 10seconds...")
    for i in range(10, 0, -1):
        print(f"{i}, ", end='')
        time.sleep(1)
    
    
if __name__ == "__main__":
    app_key = get_application_key()
    print(app_key)
    
    # params = get_txt_config(os.path.join(os.path.dirname(__file__), 'config_user.txt'))
    # print(params)
    
    # code = '2920000000'
    # name = get_district_name(code=code)
    # print(name)
    