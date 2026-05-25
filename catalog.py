#!/usr/bin/env python3
"""
Property catalog manager for student housing analysis.
Usage:
  python catalog.py list                  - show all properties
  python catalog.py show <id>             - show full property details
  python catalog.py compare <id1> <id2>  - side-by-side comparison
  python catalog.py score <id>           - print student housing score card
"""

import json
import sys
import os
from pathlib import Path

BASE = Path(__file__).parent
CATALOG_FILE = BASE / "properties" / "catalog.json"


def load_catalog():
    with open(CATALOG_FILE) as f:
        return json.load(f)


def load_property(file_path):
    with open(BASE / file_path) as f:
        return json.load(f)


def list_properties():
    cat = load_catalog()
    print(f"\n{'='*70}")
    print(f"PROPERTY CATALOG  |  Last updated: {cat['last_updated']}")
    print(f"{'='*70}")

    print(f"\n--- CANDIDATE OFFERS ({cat['summary']['total_candidates']}) ---")
    if not cat["candidates"]:
        print("  (none yet)")
    for p in cat["candidates"]:
        verdict = p["student_housing_verdict"].upper()
        print(f"  [{p['id']}]")
        print(f"    Name:       {p['name']}, {p['city']}")
        print(f"    GLA:        {p['gla_sqm']:,} sqm")
        print(f"    Broker:     {p['broker']} | {p['market_status']}")
        print(f"    Received:   {p['date_received']}")
        print(f"    SH Verdict: {verdict}")
        print()

    print(f"--- OWNED / REFERENCE PROPERTIES ({cat['summary']['total_owned']}) ---")
    if not cat["owned"]:
        print("  (none yet — add your purchased buildings to benchmark against)\n")
    for p in cat["owned"]:
        print(f"  [{p['id']}]  {p['name']}, {p['city']}  |  {p['gla_sqm']:,} sqm")
        print()


def show_property(prop_id):
    cat = load_catalog()
    all_props = cat["candidates"] + cat["owned"]
    entry = next((p for p in all_props if p["id"] == prop_id), None)
    if not entry:
        print(f"Property '{prop_id}' not found. Run `python catalog.py list` to see IDs.")
        return
    data = load_property(entry["file"])
    print(json.dumps(data, indent=2))


def compare_properties(id1, id2):
    cat = load_catalog()
    all_entries = cat["candidates"] + cat["owned"]

    def get(prop_id):
        e = next((p for p in all_entries if p["id"] == prop_id), None)
        if not e:
            print(f"Property '{prop_id}' not found.")
            sys.exit(1)
        return load_property(e["file"])

    a, b = get(id1), get(id2)

    rows = [
        ("Name",            a["property"]["name"],                          b["property"]["name"]),
        ("City",            a["property"]["city"],                          b["property"]["city"]),
        ("Neighborhood",    a["property"]["neighborhood"],                   b["property"].get("neighborhood", "-")),
        ("Location Tier",   a["property"]["location_tier"],                  b["property"].get("location_tier", "-")),
        ("Market Status",   a["property"]["market_status"],                  b["property"].get("market_status", "-")),
        ("GLA sqm",         f"{a['physical']['gla_sqm']:,}",                f"{b['physical']['gla_sqm']:,}"),
        ("Floors (above)",  str(a["physical"]["above_ground_floors"]),       str(b["physical"].get("above_ground_floors", "-"))),
        ("Car Parking",     str(a["physical"]["parking"]["car_spaces"]),     str(b["physical"]["parking"].get("car_spaces", "-"))),
        ("Current Use",     a["current_status"]["current_use"],              b["current_status"].get("current_use", "-")),
        ("Occupancy",       f"{a['current_status']['occupancy_pct']}%",      f"{b['current_status'].get('occupancy_pct', '-')}%"),
        ("Asset Profile",   a["asset_profile"]["jll_classification"],        b["asset_profile"].get("jll_classification", "-")),
        ("SH Verdict",      a["student_housing_assessment"]["verdict"],      b["student_housing_assessment"].get("verdict", "-")),
        ("Asking Price",    str(a["financials"]["asking_price_eur"] or "TBD"), str(b["financials"].get("asking_price_eur") or "TBD")),
        ("Price/sqm",       str(a["financials"]["price_per_sqm_eur"] or "TBD"), str(b["financials"].get("price_per_sqm_eur") or "TBD")),
    ]

    col_w = 22
    print(f"\n{'='*70}")
    print(f"COMPARISON: {id1}  vs  {id2}")
    print(f"{'='*70}")
    print(f"{'':22} {'LEFT':^22} {'RIGHT':^22}")
    print(f"{'-'*70}")
    for label, val_a, val_b in rows:
        diff = " <--" if val_a != val_b and val_a not in ("-", "TBD", "pending") else ""
        print(f"{label:<22} {val_a:<22} {val_b:<22}{diff}")
    print()


def score_card(prop_id):
    cat = load_catalog()
    all_entries = cat["candidates"] + cat["owned"]
    entry = next((p for p in all_entries if p["id"] == prop_id), None)
    if not entry:
        print(f"Property '{prop_id}' not found.")
        return
    data = load_property(entry["file"])
    p = data["physical"]
    cs = data["current_status"]
    prop = data["property"]

    print(f"\n{'='*60}")
    print(f"STUDENT HOUSING SCORE CARD: {prop['name']}, {prop['city']}")
    print(f"{'='*60}")

    checks = [
        ("GLA > 2,000 sqm",         p["gla_sqm"] > 2000),
        ("4+ floors",               p["above_ground_floors"] >= 4),
        ("Currently vacant",        cs["occupancy_pct"] == 0),
        ("Office/commercial (easy conversion)", cs["current_use"] in ["Office", "Commercial"]),
        ("Parking available",       p["parking"]["car_spaces"] > 0),
        ("Courtyard / outdoor",     p.get("courtyard", False)),
        ("City centre / semicentre", prop.get("location_tier", "") in ["Centre", "Semicentre", "CBD"]),
        ("Off market (less competition)", prop.get("market_status") == "Off Market"),
    ]

    score = sum(1 for _, v in checks if v)
    for label, passed in checks:
        icon = "[YES]" if passed else "[ NO]"
        print(f"  {icon}  {label}")

    print(f"\n  Score: {score}/{len(checks)}")
    assessment = data["student_housing_assessment"]
    if assessment.get("notes"):
        print("\n  Notes:")
        for n in assessment["notes"]:
            print(f"    - {n}")
    print()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "list":
        list_properties()
    elif args[0] == "show" and len(args) == 2:
        show_property(args[1])
    elif args[0] == "compare" and len(args) == 3:
        compare_properties(args[1], args[2])
    elif args[0] == "score" and len(args) == 2:
        score_card(args[1])
    else:
        print(__doc__)
