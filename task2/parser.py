import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed

def make_request(url, max_retries=5, wait_time=3, timeout=10):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Проверка успешности запроса
            return response
        except requests.RequestException as e:
            print(f"Ошибка при запросе: {e}. Попытка {retries + 1} через {wait_time} секунд...")
            time.sleep(wait_time)
            retries += 1
    print("Достигнуто максимальное количество повторов, запрос не удался.")
    return None

def extracting_data(link):
    """Функция для извлечения данных из дополнительной страницы."""
    response = make_request(link)
    if not response:
        return pd.DataFrame({'Address': [None]})

    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table')
    
    if len(tables) < 4:
        return pd.DataFrame({'Address': [None]})

    df1 = pd.read_html(StringIO(str(tables[2])))[0].drop([1, 1]).T.drop([0, 0]).reset_index()
    df1.columns = ['index', 'ИИН Руководителя', 'ФИО']
    
    df2 = pd.read_html(StringIO(str(tables[3])))[0]
    extracted_col = df2["Полный адрес(рус)"].str.cat(sep='; ')
    
    new_dataframe = pd.concat([df1, pd.Series([extracted_col], name="Address")], axis=1).drop(['index'], axis=1)
    return new_dataframe

def process_link(link):
    return extracting_data(link)

def main():
    url = "https://www.goszakup.gov.kz/ru/registry/rqc?count_record=2000&page=1"
    response = make_request(url)
    
    if response:
        soup = BeautifulSoup(response.text, 'lxml')
        
        tables = soup.find_all('table')
        if not tables:
            print("Ошибка: не удалось найти таблицу на главной странице.")
            return
        
        final_df = pd.read_html(StringIO(str(tables[0])))[0].drop_duplicates(subset=['Наименование потенциального поставщика'])
        
        links = [a['href'] for row in tables[0].find_all('tr') for a in row.find_all('a', href=True)]
        
        dfs = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_link = {executor.submit(process_link, link): link for link in links}
            for future in as_completed(future_to_link):
                try:
                    df = future.result()
                    dfs.append(df)
                except Exception as e:
                    print(f"Ошибка при обработке ссылки: {e}")
        
        if dfs:
            big_dataframe = pd.concat(dfs, ignore_index=True)
            result_df = pd.concat([final_df, big_dataframe], axis=1)
            result_df = result_df.drop(['Наименование, номер и дата выдачи документа, на основании которого потенциальный поставщик включен в Перечень', '№'], axis=1)
            result_df = result_df.drop_duplicates(subset=['Наименование потенциального поставщика'])
            result_df.reset_index(drop=True, inplace=True)
            
            result_df.to_excel('result.xlsx', index=False)  # Удален параметр encoding
            print("Данные успешно сохранены в файл result.xlsx")
        else:
            print("Не удалось собрать данные для записи.")
    else:
        print("Ошибка при загрузке главной страницы.")

if __name__ == "__main__":
    main()
