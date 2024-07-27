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
    
    
    
if __name__ == "__main__":
    code = '2920000000'
    name = get_district_name(code=code)
    print(name)
    