from utils import get_district_code
from config_base import param_name
from config_user import params
def check_district_code():
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
        district_names = ["전국"]
        district_codes = list(map(str, get_district_code()))
        
    print("")
    print("[I] 아래 조건으로 탐색합니다.")
    print("[I] 탐색 구역: ")
    for name in district_names:
        print("\t- {}".format(name))
    for k, v in params.items():
        if k == "cortarName":
            continue
        print("[I] {}:".format(param_name[k]))
        for sub_ in v:
            try:
                print("\t- {}".format(param_name[sub_]))
            except:
                print("\t- {}".format(sub_))
    print("")
    return True, district_codes
        
from config_base import decode_key
from query import WebQueryClient
from url_info import basic_url, detail_url
if __name__ == "__main__":
    flag, district_codes = check_district_code()
    if not flag:
        raise ValueError("config.py 파일을 확인하세요.")
    
    client = WebQueryClient(
        base_url=basic_url,
        detail_url=detail_url,
        query_params=params,
        decode_key=decode_key,
        )
    
    client.get_n_save_data(district_codes=district_codes)
    
    
    
    