"""Embed authored CSS into the two static pages to avoid blocking requests."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    'index.html': ('assets/css/home.css', 'assets/css/base.css'),
    'work/subdesk/index.html': ('../../assets/css/subdesk.css', '../../assets/css/base.css'),
}


def render(path, sources):
    html = path.read_text()
    for source in sources:
        escaped = re.escape(source)
        pattern = rf'<link rel="stylesheet" href="{escaped}">|<style data-source="{escaped}">.*?</style>'
        css = (path.parent / source).read_text().rstrip()
        style = f'<style data-source="{source}">\n{css}\n</style>'
        html, count = re.subn(pattern, lambda match: style, html, flags=re.DOTALL)
        if count != 1:
            raise ValueError(f'{path.relative_to(ROOT)}: expected one stylesheet slot for {source}')
    return html


def check_styles():
    errors = []
    for name, sources in PAGES.items():
        path = ROOT / name
        if path.read_text() != render(path, sources):
            errors.append(f'{name}: run python3 scripts/inline_styles.py to update embedded CSS')
    return errors


if __name__ == '__main__':
    for name, sources in PAGES.items():
        path = ROOT / name
        path.write_text(render(path, sources))
    print(f'Embedded CSS in {len(PAGES)} pages.')
