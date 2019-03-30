#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.0.1, 2019-03-30
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

def get_spacing(bib):
    for line in bib:
        if '    ' not in line:
            if '%' not in line:
                if '@' not in line:
                    if '}' not in line:
                        print(line)

def main():
    bib = readfile('max.bib')
    check_pages(bib)
    check_title(bib)
    check_equal_signs(bib)
    check_double_space(bib)
    #check_author_names(bib)
    get_entries('publisher', bib)
    #get_spacing(bib)

if __name__ == '__main__':
    main()