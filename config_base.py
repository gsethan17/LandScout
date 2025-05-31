
param_name = {}

param_name["realEstateType"] = "부동산 형태"
param_name["tradeType"] = "거래 형태"
param_name["cortarNo"] = "탐색 지역 (법정동명)"
param_name["priceMin"] = "최소 가격 (만원)"
param_name["priceMax"] = "최대 가격 (만원)"
param_name["areaMin"] = "최소 면적 (m^2)"
param_name["areaMax"] = "최대 면적 (m^2)"

param_name["APT"] = "아파트"
param_name["TJ"] = "토지"
param_name["OPST"] = "오피스텔"

param_name["A1"] = "매매"


decode_key = {
    "basic":{
        "articleName":"지목",
        "realEstateTypeName":"부동산형태",
        "tradeTypeName":"거래형태",
        "area1":"대지면적(m^2)",
        "area2":"연면적(m^2)",
        "articleConfirmYmd":"매물확인일자",
        "latitude":"위도",
        "longitude":"경도",
        "articleFeatureDesc":"설명",
        "articleNo":"매물번호",
    },
    
    "detail":{
        "articlePrice":{
            "dealPrice":"가격(만원)",
            "financePrice":"융자금(만원)",
        },
        "articleDetail":{
            "currentUsage":"현재용도",
            "recommendUsage":"추천용도",
        },
        "articleFacility":{
            "usageTypeName":"용도지역",
            "countryUsageYN":"국토이용",
            "cityPlanYN":"도기계획",
            "buildingAllowedYN":"건축허가",
            "groundTradeAllowedYN":"토지거래허가구역",
            "raodYN":"진입도로",
        },
        
    },
    
}