from collections import OrderedDict
import sys
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
    entries = OrderedDict()
    for item in maxbib_items:
        entry = OrderedDict()
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
    result = OrderedDict()
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

def enforce_order(name, entry, item_type):
    if item_type == 'article':
        order = ['author', 'title', 'journal', 'year', 'volume', 'number', 'pages', 'month', 'publisher']
        for k, v in enumerate(entry):
            if v != order[k]:
                print(name)
                print("Wrong order", v, "!=",order[k])
                print(entry)
                sys.exit(1)
    if item_type == 'inproceedings':
        order = ['author', 'title', 'booktitle', 'year', 'series', 'pages', 'address', 'month', 'publisher']
        for k, v in enumerate(entry):
            if v != order[k]:
                print(name)
                print("Wrong order", v, "!=",order[k])
                print(entry)
                sys.exit(1)
    if item_type == 'misc':
        order = ['author', 'title', 'note', 'month', 'year']
        for k, v in enumerate(entry):
            if v != order[k]:
                print(name)
                print("Wrong order", v, "!=",order[k])
                print(entry)
                #sys.exit(1)
                print()

def main():
    print("Start")
    maxbib = readfile('max.bib')
    maxbib_items = get_bibitems(maxbib)
    maxbib_entries = convert_to_bibentries(maxbib_items)
    for entry in maxbib_items:
        if entry.startswith('@misc'):
            enforce_order(entry, maxbib_entries[entry], 'misc')
    print("Done")

if __name__ == '__main__':
    main()