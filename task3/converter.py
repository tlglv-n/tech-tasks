import json
import xml.etree.ElementTree as ET

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

def prettify(elem):
    from xml.dom import minidom
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def main():
    with open('input.json', 'r') as json_file:
        json_data = json.load(json_file)
    
    root = ET.Element('root')
    
    json_to_xml(json_data, root)
    
    xml_string = prettify(root)
    
    with open('output.xml', 'w') as xml_file:
        xml_file.write(xml_string)

    print("Преобразование завершено. Результат сохранен в output.xml.")

if __name__ == '__main__':
    main()
