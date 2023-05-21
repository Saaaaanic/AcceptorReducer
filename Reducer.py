from Rex import Acceptor
from prettytable import PrettyTable

def reduce_acceptor(acceptor: Acceptor):
    A = set()
    for a in acceptor._data[0]:
        if a != 'acceptant':
            A.add(a)

    Q = [q for q in acceptor._data]

    table = {k: {l: (acceptor._data[k]['acceptant'] != acceptor._data[l]['acceptant']) for l in Q } for k in Q}

    while True:
        ic = 0
        for k in Q:
            for l in Q:
                if table[k][l] is True:
                    continue
                for a in A:
                    k_prime = acceptor.run(k, a)
                    prime = acceptor.run(l, a)
                    k_prime, prime = min(k_prime, prime), max(k_prime, prime)
                    if k_prime == prime:
                        continue
                    if table[k_prime][prime] == True:
                        ic += 1
                        table[k][l] = table[k_prime][prime]
        if (ic == 0):
            break
    print_table(table)

def print_table(table):
    headers = [""] + sorted(table.keys())
    table_to_print = PrettyTable(headers)

    for row_label in sorted(table.keys()):
        row = [row_label]
        for column_label in sorted(table.keys()):
            if row_label < column_label:
                row.append(table[row_label][column_label])
            elif row_label == column_label:
                row.append("-")
            else:
                row.append("")
        table_to_print.add_row(row)

    print(table_to_print)