import os

from utils import terminate
from utils import get_txt_config
from utils import check_district_code

from query import WebQueryClient
from config_base import decode_key

if __name__ == "__main__":
    params = get_txt_config(os.path.join(os.path.dirname(__file__), 'config', 'config_user.txt'))
    flag, district_codes = check_district_code(params)
    if not flag:
        raise ValueError("config.py 파일을 확인하세요.")
    
    client = WebQueryClient(
        query_params=params,
        decode_key=decode_key,
        address=params['address'][0] == 'True',
        ETA=params['ETA'][0] == 'True', 
        rlet_link=params['rlet_link'][0] == 'True', 
        map_link=params['map_link'][0] == 'True', 
        verbose=2,
        )
    
    client.get_n_save_data(district_codes=district_codes)
    
    terminate()
    