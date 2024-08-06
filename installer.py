from utils import build_exe
import os

if __name__ == "__main__":
    file_ = "main.py"
    path_ = os.path.join(os.path.dirname(__file__), file_)
    
    build_exe(path_)