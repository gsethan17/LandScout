from utils import get_district_code
from config_base import param_name
# from config_user import params
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
        
from config_base import decode_key
from query import WebQueryClient
from url_info import basic_url, detail_url
import os
from utils import get_txt_config
if __name__ == "__main__":
    params = get_txt_config(os.path.join(os.path.dirname(__file__), 'config_user.txt'))
    flag, district_codes = check_district_code(params)
    if not flag:
        raise ValueError("config.py 파일을 확인하세요.")
    
    client = WebQueryClient(
        base_url=basic_url,
        detail_url=detail_url,
        query_params=params,
        decode_key=decode_key,
        address=params['address'][0] == 'True',
        ETA=params['ETA'][0] == 'True', 
        rlet_link=params['rlet_link'][0] == 'True', 
        map_link=params['map_link'][0] == 'True', 
        )
    
    client.get_n_save_data(district_codes=district_codes)
    
    
    
    