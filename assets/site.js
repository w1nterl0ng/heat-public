(() => {
  const releaseUrl = "releases/latest.json";
  fetch(releaseUrl).then(r => r.ok ? r.json() : Promise.reject()).then(release => {
    document.querySelectorAll("[data-release-version]").forEach(el => el.textContent = `V${release.version} / BUILD ${release.build}`);
    document.querySelectorAll("[data-release-links]").forEach(el => {
      el.innerHTML = "";
      [["MACOS", release.assets?.mac], ["WINDOWS", release.assets?.windows]].forEach(([label, url]) => {
        if (!url) return;
        const a = document.createElement("a"); a.className = "button light"; a.href = url; a.textContent = `DOWNLOAD ${label}`; el.append(a);
      });
    });
  }).catch(() => document.querySelectorAll("[data-release-version]").forEach(el => el.textContent = "LATEST RELEASE AVAILABLE"));

  const grid = document.querySelector("#track-grid");
  if (!grid) return;
  const search = document.querySelector("#track-search");
  const filters = document.querySelector("#filters");
  const empty = document.querySelector("#track-empty");
  const count = document.querySelector("#track-count");
  let tracks = [], active = "All tracks";
  const html = (value) => String(value ?? "").replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;" }[c]));
  const tagsFor = () => ["All tracks", ...new Set(tracks.flatMap(t => [...(t.tags || []), ...(t.expansions || [])]))].slice(0, 9);
  function renderFilters() {
    filters.innerHTML = tagsFor().map(tag => `<button class="filter" data-filter="${html(tag)}" aria-pressed="${tag === active}">${html(tag)}</button>`).join("");
    filters.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { active = b.dataset.filter; render(); }));
  }
  function render() {
    const term = search.value.trim().toLowerCase();
    const shown = tracks.filter(t => {
      const haystack = [t.name,t.country,t.designer,...(t.tags || []),...(t.expansions || [])].join(" ").toLowerCase();
      return (!term || haystack.includes(term)) && (active === "All tracks" || [...(t.tags || []), ...(t.expansions || [])].includes(active));
    });
    count.textContent = `${shown.length} OF ${tracks.length} TRACK${tracks.length === 1 ? "" : "S"}`;
    grid.innerHTML = shown.map(t => `<article class="track-card" id="track-${html(t.id)}">
      <img src="${html(t.preview)}" alt="Preview map for ${html(t.name)}" loading="lazy">
      <div><p class="eyebrow">${html(t.country)}</p><h2>${html(t.name)}</h2>
      <p class="track-meta">${t.spaces} SPACES · ${t.corners} CORNERS · ${t.laps} LAPS</p>
      <div class="tags">${[...(t.tags || []), ...(t.expansions || [])].map(x => `<span class="tag">${html(x)}</span>`).join("")}</div>
      <p class="track-meta">CREATED BY ${html(t.designer)}<br>VERSION ${html(t.version)} · ${html(t.size)}</p>
      <a class="button red" href="${html(t.download)}">DOWNLOAD .ZIP</a></div></article>`).join("");
    empty.hidden = shown.length > 0;
    renderFilters();
  }
  document.querySelector("#clear-filters").addEventListener("click", () => { search.value = ""; active = "All tracks"; render(); });
  search.addEventListener("input", render);
  fetch("data/tracks.json").then(r => r.ok ? r.json() : Promise.reject()).then(data => { tracks = data.tracks || []; render(); })
    .catch(() => { count.textContent = "TRACK LIBRARY IS BEING PREPARED"; empty.hidden = false; });
})();
