import tkinter as tk
from tkinter import font
# from tkinter import messagebox
from config_base import param_name
from utils import get_district_code, get_district_name

class SearchConditionSelectionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.results = {}
        
        self.title = "LandScout"
        self.window_size = "650x500"
        
        self.H1_title = "탐색 조건 설정"
        self.H1_font_size = 18
        
        self.font_size = 12
        self.root.option_add("*Font", f"TkDefaultFont {self.font_size}")
        
        self.height_blank = 5
        self.width_blank = 30
        
        # param name #
        self.name_switch = {}
        for k, v in param_name.items():
            self.name_switch[v] = k
        
        # --- Variables to store selected/entered data ---
        self.listbox1_title = "부동산 형태 (realEstateType)"
        self.listbox1_items = ["토지"]
        self.selected_listbox1_items = []
        
        self.listbox2_title = "거래 형태 (tradeType)"
        self.listbox2_items = ["매매"]
        self.selected_listbox2_items = []
        
        self.entry1_title = "최소 가격 [만원] (priceMin)"
        self.entry2_title = "최대 가격 [만원] (priceMax)"
        self.entry3_title = "최소 면적 [m^2] (areaMin)"
        self.entry4_title = "최대 면적 [m^2] (areaMax)"
        
        self.root.title(self.title)
        self.root.geometry(self.window_size) # Adjust window size as needed

        # --- Create and place widgets ---
        
        # --- 큰 제목 추가 ---
        # 폰트 설정: 'Helvetica' 폰트, 크기 24, 볼드체
        title_font = font.Font(family="Helvetica", size=self.H1_font_size, weight="bold")
        tk.Label(self.root, text=self.H1_title, font=title_font, fg="navy").pack(pady=(20, 10)) # 제목 색상 추가 (선택 사항)
        # --- 제목 추가 끝 ---
        
        # --- 메인 프레임 생성: 좌우 두 단을 담을 프레임 ---
        # 이 프레임은 전체 창의 중앙에 배치됩니다.
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, fill="both", expand=True) # fill과 expand로 프레임이 창 크기에 맞게 확장되도록

        # --- 왼쪽 프레임 (다중 선택 리스트박스) ---
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew") # sticky로 프레임이 셀 안에서 확장되도록

        # Listbox 1 (Multi-select)
        tk.Label(left_frame, text=self.listbox1_title).pack(pady=(10, 0))
        self.listbox1 = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, height=self.height_blank, width=self.width_blank, exportselection=False)
        for item in self.listbox1_items:
            self.listbox1.insert(tk.END, item)
        self.listbox1.pack(pady=5)
        self.listbox1.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Listbox 2 (Multi-select)
        tk.Label(left_frame, text=self.listbox2_title).pack(pady=(10, 0))
        self.listbox2 = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, height=self.height_blank, width=self.width_blank, exportselection=False)
        for item in self.listbox2_items:
            self.listbox2.insert(tk.END, item)
        self.listbox2.pack(pady=5)
        self.listbox2.bind("<<ListboxSelect>>", self.on_listbox_select)
        
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew") # sticky로 프레임이 셀 안에서 확장되도록

        # Entry Field 1
        tk.Label(right_frame, text=self.entry1_title).pack(pady=(10, 0))
        self.entry1 = tk.Entry(right_frame, width=self.width_blank)
        self.entry1.pack(pady=5)

        # Entry Field 2
        tk.Label(right_frame, text=self.entry2_title).pack(pady=(10, 0))
        self.entry2 = tk.Entry(right_frame, width=self.width_blank)
        self.entry2.pack(pady=5)

        # Entry Field 3
        tk.Label(right_frame, text=self.entry3_title).pack(pady=(10, 0))
        self.entry3 = tk.Entry(right_frame, width=self.width_blank)
        self.entry3.pack(pady=5)

        # Entry Field 4
        tk.Label(right_frame, text=self.entry4_title).pack(pady=(10, 0))
        self.entry4 = tk.Entry(right_frame, width=self.width_blank)
        self.entry4.pack(pady=5)

        # Confirm Button
        tk.Button(self.root, text="확인", command=self.on_confirm).pack(pady=20)

    def on_listbox_select(self, event):
        # Determine which listbox triggered the event
        widget = event.widget
        selected_items_list = []
        
        # Clear previous selections for the respective listbox before re-populating
        if widget == self.listbox1:
            self.selected_listbox1_items = []
        elif widget == self.listbox2:
            self.selected_listbox2_items = []

        # Get all selected indices
        selected_indices = widget.curselection()

        # Update visual feedback (blue background for selected items)
        for i in range(widget.size()):
            if i in selected_indices:
                widget.itemconfig(i, {'bg': 'light blue'})
                selected_items_list.append(widget.get(i))
            else:
                widget.itemconfig(i, {'bg': 'white'}) # Reset unselected items to white

        # Store selected items
        if widget == self.listbox1:
            self.selected_listbox1_items = selected_items_list
        elif widget == self.listbox2:
            self.selected_listbox2_items = selected_items_list
            
    def on_confirm(self):
        self.results["realEstateType"] = [self.name_switch[item] for item in self.selected_listbox1_items]
        self.results["tradeType"] = [self.name_switch[item] for item in self.selected_listbox2_items]
        # Get data from entry fields
        
        entry_list = [self.entry1, self.entry2, self.entry3, self.entry4]
        entry_name = ["priceMin", "priceMax", "areaMin", "areaMax"]
        for entry, name in zip(entry_list, entry_name):
            data = [entry.get()]
            if not data[0]:
                if name[-3:] == "Min":
                    data = ['0']
                elif name[-3:] == "Max":
                    data = ['900000000']
                    
            self.results[name] = data
        
        self.root.destroy()
        

class DistrictNOptionSelectionApp:
    def __init__(self, district_dict):
        self.root = tk.Tk()
        self.results = {}
        
        self.title = "LandScout"
        self.window_size = "650x650"
        
        self.H1_title = "탐색 지역 및 옵션 설정"
        self.H1_font_size = 18
        
        # --- 전체 폰트 크기 설정 ---
        self.font_size = 12
        self.root.option_add("*Font", f"TkDefaultFont {self.font_size}")
        
        self.height_blank = 10
        self.width_blank = 20
        
        self.title_level1 = "시도"
        self.title_level2 = "시군구"
        self.title_level3 = "읍면동"
        
        self.title_address = "지번주소"
        self.title_map_link = "네이버맵 링크"
        self.title_rlet_link = "네이버부동산 링크"
        self.title_ETA = "이동시간 (강남역 출발)"
        
        self.default_address = True
        self.default_map_link = True
        self.default_rlet_link = True
        self.default_ETA = False
        
        self.root.title(self.title)
        self.root.geometry(self.window_size) # 체크박스 추가로 세로 길이를 더 늘림

        # --- 창 닫기 프로토콜 설정 (X 버튼 클릭 시 확인) ---
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.district_dict = district_dict # 외부에서 받은 딕셔너리 저장

        # --- 선택된 항목을 저장할 변수 (계층적 선택) ---
        self.selected_level1 = None
        self.selected_level2 = None
        self.selected_level3 = None

        # --- 체크박스 상태를 저장할 변수 ---
        self.checkbox_var1 = tk.BooleanVar(value=self.default_address)  # 첫 번째 체크박스: 기본값 True
        self.checkbox_var2 = tk.BooleanVar(value=self.default_map_link) # 두 번째 체크박스: 기본값 False
        self.checkbox_var3 = tk.BooleanVar(value=self.default_rlet_link) # 세 번째 체크박스: 기본값 False
        self.checkbox_var4 = tk.BooleanVar(value=self.default_ETA) # 네 번째 체크박스: 기본값 False (비활성화 예정)

        # --- 상단 큰 제목 ---
        title_font = font.Font(family="Helvetica", size=self.H1_font_size, weight="bold")
        tk.Label(self.root, text=self.H1_title, font=title_font, fg="darkblue").pack(pady=(20, 15))

        # --- 계층적 선택 영역 (기존 main_columns_frame) ---
        # 이 프레임은 상단에 위치하며 세로로 확장되지 않도록 함
        hierarchical_frame = tk.Frame(self.root)
        hierarchical_frame.pack(pady=(0, 20), fill="x", expand=False) # 가로만 채움

        # --- 각 컬럼 프레임 및 리스트박스 생성 ---
        col1_frame = tk.Frame(hierarchical_frame)
        col1_frame.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        tk.Label(col1_frame, text=self.title_level1).pack(pady=(5, 0))
        self.listbox1 = tk.Listbox(col1_frame, selectmode=tk.BROWSE, height=self.height_blank, exportselection=False, width=self.width_blank)
        self.listbox1.pack(pady=5, fill="both", expand=True)
        self.listbox1.bind("<<ListboxSelect>>", self.on_listbox1_select)
        self.listbox1.bind("<ButtonRelease-1>", self.on_listbox1_click)

        col2_frame = tk.Frame(hierarchical_frame)
        col2_frame.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")
        tk.Label(col2_frame, text=self.title_level2).pack(pady=(5, 0))
        self.listbox2 = tk.Listbox(col2_frame, selectmode=tk.BROWSE, height=self.height_blank, exportselection=False, width=self.width_blank)
        self.listbox2.pack(pady=5, fill="both", expand=True)
        self.listbox2.bind("<<ListboxSelect>>", self.on_listbox2_select)
        self.listbox2.bind("<ButtonRelease-1>", self.on_listbox2_click)

        col3_frame = tk.Frame(hierarchical_frame)
        col3_frame.grid(row=0, column=2, padx=15, pady=10, sticky="nsew")
        tk.Label(col3_frame, text=self.title_level3).pack(pady=(5, 0))
        self.listbox3 = tk.Listbox(col3_frame, selectmode=tk.BROWSE, height=self.height_blank, exportselection=False, width=self.width_blank)
        self.listbox3.pack(pady=5, fill="both", expand=True)
        self.listbox3.bind("<<ListboxSelect>>", self.on_listbox3_select)
        self.listbox3.bind("<ButtonRelease-1>", self.on_listbox3_click)

        # --- Grid 컬럼 가중치 설정 (세 컬럼이 동일한 비율로 확장) ---
        hierarchical_frame.grid_columnconfigure(0, weight=1)
        hierarchical_frame.grid_columnconfigure(1, weight=1)
        hierarchical_frame.grid_columnconfigure(2, weight=1)

        # --- 체크박스 영역 ---
        checkbox_frame = tk.Frame(self.root)
        checkbox_frame.pack(pady=10, fill="x", expand=False) # 가로만 채움

        tk.Label(checkbox_frame, text="추가 옵션 선택:", font=font.Font(size=14, weight="bold")).pack(anchor="w", padx=30, pady=(10, 5))

        self.chk_btn1 = tk.Checkbutton(checkbox_frame, text=self.title_address, variable=self.checkbox_var1)
        self.chk_btn1.pack(anchor="w", padx=50, pady=5)

        self.chk_btn2 = tk.Checkbutton(checkbox_frame, text=self.title_map_link, variable=self.checkbox_var2)
        self.chk_btn2.pack(anchor="w", padx=50, pady=5)

        self.chk_btn3 = tk.Checkbutton(checkbox_frame, text=self.title_rlet_link, variable=self.checkbox_var3)
        self.chk_btn3.pack(anchor="w", padx=50, pady=5)

        self.chk_btn4 = tk.Checkbutton(checkbox_frame, text=self.title_ETA, variable=self.checkbox_var4) #, state=tk.DISABLED)
        self.chk_btn4.pack(anchor="w", padx=50, pady=5)


        # --- 확인 버튼 ---
        tk.Button(self.root, text="확인", command=self.on_confirm).pack(pady=20)

        # --- 초기 데이터 로드 (Listbox1) ---
        self._populate_listbox1()

    def _populate_listbox1(self):
        """첫 번째 리스트박스를 딕셔너리의 최상위 키로 채웁니다."""
        self.listbox1.delete(0, tk.END)
        for key in self.district_dict.keys():
            self.listbox1.insert(tk.END, key)
        self.selected_level1 = None
        self._clear_selection_visual(self.listbox1)

    def _populate_listbox2(self, selected_key1):
        """두 번째 리스트박스를 첫 번째 선택에 따라 채웁니다."""
        self.listbox2.delete(0, tk.END)
        self._clear_selection_visual(self.listbox2)
        self.selected_level2 = None
        self.listbox3.delete(0, tk.END)
        self._clear_selection_visual(self.listbox3)
        self.selected_level3 = None

        if selected_key1 and selected_key1 in self.district_dict:
            for key in self.district_dict[selected_key1].keys():
                self.listbox2.insert(tk.END, key)

    def _populate_listbox3(self, selected_key1, selected_key2):
        """세 번째 리스트박스를 첫 번째 및 두 번째 선택에 따라 채웁니다."""
        self.listbox3.delete(0, tk.END)
        self._clear_selection_visual(self.listbox3)
        self.selected_level3 = None

        if selected_key1 and selected_key2 and \
            selected_key1 in self.district_dict and \
            selected_key2 in self.district_dict[selected_key1]:
            for item in self.district_dict[selected_key1][selected_key2]:
                self.listbox3.insert(tk.END, item)

    def _clear_selection_visual(self, listbox_widget):
        """주어진 리스트박스의 모든 시각적 선택(파란색 음영)을 해제합니다."""
        for i in range(listbox_widget.size()):
            listbox_widget.itemconfig(i, {'bg': 'white'})

    def on_listbox1_select(self, event): pass 
    def on_listbox1_click(self, event):
        current_selection = self.listbox1.curselection()
        if current_selection:
            selected_idx = current_selection[0]
            item = self.listbox1.get(selected_idx)
            if self.selected_level1 == item:
                self.listbox1.selection_clear(0, tk.END)
                self._clear_selection_visual(self.listbox1)
                self.selected_level1 = None
                self._populate_listbox2(None)
            else:
                self._clear_selection_visual(self.listbox1)
                self.listbox1.itemconfig(selected_idx, {'bg': 'light blue'})
                self.selected_level1 = item
                self._populate_listbox2(self.selected_level1)
        else:
            pass # 선택 해제 로직은 클릭한 항목이 있을 때만 동작

    def on_listbox2_select(self, event): pass
    def on_listbox2_click(self, event):
        current_selection = self.listbox2.curselection()
        if current_selection:
            selected_idx = current_selection[0]
            item = self.listbox2.get(selected_idx)
            if self.selected_level2 == item:
                self.listbox2.selection_clear(0, tk.END)
                self._clear_selection_visual(self.listbox2)
                self.selected_level2 = None
                self._populate_listbox3(self.selected_level1, None)
            else:
                self._clear_selection_visual(self.listbox2)
                self.listbox2.itemconfig(selected_idx, {'bg': 'light blue'})
                self.selected_level2 = item
                self._populate_listbox3(self.selected_level1, self.selected_level2)
        else:
            pass

    def on_listbox3_select(self, event): pass
    def on_listbox3_click(self, event):
        current_selection = self.listbox3.curselection()
        if current_selection:
            selected_idx = current_selection[0]
            item = self.listbox3.get(selected_idx)
            if self.selected_level3 == item:
                self.listbox3.selection_clear(0, tk.END)
                self._clear_selection_visual(self.listbox3)
                self.selected_level3 = None
            else:
                self._clear_selection_visual(self.listbox3)
                self.listbox3.itemconfig(selected_idx, {'bg': 'light blue'})
                self.selected_level3 = item
        else:
            pass

    def on_confirm(self):
        """확인 버튼 클릭 시 모든 선택 및 체크박스 정보를 반환합니다."""
        self.results['cortarName'] = f"{self.selected_level1}"
        if self.selected_level2:
            self.results['cortarName'] += f" {self.selected_level2}"
        if self.selected_level3:
            self.results['cortarName'] += f" {self.selected_level3}"
            
        # self.results['cortarCode'] = get_district_code(self.results['cortarName'])
        self.results['cortarName'] = [self.results['cortarName']]
        
        # 체크박스 선택 결과
        checkbox_list = [self.checkbox_var1, self.checkbox_var2, self.checkbox_var3, self.checkbox_var4]
        checkbox_name = ["address", "map_link", "rlet_link", "ETA"]
        
        for checkbox, name in zip(checkbox_list, checkbox_name):
            self.results[name] = [str(checkbox.get())]
            
        self.root.destroy()
        
        
from tkinter import filedialog, messagebox
class SaveLocationApp:
    def __init__(self):
        self.root = root = tk.Tk()
        self.selected_file_path = False
        
        self.title = "LandScout"
        self.H1_title = "파일 저장 위치 선택"
        
        self.H1_font_size = 18
        
        # --- 전체 폰트 크기 설정 ---
        self.font_size = 12
        self.root.option_add("*Font", f"TkDefaultFont {self.font_size}")
        
        self.root.title(self.title)
        self.root.geometry("650x300")

        # --- 큰 제목 ---
        title_font = font.Font(family="Helvetica", size=self.H1_font_size, weight="bold")
        tk.Label(root, text=self.H1_title, font=title_font, fg="blue").pack(pady=(20, 15))

        # --- 선택된 경로를 표시할 레이블 ---
        self.path_label = tk.Label(root, text="선택된 경로: 없음", wraplength=400)
        self.path_label.pack(pady=10)

        # --- 찾아보기 버튼 ---
        tk.Button(root, text="폴더 및 파일명 선택", command=self.select_save_location).pack(pady=10)

        # --- 최종 확인 버튼 ---
        tk.Button(root, text="확인", command=self.on_confirm).pack(pady=10)

    def select_save_location(self):
        """사용자로부터 .xlsx 파일 저장 위치를 받아옵니다."""
        # asksaveasfilename을 사용하여 파일명까지 포함하여 경로를 받음
        # defaultextension: 사용자가 확장자를 입력하지 않아도 자동으로 .xlsx를 붙임
        # filetypes: 저장할 수 있는 파일 확장자 필터
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Excel 파일 저장 위치 선택"
        )
        if file_path:
            self.selected_file_path = file_path
            self.path_label.config(text=f"선택된 경로: {self.selected_file_path}")
        else:
            self.selected_file_path = None
            self.path_label.config(text="선택된 경로: 없음")

    def on_confirm(self):
        """확인 버튼 클릭 시 선택된 경로를 반환합니다."""
        if self.selected_file_path:
            self.root.destroy() # 확인 후 창 닫기
        else:
            messagebox.showwarning("경고", "저장할 파일 경로를 선택해주세요.")
            
class IDPWSecurityApp:
    def __init__(self):
        self.root = tk.Tk()
        
        self.title = "LandScout"
        self.H1_title = "로그인 정보 입력"
        
        self.H1_font_size = 18
        
        # --- 전체 폰트 크기 설정 ---
        self.font_size = 12
        self.root.option_add("*Font", f"TkDefaultFont {self.font_size}")
        
        self.root.title(self.title)
        self.root.geometry("650x300")

        # --- 큰 제목 ---
        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        tk.Label(self.root, text=self.H1_title, font=title_font, fg="darkgreen").pack(pady=(20, 30))

        # --- ID 입력 필드 ---
        id_frame = tk.Frame(self.root)
        id_frame.pack(pady=5)
        tk.Label(id_frame, text="ID:").pack(side=tk.LEFT, padx=5)
        self.id_entry = tk.Entry(id_frame, width=25)
        self.id_entry.pack(side=tk.LEFT, padx=5)

        # --- PW 입력 필드 ---
        pw_frame = tk.Frame(self.root)
        pw_frame.pack(pady=5)
        tk.Label(pw_frame, text="PW:").pack(side=tk.LEFT, padx=0)
        self.pw_entry = tk.Entry(pw_frame, width=25, show="*") # 초기에는 '*'로 비식별
        self.pw_entry.pack(side=tk.LEFT, padx=5)

        # --- PW 식별/비식별 체크박스 ---
        self.show_pw_var = tk.BooleanVar(value=False) # 기본값: 비식별 (체크 해제 상태)
        self.show_pw_checkbox = tk.Checkbutton(
            self.root, 
            text="비밀번호 보기", 
            variable=self.show_pw_var, 
            command=self.toggle_password_visibility
        )
        self.show_pw_checkbox.pack(pady=5, anchor="e", padx=190) # 오른쪽에 정렬

        # --- 확인 버튼 ---
        tk.Button(self.root, text="로그인", command=self.on_login_confirm).pack(pady=20)

    def toggle_password_visibility(self):
        """비밀번호 필드의 식별/비식별 상태를 전환합니다."""
        if self.show_pw_var.get(): # 체크박스가 체크되면 (비밀번호 보기)
            self.pw_entry.config(show="") # 문자가 보이도록 show 옵션을 빈 문자열로 설정
        else: # 체크박스가 체크 해제되면 (비밀번호 숨기기)
            self.pw_entry.config(show="*") # '*'로 비식별

    def on_login_confirm(self):
        """로그인 버튼 클릭 시 ID와 PW를 반환합니다."""
        self.user_id = self.id_entry.get()
        self.user_pw = self.pw_entry.get()

        if not self.user_id:
            messagebox.showwarning("입력 오류", "ID를 입력해주세요.")
            return
        if not self.user_pw:
            messagebox.showwarning("입력 오류", "비밀번호를 입력해주세요.")
            return

        self.root.destroy() # 확인 후 창 닫기
        
# 메인 윈도우 생성 및 앱 실행
from utils import get_district_dict
if __name__ == "__main__":
    '''
    Create the main window
    app = SearchConditionSelectorApp()
    app.root.mainloop()
    print(app.results)
    '''
    
    '''
    sample_data = get_district_dict()
    app = DistrictNOptionSelectionApp(district_dict=sample_data)
    app.root.mainloop()
    print(app.results)
    '''

    '''
    app = SaveLocationApp()
    app.root.mainloop()
    '''

    app = IDPWSecurityApp()
    app.root.mainloop()

    print(app.user_id, app.user_pw)