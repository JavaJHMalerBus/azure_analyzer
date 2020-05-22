import json
import tkinter as tk
from tkinter import filedialog
import texttable
import argparse

rt = tk.Tk()
rt.withdraw()

parser = argparse.ArgumentParser(description='Analyzes and summarizes an AzureUsage.json file')

parser.add_argument('--path', action='store', default='',
                    help='The path to the AzureUsage.json file. If not provided, a file chooser dialog will '
                         'pop up.')
parser.add_argument('--detail', action='store', default=-1, type=int, help='Shows detailed information about the '
                                                                           'given id. The '
                                                                           'id equals to the #-column shown when this '
                                                                           'parameter '
                                                                           ' is left out.')

args = parser.parse_args()

json_path = args.path if args.path != '' else filedialog.askopenfilename()


def initialize_mappings(d):
    do = {}
    mapping = []
    for item in d:
        if item["Cost"] == 0:
            continue
        if item["ServiceName"] in do:
            do[item["ServiceName"]]["Quantity"] += item["Quantity"]
            do[item["ServiceName"]]["Cost"] += item["Cost"]
        else:
            do[item["ServiceName"]] = item
    for i, (name, value) in enumerate(do.items()):
        mapping.append(name)
    return do, mapping


def parse(d):
    do, mapping = initialize_mappings(d)
    table = texttable.Texttable()
    table.add_row(["#", "Name", "Price per unit", "Quantity", "Price"])
    for i, (name, value) in enumerate(do.items()):
        table.add_row([i, value["ServiceName"],
                       value["Cost"] / value["Quantity"] if (value["Quantity"] > 0 and value["Cost"] > 0) else "N/A",
                       value["Quantity"], value["Cost"]])
    print(table.draw())


def detail(id, d):
    do, mapping = initialize_mappings(d)
    table = texttable.Texttable()
    table.add_row(["#", "Name", "Subscription", "Price per unit", "Quantity", "Price"])
    if len(mapping) > id >= 0:
        table.add_row([id, do[mapping[id]]["ServiceName"], do[mapping[id]]["SubscriptionName"], do[mapping[id]]["Cost"] / do[mapping[id]]["Quantity"] if (do[mapping[id]]["Quantity"] > 0 and do[mapping[id]]["Cost"] > 0) else "N/A",
                       do[mapping[id]]["Quantity"], do[mapping[id]]["Cost"]])
    else:
        print("Id not found! Was the file changed since you retrieved the id?")
        return
    print(table.draw())


with open(json_path) as json_file:
    data = json.load(json_file)
    print("Parsing data from subscription \"" + data[0]["SubscriptionName"] + "\"...")
    if args.detail == -1:
        parse(data)
    else:
        detail(args.detail, data)
