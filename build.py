#!/usr/bin/env python3
"""Build the Project Buddy dashboard (index.html) from buddies.json + the view fragments.

Usage: build.py   (run from ~/workspace/projects/buddy-tree)
Reads:  buddies.json, buddy-tree.html (style + the three view fragments)
Writes: index.html
"""
import json
import re
from datetime import datetime
BUILD_NUM = datetime.now().strftime('%Y%m%d.%H%M')

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
.treewrap{position:relative;display:flex;gap:10px;align-items:flex-start}
#view-tree{margin:-36px -32px -80px;display:flex;flex-direction:column;min-height:calc(100vh - 0px)}
#view-tree #zoomwrap{flex:1;min-height:0;align-items:stretch}
#treezoom{flex:1;min-width:0;min-height:0;overflow:auto;border:1px solid #30363d;border-left:none;border-right:none;cursor:grab;border-radius:0;background:#0d1117}
#treezoom.panning{cursor:grabbing}
#treezoom,#view-projects,#view-manifest{touch-action:pan-x pan-y}
#treezoom.panning,#treezoom.panning *{user-select:none!important;-webkit-user-select:none!important}
#treezoom,#treezoom *{user-select:none;-webkit-user-select:none}
#zoombar{position:absolute;top:14px;left:14px;width:54px;height:248px;background:rgba(22,27,34,.94);border:1px solid #30363d;border-radius:12px;z-index:5;box-shadow:0 4px 16px rgba(0,0,0,.4)}
#zoombar .zt{position:absolute;top:8px;left:0;right:0;text-align:center;font-size:11px;color:#8b949e;cursor:help}
#zoomrange{position:absolute;left:50%;top:50%;width:188px;margin:0;padding:0;transform:translate(-50%,-50%) rotate(-90deg);accent-color:#1f6feb;cursor:pointer}
#zoombar .zv{position:absolute;bottom:8px;left:0;right:0;text-align:center;font-size:12px;color:#8b949e;font-variant-numeric:tabular-nums}
#zoomfit{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);background:none;border:1px solid #30363d;border-radius:8px;color:#8b949e;font-size:14px;width:30px;height:26px;cursor:pointer}
#zoomfit:hover{color:#e6edf3;border-color:#8b949e}
body.light #zoombar{background:#ffffff;border-color:#d0d7de}
#sb-resize{position:absolute;top:0;right:-5px;width:11px;height:100%;cursor:ew-resize;z-index:20}
#sb-resize:hover{background:rgba(31,111,235,.28)}
@media (max-width:900px){#sb-resize{display:none}}
.bp-topnav{display:flex;gap:4px;align-items:center;margin-bottom:6px;flex-wrap:wrap}
.bp-topnav .sep{color:#6e7681;margin:0 2px}
#journal-bar{display:none;margin:0 0 12px;background:#0d1a30;border:1px solid #1f6feb;border-radius:10px;padding:9px 13px;font-size:13px}
#journal-bar.show{display:block}
#journal-bar ul{margin:8px 0 4px;padding-left:18px;display:none}
#journal-bar.open ul{display:block}
#journal-bar li{margin:3px 0;color:#c9d1d9}
#journal-bar .jtime{color:#6e7681;font-size:11px;margin-left:6px}
.pdrop{border:2px dashed #30363d;border-radius:12px;padding:20px;text-align:center;color:#8b949e;font-size:13px;margin-top:10px;cursor:pointer}
.pdrop.over{border-color:#1f6feb;background:#0d1a30;color:#e6edf3}
.pstrip:empty{display:none}
.ghtoken{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;align-items:center}
#token-banner{display:none;border:2px solid #d29922;background:#1c1a12;border-radius:12px;padding:14px 16px;margin-bottom:18px}
#token-banner.show{display:block}
#token-banner h4{margin:0 0 6px;font-size:14px;color:#e6edf3}
#token-banner p{margin:0 0 10px;font-size:13px;color:#c9b98a}
#token-banner .ghtoken{margin-top:0}
.locked{opacity:.45;pointer-events:none}
textarea[disabled]{opacity:.5;cursor:not-allowed}
.tokenwarn{background:#3a2a00;border:2px solid #d29922;color:#f0b429;border-radius:10px;padding:14px 16px;font-size:14px;margin-top:8px;line-height:1.6}
.tokenwarn a{color:#ffd866;font-weight:bold}
.tokenwarn b{color:#ffe9a8}
#token-pill{position:fixed;top:12px;right:12px;z-index:1000;display:flex;align-items:center;gap:6px;
  padding:8px 14px;border-radius:20px;font-size:13px;font-weight:600;cursor:pointer;border:2px solid;transition:all .2s}
#token-pill.need{background:#3a2a00;border-color:#d29922;color:#ffd866}
#token-pill.ok{background:#0d2818;border-color:#2ea043;color:#7ee787}
#token-pill:hover{transform:scale(1.05)}
#token-pop{position:fixed;top:52px;right:12px;z-index:1001;background:#161b22;border:1px solid #30363d;border-radius:12px;
  padding:16px;width:300px;display:none;box-shadow:0 8px 24px rgba(0,0,0,.5)}
#token-pop.show{display:block}
#token-pop h4{margin:0 0 8px;font-size:14px}
#token-pop p{margin:0 0 10px;font-size:12px;color:#8b949e;line-height:1.5}
#token-pop input{width:100%;box-sizing:border-box;background:#0d1117;border:1px solid #30363d;color:#e6edf3;
  border-radius:8px;padding:8px 10px;font-size:13px;margin-bottom:10px}
#token-pop .saved-check{display:none;color:#7ee787;font-size:14px;font-weight:600;margin-top:8px}
#token-pop .saved-check.show{display:block}
.ctog{display:none;width:18px;height:18px;flex:0 0 18px;align-items:center;justify-content:center;
  background:none;border:none;color:#8b949e;cursor:pointer;font-size:10px;padding:0;margin-right:2px}
.brow:hover .ctog.has-kids{display:inline-flex}
.ctog.has-kids.collapsed{transform:rotate(-90deg)}
#field-settings{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:2000;
  background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;width:320px;max-height:80vh;overflow:auto;
  box-shadow:0 12px 40px rgba(0,0,0,.6);display:none}
#field-settings.show{display:block}
#field-settings h3{margin:0 0 12px;font-size:14px}
.fset-row{display:flex;align-items:center;gap:8px;padding:8px;border:1px solid #21262d;border-radius:8px;margin-bottom:6px;background:#0d1117;cursor:grab}
.fset-row.dragging{opacity:.5}
.fset-row .fh{color:#8b949e;cursor:grab;font-size:14px}
.fset-row .fl{flex:1;font-size:13px}
.fset-row input[type=checkbox]{width:16px;height:16px}
.bp-close-x{position:absolute;top:12px;right:12px;z-index:10;width:32px;height:32px;
  background:#161b22;border:1px solid #30363d;border-radius:8px;color:#8b949e;font-size:16px;
  cursor:pointer;display:flex;align-items:center;justify-content:center}
.bp-close-x:hover{color:#e6edf3;border-color:#1f6feb;background:#1c2128}
#buddy-home{position:relative}
.ghtoken input{flex:1;min-width:180px;background:#0d1117;border:1px solid #30363d;color:#e6edf3;border-radius:8px;padding:7px 10px;font-size:13px}
.linkbtn{background:none;border:none;color:#1f6feb;cursor:pointer;font-size:13px;padding:2px 4px}
.linkbtn:hover{text-decoration:underline}
.bp-topnav{margin-bottom:6px}
.bp-build{margin:26px 0 6px;font-size:11px;color:#6e7681;text-align:center}
.pstrip{display:flex;gap:10px;overflow-x:auto;padding:2px 2px 6px}
.pstrip a{flex:0 0 auto}
/* ---- standalone buddy mode ---- */
body.standalone #sidebar{display:none}
body.standalone .app{display:block}
body.standalone #main{max-width:880px;margin:0 auto;padding:28px 24px 80px}
.sa-bar{display:none;align-items:center;gap:10px;margin-bottom:18px;padding:10px 14px;
  background:#161b22;border:1px solid #30363d;border-radius:12px;font-size:13px;color:#8b949e}
body.standalone .sa-bar{display:flex}
.sa-bar .linkbtn{font-size:13px}

/* ============ RESPONSIVE ============ */
#menu-btn{display:none}
/* ---- Small: <640px (iPhone) ---- */
@media (max-width:639px){
  .app{display:block}
  #menu-btn{display:block;position:fixed;top:12px;left:12px;z-index:90;background:#161b22;
    border:1px solid #30363d;border-radius:10px;color:#e6edf3;font-size:18px;
    width:44px;height:44px;cursor:pointer}
  #sidebar{position:fixed;left:0;top:0;bottom:0;z-index:95;height:100vh;height:100dvh;
    transform:translateX(-105%);transition:transform .25s ease;width:300px;flex:none}
  #sidebar.open{transform:none;box-shadow:8px 0 32px rgba(0,0,0,.5)}
  #sb-resize{display:none}
  #main{padding:68px 14px 60px}
  .tree,.tree ul{display:block;padding:0;margin:0}
  .tree ul{padding-top:0}
  .tree li{display:block;padding:0;text-align:left}
  .tree li::before,.tree li::after,.tree ul ul::before,.root-stub{display:none}
  .node{display:block;width:auto;margin:0 0 10px}
  .node.root{width:auto}
  .standalones .grid{display:block}
  #treezoom{height:auto;max-height:none;overflow:visible;cursor:default}
  #zoombar{display:none}
  #view-buddy.sheet{position:fixed;left:0;right:0;bottom:0;top:10%;z-index:96;
    background:#0d1117;border-top:1px solid #30363d;border-radius:18px 18px 0 0;
    overflow-y:auto;padding:10px 16px 48px;box-shadow:0 -8px 32px rgba(0,0,0,.5)}
  #view-buddy.sheet::before{content:'';display:block;width:44px;height:5px;border-radius:3px;
    background:#30363d;margin:2px auto 12px}
}
/* ---- Medium: 640-1100px (iPad) ---- */
@media (min-width:640px) and (max-width:1100px){
  #sidebar{width:250px;flex:0 0 250px}
  #view-nav{display:flex;gap:4px;background:#161b22;border:1px solid #30363d;
    border-radius:12px;padding:4px}
  #view-nav .navbtn{flex:1}
  .node{width:172px}
  #view-buddy.panel{position:fixed;top:0;right:0;bottom:0;width:min(380px,92vw);z-index:60;
    background:#0d1117;border-left:1px solid #30363d;overflow-y:auto;
    padding:20px 18px 48px;box-shadow:-8px 0 32px rgba(0,0,0,.5)}
}
/* ---- Large: >1100px (desktop) ---- */
@media (min-width:1101px){
  #view-buddy.panel{position:fixed;top:0;right:0;bottom:0;width:400px;z-index:60;
    background:#0d1117;border-left:1px solid #30363d;overflow-y:auto;
    padding:24px 20px 48px;box-shadow:-8px 0 32px rgba(0,0,0,.5)}
}
#view-buddy.panel.active,#view-buddy.sheet.active{display:block}
#bp-close{display:none}
#view-buddy.panel #bp-close,#view-buddy.sheet #bp-close{display:inline-block}

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
.bp-tree-wrap{border:1px solid #21262d;border-radius:12px;background:#0d1117;overflow:auto;position:relative;height:420px;cursor:grab}
.bp-tree-wrap.panning{cursor:grabbing}
.bp-mini-zoom{position:absolute;top:8px;right:8px;z-index:5;display:flex;gap:4px}
.bp-mini-zoom button{background:rgba(22,27,34,.94);border:1px solid #30363d;color:#e6edf3;border-radius:8px;width:28px;height:28px;font-size:14px;cursor:pointer}
.bp-mini-zoom button:hover{border-color:#1f6feb}
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
  const q = (document.getElementById('buddy-search').value || '').toLowerCase().trim();
  const words = q.split(/\s+/).filter(Boolean);
  let h = '';
  function matches(b){
    if (!words.length) return true;
    const hay = ((b.name || '') + ' ' + (b.tagline || '')).toLowerCase();
    return words.every(w => hay.includes(w));
  }
  function row(id, depth){
    const b = byId[id]; if(!b) return;
    if (words.length && !matches(b)) { (kidsOf[id] || []).forEach(c => row(c.id, depth+1)); return; }
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
function closeDetail(){
  document.getElementById('view-buddy').classList.remove('active', 'panel', 'sheet');
}
const FIELD_DEFS = [
  {id:'ingest', label:'Ingest'},
  {id:'attention', label:'Needs your attention'},
  {id:'mission', label:'What it does'},
  {id:'photos', label:'Photos'},
  {id:'tree', label:'The Buddy Tree'},
  {id:'artifacts', label:'Artifacts'},
  {id:'plans', label:'Business plans'},
  {id:'notes', label:'Notes'},
  {id:'shared', label:'Shared notes'},
];
function getFieldOrder(){
  if (!S.fieldOrder || !Array.isArray(S.fieldOrder)) S.fieldOrder = FIELD_DEFS.map(f => f.id);
  return S.fieldOrder;
}
function isFieldVisible(fid){
  if (!S.fieldHidden) S.fieldHidden = {};
  return !S.fieldHidden[fid];
}
function openFieldSettings(){
  let m = document.getElementById('field-settings');
  if (!m) {
    m = document.createElement('div'); m.id = 'field-settings';
    m.innerHTML = '<h3>Buddy fields</h3><p class="fineprint" style="margin-bottom:12px">Drag to reorder. Uncheck to hide.</p><div id="fset-list"></div>'
      + '<div style="margin-top:12px;text-align:right"><button class="linkbtn" id="fset-close">Done</button></div>';
    document.body.appendChild(m);
    document.getElementById('fset-close').addEventListener('click', () => m.classList.remove('show'));
  }
  const list = document.getElementById('fset-list');
  list.innerHTML = getFieldOrder().map(fid => {
    const def = FIELD_DEFS.find(f => f.id === fid);
    if (!def) return '';
    const vis = isFieldVisible(fid);
    return '<div class="fset-row" draggable="true" data-fid="' + fid + '">'
      + '<span class="fh">\u2630</span><span class="fl">' + def.label + '</span>'
      + '<input type="checkbox" ' + (vis ? 'checked' : '') + ' data-vis="' + fid + '" title="Show/hide"></div>';
  }).join('');
  // Drag reorder
  let dragEl = null;
  list.querySelectorAll('.fset-row').forEach(row => {
    row.addEventListener('dragstart', e => { dragEl = row; row.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move'; });
    row.addEventListener('dragend', () => row.classList.remove('dragging'));
    row.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; });
    row.addEventListener('drop', e => {
      e.preventDefault();
      if (!dragEl || dragEl === row) return;
      const ids = Array.from(list.querySelectorAll('.fset-row')).map(r => r.dataset.fid);
      const from = ids.indexOf(dragEl.dataset.fid), to = ids.indexOf(row.dataset.fid);
      const order = getFieldOrder();
      const [moved] = order.splice(from, 1);
      order.splice(to, 0, moved);
      S.fieldOrder = order; save();
      openFieldSettings();
      const mm = S.sel.match(/^buddy:(.+)$/); if (mm) renderBuddy(mm[1]);
    });
  });
  list.querySelectorAll('[data-vis]').forEach(cb => {
    cb.addEventListener('change', () => {
      if (!S.fieldHidden) S.fieldHidden = {};
      S.fieldHidden[cb.dataset.vis] = !cb.checked;
      save();
      const mm = S.sel.match(/^buddy:(.+)$/); if (mm) renderBuddy(mm[1]);
    });
  });
  m.classList.add('show');
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
  const seedStrip = (b.photos || []).map(u => '<a href="'+escHtml(u)+'" target="_blank" rel="noopener"><img src="'+escHtml(u)+'" loading="lazy" alt=""></a>').join('');
  photos = '<div class="bp-sec"><h3>Photos</h3><div class="pstrip" id="pstrip">' + seedStrip + '</div>'
    + '<div class="pdrop" id="pdrop">Drop photos here or click to choose<br><span style="font-size:12px">JPEG, PNG, GIF, WebP, HEIC \u2014 all supported</span></div>'
    + '<p class="fineprint" id="pstat"></p></div>';
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
    + '<div id="token-banner"><h4>\U0001f511 Connect GitHub to unlock this buddy</h4>'
    + '<p>Photos, shared notes, and ingest save to the buddy\u2019s repo. Paste a token once \u2014 it stays on this device.</p>'
    + '<div class="ghtoken"><input type="password" id="ghtok2" placeholder="GitHub token (repo scope)" aria-label="GitHub token">'
    + '<button class="linkbtn" id="ghtok2-save">Save token</button></div></div>'
    + '<div class="sa-bar"><span>\U0001f516 Standalone view</span><button class="linkbtn" id="sa-full">Open full dashboard \u2192</button></div>'
    + '<button class="bp-close-x" id="bp-close-x" title="Close">\u2715</button>'
    + '<div class="bp-topnav"><button class="linkbtn" data-navbtn="back">\u2190 Back</button>'
    + '<button class="linkbtn" data-navbtn="prev">\u2039 Prev</button><button class="linkbtn" data-navbtn="next">Next \u203a</button>'
    + '<span class="sep">\u00b7</span><button class="linkbtn" data-view="tree">All buddies</button>'
    + '<span class="sep">\u00b7</span><button class="linkbtn" id="bp-close">\u2715 Close</button><span class="sep">\u00b7</span><button class="linkbtn" id="bp-desktop">\U0001f4be Save to desktop</button></div>'
    + '<div class="bp-crumb">'+crumb(id)+'</div>'
    + '<div class="bp-top"><span class="bp-icon">'+escHtml(b.icon||'')+'</span><h2 class="bp-name" id="bp-name" contenteditable="true" spellcheck="false" data-buddy="'+id+'">'+escHtml(dispName(b))+'</h2>'
    + '<span class="status '+b.statusClass+'">'+escHtml(b.status)+'</span></div>'
    + '<p class="bp-tagline">'+escHtml(b.tagline||'')+'</p>'
    + '<div class="bp-sec"><h3>Ingest</h3><p class="fineprint">Brain-dump anything about this buddy \u2014 raw and unfiltered. '
    + 'Each dump lands in the buddy\u2019s repo (docs/ingest.md) as a timestamped entry, ready to be worked into the dossier later.</p>'
    + '<textarea class="notes" id="bp-ingest" placeholder="Dump what\u2019s in your head about '+escHtml(dispName(b))+'\u2026"></textarea>'
    + '<div style="margin-top:8px"><span class="fineprint" id="ingest-status"></span></div>'
    + '<div id="ingest-feed" style="margin-top:8px"></div></div>'
    + '<div class="bp-sec"><h3>Needs your attention</h3>'+attn+'</div>'
    + '<div class="bp-sec"><h3>What it does</h3><p class="bp-mission">'+escHtml(b.mission)+'</p>'
    + '<p class="fineprint">The mission is the brief\u2019s executive summary — tweak it through the buddy\u2019s chat thread and it updates everywhere.</p></div>'
    + photos
    + (id === 'project-buddy'
        ? '<div class="bp-sec"><h3>The Buddy Tree</h3><div class="bp-tree-wrap"></div>'
          + '<p class="fineprint"><button class="linkbtn" data-view="tree">Open the tree as its own view \u2192</button></p></div>'
        : '')
    + '<div class="bp-sec"><h3>Artifacts</h3>'+arts+'</div>'
    + planSec
    + '<div class="bp-sec"><h3>Notes</h3><textarea class="notes" id="bp-notes" placeholder="Scratch pad for this buddy\u2026">'+escHtml(S.notes[id]||'')+'</textarea>'
    + '<p class="fineprint">Saved on this device only.</p></div>'
    + '<div class="bp-sec"><h3>Shared notes</h3><p class="fineprint">Saved to the buddy\u2019s repo (docs/notes.md) \u2014 visible to everyone with repo access.</p>'
    + '<textarea class="notes" id="bp-shared-notes" placeholder="Shared notes\u2026"></textarea>'
    + '<p class="fineprint" id="shared-status"></p></div>'
    + '<div class="bp-build">Build __BUILD__</div>'
    + '</div>';
  const nm = document.getElementById('bp-name');
  nm.addEventListener('keydown', e => { if (e.key === 'Enter'){ e.preventDefault(); nm.blur(); } });
  nm.addEventListener('blur', () => {
    const v = nm.textContent.trim();
    const before = S.names[id] != null ? S.names[id] : null;
    const beforeLabel = dispName(b);
    if (v && v !== beforeLabel) S.names[id] = v; else delete S.names[id];
    const after = S.names[id] != null ? S.names[id] : null;
    if (before !== after) logChange('rename', id, 'Renamed \u201c' + beforeLabel + '\u201d \u2192 \u201c' + dispName(byId[id]) + '\u201d', before, after);
    save(); renderNav();
  });
  const nt = document.getElementById('bp-notes');
  let t = null, notesBefore = null;
  nt.addEventListener('focus', () => { notesBefore = nt.value; });
  nt.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { S.notes[id] = nt.value; save(); }, 400); });
  nt.addEventListener('blur', () => {
    if (notesBefore !== null && notesBefore !== nt.value) logChange('notes', id, 'Edited notes for \u201c' + dispName(byId[id]) + '\u201d', notesBefore, nt.value);
    notesBefore = null;
  });
  (function initIngestAuto(bid){
    const ta = document.getElementById('bp-ingest'), st = document.getElementById('ingest-status');
    if (!ta || ta.dataset.auto) return;
    ta.dataset.auto = '1';
    let t = null, lastDumped = '';
    ta.addEventListener('input', () => {
      clearTimeout(t);
      const txt = ta.value.trim();
      if (!txt || txt === lastDumped) { if (st && !txt) st.textContent = ''; return; }
      if (st) st.textContent = 'waiting\u2026';
      t = setTimeout(async () => {
        const cur = ta.value.trim();
        if (!cur || cur === lastDumped) return;
        if (st) st.textContent = 'dumping\u2026';
        await dumpIngest(bid, true);
        lastDumped = ta.value.trim();
        if (st && lastDumped) st.textContent = 'dumped \u2713';
      }, 2000);
    });
  })(id);
  loadPhotos(id);
  initPhotoDrop(id);
  refreshTokenUI(id);
  renderJournal();
  if (id === 'project-buddy') {
    const tw = document.querySelector('#buddy-home .bp-tree-wrap');
    const srcEl = document.getElementById('view-tree');
    if (tw && srcEl) {
      tw.innerHTML = '<div class="bp-mini-zoom"><button id="bp-mz-out" title="Zoom out">\u2212</button><button id="bp-mz-in" title="Zoom in">+</button></div><div class="bp-mini-chart"></div>';
      const mc = tw.querySelector('.bp-mini-chart');
      mc.innerHTML = srcEl.innerHTML;
      const zb = mc.querySelector('#zoombar'); if (zb) zb.remove();
      const zw = mc.querySelector('#zoomwrap'); if (zw) { zw.style.display = 'block'; }
      const tz = mc.querySelector('#treezoom'); if (tz) { tz.style.overflow = 'visible'; tz.style.height = 'auto'; tz.removeAttribute('id'); }
      let mz = 80;
      const applyMz = () => { const ch = mc.querySelector('.chart'); if (ch) ch.style.zoom = mz + '%'; };
      applyMz();
      document.getElementById('bp-mz-in').addEventListener('click', e => { e.stopPropagation(); mz = Math.min(150, mz + 10); applyMz(); });
      document.getElementById('bp-mz-out').addEventListener('click', e => { e.stopPropagation(); mz = Math.max(20, mz - 10); applyMz(); });
      attachPan(tw);
    }
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
  const beforeParent = effParent(b);
  if (target === b.parent) delete S.parents[src]; else S.parents[src] = target;
  logChange('move', src, 'Moved \u201c' + dispName(byId[src]) + '\u201d under \u201c' + dispName(byId[target]) + '\u201d', beforeParent, target);
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
function gripHtml(b){
  if (b.id === 'project-buddy') return '';
  return '<span class="grip" draggable="true" data-buddy="' + b.id + '" title="Drag to move under a different parent">\u28ff</span>';
}
function orgNode(b, depth){
  const kids = kidsOf[b.id] || [];
  const kc = kids.length ? '<span class="kcount">' + kids.length + '</span>' : '';
  let s = '<li><div class="node ' + b.kind + '" data-buddy="' + b.id + '">' + gripHtml(b) + '<div class="name">' + iconName(b) + kc + '</div>'
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
      + rest.map(b => '<div class="node ' + b.kind + '" data-buddy="' + b.id + '">' + gripHtml(b) + '<div class="name">' + iconName(b) + '</div>'
        + '<div class="desc">' + escHtml(b.tagline || '') + '</div><div class="tag">' + nodeTag(b, 1) + '</div>'
        + gridKids(b) + '</div>').join('')
      + '</div></section>';
  }
  const orphans = (kidsOf['__root'] || []).filter(b => b.id !== 'project-buddy');
  if (orphans.length) {
    s += '<section class="standalones"><h2>Orphaned buddies</h2>'
      + '<p class="sub">No parent yet &mdash; drag one onto a buddy in the tree to give it a home.</p>'
      + '<div class="grid">'
      + orphans.map(b => '<div class="node ' + b.kind + '" data-buddy="' + b.id + '">' + gripHtml(b) + '<div class="name">' + iconName(b) + '</div>'
        + '<div class="desc">' + escHtml(b.tagline || '') + '</div></div>').join('')
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
function zoomToFit(){
  const tz = document.getElementById('treezoom');
  const chart = tz ? tz.querySelector('.chart') : null;
  if (!tz || !chart) return;
  const z = (S.zoom || 100) / 100;
  const natW = chart.scrollWidth / z, natH = chart.scrollHeight / z;
  const vw = tz.clientWidth, vh = tz.clientHeight;
  if (!natW || !natH || !vw || !vh) return;
  const fit = Math.min(vw / natW, vh / natH) * 100;
  S.zoom = Math.min(160, Math.max(50, Math.round(fit / 5) * 5));
  save(); applyZoom();
  toast('Zoomed to fit (' + S.zoom + '%).');
}
(function initZoom(){
  const vt = document.getElementById('view-tree');
  vt.insertAdjacentHTML('afterbegin',
    '<div class="treewrap" id="zoomwrap"><div class="zoombar" id="zoombar"><span class="zt" title="Tip: hold Shift and scroll over the tree to zoom">Zoom</span>'
    + '<input type="range" id="zoomrange" min="50" max="160" step="5" value="100" aria-label="Tree zoom">'
    + '<span class="zv" id="zoomval">100%</span><button id="zoomfit" title="Zoom to fit">\u26f6</button></div><div id="treezoom"></div></div>');
  const tw = document.getElementById('zoomwrap'), tz = document.getElementById('treezoom');
  Array.from(vt.childNodes).forEach(n => { if (n !== tw) tz.appendChild(n); });
  document.getElementById('zoomrange').addEventListener('input', e => {
    S.zoom = parseInt(e.target.value, 10) || 100; save(); applyZoom();
  });
  document.getElementById('zoomfit').addEventListener('click', zoomToFit);
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
    const before = S.appName || null;
    if (v && v !== 'Buddies') S.appName = v; else delete S.appName;
    const after = S.appName || null;
    if (before !== after) logChange('brand', null, 'Renamed app \u201c' + (before || 'Buddies') + '\u201d \u2192 \u201c' + (after || 'Buddies') + '\u201d', before, after);
    applyBrand();
    save();
  });
})();
function attachPan(el){
  if (!el || el.dataset.panAttached) return;
  el.dataset.panAttached = '1';
  let pan = null, swallow = false;
  el.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse') return;
    if (e.button !== 0) return;
    if (e.target.closest && (e.target.closest('.grip') || e.target.closest('input,textarea,button,a'))) return;
    pan = { x: e.clientX, y: e.clientY, sl: el.scrollLeft, st: el.scrollTop, moved: false, id: e.pointerId };
  });
  el.addEventListener('pointermove', e => {
    if (!pan || e.pointerId !== pan.id) return;
    const dx = e.clientX - pan.x, dy = e.clientY - pan.y;
    if (!pan.moved && Math.abs(dx) + Math.abs(dy) < 5) return;
    pan.moved = true;
    el.classList.add('panning');
    el.scrollLeft = pan.sl - dx;
    el.scrollTop = pan.st - dy;
    e.preventDefault();
  });
  function endPan(e){
    if (!pan) return;
    if (e && e.pointerId !== pan.id) return;
    el.classList.remove('panning');
    if (pan.moved) { swallow = true; setTimeout(() => { swallow = false; }, 80); }
    pan = null;
  }
  el.addEventListener('pointerup', endPan);
  el.addEventListener('pointercancel', endPan);
  window.addEventListener('pointerup', () => endPan(null));
  el.addEventListener('click', e => {
    if (swallow) { e.preventDefault(); e.stopPropagation(); }
  }, true);
}
function initPan(){
  attachPan(document.getElementById('treezoom'));
  attachPan(document.getElementById('view-projects'));
  attachPan(document.getElementById('view-manifest'));
}
initPan();
(function initGripDrag(){
  const tz = document.getElementById('treezoom');
  tz.addEventListener('dragstart', e => {
    const g = e.target.closest ? e.target.closest('.grip') : null;
    if (!g) return;
    const id = g.dataset.buddy;
    if (!id || id === 'project-buddy') { e.preventDefault(); return; }
    dragId = id;
    e.dataTransfer.effectAllowed = 'move';
    try { e.dataTransfer.setData('text/plain', id); } catch (_e) {}
  });
  tz.addEventListener('dragend', () => {
    dragId = null;
    document.querySelectorAll('#treezoom .node.drop-target').forEach(x => x.classList.remove('drop-target'));
  });
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
    + '<div class="bp-build">Build __BUILD__</div>'
    + '</div>';
  const nt = document.getElementById('bp-notes');
  let t = null;
  nt.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { S.notes[id] = nt.value; save(); }, 400); });
}
const navHist = [];
function locHash(){ try { return (typeof location !== 'undefined' && location.hash) || ''; } catch (e) { return ''; } }
function isStandalone(){ return /(^|\/)standalone$/.test(locHash().replace(/^#\//, '')); }
function hashFor(sel){ return '#/' + sel + (isStandalone() ? '/standalone' : ''); }
function show(sel, push){
  if (push !== false && S.sel && sel !== S.sel) { navHist.push(S.sel); if (navHist.length > 60) navHist.shift(); }
  S.sel = sel; save();
  const h = hashFor(sel);
  try { if (typeof location !== 'undefined' && location.hash !== h) location.hash = h; } catch (e) {}
  document.body.classList.toggle('standalone', isStandalone());
  const vb = document.getElementById('view-buddy');
  const asOverlay = sel.startsWith('buddy:') && !isStandalone();
  if (asOverlay) {
    vb.classList.add('active');
    vb.classList.toggle('panel', window.innerWidth >= 640);
    vb.classList.toggle('sheet', window.innerWidth < 640);
    renderBuddy(sel.slice(6));
  } else {
    document.querySelectorAll('#main .view').forEach(v => v.classList.remove('active', 'panel', 'sheet'));
    if (sel.startsWith('view:')) {
      document.getElementById('view-' + sel.slice(5)).classList.add('active');
    } else if (sel.startsWith('plan:')) {
      vb.classList.add('active');
      renderPlan(sel.slice(5));
    } else {
      vb.classList.add('active');
      renderBuddy(sel.slice(6));
    }
  }
  renderNav();
  document.getElementById('main').scrollTop = 0;
  window.scrollTo(0,0);
  setIcon(sel.startsWith('plan:') ? ((planById[sel.slice(5)] || {}).icon)
    : sel.startsWith('buddy:') ? ((byId[sel.slice(6)] || {}).icon) : byId['project-buddy'].icon);
}
/* ---------- keyboard nav ---------- */
document.addEventListener('keydown', e => {
  if (e.target && e.target.matches && e.target.matches('input, textarea, [contenteditable="true"]')) return;
  if (e.key === 'Escape') { closeDetail(); return; }
  if (e.key === '/' && !e.target.matches('input, textarea, [contenteditable="true"]')) { e.preventDefault(); const bs = document.getElementById('buddy-search'); if (bs) bs.focus(); return; }
  if (e.key === '+' || e.key === '=') { S.zoom = Math.min(160, (S.zoom || 100) + 5); save(); applyZoom(); return; }
  if (e.key === '-' || e.key === '_') { S.zoom = Math.max(50, (S.zoom || 100) - 5); save(); applyZoom(); return; }
  if (e.key === '0') { S.zoom = 100; save(); applyZoom(); return; }
  if (/^[1-9]$/.test(e.key)) { S.zoom = parseInt(e.key, 10) * 10; save(); applyZoom(); return; }
  if (!['ArrowDown','ArrowUp','ArrowLeft','ArrowRight'].includes(e.key)) return;
  const items = Array.from(document.querySelectorAll('#buddy-nav [data-buddy]'));
  if (!items.length) return;
  e.preventDefault();
  const curId = (S.sel || '').startsWith('buddy:') ? S.sel.slice(6) : null;
  let idx = items.findIndex(el => el.dataset.buddy === curId);
  if (e.key === 'ArrowDown') idx = idx + 1;
  else if (e.key === 'ArrowUp') idx = idx - 1;
  else if (e.key === 'ArrowLeft') idx = 0;
  else if (e.key === 'ArrowRight') idx = items.length - 1;
  idx = Math.max(0, Math.min(items.length - 1, idx));
  show('buddy:' + items[idx].dataset.buddy);
});
/* ---------- sidebar resize ---------- */
(function initSbResize(){
  const sb = document.getElementById('sidebar');
  function apply(){ const w = S.sbWidth || 308; sb.style.width = w + 'px'; sb.style.flex = '0 0 ' + w + 'px'; }
  apply();
  const h = document.getElementById('sb-resize');
  let sx = null, sw = 0;
  h.addEventListener('pointerdown', e => { sx = e.clientX; sw = sb.getBoundingClientRect().width; h.setPointerCapture(e.pointerId); e.preventDefault(); });
  h.addEventListener('pointermove', e => { if (sx === null) return; const w = Math.min(560, Math.max(220, sw + e.clientX - sx)); sb.style.width = w + 'px'; sb.style.flex = '0 0 ' + w + 'px'; });
  const done = () => { if (sx === null) return; sx = null; S.sbWidth = Math.round(sb.getBoundingClientRect().width); save(); };
  h.addEventListener('pointerup', done);
  h.addEventListener('pointercancel', done);
})();
/* ---------- prev/next/back ---------- */
function goBack(){ const p = navHist.pop(); show(p || 'view:tree', false); }
function stepBuddy(d){
  const ids = BUDDIES.map(b => b.id);
  let i = S.sel.startsWith('buddy:') ? ids.indexOf(S.sel.slice(6)) : (d > 0 ? -1 : 0);
  i = (i + d + ids.length) % ids.length;
  show('buddy:' + ids[i]);
}
/* ---------- change journal ---------- */
if (!Array.isArray(S.journal)) S.journal = [];
function logChange(type, buddyId, desc, before, after){
  S.journal.push({t: Date.now(), type, buddy: buddyId, desc, before: before == null ? null : before, after: after == null ? null : after});
  save(); renderJournal();
}
function renderJournal(){
  const bar = document.getElementById('journal-bar'); if (!bar) return;
  const n = S.journal.length;
  if (!n) { bar.classList.remove('show'); bar.innerHTML = ''; return; }
  const items = S.journal.map(c => '<li>' + escHtml(c.desc) + '<span class="jtime">' + new Date(c.t).toLocaleString() + '</span></li>').join('');
  bar.innerHTML = '<button class="linkbtn" id="j-revert">Revert (' + n + ')</button>'
    + '<button class="linkbtn" id="j-toggle">What changed?</button>'
    + '<ul>' + items + '</ul>';
  bar.classList.add('show');
}
function applyBrand(){
  const bn = document.getElementById('brand-name'); const name = S.appName || 'Buddies';
  if (bn && document.activeElement !== bn) bn.textContent = name;
  document.title = name;
}
function revertJournal(){
  const js = S.journal.slice().reverse(), n = js.length;
  js.forEach(c => {
    if (c.type === 'rename') { if (c.before == null) delete S.names[c.buddy]; else S.names[c.buddy] = c.before; }
    else if (c.type === 'brand') { if (c.before == null) delete S.appName; else S.appName = c.before; applyBrand(); }
    else if (c.type === 'notes') { S.notes[c.buddy] = c.before || ''; }
    else if (c.type === 'move') { const reg = (byId[c.buddy] || {}).parent; if (c.before === reg) delete S.parents[c.buddy]; else S.parents[c.buddy] = c.before; }
  });
  S.journal = []; save(); buildKids(); renderNav(); refreshViews();
  if (S.sel.startsWith('buddy:')) renderBuddy(S.sel.slice(6));
  renderJournal();
  toast('Reverted ' + n + ' change' + (n === 1 ? '' : 's') + '.');
}
function buddyStandaloneUrl(id){
  return 'https://davedellaquila.github.io/buddy-tree/#/buddy:' + id + '/standalone';
}
function saveToDesktop(id){
  const b = byId[id]; if (!b) return;
  const url = buddyStandaloneUrl(id);
  const isMac = /mac/i.test(navigator.platform || '') || /mac/i.test(navigator.userAgent || '');
  let filename, content, type;
  if (isMac) {
    filename = b.name + '.webloc';
    content = '<?xml version="1.0" encoding="UTF-8"?>' + String.fromCharCode(10)
      + '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">' + String.fromCharCode(10)
      + '<plist version="1.0"><dict><key>URL</key><string>' + url + '</string></dict></plist>';
    type = 'application/xml';
  } else {
    filename = b.name + '.url';
    content = '[InternetShortcut]' + String.fromCharCode(13,10) + 'URL=' + url + String.fromCharCode(13,10);
    type = 'text/plain';
  }
  const blob = new Blob([content], {type: type});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = filename;
  document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 800);
  toast('Saved ' + filename + ' ' + String.fromCharCode(8212) + ' move it to your desktop.');
}
/* ---------- ingest ---------- */
async function dumpIngest(id, keepText){
  const ta = document.getElementById('bp-ingest'), st = document.getElementById('ingest-status');
  const text = ta.value.trim();
  if (!text) return;
  const b = byId[id];
  const stamp = new Date().toLocaleString();
  const entry = '## ' + stamp + String.fromCharCode(10,10) + text + String.fromCharCode(10,10);
  if (!ghToken() || !b.repo) { if (st) st.textContent = 'Add a GitHub token above to unlock ingest.'; return; }
  if (st) st.textContent = 'Dumping\u2026';
  try {
    const cur = await ghGetFile(b.repo, 'docs/ingest.md') || '# Ingest log \u2014 ' + b.name + String.fromCharCode(10,10);
    await ghPutFile(b.repo, 'docs/ingest.md', b64encode(cur + entry), 'Ingest dump for ' + id);
    if (!keepText) ta.value = '';
    if (st) st.textContent = 'Dumped to ' + b.repo + '/docs/ingest.md';
  } catch (err) { if (st) st.textContent = 'Save failed: ' + (err.message || err); }
  renderIngestFeed(id);
}
function parseIngest(md){
  return md.split(/^## /m).slice(1).map(p => {
    const nl = p.indexOf(String.fromCharCode(10));
    return {stamp: p.slice(0, nl).trim(), body: p.slice(nl).trim()};
  }).reverse();
}
async function renderIngestFeed(id){
  const feed = document.getElementById('ingest-feed'); if (!feed) return;
  const b = byId[id];
  let entries = [];
  if (ghToken() && b.repo) {
    const md = await ghGetFile(b.repo, 'docs/ingest.md');
    if (md) entries = parseIngest(md);
  } else {
    try { entries = (JSON.parse(localStorage.getItem('ingest:' + id) || '[]')).map(e => ({stamp: new Date(e.t).toLocaleString(), body: e.text})).reverse(); } catch (e) {}
  }
  if (!entries.length) { feed.innerHTML = '<p class="fineprint">No dumps yet.</p>'; return; }
  feed.innerHTML = '<p class="fineprint">' + entries.length + ' dump' + (entries.length === 1 ? '' : 's') + ' \u2014 most recent:</p>'
    + '<div class="attn"><div class="attn-body"><div class="attn-text">' + escHtml(entries[0].body.slice(0, 300)) + (entries[0].body.length > 300 ? '\u2026' : '') + '</div>'
    + '<div class="attn-date">' + escHtml(entries[0].stamp) + '</div></div></div>';
}
/* ---------- GitHub repo write-back (photos + shared notes) ---------- */
function ghToken(){ return S.ghToken || ''; }
async function ghApi(path, method, body){
  const t = ghToken(); if (!t) throw new Error('Add a GitHub token first.');
  const r = await fetch('https://api.github.com' + path, {
    method: method || 'GET',
    headers: {'Authorization': 'Bearer ' + t, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'},
    body: body ? JSON.stringify(body) : undefined
  });
  if (!r.ok) throw new Error('GitHub ' + r.status);
  return r.status === 204 ? null : await r.json();
}
async function ghPutFile(repo, path, b64, msg){
  let sha;
  try { const ex = await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path); sha = ex.sha; } catch (e) {}
  const body = {message: msg, content: b64}; if (sha) body.sha = sha;
  await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path, 'PUT', body);
}
async function ghGetFile(repo, path){
  try {
    const j = await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path);
    if (j && j.content) return new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\\n/g, '')), c => c.charCodeAt(0)));
  } catch (e) {}
  return null;
}
function b64encode(str){ const bytes = new TextEncoder().encode(str); let bin = ''; bytes.forEach(b => { bin += String.fromCharCode(b); }); return btoa(bin); }
function blobToB64(blob){ return new Promise((res, rej) => { const fr = new FileReader(); fr.onload = () => res(String(fr.result).split(',')[1]); fr.onerror = rej; fr.readAsDataURL(blob); }); }
function loadHeicLib(){
  return new Promise((res, rej) => {
    if (window.heic2any) return res();
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js';
    s.onload = res; s.onerror = () => rej(new Error('HEIC converter failed to load'));
    document.head.appendChild(s);
  });
}
/* ---------- photos ---------- */
async function loadPhotos(id){
  const strip = document.getElementById('pstrip'); if (!strip) return;
  const b = byId[id];
  const seeds = (b.photos || []).map(u => ({src: u, href: u}));
  let repo = [];
  try {
    const r = await fetch('https://api.github.com/repos/davedellaquila/buddy-tree/contents/photos/' + id);
    if (r.ok) { const j = await r.json(); repo = (Array.isArray(j) ? j : []).filter(f => f.type === 'file').map(f => ({src: f.download_url, href: f.download_url})); }
  } catch (e) {}
  const all = seeds.concat(repo.filter(x => !seeds.some(s => s.src === x.src)));
  strip.innerHTML = all.map(p => '<a href="' + escHtml(p.href) + '" target="_blank" rel="noopener"><img src="' + escHtml(p.src) + '" loading="lazy" alt=""></a>').join('');
  const st = document.getElementById('pstat');
  if (st) st.textContent = all.length
    ? all.length + ' photo' + (all.length === 1 ? '' : 's') + ' \u2014 stored in the buddy-tree repo under photos/' + id + '/'
    : 'No photos yet \u2014 drop some below. They land in the buddy-tree repo under photos/' + id + '/';
}
async function handlePhotoFiles(id, files){
  const st = document.getElementById('pstat');
  const list = Array.from(files || []).filter(f => /^image\//.test(f.type) || /\.hei[cf]$/i.test(f.name));
  if (!list.length) { toast('No image files in that drop.'); return; }
  if (!ghToken()) { toast('Add your GitHub token first — click the token pill (top right).'); document.getElementById('token-pop').classList.add('show'); return; }
  let n = 0;
  for (const f of list) {
    try {
      let blob = f, ext = (f.name.split('.').pop() || 'jpg').toLowerCase();
      if (/\.hei[cf]$/i.test(f.name) || f.type === 'image/heic' || f.type === 'image/heif') {
        if (st) st.textContent = 'Converting HEIC\u2026';
        await loadHeicLib();
        blob = await window.heic2any({blob: f, toType: 'image/jpeg', quality: 0.92});
        ext = 'jpg';
      }
      if (!/^(jpg|jpeg|png|gif|webp)$/.test(ext)) ext = 'jpg';
      const b64 = await blobToB64(blob);
      const safe = (f.name.replace(/\.[^.]+$/, '').replace(/[^\w\-]+/g, '_').slice(0, 40) || 'photo');
      await ghPutFile('buddy-tree', 'photos/' + id + '/' + Date.now() + '-' + safe + '.' + ext, b64, 'Add photo for ' + id);
      n++;
      if (st) st.textContent = 'Uploaded ' + n + '/' + list.length + '\u2026';
    } catch (err) { toast('Photo failed: ' + (err.message || err)); }
  }
  loadPhotos(id);
}
function renderTokenRow(id){
  const st = document.getElementById('pstat'); if (!st || document.getElementById('ghtok')) return;
  const d = document.createElement('div'); d.className = 'ghtoken';
  d.innerHTML = '<input type="password" id="ghtok" placeholder="GitHub token (repo scope) \u2014 stored on this device only" aria-label="GitHub token">'
    + '<button class="linkbtn" id="ghtok-save">Save token</button>';
  st.after(d);
  document.getElementById('ghtok-save').addEventListener('click', () => {
    const v = document.getElementById('ghtok').value.trim();
    if (v) { S.ghToken = v; save(); d.remove(); toast('Token saved on this device.'); loadSharedNotes(id); }
  });
}
function initPhotoDrop(id){
  const z = document.getElementById('pdrop'); if (!z) return;
  ['dragenter', 'dragover'].forEach(ev => z.addEventListener(ev, e => { e.preventDefault(); z.classList.add('over'); }));
  ['dragleave', 'drop'].forEach(ev => z.addEventListener(ev, e => { e.preventDefault(); z.classList.remove('over'); }));
  z.addEventListener('drop', e => handlePhotoFiles(id, e.dataTransfer.files));
  z.addEventListener('click', () => {
    const inp = document.createElement('input'); inp.type = 'file'; inp.accept = 'image/*,.heic,.heif'; inp.multiple = true;
    inp.addEventListener('change', () => handlePhotoFiles(id, inp.files));
    inp.click();
  });
  if (!ghToken()) { const tp = document.getElementById('token-pop'); if (tp) tp.classList.add('show'); }
}
/* ---------- shared notes ---------- */
function updateTokenPill(){
  const has = !!ghToken();
  const pill = document.getElementById('token-pill');
  if (!pill) return;
  pill.className = has ? 'ok' : 'need';
  document.getElementById('token-pill-icon').textContent = has ? '\u2713' : '\U0001f511';
  document.getElementById('token-pill-text').textContent = has ? 'GitHub' : 'Token needed';
}
function initTokenPill(){
  const pill = document.getElementById('token-pill'), pop = document.getElementById('token-pop');
  if (!pill || !pop) return;
  pill.addEventListener('click', e => { e.stopPropagation(); pop.classList.toggle('show'); });
  document.addEventListener('click', e => { if (!e.target.closest('#token-pop') && !e.target.closest('#token-pill')) pop.classList.remove('show'); });
  document.getElementById('ghtok-global-save').addEventListener('click', () => {
    const v = document.getElementById('ghtok-global').value.trim();
    if (!v) return;
    S.ghToken = v; save();
    const mm = S.sel.match(/^buddy:(.+)$/); refreshTokenUI(mm ? mm[1] : null);
    const chk = document.getElementById('token-saved-check'); chk.classList.add('show');
    setTimeout(() => { chk.classList.remove('show'); pop.classList.remove('show'); }, 1800);
    toast('\u2713 Token saved on this device.');
  });
  document.getElementById('ghtok-global-clear').addEventListener('click', () => {
    S.ghToken = ''; save();
    const m3 = S.sel.match(/^buddy:(.+)$/); refreshTokenUI(m3 ? m3[1] : null);
    document.getElementById('ghtok-global').value = '';
    toast('Token removed.');
  });
  updateTokenPill();
}
function centerOnBuddy(id){
  const tz = document.getElementById('treezoom');
  const node = tz ? tz.querySelector('.node[data-buddy="' + id + '"]') : null;
  if (!tz || !node) return;
  const nr = node.getBoundingClientRect(), tr = tz.getBoundingClientRect();
  tz.scrollLeft += (nr.left + nr.width / 2) - (tr.left + tr.width / 2);
  tz.scrollTop += (nr.top + nr.height / 2) - (tr.top + tr.height / 2);
}
function firstSearchMatch(){
  const q = (document.getElementById('buddy-search').value || '').toLowerCase().trim();
  const words = q.split(/\s+/).filter(Boolean);
  if (!words.length) return null;
  for (const b of BUDDIES) {
    const hay = ((b.name || '') + ' ' + (b.tagline || '')).toLowerCase();
    if (words.every(w => hay.includes(w))) return b.id;
  }
  return null;
}
function initSearch(){
  const bs = document.getElementById('buddy-search');
  if (bs && !bs.dataset.init) {
    bs.dataset.init = '1';
    bs.addEventListener('input', () => {
      renderNav();
      if (S.sel === 'view:tree') { const m = firstSearchMatch(); if (m) centerOnBuddy(m); }
    });
  }
}
function refreshTokenUI(id){
  updateTokenPill();
  updateTokenGating(id);
  if (id && S.sel === 'buddy:' + id) {
    loadSharedNotes(id);
    renderIngestFeed(id);
    const pz = document.getElementById('pstat');
    if (pz && ghToken()) pz.textContent = 'Ready — drop photos to publish to the repo.';
  }
}
function updateTokenGating(id){
  const has = !!ghToken();
  const banner = document.getElementById('token-banner');
  if (banner) banner.classList.toggle('show', !has);
  const sn = document.getElementById('bp-shared-notes');
  if (sn) {
    sn.disabled = !has;
    sn.placeholder = has ? 'Shared notes\u2026' : 'Add a GitHub token above to unlock shared notes.';
    const oldW = document.getElementById('shared-token-warn'); if (oldW) oldW.remove();
    if (!has) {
      sn.value = '';
      const w = document.createElement('div');
      w.id = 'shared-token-warn'; w.className = 'tokenwarn';
      w.innerHTML = '⚠️ <b>Shared notes are off — you gotta go get the token, bro.</b><br>Nothing you type here will save until then. <a href="https://github.com/settings/tokens/new" target="_blank" rel="noopener">Get a GitHub token</a> (classic token, <b>repo</b> scope), then paste it above — it never leaves this device.';
      if (sn.parentNode) sn.parentNode.insertBefore(w, sn.nextSibling);
    }
  }
  const ig = document.getElementById('bp-ingest');
  if (ig) { ig.disabled = !has; ig.placeholder = has ? ig.placeholder : 'Add a GitHub token above to unlock ingest.'; }

  const pz = document.getElementById('pdrop');
  if (pz) pz.classList.toggle('locked', !has);
}
async function loadSharedNotes(id){
  const ta = document.getElementById('bp-shared-notes'), st = document.getElementById('shared-status');
  if (!ta) return;
  const b = byId[id];
  if (!ghToken() || !b.repo) { if (st) st.textContent = ghToken() ? 'No repo linked for shared notes.' : 'Locked \u2014 add a GitHub token above.'; return; }
  if (st) st.textContent = 'Loading\u2026';
  const txt = await ghGetFile(b.repo, 'docs/notes.md');
  ta.value = txt || '';
  if (st) st.textContent = txt == null ? 'No shared notes yet.' : 'Synced from ' + b.repo + '/docs/notes.md';
  let t = null;
  ta.addEventListener('input', () => {
    clearTimeout(t);
    if (st) st.textContent = 'Saving\u2026';
    t = setTimeout(async () => {
      try { await ghPutFile(b.repo, 'docs/notes.md', b64encode(ta.value), 'Update shared notes'); if (st) st.textContent = 'Saved to ' + b.repo + '/docs/notes.md'; }
      catch (err) { if (st) st.textContent = 'Save failed: ' + (err.message || err); }
    }, 900);
  });
}
document.addEventListener('click', e => {
  if (e.target.closest && (e.target.closest('#bp-close') || e.target.closest('#bp-close-x'))) { closeDetail(); return; }
  if (e.target.closest && e.target.closest('#menu-btn')) { document.getElementById('sidebar').classList.toggle('open'); return; }
  if (e.target.closest && e.target.closest('#ghtok2-save')) {
    const v = document.getElementById('ghtok2').value.trim();
    if (!v) return;
    S.ghToken = v; save();
    const m2 = S.sel.match(/^buddy:(.+)$/); refreshTokenUI(m2 ? m2[1] : null);
    toast('Token saved on this device.');
    return;
  }
  if (e.target.closest && e.target.closest('#bp-desktop')) { const m = S.sel.match(/^buddy:(.+)$/); if (m) saveToDesktop(m[1]); return; }
  if (e.target.closest && e.target.closest('#sa-full')) { try { location.hash = '#/' + S.sel; } catch (e) {} document.body.classList.remove('standalone'); return; }
  if (e.target.closest && e.target.closest('.grip')) { e.preventDefault(); return; }
  const vb = e.target.closest('[data-view]');
  if (vb) { show('view:' + vb.dataset.view); return; }
  const pb = e.target.closest('[data-plan]');
  if (pb) { e.preventDefault(); show('plan:' + pb.dataset.plan); return; }
  const sb2 = document.getElementById('sidebar');
  if (sb2) sb2.classList.remove('open');
  const bb = e.target.closest('[data-buddy]');
  if (bb) { show('buddy:' + bb.dataset.buddy); return; }
  const sb = e.target.closest('[data-seen]');
  if (sb) { S.seen[sb.dataset.seen] = Date.now(); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const sa = e.target.closest('[data-seen-all]');
  if (sa) { (byId[sa.dataset.seenAll].attention || []).forEach(a => S.seen[a.id] = Date.now()); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const gt = e.target.closest('[data-goto]');
  if (gt) { e.preventDefault(); show('buddy:' + gt.dataset.goto); return; }
  const nb = e.target.closest('[data-navbtn]');
  if (nb) { const k = nb.dataset.navbtn; if (k === 'back') goBack(); else stepBuddy(k === 'next' ? 1 : -1); return; }
  if (e.target.closest('#j-revert')) { revertJournal(); return; }
  if (e.target.closest('#j-toggle')) { document.getElementById('journal-bar').classList.toggle('open'); return; }
  const rp = e.target.closest('#reset-parents');
  if (rp) { S.parents = {}; save(); buildKids(); renderNav(); refreshViews();
    if (S.sel.startsWith('buddy:')) renderBuddy(S.sel.slice(6));
    toast('Hierarchy reset to the registry.'); return; }
});
refreshViews();
(function initRoute(){
  const m = locHash().match(/^#\/(buddy:[^\/]+|view:[^\/]+|plan:[^\/]+)(\/standalone)?$/);
  if (m) { document.body.classList.toggle('standalone', !!m[2]); show(m[1], false); }
  else show(S.sel || 'view:tree');
  window.addEventListener('hashchange', () => {
    const mm = locHash().match(/^#\/(buddy:[^\/]+|view:[^\/]+|plan:[^\/]+)(\/standalone)?$/);
    if (!mm) return;
    document.body.classList.toggle('standalone', !!mm[2]);
    if (mm[1] !== S.sel) show(mm[1], false);
  });
})();
renderJournal();
initTokenPill();
initSearch();
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
<button id="menu-btn" aria-label="Open menu">\u2630</button>
<aside id="sidebar">
<div id="sb-resize" title="Drag to resize sidebar"></div>
  <div class="brand"><div class="eyebrow">Project Buddy &middot; macro view</div><h1 id="brand-name" title="Click to rename">Buddies</h1><div class="bcount">NBUD buddies &middot; one family</div></div>
  <div class="nav-sec"><h3>Views</h3><div id="view-nav"></div></div>
  <div class="nav-sec">
  <div style="padding:0 10px 8px"><input type="search" id="buddy-search" placeholder="Search buddies\u2026" aria-label="Search buddies"
    style="width:100%;box-sizing:border-box;background:#0d1117;border:1px solid #30363d;color:#e6edf3;border-radius:8px;padding:7px 10px;font-size:13px"></div>
  <h3>Buddies <span id="attn-pill" class="zero">0</span></h3><div id="buddy-nav"></div></div>
  <div class="nav-sec"><h3>Business Plans</h3><div id="plan-nav"></div></div>
</aside>
<main id="main">
<div id="journal-bar"></div>
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
    out = out.replace("__BUILD__", BUILD_NUM)
    open(f"{HERE}/index.html", "w").write(out)
    print("wrote index.html", len(out), "bytes")


if __name__ == "__main__":
    build()
