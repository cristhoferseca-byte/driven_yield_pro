import re
import glob

# SVG genérico para reemplazar emojis
SVG_ICON = '<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>'

# Regex para detectar emojis (rangos Unicode comunes para emojis)
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27BF\u2300-\u23FF\u2B50\u2B55\u2934\u2935\u2B05-\u2B07\u2B1B\u2B1C\u2190-\u2199\u21A9\u21AA\u25B6\u25C0\u25FB-\u25FE\u203C\u2049\u2122\u2139\u2194\u2195]')

vue_files = glob.glob('c:/Users/admin/Downloads/driven-yield-pro/proyecto_final/src/**/*.vue', recursive=True)

for file in vue_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if emoji_pattern.search(content):
        # Reemplazar emojis con SVG_ICON
        new_content = emoji_pattern.sub(SVG_ICON, content)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Reemplazados emojis en: {file}")
