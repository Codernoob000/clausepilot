"""Scrub remaining hardcoded strings from templates per frontend-wiring-spec.md Phase 4 exit check."""

import os

replacements = {
    "templates/screen2.html": [
        ("Apex_Creative_Studio_MSA_2025.pdf", "Contract_Agreement_Review.pdf"),
        ("Apex", "Contract"),
        ("38 Clauses found", '<span id="screen2-clause-count">Scanning clauses</span>'),
        ("38 Clauses", "Clauses"),
        ("94% of independent contractors", "Freelance benchmark standard: Most contractors"),
        ('<span class="absolute font-label-sm text-label-sm font-bold text-primary">94%</span>', '<span class="absolute font-label-sm text-label-sm font-bold text-primary">Benchmark</span>')
    ],
    "templates/screen3.html": [
        ("Apex", "Client"),
        ("94% of independent design contracts", "Most independent commercial contracts"),
    ],
    "templates/screen4.html": [
        ("Apex", "Client"),
        ("Elena", "Client Team"),
        ('<span class="font-headline-sm text-headline-sm text-on-surface font-bold">82%</span>', '<span id="acceptance-rate-stat" class="font-headline-sm text-headline-sm text-on-surface font-bold">--</span>'),
        ("<strong>94%</strong>", "<strong>Industry benchmark</strong>"),
        ("82%", "--")
    ],
    "templates/screen5.html": [
        ("Apex", "Client"),
        ("3 of 38 Clauses Flagged", '<span id="prep-flagged-stat">Key Flagged Clauses</span>'),
        ("38 Clauses", "Clauses")
    ]
}

for file_path, pairs in replacements.items():
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in pairs:
        content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Scrubbed {file_path}")
