const menu = document.querySelector('.menu-toggle');
const navigation = document.getElementById('main-navigation');
const compactLayout = window.matchMedia('(max-width: 900px)');

if (menu && navigation) {
  document.documentElement.classList.add('nav-enhanced');

  function closeMenu(returnFocus = false) {
    menu.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
    if (returnFocus) menu.focus();
  }

  menu.addEventListener('click', () => {
    const opening = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(opening));
    navigation.classList.toggle('is-open', opening);
    if (opening) navigation.querySelector('a').focus();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu(true);
    }
  });

  navigation.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link || !compactLayout.matches) return;
    closeMenu();
    const target = document.getElementById(link.hash.slice(1));
    if (target) {
      target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    }
  });

  compactLayout.addEventListener('change', () => {
    const focusWillHide = compactLayout.matches && navigation.contains(document.activeElement);
    closeMenu(focusWillHide);
  });
}
