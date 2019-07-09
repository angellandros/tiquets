from __future__ import print_function

import argparse
import csv
from collections import defaultdict
import logging


def load_orders(orders_file):
    """
    Load orders into a list
    :param orders: CSV file containing data of order_id and customer_id
    :return: a list containing the whole data

    >>> load_orders(open('orders_test.csv'))
    [['1', '10'], ['2', '11']]
    """
    csv_reader = csv.reader(orders_file, delimiter=',', quotechar='"')
    return [row for row in csv_reader][1:]


def load_barcodes(barcodes_file):
    """
    Load barcodes and create an inverted index out of them
    :param barcodes: CSV file containing data of barcode and order_id
    :return: a map from order_ids into barcodes, and a list of unassigned barcodes

    >>> inverted_index, unassigned_barcodes = load_barcodes(open('barcodes_test.csv'))
    >>> sorted(inverted_index.items(), key=lambda x: x[0])
    [('1', ['11111111111']), ('2', ['11111111112'])]
    >>> unassigned_barcodes
    ['11111111113']
    """
    inverted_index = defaultdict(list)
    assigned_barcodes = dict()
    unassigned_barcodes = list()
    title_row = True
    for barcode, order_id in csv.reader(barcodes_file, delimiter=',', quotechar='"'):
        if title_row:
            title_row = False
            continue
        if barcode in assigned_barcodes:
            logging.error('barcode=%s is already assigned to order_id=%s, ignoring new assignment: order_id=%s',
                          barcode, assigned_barcodes[barcode], order_id)
            continue
        if order_id == '':
            unassigned_barcodes.append(barcode)
            continue
        assigned_barcodes[barcode] = order_id
        inverted_index[order_id].append(barcode)

    return dict(inverted_index), unassigned_barcodes


def make_complete_report(orders_data, barcodes_index, output_file):
    """
    Create a CSV file reporting all the barcodes for the every order
    :param orders_data: output of load_orders
    :param barcodes_index: first output of load_barcodes
    :param output_file: pointer to the CSV file, with writing permissions
    :return: None

    >>> output_file = open('out.csv', 'w')
    >>> make_complete_report([['1', '10'], ['2', '11']], {'1': ['11111111111'], '2': ['11111111112']}, output_file)
    >>> output_file.close()
    >>> open('out.csv', 'r').read()
    '10,1,11111111111\\n11,2,11111111112\\n'
    """
    for order_id, customer_id in orders_data:
        if order_id not in barcodes_index:
            logging.error('no barcode assigned to order with order_id=%s', order_id)
            continue
        output_file.write('%s,%s,%s\n' % (customer_id, order_id, ','.join(barcodes_index[order_id])))


def main(orders_file, barcodes_file, output_file):
    orders_data = load_orders(orders_file)
    barcodes_index, unassigned_barcodes = load_barcodes(barcodes_file)
    make_complete_report(orders_data, barcodes_index, output_file)
    # log unused barcodes
    print('unused barcodes:', ', '.join(unassigned_barcodes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--orders', help='CSV file containing data of orders', default='orders.csv',
                        type=argparse.FileType('r'))
    parser.add_argument('-b', '--barcodes', help='CSV file containing data of barcodes', default='barcodes.csv',
                        type=argparse.FileType('r'))
    parser.add_argument('-O', '--output', help='output CSV file', default='output.csv',
                        type=argparse.FileType('w'))
    args = parser.parse_args()
    main(orders_file=args.orders, barcodes_file=args.barcodes, output_file=args.output)
