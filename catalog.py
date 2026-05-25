#!/usr/bin/env python3
"""
Property catalog manager for student housing analysis.
Usage:
  python catalog.py list                  - show all properties
  python catalog.py show <id>             - show full property details
  python catalog.py compare <id1> <id2>  - side-by-side comparison
  python catalog.py score <id>           - print student housing score card
  python catalog.py market <city>        - show market benchmarks for a city
  python catalog.py reports              - list available market reports
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
        gla = f"{p['gla_sqm']:,} sqm" if p.get("gla_sqm") else "GLA TBD"
        complete = "" if p.get("data_complete", True) else "  [data incomplete]"
        print(f"  [{p['id']}]  {p['name']}, {p['city']}  |  {gla}{complete}")
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


def load_market_report(report_id):
    cat = load_catalog()
    entry = next((r for r in cat.get("market_reports", []) if r["id"] == report_id), None)
    if not entry:
        return None
    with open(BASE / entry["file"]) as f:
        return json.load(f)


def market_benchmarks(city):
    cat = load_catalog()
    reports = cat.get("market_reports", [])
    if not reports:
        print("No market reports loaded yet.")
        return

    city_cap = city.strip().title()
    found = False
    for r_entry in reports:
        report = load_market_report(r_entry["id"])
        if not report:
            continue

        city_data = report.get("city_profiles", {}).get(city_cap)
        prime_rent = report.get("rental_prices_prime_pbsa_per_month_eur", {}).get(city_cap)
        shared_rent = report.get("rental_prices_private_shared_rooms_per_month_eur", {}).get(city_cap)
        unis = [u for u in report.get("universities_by_international_enrollment_2024_25", [])
                if u.get("city", "").lower() == city_cap.lower()]

        if not city_data and not prime_rent and not unis:
            continue

        found = True
        print(f"\n{'='*60}")
        print(f"MARKET BENCHMARKS: {city_cap}  |  Source: {report['publisher']} {report['date'][:4]}")
        print(f"{'='*60}")

        print(f"\n  DEMAND")
        d = report["demand"]
        print(f"    Italy total HE students:   {d['total_students_he_2024_25']:,}")
        print(f"    International students:    {d['international_students_2024_25']:,} (+{d['international_yoy_growth_pct']}% YoY)")
        if city_data:
            print(f"\n  {city_cap.upper()} PROFILE")
            for k, v in city_data.items():
                if v is not None:
                    print(f"    {k.replace('_', ' ').title():<30} {v}")

        print(f"\n  RENTAL PRICES")
        if prime_rent:
            print(f"    Prime PBSA (all-in):       €{prime_rent:,}/month")
        if shared_rent:
            print(f"    Private shared room:       €{shared_rent['low']}–€{shared_rent['high']}/month")

        if unis:
            print(f"\n  UNIVERSITIES (international enrollment 2024/25)")
            for u in unis:
                growth = f"+{u['5yr_growth_pct']}% (5yr)" if u.get("5yr_growth_pct") else ""
                print(f"    {u['university']:<25} {u['intl_students']:>6} intl students  {growth}")

        print(f"\n  SUPPLY (national context)")
        s = report["supply"]
        print(f"    National bed stock:        ~{s['total_beds_national']:,}")
        print(f"    Private sector share:      {s['private_sector_share_current_pct']}% (was {s['private_sector_share_2021_pct']}% in 2021)")
        p = s["pipeline_by_2027"]
        city_pipe = p.get(f"{city_cap.lower()}_beds_in_development") or p.get(f"{city_cap.lower()}_new_facilities_30mo")
        if city_pipe:
            print(f"    Pipeline beds ({city_cap}):     {city_pipe:,}")

        print(f"\n  KEY DESIGN IMPLICATIONS")
        for imp in report.get("key_design_implications", []):
            print(f"    - {imp}")
        print()

    if not found:
        available = list(next(load_market_report(r["id"]) for r in reports
                              if load_market_report(r["id"]))
                         .get("rental_prices_prime_pbsa_per_month_eur", {}).keys())
        print(f"No market data found for '{city_cap}'. Available: {', '.join(available)}")


def list_reports():
    cat = load_catalog()
    reports = cat.get("market_reports", [])
    print(f"\n--- MARKET REPORTS ({len(reports)}) ---")
    for r in reports:
        print(f"  [{r['id']}]  {r['title']}")
        print(f"    Country: {r['country']} | Date: {r['date']}")
        print(f"    File:    {r['file']}")
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
    elif args[0] == "market" and len(args) == 2:
        market_benchmarks(args[1])
    elif args[0] == "reports":
        list_reports()
    else:
        print(__doc__)
