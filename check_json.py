import json

with open("modules/krc_data.json", "r", encoding="utf-8") as f:
    content = f.read()

# Check for duplicate keys
from collections import Counter
import re

keys = re.findall(r'"\s*(\d+)"\s*:', content)
counts = Counter(keys)
duplicates = {k: v for k, v in counts.items() if v > 1}
print("Duplicate keys:", duplicates)
print("Total entries found:", len(keys))

# Also validate it's proper JSON
try:
    data = json.loads(content)
    print("✅ Valid JSON! Total unique entries:", len(data))
except json.JSONDecodeError as e:
    print("❌ JSON Error:", e)