#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.0.1, 2022-03-02
:description: Helper script to identify interesting papers missing in the bib
'''
def readfile(filename):
    result = []
    with open(filename, 'r') as inputfile:
        for line in inputfile:
            line = line.rstrip('\r\n')
            if not line.startswith('%'): # Skip comments
                result.append(line)
    return result

def convert_to_bibentries(maxbib_items):
    """Parse the bib item to something meaningful, aka identify title, author, year etc."""
    entries = dict()
    for item in maxbib_items:
        entry = dict()
        for line in maxbib_items[item]:
            if not line.startswith('@') and not line.startswith('}'):
                try:
                    label = line.split('=', 1)[0].strip()
                    content = line.split('=', 1)[1].strip()
                    entry[label] = content
                except:
                    print(f"Broken Bibtex Entry: {line}")
        entries[item] = entry
    return entries

def get_bibitems(bib):
    """Where does a bibentry start, where does it end?"""
    result = dict()
    item = []
    entry_name = ''
    for line in bib:
        if line != '':
            item.append(line)
        if line.startswith('@'):
            entry_name = line
        if line.startswith('}'):
            result[entry_name] = item
            entry_name = ''
            item = []
    return result

def main():
    maxbib = readfile('max.bib')
    maxbib_items = get_bibitems(maxbib)
    maxbib_entries = convert_to_bibentries(maxbib_items)

    newbib = readfile('newpaper.bib')
    newbib_items = get_bibitems(newbib)
    newbib_entries = convert_to_bibentries(newbib_items)

    # Compare the two bibfiles based on the paper title
    # This is expensive O(n*n) but we do not care...
    for outer_entry in newbib_entries:
        found = False
        for inner_entry in maxbib_entries:
            if newbib_entries[outer_entry]['title'] in maxbib_entries[inner_entry]['title']:
                found = True
        if found == False:
            print(outer_entry)
            print("Missing: {}".format(newbib_entries[outer_entry]['title'].replace('{{', '').replace('}}', '').rstrip(',')))
            print()

if __name__ == '__main__':
    main()