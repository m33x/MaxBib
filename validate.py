#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.0.2, 2021-02-07
:description: Checks bibfile for common errors
'''

import sys, operator

def readfile(filename):
    result = []
    with open(filename, 'r') as inputfile:
        for line in inputfile:
            line = line.rstrip('\r\n')
            result.append(line)
    return result

def check_title(bib):
    for line in bib:
        if 'title' in line:
            if '{{' not in line:
                if 'booktitle' not in line:
                    print(line)

def check_pages(bib):
    for line in bib:
        if 'pages' in line:
            if '--' not in line:
                if 'pages = {},' not in line:
                    print(line)

def check_equal_signs(bib):
    for line in bib:
        if '=' in line:
            if ' = ' not in line:
                print(line)

def check_double_space(bib):
    for line in bib:
        if '  ' in line:
            if not line.startswith('    '):
                print(line)

def check_author_names(bib):
    for line in bib:
        if 'author' in line:
            if ', ' not in line:
                print(line)

def get_entries(kind, bib):
    result = {}
    for line in bib:
        if kind in line:
            if line in result:
                result[line] += 1
            else:
                result[line] = 1
    result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    once = []
    for entry in result:
        if entry[1] == 1:
            once.append(entry[0])
        else:
            print("{} -- {}".format(entry[1], entry[0]))
    once.sort()
    for entry in once:
        print("{} -- {}".format(1, entry))

def get_bibitem(bib, item_type):
    results = []
    item = ''
    for line in bib:
        item += line + '\n'
        if line.startswith(item_type):
            item = line + '\n'
        if line.startswith('}'):
            results.append([item])
            item = ''
    return results

def get_allitems(bib):
    no_of_entries = 0
    allitems = []
    allitems += get_bibitem(bib, '@')
    for bibitem in allitems:
        no_of_entries += 1
    print("Found {} entries in the provided bib file.".format(no_of_entries))
    return allitems

def find_sorting_error(bibitems):
    before = []
    entries = 0
    for item in bibitems:
        for line in item:
            firstline = line.split('\n')[0]
            break
        currentline = firstline.replace('@inproceedings{', '').replace('@article{', '').replace('@misc{', '').replace('@book{', '').replace('@techreport{', '').replace('@phdthesis{', '').replace('@incollection{', '').replace('@inbook{', '')
        entries += 1
        before.append(currentline)
        #print("{}\t{}".format(entries, currentline))
    print("###########\n\n\n")
    after = sorted(before)
    for k, v in enumerate(after):
        if after[k].split('-')[0] != before[k].split('-')[0]:
            print("Check", k, after[k], before[k])

def get_spacing(bib):
    entries = 0
    counter = 0
    for line in bib:
        counter += 1
        if '    ' not in line:
            if '%' not in line:
                if '@' not in line:
                    if '}' not in line:
                        entries += 1
                        print(entries, counter, line)

def check_brokes_series(bib):
    allitems = []
    allitems += get_bibitem(bib, '@inproceedings')
    for item in allitems:
        if '@inproceedings' in str(item):
            if 'series' not in str(item):
                print(item)
                print()

def main():
    bib = readfile('max.bib')
    #check_pages(bib)
    #check_title(bib)
    #check_equal_signs(bib)
    #check_double_space(bib)
    #check_author_names(bib)
    #get_entries('publisher', bib)
    #get_entries('series', bib)
    #get_spacing(bib)
    #allitems = get_allitems(bib)
    #find_sorting_error(allitems)
    check_brokes_series(bib)

if __name__ == '__main__':
    main()