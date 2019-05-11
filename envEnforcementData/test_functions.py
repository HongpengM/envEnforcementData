import pandas as pd
import os; import os.path as osp
from settings import  ENTRY_URLS_FILE


def test_read_entry_urls():
    file_path = osp.join('..',ENTRY_URLS_FILE)
    df = pd.read_excel(file_path)
    print(df)
    
def main():
    test_read_entry_urls()

if __name__ == '__main__':
    main()


