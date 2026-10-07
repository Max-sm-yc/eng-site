// Route direct SWF links through the local Ruffle player.
document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (!link) return;
  const target = new URL(link.href, location.href);
  if (target.origin !== location.origin || !target.pathname.toLowerCase().endsWith('.swf')) return;
  event.preventDefault();
  location.href = '/player.html?movie=' + encodeURIComponent(target.pathname + target.search);
});
