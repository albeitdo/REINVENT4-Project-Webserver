with open(r'C:\Users\lenovonew\.gemini\antigravity\brain\2dfba1ae-2ec8-429e-bdae-5d30939919fe\.system_generated\steps\1008\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'https://media\.slidesgo\.com/storage/[^\s"\'<>]+', text)
for m in sorted(set(matches)):
    if 'interface-style' in m:
        print(m)
