# tech-tasks

# Task 2
- Purpose: Makes an HTTP GET request to the given url.
- If the request fails, it retries up to max_retries times, waiting wait_time seconds between retries.
```
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
```

- Purpose: Extracts data from a given link. It performs the following tasks:
- 1) Fetch Data
- 2) Parse HTML
- 3) Process Tables
- 4) Create DataFrame: Combines extracted data into a DataFrame.
```
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
```

- main function: Orchestrates the scraping process, handles data extraction and processing, and saves the results to an Excel file.
```
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

```




# Task 3

- Converts JSON data into XML format.
```
def json_to_xml(json_obj, parent):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            sub_elem = ET.SubElement(parent, key)
            json_to_xml(value, sub_elem)
    elif isinstance(json_obj, list):
        for item in json_obj:
            item_elem = ET.SubElement(parent, parent.tag[:-1])  
            json_to_xml(item, item_elem)
    else:
        parent.text = str(json_obj)
```


-  Formats XML data to make it more readable.
```
def prettify(elem):
    from xml.dom import minidom
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
```


- Main function to execute the JSON to XML conversion.
```
def main():
    with open('input.json', 'r') as json_file:
        json_data = json.load(json_file)
    
    root = ET.Element('root')
    
    json_to_xml(json_data, root)
    
    xml_string = prettify(root)
    
    with open('output.xml', 'w') as xml_file:
        xml_file.write(xml_string)

    print("Преобразование завершено. Результат сохранен в output.xml.")
```
