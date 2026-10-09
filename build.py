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
    "car-buddy", "mga-buddy", "ml500-buddy", "tv-buddy", "news-buddy", "wisdom-buddy", "birthday-buddy",
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
#brand-name{outline:none;border-bottom:2px dashed transparent;cursor:text;display:inline-block;min-width:60px}
#brand-name:hover{border-bottom-color:#30363d}
#brand-name:focus{border-bottom-color:#1f6feb}
.brand .bcount{font-size:12.5px;color:#8b949e;margin-top:4px}
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
.bicon{width:20px;flex:0 0 20px;text-align:center;font-size:15px}
.brow.dragging{opacity:.35}
.brow.drop-target{background:#1c2330;box-shadow:inset 0 0 0 2px #1f6feb}
.bp-icon{font-size:38px;line-height:1}
.toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%);background:#161b22;
  border:1px solid #1f6feb;color:#e6edf3;padding:10px 20px;border-radius:999px;
  font-size:14px;z-index:99;box-shadow:0 4px 24px rgba(0,0,0,.5);white-space:nowrap;
  max-width:92vw;overflow:hidden;text-overflow:ellipsis}
.zoombar{display:flex;align-items:center;gap:10px;justify-content:flex-end;
  padding:2px 4px 14px;color:#8b949e;font-size:13px}
.zoombar input{width:170px;accent-color:#1f6feb}
.zoombar .zv{min-width:46px;text-align:right;font-variant-numeric:tabular-nums}
.pstrip{display:flex;gap:10px;overflow-x:auto;padding:2px 2px 6px}
.pstrip a{flex:0 0 auto}
.pstrip img{height:150px;border-radius:10px;border:1px solid #30363d;display:block}
.pstrip img:hover{border-color:#1f6feb}
.node.drop-target{outline:2px solid #1f6feb;outline-offset:3px}
.proj-row.drop-target{background:#1c2330;box-shadow:inset 0 0 0 2px #1f6feb}
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
.proj-row[data-plan]{cursor:pointer}
.proj-row[data-plan]:hover{background:#161b22}
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
  .brow.drop-target{background:#ddf4ff;box-shadow:inset 0 0 0 2px #1f6feb}
  .toast{background:#fff;border-color:#1f6feb;color:#1f2328}
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
  .proj-row[data-plan]:hover{background:#f6f8fa}
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
    plans = json.load(open(f"{HERE}/plans.json"))["plans"]
    plans_js = json.dumps(plans)
    n_buddies = len(buddies)

    plan_rows = "".join(
        f'<div class="proj-row d1" data-plan="{p["id"]}">'
        f'<span class="pname">{esc(p["icon"] + " " + p["name"])}</span>'
        f'<span class="pdesc">{esc(p["desc"][:110])}</span>'
        f'<span class="status {p["statusClass"]}">{esc(p["status"])}</span></div>'
        for p in plans
    )
    vpl = ('<div id="view-plans" class="view"><section class="projects-view" style="margin-top:24px">'
           '<h2>Business Plans</h2>'
           '<p class="sub">BRDs and business plans \u2014 real-world ventures, separate from the buddy-app '
           'software projects. Plans link to the buddies that build them.</p>'
           f'<div class="proj-list">{plan_rows}</div></section></div>')

    js = """const BUDDIES = BUDDIES_JSON;
const ROOT_ORDER = ORDER_JSON;
const byId = Object.fromEntries(BUDDIES.map(b => [b.id, b]));
const PLANS = PLANS_JSON;
const planById = Object.fromEntries(PLANS.map(p => [p.id, p]));
const kidsOf = {};
function effParent(b){ return (S.parents && S.parents[b.id]) || b.parent; }
function buildKids(){
  for (const k in kidsOf) delete kidsOf[k];
  BUDDIES.forEach(b => { const p = effParent(b) || '__root'; (kidsOf[p] = kidsOf[p] || []).push(b); });
}
const LS_KEY = 'buddyTree.v3';
let S = {seen:{}, notes:{}, names:{}, parents:{}, zoom:100, sel:'view:tree'};
try { Object.assign(S, JSON.parse(localStorage.getItem(LS_KEY) || '{}')); } catch(e) {}
S.parents = S.parents || {};
S.zoom = S.zoom || 100;
buildKids();
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
  while (b) { chain.unshift(b); const p = effParent(b); b = p ? byId[p] : null; }
  return chain.map((c,i) => i < chain.length-1
    ? '<a href="#" data-goto="'+c.id+'" style="color:#8b949e">'+escHtml(dispName(c))+'</a>'
    : '<b>'+escHtml(dispName(c))+'</b>').join(' <span style="color:#6e7681">/</span> ');
}
function escHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function renderNav(){
  const views = [['tree','Tree','▦'],['projects','Projects','☰'],['plans','Plans','💼'],['manifest','Manifest','✓']];
  document.getElementById('view-nav').innerHTML = views.map(([v,l,ic]) =>
    '<button class="navbtn'+(S.sel==='view:'+v?' sel':'')+'" data-view="'+v+'"><span class="nic">'+ic+'</span>'+l+'</button>').join('');
  let h = '';
  function row(id, depth){
    const b = byId[id]; if(!b) return;
    const un = descUnseen(id);
    const kind = b.kind === 'root' ? 'root' : (b.parent === 'project-buddy' ? 'direct' : b.kind);
    h += '<button class="brow'+(S.sel==='buddy:'+id?' sel':'')+(un?' has-unseen':'')+'" data-buddy="'+id+'"'
      + ' draggable="'+(id==='project-buddy'?'false':'true')+'"'
      + ' style="padding-left:'+(8+depth*16)+'px" title="'+escHtml(b.tagline||'')+'">'
      + '<span class="bdot"></span><span class="bicon">'+escHtml(b.icon||'')+'</span><span class="bname">'+escHtml(dispName(b))+'</span>'
      + '<span class="bkind">'+kind+'</span></button>';
    (kidsOf[id] || []).forEach(c => row(c.id, depth+1));
  }
  ROOT_ORDER.filter(id => { const b = byId[id]; const p = b ? effParent(b) : null; return p === null || p === 'project-buddy'; })
    .forEach(id => row(id, 0));
  document.getElementById('buddy-nav').innerHTML = h;
  if (Object.keys(S.parents).length) {
    document.getElementById('buddy-nav').insertAdjacentHTML('beforeend',
      '<div style="padding:10px 10px 0"><button class="linkbtn" id="reset-parents">Reset moved buddies</button></div>'
      + '<div class="fineprint" style="padding:2px 10px 0">Hierarchy moves save on this device.</div>');
  }
  const t = totalUnseen();
  const pill = document.getElementById('attn-pill');
  pill.textContent = t; pill.classList.toggle('zero', t === 0);
  document.getElementById('plan-nav').innerHTML = PLANS.map(p =>
    '<button class="brow'+(S.sel==='plan:'+p.id?' sel':'')+'" data-plan="'+p.id+'" style="padding-left:8px">'
    + '<span class="bicon">'+escHtml(p.icon||'')+'</span><span class="bname">'+escHtml(p.name)+'</span></button>').join('');
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
  let photos = '';
  if ((b.photos || []).length) {
    photos = '<div class="bp-sec"><h3>Photos</h3><div class="pstrip">'
      + b.photos.map(u => '<a href="'+escHtml(u)+'" target="_blank" rel="noopener"><img src="'+escHtml(u)+'" loading="lazy" alt=""></a>').join('')
      + '</div></div>';
  }
  const linkedPlans = PLANS.filter(p => (p.buddies || []).includes(id));
  let planSec = '';
  if (linkedPlans.length) {
    planSec = '<div class="bp-sec"><h3>Business plans</h3>' + linkedPlans.map(p =>
      '<a class="art-row" href="#" data-plan="'+p.id+'">'
      + '<span class="art-ic">'+escHtml(p.icon||'💼')+'</span>'
      + '<span><span class="art-label">'+escHtml(p.name)+'</span><div class="art-sub">BRD / business plan · '+escHtml(p.status)+'</div></span>'
      + '<span class="art-go">→</span></a>').join('') + '</div>';
  }
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
    + '<div class="bp-top"><span class="bp-icon">'+escHtml(b.icon||'')+'</span><h2 class="bp-name" id="bp-name" contenteditable="true" spellcheck="false" data-buddy="'+id+'">'+escHtml(dispName(b))+'</h2>'
    + '<span class="status '+b.statusClass+'">'+escHtml(b.status)+'</span></div>'
    + '<p class="bp-tagline">'+escHtml(b.tagline||'')+'</p>'
    + '<div class="bp-sec"><h3>What it does</h3><p class="bp-mission">'+escHtml(b.mission)+'</p>'
    + '<p class="fineprint">The mission is the brief\u2019s executive summary — tweak it through the buddy\u2019s chat thread and it updates everywhere.</p></div>'
    + photos
    + (id === 'project-buddy'
        ? '<div class="bp-sec"><h3>The Buddy Tree</h3><div class="bp-tree-wrap"></div>'
          + '<p class="fineprint"><button class="linkbtn" data-view="tree">Open the tree as its own view \u2192</button></p></div>'
        : '')
    + '<div class="bp-sec"><h3>Artifacts</h3>'+arts+'</div>'
    + planSec
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
    if (tw && src) { tw.innerHTML = src.innerHTML; const zb = tw.querySelector('#zoombar'); if (zb) zb.remove(); }
  }
}
function toast(msg){
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const t = document.createElement('div');
  t.className = 'toast'; t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => { if (t.parentNode) t.remove(); }, 3400);
}
function setIcon(emoji){
  if (!emoji) return;
  const svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>"+emoji+"</text></svg>";
  let l = document.querySelector("link[rel='icon']");
  if (!l) { l = document.createElement('link'); l.rel = 'icon'; document.head.appendChild(l); }
  l.type = 'image/svg+xml';
  l.href = 'data:image/svg+xml,' + encodeURIComponent(svg);
  try {
    const c = document.createElement('canvas'); c.width = c.height = 180;
    const x = c.getContext('2d');
    x.fillStyle = '#0d1117'; x.fillRect(0, 0, 180, 180);
    x.font = '135px serif'; x.textAlign = 'center'; x.textBaseline = 'middle';
    x.fillText(emoji, 90, 96);
    let a = document.querySelector("link[rel='apple-touch-icon']");
    if (!a) { a = document.createElement('link'); a.rel = 'apple-touch-icon'; document.head.appendChild(a); }
    a.href = c.toDataURL('image/png');
  } catch (e) {}
}
function isDesc(id, anc){
  let p = byId[id] ? effParent(byId[id]) : null;
  while (p) { if (p === anc) return true; p = byId[p] ? effParent(byId[p]) : null; }
  return false;
}
function moveBuddy(src, target){
  if (!src || !target || src === target) return;
  const b = byId[src]; if (!b || !byId[target]) return;
  if (isDesc(target, src)) { toast('Can\u2019t move ' + dispName(b) + ' under ' + dispName(byId[target]) + ' \u2014 that would create a loop.'); return; }
  if (target === b.parent) delete S.parents[src]; else S.parents[src] = target;
  save(); buildKids(); renderNav(); refreshViews();
  if (S.sel === 'buddy:' + src || S.sel === 'buddy:' + target || S.sel === 'buddy:project-buddy') renderBuddy(S.sel.slice(6));
  toast(dispName(b) + ' moved under ' + dispName(byId[target]) + '.');
}
const FAMKINDS = ['personal', 'family', 'property', 'finance', 'work'];
function nodeTag(b, depth){
  if (depth === 1) {
    if (b.kind === 'work') return 'direct child';
    if (b.kind === 'meta') return 'meta';
    if (b.kind === 'standalone') return 'direct';
    return 'family';
  }
  return depth === 2 ? 'child' : 'grandchild';
}
function iconName(b){ return escHtml((b.icon ? b.icon + ' ' : '') + dispName(b)); }
function gridKids(b){
  const kids = kidsOf[b.id] || [];
  if (!kids.length) return '';
  return '<ul class="subkids">' + kids.map(c =>
    '<li><div class="node ' + c.kind + '" data-buddy="' + c.id + '"><div class="name">' + iconName(c) + '</div>'
    + '<div class="desc">' + escHtml(c.tagline || '') + '</div><div class="tag">' + nodeTag(c, 2) + '</div>'
    + gridKids(c) + '</div></li>').join('') + '</ul>';
}
function orgNode(b, depth){
  const kids = kidsOf[b.id] || [];
  let s = '<li><div class="node ' + b.kind + '" data-buddy="' + b.id + '"><div class="name">' + iconName(b) + '</div>'
    + '<div class="desc">' + escHtml(b.tagline || '') + '</div>'
    + '<div class="tag">' + nodeTag(b, depth) + '</div></div>';
  if (kids.length) s += '<ul>' + kids.map(c => orgNode(c, depth + 1)).join('') + '</ul>';
  return s + '</li>';
}
function renderOrgTree(){
  const root = byId['project-buddy'];
  const kids = kidsOf['project-buddy'] || [];
  const fam = kids.filter(b => FAMKINDS.includes(b.kind));
  const rest = kids.filter(b => !FAMKINDS.includes(b.kind));
  let s = '<div class="chart"><div style="text-align:center"><div class="node root" data-buddy="project-buddy">'
    + '<div class="name">' + iconName(root) + '</div>'
    + '<div class="desc">' + escHtml(root.tagline || '') + '</div></div></div>'
    + '<div class="root-stub"></div><div class="tree"><ul>'
    + fam.map(b => orgNode(b, 1)).join('') + '</ul></div></div>';
  if (rest.length) {
    s += '<section class="standalones"><h2>Direct children of ' + escHtml(dispName(root)) + '</h2>'
      + '<p class="sub">Standalone buddies &mdash; parent is ' + escHtml(dispName(root)) + ' itself. Two meta-projects are tagged.</p>'
      + '<div class="grid">'
      + rest.map(b => '<div class="node ' + b.kind + '" data-buddy="' + b.id + '"><div class="name">' + iconName(b) + '</div>'
        + '<div class="desc">' + escHtml(b.tagline || '') + '</div><div class="tag">' + nodeTag(b, 1) + '</div>'
        + gridKids(b) + '</div>').join('')
      + '</div></section>';
  }
  document.getElementById('treezoom').innerHTML = s;
}
function renderProjects(){
  let s = '<section class="projects-view" style="margin-top:24px"><h2>Projects by Buddy</h2>'
    + '<p class="sub">Every buddy, in hierarchy order, with its current status.</p><div class="proj-list">';
  (function walk(id, depth){
    const b = byId[id]; if (!b) return;
    s += '<div class="proj-row d' + Math.min(depth, 3) + '" data-buddy="' + b.id + '">'
      + (depth ? '<span class="dot">\u2514</span>' : '')
      + '<span class="pname">' + iconName(b) + '</span>'
      + '<span class="pdesc">' + escHtml(b.tagline || '') + '</span>'
      + '<span class="status ' + b.statusClass + '">' + escHtml(b.status) + '</span></div>';
    (kidsOf[id] || []).forEach(c => walk(c.id, depth + 1));
  })('project-buddy', 0);
  s += '</div></section>';
  document.getElementById('view-projects').innerHTML = s;
}
let treeHTML0 = null, projHTML0 = null;
function refreshViews(){
  const tz = document.getElementById('treezoom'), vp = document.getElementById('view-projects');
  if (treeHTML0 === null) { treeHTML0 = tz.innerHTML; projHTML0 = vp.innerHTML; }
  if (Object.keys(S.parents).length) { renderOrgTree(); renderProjects(); }
  else { tz.innerHTML = treeHTML0; vp.innerHTML = projHTML0; }
}
function applyZoom(){
  const tz = document.getElementById('treezoom');
  if (tz) tz.style.zoom = (S.zoom || 100) + '%';
  const r = document.getElementById('zoomrange'), v = document.getElementById('zoomval');
  if (r) r.value = S.zoom || 100;
  if (v) v.textContent = (S.zoom || 100) + '%';
}
(function initZoom(){
  const vt = document.getElementById('view-tree');
  vt.insertAdjacentHTML('afterbegin',
    '<div class="zoombar" id="zoombar"><span title="Tip: hold Shift and scroll over the tree to zoom">Zoom</span>'
    + '<input type="range" id="zoomrange" min="50" max="160" step="5" value="100" aria-label="Tree zoom">'
    + '<span class="zv" id="zoomval">100%</span></div><div id="treezoom"></div>');
  const tz = document.getElementById('treezoom');
  Array.from(vt.childNodes).forEach(n => { if (n.id !== 'zoombar' && n.id !== 'treezoom') tz.appendChild(n); });
  document.getElementById('zoomrange').addEventListener('input', e => {
    S.zoom = parseInt(e.target.value, 10) || 100; save(); applyZoom();
  });
  applyZoom();
})();
(function initBrand(){
  const bn = document.getElementById('brand-name');
  const name = S.appName || 'Buddies';
  bn.textContent = name;
  document.title = name;
  bn.setAttribute('contenteditable', 'true');
  bn.setAttribute('spellcheck', 'false');
  bn.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); bn.blur(); } });
  bn.addEventListener('blur', () => {
    const v = bn.textContent.trim();
    if (v && v !== 'Buddies') S.appName = v; else delete S.appName;
    const n = S.appName || 'Buddies';
    bn.textContent = n;
    document.title = n;
    save();
  });
})();
(function initPan(){
  const tz = document.getElementById('treezoom');
  let pan = null;
  tz.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    const ch = e.target.closest('.chart');
    if (!ch) return;
    pan = { el: ch, x: e.clientX, y: e.clientY, sl: ch.scrollLeft, st: window.scrollY, moved: false, id: e.pointerId };
  });
  tz.addEventListener('pointermove', e => {
    if (!pan || e.pointerId !== pan.id) return;
    const dx = e.clientX - pan.x, dy = e.clientY - pan.y;
    if (!pan.moved && Math.abs(dx) + Math.abs(dy) < 5) return;
    pan.moved = true;
    pan.el.classList.add('panning');
    pan.el.scrollLeft = pan.sl - dx;
    window.scrollTo(0, pan.st - dy);
  });
  function endPan(e){
    if (!pan) return;
    if (e && e.pointerId !== pan.id) return;
    pan.el.classList.remove('panning');
    pan = null;
  }
  tz.addEventListener('pointerup', endPan);
  tz.addEventListener('pointercancel', endPan);
  window.addEventListener('pointerup', () => endPan(null));
})();
(function initTreeDrop(){
  function target(e){
    return (e.target && e.target.closest) ? e.target.closest('#treezoom .node[data-buddy], #view-projects .proj-row[data-buddy]') : null;
  }
  function clearHl(){ document.querySelectorAll('.node.drop-target,.proj-row.drop-target').forEach(x => x.classList.remove('drop-target')); }
  document.addEventListener('dragover', e => {
    const n = target(e);
    if (!n || !dragId || n.dataset.buddy === dragId) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    document.querySelectorAll('.node.drop-target,.proj-row.drop-target').forEach(x => { if (x !== n) x.classList.remove('drop-target'); });
    n.classList.add('drop-target');
  });
  document.addEventListener('drop', e => {
    const n = target(e);
    if (!n || !dragId) return;
    e.preventDefault();
    const src = dragId, dst = n.dataset.buddy;
    dragId = null; clearHl();
    moveBuddy(src, dst);
  });
  document.addEventListener('dragend', () => { dragId = null; clearHl(); });
})();
document.getElementById('view-tree').addEventListener('wheel', e => {
  if (!e.shiftKey) return;
  e.preventDefault();
  S.zoom = Math.min(160, Math.max(50, (S.zoom || 100) + (e.deltaY > 0 ? -5 : 5)));
  save(); applyZoom();
}, { passive: false });
let dragId = null;
(function initDrag(){
  const nav = document.getElementById('buddy-nav');
  nav.addEventListener('dragstart', e => {
    const r = e.target.closest('[data-buddy]');
    if (!r || r.dataset.buddy === 'project-buddy') { e.preventDefault(); return; }
    dragId = r.dataset.buddy;
    e.dataTransfer.effectAllowed = 'move';
    try { e.dataTransfer.setData('text/plain', dragId); } catch (_e) {}
    r.classList.add('dragging');
  });
  nav.addEventListener('dragend', () => {
    dragId = null;
    nav.querySelectorAll('.dragging,.drop-target').forEach(x => x.classList.remove('dragging', 'drop-target'));
  });
  nav.addEventListener('dragover', e => {
    const r = e.target.closest('[data-buddy]');
    if (!r || !dragId || r.dataset.buddy === dragId) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    nav.querySelectorAll('.drop-target').forEach(x => { if (x !== r) x.classList.remove('drop-target'); });
    r.classList.add('drop-target');
  });
  nav.addEventListener('drop', e => {
    const r = e.target.closest('[data-buddy]');
    if (!r || !dragId) return;
    e.preventDefault();
    const src = dragId, target = r.dataset.buddy;
    dragId = null;
    nav.querySelectorAll('.drop-target').forEach(x => x.classList.remove('drop-target'));
    moveBuddy(src, target);
  });
})();
function renderPlan(id){
  const p = planById[id]; if(!p) return;
  let docs = '';
  (p.docs || []).forEach(d => { docs += artRow(ICON_LINK, d.label, 'Related document', d.url); });
  if (!docs) docs = '<p class="bp-empty">No BRD or plan doc yet.</p>';
  const rel = (p.buddies || []).map(bid => byId[bid]).filter(Boolean);
  let buds = '';
  if (!rel.length) buds = '<p class="bp-empty">No buddy linked yet.</p>';
  else buds = rel.map(b => '<a class="art-row" href="#" data-buddy="'+b.id+'">'
    + '<span class="art-ic">'+escHtml(b.icon||'')+'</span>'
    + '<span><span class="art-label">'+escHtml(dispName(b))+'</span><div class="art-sub">'+escHtml(b.tagline||'')+'</div></span>'
    + '<span class="art-go">→</span></a>').join('');
  document.getElementById('buddy-home').innerHTML =
    '<div class="bp-wrap">'
    + '<div class="bp-crumb"><button class="linkbtn" data-view="plans">Business Plans</button> <span style="color:#6e7681">/</span> <b>'+escHtml(p.name)+'</b></div>'
    + '<div class="bp-top"><span class="bp-icon">'+escHtml(p.icon||'')+'</span>'
    + '<h2 style="font-size:32px;font-weight:700;margin:0">'+escHtml(p.name)+'</h2>'
    + '<span class="status '+p.statusClass+'">'+escHtml(p.status)+'</span></div>'
    + '<div class="bp-sec"><h3>What it is</h3><p class="bp-mission">'+escHtml(p.desc)+'</p></div>'
    + '<div class="bp-sec"><h3>Documents</h3>'+docs+'</div>'
    + '<div class="bp-sec"><h3>Related buddies</h3>'+buds+'</div>'
    + '<div class="bp-sec"><h3>Notes</h3><textarea class="notes" id="bp-notes" placeholder="Scratch pad for this plan\u2026">'+escHtml(S.notes[id]||'')+'</textarea>'
    + '<p class="fineprint">Saved on this device only.</p></div>'
    + '</div>';
  const nt = document.getElementById('bp-notes');
  let t = null;
  nt.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { S.notes[id] = nt.value; save(); }, 400); });
}
function show(sel){
  S.sel = sel; save();
  document.querySelectorAll('#main .view').forEach(v => v.classList.remove('active'));
  if (sel.startsWith('view:')) {
    document.getElementById('view-' + sel.slice(5)).classList.add('active');
  } else if (sel.startsWith('plan:')) {
    document.getElementById('view-buddy').classList.add('active');
    renderPlan(sel.slice(5));
  } else {
    document.getElementById('view-buddy').classList.add('active');
    renderBuddy(sel.slice(6));
  }
  renderNav();
  document.getElementById('main').scrollTop = 0;
  window.scrollTo(0,0);
  setIcon(sel.startsWith('plan:') ? ((planById[sel.slice(5)] || {}).icon)
    : sel.startsWith('buddy:') ? ((byId[sel.slice(6)] || {}).icon) : byId['project-buddy'].icon);
}
document.addEventListener('click', e => {
  const vb = e.target.closest('[data-view]');
  if (vb) { show('view:' + vb.dataset.view); return; }
  const pb = e.target.closest('[data-plan]');
  if (pb) { e.preventDefault(); show('plan:' + pb.dataset.plan); return; }
  const bb = e.target.closest('[data-buddy]');
  if (bb) { show('buddy:' + bb.dataset.buddy); return; }
  const sb = e.target.closest('[data-seen]');
  if (sb) { S.seen[sb.dataset.seen] = Date.now(); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const sa = e.target.closest('[data-seen-all]');
  if (sa) { (byId[sa.dataset.seenAll].attention || []).forEach(a => S.seen[a.id] = Date.now()); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const gt = e.target.closest('[data-goto]');
  if (gt) { e.preventDefault(); show('buddy:' + gt.dataset.goto); return; }
  const rp = e.target.closest('#reset-parents');
  if (rp) { S.parents = {}; save(); buildKids(); renderNav(); refreshViews();
    if (S.sel.startsWith('buddy:')) renderBuddy(S.sel.slice(6));
    toast('Hierarchy reset to the registry.'); return; }
});
refreshViews();
show(S.sel || 'view:tree');
"""
    js = js.replace("BUDDIES_JSON", buddies_js).replace("ORDER_JSON", order_js).replace("PLANS_JSON", plans_js)
    js = js.replace("ICON_DOC", "'" + ICON_DOC.replace("'", "\\'") + "'")
    js = js.replace("ICON_REPO", "'" + ICON_REPO.replace("'", "\\'") + "'")
    js = js.replace("ICON_LINK", "'" + ICON_LINK.replace("'", "\\'") + "'")

    out = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="application-name" content="Buddies">
<meta name="apple-mobile-web-app-title" content="Buddies">
<title>Buddies</title>
<style>
""" + style + NEW_CSS + """
</style>
</head>
<body>
<div class="app">
<aside id="sidebar">
  <div class="brand"><div class="eyebrow">Project Buddy &middot; macro view</div><h1 id="brand-name" title="Click to rename">Buddies</h1><div class="bcount">NBUD buddies &middot; one family</div></div>
  <div class="nav-sec"><h3>Views</h3><div id="view-nav"></div></div>
  <div class="nav-sec"><h3>Buddies <span id="attn-pill" class="zero">0</span></h3><div id="buddy-nav"></div></div>
  <div class="nav-sec"><h3>Business Plans</h3><div id="plan-nav"></div></div>
</aside>
<main id="main">
""" + vt + vp + vpl + vm + """
<section id="view-buddy" class="view"><div id="buddy-home"></div></section>
</main>
</div>
<script>
""" + js + """
</script>
</body>
</html>
"""
    out = out.replace("NBUD", str(n_buddies))
    open(f"{HERE}/index.html", "w").write(out)
    print("wrote index.html", len(out), "bytes")


if __name__ == "__main__":
    build()
