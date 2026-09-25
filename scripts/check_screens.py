import glob
import os
import re

forbidden = ['Apex', 'Elena', 'Maya Lin', '82%', '94%', '38 Clauses']

for path in sorted(glob.glob('templates/screen*.html')):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    print(f'=== {os.path.basename(path)} ===')
    found_any = False
    for term in forbidden:
        count = content.count(term)
        if count > 0:
            found_any = True
            print(f'  Found "{term}": {count} occurrences')
            # Show matching lines/context
            for line_no, line in enumerate(content.splitlines(), 1):
                if term in line:
                    print(f'    Line {line_no}: {line.strip()[:100]}')
    if not found_any:
        print('  CLEAN: 0 forbidden strings')
