import pandas as pd
import os; import os.path as osp
import yaml
from envEnforcementData.settings import ENTRY_URLS_FILE


def loadEntryUrls(path):
    df = pd.read_excel(path)
    print(ENTRY_URLS_FILE)
    return df


def main():
    
    loadEntryUrls('../entryUrls.xlsx')
    
if __name__ == '__main__':
    main()
