# streamlit_app.py  –  Kensite Hire Dashboard (v2)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, timedelta
import os

# ---------- PAGE CONFIG / THEME ----------
st.set_page_config(
    page_title="Kensite Hire Dashboard",
    layout="wide"
)

import base64

# Embed the Kensite logo as base64
_LOGO_PATH = os.path.join(os.path.dirname(__file__), "kensite_logo.png")
def _get_logo_b64():
    if os.path.exists(_LOGO_PATH):
        with open(_LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

_LOGO_B64 = _get_logo_b64()

st.markdown("""
<style>
/* ── Google Font: Figtree (brand typeface) ── */
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700;800&display=swap');

/* ── Base app ── */
.stApp {
    background-color: #f5f5f5;
    color: #40424a;
    font-family: 'Figtree', system-ui, sans-serif;
}

/* ── Hide Streamlit's default top bar ── */
[data-testid="stHeader"] {
    display: none;
}

/* ── Main content padding ── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem;
    max-width: 97%;
}

/* ── Sidebar ── */
div[data-testid="stSidebar"] {
    background-color: #40424a;
    border-right: 3px solid #0d823b;
}
div[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-family: 'Figtree', system-ui, sans-serif;
}
div[data-testid="stSidebar"] .stSelectbox label,
div[data-testid="stSidebar"] .stMultiSelect label,
div[data-testid="stSidebar"] .stTextInput label,
div[data-testid="stSidebar"] .stSlider label,
div[data-testid="stSidebar"] .stDateInput label,
div[data-testid="stSidebar"] .stCheckbox label {
    color: #dadada !important;
    font-size: 0.82rem;
    font-weight: 500;
}
div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    border-bottom: 1px solid #0d823b;
    padding-bottom: 4px;
}

/* ── Headings ── */
h1, h2, h3, h4 {
    color: #40424a;
    font-family: 'Figtree', system-ui, sans-serif;
    font-weight: 700;
}

/* ── Brand header bar ── */
.kensite-header {
    background: #40424a;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
    border-bottom: 4px solid #0d823b;
}
.kensite-header img {
    height: 40px;
    width: auto;
}
.kensite-header .header-title {
    color: #ffffff;
    font-size: 1.3rem;
    font-weight: 700;
    font-family: 'Figtree', system-ui, sans-serif;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}
.kensite-header .header-sub {
    color: #0d823b;
    font-size: 0.75rem;
    font-weight: 500;
    font-family: 'Figtree', system-ui, sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── KPI cards ── */
.kpi-card {
    background: #ffffff;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #0d823b;
    border-top: 1px solid #dadada;
    border-right: 1px solid #dadada;
    border-bottom: 1px solid #dadada;
}
.kpi-card .kpi-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #40424a;
    font-family: 'Figtree', system-ui, sans-serif;
}
.kpi-card .kpi-label {
    font-size: 0.78rem;
    color: #888;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: 'Figtree', system-ui, sans-serif;
}

/* ── Small labels ── */
.small-label {
    font-size: 0.8rem;
    color: #888;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-bottom: 2px solid #0d823b;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    color: #40424a;
    font-family: 'Figtree', system-ui, sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 10px 18px;
    border-radius: 0;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: #0d823b !important;
    color: #ffffff !important;
    border-radius: 0 !important;
}

/* ── Hire lines table ── */
.highlight-red  { background-color: rgba(210, 40,  40,  0.12); }
.highlight-amber{ background-color: rgba(210, 140, 0,   0.15); }
.highlight-purple{ background-color: rgba(110, 40,  160, 0.12); }
.highlight-grey { background-color: rgba(130, 130, 130, 0.10); }
.highlight-dupe { background-color: rgba(220, 90,  0,   0.15); }

.styled-table {
    font-family: 'Figtree', system-ui, sans-serif;
    font-size: 0.8rem;
}
.styled-table thead th {
    position: sticky;
    top: 0;
    background-color: #40424a !important;
    color: #ffffff !important;
    z-index: 10;
    padding: 8px 10px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
}
.styled-table tbody td {
    padding: 6px 10px;
    color: #40424a;
    border-bottom: 1px solid #e8e8e8;
}

/* ── Section dividers ── */
.section-header {
    border-left: 4px solid #0d823b;
    padding-left: 10px;
    margin: 18px 0 10px 0;
    color: #40424a;
    font-weight: 700;
    font-family: 'Figtree', system-ui, sans-serif;
}

/* ── Upload boxes ── */
.upload-zone {
    background: #ffffff;
    border: 2px dashed #0d823b;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.upload-zone label {
    font-weight: 600;
    color: #40424a;
    font-family: 'Figtree', system-ui, sans-serif;
}

/* ── Buttons ── */
.stDownloadButton > button {
    background-color: #0d823b !important;
    color: #ffffff !important;
    border: none !important;
    font-family: 'Figtree', system-ui, sans-serif !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
}
.stDownloadButton > button:hover {
    background-color: #0a6830 !important;
}

/* ── Dataframes ── */
.stDataFrame {
    border: 1px solid #dadada !important;
    border-radius: 6px;
}

/* ── Alerts / info boxes ── */
.stAlert {
    border-radius: 6px;
    font-family: 'Figtree', system-ui, sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ── Brand header ──
if _LOGO_B64:
    logo_html = f'<img src="data:image/png;base64,{_LOGO_B64}" alt="Kensite Logo">'
else:
    logo_html = '<span style="color:#0d823b;font-size:1.6rem;font-weight:800;">K</span>'

st.markdown(f"""
<div class="kensite-header">
    {logo_html}
    <div>
        <div class="header-title">Hire Dashboard</div>
        <div class="header-sub">Complete Site Solutions</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- COMMON HELPERS ----------
def money(x):
    if pd.isna(x):
        return ""
    return f"£{x:,.2f}"


# ---------- HIRE EXPORT LOADING / CLEANING ----------
def load_hire_file(upload) -> pd.DataFrame:
    df = pd.read_excel(upload)

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"[^0-9a-zA-Z]+", "_", regex=True)
        .str.lower()
    )

    col_map = {
        "custname": "customer",
        "sname": "site_name",
        "saddr1": "site_addr1",
        "scity": "site_city",
        "job_number": "job_number",
        "po_number": "po_number",
        "item_or_regnum": "unit_number",
        "descr": "description",
        "sortgroup": "subgroup_code",
        "sortgroup_desc": "subgroup_desc",
        "orig_start_rent": "start_date",
        "projectedreturn": "projected_return",
        "weekchg": "weekly_charge",
        "qty_out": "qty_out",
        "phonenum": "phone",
        "dticket": "ticket_ref",
        "print_time": "report_generated_at",
    }

    for raw_col, nice_col in col_map.items():
        if raw_col in df.columns:
            df[nice_col] = df[raw_col]
        else:
            df[nice_col] = np.nan

    for dcol in ["start_date", "projected_return", "report_generated_at"]:
        if dcol in df.columns:
            df[dcol] = pd.to_datetime(df[dcol], errors="coerce")

    if "weekly_charge" in df.columns:
        df["weekly_charge"] = pd.to_numeric(df["weekly_charge"], errors="coerce")

    text_cols = [
        "customer","site_name","site_addr1","site_city","job_number","po_number",
        "unit_number","description","subgroup_code","subgroup_desc","phone"
    ]
    for c in text_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

    return df


# ---------- UTILISATION / FLEET LOADING ----------
def load_fleet_file(upload) -> pd.DataFrame:
    df = pd.read_excel(upload)

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"[^0-9a-zA-Z]+", "_", regex=True)
        .str.lower()
    )

    col_guess_map = {
        "subgroup": "subgroup_code",
        "sub_group": "subgroup_code",
        "subgroup_code": "subgroup_code",
        "subgroup_description": "subgroup_desc",
        "subgroup_desc": "subgroup_desc",
        "sub_group_description": "subgroup_desc",
        "itemised_status": "asset_status",
        "status": "asset_status",
        "item_code": "asset_id",
        "unit_number": "asset_id",
        "unit_no": "asset_id",
        "unit": "asset_id",
        "unitnumber": "asset_id",
        "unitcode": "asset_id",
    }

    for raw_col, nice_col in col_guess_map.items():
        if raw_col in df.columns:
            df[nice_col] = df[raw_col]

    for c in ["subgroup_code","subgroup_desc","asset_status","asset_id"]:
        if c not in df.columns:
            df[c] = np.nan
        df[c] = df[c].astype(str).str.strip()

    return df


def current_utilisation_table(fleet_df: pd.DataFrame) -> pd.DataFrame:
    fleet_df["asset_status_norm"] = fleet_df["asset_status"].str.upper().str.strip()

    total_counts = (
        fleet_df
        .groupby(["subgroup_code","subgroup_desc"], dropna=False)
        .agg(total_units=("asset_id","count"))
        .reset_index()
    )

    on_hire_counts = (
        fleet_df[fleet_df["asset_status_norm"]=="ON HIRE"]
        .groupby(["subgroup_code","subgroup_desc"], dropna=False)
        .agg(on_hire_units=("asset_id","count"))
        .reset_index()
    )

    avail_counts = (
        fleet_df[fleet_df["asset_status_norm"]=="AVAILABLE"]
        .groupby(["subgroup_code","subgroup_desc"], dropna=False)
        .agg(available_units=("asset_id","count"))
        .reset_index()
    )

    util = total_counts.merge(on_hire_counts, on=["subgroup_code","subgroup_desc"], how="left")
    util = util.merge(avail_counts, on=["subgroup_code","subgroup_desc"], how="left")

    util["on_hire_units"]   = util["on_hire_units"].fillna(0).astype(int)
    util["available_units"] = util["available_units"].fillna(0).astype(int)
    util["total_units"]     = util["total_units"].fillna(0).astype(int)

    util["utilisation_pct"] = np.where(
        util["total_units"] > 0,
        (util["on_hire_units"] / util["total_units"]) * 100,
        0.0
    ).round(1)

    util = util.sort_values("utilisation_pct", ascending=False)

    util_display = util.rename(columns={
        "subgroup_code": "Subgroup",
        "subgroup_desc": "Subgroup Desc",
        "total_units": "Total Units",
        "on_hire_units": "On Hire",
        "available_units": "Available",
        "utilisation_pct": "Utilisation %",
    })

    return util_display


# ---------- UTILISATION HISTORY SNAPSHOTS ----------
HISTORY_FILE = "utilisation_history.csv"

def append_snapshot_to_history(util_table: pd.DataFrame):
    """
    Append today's utilisation snapshot to history CSV.
    Deduplicates so each (date, subgroup) only appears once.
    """
    snap_date = pd.Timestamp.today().strftime("%Y-%m-%d")

    hist_chunk = util_table[["Subgroup","Utilisation %"]].copy()
    hist_chunk["snapshot_date"] = snap_date
    hist_chunk = hist_chunk[["snapshot_date","Subgroup","Utilisation %"]]

    if os.path.exists(HISTORY_FILE):
        old = pd.read_csv(HISTORY_FILE)
        # Remove any existing rows for today to avoid duplicates on re-upload
        old = old[old["snapshot_date"] != snap_date]
        combined = pd.concat([old, hist_chunk], ignore_index=True)
    else:
        combined = hist_chunk

    combined.to_csv(HISTORY_FILE, index=False)


def load_history():
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce")
        # Deduplicate fully — keep last occurrence per date+subgroup
        df = df.drop_duplicates(subset=["snapshot_date","Subgroup"], keep="last")
        return df
    else:
        return pd.DataFrame(columns=["snapshot_date","Subgroup","Utilisation %"])


def utilisation_trend_for_subgroup(history_df, subgroup_code):
    sub = history_df[history_df["Subgroup"] == subgroup_code].copy()
    sub = sub.sort_values("snapshot_date")
    return sub


# ---------- REVENUE HISTORY SNAPSHOTS ----------
REVENUE_HISTORY_FILE = "revenue_history.csv"

def append_revenue_snapshot(total_weekly: float):
    """Save today's total weekly hire value to revenue_history.csv."""
    snap_date = pd.Timestamp.today().strftime("%Y-%m-%d")
    new_row = pd.DataFrame([{"snapshot_date": snap_date, "total_weekly": total_weekly}])

    if os.path.exists(REVENUE_HISTORY_FILE):
        old = pd.read_csv(REVENUE_HISTORY_FILE)
        old = old[old["snapshot_date"] != snap_date]   # replace today if re-uploaded
        combined = pd.concat([old, new_row], ignore_index=True)
    else:
        combined = new_row

    combined.to_csv(REVENUE_HISTORY_FILE, index=False)


def load_revenue_history():
    if os.path.exists(REVENUE_HISTORY_FILE):
        df = pd.read_csv(REVENUE_HISTORY_FILE)
        df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce")
        df = df.drop_duplicates(subset=["snapshot_date"], keep="last")
        df = df.sort_values("snapshot_date")
        return df
    else:
        return pd.DataFrame(columns=["snapshot_date","total_weekly"])


# ---------- DUPLICATE UNIT DETECTION ----------
def find_duplicate_units(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows where the same unit_number appears on more than one active hire line."""
    unit_col = "unit_number"
    if unit_col not in df.columns:
        return pd.DataFrame()

    # Exclude blanks / nan
    valid = df[~df[unit_col].isin(["", "nan", "NaN"])].copy()
    counts = valid.groupby(unit_col)[unit_col].transform("count")
    dupes = valid[counts > 1].copy()

    if dupes.empty:
        return pd.DataFrame()

    display_cols = [
        "unit_number","customer","site_name","description",
        "subgroup_desc","weekly_charge","start_date","projected_return","job_number","po_number"
    ]
    display_cols = [c for c in display_cols if c in dupes.columns]
    result = dupes[display_cols].copy()

    if "weekly_charge" in result.columns:
        result["weekly_charge"] = result["weekly_charge"].apply(money)
    for dcol in ["start_date","projected_return"]:
        if dcol in result.columns:
            result[dcol] = result[dcol].dt.strftime("%d/%m/%Y")

    result = result.rename(columns={
        "unit_number": "Unit #",
        "customer": "Customer",
        "site_name": "Site",
        "description": "Description",
        "subgroup_desc": "Subgroup",
        "weekly_charge": "Weekly £",
        "start_date": "Start",
        "projected_return": "Projected Return",
        "job_number": "Job #",
        "po_number": "PO",
    })

    return result.sort_values("Unit #")


# ---------- WATCHLIST BUILDER ----------
def build_watchlists(df):
    today = pd.Timestamp.today().normalize()

    def nice_subset(mask, label):
        sub = df.loc[mask, [
            "customer","site_name","phone","unit_number","description",
            "subgroup_desc","weekly_charge","start_date","projected_return"
        ]].copy()

        sub["weekly_charge"]     = sub["weekly_charge"].apply(money)
        sub["start_date"]        = sub["start_date"].dt.strftime("%d/%m/%Y")
        sub["projected_return"]  = sub["projected_return"].dt.strftime("%d/%m/%Y")

        sub = sub.rename(columns={
            "customer": "Customer",
            "site_name": "Site",
            "phone": "Phone",
            "unit_number": "Unit #",
            "description": "Description",
            "subgroup_desc": "Subgroup",
            "weekly_charge": "Weekly £",
            "start_date": "Start",
            "projected_return": "Projected Return",
        })

        return label, sub

    overdue = (
        df["projected_return"].notna() &
        (df["projected_return"].dt.normalize() < today)
    )
    due_soon = (
        df["projected_return"].notna() &
        ((df["projected_return"].dt.normalize()-today).dt.days.between(0,7))
    )
    long_running = (
        df["start_date"].notna() &
        ((today - df["start_date"].dt.normalize()).dt.days > 120)
    )
    missing_po = (
        (df["po_number"].astype(str).str.strip().isin(["","nan"])) &
        ((df["weekly_charge"].fillna(0)) > 0)
    )

    lists = [
        nice_subset(overdue,      "🔴 Overdue Off-Hire (Projected Return < Today)"),
        nice_subset(due_soon,     "🟡 Due Off-Hire Within 7 Days"),
        nice_subset(long_running, "⏳ 120+ Days On Hire"),
        nice_subset(missing_po,   "🟣 Missing PO But Billing"),
    ]
    return lists


# ---------- SUBGROUP ROLLUP ----------
def subgroup_rollup(df):
    grp = df.groupby(
        ["subgroup_code","subgroup_desc"],
        dropna=False,
        as_index=False
    ).agg(
        units_on_hire=("unit_number","count"),
        total_weekly=("weekly_charge","sum"),
        avg_weekly=("weekly_charge","mean"),
        earliest_start=("start_date","min"),
        pct_no_po=("po_number", lambda x: (x.isna() | (x.astype(str).str.strip()=="")).mean()*100),
        pct_with_proj_return=("projected_return", lambda x: x.notna().mean()*100),
    )

    grp["earliest_start"]         = pd.to_datetime(grp["earliest_start"], errors="coerce").dt.strftime("%d/%m/%Y")
    grp["total_weekly"]           = grp["total_weekly"].apply(money)
    grp["avg_weekly"]             = grp["avg_weekly"].apply(money)
    grp["pct_no_po"]              = grp["pct_no_po"].round(1).astype(str) + "%"
    grp["pct_with_proj_return"]   = grp["pct_with_proj_return"].round(1).astype(str) + "%"

    return grp.rename(columns={
        "subgroup_code": "Subgroup",
        "subgroup_desc": "Subgroup Desc",
        "units_on_hire": "Units On Hire",
        "total_weekly": "Total Weekly £",
        "avg_weekly": "Avg £ / Unit",
        "earliest_start": "Oldest Start",
        "pct_no_po": "% No PO",
        "pct_with_proj_return": "% Has Proj.Return",
    })


# ---------- CUSTOMER ROLLUP ----------
def customer_rollup(df):
    site_counts = (
        df.groupby(["customer","site_name"], dropna=False)["unit_number"]
          .count()
          .reset_index()
          .groupby("customer")["site_name"]
          .nunique()
          .reset_index(name="site_count")
    )

    grp = df.groupby(
        ["customer"],
        dropna=False,
        as_index=False
    ).agg(
        total_weekly=("weekly_charge","sum"),
        assets_on_hire=("unit_number","count"),
        oldest_start=("start_date","min"),
        missing_po_lines=("po_number", lambda x: (x.isna() | (x.astype(str).str.strip()=="")).sum()),
        total_lines=("po_number","size"),
    )

    grp = grp.merge(site_counts, on="customer", how="left")

    grp["oldest_start"]   = pd.to_datetime(grp["oldest_start"], errors="coerce").dt.strftime("%d/%m/%Y")
    grp["total_weekly"]   = grp["total_weekly"].apply(money)
    grp["pct_missing_po"] = (
        (grp["missing_po_lines"] / grp["total_lines"]) * 100
    ).round(1).astype(str) + "%"

    final = grp.rename(columns={
        "customer": "Customer",
        "total_weekly": "Total Weekly £",
        "assets_on_hire": "Assets On Hire",
        "site_count": "Active Sites",
        "oldest_start": "Oldest Start On Hire",
        "pct_missing_po": "% Lines Missing PO",
    })[
        ["Customer","Total Weekly £","Assets On Hire","Active Sites","Oldest Start On Hire","% Lines Missing PO"]
    ]
    return final


# ---------- HIRE LINES TABLE (COLOUR ROWS) ----------
def classify_row_style(row, dupe_units=None, today=None):
    if today is None:
        today = pd.Timestamp.today().normalize()

    unit = str(row.get("unit_number","")).strip()
    if dupe_units and unit in dupe_units:
        return "highlight-dupe"

    pr  = row.get("projected_return", pd.NaT)
    po  = str(row.get("po_number", "")).strip()
    chg = row.get("weekly_charge", 0)

    if pd.notna(pr) and pr.normalize() < today:
        return "highlight-red"

    if pd.notna(pr) and 0 <= (pr.normalize() - today).days <= 7:
        return "highlight-amber"

    if (po == "" or po.lower() == "nan") and (chg or 0) > 0:
        return "highlight-purple"

    if (chg or 0) == 0:
        return "highlight-grey"

    return ""


def df_with_highlight_classes(df, dupe_units=None):
    today = pd.Timestamp.today().normalize()
    display_df = df.copy()

    if "weekly_charge" in display_df.columns:
        display_df["weekly_charge"] = display_df["weekly_charge"].apply(money)
    for dcol in ["start_date","projected_return"]:
        if dcol in display_df.columns:
            display_df[dcol] = display_df[dcol].dt.strftime("%d/%m/%Y")

    cols = [
        "customer","site_name","site_addr1","site_city","phone",
        "po_number","job_number","unit_number","description",
        "subgroup_code","subgroup_desc","start_date","projected_return",
        "weekly_charge","ticket_ref",
    ]
    cols = [c for c in cols if c in display_df.columns]

    pretty = display_df[cols].rename(columns={
        "customer": "Customer","site_name": "Site","site_addr1": "Addr1",
        "site_city": "City","phone": "Phone","po_number": "PO",
        "job_number": "Job #","unit_number": "Unit #","description": "Description",
        "subgroup_code": "Subgroup","subgroup_desc": "Subgroup Desc",
        "start_date": "Start","projected_return": "Projected Return",
        "weekly_charge": "Weekly £","ticket_ref": "Ticket Ref",
    })

    thead_html = "<thead><tr>" + "".join([f"<th>{c}</th>" for c in pretty.columns]) + "</tr></thead>"

    body_rows = []
    for idx, r in pretty.iterrows():
        original_row = df.loc[idx] if idx in df.index else {}
        css_class = classify_row_style(original_row, dupe_units=dupe_units, today=today)
        tds = "".join([f"<td>{r[c] if pd.notna(r[c]) else ''}</td>" for c in pretty.columns])
        body_rows.append(f"<tr class='{css_class}'>{tds}</tr>")

    tbody_html = "<tbody>" + "\n".join(body_rows) + "</tbody>"

    full_html = f"""
    <div style="max-height:70vh; overflow:auto; border:1px solid #dadada; border-radius:6px;">
    <table class="styled-table" style="width:100%; border-collapse:collapse; font-size:0.8rem; color:#40424a; background:#fff;">
    {thead_html}
    {tbody_html}
    </table>
    </div>
    """

    return full_html, pretty


# ---------- EXPORT HELPERS ----------
def export_button(df, filename_prefix="export"):
    csv_bytes = df.to_csv(index=False).encode("utf-8")

    to_xlsx = BytesIO()
    with pd.ExcelWriter(to_xlsx, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    to_xlsx.seek(0)

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            label="⬇ Download CSV",
            data=csv_bytes,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with c2:
        st.download_button(
            label="⬇ Download Excel",
            data=to_xlsx,
            file_name=f"{filename_prefix}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


def build_pdf_snapshot(
    report_date: str,
    total_weekly: float,
    total_lines: int,
    unique_customers: int,
    unique_sites: int,
    top_sub_df: pd.DataFrame,
    watchlists: list,
    dupe_df: pd.DataFrame,
) -> bytes:
    """
    Build a simple HTML-based PDF snapshot using reportlab-free approach —
    we produce an HTML string and use the built-in BytesIO + base64 trick
    to deliver it as a downloadable HTML file styled for print.
    This avoids any extra dependencies beyond what's already installed.
    """
    watch_html = ""
    for label, sub in watchlists:
        if sub.empty:
            watch_html += f"<h3>{label}</h3><p style='color:#666'>None</p>"
        else:
            watch_html += f"<h3>{label}</h3>"
            watch_html += sub.to_html(index=False, border=0, classes="snapshot-table")

    dupe_section = ""
    if not dupe_df.empty:
        dupe_section = "<h3>⚠️ Duplicate Unit Numbers Detected</h3>"
        dupe_section += dupe_df.to_html(index=False, border=0, classes="snapshot-table")
    else:
        dupe_section = "<h3>✅ No Duplicate Unit Numbers</h3>"

    top_sub_html = top_sub_df.to_html(index=False, border=0, classes="snapshot-table")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>Kensite Hire Snapshot – {report_date}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 2cm; color: #222; font-size: 12px; }}
  h1 {{ color: #0d823b; border-bottom: 3px solid #0d823b; padding-bottom: 6px; }}
  h2 {{ color: #40424a; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 24px; }}
  h3 {{ color: #40424a; margin-top: 18px; font-size: 13px; }}
  .kpi-row {{ display: flex; gap: 20px; margin: 16px 0; }}
  .kpi {{ background: #f4faf6; border: 1px solid #0d823b; border-radius: 6px;
           padding: 10px 18px; flex: 1; text-align: center; }}
  .kpi .val {{ font-size: 22px; font-weight: bold; color: #0d823b; }}
  .kpi .lbl {{ font-size: 11px; color: #555; }}
  table.snapshot-table {{ border-collapse: collapse; width: 100%; margin-top: 8px; font-size: 11px; }}
  table.snapshot-table th {{ background: #0d823b; color: white; padding: 5px 8px; text-align: left; }}
  table.snapshot-table td {{ border-bottom: 1px solid #ddd; padding: 4px 8px; }}
  table.snapshot-table tr:nth-child(even) td {{ background: #f8f8f8; }}
  .footer {{ margin-top: 30px; font-size: 10px; color: #999; border-top: 1px solid #eee; padding-top: 8px; }}
  @media print {{
    body {{ margin: 1cm; }}
    .kpi-row {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
<h1>Kensite Hire Dashboard – Snapshot</h1>
<p><strong>Report Date:</strong> {report_date}</p>

<h2>Key Metrics</h2>
<div class='kpi-row'>
  <div class='kpi'><div class='val'>£{total_weekly:,.2f}</div><div class='lbl'>Total Weekly Hire</div></div>
  <div class='kpi'><div class='val'>{total_lines}</div><div class='lbl'>Active Lines</div></div>
  <div class='kpi'><div class='val'>{unique_customers}</div><div class='lbl'>Customers</div></div>
  <div class='kpi'><div class='val'>{unique_sites}</div><div class='lbl'>Sites</div></div>
</div>

<h2>Top Subgroups by Weekly £</h2>
{top_sub_html}

<h2>Operational Watchlist</h2>
{watch_html}

<h2>Data Quality</h2>
{dupe_section}

<div class='footer'>Generated by Kensite Hire Dashboard · {report_date} · kensite.co.uk</div>
</body>
</html>"""

    return html.encode("utf-8")


# ---------- FILTER SIDEBAR ----------
def filter_df(df):
    s = st.sidebar
    s.header("Filters")

    customers = sorted(df["customer"].dropna().unique().tolist())
    pick_customers = s.multiselect("Customer", customers)

    sites = sorted(df["site_name"].dropna().unique().tolist())
    pick_sites = s.multiselect("Site / Job Name", sites)

    subgroups = (
        df[["subgroup_code","subgroup_desc"]]
        .drop_duplicates()
        .sort_values(["subgroup_code","subgroup_desc"])
    )
    subgroups["label"] = subgroups["subgroup_code"].fillna("") + " - " + subgroups["subgroup_desc"].fillna("")
    subgroup_options = subgroups["label"].tolist()
    pick_subgroups = s.multiselect("Subgroup", subgroup_options)

    po_search   = s.text_input("PO contains…").strip()
    job_search  = s.text_input("Job # contains…").strip()
    desc_search = s.text_input("Description contains…").strip()

    chg_min = float(df["weekly_charge"].min(skipna=True) or 0)
    chg_max = float(df["weekly_charge"].max(skipna=True) or 0)
    picked_chg = s.slider(
        "Weekly charge £ range",
        min_value=0.0,
        max_value=max(chg_max, 0.0),
        value=(0.0, max(chg_max, 0.0))
    )

    min_start = pd.to_datetime(df["start_date"]).min()
    max_start = pd.to_datetime(df["start_date"]).max()
    start_range = s.date_input(
        "Hire start between",
        value=(
            min_start.date() if pd.notna(min_start) else datetime(2000,1,1).date(),
            max_start.date() if pd.notna(max_start) else datetime.today().date()
        ),
    )

    min_proj = pd.to_datetime(df["projected_return"]).min()
    max_proj = pd.to_datetime(df["projected_return"]).max()
    proj_range = s.date_input(
        "Projected return between",
        value=(
            min_proj.date() if pd.notna(min_proj) else datetime(2000,1,1).date(),
            max_proj.date() if pd.notna(max_proj) else datetime.today().date()
        ),
    )

    only_missing_po      = s.checkbox("Only lines with no PO", value=False)
    only_has_proj_return = s.checkbox("Only lines with a Projected Return", value=False)
    exclude_service_like = s.checkbox("Exclude SERVICE / WATER / REHIRE / etc", value=True)

    out = df.copy()

    if pick_customers:
        out = out[out["customer"].isin(pick_customers)]
    if pick_sites:
        out = out[out["site_name"].isin(pick_sites)]
    if pick_subgroups:
        codes = [p.split(" - ")[0].strip() for p in pick_subgroups]
        out = out[out["subgroup_code"].isin(codes)]

    if po_search:
        out = out[out["po_number"].astype(str).str.contains(po_search, case=False, na=False)]
    if job_search:
        out = out[out["job_number"].astype(str).str.contains(job_search, case=False, na=False)]
    if desc_search:
        out = out[out["description"].astype(str).str.contains(desc_search, case=False, na=False)]

    out = out[
        (out["weekly_charge"].fillna(0) >= picked_chg[0]) &
        (out["weekly_charge"].fillna(0) <= picked_chg[1])
    ]

    if len(start_range) == 2:
        start_lo = pd.Timestamp(start_range[0])
        start_hi = pd.Timestamp(start_range[1]) + pd.Timedelta(days=1)
        out = out[
            out["start_date"].between(start_lo, start_hi, inclusive="left")
            | out["start_date"].isna()
        ]

    if len(proj_range) == 2:
        proj_lo = pd.Timestamp(proj_range[0])
        proj_hi = pd.Timestamp(proj_range[1]) + pd.Timedelta(days=1)
        out = out[
            out["projected_return"].between(proj_lo, proj_hi, inclusive="left")
            | out["projected_return"].isna()
        ]

    if only_missing_po:
        out = out[out["po_number"].astype(str).str.strip().isin(["","nan"])]

    if only_has_proj_return:
        out = out[out["projected_return"].notna()]

    if exclude_service_like:
        bad_words = [
            "SERVICE","SERVICING","WATER","REFILL","EMPTY","PUMP",
            "REHIRE","DISPOSAL","FUEL","CLEAN","TANKER"
        ]
        mask_bad = out["description"].str.upper().apply(
            lambda x: any(w in x for w in bad_words) if isinstance(x, str) else False
        )
        out = out[~mask_bad]

    s.markdown(f"<div class='small-label'>{len(out)} lines after filter</div>", unsafe_allow_html=True)
    return out


# ============================================================
# APP BODY
# ============================================================
st.markdown("#### Step 1: Upload current hire export (what's on hire / billing)")
hire_upload = st.file_uploader(
    "Equipment On Hire Excel (.xlsx)",
    type=["xlsx"],
    key="hire_file_uploader"
)

st.markdown("#### Step 2: Upload full fleet export (all assets + status for utilisation)")
fleet_upload = st.file_uploader(
    "Full Fleet / Utilisation Excel (.xlsx)",
    type=["xlsx"],
    key="fleet_file_uploader"
)

if hire_upload is None:
    st.info("⬆ Please upload the hire export to continue.")
    st.stop()

# Load hire data
raw_df = load_hire_file(hire_upload)

# Save revenue snapshot as soon as data is loaded (unfiltered total)
_raw_weekly_total = raw_df["weekly_charge"].sum(skipna=True)
try:
    append_revenue_snapshot(_raw_weekly_total)
except Exception:
    pass

# Sidebar filters
filtered_df = filter_df(raw_df)

# Detect duplicates once (on full unfiltered data so nothing is missed)
_dupe_set = set()
if "unit_number" in raw_df.columns:
    valid_units = raw_df[~raw_df["unit_number"].isin(["","nan","NaN"])]["unit_number"]
    counts = valid_units.value_counts()
    _dupe_set = set(counts[counts > 1].index.tolist())

# Create tabs
tab_dashboard, tab_lines, tab_subgroup, tab_customer, tab_watch, tab_util = st.tabs(
    ["📊 Dashboard", "📋 Hire Lines", "🏷 Subgroups", "👤 Customers", "🚨 Watchlist", "📈 Utilisation"]
)


# ========== DASHBOARD TAB ==========
with tab_dashboard:
    total_weekly      = filtered_df["weekly_charge"].sum(skipna=True)
    total_lines       = len(filtered_df)
    unique_customers  = filtered_df["customer"].nunique()
    unique_sites      = filtered_df["site_name"].nunique()

    sub_rev = (
        filtered_df.groupby("subgroup_desc", dropna=False)["weekly_charge"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-label'>Weekly Hire (filtered)</div>"
            f"<div class='kpi-value'>{money(total_weekly)}</div></div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-label'>Active Lines</div>"
            f"<div class='kpi-value'>{total_lines}</div></div>",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-label'>Customers</div>"
            f"<div class='kpi-value'>{unique_customers}</div></div>",
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-label'>Sites</div>"
            f"<div class='kpi-value'>{unique_sites}</div></div>",
            unsafe_allow_html=True
        )

    # Duplicate unit alert on dashboard
    if _dupe_set:
        st.warning(f"⚠️ {len(_dupe_set)} unit number(s) appear on multiple active hire lines — see Hire Lines tab (orange rows) or Watchlist.")

    st.markdown("#### Top 5 Subgroups by Weekly £ (filtered)")
    top_sub_df = (
        sub_rev.reset_index()
        .rename(columns={"subgroup_desc":"Subgroup", "weekly_charge":"Weekly £"})
    )
    top_sub_df["Weekly £"] = top_sub_df["Weekly £"].apply(money)
    st.dataframe(top_sub_df, use_container_width=True, hide_index=True)

    # ── IMPROVEMENT 2: Weekly revenue trend chart ──
    rev_hist = load_revenue_history()
    if not rev_hist.empty and len(rev_hist) >= 2:
        st.markdown("#### Weekly Hire Revenue Trend")
        rev_fig = go.Figure()
        rev_fig.add_trace(go.Scatter(
            x=rev_hist["snapshot_date"],
            y=rev_hist["total_weekly"],
            mode="lines+markers",
            line=dict(color="#0d823b", width=2),
            marker=dict(size=6, color="#0d823b"),
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>£%{y:,.2f}<extra></extra>",
        ))
        rev_fig.update_layout(
            height=260,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#f9fafb",
            font=dict(color="#40424a", family="Figtree, system-ui, sans-serif"),
            xaxis=dict(gridcolor="#e8e8e8", title="Date", linecolor="#dadada"),
            yaxis=dict(gridcolor="#e8e8e8", title="Total Weekly £",
                       tickprefix="£", tickformat=",.0f", linecolor="#dadada"),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(rev_fig, use_container_width=True)
    elif not rev_hist.empty:
        st.caption("Revenue trend will appear here once you've uploaded data on more than one date.")

    # ── IMPROVEMENT 5: PDF/HTML snapshot export ──
    st.markdown("#### Export Dashboard Snapshot")
    st.caption("Downloads a print-ready HTML file — open in your browser and use Ctrl+P / ⌘+P to save as PDF.")

    watchlists_for_pdf = build_watchlists(filtered_df)
    dupe_df_for_pdf    = find_duplicate_units(raw_df)
    report_date_str    = datetime.today().strftime("%d/%m/%Y")

    snapshot_html = build_pdf_snapshot(
        report_date=report_date_str,
        total_weekly=total_weekly,
        total_lines=total_lines,
        unique_customers=unique_customers,
        unique_sites=unique_sites,
        top_sub_df=top_sub_df,
        watchlists=watchlists_for_pdf,
        dupe_df=dupe_df_for_pdf,
    )

    st.download_button(
        label="⬇ Download Snapshot (HTML → Print as PDF)",
        data=snapshot_html,
        file_name=f"kensite_snapshot_{datetime.today().strftime('%Y%m%d')}.html",
        mime="text/html",
        use_container_width=True,
    )

    if "report_generated_at" in raw_df.columns and raw_df["report_generated_at"].notna().any():
        ts = raw_df["report_generated_at"].dropna().iloc[0]
        ts_txt = ts.strftime("%d/%m/%Y %H:%M") if isinstance(ts, pd.Timestamp) else str(ts)
        st.caption(f"Source export timestamp: {ts_txt}")


# ========== HIRE LINES TAB ==========
with tab_lines:
    st.markdown("### Hire Lines (Filtered)")
    st.caption("Row colours: 🟠 Duplicate unit · 🔴 Overdue · 🟡 Due within 7 days · 🟣 Missing PO · ⬜ £0 rate")

    html_table, export_df = df_with_highlight_classes(filtered_df, dupe_units=_dupe_set)
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("##### Export these rows")
    export_button(export_df, filename_prefix="hire_lines_filtered")


# ========== SUBGROUP TAB ==========
with tab_subgroup:
    st.markdown("### Subgroup Summary (Filtered)")
    sg = subgroup_rollup(filtered_df)
    st.dataframe(sg, use_container_width=True, hide_index=True)
    st.markdown("##### Export subgroup summary")
    export_button(sg, filename_prefix="subgroup_summary")


# ========== CUSTOMER TAB ==========
with tab_customer:
    st.markdown("### Customer Summary (Filtered)")
    cust = customer_rollup(filtered_df)
    st.dataframe(cust, use_container_width=True, hide_index=True)
    st.markdown("##### Export customer summary")
    export_button(cust, filename_prefix="customer_summary")


# ========== WATCHLIST TAB ==========
with tab_watch:
    st.markdown("### Operational Watchlist (Filtered)")
    st.caption("Who do we need to call today?")

    watchlists = build_watchlists(filtered_df)

    # ── IMPROVEMENT 3: Single watchlist export ──
    all_watch_frames = []
    for label, subdf in watchlists:
        if not subdf.empty:
            subdf_copy = subdf.copy()
            subdf_copy.insert(0, "Category", label.split(" ", 1)[-1])  # strip emoji prefix
            all_watch_frames.append(subdf_copy)
        st.markdown(f"#### {label}")
        if subdf.empty:
            st.success("None — clear.")
        else:
            st.dataframe(subdf, use_container_width=True, hide_index=True)
        st.markdown("---")

    if all_watch_frames:
        combined_watch = pd.concat(all_watch_frames, ignore_index=True)
        st.markdown("##### Export full watchlist")
        export_button(combined_watch, filename_prefix=f"watchlist_{datetime.today().strftime('%Y%m%d')}")
    else:
        st.success("All clear — no items on the watchlist today.")

    # ── IMPROVEMENT 4: Duplicate unit detection ──
    st.markdown("### ⚠️ Duplicate Unit Numbers")
    st.caption("Same unit appearing on more than one active hire line — may indicate a billing error.")
    dupe_df = find_duplicate_units(raw_df)
    if dupe_df.empty:
        st.success("No duplicate unit numbers detected.")
    else:
        st.error(f"{len(_dupe_set)} unit(s) appear on multiple active hire lines.")
        st.dataframe(dupe_df, use_container_width=True, hide_index=True)
        export_button(dupe_df, filename_prefix="duplicate_units")


# ========== UTILISATION TAB ==========
with tab_util:
    st.markdown("### Fleet Utilisation")

    if fleet_upload is None:
        st.info("⬆ Upload the full fleet / utilisation export above to see this tab.")
    else:
        fleet_df  = load_fleet_file(fleet_upload)
        util_now  = current_utilisation_table(fleet_df)

        st.markdown("#### Current Utilisation by Subgroup")
        st.dataframe(util_now, use_container_width=True, hide_index=True)

        st.markdown("##### Export utilisation table")
        export_button(util_now, filename_prefix="utilisation_current")

        try:
            append_snapshot_to_history(util_now)
            st.caption("Snapshot recorded to utilisation_history.csv")
        except Exception as e:
            st.warning(f"Couldn't write utilisation_history.csv: {e}")

        history_df = load_history()

        if history_df.empty:
            st.info("No utilisation history logged yet. Upload again next week and you'll start to see trends.")
        else:
            # Only show real asset subgroups (exclude service/labour codes with 0% across all dates)
            meaningful = (
                history_df.groupby("Subgroup")["Utilisation %"]
                .max()
                .reset_index()
            )
            meaningful = meaningful[meaningful["Utilisation %"] > 0]["Subgroup"].tolist()

            all_codes = sorted(meaningful)

            st.markdown("#### Utilisation Trend")
            st.caption("Select one or more subgroups to compare.")

            pick_codes = st.multiselect(
                "Subgroup(s) to view:",
                options=all_codes,
                default=all_codes[:3] if len(all_codes) >= 3 else all_codes
            )

            if pick_codes:
                hist_sub = history_df[history_df["Subgroup"].isin(pick_codes)].copy()

                # ── IMPROVEMENT 1: Line chart for utilisation trend ──
                util_fig = go.Figure()
                colours = [
                    "#0d823b","#40424a","#4fc97e","#a0c4ff","#e07020",
                    "#c060e0","#e06080","#f0c040","#60b0f0","#80e0d0",
                ]
                for i, code in enumerate(pick_codes):
                    sub_plot = hist_sub[hist_sub["Subgroup"] == code].sort_values("snapshot_date")
                    util_fig.add_trace(go.Scatter(
                        x=sub_plot["snapshot_date"],
                        y=sub_plot["Utilisation %"],
                        mode="lines+markers",
                        name=code,
                        line=dict(color=colours[i % len(colours)], width=2),
                        marker=dict(size=6),
                        hovertemplate=f"<b>{code}</b><br>%{{x|%d/%m/%Y}}<br>%{{y:.1f}}%<extra></extra>",
                    ))
                util_fig.update_layout(
                    height=320,
                    paper_bgcolor="#ffffff",
                    plot_bgcolor="#f9fafb",
                    font=dict(color="#40424a", family="Figtree, system-ui, sans-serif"),
                    xaxis=dict(gridcolor="#e8e8e8", title="Date", linecolor="#dadada"),
                    yaxis=dict(gridcolor="#e8e8e8", title="Utilisation %",
                               range=[0, 100], ticksuffix="%", linecolor="#dadada"),
                    legend=dict(bgcolor="#ffffff", bordercolor="#dadada",
                                font=dict(color="#40424a")),
                    margin=dict(l=10, r=10, t=10, b=10),
                )
                st.plotly_chart(util_fig, use_container_width=True)

                # Text summary per selected subgroup
                for code in pick_codes:
                    sub = hist_sub[hist_sub["Subgroup"] == code].sort_values("snapshot_date")
                    if len(sub) >= 2:
                        first_val  = float(sub.iloc[0]["Utilisation %"])
                        last_val   = float(sub.iloc[-1]["Utilisation %"])
                        first_date = sub.iloc[0]["snapshot_date"].date()
                        last_date  = sub.iloc[-1]["snapshot_date"].date()
                        arrow      = "↑" if last_val > first_val else "↓" if last_val < first_val else "→"
                        delta      = abs(last_val - first_val)
                        st.markdown(
                            f"**{code}** {arrow} {first_val:.1f}% → {last_val:.1f}% "
                            f"({delta:.1f}pp change · {first_date} to {last_date})"
                        )
