
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