```{=html}
<div class="quarto-listing-container-custom">
<div class="list quarto-listing-custom" id="quarto-listing-listing">

<% for (const item of items) { %>
<%
  const d = new Date(item.date);
  const dateStr = d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const isLink = item.categories && item.categories.includes('linkblog');
  const isQuote = item.categories && item.categories.includes('quote');
  const isProject = item.categories && item.categories.includes('project');
  // Pass description through as-is — <!-- desc(...) --> placeholders are resolved by
  // scripts/resolve-descriptions.py after render.
  const cleanDesc = item.description || '';
%>

<% if (isLink) { %>
<article class="plc-entry plc-link-entry" <%- metadataAttrs(item) %>>

  <div class="plc-meta">
    <span class="plc-type-badge plc-type-link">link</span>
    <time class="plc-date listing-date" datetime="<%- item.date %>"><%- dateStr %></time>
  </div>

  <div class="plc-body">
    <div class="plc-content">
      <h2 class="plc-title listing-title">
        <a href="<%- item.path %>" class="plc-title-link"><%- item.title %> &#x2197;</a>
      </h2>

      <% if (cleanDesc) { %>
      <p class="plc-description listing-description"><%- cleanDesc %></p>
      <% } %>

      <% if (item.categories && item.categories.length > 0) { %>
      <div class="plc-categories">
        <% for (const cat of item.categories) { %>
        <a class="plc-category listing-category quarto-category"
           href="#"
           onclick="window.quartoListingCategory && window.quartoListingCategory('<%- cat %>'); return false;"><%- cat %></a>
        <% } %>
      </div>
      <% } %>
    </div>
  </div>

</article>
<% } else if (isProject) { %>
<article class="plc-entry plc-project-entry" <%- metadataAttrs(item) %>>

  <div class="plc-meta">
    <span class="plc-type-badge plc-type-project">project</span>
    <time class="plc-date listing-date" datetime="<%- item.date %>"><%- dateStr %></time>
  </div>

  <div class="plc-body">
    <div class="plc-content">
      <h2 class="plc-title listing-title">
        <a href="<%- item.path %>" class="plc-title-link plc-project-title"><%- item.title %></a>
      </h2>

      <% if (cleanDesc) { %>
      <p class="plc-description listing-description"><%- cleanDesc %></p>
      <% } %>

      <% if (item.categories && item.categories.length > 0) { %>
      <div class="plc-categories">
        <% for (const cat of item.categories) { %>
        <a class="plc-category listing-category quarto-category"
           href="#"
           onclick="window.quartoListingCategory && window.quartoListingCategory('<%- cat %>'); return false;"><%- cat %></a>
        <% } %>
      </div>
      <% } %>
    </div>
  </div>

</article>
<% } else if (isQuote) { %>
<article class="plc-entry plc-quote-entry" <%- metadataAttrs(item) %>>

  <div class="plc-meta">
    <span class="plc-type-badge plc-type-quote">quote</span>
    <time class="plc-date listing-date" datetime="<%- item.date %>"><%- dateStr %></time>
  </div>

  <div class="plc-body">
    <div class="plc-content">
      <% if (cleanDesc) { %>
      <blockquote class="plc-quote-block"><%- cleanDesc %></blockquote>
      <% } %>
      <p class="plc-quote-attribution">
        — <a href="<%- item.path %>" class="plc-title-link"><%- item.title %></a>
      </p>
      <% if (item.categories && item.categories.length > 0) { %>
      <div class="plc-categories">
        <% for (const cat of item.categories) { %>
        <a class="plc-category listing-category quarto-category"
           href="#"
           onclick="window.quartoListingCategory && window.quartoListingCategory('<%- cat %>'); return false;"><%- cat %></a>
        <% } %>
      </div>
      <% } %>
    </div>
  </div>

</article>
<% } else { %>
<article class="plc-entry" <%- metadataAttrs(item) %>>

  <div class="plc-meta">
    <time class="plc-date listing-date" datetime="<%- item.date %>"><%- dateStr %></time>
    <% if (item['reading-time']) { %>
    <span class="plc-sep">·</span>
    <span class="plc-reading-time listing-reading-time"><%- item['reading-time'] %></span>
    <% } %>
  </div>

  <div class="plc-body">
    <% if (item.image) { %>
    <a href="<%- item.path %>" class="plc-image-link" tabindex="-1" aria-hidden="true">
      <img src="<%- item.image %>" alt="" class="plc-image" loading="lazy">
    </a>
    <% } %>

    <div class="plc-content">
      <h2 class="plc-title listing-title">
        <a href="<%- item.path %>" class="plc-title-link"><%- item.title %></a>
      </h2>

      <% if (cleanDesc) { %>
      <p class="plc-description listing-description"><%- cleanDesc %></p>
      <% } %>

      <% if (item.categories && item.categories.length > 0) { %>
      <div class="plc-categories">
        <% for (const cat of item.categories) { %>
        <a class="plc-category listing-category quarto-category"
           href="#"
           onclick="window.quartoListingCategory && window.quartoListingCategory('<%- cat %>'); return false;"><%- cat %></a>
        <% } %>
      </div>
      <% } %>
    </div>
  </div>

</article>
<% } %>

<% } %>

</div>
</div>
```

