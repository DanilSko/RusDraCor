import os
import re
import xml.etree.ElementTree as ET
import csv

csv_path = './ready_CSV/'
tei_path = './ready_TEI/'

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

table = open('calculations.csv', 'w', encoding='utf-8')
table.write('Play,Num_of_scenes,Num_of_char,Max_degree,\n')


def write_filename(file):
    """This function returns the filename without extension
    = the drama title"""
    file_name0 = file.split('/')[2]
    return file_name0.split('.xml')[0]


def get_body(file):
    """This function parse the file at initial phase
    and gets its xml body or returns None if the file is invalid"""
    try:
        tree = ET.parse(file)
        tei = tree.getroot()
        text = tei[1]
        body = text.find('tei:body', ns)
        return body
    except:
        print('ERROR while parsing', file)
        return None


def get_divs(file):
    """This function gets all the divs of the play
    with their contents"""
    body = get_body(file)
    if body is not None:
        divs = body.findall('tei:div', ns)
        return divs
    else:
        return None


def num_of_scenes(file):
    """This function parses the divs and returns the number of scenes.
    If div contains divs,
    the number of these subdivs are added to the number of scenes,
    else number of scenes gets +1.
    If there were no divs in the xml, number of scenes is 1."""
    scenes_num = 0
    divs = get_divs(file)
    if divs is not None:
        for div in divs:
            subdivs = div.findall('tei:div', ns)
            if len(subdivs) == 0:
                scenes_num += 1
            else:
                scenes_num += len(subdivs)
    else:
        scenes_num = 'ERROR while parsing'
    if scenes_num == 0:
        scenes_num = 1
    return scenes_num


def num_of_char(file):
    """This function returns the number of characters in the file"""
    tei = open(file).read()
    characters = re.findall('<sp who="(.*?)">', tei)
    characters = set(characters)
    return str(len(characters))


def max_degree(file):
    weights = []
    degrees = open(file)
    degrees = csv.DictReader(degrees, delimiter=';')
    for row in degrees:
        weights.append(row['Weight'])
    try:
        return max(weights)
    except:
        return 'empty weights'


data = list()
for file in os.listdir(tei_path):
    if file.endswith('.xml'):
        data_f = list()
        file_name = write_filename(tei_path + file)
        print(file_name)
        data_f.append(file_name)
        data_f.append(num_of_scenes(tei_path + file))
        data_f.append(num_of_char(tei_path + file))
        data_f.append(max_degree(csv_path + file_name + '.csv'))
        data.append(data_f)

for d in data:
    for el in d:
        table.write(str(el) + ',')
    table.write('\n')



