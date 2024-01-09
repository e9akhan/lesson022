"""
    Module name :- accounts
    Method(s) :- previous_balance(filename), credit_amount(amount),
    debit(amount), transaction(amount, category, desc, mode_of_payment, credit=False),
    ledger(date, amount, category, desc, mode_of_payment),
    generate_csv_file(in_file, out_file, *keys), generate_category_report(),
    generate_payment_report(), print_report(), generate_txt_file(output),
    generate_html_file(output), generate_random_data()
    Classes:- Account.
"""

import random
import csv
import datetime
import os


class Account:
    """
    Class to manage an account.
    """

    def __init__(self, account_number, full_name, initial_amount_paid):
        """
        Initializes the class with accont_number and full_name.

        Args:-
            account_number(int):- Account Number
            full_name(str):- Full name of account holder
        """
        self.account_number = account_number
        self.full_name = full_name
        self.path = os.path.join(os.getcwd(), full_name.replace(" ", ""))

        date = datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")

        self.ledger(
            date,
            round(initial_amount_paid, 2),
            "Credit",
            "Initial amount credited",
            "UPI",
        )

    def previous_balance(self, filename):
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

    def credit_amount(self, amount):
        """
        Add an amount to balance.

        Args:-
            amount(float) :- Amount.

        Return
            Total balance.
        """
        balance = amount + self.previous_balance(self.path + "/ledger.csv")
        return balance

    def debit(self, amount):
        """
        Debit an amount from balance.

        Args:-
            amount(float) :- Amount.

        Return
            Remaining balance.
        """
        balance = self.previous_balance(self.path + "/ledger.csv") - amount
        return balance

    def transaction(self, amount, category, desc, mode_of_payment, credit=False):
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
            amount = self.credit_amount(amount)
        else:
            amount = self.debit(amount)

        if amount < 0:
            return "Unable to make transaction"

        self.ledger(date, round(amount, 2), category, desc, mode_of_payment)
        return "Transaction successful."

    def ledger(self, date, amount, category, desc, mode_of_payment):
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
            "amount": round(amount),
        }

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        with open(self.path + "/ledger.csv", "a", encoding="utf-8") as ledger_file:
            csvwriter = csv.DictWriter(ledger_file, fieldnames=data.keys())
            if ledger_file.tell() == 0:
                csvwriter.writeheader()
            csvwriter.writerow(data)

    def generate_csv_file(self, in_file, out_file, *keys):
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

    def generate_category_report(self):
        """
        Generate category csv file.

        Return
            Name of generated file.
        """
        self.generate_csv_file(
            self.path + "/ledger.csv",
            self.path + "/category.csv",
            "date",
            "category",
            "desc",
            "amount",
        )

        return "category.csv"

    def generate_payment_report(self):
        """
        Generate payment csv file.

        Return
            Name of generated file.
        """
        self.generate_csv_file(
            self.path + "/ledger.csv",
            self.path + "/payment.csv",
            "date",
            "mode_of_payment",
            "desc",
            "amount",
        )

        return "payment.csv"

    def print_report(self):
        """
        Print the information and generate txt and html file.
        """
        with open(self.path + "/ledger.csv", "r", encoding="utf-8") as ledger_file:
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
        today = datetime.date.today()

        for category in categories:
            category_data = []
            for year in years:
                month_end = 13
                if year == today.year:
                    month_end = today.month + 1
                for month in range(1, month_end):
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
                    category_data.append(round(amount, 2))
            categorized_data.append(category_data)

        print(f"{'Category':10}", end="")
        txt = f"{'Category':10}"
        html = "<table><tr><th>Category</th>"

        for year in years:
            month_end = 13
            if year == today.year:
                month_end = today.month + 1
            for month in range(1, month_end):
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

        self.generate_txt_file(txt)
        self.generate_html_file(html)

    def generate_txt_file(self, output):
        """
        Generate txt file for report.
        """
        with open(self.path + "/report.txt", "w", encoding="utf-8") as txt:
            txt.write(output)

    def generate_html_file(self, output):
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

        with open(self.path + "/report.html", "w", encoding="utf-8") as html_file:
            html_file.write(html)


def generate_random_data(n, folder):
    """
    Generate random data for ledger.csv file.
    """
    categories = ["Food", "Rent", "Credit", "Debit", "Fare", "Picnic"]
    mode_of_payment = ["Net Banking", "Mobile Banking", "UPI", "Card Payment"]

    ledger_data = []

    current_year = datetime.date.today().year

    for year in range(current_year - n, current_year):
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

    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(folder + "/ledger.csv", "a", encoding="utf-8") as ledger_file:
        csvwriter = csv.DictWriter(ledger_file, fieldnames=ledger_data[0].keys())
        if ledger_file.tell() == 0:
            csvwriter.writeheader()
        csvwriter.writerows(ledger_data)


if __name__ == "__main__":
    account = Account("111222", "John Mitchell", 2000)
    generate_random_data(2, "JohnMitchell")
    account.print_report()
    print(account.generate_category_report())
    print(account.generate_payment_report())
