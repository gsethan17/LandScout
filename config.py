
param_name = {}
param_name["rletTpCd"] = "부동산 형태"
param_name["tradTpCd"] = "거래 형태"
param_name["cortarNo"] = "탐색 지역 (법정동명)"
param_name["dprcMin"] = "최소 가격 (만원)"
param_name["dprcMax"] = "최대 가격 (만원)"
param_name["spcMin"] = "최소 면적 (m^2)"
param_name["spcMax"] = "최대 면적 (m^2)"

param_name["APT"] = "아파트"
param_name["TJ"] = "토지"
param_name["OPST"] = "오피스텔"

param_name["A1"] = "매매"


params = {}

# 부동산 타입
params["rletTpCd"] = [
    # "APT",  # 아파트
    "TJ",   # 토지
    # "OPST", # 오피스텔
]

# 거래 타입
params["tradTpCd"] = [
    "A1",   # 매매
]

# 탐색 지역 (법정동명) 
# ref. https://www.code.go.kr/stdcode/regCodeL.do
params["cortarName"] = [
    # "경기도 가평군",
    # "경기도 양평군",
    # "강원특별자치도 춘천시",
    # "강원특별자치도 화천군",
    # "강원특별자치도 홍천군",
    # "강원특별자치도 평창군",
    # "경상북도 양주시",
    # "충청북도 단양군",
    "경기도 이천시",
    # "경기도 포천시",
    # "경기도 여주시",
]

# 가격 (만원)
params["dprcMin"] = "10000",
params["dprcMax"] = "25000",

# 면적 (m^2) 3.3
spcMin = []
spcMax = []
# # 50
# spcMax.append(165)
# # 100
# spcMin.append(165)
# spcMax.append(331)
# # 200
# spcMin.append(331)
# spcMax.append(661)
# 300
spcMin.append(661)
spcMax.append(992)
# 400
spcMin.append(992)
spcMax.append(1322)
# 500
spcMin.append(1322)
spcMax.append(1653)
# # 600
# spcMin.append(1653)
# spcMax.append(1983)
# # 700
# spcMin.append(1983)
# spcMax.append(2314)
# # 800
# spcMin.append(2314)
# spcMax.append(2645)
# # 900
# spcMin.append(2645)
# spcMax.append(2975)
# # 1000
# spcMin.append(2975)
# spcMax.append(3306)
# # 1000~
# spcMin.append(3306)
# spcMax.append(900000000)

if len(spcMin) > 0:
    params["spcMin"] = [str(min(spcMin))]
if len(spcMax) > 0:
    params["spcMax"] = [str(max(spcMax))]


# # 대상 URL

decode_key = {
    "basic":{
        "atclNm":"지목",
        "rletTpNm":"부동산형태",
        "tradTpNm":"거래형태",
        "spc1":"대지면적(m^2)",
        "spc2":"연면적(m^2)",
        "atclCfmYmd":"매물확인일자",
        "lat":"위도",
        "lng":"경도",
        "atclFetrDesc":"설명",
        # "tagList":"키워드",
        "rltrNm":"부동산",
    },
    
    "detail":{
        "result":{
            "priceInfo":{
                "price":"가격(원)",
            },
            
            "detailInfo":{
            #     "articleDetailInfo":{
            #         "articleName":"지목",
            #         "articleFeatureDescription":"특징",
            #         "articleDescription":"설명",
            #     }
                "spaceInfo":{
                    "currentPurpose":"현재용도",
                    "recommendedPurpose":"추천용도",
                    "areaUsage":"용도지역",
                    "landUsage":"국토용도",
                    "cityPlan":"도시계획",
                    "buildingPermission":"건축허가",
                    "landTradePermission":"거래허가",
                    "approachRoad":"진입도로",
                },
            },
            
        },
    },
    
}