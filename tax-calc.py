import pandas as pd
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the config.ini file
config.read("config.ini")

input_file = config["file"]["Input"]
output_file = config["file"]["Output"]


def tax2005_6(income: float) -> float:
    if income <= 7664:
        return 0
    elif income <= 12739:
        y = (income - 7664) / 10000
        return (1767.48 * y + 1500) / 100
    elif income <= 52151:
        z = (income - 12739) / 10000
        return (457.48 * z + 2.397) / 100
    else:
        return 42


def tax2007_8(income: float) -> float:
    if income <= 7664:
        return 0
    elif income <= 12739:
        y = (income - 7664) / 10000
        return (1767.48 * y + 1500) / 100
    elif income <= 52151:
        z = (income - 12739) / 10000
        return (457.48 * z + 2.397) / 100
    elif income <= 250000:
        return 42
    else:
        return 45


def tax2009(income: float) -> float:
    if income <= 7834:
        return 0
    elif income <= 13139:
        y = (income - 7834) / 10000
        return (1873.36 * y + 1400) / 100
    elif income <= 52551:
        z = (income - 13139) / 10000
        return (457.48 * z + 2.397) / 100
    elif income <= 250400:
        return 42
    else:
        return 45


def tax2010(income: float) -> float:
    if income <= 8004:
        return 0
    elif income <= 13469:
        y = (income - 8004) / 10000
        return (1824.34 * y + 1400) / 100
    elif income <= 52881:
        z = (income - 13469) / 10000
        return (457.48 * z + 2.397) / 100
    elif income <= 250730:
        return 42
    else:
        return 45


def calculate_tax(income: float, year: int):
    if year == 2005 or year == 2006:
        return tax2005_6(income)
    elif year == 2007 or year == 2008:
        return tax2007_8(income)
    elif year == 2009:
        return tax2009(income)
    elif year == 2010:
        return tax2010(income)
    else:
        raise ValueError(
            f"year out of range, only valid from 2005-2010, {year} out of range"
        )


def is_married(partner):
    if partner == "[2] Lebenspartner":  # Juliane added new filter -.-
        return 0
    return int(partner[1])  # Assumes second char is bool value


# some logic that should be improved
def do_calculate_tax(row):
    income = row["EKindiv"]
    year = row["syear"]
    return round(calculate_tax(income, year), 2)


# Read dataset
print(input_file)
df = pd.read_excel(input_file)

# Perform tax calculation for each row
df["MTRsolo"] = df.apply(do_calculate_tax, axis=1)

df["MTRsplit"] = df.apply(
    lambda row: (
        round((calculate_tax((row["EKindiv"] + row["EKspouse"] / 2), row["syear"])), 2)
        if is_married(row["partner"])
        else None
    ),
    axis=1,
)

# Write results back to Excel file
df.to_excel("dataset_with_tax.xlsx", index=False)
