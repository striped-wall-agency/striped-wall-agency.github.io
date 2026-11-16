"""Check the static site's structure and relative resources without dependencies."""
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from inline_styles import PAGES, ROOT, check_styles

CASE_DISCLOSURES = {
    'subdesk': (
        'IndexedDB', 'Fictional', 'no server, payment provider or real money',
        'not server authentication', 'illustrative HTML/CSS recreations',
    ),
    'subflow': ('Fictional customers and billing data', 'No real recurring charges'),
    'paycontrol': ('Fictional Northstar Commerce data', 'No live provider connection or real payment actions'),
}


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
    pages = {ROOT / name: Page(ROOT / name) for name in PAGES}
    errors = check_styles()
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
    home = pages[ROOT / 'index.html']
    for slug, disclosures in CASE_DISCLOSURES.items():
        route = f'work/{slug}/'
        case = pages[ROOT / route / 'index.html']
        case_html = ' '.join(case.path.read_text().split())
        for disclosure in disclosures:
            if disclosure not in case_html:
                errors.append(f'{route}: missing disclosure {disclosure}')
        if route not in home.links or '../../index.html#work' not in case.links:
            errors.append(f'{route}: missing homepage/case navigation')
        if f'https://stripedwall.agency/{slug}-demo/' not in case.links:
            errors.append(f'{route}: missing exact demo URL')
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
