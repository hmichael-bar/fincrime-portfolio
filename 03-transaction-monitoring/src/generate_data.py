"""Generate a synthetic KYC + transaction dataset with seeded money-laundering typologies.

EVERYTHING HERE IS FICTIONAL. Names, accounts, companies and the bank
("Meridian Harbor Bank") are randomly generated. Any resemblance to real people
or businesses is coincidence.

Outputs (in ../data):
  customers.csv               KYC profiles the monitoring system can see
  transactions.csv            6 months of activity (Jan-Jun 2026) the system can see
  branches.csv                branch reference table
  ground_truth_customers.csv  WHICH customers are bad actors (hidden from the rules)
  ground_truth_transactions.csv  which transactions belong to a seeded typology

The rules engine and the anomaly model never read the ground_truth files. They are
only used afterwards to score precision and recall.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reference import FATF_GREY  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SEED = 42
START = pd.Timestamp("2026-01-01")
N_DAYS = 181  # 1 Jan - 30 Jun 2026
MONTHS = [(0, 31), (31, 28), (59, 31), (90, 30), (120, 31), (151, 30)]  # (start day, length)

rng = np.random.default_rng(SEED)

# --------------------------------------------------------------------------- names
FIRST = ["James", "Maria", "Wei", "Aisha", "Daniel", "Sofia", "Omar", "Priya", "Michael", "Fatima",
         "Carlos", "Mei", "David", "Yasmin", "Luis", "Grace", "Ahmed", "Hannah", "Jose", "Leila",
         "Kevin", "Ana", "Tariq", "Emily", "Diego", "Nadia", "Brian", "Rosa", "Samuel", "Amira",
         "Jason", "Lucia", "Ravi", "Chloe", "Miguel", "Zainab", "Eric", "Elena", "Kwame", "Sarah",
         "Andre", "Hye-jin", "Noah", "Ines", "Tunde", "Rachel", "Ivan", "Camila", "Yusuf", "Olivia",
         "Hector", "Linh", "Marcus", "Dalia", "Pedro", "Naomi", "Arjun", "Megan", "Karim", "Julia"]
LAST = ["Smith", "Garcia", "Chen", "Haddad", "Johnson", "Rodriguez", "Patel", "Nguyen", "Williams",
        "Khan", "Martinez", "Kim", "Brown", "Okafor", "Lopez", "Cohen", "Hernandez", "Ali", "Davis",
        "Mensah", "Gonzalez", "Wong", "Miller", "Rahman", "Perez", "Silva", "Wilson", "Mansour",
        "Taylor", "Sanchez", "Anderson", "Ibrahim", "Thomas", "Ramirez", "Moore", "Levi", "Jackson",
        "Torres", "Shah", "White", "Flores", "Park", "Harris", "Rivera", "Martin", "Adeyemi", "Clark",
        "Gomez", "Lewis", "Diaz", "Walker", "Reyes", "Young", "Morales", "Allen", "Cruz", "King",
        "Ortiz", "Scott", "Farouk"]

BRANCHES = pd.DataFrame(
    [("BR01", "Jersey City", "NJ"), ("BR02", "Newark", "NJ"), ("BR03", "Paterson", "NJ"),
     ("BR04", "Hoboken", "NJ"), ("BR05", "Brooklyn", "NY"), ("BR06", "Queens", "NY"),
     ("BR07", "Manhattan", "NY"), ("BR08", "Yonkers", "NY"), ("BR09", "Houston", "TX"),
     ("BR10", "El Paso", "TX"), ("BR11", "Phoenix", "AZ"), ("BR12", "Tucson", "AZ"),
     ("BR13", "Los Angeles", "CA"), ("BR14", "San Diego", "CA"), ("BR15", "Miami", "FL"),
     ("BR16", "Orlando", "FL"), ("BR17", "Atlanta", "GA"), ("BR18", "Chicago", "IL"),
     ("BR19", "Philadelphia", "PA"), ("BR20", "Charlotte", "NC")],
    columns=["branch_id", "city", "state"])
BRANCH_STATE = dict(zip(BRANCHES.branch_id, BRANCHES.state))
BRANCHES_BY_STATE = BRANCHES.groupby("state").branch_id.apply(list).to_dict()
HOME_STATE_WEIGHTS = {"NJ": .32, "NY": .30, "TX": .07, "AZ": .04, "CA": .06, "FL": .07,
                      "GA": .04, "IL": .04, "PA": .04, "NC": .02}

MERCHANTS = ["GROCERY MART #221", "FUEL STOP 88", "ONLINE MARKETPLACE", "CITY PHARMACY",
             "BIG BOX STORE #12", "COFFEE HOUSE", "RIDESHARE TRIP", "STREAMING SVC",
             "HOME IMPROVEMENT CTR", "FAST FOOD #430", "DEPARTMENT STORE", "AIRLINE TICKET",
             "ELECTRONICS OUTLET", "GYM MEMBERSHIP", "RESTAURANT", "PET SUPPLY"]
UTILITIES = ["GARDEN STATE ELECTRIC CO", "CITY WATER AUTH", "METRO GAS CO", "CELLCO WIRELESS",
             "FIBERNET ISP", "AUTO INSURANCE CO"]
EMPLOYERS = ["Northgate Logistics Inc", "Riverside Medical Group", "Harborview School District",
             "Summit Retail Holdings", "Atlas Engineering LLC", "Bayside Health Partners",
             "Keystone Transit Authority", "Pinecrest Software Corp", "Liberty Insurance Svcs",
             "Granite State Builders", "Clearwater Pharmacy Inc", "Union County Government",
             "Metro Hospitality Group", "Brightline Telecom", "Oakridge Accounting LLP"]
NATIONALITIES = ["Mexico", "India", "Dominican Republic", "China", "Philippines", "Egypt",
                 "Lebanon", "Nigeria", "Colombia", "Vietnam", "Jamaica", "Pakistan", "Haiti",
                 "Ecuador", "Kenya", "Bangladesh", "Israel", "Morocco"]
CRYPTO_EXCHANGES = ["CoinHarbor Exchange", "BlockVault Markets", "SatoshiPay Kiosk"]
MULE_MEMOS = ["investment", "crypto profit release fee", "rent deposit", "gift", "loan repayment",
              "invoice", "shipping fee", "romance - for you", "tax release fee", ""]


def person():
    return f"{rng.choice(FIRST)} {rng.choice(LAST)}"


USED_NAMES: set[str] = set()


def unique_person():
    """Customer names are unique so case files never confuse two people."""
    while True:
        n = person()
        if n not in USED_NAMES:
            USED_NAMES.add(n)
            return n


def ext_acct(prefix="EXT"):
    return f"{prefix}{rng.integers(10**8, 10**9)}"


# ------------------------------------------------------------------- transactions
TX: list[dict] = []
IN_TYPES = {"CASH_DEPOSIT", "WIRE_IN", "ACH_IN", "P2P_IN", "CRYPTO_SELL"}
DEFAULT_CHANNEL = {"CASH_DEPOSIT": "branch", "CASH_WITHDRAWAL": "atm", "WIRE_IN": "wire",
                   "WIRE_OUT": "online", "ACH_IN": "ach", "ACH_OUT": "ach", "P2P_IN": "mobile",
                   "P2P_OUT": "mobile", "CRYPTO_BUY": "online", "CRYPTO_SELL": "online",
                   "CARD_PURCHASE": "card"}


def add(c, day, ttype, amount, cp_name="", cp_acct="", cp_country="United States",
        channel=None, memo="", branch=None, tag=None, device=None, hours=(8, 20), force=False):
    """Append one transaction for customer c on day offset `day`.

    Baseline activity (force=False) is suppressed before the account opens and during
    any dormancy block. Typology overlays pass force=True.
    """
    day = int(day)
    if day < 0 or day >= N_DAYS:
        return None
    if not force:
        if day < c["_active_from"]:
            return None
        if any(a <= day <= b for a, b in c["_blocked"]):
            return None
    if tag is not None:  # low-intensity bad actors move smaller amounts and are harder to catch
        amount = amount * c.get("_intensity", 1.0)
    channel = channel or DEFAULT_CHANNEL[ttype]
    if channel in ("branch", "atm") and branch is None:
        branch = c["home_branch"]
    if channel in ("online", "mobile") and device is None:
        device = c["device_id"]
    ts = START + pd.Timedelta(days=day, seconds=int(rng.integers(hours[0] * 3600, hours[1] * 3600)))
    rec = dict(customer_id=c["customer_id"], account_no=c["account_no"], timestamp=ts,
               txn_type=ttype, direction="IN" if ttype in IN_TYPES else "OUT",
               amount=round(float(amount), 2), channel=channel, branch_id=branch or "",
               branch_state=BRANCH_STATE.get(branch, "") if branch else "",
               counterparty_name=cp_name, counterparty_account=cp_acct,
               counterparty_country=cp_country, memo=memo, device_id=device or "", _tag=tag)
    TX.append(rec)
    return rec


def poisson(lam):
    return int(rng.poisson(lam))


def days_in(ms, ml, n):
    return np.sort(rng.integers(ms, ms + ml, size=n))


# ------------------------------------------------------------- baseline segments
def card_and_atm(c, ms, ml, card_lam=14, card_mu=45, atm_lam=2):
    for d in days_in(ms, ml, poisson(card_lam * 0.3)):  # card spend kept light to hold the file to ~50k rows
        add(c, d, "CARD_PURCHASE", rng.lognormal(np.log(card_mu), 0.8), rng.choice(MERCHANTS))
    for d in days_in(ms, ml, poisson(atm_lam)):
        add(c, d, "CASH_WITHDRAWAL", 20 * rng.integers(2, 20), "ATM")


def p2p_social(c, ms, ml, out_lam=2, in_lam=1):
    for d in days_in(ms, ml, poisson(out_lam)):
        f = c["_friends"][rng.integers(len(c["_friends"]))]
        add(c, d, "P2P_OUT", rng.uniform(15, 300), f[0], f[1], memo=rng.choice(["dinner", "split", "", "thanks"]))
    for d in days_in(ms, ml, poisson(in_lam)):
        f = c["_friends"][rng.integers(len(c["_friends"]))]
        add(c, d, "P2P_IN", rng.uniform(15, 250), f[0], f[1], memo=rng.choice(["", "rent share", "tickets"]))


def household_bills(c, ms, rent):
    add(c, ms + rng.integers(0, 3), "ACH_OUT", rent, c["_landlord"], c["_landlord_acct"], memo="RENT")
    for u in rng.choice(UTILITIES, size=rng.integers(2, 4), replace=False):
        add(c, ms + rng.integers(5, 25), "ACH_OUT", rng.uniform(55, 260), u, "UTIL" + u[:4].upper(), memo="AUTOPAY")


def seg_salaried(c):
    sal = float(np.clip(rng.lognormal(np.log(66000), 0.35), 32000, 190000))
    c["_income"] = sal
    emp_acct = ext_acct("EMP")
    for d in range(int(rng.integers(0, 14)), N_DAYS, 14):
        add(c, d, "ACH_IN", sal / 26 * rng.uniform(0.98, 1.02), c["_employer"], emp_acct,
            memo="PAYROLL DIRECT DEP", hours=(2, 6))
    rent = sal / 12 * rng.uniform(0.22, 0.34)
    for ms, ml in MONTHS:
        household_bills(c, ms, rent)
        card_and_atm(c, ms, ml)
        p2p_social(c, ms, ml)
        for d in days_in(ms, ml, poisson(0.25)):
            add(c, d, "CASH_DEPOSIT", rng.uniform(100, 1800))
        if c.get("_remit_country") and rng.random() < 0.8:
            add(c, ms + rng.integers(0, ml), "WIRE_OUT", rng.uniform(200, 1600), c["_remit_name"],
                ext_acct("INTL"), c["_remit_country"], memo="FAMILY SUPPORT")
        if c.get("_travel"):  # e.g. truck drivers / travel nurses deposit cash on the road
            for d in days_in(ms, ml, poisson(1.2)):
                st = rng.choice([s for s in BRANCHES_BY_STATE if s != c["home_state"]])
                add(c, d, "CASH_DEPOSIT", rng.uniform(150, 2200), branch=rng.choice(BRANCHES_BY_STATE[st]))
        if c.get("_crypto"):
            for d in days_in(ms, ml, poisson(3)):
                add(c, d, "CRYPTO_BUY", rng.uniform(150, 4000), rng.choice(CRYPTO_EXCHANGES), "XCH001")
            for d in days_in(ms, ml, poisson(0.6)):
                add(c, d, "CRYPTO_SELL", rng.uniform(300, 6000), rng.choice(CRYPTO_EXCHANGES), "XCH001")


def seg_retiree(c):
    ss = rng.uniform(1400, 3200)
    pension = ss * rng.uniform(0, 0.9)
    for ms, ml in MONTHS:
        add(c, ms + 2, "ACH_IN", ss, "SSA TREAS 310", "TREAS310", memo="SOC SEC", hours=(2, 6))
        if pension > 300:
            add(c, ms + 0, "ACH_IN", pension, "State Pension Fund", "PENS01", memo="PENSION", hours=(2, 6))
        for u in rng.choice(UTILITIES, size=2, replace=False):
            add(c, ms + rng.integers(5, 25), "ACH_OUT", rng.uniform(55, 220), u, "UTIL" + u[:4].upper())
        card_and_atm(c, ms, ml, card_lam=10, card_mu=38, atm_lam=3)
        p2p_social(c, ms, ml, 0.5, 0.5)


def seg_student(c):
    intl = c["nationality"] != "United States"
    for ms, ml in MONTHS:
        if intl:
            if rng.random() < 0.45:
                add(c, ms + rng.integers(0, ml), "WIRE_IN", rng.uniform(2000, 14000), c["_parent"],
                    ext_acct("INTL"), c["nationality"], memo="TUITION AND LIVING EXPENSES")
        else:
            add(c, ms + rng.integers(0, 5), "ACH_IN", rng.uniform(400, 1800), c["_parent"], c["_parent_acct"], memo="TRANSFER")
        add(c, ms + rng.integers(0, 4), "ACH_OUT", rng.uniform(700, 1500), c["_landlord"], c["_landlord_acct"], memo="RENT")
        card_and_atm(c, ms, ml, card_lam=18, card_mu=22, atm_lam=1.5)
        p2p_social(c, ms, ml, 5, 3)
    if intl:  # spring tuition
        add(c, 10 + rng.integers(0, 20), "WIRE_OUT", rng.uniform(9000, 26000), "Metro State University",
            "UNIV001", memo="SPRING TUITION")


def seg_gig(c):
    platform = rng.choice(["RideNow Payouts", "DashFleet Payouts", "TaskHub Inc", "CreatorPay"])
    for ms, ml in MONTHS:
        for d in range(ms + int(rng.integers(0, 7)), ms + ml, 7):
            add(c, d, "ACH_IN", rng.uniform(180, 950), platform, "PLAT" + platform[:3].upper(), memo="WEEKLY PAYOUT")
        for d in days_in(ms, ml, poisson(10)):  # many small clients -> many distinct senders
            add(c, d, "P2P_IN", rng.uniform(15, 260), person(), ext_acct(), memo=rng.choice(["session", "design work", "lesson", ""]))
        household_bills(c, ms, rng.uniform(900, 1700))
        card_and_atm(c, ms, ml, card_lam=16, card_mu=35)
        p2p_social(c, ms, ml, 3, 1)
        if rng.random() < 0.3:
            add(c, ms + rng.integers(0, ml), "CRYPTO_BUY", rng.uniform(50, 600), rng.choice(CRYPTO_EXCHANGES), "XCH001")


def seg_cash_business(c):
    size = c["_biz_size"]  # mean cash deposit
    payroll = size * rng.uniform(3, 6)
    supplier = person().split()[1] + " Wholesale Foods"
    proc = rng.choice(["SquareTill Merchant Svcs", "CardFlow Processing", "PayPoint Settlements"])
    for ms, ml in MONTHS:
        for wk in range(ms, ms + ml, 7):
            for d in sorted(rng.choice(range(wk, min(wk + 7, ms + ml)), size=min(rng.integers(3, 6), min(7, ms + ml - wk)), replace=False)):
                amt = rng.lognormal(np.log(size), 0.45)
                if amt > 7500 and rng.random() < 0.5:  # many owners split nothing; amounts just land where they land
                    amt *= rng.uniform(0.9, 1.25)
                add(c, d, "CASH_DEPOSIT", amt, memo="DAILY RECEIPTS", hours=(9, 18))
            add(c, wk + rng.integers(0, 3), "ACH_IN", size * rng.uniform(1.5, 4), proc, "PROC01", memo="CARD SETTLEMENT")
            add(c, wk + rng.integers(1, 5), "ACH_OUT", size * rng.uniform(0.8, 2.0), supplier, "SUPP01", memo="SUPPLIES")
        for d in (ms + 13, ms + 27):
            add(c, d, "ACH_OUT", payroll * rng.uniform(0.95, 1.05), "PayrollPro Services", "PAYR01", memo="PAYROLL")
        add(c, ms + 1, "ACH_OUT", size * rng.uniform(2, 4), c["_landlord"], c["_landlord_acct"], memo="COMMERCIAL RENT")
        add(c, ms + rng.integers(10, 20), "ACH_OUT", size * rng.uniform(0.5, 1.5), "NJ Div of Taxation", "TAX01", memo="SALES TAX")
        card_and_atm(c, ms, ml, card_lam=6, card_mu=120, atm_lam=0.5)


def seg_import_export(c):
    goods = c["expected_goods"]
    suppliers = c["_suppliers"]  # list of (name, country)
    buyers = [(person().split()[1] + " " + rng.choice(["Retail", "Stores", "Distributors"]) + " Inc", ext_acct("CUST")) for _ in range(6)]
    fixed = c.get("_fixed_order")
    inv = int(rng.integers(1000, 8000))
    for ms, ml in MONTHS:
        for d in days_in(ms, ml, int(rng.integers(2, 5))):
            name, ctry = suppliers[rng.integers(len(suppliers))]
            amt = fixed if (fixed and rng.random() < 0.6) else rng.uniform(8000, 85000)
            inv += int(rng.integers(1, 40))
            add(c, d, "WIRE_OUT", amt, name, ext_acct("INTL"), ctry, memo=f"INV-{inv} {goods}")
        for d in days_in(ms, ml, int(rng.integers(6, 14))):
            b = buyers[rng.integers(len(buyers))]
            add(c, d, "ACH_IN", rng.uniform(2500, 32000), b[0], b[1], memo="PAYMENT FOR ORDER")
        for d in (ms + 13, ms + 27):
            add(c, d, "ACH_OUT", rng.uniform(9000, 30000), "PayrollPro Services", "PAYR01", memo="PAYROLL")
        add(c, ms + 1, "ACH_OUT", rng.uniform(5000, 15000), c["_landlord"], c["_landlord_acct"], memo="WAREHOUSE LEASE")
        add(c, ms + rng.integers(5, 20), "ACH_OUT", rng.uniform(2000, 9000), "Port Freight Forwarders", "FRT01", memo="FREIGHT")
        card_and_atm(c, ms, ml, card_lam=8, card_mu=150, atm_lam=0.3)


def seg_professional(c):
    sal = rng.uniform(180000, 420000)
    c["_income"] = sal
    emp_acct = ext_acct("EMP")
    for d in range(int(rng.integers(0, 15)), N_DAYS, 15):
        add(c, d, "ACH_IN", sal / 24 * rng.uniform(0.98, 1.02), c["_employer"], emp_acct, memo="PAYROLL", hours=(2, 6))
    for ms, ml in MONTHS:
        add(c, ms + rng.integers(0, 3), "ACH_OUT", sal / 12 * rng.uniform(0.15, 0.25), "Home Mortgage Servicing", "MTG01", memo="MORTGAGE")
        card_and_atm(c, ms, ml, card_lam=22, card_mu=90, atm_lam=1)
        p2p_social(c, ms, ml, 2, 1)
        if rng.random() < 0.35:
            add(c, ms + rng.integers(0, ml), "WIRE_OUT", float(rng.choice([5000, 10000, 15000, 25000])),
                "Granite Brokerage LLC", "BRK001", memo="TRANSFER TO BROKERAGE ACCT")
    if c.get("_closing"):  # buys a home: brokerage -> account -> title company within days (classic FP)
        d = int(rng.integers(30, 160))
        price = float(rng.choice([150000, 185000, 220000, 260000, 310000]))
        add(c, d, "WIRE_IN", price * rng.uniform(1.0, 1.04), "Granite Brokerage LLC", "BRK001", memo="LIQUIDATION PROCEEDS")
        add(c, d + int(rng.integers(1, 3)), "WIRE_OUT", price, "First Keystone Title Agency", "TTL001", memo="CLOSING FUNDS - 14 ELM ST")


def seg_property_mgmt(c):
    tenants = [(person(), ext_acct()) for _ in range(int(rng.integers(14, 36)))]
    owners = [(person(), ext_acct("OWN")) for _ in range(int(rng.integers(3, 7)))]
    for ms, ml in MONTHS:
        collected = 0
        for t in tenants:
            amt = rng.uniform(1200, 3400)
            collected += amt
            add(c, ms + rng.integers(0, 6), "ACH_IN", amt, t[0], t[1], memo="RENT")
        for o in owners:  # owner distributions, often round amounts
            amt = float(round(collected * 0.8 / len(owners), -3)) if rng.random() < 0.6 else collected * 0.8 / len(owners)
            add(c, ms + rng.integers(10, 15), "WIRE_OUT", amt, o[0], o[1], memo="OWNER DISTRIBUTION")
        add(c, ms + rng.integers(5, 25), "ACH_OUT", collected * 0.1, "Ace Building Maintenance", "MNT01", memo="MAINTENANCE")
        card_and_atm(c, ms, ml, card_lam=5, card_mu=200, atm_lam=0.2)


def seg_low_activity(c):
    base = rng.uniform(300, 1400)
    for ms, ml in MONTHS:
        if rng.random() < 0.8:
            add(c, ms + rng.integers(0, 5), "ACH_IN", base, c["_parent"], c["_parent_acct"], memo="TRANSFER")
        card_and_atm(c, ms, ml, card_lam=4, card_mu=40, atm_lam=1)
    if c.get("_lump"):  # legit lump after a quiet spell: tax refund / insurance / estate
        d = c["_blocked"][0][1] + 1 if c["_blocked"] else int(rng.integers(60, 170))
        name, memo, amt = c["_lump"]
        add(c, d, "ACH_IN" if amt < 10000 else "WIRE_IN", amt, name, ext_acct("LMP"), memo=memo)
        add(c, d + int(rng.integers(3, 15)), "ACH_OUT", amt * rng.uniform(0.3, 0.7), "Home Equity Lender", "HEL01", memo="LOAN PAYOFF")


SEGMENT_FN = {"salaried": seg_salaried, "retiree": seg_retiree, "student": seg_student,
              "gig": seg_gig, "cash_business": seg_cash_business, "import_export": seg_import_export,
              "professional": seg_professional, "property_mgmt": seg_property_mgmt,
              "crypto_investor": seg_salaried, "low_activity": seg_low_activity}

OCCUPATIONS = {
    "salaried": ["Registered Nurse", "Software Developer", "Teacher", "Accountant", "Retail Manager",
                 "Pharmacist", "Electrician", "Administrative Assistant", "Police Officer",
                 "Marketing Coordinator", "Dental Hygienist", "Paralegal", "HVAC Technician", "Bus Operator"],
    "retiree": ["Retired"], "student": ["Student"],
    "gig": ["Rideshare Driver", "Freelance Designer", "Delivery Courier", "Freelance Photographer", "Personal Trainer", "Tutor"],
    "professional": ["Physician", "Attorney", "Engineering Manager", "Financial Analyst", "Dentist", "Architect"],
    "crypto_investor": ["Software Developer", "Financial Analyst", "Sales Representative", "Data Analyst"],
    "low_activity": ["Homemaker", "Unemployed", "Part-time Cashier", "Retired"],
}
CASH_BIZ = ["Restaurant", "Deli / Bodega", "Laundromat", "Nail Salon", "Food Truck", "Convenience Store", "Car Wash", "Barbershop"]
TRADE_GOODS = {"textiles": [("Zhejiang Silkline Textiles Co", "China"), ("Bursa Weave Tekstil AS", "Turkey"), ("Saigon Garment JSC", "Vietnam")],
               "auto parts": [("Ningbo Precision Auto Parts", "China"), ("Monterrey Autopartes SA", "Mexico")],
               "furniture": [("Foshan Homecraft Furniture", "China"), ("Binh Duong Woodworks", "Vietnam")],
               "food products": [("Anatolia Dried Fruits AS", "Turkey"), ("Gujarat Spice Exports Pvt", "India")],
               "cosmetics": [("Seoul Glow Cosmetics", "South Korea"), ("Dubai Fragrance Trading FZE", "United Arab Emirates")],
               "used clothing": [("Pacific Rag Exporters", "Pakistan")],
               "mobile phone accessories": [("Shenzhen Brightcase Electronics", "China"), ("Jebel Ali Gadget Hub FZE", "United Arab Emirates")]}
WEIGHTS = {"salaried": .36, "retiree": .10, "student": .08, "gig": .08, "cash_business": .10,
           "import_export": .06, "professional": .08, "property_mgmt": .04, "crypto_investor": .05, "low_activity": .05}


# --------------------------------------------------------------------- customers
def make_customer(i, segment):
    c = dict(customer_id=f"C{i:04d}", account_no=f"MHB{rng.integers(10**7, 10**8)}", _segment=segment,
             _active_from=0, _blocked=[], _typology="none", _role="")
    c["home_state"] = rng.choice(list(HOME_STATE_WEIGHTS), p=list(HOME_STATE_WEIGHTS.values()))
    c["home_branch"] = rng.choice(BRANCHES_BY_STATE[c["home_state"]])
    c["device_id"] = f"DEV-{rng.integers(10**5, 10**6)}"
    business = segment in ("cash_business", "import_export", "property_mgmt")
    c["customer_type"] = "Business" if business else "Individual"
    c["nationality"] = "United States" if rng.random() < 0.68 else rng.choice(NATIONALITIES)
    if segment == "student" and rng.random() < 0.5:
        c["nationality"] = rng.choice(["India", "China", "Nigeria", "Vietnam", "Lebanon", "Kenya", "South Korea", "Brazil"])
    owner = unique_person()
    if segment == "cash_business":
        bt = rng.choice(CASH_BIZ)
        c["name"] = f"{owner.split()[1]} {bt.split(' /')[0]} LLC"
        c["occupation"] = bt
        c["_biz_size"] = float(rng.choice([900, 1500, 2500, 4000, 6000], p=[.25, .3, .25, .12, .08]))
    elif segment == "import_export":
        goods = rng.choice(list(TRADE_GOODS))
        c["name"] = f"{owner.split()[1]} {rng.choice(['Global', 'Trading', 'International', 'Imports'])} LLC"
        c["occupation"] = f"Import/Export - {goods.title()}"
        c["expected_goods"] = goods
        c["_suppliers"] = TRADE_GOODS[goods]
        if rng.random() < 0.3:
            c["_fixed_order"] = float(round(rng.uniform(12000, 40000), 2))
    elif segment == "property_mgmt":
        c["name"] = f"{owner.split()[1]} Property Management LLC"
        c["occupation"] = "Property Management"
    else:
        c["name"] = owner
        c["occupation"] = rng.choice(OCCUPATIONS[segment])
    c.setdefault("expected_goods", "")
    c["beneficial_owner"] = owner if business else ""
    c["age"] = int(rng.integers(19, 26)) if segment == "student" else int(rng.integers(66, 88)) if segment == "retiree" else int(rng.integers(24, 66))
    c["account_open_date"] = (pd.Timestamp("2008-01-01") + pd.Timedelta(days=int(rng.integers(0, 6200)))).date()
    c["last_txn_before_2026"] = (pd.Timestamp("2025-12-31") - pd.Timedelta(days=int(rng.integers(0, 12)))).date()
    c["pep_flag"] = bool(rng.random() < 0.01)
    c["_employer"] = rng.choice(EMPLOYERS)
    c["_landlord"] = person() + " Realty"
    c["_landlord_acct"] = ext_acct("LND")
    c["_parent"] = person()
    c["_parent_acct"] = ext_acct()
    c["_friends"] = [(person(), ext_acct()) for _ in range(6)]
    if c["nationality"] != "United States" and segment in ("salaried", "gig") and rng.random() < 0.5:
        c["_remit_country"] = c["nationality"]
        c["_remit_name"] = person()
    if segment == "salaried" and rng.random() < 0.06:
        c["_travel"] = True
        c["occupation"] = rng.choice(["Truck Driver", "Travel Nurse"])
    if segment == "crypto_investor":
        c["_crypto"] = True
    if segment == "professional" and rng.random() < 0.3:
        c["_closing"] = True
    if segment == "low_activity" and rng.random() < 0.45:
        a = int(rng.integers(5, 40))
        c["_blocked"] = [(a, a + int(rng.integers(95, 130)))]
        c["_lump"] = [("IRS TREAS 310", "TAX REFUND", rng.uniform(1500, 6000)),
                      ("Hartwell & Lowe Estate Attorneys", "ESTATE DISTRIBUTION", rng.uniform(20000, 65000)),
                      ("Shield Mutual Insurance", "CLAIM SETTLEMENT", rng.uniform(12000, 40000))][rng.integers(3)]
    return c


# ---------------------------------------------------------------- typology overlays
def ty_structuring(c, smart=False):
    lo, hi = (4600, 7800) if smart else (8100, 9950)
    nearby = BRANCHES_BY_STATE[c["home_state"]] + (BRANCHES_BY_STATE.get("NY" if c["home_state"] == "NJ" else "NJ", []))
    for _ in range(int(rng.integers(3, 6))):
        start = int(rng.integers(0, N_DAYS - 8))
        for k in range(int(rng.integers(3, 6))):
            amt = round(rng.uniform(lo, hi), -1 if rng.random() < 0.5 else -2)
            add(c, start + int(rng.integers(0, 6)), "CASH_DEPOSIT", amt, branch=rng.choice(nearby), tag="structuring", force=True)
        add(c, start + int(rng.integers(6, 12)), "ACH_OUT", rng.uniform(15000, 30000), "Self - Ext Acct Pinnacle Bank", ext_acct(),
            memo="TRANSFER TO OWN ACCOUNT", tag="structuring", force=True)


def ty_rapid(c):
    senders = [("Sterling Pacific Holdings Ltd", "Hong Kong"), ("Larnaca Meridian Ventures", "Cyprus"),
               ("Northbridge Commodities LLC", "United States"), ("Vistula Capital Sp z o o", "Poland")]
    receivers = [("Golden Crest General Trading LLC", "United Arab Emirates"), ("Kowloon Bayview Ltd", "Hong Kong"),
                 ("Baltic Amber Consulting SIA", "Latvia"), ("Bosphorus Line Dis Ticaret", "Turkey")]
    for _ in range(int(rng.integers(4, 7))):
        d = int(rng.integers(0, N_DAYS - 4))
        s = senders[rng.integers(len(senders))]
        amt = rng.uniform(25000, 180000)
        add(c, d, "WIRE_IN", amt, s[0], ext_acct("INTL"), s[1], memo=rng.choice(["CONSULTING FEE", "LOAN", "INVOICE 2026-03", ""]), tag="rapid_movement", force=True)
        remaining = amt * rng.uniform(0.92, 0.99)
        for part in ([remaining] if rng.random() < 0.5 else [remaining * 0.6, remaining * 0.4]):
            r = receivers[rng.integers(len(receivers))]
            add(c, d + int(rng.integers(0, 3)), "WIRE_OUT", part, r[0], ext_acct("INTL"), r[1], memo=rng.choice(["SERVICES", "PAYMENT", ""]), tag="rapid_movement", force=True)


def ty_funnel(c):
    far = [s for s in ["TX", "AZ", "CA", "FL", "GA", "IL"] if s != c["home_state"]]
    for wk in range(14, N_DAYS - 7, 7):
        total = 0
        for _ in range(poisson(4) + 1):
            st = rng.choice(far)
            amt = rng.uniform(1200, 6500)
            total += amt
            add(c, wk + int(rng.integers(0, 6)), "CASH_DEPOSIT", amt, branch=rng.choice(BRANCHES_BY_STATE[st]), memo="", tag="funnel", force=True)
        if rng.random() < 0.5:
            add(c, wk + 6, "CASH_WITHDRAWAL", min(total * 0.9, 9000), "BRANCH TELLER", channel="branch", tag="funnel", force=True)
        else:
            dest = rng.choice([("Comercializadora del Norte SA", "Mexico"), ("Importadora Quetzal Ltda", "Guatemala"), ("Yiwu Bright Star Trading", "China")])
            add(c, wk + 6, "WIRE_OUT", total * rng.uniform(0.85, 0.95), dest[0], ext_acct("INTL"), dest[1], memo="MERCHANDISE", tag="funnel", force=True)


def ty_high_risk_geo(c):
    dests = [("Caracas Andes Import CA", "Venezuela"), ("Cedar Coast Exchange SAL", "Lebanon"),
             ("Juba Frontier Supplies", "South Sudan"), ("Port-au-Prince Commerce SA", "Haiti"),
             ("Aden Gate Trading Est", "Yemen"), ("Vientiane Mekong Trading", "Laos"),
             ("Al Safwa Exchange House LLC", "United Arab Emirates"), ("Bishkek Silkroad LLC", "Kyrgyzstan"),
             ("Yerevan Ararat Trade LLC", "Armenia"), ("Mandalay Jade Holdings", "Myanmar")]
    picks = rng.choice(len(dests), size=3, replace=False)
    for _ in range(int(rng.integers(6, 11))):
        dname, dc = dests[picks[rng.integers(3)]]
        d = int(rng.integers(5, N_DAYS))
        amt = rng.uniform(9000, 70000)
        add(c, d - int(rng.integers(1, 5)), "WIRE_IN", amt * rng.uniform(1.0, 1.05), "Brightwater Holdings LLC", ext_acct(), "United States", memo="LOAN", tag="high_risk_geo", force=True)
        add(c, d, "WIRE_OUT", amt, dname, ext_acct("INTL"), dc, memo=rng.choice(["GOODS", "FAMILY", "BUSINESS", ""]), tag="high_risk_geo", force=True)


def ty_round_dollar(c):
    shells = [("Teton Ridge Advisors LLC", "United States"), ("Cheyenne Peak Holdings LLC", "United States"),
              ("Tortola Harbour Ltd", "British Virgin Islands"), ("Limassol Crest Services", "Cyprus"),
              ("Delmarva Strategic LLC", "United States")]
    use = [shells[i] for i in rng.choice(len(shells), size=3, replace=False)]
    for _ in range(int(rng.integers(8, 13))):
        d = int(rng.integers(3, N_DAYS))
        amt = float(rng.choice([10000, 15000, 20000, 25000, 40000, 50000]))
        add(c, d - int(rng.integers(1, 4)), "WIRE_IN", amt + float(rng.choice([0, 0, 5000])), "Evergreen Consulting Partners LLC", ext_acct(), memo="RETAINER", tag="round_dollar", force=True)
        s = use[rng.integers(len(use))]
        add(c, d, "WIRE_OUT", amt, s[0], ext_acct("INTL" if s[1] != "United States" else "EXT"), s[1], memo=rng.choice(["CONSULTING SERVICES", "LOAN", "ADVISORY FEE", ""]), tag="round_dollar", force=True)


def ty_dormant(c):
    r = c["_active_from"]
    for k in range(int(rng.integers(3, 6))):
        d = r + k * int(rng.integers(3, 9))
        amt = rng.uniform(15000, 85000)
        if rng.random() < 0.6:
            add(c, d, "WIRE_IN", amt, rng.choice(["Orion Asset Partners Ltd", "Meridian Star Holdings", "Quick Funds Transfer Co"]), ext_acct("INTL"), rng.choice(["Hong Kong", "United Arab Emirates", "United Kingdom"]), memo="", tag="dormant_reactivation", force=True)
        else:
            add(c, d, "CASH_DEPOSIT", min(amt, 9800), tag="dormant_reactivation", force=True)
            amt = min(amt, 9800)
        out = rng.choice(["wire", "crypto", "cash"])
        if out == "wire":
            add(c, d + 1, "WIRE_OUT", amt * 0.95, "Danube Reliance Trading", ext_acct("INTL"), "Turkey", memo="PAYMENT", tag="dormant_reactivation", force=True)
        elif out == "crypto":
            add(c, d + 1, "CRYPTO_BUY", amt * 0.9, rng.choice(CRYPTO_EXCHANGES), "XCH001", tag="dormant_reactivation", force=True)
        else:
            add(c, d + 2, "CASH_WITHDRAWAL", min(amt * 0.9, 9500), "BRANCH TELLER", channel="branch", tag="dormant_reactivation", force=True)


def ty_tbml(c):
    fz = [("Gulf Horizon General Trading FZE", "United Arab Emirates"), ("Hamriyah Polar Star FZC", "United Arab Emirates"),
          ("Al Rasheed Industrial Supplies FZCO", "United Arab Emirates"), ("Victoria Harbour Components Ltd", "Hong Kong")]
    payers = [("Ala-Too Logistics OSOO", "Kyrgyzstan"), ("Ararat Machinery LLC", "Armenia"), ("Anadolu Sanayi Ticaret", "Turkey")]
    mismatch = rng.choice(["industrial electronics", "CNC machine parts", "aircraft spare parts", "semiconductor modules", "marine engines"])
    inv = int(rng.integers(100, 400))
    repeat_amt = float(round(rng.uniform(30000, 75000), -1) + rng.choice([0, 0.5]) * 500)
    for k in range(int(rng.integers(6, 11))):
        d = int(rng.integers(0, N_DAYS - 3))
        f = fz[rng.integers(len(fz))]
        inv += 1
        amt = repeat_amt if rng.random() < 0.55 else rng.uniform(20000, 120000)
        add(c, d, "WIRE_OUT", amt, f[0], ext_acct("INTL"), f[1], memo=f"INV-2026-{inv:04d} {mismatch}", tag="tbml", force=True)
        if rng.random() < 0.6:  # third-party payments "on behalf of" the buyer
            p = payers[rng.integers(len(payers))]
            add(c, d - int(rng.integers(1, 6)), "WIRE_IN", amt * rng.uniform(1.05, 1.3), p[0], ext_acct("INTL"), p[1],
                memo=f"INV-2026-{inv:04d} PAYMENT ON BEHALF OF BUYER", tag="tbml", force=True)


MULE_DEVICES = ["DEV-M00001", "DEV-M00002", "DEV-M00003"]
COLLECTOR_BENE_COUNTRY = {"Kowloon Bayview Ltd": "Hong Kong", "Golden Crest General Trading LLC": "United Arab Emirates"}


def ty_mule_network(mules, collectors):
    for m in mules:
        start = max(m["_active_from"], int(rng.integers(20, 70)))
        for d in range(start, N_DAYS - 2):
            if rng.random() > 0.55:
                continue
            got = 0.0
            for _ in range(poisson(1.6) + 1):  # victims: each a distinct person
                amt = rng.uniform(250, 4800)
                got += amt
                add(m, d, rng.choice(["P2P_IN", "P2P_IN", "ACH_IN"]), amt, person(), ext_acct(), memo=rng.choice(MULE_MEMOS), tag="mule_network", force=True)
            out = got * rng.uniform(0.85, 0.96)
            how = rng.choice(["collector", "collector", "crypto", "atm"])
            if how == "collector":
                col = collectors[rng.integers(len(collectors))]
                dd = d + int(rng.integers(0, 2))
                add(m, dd, "P2P_OUT", out, col["name"], col["account_no"], memo="", tag="mule_network", force=True)
                rec = add(col, dd, "P2P_IN", out, m["name"], m["account_no"], memo="", tag="mule_network", force=True)
                if rec:
                    col.setdefault("_recv", []).append((dd, rec["amount"]))
            elif how == "crypto":
                add(m, d + int(rng.integers(0, 2)), "CRYPTO_BUY", out, rng.choice(CRYPTO_EXCHANGES), "XCH001", tag="mule_network", force=True)
            else:
                add(m, d + 1, "CASH_WITHDRAWAL", min(out, 3000), "ATM", tag="mule_network", force=True)
    for col in collectors:  # every few days the collector sweeps what arrived: ~70% by wire abroad, ~25% into crypto
        recv = col.get("_recv", [])
        for d0 in range(0, N_DAYS, 4):
            got = sum(a for d, a in recv if d0 <= d < d0 + 4)
            if got < 3000:
                continue
            amt = got * rng.uniform(0.65, 0.75)
            bene = str(rng.choice(["Kowloon Bayview Ltd", "Golden Crest General Trading LLC"]))
            acct = ext_acct("INTL")
            rng.choice(["Hong Kong", "United Arab Emirates"])  # draw kept so the random stream (and alert IDs) stay stable
            add(col, d0 + 4, "WIRE_OUT", amt, bene, acct, COLLECTOR_BENE_COUNTRY[bene], memo="GOODS", tag="mule_network", force=True)
            add(col, d0 + 5, "CRYPTO_BUY", got * rng.uniform(0.2, 0.28), rng.choice(CRYPTO_EXCHANGES), "XCH001", tag="mule_network", force=True)


# ------------------------------------------------------------- legitimate noise
def life_events(normals):
    """Legitimate but unusual one-off events that happen AFTER the KYC profile was written.

    These are the raw material of false positives: a wedding paid for in Beirut, a car
    sold for cash, an inheritance. Nothing here is tagged as suspicious.
    """
    abroad = [("WEDDING VENUE PAYMENT", "Lebanon", "Le Jardin Events SAL"), ("PROPERTY DEPOSIT - ANTALYA", "Turkey", "Antalya Coast Realty"),
              ("HOSPITAL BILL - NAIROBI", "Kenya", "Aga Medical Centre"), ("GOLD JEWELRY - DUBAI", "United Arab Emirates", "Deira Gold Souk Jewellers LLC"),
              ("FAMILY HOME REPAIR", "Vietnam", "Hanoi Build Co"), ("UNIVERSITY FEES - TBILISI", "Georgia", "Tbilisi State Medical Univ"),
              ("FAMILY SUPPORT - HURRICANE", "Haiti", None), ("FUNERAL EXPENSES", "Lebanon", None)]
    for c in normals:
        r = rng.random()
        d = int(rng.integers(5, N_DAYS - 10))
        if r < 0.07:  # one-off overseas wire outside the KYC profile
            memo, ctry, name = abroad[rng.integers(len(abroad))]
            amt = rng.uniform(4000, 45000)
            if amt > 15000:  # usually funded first (savings transfer / loan)
                add(c, d - 2, "ACH_IN", amt * rng.uniform(1.0, 1.1), "Own Savings - Pinnacle Bank", ext_acct(), memo="TRANSFER FROM SAVINGS")
            add(c, d, "WIRE_OUT", amt, name or person(), ext_acct("INTL"), ctry, memo=memo)
        elif r < 0.12:  # sells old car, buys new one within days
            sale = rng.uniform(22000, 48000)
            add(c, d, "ACH_IN", sale, "AutoBid Online Car Buyer", ext_acct(), memo="VEHICLE PURCHASE PAYOUT")
            add(c, d + int(rng.integers(1, 3)), "WIRE_OUT", sale * rng.uniform(0.95, 1.2), "Route 17 Auto Mall", ext_acct(), memo="VEHICLE PURCHASE")
        elif r < 0.16:  # bonus / inheritance / legal settlement that stays put
            add(c, d, rng.choice(["ACH_IN", "WIRE_IN"]), rng.uniform(25000, 110000),
                rng.choice(["Hartwell & Lowe Estate Attorneys", "Annual Bonus - Employer", "Class Action Settlement Admin"]), ext_acct(), memo="DISTRIBUTION")
        elif r < 0.19:  # private car sale paid in cash, deposited over two trips
            add(c, d, "CASH_DEPOSIT", float(round(rng.uniform(8500, 9900), -2)), memo="")
            add(c, d + int(rng.integers(1, 4)), "CASH_DEPOSIT", float(round(rng.uniform(5000, 9800), -2)), memo="")
        elif r < 0.21:  # family pays down a debt in round wires
            for k in range(2):
                add(c, d + k * 3, "WIRE_OUT", float(rng.choice([10000, 15000, 20000])), "Keystone Student Loan Servicing", ext_acct(), memo="LOAN PAYOFF")


# ------------------------------------------------------------------- KYC profile
def risk_rating(c):
    s = 0
    s += {"cash_business": 3, "import_export": 3, "property_mgmt": 1, "crypto_investor": 1}.get(c["_segment"], 0)
    s += 2 if c["nationality"] in FATF_GREY else 0
    s += 3 if c["pep_flag"] else 0
    s += 1 if c["expected_international"] else 0
    s += 1 if c["customer_type"] == "Business" else 0
    return "High" if s >= 4 else "Medium" if s >= 2 else "Low"


def build():
    n_total = 500
    plan = ([("structuring", "salaried")] * 3 + [("structuring", "gig")] * 2 + [("structuring", "cash_business")] * 1
            + [("structuring_smart", "salaried")] * 2
            + [("rapid_movement", s) for s in ["salaried", "salaried", "professional", "low_activity", "gig", "student", "salaried"]]
            + [("funnel", s) for s in ["salaried", "gig", "student", "salaried", "gig", "low_activity"]]
            + [("high_risk_geo", s) for s in ["salaried", "salaried", "gig", "student", "professional", "salaried", "retiree"]]
            + [("round_dollar", s) for s in ["professional", "professional", "salaried", "salaried", "gig", "professional"]]
            + [("dormant_reactivation", s) for s in ["low_activity", "low_activity", "retiree", "retiree", "low_activity", "salaried"]]
            + [("tbml", "import_export")] * 6
            + [("mule", "student")] * 4 + [("mule", "gig")] * 3 + [("mule", "low_activity")] * 1
            + [("mule_collector", "gig")] * 2)
    segs = list(rng.choice(list(WEIGHTS), size=n_total - len(plan), p=list(WEIGHTS.values())))
    assignments = [(None, s) for s in segs] + plan
    order = rng.permutation(len(assignments))
    customers = []
    for idx, j in enumerate(order, start=1):
        typ, seg = assignments[j]
        c = make_customer(idx, seg)
        if typ:
            c["_typology"] = "structuring" if typ.startswith("structuring") else ("mule_network" if typ.startswith("mule") else typ)
            c["_role"] = {"structuring_smart": "structurer (sub-$8K deposits)", "mule": "money mule", "mule_collector": "collector / herder"}.get(typ, "subject")
            c["_typ_raw"] = typ
            c.pop("_lump", None)
            c["_blocked"] = []
            if typ == "dormant_reactivation":
                c["_active_from"] = int(rng.integers(115, 150))
                c["last_txn_before_2026"] = (pd.Timestamp("2025-06-01") + pd.Timedelta(days=int(rng.integers(0, 120)))).date()
                c["account_open_date"] = (pd.Timestamp("2012-01-01") + pd.Timedelta(days=int(rng.integers(0, 2500)))).date()
            if typ.startswith("mule"):
                op = pd.Timestamp("2025-10-01") + pd.Timedelta(days=int(rng.integers(0, 130)))
                c["account_open_date"] = op.date()
                c["age"] = int(rng.integers(19, 27)) if typ == "mule" else int(rng.integers(26, 40))
                if c["occupation"] == "Retired":
                    c["occupation"] = "Unemployed"
                c["_active_from"] = max(0, (op - START).days)
                c["last_txn_before_2026"] = (op + pd.Timedelta(days=3)).date() if op < START else None
            if typ == "tbml":
                c["expected_goods"] = rng.choice(["used clothing", "furniture", "food products", "textiles"])
                c["occupation"] = f"Import/Export - {c['expected_goods'].title()}"
                c["_suppliers"] = TRADE_GOODS[c["expected_goods"]]
                c.pop("_fixed_order", None)
        customers.append(c)

    # a few households share one device (legitimate) -> noise for the shared-device rule
    normals = [c for c in customers if c["_typology"] == "none" and c["customer_type"] == "Individual"]
    for k in range(0, 24, 2):
        normals[k + 1]["device_id"] = normals[k]["device_id"]
    for k in (30, 31, 32):  # one legit family of three on one tablet
        normals[k]["device_id"] = normals[30]["device_id"]
    mules = [c for c in customers if c.get("_typ_raw", "").startswith("mule")]
    for i, m in enumerate(mules):  # the herder runs several mule accounts from the same phones
        m["device_id"] = MULE_DEVICES[i % 3]
    seen = set()
    for c in customers:  # first-listed actor of most typologies is a "low-intensity" variant
        t = c.get("_typ_raw")
        if t and t not in seen and t not in ("structuring_smart", "mule", "mule_collector"):
            c["_intensity"] = 0.2
            seen.add(t)

    for c in customers:
        start_len = len(TX)
        SEGMENT_FN[c["_segment"]](c)
        base = [t for t in TX[start_len:]]
        active_months = max(1, len({(t["timestamp"].month) for t in base}))
        vol = sum(t["amount"] for t in base) / active_months
        cnt = len(base) / active_months
        c["expected_monthly_volume_usd"] = float(max(1000, round(vol * rng.uniform(0.9, 1.5), -2)))
        c["expected_monthly_txn_count"] = int(max(3, round(cnt * rng.uniform(0.9, 1.3))))
        intl = sorted({t["counterparty_country"] for t in base if t["counterparty_country"] != "United States"})
        c["expected_countries"] = ";".join(intl)
        c["expected_international"] = bool(intl)
        c["expected_cash_activity"] = "High" if c["_segment"] == "cash_business" else ("Medium" if c.get("_travel") else "Low")

    by_typ = {}
    for c in customers:
        by_typ.setdefault(c.get("_typ_raw"), []).append(c)
    for c in by_typ.get("structuring", []):
        ty_structuring(c)
    for c in by_typ.get("structuring_smart", []):
        ty_structuring(c, smart=True)
    for name, fn in [("rapid_movement", ty_rapid), ("funnel", ty_funnel), ("high_risk_geo", ty_high_risk_geo),
                     ("round_dollar", ty_round_dollar), ("dormant_reactivation", ty_dormant), ("tbml", ty_tbml)]:
        for c in by_typ.get(name, []):
            fn(c)
    ty_mule_network(by_typ["mule"], by_typ["mule_collector"])
    life_events([c for c in customers if c["_typology"] == "none"])

    for c in customers:
        c["kyc_risk_rating"] = risk_rating(c)

    tx = pd.DataFrame(TX).sort_values(["timestamp", "customer_id"]).reset_index(drop=True)
    tx.insert(0, "txn_id", [f"T{i:06d}" for i in range(1, len(tx) + 1)])
    gt_tx = tx.loc[tx._tag.notna(), ["txn_id", "customer_id", "_tag"]].rename(columns={"_tag": "typology"})
    tx = tx.drop(columns="_tag")

    cust_cols = ["customer_id", "account_no", "name", "customer_type", "occupation", "beneficial_owner", "age",
                 "nationality", "home_state", "home_branch", "account_open_date", "last_txn_before_2026",
                 "expected_monthly_volume_usd", "expected_monthly_txn_count", "expected_cash_activity",
                 "expected_international", "expected_countries", "expected_goods", "pep_flag",
                 "kyc_risk_rating", "device_id"]
    cust = pd.DataFrame(customers)
    gt_c = cust[["customer_id", "_typology", "_role"]].rename(columns={"_typology": "typology", "_role": "role"})
    gt_c["is_suspicious"] = gt_c.typology != "none"

    DATA.mkdir(exist_ok=True)
    cust[cust_cols].to_csv(DATA / "customers.csv", index=False)
    tx.to_csv(DATA / "transactions.csv", index=False)
    BRANCHES.to_csv(DATA / "branches.csv", index=False)
    gt_c.to_csv(DATA / "ground_truth_customers.csv", index=False)
    gt_tx.to_csv(DATA / "ground_truth_transactions.csv", index=False)
    print(f"customers: {len(cust)}  transactions: {len(tx):,}  suspicious customers: {int(gt_c.is_suspicious.sum())}")
    print(gt_c[gt_c.is_suspicious].typology.value_counts().to_string())


if __name__ == "__main__":
    build()
