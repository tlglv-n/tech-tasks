import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO

def make_request(url, max_retries=5, wait_time=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  
            return response
        except requests.RequestException as e:
            print(f"Request error: {e}. Retry {retries + 1} in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
    print("Max retries reached, request failed.")
    return None

def extract_data(link):
    response = make_request(link)
    if not response:
        return pd.DataFrame({'Address': [None]})

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    
    if len(tables) < 4:
        return pd.DataFrame({'Address': [None]})

    df1 = pd.read_html(StringIO(str(tables[2])))[0].drop([1, 1]).T.drop([0, 0]).reset_index()
    df1.columns = ['index', 'ИИН Руководителя', 'ФИО']
    
    df2 = pd.read_html(StringIO(str(tables[3])))[0]
    extracted_col = df2["Полный адрес(рус)"].str.cat(sep='; ')
    
    new_dataframe = pd.concat([df1, pd.Series([extracted_col], name="Address")], axis=1).drop(['index'], axis=1)
    return new_dataframe

def main():
    url = "https://www.goszakup.gov.kz/ru/registry/rqc?count_record=2000&page=1"
    response = make_request(url)
    
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')[0]
        final_df = pd.read_html(StringIO(str(table)))[0].drop_duplicates(subset=['Наименование потенциального поставщика'])
        
        dfs = []
        for row in table.find_all('tr'):
            for link in row.find_all('a', href=True):
                df = extract_data(link['href'])
                dfs.append(df)
                
                print(f"Processed link: {link['href']}")
                print(f"Current DataFrame shape: {df.shape}")
                
                time.sleep(3)
        
        big_dataframe = pd.concat(dfs, ignore_index=True)
        result_df = pd.concat([final_df, big_dataframe], axis=1)
        result_df = result_df.drop(['Наименование, номер и дата выдачи документа, на основании которого потенциальный поставщик включен в Перечень', '№'], axis=1)
        result_df = result_df.drop_duplicates(subset=['Наименование потенциального поставщика'])
        result_df.reset_index(drop=True, inplace=True)
        
        result_df.to_excel('result.xlsx', index=False, engine='openpyxl')
        print("Data successfully saved to result.xlsx")

if __name__ == "__main__":
    main()
