import pandas as pd
import json
import re

URL = "https://mmhapu.ac.in/krc_without_aicte"

def find_column(df, keywords):
    """Column ka naam dhoondo jisme diye gaye keywords mile"""
    for col in df.columns:
        col_lower = str(col).lower()
        if any(kw in col_lower for kw in keywords):
            return col
    return None

def scrape_and_build():
    print("🔍 Fetching tables from website...")
    tables = pd.read_html(URL)
    print(f"✅ Total tables found: {len(tables)}\n")

    all_data = {}

    for i, df in enumerate(tables):
        print(f"--- Table {i} ---")
        print("Columns:", df.columns.tolist())
        print(df.head(2))
        print()

        # Column auto-detect karna
        code_col = find_column(df, ["code"])
        name_col = find_column(df, ["name", "krcn"])
        district_col = find_column(df, ["district"])
        address_col = find_column(df, ["address"])
        email_col = find_column(df, ["email"])
        incharge_col = find_column(df, ["incharge", "in-charge", "director"])
        contact_col = find_column(df, ["contact", "phone", "mobile"])
        management_col = find_column(df, ["management"])
        course_col = find_column(df, ["course"])
        intake_col = find_column(df, ["intake", "seat"])

        # Agar is table mein "code" column nahi mila, skip kar (galat table hai)
        if not code_col:
            print(f"⚠️ Table {i} mein 'code' column nahi mila, skip kar raha hoon.\n")
            continue

        for _, row in df.iterrows():
            code = str(row[code_col]).strip()
            if not code or code.lower() == "nan" or not re.match(r'^\d+$', code):
                continue  # invalid/empty code skip karo

            entry = all_data.get(code, {})  # agar pehle se hai toh existing data merge karo
            if name_col and pd.notna(row.get(name_col)):
                entry["name"] = str(row[name_col]).strip()
            if district_col and pd.notna(row.get(district_col)):
                entry["district"] = str(row[district_col]).strip()
            if address_col and pd.notna(row.get(address_col)):
                entry["address"] = str(row[address_col]).strip()
            if email_col and pd.notna(row.get(email_col)):
                entry["email"] = str(row[email_col]).strip()
            if incharge_col and pd.notna(row.get(incharge_col)):
                entry["incharge"] = str(row[incharge_col]).strip()
            if contact_col and pd.notna(row.get(contact_col)):
                entry["contact"] = str(row[contact_col]).strip()
            if management_col and pd.notna(row.get(management_col)):
                entry["management"] = str(row[management_col]).strip()
            if course_col and pd.notna(row.get(course_col)):
                entry["course"] = str(row[course_col]).strip()
            if intake_col and pd.notna(row.get(intake_col)):
                entry["intake"] = str(row[intake_col]).strip()

            all_data[code] = entry

    return all_data

if __name__ == "__main__":
    data = scrape_and_build()

    output_path = "modules/krc_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Done! {len(data)} KRC entries saved to {output_path}")