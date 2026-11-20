"""
Generate synthetic Microsoft Entra ID sign-in logs and Microsoft 365 mailbox
audit logs for a fictional company (Contoso Freight, contosofreight.com).

Planted inside 14 days of normal activity is one attack chain:
  1. Low-and-slow password spray from rented VPS IPs (T1110.003)
  2. Three accounts fall; attacker signs in as a finance user (T1078.004)
  3. Attacker adds an inbox rule hiding replies about invoices (T1564.008)
  4. Attacker reads the mailbox (T1114.002) and sends a fake
     "updated bank details" email to a customer (business email compromise)

Every name, IP and domain here is fictional (IPs come from reserved ranges). Output: data/SigninLogs.csv,
data/OfficeActivity.csv and data/ground_truth.json (answer key).
"""
import csv, json, random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(7)
OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)

START = datetime(2026, 11, 2, 0, 0, 0)
DAYS = 14
DOMAIN = "contosofreight.com"

FIRST = ["ana", "ben", "carla", "dev", "eli", "fatima", "gus", "hana", "ivan", "jade",
         "kofi", "lena", "marco", "nadia", "omar", "priya", "quinn", "rosa", "sam", "tariq",
         "uma", "victor", "wen", "xavier", "yara", "zane"]
LAST = ["alvarez", "brooks", "chen", "diaz", "evans", "flores", "garcia", "haddad", "ito",
        "jones", "kim", "lopez", "moreno", "nguyen", "okafor", "patel", "reyes", "smith"]
users = sorted({f"{random.choice(FIRST)}.{random.choice(LAST)}@{DOMAIN}" for _ in range(400)})[:300]
DEPTS = ["Finance", "Operations", "Sales", "IT", "HR", "Dispatch"]
dept = {u: random.choice(DEPTS) for u in users}
VICTIM = "marco.reyes@" + DOMAIN          # finance user the attacker uses for BEC
if VICTIM not in users:
    users[0] = VICTIM
dept[VICTIM] = "Finance"

# Each user has a home office IP block and a usual city
OFFICES = [("Los Angeles", "US", "203.0.113."), ("Long Beach", "US", "198.51.100."),
           ("Phoenix", "US", "192.0.2.")]
home = {u: random.choice(OFFICES) for u in users}
APPS = ["Office 365 Exchange Online", "Microsoft Teams", "SharePoint Online", "Microsoft Outlook"]
BROWSERS = ["Edge 130", "Chrome 131", "Outlook 16.0"]

signins, office = [], []

def sid(prefix):
    return f"{prefix}-{random.getrandbits(48):012x}"

def signin(t, user, ip, city, country, result, app="Office 365 Exchange Online",
           ua="Edge 130", mfa="satisfied", client="Browser"):
    signins.append({
        "TimeGenerated": t.isoformat() + "Z", "UserPrincipalName": user,
        "IPAddress": ip, "City": city, "Country": country,
        "ResultType": result,  # 0 = success, 50126 = bad password, 50053 = locked, 50074 = MFA required
        "ResultDescription": {0: "Success", 50126: "Invalid username or password",
                              50053: "Account locked", 50074: "Strong authentication required"}[result],
        "AppDisplayName": app, "UserAgent": ua, "ClientAppUsed": client,
        "AuthenticationRequirement": "multiFactorAuthentication" if mfa == "satisfied" else "singleFactorAuthentication",
        "CorrelationId": sid("corr"),
    })

def op(t, user, operation, ip, details=""):
    office.append({"TimeGenerated": t.isoformat() + "Z", "UserId": user, "Operation": operation,
                   "ClientIP": ip, "Details": details})

# ---------- normal activity ----------
for d in range(DAYS):
    day = START + timedelta(days=d)
    if day.weekday() >= 5:
        active = random.sample(users, 25)       # light weekend use
    else:
        active = users
    for u in active:
        city, country, block = home[u]
        ip = block + str(10 + users.index(u) % 200)
        for _ in range(random.randint(1, 4)):
            t = day + timedelta(hours=random.uniform(7, 18.5))
            if random.random() < 0.03:           # ordinary typo
                signin(t - timedelta(seconds=40), u, ip, city, country, 50126, ua=random.choice(BROWSERS))
            signin(t, u, ip, city, country, 0, app=random.choice(APPS), ua=random.choice(BROWSERS))
            if random.random() < 0.5:
                op(t + timedelta(minutes=random.randint(1, 50)), u, "MailItemsAccessed", ip,
                   f"items={random.randint(1, 25)}")
            if random.random() < 0.15:
                op(t + timedelta(minutes=random.randint(1, 50)), u, "Send", ip,
                   f"to=internal recipients={random.randint(1, 4)}")
        if random.random() < 0.002:              # rare legitimate inbox rule
            op(day + timedelta(hours=10), u, "New-InboxRule", ip,
               "Name='Newsletters' From='news@vendor-updates.example' MoveToFolder='Newsletters'")

# A few real travellers so "new country" alone is not proof of compromise
for u, city, country, ip in [(users[5], "London", "GB", "198.19.20.5"),
                             (users[40], "Toronto", "CA", "198.19.31.8"),
                             (users[77], "Mexico City", "MX", "198.19.52.9")]:
    for d in (8, 9):
        signin(START + timedelta(days=d, hours=9), u, ip, city, country, 0, ua="Outlook 16.0", client="Mobile Apps and Desktop clients")

# ---------- attack ----------
SPRAY_IPS = [("198.18.44.%d" % i, "Amsterdam", "NL") for i in (11, 12, 13)] + \
            [("198.18.91.%d" % i, "Frankfurt", "DE") for i in (40, 41)]
SPRAY_PW_ROUNDS = 3                              # 3 passwords, each tried once per user
spray_start = START + timedelta(days=9, hours=1)   # Wed Nov 11, ~01:00 UTC
compromised = [VICTIM, users[120], users[201]]
t = spray_start
for rnd in range(SPRAY_PW_ROUNDS):
    targets = users[:]
    random.shuffle(targets)
    for u in targets:
        ip, city, country = random.choice(SPRAY_IPS)
        t += timedelta(seconds=random.uniform(4, 11))   # slow: ~1 try / 7s, spread over IPs
        ok = (rnd == 2 and u in compromised)
        signin(t, u, ip, city, country, 0 if ok else 50126,
               app="Office 365 Exchange Online", ua="python-requests/2.31",
               mfa="none", client="Exchange ActiveSync" if ok else "Other clients")
    t += timedelta(hours=2)                      # pause between rounds to dodge lockout

spray_end = t
# MFA blocks two of the three when the attacker tries the browser
for u in compromised[1:]:
    ip, city, country = SPRAY_IPS[0]
    signin(spray_end + timedelta(minutes=15), u, ip, city, country, 50074, mfa="none", ua="Chrome 131")

# Victim's legacy ActiveSync client had no MFA -> attacker gets in
atk_ip, atk_city, atk_country = "198.18.44.12", "Amsterdam", "NL"
t0 = spray_end + timedelta(minutes=40)
signin(t0, VICTIM, atk_ip, atk_city, atk_country, 0, ua="python-requests/2.31",
       mfa="none", client="Exchange ActiveSync")
op(t0 + timedelta(minutes=3), VICTIM, "MailItemsAccessed", atk_ip, "items=1840 (bulk sync)")
op(t0 + timedelta(minutes=9), VICTIM, "New-InboxRule", atk_ip,
   "Name='.' SubjectOrBodyContainsWords='invoice;payment;wire;bank' MoveToFolder='RSS Feeds' MarkAsRead=True")
op(t0 + timedelta(minutes=31), VICTIM, "Send", atk_ip,
   "to=ap@harborlogistics.example subject='Updated remittance details - Contoso Freight' recipients=1")
op(t0 + timedelta(hours=5), VICTIM, "Send", atk_ip,
   "to=billing@pacifictrade.example subject='Updated remittance details - Contoso Freight' recipients=1")

signins.sort(key=lambda r: r["TimeGenerated"])
office.sort(key=lambda r: r["TimeGenerated"])
for name, rows in (("SigninLogs.csv", signins), ("OfficeActivity.csv", office)):
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

json.dump({
    "spray_ips": [s[0] for s in SPRAY_IPS],
    "spray_window_utc": [spray_start.isoformat() + "Z", spray_end.isoformat() + "Z"],
    "compromised_accounts": compromised,
    "bec_account": VICTIM,
    "attacker_ip": atk_ip,
    "external_recipients": ["ap@harborlogistics.example", "billing@pacifictrade.example"],
}, open(OUT / "ground_truth.json", "w"), indent=2)

print(f"users={len(users)} signins={len(signins)} office_events={len(office)}")
