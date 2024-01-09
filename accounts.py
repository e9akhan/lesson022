"""
    Module name :- accounts
    Method(s) :- previous_balance(filename), credit_amount(amount),
    debit(amount), transaction(amount, category, desc, mode_of_payment, credit=False),
    ledger(date, amount, category, desc, mode_of_payment),
    generate_csv_file(in_file, out_file, *keys), generate_category_report(),
    generate_payment_report(), print_report(), generate_txt_file(output),
    generate_html_file(output), generate_random_data()
"""

import random
import csv
import datetime


def previous_balance(filename):
    """
    Find the last amount present in file.

    Args:-
        filename(str) :- Name of file.

    Return
        Latest amount in file.
    """
    with open(filename, "r", encoding="utf-8") as f:
        csvreader = csv.DictReader(f)
        data = list(csvreader)

    return float(data[-1]["amount"])


def credit_amount(amount):
    """
    Add an amount to balance.

    Args:-
        amount(float) :- Amount.

    Return
        Total balance.
    """
    balance = amount + previous_balance("ledger.csv")
    return balance


def debit(amount):
    """
    Debit an amount from balance.

    Args:-
        amount(float) :- Amount.

    Return
        Remaining balance.
    """
    balance = previous_balance("ledger.csv") - amount
    return balance


def transaction(amount, category, desc, mode_of_payment, credit=False):
    """
    Make a transaction.

    Args:-
        amount(float) :- Amount.
        category(str) :- Category.
        desc(str) :- Description of transaction.
        mode_of_payment(str) :- Mode of payment.

    Return
        Status of transaction.
    """
    date = datetime.date.today()
    if credit:
        amount = credit_amount(amount)
    else:
        amount = debit(amount)

    if amount < 0:
        return "Unable to make transaction"

    ledger(date, round(amount, 2), category, desc, mode_of_payment)
    return "Transaction successful."


def ledger(date, amount, category, desc, mode_of_payment):
    """
    Add transaction record to a file.

    Args:-
        date(datetime.date) :- Date of transaction.
        amount(float) :- Amount.
        category(str) :- Category.
        desc(str) :- Description of transaction.
        mode_of_payment(str) :- Mode of payment.
    """
    data = {
        "date": date,
        "category": category,
        "desc": desc,
        "mode_of_payment": mode_of_payment,
        "amount": amount,
    }

    with open("ledger.csv", "a", encoding="utf-8") as ledger_file:
        csvwriter = csv.DictWriter(ledger_file, fieldnames=data.keys())
        csvwriter.writerow(data)


def generate_csv_file(in_file, out_file, *keys):
    """
    Generate csv file with name in out_file with given keys
    from in_file.

    Args:-
        in_file(str) :- Name of input file.
        out_file(str) :- Name of output file.
        keys(list) :- List of keys.
    """
    with open(in_file, "r", encoding="utf-8") as f:
        csvreader = csv.DictReader(f)
        data = list(csvreader)

    data2 = [{key: entry[key] for key in keys} for entry in data]

    with open(out_file, "w", encoding="utf-8") as f:
        csvwriter = csv.DictWriter(f, fieldnames=data2[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(data2)


def generate_category_report():
    """
    Generate category csv file.

    Return
        Name of generated file.
    """
    generate_csv_file(
        "ledger.csv", "category.csv", "date", "category", "desc", "amount"
    )

    return "category.csv"


def generate_payment_report():
    """
    Generate payment csv file.

    Return
        Name of generated file.
    """
    generate_csv_file(
        "ledger.csv", "payment.csv", "date", "mode_of_payment", "desc", "amount"
    )

    return "payment.csv"


def print_report():
    """
    Print the information and generate txt and html file.
    """
    with open("ledger.csv", "r", encoding="utf-8") as ledger_file:
        csvreader = csv.DictReader(ledger_file)
        data = list(csvreader)

    categories = {entry["category"] for entry in data}
    years = sorted(
        list(
            {
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").year
                for entry in data
            }
        )
    )

    categorized_data = []

    for category in categories:
        category_data = []
        for year in years:
            for month in range(1, 13):
                amount = 0
                for entry in data:
                    date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d")
                    amount += (
                        float(entry["amount"])
                        if (
                            entry["category"] == category
                            and date_obj.month == month
                            and date_obj.year == year
                        )
                        else 0
                    )
                category_data.append(amount)
        categorized_data.append(category_data)

    today = datetime.date.today()

    print(f"{'Category':10}", end="")
    txt = f"{'Category':10}"
    html = "<table><tr><th>Category</th>"

    for year in years:
        for month in range(1, 13):
            date = str(month) + "-" + str(year)
            print(f"{date:>12}", end="")
            txt += f"{date:>12}"
            html += f"<th>{date}</th>"

    txt += "\n"
    html += "</tr>"

    print()

    for index, category in enumerate(categories):
        print(f"{category:10}", end="")
        txt += f"{category:10}"
        html += f"<tr><td>{category}</td>"
        for data in categorized_data[index]:
            print(f"{data:12}", end="")
            txt += f"{data:12}"
            html += f"<td>{data}</td>"
        txt += "\n"
        html += "</tr>"
        print()

    html += "</table>"

    generate_txt_file(txt)
    generate_html_file(html)


def generate_txt_file(output):
    """
    Generate txt file for report.
    """
    with open("report.txt", "w", encoding="utf-8") as txt:
        txt.write(output)


def generate_html_file(output):
    """
    Generate html file for report.
    """
    style = """
    table, th, td{
    margin: auto;
    padding: 5px;
    border: 2px solid black;
    border-collapse: collapse;
    }
"""

    html = f"""
    <html>
    <head>
    <style>
        {style}
    </style>
    </head>
    <body>
    {output}
    </body>
    </html>
"""

    with open("report.html", "w", encoding="utf-8") as html_file:
        html_file.write(html)


def generate_random_data(n):
    """
    Generate random data for ledger.csv file.
    """
    categories = ["Food", "Rent", "Credit", "Debit", "Fare", "Picnic"]
    mode_of_payment = ["Net Banking", "Mobile Banking", "UPI", "Card Payment"]

    ledger_data = []

    current_year = datetime.date.today().year

    for year in range(current_year - n - 1, current_year):
        for month in range(1, 13):
            for category in categories:
                date = random.randint(1, 28)
                ledger_data.append(
                    {
                        "date": f"{year}-{month}-{date}",
                        "category": category,
                        "desc": f"Added {category}",
                        "mode_of_payment": random.choice(mode_of_payment),
                        "amount": round(random.random() * 10000, 2),
                    }
                )

    with open("ledger.csv", "w", encoding="utf-8") as ledger_file:
        csvwriter = csv.DictWriter(ledger_file, fieldnames=ledger_data[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(ledger_data)


if __name__ == "__main__":
    generate_random_data(3)
    print(credit_amount(11000))
    print(debit(1000))
    print_report()
    print(generate_category_report())
    print(generate_payment_report())
