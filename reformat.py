#!/usr/bin/env python3

import pprint
import bibtexparser
from fuzzywuzzy import fuzz


conference_names = {
    "Annual International Symposium on Computer Architecture" : "ISCA",
    "Annual IEEE/ACM International Symposium on Microarchitecture": "MICRO",
    "IEEE micro":"micro",
    "IEEE International Symposium on High Performance Computer Architecture": "HPCA",
    "Transactions on Embedded Computing Systems": "TECS",
    "ACM/SIGDA International Symposium on Field-Programmable Gate Arrays":"FPGA",
    "European Solid State Circuits Conference" : "ESSCIRC",
    "International Conference on Field-Programmable Technology":"FPT",
    "IEEE Journal of Solid-State Circuits":"Solid_State_Computat",
    "IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems":"TCAD",
    "IEEE Transactions on computers":"TC",
    "ACM Trans. Graph.":"TOG",
    "ACM SIGARCH Computer Architecture News":"SIGARCH",
    "Acm Sigplan Notices":"SIGPLAN"
}

def warning_conf_name(entry_conf_name, conf_name):
    if entry_conf_name[1] < 60:
        print("[WARNING] Conference name fuzzy ratio is less than 60%: {0} -> {1}".format(conf_name, entry_conf_name[0]))

with open('test/references.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

for entry in bib_database.entries:
    names = entry['author']
    first_name = str.split(names, 'and')
    first_name = [x.strip().replace(', ', '_').replace(' ','_') for x in first_name if x.strip() != 'others']
    conference = []
    if 'journal' in entry.keys():
        conf_name = entry['journal']
        search_ratio = [ fuzz.partial_ratio(x,conf_name) for x in conference_names.keys()]
        res_ratio = [(val,key) for (val, key) in zip(conference_names.values(), search_ratio)]
        entry_conf_name = max(res_ratio,key=lambda item:item[1])
        warning_conf_name(entry_conf_name, conf_name)
    elif 'booktitle' in entry.keys():
        conf_name = entry['booktitle']
        search_ratio = [ fuzz.partial_ratio(x,conf_name) for x in conference_names.keys()]
        res_ratio = [(val,key) for (val, key) in zip(conference_names.values(), search_ratio)]
        entry_conf_name = max(res_ratio,key=lambda item:item[1])
        warning_conf_name(entry_conf_name, conf_name)

    else:
        conference.append('')

# pp = pprint.PrettyPrinter(depth=6)
# pp.pprint(bib_database.entries)
