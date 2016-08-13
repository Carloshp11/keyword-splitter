# -*- coding: utf-8 -*-

import os
import re


def detect_delimiter(sample_line):
    if len(sample_line.split('\t')) > 1:
        return '\t'
    if len(sample_line.split(';')) > 1:
        return ';'
    if len(sample_line.split(',')) > 1:
        return ','
    input('Error: Delimiter wasn\'t detected as one of these values: \\t, ; or ,')
    raise SyntaxError('Delimiter wasn\'t detected as one of these values: \\t, ; or ,')


for file in os.listdir(os.path.dirname(__file__)):
    if file[-4:] != '.csv' or not(os.path.isfile(file)):
        continue
    try:
        input_handler = open(file, mode='r', encoding='utf-8')
    except UnicodeDecodeError:
        input('Error: Probably encoding is not utf-8')
        raise SyntaxError('Error: Probably encoding is not utf-8')
    break
# It'll break if there is no csv file on the same directory as the python executable

if re.match('[0-9]{8}_.+_[0-9]+.*\.csv', input_handler.name) is None:
    input('file name ' + input_handler.name +
          ' doesn\'t comply with the structure <YYYYMMDD>_<MODE>_<COLUMN-ID>.csv\n\n'
          'Press enter to finish')
    raise NameError('file name ' + input_handler.name +
                    ' doesn\'t comply with the structure <YYYYMMDD>_<MODE>_<COLUMN-ID>.csv')
try:
    ColumnId = int(input_handler.name.split('_')[2].split('.')[0])
except ValueError:
    ColumnId = int(input_handler.name.split('_')[1])

output_handler = open(input_handler.name[:-4] + '_output.csv', mode='w', encoding='utf-8')


def writeline(fullline, swapped_term):
    global output_handler
    output_handler.write(fullline + '\t' + swapped_term + '\n')


first = True
print('Starting to read file ' + input_handler.name)
i, u = 0, 0
try:
    for line in input_handler:
        i += 1
        if first:
            if line.find('Keyword report') != -1:
                print('Adwords download \"Keyword report\" line detected and skipped')
                continue
            first_line = line.rstrip('\n').rstrip('\r')
            d = detect_delimiter(line)
            first_line = first_line.split(d)
            output_handler.write('\t'.join(first_line) + '\n')
            first = False
            continue
        if i % 100000 == 0:
            u += 1
            print('Processinbg line ' + str(u * 100000))
        line = line.rstrip('\r').rstrip('\n').split(d)
        if len(line[ColumnId].split(' ')) > 1:
            keywords = line[ColumnId].split(' ')
        else:
            writeline('\t'.join(line), line[ColumnId])
            continue
        terms = []
        for keyword in keywords:
            if len(keyword) > 3:
                terms.append(keyword)
        Combinations = []
        for term in terms:
            writeline('\t'.join(line), term)
            for term2 in terms[0:terms.index(term)] + terms[terms.index(term) + 1:]:
                try:
                    Combinations.index(terms.index(term) + terms.index(term2))
                except ValueError:
                    Combinations.append(terms.index(term) + terms.index(term2))
                    # print('\t'.join(line) + '\t' + term + ' ' + term2)
                    writeline('\t'.join(line), term + ' ' + term2)
except UnicodeDecodeError:
    input('Error: Probably encoding is not utf-8')
    raise SyntaxError('Error: Probably encoding is not utf-8')

input('Script finished succesfully. Press enter to close window.')


