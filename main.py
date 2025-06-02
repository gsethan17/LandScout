from copy import deepcopy

from utils import terminate
from utils import get_district_dict

from query import WebQueryClient
from config_base import decode_key

from gui import SearchConditionSelectionApp
from gui import DistrictNOptionSelectionApp

if __name__ == "__main__":
    app1 = SearchConditionSelectionApp()
    app1.root.mainloop()
    params1 = deepcopy(app1.results)
    
    district_dict = get_district_dict()
    app2 = DistrictNOptionSelectionApp(district_dict=district_dict)
    app2.root.mainloop()
    params2 = deepcopy(app2.results)
    
    params = params1 | params2
    
    # raise BrokenPipeError()
    if len(params) < 1:
        raise BrokenPipeError()

    client = WebQueryClient(
        params=params,
        decode_key=decode_key,
        address=params['address'][0] == 'True',
        ETA=params['ETA'][0] == 'True', 
        rlet_link=params['rlet_link'][0] == 'True', 
        map_link=params['map_link'][0] == 'True', 
        verbose=0,
        )
    
    client.get_n_save_data()
    