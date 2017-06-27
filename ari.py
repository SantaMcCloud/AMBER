#!/usr/bin/env python

import sys
import argparse
import precision_recall_average
import numpy as np
from utils import load_data


def choose2(n):
    return (n * (n - 1)) / 2


def ari(bin_id_to_list_of_sequence_id, sequence_id_to_genome_id, sequence_id_to_bin_id):

    # metrics = precision_recall_average.filter_tail(metrics, 1)

    bin_id_to_genome_id_to_total_contigs = {}
    for bin_id in bin_id_to_list_of_sequence_id:
        bin_id_to_genome_id_to_total_contigs[bin_id] = {}
        for sequence_id in bin_id_to_list_of_sequence_id[bin_id]:
            genome_id = sequence_id_to_genome_id[sequence_id]
            # metric_entry = filter(lambda x: x['mapped_genome'] == genome_id, metrics)
            # if len(metric_entry) > 0 and np.isnan(metric_entry[0]['precision']):
            #     continue
            if genome_id not in bin_id_to_genome_id_to_total_contigs[bin_id]:
                bin_id_to_genome_id_to_total_contigs[bin_id][genome_id] = 0
            bin_id_to_genome_id_to_total_contigs[bin_id][genome_id] += 1
    genome_id_to_bin_id_to_total_contigs = {}
    for sequence_id in sequence_id_to_bin_id:
        genome_id = sequence_id_to_genome_id[sequence_id]
        # metric_entry = filter(lambda x: x['mapped_genome'] == genome_id, metrics)
        # if len(metric_entry) > 0 and np.isnan(metric_entry[0]['precision']):
        #     continue
        if genome_id not in genome_id_to_bin_id_to_total_contigs:
            genome_id_to_bin_id_to_total_contigs[genome_id] = {}
        bin_id = sequence_id_to_bin_id[sequence_id]
        if bin_id not in genome_id_to_bin_id_to_total_contigs[genome_id]:
            genome_id_to_bin_id_to_total_contigs[genome_id][bin_id] = 0
        genome_id_to_bin_id_to_total_contigs[genome_id][bin_id] += 1

    bin_genome_comb = 0.0
    bin_comb = 0.0
    genome_comb = 0.0
    num_contigs = 0
    for bin_id in bin_id_to_genome_id_to_total_contigs:
        for genome_id in bin_id_to_genome_id_to_total_contigs[bin_id]:
            bin_genome_comb += choose2(bin_id_to_genome_id_to_total_contigs[bin_id][genome_id])

    for bin_id in bin_id_to_genome_id_to_total_contigs:
        bin_totals = 0
        for genome_id in bin_id_to_genome_id_to_total_contigs[bin_id]:
            bin_totals += bin_id_to_genome_id_to_total_contigs[bin_id][genome_id]
        num_contigs += bin_totals
        bin_comb += choose2(bin_totals)

    for genome_id in genome_id_to_bin_id_to_total_contigs:
        genome_totals = 0
        for bin_id in genome_id_to_bin_id_to_total_contigs[genome_id]:
            genome_totals += genome_id_to_bin_id_to_total_contigs[genome_id][bin_id]
        genome_comb += choose2(genome_totals)

    temp = float(bin_comb * genome_comb) / float(choose2(num_contigs))
    ret = bin_genome_comb - temp
    print "%1.3f" % (ret / (float((bin_comb + genome_comb) / 2.0) - temp))


def compute_metrics(file_path_mapping, file_path_query):
    # metrics = precision_recall_average.load_tsv_table(sys.stdin)
    genome_id_to_list_of_contigs, sequence_id_to_genome_id = load_data.get_genome_mapping_without_lenghts(file_path_mapping)
    bin_id_to_list_of_sequence_id,sequence_id_to_bin_id = load_data.open_query(file_path_query)
    ari(bin_id_to_list_of_sequence_id, sequence_id_to_genome_id, sequence_id_to_bin_id)


def main():
    parser = argparse.ArgumentParser(description="Compute adjusted rand index from binning file")
    parser.add_argument("-g", "--gold_standard_file", help="gold standard - ground truth - file", required=True)
    parser.add_argument("query_file", help="Query file")
    args = parser.parse_args()
    if not args.gold_standard_file or not args.query_file:
        parser.print_help()
        parser.exit(1)
    compute_metrics(file_path_mapping=args.gold_standard_file,
                    file_path_query=args.query_file)


if __name__ == "__main__":
    main()