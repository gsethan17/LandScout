import os
import requests
import pandas as pd
from tqdm import tqdm
from copy import deepcopy
from utils import get_district_name
from utils import get_application_key

from url_info import reverse_gc_url, driving_url
from application_key import client_id, client_secret

class WebQueryClient(object):
    def __init__(self, base_url, detail_url, query_params, decode_key, **kwargs):
        self.url = base_url
        self.detail_url = detail_url
        self.decode_key = decode_key
        self.query_params = {}
        for k, v in query_params.items():
            if k == "cortarName":
                continue
            if len(v) > 1:
                value = ""
                for sub_v in v:
                    value+=str(sub_v)
                    value+=":"
                self.query_params[str(k)] = str(value[:-1])
                
            else:
                self.query_params[str(k)] = str(v[0])
                
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        
        # preprocessing function
        self.kwargs = kwargs
        self.add_get_address = self.kwargs.get('address', False)
        self.add_get_ETA = self.kwargs.get('ETA', False)
        self.add_map_link = self.kwargs.get('map_link', False)
        self.add_rlet_link = self.kwargs.get('rlet_link', False)
        
        if (self.add_get_address or 
            self.add_get_ETA or
            self.add_get_map_link
            ):
            application_key = get_application_key()
            self.headers_post = {
                'X-NCP-APIGW-API-KEY-ID': application_key['client_id'],
                'X-NCP-APIGW-API-KEY': application_key['client_secret'],
            }
        
    def get_basic_data(self, district_code):
        total_data = []
        params = deepcopy(self.query_params)
        
        params['cortarNo'] = district_code
        params['page'] = 1
        continue_ = True
        
        
        while continue_:
            response = requests.get(
                url=self.url, 
                params=params, 
                headers=self.headers,
                )
            
            # check response status
            if response.status_code == 200:
                data_dic = response.json()
                
                # check there is more data
                if not data_dic['more']:
                    break
                
                total_data += data_dic['body']
                
                params['page'] += 1
                
            else:
                print(f"Failed to retrieve data: {response.status_code}")
                break
                
        return total_data
    
    def get_detail_data(self, basic_data):
        total_detail_data = []
        
        for data in basic_data:
            params = {
                "articleId":data["atclNo"],
                "realEstateType":data["rletTpCd"],
                "tradeType":data["tradTpCd"],
            }
            
            response = requests.get(
                url=self.detail_url, 
                params=params, 
                headers=self.headers,
                )
            
            # check response status
            if response.status_code == 200:
                data_dic = response.json()
                # check there is more data
                if not data_dic['isSuccess']:
                    break
                total_detail_data.append(data_dic)
                
        return total_detail_data
            
    def find_all_values_with_keys(self, dict_, current_path=None):
        if current_path is None:
            current_path = []
        values_with_keys = []
        for key, value in dict_.items():
            new_path = current_path + [key]
            if isinstance(value, dict):
                values_with_keys.extend(self.find_all_values_with_keys(value, new_path))
            else:
                values_with_keys.append((new_path, value))
        return values_with_keys
            
    def decode_to_dataframe(self, basic_data, detail_data):
        basic_columns = self.decode_key["basic"].values()
        detail_keys, detail_columns = zip(*self.find_all_values_with_keys(self.decode_key["detail"]))
        columns = list(basic_columns) + list(detail_columns)
        
        decode_dict = {key:[] for key in columns}
        
        for i, basic_ in enumerate(basic_data):
            # print(basic_)
            values = [basic_[k] if k in basic_.keys() else None for k in self.decode_key["basic"].keys()]
            
            for keys in detail_keys:
                value = deepcopy(detail_data[i])
                for key in keys:
                    value = value[key]
                values += [value]
            
            for i, col in enumerate(columns):
                decode_dict[col].append(values[i])
        
        df = pd.DataFrame(decode_dict)
        
        return df
    
    def request_address(self, lat, lng):
        add = ''
        orders = "addr"     # 지번
        url = f"{reverse_gc_url}?coords={lng},{lat}&output=json&orders={orders}"
        
        response = requests.get(
                    url,
                    headers=self.headers_post,
                    )
        
        # 응답 상태 코드 확인
        if response.status_code == 200:
            # JSON 데이터 파싱
            data_dic = response.json()
            if len(data_dic['results']) != 0:
            
                add += data_dic['results'][0]['region']['area3']['name'] + ' '
                area4 = data_dic['results'][0]['region']['area4']['name']
                if area4 != '':
                    add += area4 + ' '
                
                type_ = data_dic['results'][0]['land']['type']
                if type_ == '2':
                    add += '산 '
                
                add += data_dic['results'][0]['land']['number1']
                
                num2 = data_dic['results'][0]['land']['number2']
                if num2 != '':
                    add += '-' + num2
                    
            else:
                print(f"Failed to retrieve data: {response.status_code}, {response.text}")
                
        return add
    
        
    def get_address(self, df):
        df['주소'] = ''
        
        # orders = "roadaddr" # 도로명
        print(f"[I] 토지 주소 변환 중...")
        for i in tqdm(range(len(df))):
            
            row = df.iloc[i]
            lat = str(row['위도'])
            lng = str(row['경도'])
            
            add = self.request_address(lat, lng)
            
            df.iloc[i, df.columns.get_loc("주소")] = add
        
        return df
    
    def request_ETA(self, start_lat, start_lng, goal_lat, goal_lng):
        eta_m = ''
        params = {
            "start": f"{start_lng},{start_lat}",
            "goal": f"{goal_lng},{goal_lat}",
            "option": "trafast",     # 빠른 경로를 위한 옵션
            # "option": "traoptimal",  # 최적 경로를 위한 옵션
        }
        
        response = requests.get(
                    driving_url, 
                    params=params,
                    headers=self.headers_post,
                    )
        
        # 응답 상태 코드 확인
        if response.status_code == 200:
            # JSON 데이터 파싱
            data_dic = response.json()
            
            if data_dic['code'] == 0:
                request_time = data_dic['currentDateTime']
                eta_ms = data_dic['route'][params['option']][0]['summary']['duration']
                eta_m = (eta_ms // 1000) // 60
                
        else:
            print(f"Failed to retrieve data: {response.status_code}, {response.text}")
                
        return eta_m, request_time
        
    def get_ETA(self, df, start="강남역"):
        if start == "강남역":
            start_lat = '37.498716'
            start_lng = '127.027021'
        else:
            raise NotImplementedError("[E] Starting points other than Gangnam Station are not implemented or provided.")
        
        df['소요시간(분)'] = ''
        df['소요시간 탐색 시각'] = ''
        
        print(f"[I] 소요시간 (from {start}) 계산 중...")
        for i in tqdm(range(len(df))):
            
            row = df.iloc[i]
            lat = str(row['위도'])
            lng = str(row['경도'])
            
            eta_m, request_time = self.request_ETA(start_lat, start_lng, lat, lng)
            
            df.iloc[i, df.columns.get_loc("소요시간(분)")] = eta_m
            df.iloc[i, df.columns.get_loc("소요시간 탐색 시각")] = request_time
        
        return df
    
    def get_map_link(self, df):
        map_url = "https://map.naver.com/p/search/"
        df["네이버지도"] = ''
        
        print(f"[I] 네이버지도 링크 생성 중...")
        for i in tqdm(range(len(df))):
            
            row = df.iloc[i]
            add = str(row['주소']).split(" ")
            url = map_url
            for add in str(row['주소']).split(" "):
                url += add + "%20"
            
            df.iloc[i, df.columns.get_loc("네이버지도")] = f'=HYPERLINK("{url[:-3]}", "링크")'
        
        return df

    def get_rlet_link(self, df):
        rlet_url = "https://fin.land.naver.com/articles/"
        df["네이버부동산"] = ''
        
        print(f"[I] 네이버부동산 링크 생성 중...")
        for i in tqdm(range(len(df))):
            
            row = df.iloc[i]
            no_atcl = str(row['매물번호'])
            
            url = rlet_url + no_atcl
            
            df.iloc[i, df.columns.get_loc("네이버부동산")] = f'=HYPERLINK("{url}", "링크")'
        
        return df
        
    def post_processing(self, df):
        if self.add_get_ETA:
            df = self.get_ETA(df)
        if self.add_get_address:
            df = self.get_address(df)
        if self.add_map_link:
            if not self.add_get_address:
                raise KeyError("[E] 링크를 추가하려면 주소 기능을 활성화하세요.")
            df = self.get_map_link(df)
        if self.add_rlet_link:
            df = self.get_rlet_link(df)
        
        return df
        
        
    def get_n_save_data(self, district_codes, save_dir=os.path.join(os.path.expanduser("~"), "Downloads", "LandScout")):
        for i, code in enumerate(district_codes):
            
            code_name = get_district_name(code)
            print(f"[I] ({i+1}/{len(district_codes)}) {code_name} 작업 중...")
            
            
            # get basic data
            basic_data = self.get_basic_data(code)
            if len(basic_data) < 1:
                print(f"[I] {code_name}: There is no valid data.")
                continue
            
            # get detail data
            detail_data = self.get_detail_data(basic_data)
            if len(basic_data) != len(detail_data):
                print(f"[I] [{code_name}] Failed to retrieve detailed information. # of basic info: {len(basic_data)} / # of detail info: {len(detail_data)} ")
                continue
                
            df = self.decode_to_dataframe(basic_data, detail_data)
            print(f"[I] {code_name} 토지 검색 완료 (총 {len(basic_data)} 도출).")
            
            # post processing
            if sum(self.kwargs.values()) > 0:
                df = self.post_processing(df)
            
            if not os.path.isdir(save_dir):
                os.makedirs(save_dir)
                
            df.to_csv(os.path.join(save_dir, f'{code_name}.csv'), index=False, encoding="utf-8-sig")
            print(f"[I] {code_name} 저장 완료.")