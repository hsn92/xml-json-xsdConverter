import json
import xml.etree.ElementTree as ET
from lxml import etree
import csv
import sys
from io import StringIO


def prettify(element, indent='  '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            element.text = '\n' + indent * (level + 1)  # for child open
        if queue:
            element.tail = '\n' + indent * queue[0][0]  # for sibling open
        else:
            element.tail = '\n' + indent * (level - 1)  # for parent close
        queue[0:0] = children  

def csv2xml(csv_name,xml_name):
    with open(csv_name, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile,delimiter=";")
        xml_doc = ET.Element('departments')
        lng=''
        for line in csv_reader:
            university = ET.SubElement(xml_doc,'university',uType=line["ÜNİVERSİTE_TÜRÜ"],name=line["ÜNİVERSİTE"])
            item = ET.SubElement(university,'item',faculty=line["FAKÜLTE"],id=line["PROGRAM_KODU"])
            if line["DİL"]=='İngilizce':
                lng='en'
            else:
                lng='tr'
            ET.SubElement(item,'name',lang=lng,second=line["ÖĞRENİM_TÜRÜ"]).text = line["PROGRAM"]
            ET.SubElement(item,'period').text = line["ÖĞRENİM_SÜRESİ"]
            ET.SubElement(item,'quota' ,spec=line["OKUL_BİRİNCİSİ_KONTENJANI"]).text = line["KONTENJAN"]
            ET.SubElement(item,'field').text = line["PUAN_TÜRÜ"]
            ET.SubElement(item,'last_min_score',order=line["GEÇEN_YIL_MİN_SIRALAMA"]).text = line["GEÇEN_YIL_MİN_PUAN"]
            ET.SubElement(item,'grant').text = line["BURS"]
        
        prettify(xml_doc)
        tree = ET.ElementTree(xml_doc)
        tree.write(xml_name,encoding='utf-8',xml_declaration=True)

def xml2csv(xml_name,csv_name):
    xml_file = ET.parse(xml_name)
    myroot = xml_file.getroot()
    with open(csv_name, 'w', encoding='utf-8',newline='') as csvfile:
        field_name = ['ÜNİVERSİTE_TÜRÜ','ÜNİVERSİTE','FAKÜLTE','PROGRAM_KODU','PROGRAM','DİL','ÖĞRENİM_TÜRÜ','BURS','ÖĞRENİM_SÜRESİ','PUAN_TÜRÜ','KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI','GEÇEN_YIL_MİN_SIRALAMA','GEÇEN_YIL_MİN_PUAN']
        csvwriter = csv.writer(csvfile,delimiter=";")
        csvwriter.writerow(field_name)
        lng=''
        for uni in myroot.findall('university'):
        
            uType = uni.attrib.get('uType')
            uName = uni.attrib.get('name')
            itemID = uni[0].attrib.get('id')
            faculty = uni[0].attrib.get('faculty')
            dName = uni[0][0].text
            if uni[0][0].attrib.get('lang')=='en':
                lng='İngilizce'
            else:
                lng=''
            lang = lng
            second = uni[0][0].attrib.get('second')
            period = uni[0][1].text
            quota = uni[0][2].text
            spec = uni[0][2].attrib.get('spec')
            field = uni[0][3].text
            lmin_score = uni[0][4].text
            order = uni[0][4].attrib.get('order')
            grant = uni[0][5].text

            row = [uType,uName,faculty,itemID,dName,lang,second,grant,period,field,quota,spec,order,lmin_score]
            csvwriter.writerow(row)
    
def csv2json(csv_name,json_name):
    #csv2json
    with open(csv_name, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile,delimiter=";")

            universitys = []
            university = {}
            items = []
            item = {}
            department = {}
            departments = []
            lng=''
            strs = ''
            bool = True
            for line in csv_reader:
                if bool == True:
                    strs = line['ÜNİVERSİTE']
                    bool = False

                if strs != line['ÜNİVERSİTE']:
                    item['department'] = departments.copy()
                    items.append(dict(item))
                    university['items'] = items.copy()
                    universitys.append(dict(university))
                    strs = line['ÜNİVERSİTE']
                    departments[:] = []
                    item.clear()
                    items[:] = []
                    

                university['university name'] = line['ÜNİVERSİTE']
                university['uType'] = line['ÜNİVERSİTE_TÜRÜ']
            
           
                item['faculty'] = line['FAKÜLTE']


                department['id'] = line['PROGRAM_KODU']
                department['name'] = line['PROGRAM']
                if line["DİL"]=='İngilizce':
                    lng='en'
                else:
                    lng='tr'
                department['lang'] = lng
                department['second'] = line['ÖĞRENİM_TÜRÜ']
                department['period'] = line['ÖĞRENİM_SÜRESİ']
                department['spec'] = line['OKUL_BİRİNCİSİ_KONTENJANI']
                department['quota'] = line['KONTENJAN']
                department['field'] = line['PUAN_TÜRÜ']
                department['last_min_score'] = line['GEÇEN_YIL_MİN_PUAN']
                department['last_min_order'] = line['GEÇEN_YIL_MİN_SIRALAMA']
                department['grant'] = line['BURS']

            

                departments.append(dict(department))
            item['department'] = departments.copy()
            items.append(dict(item))
            university['items'] = items.copy()
            universitys.append(dict(university))  
                

                
            
    with open(json_name, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(universitys, indent=4, ensure_ascii=False))

def json2csv(json_name,csv_name):
    #json2csv
    with open(json_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    with open(csv_name, 'w', encoding='utf-8',newline='') as csvfile:
        field_name = ['ÜNİVERSİTE_TÜRÜ','ÜNİVERSİTE','FAKÜLTE','PROGRAM_KODU','PROGRAM','DİL','ÖĞRENİM_TÜRÜ','BURS','ÖĞRENİM_SÜRESİ','PUAN_TÜRÜ','KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI','GEÇEN_YIL_MİN_SIRALAMA','GEÇEN_YIL_MİN_PUAN']
        csvwriter = csv.writer(csvfile,delimiter=";")
        csvwriter.writerow(field_name)
        lng=''
        i=0
        for item in data:
            uName = item['university name']
            uType = item['uType']
            faculty = item['items'][i]['faculty']
            for depart in item['items'][i]['department']:
                itemID = depart['id']
                dName = depart['name']
                if depart['lang']=='en':
                    lng='İngilizce'
                else:
                    lng=''
                lang = lng
                second = depart['second']
                period = depart['period']
                spec = depart['spec']
                quota = depart['quota']
                field = depart['field']
                lmin_score = depart['last_min_score']
                order = depart['last_min_order']
                grant = depart['grant']
                row = [uType,uName,faculty,itemID,dName,lang,second,grant,period,field,quota,spec,order,lmin_score]
                csvwriter.writerow(row)

def xml2json(xml_name,json_name):
    xml_file = ET.parse(xml_name)
    myroot = xml_file.getroot()              
    
    universitys = []
    university = {}
    items = []
    item = {}
    department = {}
    departments = []
    strs = ''
    bool = True

    for uni in myroot.findall('university'):
        

        if bool == True:
            strs = uni.attrib.get('name')
            bool = False

        if strs != uni.attrib.get('name'):
            item['department'] = departments.copy()
            items.append(dict(item))
            university['items'] = items.copy()
            universitys.append(dict(university))
            strs = uni.attrib.get('name')#
            departments[:] = []
            item.clear()
            items[:] = []

        university['uType'] = uni.attrib.get('uType')
        university['university name'] = uni.attrib.get('name')
        
        item['faculty'] = uni[0].attrib.get('faculty')


        department['id'] = uni[0].attrib.get('id')
        department['name'] = uni[0][0].text
        department['lang'] = uni[0][0].attrib.get('lang')
        department['second'] = uni[0][0].attrib.get('second')
        department['period'] = uni[0][1].text
        department['quota'] = uni[0][2].text
        department['spec'] = uni[0][2].attrib.get('spec')
        department['field'] = uni[0][3].text
        department['last_min_score'] = uni[0][4].text
        department['last_min_order'] = uni[0][4].attrib.get('order')
        department['grant'] = uni[0][5].text

        departments.append(dict(department))
              
    item['department'] = departments.copy()
    items.append(dict(item))
    university['items'] = items.copy()
    universitys.append(dict(university))

    with open(json_name, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(universitys, indent=4, ensure_ascii=False))

def json2xml(json_name,xml_name):
    with open(json_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    xml_doc = ET.Element('departments')
    i=0
    for item in data:
        uName = item['university name']
        uType = item['uType']
        faculty = item['items'][i]['faculty']
        for depart in item['items'][i]['department']:
            itemID = depart['id']
            dName = depart['name']
            lang = depart['lang']
            second = depart['second']
            period = depart['period']
            spec = depart['spec']
            quota = depart['quota']
            field = depart['field']
            lmin_score = depart['last_min_score']
            order = depart['last_min_order']
            grant = depart['grant']

            university = ET.SubElement(xml_doc,'university',uType=uType,name=uName)
            xitem = ET.SubElement(university,'item',faculty=faculty,id=itemID)
            ET.SubElement(xitem,'name',lang=lang,second=second).text = dName
            ET.SubElement(xitem,'period').text = period
            ET.SubElement(xitem,'quota' ,spec=spec).text = quota
            ET.SubElement(xitem,'field').text = field
            ET.SubElement(xitem,'last_min_score',order=order).text = lmin_score
            ET.SubElement(xitem,'grant').text = grant


    prettify(xml_doc)
    tree = ET.ElementTree(xml_doc)
    tree.write(xml_name,encoding='utf-8',xml_declaration=True)

def xml2xsd(xml_name,xsd_name):
    doc = etree.parse(xml_name)
    root = doc.getroot()
    xmlschema_doc = etree.parse(StringIO(xsd_name))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(etree.tostring(root))
    validation_result = xmlschema.validate(doc)
    print(validation_result)
    xmlschema.assert_(doc)

    
inputfilename = sys.argv[1]
outputfilename = sys.argv[2]
type = int(sys.argv[3])

if  type==1:
    csv2xml(inputfilename,outputfilename)

elif type==2:
    xml2csv(inputfilename,outputfilename)

elif type==3:
    xml2json(inputfilename,outputfilename)

elif type==4:
    json2xml(inputfilename,outputfilename)

elif type==5:
    csv2json(inputfilename,outputfilename)

elif type==6:
    json2csv(inputfilename,outputfilename)

elif type==7:
    xml2xsd(inputfilename,outputfilename)
