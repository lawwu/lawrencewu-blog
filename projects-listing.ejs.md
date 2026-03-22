```{=html}
<div class="proj-grid">

<% for (const item of items) { %>
<%
  const d = new Date(item.date);
  const dateStr = d.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
  const stars = item.stars || 0;
  const lang = item['project_lang'] || '';
  const githubUrl = item['github_url'] || item.path;
  const projectUrl = item.path;
  const cleanDesc = item.description ? item.description.replace(/<!--[\s\S]*?-->/g, '').trim() : '';
%>

<article class="proj-card" <%- metadataAttrs(item) %>>
  <% if (item.image) { %>
  <a href="<%- projectUrl %>" class="proj-image-link">
    <img src="<%- item.image %>" alt="<%- item.title %>" class="proj-image" loading="lazy">
  </a>
  <% } %>

  <div class="proj-body">
    <div class="proj-header">
      <h2 class="proj-title">
        <a href="<%- projectUrl %>" class="proj-title-link"><%- item.title %></a>
      </h2>
      <div class="proj-meta">
        <% if (stars > 0) { %>
        <span class="proj-stars">★ <%- stars %></span>
        <% } %>
        <% if (lang) { %>
        <span class="proj-lang"><%- lang %></span>
        <% } %>
        <span class="proj-date"><%- dateStr %></span>
      </div>
    </div>

    <% if (cleanDesc) { %>
    <p class="proj-desc"><%- cleanDesc %></p>
    <% } %>

    <div class="proj-footer">
      <% if (item.categories && item.categories.length > 0) { %>
      <div class="proj-categories">
        <% for (const cat of item.categories.filter(c => c !== 'project')) { %>
        <a class="plc-category listing-category quarto-category"
           href="#"
           onclick="window.quartoListingCategory && window.quartoListingCategory('<%- cat %>'); return false;"><%- cat %></a>
        <% } %>
      </div>
      <% } %>
      <a href="<%- githubUrl %>" class="proj-gh-link" target="_blank" rel="noopener">GitHub ↗</a>
    </div>
  </div>
</article>

<% } %>

</div>
```

