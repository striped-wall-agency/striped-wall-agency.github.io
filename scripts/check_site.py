"""Check the static site's structure and relative resources without dependencies."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / 'index.html', ROOT / 'work/subdesk/index.html']


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.tags = Counter()
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


def check():
    pages = {path: Page(path) for path in PAGES}
    errors = []
    for path, page in pages.items():
        label = path.relative_to(ROOT)
        for tag in ('main', 'h1', 'title'):
            if page.tags[tag] != 1:
                errors.append(f'{label}: expected one {tag}')
        if len(page.ids) != len(set(page.ids)):
            errors.append(f'{label}: duplicate IDs')
        if 'main-navigation' not in page.ids or '#main' not in page.links:
            errors.append(f'{label}: missing navigation or skip link')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith('/'):
                errors.append(f'{label}: non-relative URL {link}')
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= 'index.html'
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f'{label}: missing resource {link}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{label}: missing anchor {link}')
    home = PAGES[0].read_text()
    case = PAGES[1].read_text()
    for text in ('IndexedDB', 'Fictional', 'no server, payment provider or real money', 'not server authentication', 'illustrative HTML/CSS recreations'):
        if text not in case:
            errors.append(f'case: missing disclosure {text}')
    if 'work/subdesk/' not in home or '../../index.html#work' not in case:
        errors.append('missing homepage/case navigation')
    if 'https://stripedwall.agency/subdesk-demo/' not in case:
        errors.append('missing exact demo URL')
    if (ROOT / 'CNAME').read_text().strip() != 'stripedwall.agency':
        errors.append('CNAME changed')
    for css in (ROOT / 'assets/css').glob('*.css'):
        if any(line.startswith('+') for line in css.read_text().splitlines()):
            errors.append(f'{css.name}: source patch artifact')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Checked {len(pages)} pages: structure, disclosures, relative resources and anchors OK.')


if __name__ == '__main__':
    check()
