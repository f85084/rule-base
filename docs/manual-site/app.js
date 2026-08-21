(() => {
  "use strict";

  const state = {
    manifest: null,
    documents: new Map(),
    sources: new Map(),
    currentId: null,
  };

  const $ = (selector) => document.querySelector(selector);
  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

  function flattenDocuments(manifest) {
    return manifest.groups.flatMap((group) => group.documents.map((doc) => ({ ...doc, groupId: group.id, groupTitle: group.title })));
  }

  function sourceRootUrl() {
    return new URL("../../", window.location.href);
  }

  function sourceUrl(source) {
    return new URL(source, sourceRootUrl()).href;
  }

  function normalizedRepoPath(sourcePath, target) {
    const base = sourcePath.split("/").slice(0, -1);
    for (const segment of target.split("/")) {
      if (!segment || segment === ".") continue;
      if (segment === "..") base.pop();
      else base.push(segment);
    }
    return base.join("/");
  }

  function linkTarget(target, sourcePath) {
    const raw = target.trim();
    if (!raw || raw.startsWith("#")) return { href: raw || "#", external: false };
    if (/^(https?:|mailto:)/i.test(raw)) return { href: raw, external: true };
    if (raw.startsWith("/")) return { href: raw, external: false };
    const path = normalizedRepoPath(sourcePath, raw.split("#")[0]);
    if (path.startsWith("project-docs/") || path.startsWith("/project-docs/")) {
      return { href: "#source-not-mounted", external: false, unavailable: true };
    }
    return { href: `/${path}${raw.includes("#") ? `#${raw.split("#").slice(1).join("#")}` : ""}`, external: false };
  }

  function renderInline(value, sourcePath) {
    let html = escapeHtml(value);
    html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, target) => {
      const link = linkTarget(target, sourcePath);
      const className = link.unavailable ? " class=\"source-link-unavailable\" title=\"本機原型未掛載 repo 外來源\"" : "";
      const external = link.external ? " target=\"_blank\" rel=\"noreferrer\"" : "";
      return `<a href=\"${escapeHtml(link.href)}\"${className}${external}>${label}</a>`;
    });
    return html.replace(/  \n/g, "<br>");
  }

  function slug(value) {
    return value.toLowerCase().replace(/[^\w\-\u4e00-\u9fff ]+/g, "").trim().replace(/\s+/g, "-");
  }

  function isTableSeparator(line) {
    return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
  }

  function tableCells(line, sourcePath) {
    const trimmed = line.trim().replace(/^\|/, "").replace(/\|$/, "");
    return trimmed.split("|").map((cell) => renderInline(cell.trim(), sourcePath));
  }

  function renderMarkdown(markdown, sourcePath) {
    const lines = markdown.replaceAll("\r\n", "\n").split("\n");
    const out = [];
    let index = 0;

    while (index < lines.length) {
      const line = lines[index];
      if (!line.trim()) { index += 1; continue; }

      if (/^```/.test(line)) {
        const language = line.slice(3).trim();
        const code = [];
        index += 1;
        while (index < lines.length && !/^```/.test(lines[index])) { code.push(lines[index]); index += 1; }
        if (index < lines.length) index += 1;
        out.push(`<pre><code class="language-${escapeHtml(language)}">${escapeHtml(code.join("\n"))}</code></pre>`);
        continue;
      }

      const heading = line.match(/^(#{1,4})\s+(.+?)\s*#*$/);
      if (heading) {
        const level = heading[1].length;
        const text = heading[2];
        out.push(`<h${level} id="${escapeHtml(slug(text))}">${renderInline(text, sourcePath)}</h${level}>`);
        index += 1;
        continue;
      }

      if (index + 1 < lines.length && line.includes("|") && isTableSeparator(lines[index + 1])) {
        const header = tableCells(line, sourcePath);
        index += 2;
        const rows = [];
        while (index < lines.length && lines[index].includes("|") && lines[index].trim()) {
          rows.push(tableCells(lines[index], sourcePath));
          index += 1;
        }
        out.push(`<div class="table-scroll"><table><thead><tr>${header.map((cell) => `<th>${cell}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
        continue;
      }

      if (/^\s*[-*]\s+/.test(line) || /^\s*\d+\.\s+/.test(line)) {
        const ordered = /^\s*\d+\.\s+/.test(line);
        const items = [];
        const pattern = ordered ? /^\s*\d+\.\s+(.*)$/ : /^\s*[-*]\s+(.*)$/;
        while (index < lines.length) {
          const match = lines[index].match(pattern);
          if (!match) break;
          items.push(match[1]);
          index += 1;
        }
        const tag = ordered ? "ol" : "ul";
        out.push(`<${tag}>${items.map((item) => `<li>${renderInline(item, sourcePath)}</li>`).join("")}</${tag}>`);
        continue;
      }

      if (/^>\s?/.test(line)) {
        const quote = [];
        while (index < lines.length && /^>\s?/.test(lines[index])) { quote.push(lines[index].replace(/^>\s?/, "")); index += 1; }
        out.push(`<blockquote>${quote.map((item) => renderInline(item, sourcePath)).join("<br>")}</blockquote>`);
        continue;
      }

      if (/^\s*([-*_])\s*\1\s*\1/.test(line)) { out.push("<hr>"); index += 1; continue; }

      const paragraph = [line];
      index += 1;
      while (index < lines.length && lines[index].trim() &&
        !/^```/.test(lines[index]) && !/^(#{1,4})\s+/.test(lines[index]) &&
        !/^\s*[-*]\s+/.test(lines[index]) && !/^\s*\d+\.\s+/.test(lines[index]) &&
        !/^>\s?/.test(lines[index])) {
        paragraph.push(lines[index]);
        index += 1;
      }
      out.push(`<p>${paragraph.map((item) => renderInline(item, sourcePath)).join("\n")}</p>`);
    }
    return out.join("\n");
  }

  function section(markdown, heading) {
    const lines = markdown.replaceAll("\r\n", "\n").split("\n");
    const start = lines.findIndex((line) => line.trim() === `## ${heading}`);
    if (start === -1) return "";
    const body = [];
    for (let index = start + 1; index < lines.length; index += 1) {
      if (/^##\s+/.test(lines[index])) break;
      body.push(lines[index]);
    }
    return body.join("\n").trim();
  }

  function numberedSteps(markdown) {
    const lines = markdown.split("\n");
    const steps = [];
    let current = null;
    for (const line of lines) {
      const match = line.match(/^\s*(\d+)\.\s+(.*)$/);
      if (match) {
        if (current) steps.push(current);
        current = { number: match[1], text: match[2] };
      } else if (current && line.trim() && !/^\s*\*\*/.test(line)) {
        current.text += ` ${line.trim()}`;
      }
    }
    if (current) steps.push(current);
    return steps;
  }

  function splitExpected(text) {
    const match = text.match(/^(.*?)(?:預期結果[：:]\s*)(.*)$/);
    return match ? { action: match[1], expected: match[2] } : { action: text, expected: "來源未提供獨立預期結果／待補。" };
  }

  function renderNav() {
    const nav = $("#site-nav");
    nav.innerHTML = state.manifest.groups.map((group) => {
      const items = group.documents.map((doc) => {
        const isPlaceholder = !doc.source;
        return `<button class="nav-item${isPlaceholder ? " placeholder" : ""}" type="button" data-doc-id="${escapeHtml(doc.id)}" ${isPlaceholder ? "disabled" : ""}>
          <span class="nav-item-title">${escapeHtml(doc.title)}</span>
          <span class="nav-item-meta">${escapeHtml(doc.route || doc.sourceStatus)}</span>
        </button>`;
      }).join("");
      return `<section class="nav-group" data-group="${escapeHtml(group.id)}"><div class="nav-group-title">${escapeHtml(group.title)} <span class="nav-item-meta">${escapeHtml(group.description || "")}</span></div><div class="nav-list">${items}</div></section>`;
    }).join("");
    $("#nav-count").textContent = `${state.documents.size} 頁`;
    nav.querySelectorAll("[data-doc-id]").forEach((button) => button.addEventListener("click", () => loadDocument(button.dataset.docId)));
  }

  function setError(message) {
    const error = $("#load-error");
    error.textContent = message;
    error.hidden = false;
  }

  function clearError() { $("#load-error").hidden = true; }

  function documentMeta(id) { return state.documents.get(id); }

  function renderEmptyDocument(doc) {
    $("#page-title").textContent = doc.title;
    $("#page-category").textContent = doc.category;
    $("#page-lede").textContent = "這是後續擴充的導航入口；canonical source 尚未指定。";
    $("#source-chip").textContent = "source: 來源未提供／待補";
    $("#source-status").textContent = "來源未提供／待補";
    $("#source-status-note").textContent = "此入口只保留分類與待補狀態，未自行補寫 CSP 操作正文。";
    $("#steps").innerHTML = '<div class="empty-source">來源未提供／待補：請在 navigation manifest 指定 canonical Markdown 後再加入頁面。</div>';
    $("#step-count").textContent = "待補";
    $("#completion").innerHTML = '<h3>完成判斷</h3><p>目前沒有可供核對的來源正文。</p>';
    $("#faq").innerHTML = '<details open><summary>常見問題</summary><p>來源未提供／待補。</p></details>';
    $("#source-body").innerHTML = '<p class="empty-source">來源未提供／待補。</p>';
    $("#technical-body").innerHTML = '<div class="empty-source">技術附錄與 business-flow 來源未提供／待補。</div>';
  }

  function renderDocument(id, markdown) {
    const doc = documentMeta(id);
    const general = section(markdown, "一般人員操作");
    const status = section(markdown, "敘述狀態與查核界線");
    const completion = section(markdown, "完成判斷") || section(markdown, "完成確認");
    const faq = section(markdown, "常見問題");
    const sourceSection = section(markdown, "需求與 business-flow 來源");
    const steps = numberedSteps(general || section(markdown, "正常流程"));

    $("#page-title").textContent = doc.title;
    $("#page-category").textContent = doc.category;
    $("#page-lede").textContent = general ? "依 canonical 操作手冊整理入口、步驟與完成判斷；技術內容可在下方收合查看。" : "來源未提供獨立一般人員操作段落；以下保留 canonical 正文並標示待補。";
    $("#source-chip").textContent = `source: ${doc.source}`;
    $("#source-status").textContent = doc.sourceStatus;
    $("#source-status-note").textContent = "current source 已由瀏覽器 fetch；畫面權限、即時連線、外部送達與部署版本仍是 runtime unknown。";
    $("#source-path-link").href = sourceUrl(doc.source);
    $("#source-path-link").target = "_blank";
    $("#source-path-link").rel = "noreferrer";
    $("#source-body").innerHTML = renderMarkdown(markdown, doc.source);
    $("#technical-body").innerHTML = `<div class="markdown-body">${status ? renderMarkdown(status, doc.source) : '<p class="empty-source">來源未提供狀態段落／待補。</p>'}${sourceSection ? renderMarkdown(`## 需求與 business-flow 來源\n${sourceSection}`, doc.source) : '<p class="empty-source">需求與 business-flow 來源段落未提供／待補。</p>'}</div>`;

    $("#step-count").textContent = steps.length ? `${steps.length} 步` : "待補";
    $("#steps").innerHTML = steps.length ? steps.map((step) => {
      const split = splitExpected(step.text);
      return `<article class="step-card"><span class="step-number">${escapeHtml(step.number)}</span><div><p>${renderInline(split.action, doc.source)}</p><p class="expected"><strong>預期結果</strong>　${renderInline(split.expected, doc.source)}</p></div></article>`;
    }).join("") : '<div class="empty-source">來源未提供編號操作步驟／待補；請查看下方 canonical 正文。</div>';

    $("#completion").innerHTML = `<h3>完成確認</h3>${completion ? renderMarkdown(completion, doc.source) : '<p>來源未提供獨立完成確認／待補。</p>'}`;
    $("#faq").innerHTML = faq ? `<details open><summary>常見問題／第一個排錯</summary>${renderMarkdown(faq, doc.source)}</details>` : '<details open><summary>常見問題</summary><p>來源未提供獨立 FAQ／待補；請依來源的「第一個排錯」段落處理。</p></details>';
  }

  async function loadDocument(id) {
    const doc = documentMeta(id);
    if (!doc) return;
    state.currentId = id;
    document.querySelectorAll(".nav-item").forEach((button) => button.setAttribute("aria-current", button.dataset.docId === id ? "page" : "false"));
    clearError();
    if (!doc.source) { renderEmptyDocument(doc); return; }
    try {
      let markdown = state.sources.get(id);
      if (!markdown) {
        const response = await fetch(sourceUrl(doc.source), { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        markdown = await response.text();
        state.sources.set(id, markdown);
      }
      renderDocument(id, markdown);
      $("#main-content").focus({ preventScroll: true });
    } catch (error) {
      setError(`無法載入 canonical source：${doc.source}（${error.message}）。請從 repo root 啟動靜態伺服器。`);
      $("#source-status").textContent = "載入失敗";
    }
  }

  function applySearch(query) {
    const term = query.trim().toLowerCase();
    let visible = 0;
    document.querySelectorAll(".nav-item[data-doc-id]").forEach((button) => {
      const doc = documentMeta(button.dataset.docId);
      const haystack = `${doc.title} ${doc.category} ${doc.route || ""} ${doc.source || ""}`.toLowerCase();
      const match = !term || haystack.includes(term) || (state.sources.get(doc.id) || "").toLowerCase().includes(term);
      button.hidden = !match;
      if (match) visible += 1;
    });
    document.querySelectorAll(".nav-group").forEach((group) => { group.hidden = !Array.from(group.querySelectorAll(".nav-item")).some((item) => !item.hidden); });
    const message = $("#search-message");
    if (!term) { message.hidden = true; return; }
    message.hidden = false;
    message.textContent = visible ? `搜尋「${query}」：${visible} 個導覽項目或已載入正文命中。` : `搜尋「${query}」沒有命中目前已載入的來源；來源未載入的文件不會被複製到本站索引。`;
  }

  async function init() {
    try {
      const response = await fetch("nav.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.manifest = await response.json();
      flattenDocuments(state.manifest).forEach((doc) => state.documents.set(doc.id, doc));
      renderNav();
      $("#search-input").addEventListener("input", (event) => applySearch(event.target.value));
      document.addEventListener("keydown", (event) => {
        if (event.key === "/" && document.activeElement !== $("#search-input")) { event.preventDefault(); $("#search-input").focus(); }
      });
      await loadDocument(state.manifest.defaultDocument);
    } catch (error) {
      setError(`無法載入 navigation manifest（${error.message}）。請從 repo root 啟動靜態伺服器。`);
      $("#nav-count").textContent = "載入失敗";
    }
  }

  init();
})();
