(function () {
  // Only run on post pages
  const path = window.location.pathname;
  const postMatch = path.match(/\/(posts\/[^/]+)\//);
  if (!postMatch) return;

  const postPath = postMatch[1]; // e.g. "posts/2026-03-10-ai-tutorial"
  const rawUrl = `https://raw.githubusercontent.com/lawwu/lawwu.github.io/main/${postPath}/index.qmd`;

  function createButton() {
    const btn = document.createElement('button');
    btn.id = 'copy-markdown-btn';
    btn.innerHTML = '<i class="bi bi-clipboard"></i> Copy Markdown';
    btn.title = 'Copy post source as Markdown (.qmd)';
    btn.style.cssText = [
      'position:fixed',
      'top:0.6rem',
      'right:1rem',
      'z-index:1000',
      'padding:0.35rem 0.85rem',
      'background:#fff',
      'color:#333',
      'border:1px solid #ccc',
      'border-radius:4px',
      'cursor:pointer',
      'font-family:Georgia,serif',
      'font-size:0.75rem',
      'font-weight:400',
      'letter-spacing:0',
      'text-transform:none',
      'opacity:1',
      'transition:background 0.2s,border-color 0.2s',
      'box-shadow:0 1px 4px rgba(0,0,0,0.1)',
    ].join(';');

    btn.addEventListener('mouseenter', () => {
      btn.style.background = '#f5f5f5';
      btn.style.borderColor = '#999';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.background = '#fff';
      btn.style.borderColor = '#ccc';
    });

    btn.addEventListener('click', async () => {
      btn.disabled = true;
      btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Fetching…';
      try {
        const resp = await fetch(rawUrl);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const text = await resp.text();
        await navigator.clipboard.writeText(text);
        btn.innerHTML = '<i class="bi bi-check2"></i> Copied!';
        btn.style.color = '#198754';
        btn.style.borderColor = 'rgba(25,135,84,0.4)';
      } catch (err) {
        console.error('copy-markdown: failed', err);
        btn.innerHTML = '<i class="bi bi-x-circle"></i> Failed';
        btn.style.color = '#dc3545';
        btn.style.borderColor = 'rgba(220,53,69,0.4)';
      }
      setTimeout(() => {
        btn.innerHTML = '<i class="bi bi-clipboard"></i> Copy Markdown';
        btn.style.color = '#B5621E';
        btn.style.borderColor = 'rgba(181,98,30,0.35)';
        btn.disabled = false;
      }, 2500);
    });

    return btn;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => document.body.appendChild(createButton()));
  } else {
    document.body.appendChild(createButton());
  }
})();
