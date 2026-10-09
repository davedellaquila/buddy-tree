#!/usr/bin/env python3
"""Build the Project Buddy dashboard (index.html) from buddies.json + the view fragments.

Usage: build.py   (run from ~/workspace/projects/buddy-tree)
Reads:  buddies.json, buddy-tree.html (style + the three view fragments)
Writes: index.html
"""
import json
import re

HERE = "/home/hatch/workspace/projects/buddy-tree"

ROOT_ORDER = [
    "project-buddy",
    "personal-buddy", "family-buddy", "property-buddy", "finance-buddy", "work-buddy",
    "car-buddy", "tv-buddy", "news-buddy", "wisdom-buddy", "birthday-buddy",
    "job-buddy", "reminder-buddy", "housing-buddy", "zen-buddy", "school-buddy",
    "document-buddy", "dream-buddy", "tech-buddy", "feedback-buddy",
    "scaffold-buddy", "buddy-suite",
]

NEW_CSS = """
/* ---- app shell ---- */
body{padding:0}
.app{display:flex;min-height:100vh;align-items:stretch}
#sidebar{width:308px;flex:0 0 308px;background:#0d1117;border-right:1px solid #21262d;
  padding:22px 14px 32px;position:sticky;top:0;height:100vh;overflow-y:auto}
#main{flex:1;min-width:0;padding:36px 32px 80px}
.brand{padding:0 8px 14px}
.brand .eyebrow{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#8b949e}
.brand h1{font-size:22px;margin:4px 0 0}
.nav-sec{margin-top:18px}
.nav-sec>h3{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#8b949e;
  margin:0 8px 8px;display:flex;align-items:center;gap:8px}
#attn-pill{background:#1f6feb;color:#fff;font-size:11px;font-weight:700;border-radius:999px;
  padding:1px 8px;letter-spacing:0;text-transform:none}
#attn-pill.zero{background:#21262d;color:#8b949e}
.navbtn{display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:none;border:0;
  color:#e6edf3;font:inherit;font-size:14px;padding:8px 10px;border-radius:8px;cursor:pointer}
.navbtn:hover{background:#161b22}
.navbtn.sel{background:#1c2330;box-shadow:inset 2px 0 0 #1f6feb}
.navbtn .nic{width:20px;text-align:center;color:#8b949e}
.brow{display:flex;align-items:center;gap:8px;width:100%;text-align:left;background:none;border:0;
  color:#e6edf3;font:inherit;font-size:13.5px;padding:6px 10px 6px 8px;border-radius:8px;cursor:pointer}
.brow:hover{background:#161b22}
.brow.sel{background:#1c2330;box-shadow:inset 2px 0 0 #1f6feb}
.bdot{width:8px;height:8px;border-radius:50%;background:#1f6feb;flex:0 0 8px;visibility:hidden}
.brow.has-unseen .bdot{visibility:visible}
.bname{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bkind{font-size:10px;color:#6e7681;letter-spacing:.5px;text-transform:uppercase}
/* ---- buddy homepage ---- */
.bp-wrap{max-width:880px;margin:0 auto;padding:6px 4px}
.bp-crumb{font-size:12.5px;color:#8b949e;margin-bottom:10px}
.bp-crumb b{color:#e6edf3;font-weight:600}
.bp-top{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.bp-name{font-size:32px;font-weight:700;margin:0;outline:none;border-bottom:2px dashed transparent;
  padding-bottom:2px;min-width:120px}
.bp-name:hover{border-bottom-color:#30363d}
.bp-name:focus{border-bottom-color:#1f6feb;background:#0f1a2e}
.bp-tagline{color:#8b949e;font-size:15px;margin:8px 0 0}
.bp-sec{margin-top:30px}
.bp-sec>h3{font-size:13px;letter-spacing:1.2px;text-transform:uppercase;color:#8b949e;margin:0 0 12px}
.bp-mission{font-size:15.5px;line-height:1.7;background:#161b22;border:1px solid #30363d;
  border-radius:12px;padding:16px 18px;margin:0}
.art-row{display:flex;align-items:center;gap:14px;padding:11px 14px;border:1px solid #21262d;
  border-radius:12px;margin-bottom:10px;text-decoration:none;color:inherit;background:#0d1117}
.art-row:hover{border-color:#1f6feb;background:#11161d}
.art-ic{width:38px;height:38px;border-radius:10px;background:#161b22;border:1px solid #30363d;
  display:flex;align-items:center;justify-content:center;flex:0 0 38px;color:#8b949e}
.art-label{font-weight:650;font-size:14.5px}
.art-sub{font-size:12.5px;color:#8b949e;margin-top:2px}
.art-go{margin-left:auto;color:#6e7681;font-size:18px}
.attn{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:13px 15px;
  margin-bottom:10px;display:flex;gap:12px;align-items:flex-start}
.attn.unseen{border-color:#1f6feb;background:#0d1a30}
.attn .adot{width:9px;height:9px;border-radius:50%;background:#1f6feb;margin-top:6px;flex:0 0 9px;visibility:hidden}
.attn.unseen .adot{visibility:visible}
.attn-body{flex:1;min-width:0}
.attn-text{font-size:14.5px;line-height:1.5}
.attn-date{font-size:12px;color:#8b949e;margin-top:5px}
.seenbtn{flex:0 0 auto;background:#21262d;border:1px solid #30363d;color:#e6edf3;font:inherit;
  font-size:12.5px;padding:6px 12px;border-radius:999px;cursor:pointer}
.seenbtn:hover{border-color:#1f6feb}
.attn.seen{opacity:.55}
.attn.seen .seenbtn{visibility:hidden}
.attn-all{margin-top:6px}
.notes{width:100%;min-height:120px;background:#0d1117;border:1px solid #30363d;border-radius:12px;
  color:#e6edf3;font:inherit;font-size:14.5px;line-height:1.6;padding:13px 15px;resize:vertical}
.notes:focus{outline:none;border-color:#1f6feb}
.fineprint{font-size:12.5px;color:#6e7681;margin-top:8px;line-height:1.5}
.bp-empty{color:#8b949e;font-size:14px}
.bp-tree-wrap{border:1px solid #21262d;border-radius:12px;padding:18px 8px;background:#0d1117;overflow:hidden}
.linkbtn{background:none;border:0;color:#1f6feb;font:inherit;font-size:12.5px;cursor:pointer;padding:0}
.linkbtn:hover{text-decoration:underline}
@media (max-width:900px){
  .app{flex-direction:column}
  #sidebar{width:auto;flex:none;position:static;height:auto;max-height:46vh;border-right:0;border-bottom:1px solid #21262d}
  #main{padding:24px 18px 64px}
}
@media (prefers-color-scheme:light){
  #sidebar{background:#f6f8fa;border-right-color:#d0d7de}
  .navbtn,.brow{color:#1f2328}
  .navbtn:hover,.brow:hover{background:#eaeef2}
  .navbtn.sel,.brow.sel{background:#ddf4ff}
  .brand .eyebrow,.nav-sec>h3,.bkind,.bp-crumb,.bp-tagline,.attn-date,.art-sub,.fineprint,.bp-empty{color:#57606a}
  .bp-crumb b{color:#1f2328}
  .bp-mission{background:#f6f8fa;border-color:#d0d7de}
  .art-row{background:#fff;border-color:#d0d7de}
  .art-row:hover{background:#f6f8fa}
  .art-ic{background:#f6f8fa;border-color:#d0d7de;color:#57606a}
  .attn{background:#f6f8fa;border-color:#d0d7de}
  .attn.unseen{background:#ddf4ff;border-color:#1f6feb}
  .notes{background:#fff;border-color:#d0d7de;color:#1f2328}
  .seenbtn{background:#eaeef2;border-color:#d0d7de;color:#1f2328}
  .bp-name:focus{background:#ddf4ff}
}
"""

ICON_DOC = ('<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
            ' stroke-width="1.5"><path d="M4 1.5h5.5L12.5 4.5v10h-8.5z"/>'
            '<path d="M9.5 1.5v3h3M6 8.5h4M6 11h4"/></svg>')
ICON_REPO = ('<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
             ' stroke-width="1.5"><rect x="2" y="2" width="12" height="12" rx="2"/>'
             '<path d="M5.5 5.5l-2 2 2 2M10.5 5.5l2 2-2 2"/></svg>')
ICON_LINK = ('<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
             ' stroke-width="1.5"><path d="M6.5 9.5l3-3M7.5 5.5l1.5-1.5a2.5 2.5 0 013.5 3.5L11 9"/>'
             '<path d="M8.5 10.5L7 12a2.5 2.5 0 01-3.5-3.5L5 7"/></svg>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    data = json.load(open(f"{HERE}/buddies.json"))
    buddies = data["buddies"]
    frag = open(f"{HERE}/buddy-tree.html").read()

    style = frag.split("<style>", 1)[1].split("</style>", 1)[0]
    vt = frag.split('<div id="view-tree"', 1)[1].split('<div id="view-projects"', 1)[0]
    vp = frag.split('<div id="view-projects"', 1)[1].split('<div id="view-manifest"', 1)[0]
    vm = frag.split('<div id="view-manifest"', 1)[1].split('<footer class="legend">', 1)[0]
    vt = '<div id="view-tree"' + vt.replace('class="view active"', 'class="view"', 1)
    vp = '<div id="view-projects"' + vp
    vm = '<div id="view-manifest"' + vm

    buddies_js = json.dumps(buddies)
    order_js = json.dumps(ROOT_ORDER)

    js = """const BUDDIES = BUDDIES_JSON;
const ROOT_ORDER = ORDER_JSON;
const byId = Object.fromEntries(BUDDIES.map(b => [b.id, b]));
const kidsOf = {};
BUDDIES.forEach(b => { const p = b.parent || '__root'; (kidsOf[p] = kidsOf[p] || []).push(b); });
const LS_KEY = 'buddyTree.v3';
let S = {seen:{}, notes:{}, names:{}, sel:'view:tree'};
try { Object.assign(S, JSON.parse(localStorage.getItem(LS_KEY) || '{}')); } catch(e) {}
function save(){ localStorage.setItem(LS_KEY, JSON.stringify(S)); }
function dispName(b){ return S.names[b.id] || b.name; }
function unseenItems(b){ return (b.attention || []).filter(a => !S.seen[a.id]); }
function descUnseen(id){
  let n = 0;
  (function walk(x){ const b = byId[x]; if(!b) return; n += unseenItems(b).length;
    (kidsOf[x] || []).forEach(c => walk(c.id)); })(id);
  return n;
}
function totalUnseen(){ return ROOT_ORDER.reduce((n,id) => n + (byId[id] && byId[id].parent === null ? descUnseen(id) : 0), 0); }
function crumb(id){
  const chain = []; let b = byId[id];
  while (b) { chain.unshift(b); b = b.parent ? byId[b.parent] : null; }
  return chain.map((c,i) => i < chain.length-1
    ? '<a href="#" data-goto="'+c.id+'" style="color:#8b949e">'+escHtml(dispName(c))+'</a>'
    : '<b>'+escHtml(dispName(c))+'</b>').join(' <span style="color:#6e7681">/</span> ');
}
function escHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function renderNav(){
  const views = [['tree','Tree','▦'],['projects','Projects','☰'],['manifest','Manifest','✓']];
  document.getElementById('view-nav').innerHTML = views.map(([v,l,ic]) =>
    '<button class="navbtn'+(S.sel==='view:'+v?' sel':'')+'" data-view="'+v+'"><span class="nic">'+ic+'</span>'+l+'</button>').join('');
  let h = '';
  function row(id, depth){
    const b = byId[id]; if(!b) return;
    const un = descUnseen(id);
    const kind = b.kind === 'root' ? 'root' : (b.parent === 'project-buddy' ? 'direct' : b.kind);
    h += '<button class="brow'+(S.sel==='buddy:'+id?' sel':'')+(un?' has-unseen':'')+'" data-buddy="'+id+'"'
      + ' style="padding-left:'+(8+depth*16)+'px" title="'+escHtml(b.tagline||'')+'">'
      + '<span class="bdot"></span><span class="bname">'+escHtml(dispName(b))+'</span>'
      + '<span class="bkind">'+kind+'</span></button>';
    (kidsOf[id] || []).forEach(c => row(c.id, depth+1));
  }
  ROOT_ORDER.forEach(id => row(id, 0));
  document.getElementById('buddy-nav').innerHTML = h;
  const t = totalUnseen();
  const pill = document.getElementById('attn-pill');
  pill.textContent = t; pill.classList.toggle('zero', t === 0);
}
function artRow(icon, label, sub, url){
  return '<a class="art-row" href="'+url+'" target="_blank" rel="noopener">'
    + '<span class="art-ic">'+icon+'</span>'
    + '<span><span class="art-label">'+escHtml(label)+'</span><div class="art-sub">'+escHtml(sub)+'</div></span>'
    + '<span class="art-go">→</span></a>';
}
function renderBuddy(id){
  const b = byId[id]; if(!b) return;
  const items = (b.attention || []).slice().sort((x,y) => (S.seen[x.id]?1:0) - (S.seen[y.id]?1:0));
  let arts = '';
  if (b.brief) arts += artRow(ICON_DOC, 'Product Brief', 'The canonical mission & intent — Google Doc', b.brief);
  if (b.repo) arts += artRow(ICON_REPO, 'GitHub Repo', 'davedellaquila/'+b.repo+' (private)', 'https://github.com/davedellaquila/'+b.repo);
  (b.docs || []).forEach(d => { arts += artRow(ICON_LINK, d.label, 'Related document — Google Doc', d.url); });
  if (!arts) arts = '<p class="bp-empty">No artifacts yet — the drill adds the brief and repo here when they exist.</p>';
  let attn = '';
  if (!items.length) attn = '<p class="bp-empty">Nothing needs your attention right now.</p>';
  else {
    attn = items.map(a => {
      const seen = !!S.seen[a.id];
      return '<div class="attn'+(seen?' seen':' unseen')+'" data-attn="'+a.id+'"><span class="adot"></span>'
        + '<div class="attn-body"><div class="attn-text">'+escHtml(a.text)+'</div>'
        + '<div class="attn-date">Asked '+a.date+'</div></div>'
        + '<button class="seenbtn" data-seen="'+a.id+'">Mark seen</button></div>';
    }).join('');
    const un = items.filter(a => !S.seen[a.id]).length;
    if (un > 1) attn += '<div class="attn-all"><button class="seenbtn" data-seen-all="'+id+'">Mark all seen</button></div>';
  }
  document.getElementById('buddy-home').innerHTML =
    '<div class="bp-wrap">'
    + '<div class="bp-crumb">'+crumb(id)+'</div>'
    + '<div class="bp-top"><h2 class="bp-name" id="bp-name" contenteditable="true" spellcheck="false" data-buddy="'+id+'">'+escHtml(dispName(b))+'</h2>'
    + '<span class="status '+b.statusClass+'">'+escHtml(b.status)+'</span></div>'
    + '<p class="bp-tagline">'+escHtml(b.tagline||'')+'</p>'
    + '<div class="bp-sec"><h3>What it does</h3><p class="bp-mission">'+escHtml(b.mission)+'</p>'
    + '<p class="fineprint">The mission is the brief\u2019s executive summary — tweak it through the buddy\u2019s chat thread and it updates everywhere.</p></div>'
    + (id === 'project-buddy'
        ? '<div class="bp-sec"><h3>The Buddy Tree</h3><div class="bp-tree-wrap"></div>'
          + '<p class="fineprint"><button class="linkbtn" data-view="tree">Open the tree as its own view \u2192</button></p></div>'
        : '')
    + '<div class="bp-sec"><h3>Artifacts</h3>'+arts+'</div>'
    + '<div class="bp-sec"><h3>Needs your attention</h3>'+attn+'</div>'
    + '<div class="bp-sec"><h3>Notes</h3><textarea class="notes" id="bp-notes" placeholder="Scratch pad for this buddy\u2026">'+escHtml(S.notes[id]||'')+'</textarea>'
    + '<p class="fineprint">Saved on this device only.</p></div>'
    + '</div>';
  const nm = document.getElementById('bp-name');
  nm.addEventListener('keydown', e => { if (e.key === 'Enter'){ e.preventDefault(); nm.blur(); } });
  nm.addEventListener('blur', () => {
    const v = nm.textContent.trim();
    if (v && v !== dispName(b)) { S.names[id] = v; }
    else { delete S.names[id]; }
    save(); renderNav();
  });
  const nt = document.getElementById('bp-notes');
  let t = null;
  nt.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { S.notes[id] = nt.value; save(); }, 400); });
  if (id === 'project-buddy') {
    const tw = document.querySelector('#buddy-home .bp-tree-wrap');
    const src = document.getElementById('view-tree');
    if (tw && src) tw.innerHTML = src.innerHTML;
  }
}
function show(sel){
  S.sel = sel; save();
  document.querySelectorAll('#main .view').forEach(v => v.classList.remove('active'));
  if (sel.startsWith('view:')) {
    document.getElementById('view-' + sel.slice(5)).classList.add('active');
  } else {
    document.getElementById('view-buddy').classList.add('active');
    renderBuddy(sel.slice(6));
  }
  renderNav();
  document.getElementById('main').scrollTop = 0;
  window.scrollTo(0,0);
}
document.addEventListener('click', e => {
  const vb = e.target.closest('[data-view]');
  if (vb) { show('view:' + vb.dataset.view); return; }
  const bb = e.target.closest('[data-buddy]');
  if (bb) { show('buddy:' + bb.dataset.buddy); return; }
  const sb = e.target.closest('[data-seen]');
  if (sb) { S.seen[sb.dataset.seen] = Date.now(); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const sa = e.target.closest('[data-seen-all]');
  if (sa) { (byId[sa.dataset.seenAll].attention || []).forEach(a => S.seen[a.id] = Date.now()); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const gt = e.target.closest('[data-goto]');
  if (gt) { e.preventDefault(); show('buddy:' + gt.dataset.goto); return; }
});
show(S.sel || 'view:tree');
"""
    js = js.replace("BUDDIES_JSON", buddies_js).replace("ORDER_JSON", order_js)
    js = js.replace("ICON_DOC", "'" + ICON_DOC.replace("'", "\\'") + "'")
    js = js.replace("ICON_REPO", "'" + ICON_REPO.replace("'", "\\'") + "'")
    js = js.replace("ICON_LINK", "'" + ICON_LINK.replace("'", "\\'") + "'")

    out = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Buddy Tree — Project Buddy dashboard</title>
<style>
""" + style + NEW_CSS + """
</style>
</head>
<body>
<div class="app">
<aside id="sidebar">
  <div class="brand"><div class="eyebrow">Project Buddy &middot; macro view</div><h1>The Buddy Tree</h1></div>
  <div class="nav-sec"><h3>Views</h3><div id="view-nav"></div></div>
  <div class="nav-sec"><h3>Buddies <span id="attn-pill" class="zero">0</span></h3><div id="buddy-nav"></div></div>
</aside>
<main id="main">
""" + vt + vp + vm + """
<section id="view-buddy" class="view"><div id="buddy-home"></div></section>
</main>
</div>
<script>
""" + js + """
</script>
</body>
</html>
"""
    open(f"{HERE}/index.html", "w").write(out)
    print("wrote index.html", len(out), "bytes")


if __name__ == "__main__":
    build()
