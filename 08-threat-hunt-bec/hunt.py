"""
Run the five KQL hunts in kql/ as pandas code against the CSV logs, so the
project works without a Microsoft Sentinel workspace. Each function mirrors
one .kql file line for line. Results go to findings/ and are scored against
data/ground_truth.json.
"""
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
DATA, OUT = HERE / "data", HERE / "findings"
OUT.mkdir(exist_ok=True)

signins = pd.read_csv(DATA / "SigninLogs.csv")
office = pd.read_csv(DATA / "OfficeActivity.csv")
for df in (signins, office):
    df["TimeGenerated"] = pd.to_datetime(df.TimeGenerated, format="ISO8601")
truth = json.load(open(DATA / "ground_truth.json"))


def hunt1_password_spray(min_accounts=20):
    """T1110.003: one IP failing against many accounts."""
    f = signins[signins.ResultType == 50126]
    g = f.groupby(["IPAddress", "Country"]).agg(
        FailedAccounts=("UserPrincipalName", "nunique"),
        Attempts=("UserPrincipalName", "size"),
        FirstSeen=("TimeGenerated", "min"),
        LastSeen=("TimeGenerated", "max"),
        UserAgents=("UserAgent", lambda s: sorted(set(s)))).reset_index()
    g = g[g.FailedAccounts >= min_accounts].copy()
    g["AttemptsPerAccount"] = (g.Attempts / g.FailedAccounts).round(1)
    return g.sort_values("FailedAccounts", ascending=False)


def hunt2_spray_success(spray_ips):
    """T1078.004: did any spraying IP get a correct password?"""
    h = signins[signins.IPAddress.isin(spray_ips) & signins.ResultType.isin([0, 50074])]
    return h[["TimeGenerated", "UserPrincipalName", "IPAddress", "Country", "ResultType",
              "ClientAppUsed", "AuthenticationRequirement", "UserAgent"]].sort_values("TimeGenerated")


def hunt3_legacy_auth():
    """Successful single-factor sign-ins over protocols that cannot do MFA."""
    legacy = ["Exchange ActiveSync", "IMAP4", "POP3", "Other clients"]
    h = signins[(signins.ResultType == 0) & signins.ClientAppUsed.isin(legacy)
                & (signins.AuthenticationRequirement == "singleFactorAuthentication")]
    return h[["TimeGenerated", "UserPrincipalName", "IPAddress", "Country", "ClientAppUsed", "UserAgent"]]


def hunt4_inbox_rules():
    """T1564.008: inbox rules that hide money-related mail."""
    r = office[office.Operation.isin(["New-InboxRule", "Set-InboxRule", "UpdateInboxRules"])]
    words = r.Details.str.contains("invoice|payment|wire|bank|remittance", case=False)
    folders = r.Details.str.contains("RSS Feeds|Conversation History|Archive", case=False)
    blank = r.Details.str.contains(r"Name='.{0,2}'", regex=True)
    return r[words | folders | blank][["TimeGenerated", "UserId", "ClientIP", "Details"]]


def hunt5_bec_chain(window_hours=6):
    """T1114.002 + BEC: foreign sign-in followed by mailbox actions from the same IP."""
    s = signins[(signins.ResultType == 0) & (signins.Country != "US")][
        ["TimeGenerated", "UserPrincipalName", "IPAddress", "Country", "ClientAppUsed"]
    ].rename(columns={"TimeGenerated": "SigninTime", "UserPrincipalName": "User"})
    a = office[office.Operation.isin(["MailItemsAccessed", "New-InboxRule", "Send"])].rename(
        columns={"TimeGenerated": "ActTime", "UserId": "User"})
    j = s.merge(a, on="User")
    j = j[(j.ClientIP == j.IPAddress) & (j.ActTime >= j.SigninTime)
          & (j.ActTime <= j.SigninTime + pd.Timedelta(hours=window_hours))]
    j["Action"] = j.ActTime.dt.strftime("%H:%M") + " " + j.Operation + " " + j.Details
    out = j.groupby(["User", "IPAddress", "Country", "SigninTime"]).Action.apply(list).reset_index()
    return out[out.Action.str.len() >= 2]


if __name__ == "__main__":
    h1 = hunt1_password_spray()
    h2 = hunt2_spray_success(h1.IPAddress.tolist())
    h3 = hunt3_legacy_auth()
    h4 = hunt4_inbox_rules()
    h5 = hunt5_bec_chain()
    for name, df in [("01_password_spray", h1), ("02_spray_success", h2), ("03_legacy_auth", h3),
                     ("04_inbox_rules", h4), ("05_bec_chain", h5)]:
        df.to_csv(OUT / f"{name}.csv", index=False)
        print(f"\n=== {name}: {len(df)} rows ===")
        print(df.to_string(index=False, max_colwidth=90))

    # Score against the answer key
    found_ips = set(h1.IPAddress)
    pw_correct = set(h2.UserPrincipalName)
    bec = set(h5.User)
    print("\n=== Score vs ground truth ===")
    print(f"Spray IPs found: {len(found_ips & set(truth['spray_ips']))}/{len(truth['spray_ips'])}"
          f" (false positives: {len(found_ips - set(truth['spray_ips']))})")
    print(f"Accounts with password guessed: {len(pw_correct & set(truth['compromised_accounts']))}/"
          f"{len(truth['compromised_accounts'])}")
    print(f"BEC account identified: {truth['bec_account'] in bec}"
          f" (false positives: {len(bec - {truth['bec_account']})})")
    print(f"Legitimate travellers wrongly flagged in hunt 5: {len(bec - {truth['bec_account']})}")
