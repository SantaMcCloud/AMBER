#!/usr/bin/env python

RANKS = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
DICT_RANK_TO_INDEX = dict(zip(RANKS, list(range(len(RANKS)))))


def load_tax_info(ncbi_nodes_file):
    tax_id_to_parent = {}
    tax_id_to_rank = {}
    with open(ncbi_nodes_file) as read_handler:
        for line in read_handler:
            if len(line.strip()) == 0:
                continue
            line = line.split('|')
            line = list(map(str.strip, line))
            tax_id = line[0]
            tax_id_to_parent[tax_id] = line[1]
            tax_id_to_rank[tax_id] = line[2]

    return tax_id_to_parent, tax_id_to_rank


def get_id_path(tax_id, tax_id_to_parent, tax_id_to_rank):
    if tax_id not in tax_id_to_rank:
        # TODO report this in a log file
        return None

    while tax_id_to_rank[tax_id] not in RANKS:
        tax_id = tax_id_to_parent[tax_id]
        if tax_id == '1':
            return None

    index = DICT_RANK_TO_INDEX[tax_id_to_rank[tax_id]]
    path = [''] * (index + 1)
    path[index] = tax_id

    id = tax_id
    while id in tax_id_to_parent:
        id = tax_id_to_parent[id]
        if id == '1':
            break
        if tax_id_to_rank[id] not in RANKS:
            continue
        index = DICT_RANK_TO_INDEX[tax_id_to_rank[id]]
        path[index] = id
        if tax_id_to_rank[id] == "superkingdom":
            break
    return path
