// domcss.js — mo phỏng selector CSS va tinh `display` tren jsdom, khong can
// trinh duyet. Phuc vu cac test kiem tra loi :target bi .admin-view nuot mat.
// jsdom duoc tim o ngay thu muc tests/, hoac theo bien moi truong JSDOM_PATH
// (phong khi node_modules chua duoc cai o day).
let JSDOM;
try {
  ({ JSDOM } = require('jsdom'));
} catch (e) {
  ({ JSDOM } = require(process.env.JSDOM_PATH || '/tmp/dtest/node_modules/jsdom'));
}


// Tach CSS thanh cac khop { sel, body } o tang dau.
// Khop ben trong @media duoc tra ve voi sel bat dau bang '@' — cac test se bo qua.
function rules(css) {
  const out = [];
  let i = 0, sel = '', depth = 0;
  const n = css.length;
  while (i < n) {
    const ch = css[i];
    if (ch === '/' && css[i + 1] === '*') {            // bo comment
      const e = css.indexOf('*/', i + 2);
      i = e < 0 ? n : e + 2;
      continue;
    }
    if (ch === '{') {
      if (depth === 0) { out.push({ sel: sel.trim(), body: '' }); sel = ''; }
      else out[out.length - 1].body += ch;
      depth++; i++; continue;
    }
    if (ch === '}') {
      if (depth > 1) { out[out.length - 1].body += ch; depth--; }
      else { depth = 0; sel = ''; }
      i++; continue;
    }
    if (depth === 0) sel += ch;
    else out[out.length - 1].body += ch;
    i++;
  }
  return out;
}

// Tach selector thanh cac { op, simple } — op la ' ' | '>' | '+' | '~'
function parseSel(sel) {
  const out = [];
  let buf = '', depth = 0, op = ' ';
  const push = () => { const s = buf.trim(); if (s) out.push({ op, simple: s }); buf = ''; };
  for (let i = 0; i < sel.length; i++) {
    const ch = sel[i];
    if (depth === 0 && (ch === '>' || ch === '+' || ch === '~')) { push(); op = ch; continue; }
    if (depth === 0 && /\s/.test(ch)) { if (buf.trim()) { push(); op = ' '; } continue; }
    if (ch === '[' || ch === '(') depth++;
    else if (ch === ']' || ch === ')') depth = Math.max(0, depth - 1);
    buf += ch;
  }
  push();
  return out;
}

// Cac :pseudo la phan tu (khong phai element) -> khong doi chieu duoc len element
const PSEUDO_ELEM = new Set(['before', 'after', 'first-line', 'first-letter',
  'placeholder', 'file-selector-button', 'marker', 'backdrop', 'selection', 'cue']);

function matchAttr(el, tok) {
  const inner = tok.slice(1, -1);
  const m = inner.match(/^([\w-]+)\s*(?:([~^$*|]?=)\s*(.*))?$/);
  if (!m) return false;
  if (!el.hasAttribute(m[1])) return false;
  if (!m[2]) return true;
  let val = m[3].trim();
  if ((val[0] === '"' && val[val.length - 1] === '"') || (val[0] === "'" && val[val.length - 1] === "'"))
    val = val.slice(1, -1);
  const actual = el.getAttribute(m[1]);
  switch (m[2]) {
    case '=': return actual === val;
    case '^=': return actual.startsWith(val);
    case '$=': return actual.endsWith(val);
    case '*=': return actual.includes(val);
    case '~=': return actual.split(/\s+/).includes(val);
    case '|=': return actual === val || actual.startsWith(val + '-');
    default: return false;
  }
}

function matchNth(el, arg) {
  const parent = el.parentElement;
  if (!parent) return false;
  const idx = [...parent.children].indexOf(el) + 1;
  const a = arg.trim();
  if (/^\d+$/.test(a)) return idx === parseInt(a, 10);
  if (a === 'odd') return idx % 2 === 1;
  if (a === 'even') return idx % 2 === 0;
  const m = a.match(/^([+-]?\d*)n\s*([+-]\s*\d+)?$/);
  if (!m) return false;
  const A = (m[1] === '' || m[1] === '+') ? 1 : (m[1] === '-' ? -1 : parseInt(m[1], 10));
  const B = m[2] ? parseInt(m[2].replace(/\s+/g, ''), 10) : 0;
  if (A === 0) return idx === B;
  const k = idx - B;
  return A > 0 ? (k >= 0 && k % A === 0) : (k <= 0 && k % -A === 0);
}

function matchPseudo(el, tok) {
  if (tok.startsWith('::')) return false;                 // pseudo-element
  const name = tok.slice(1);
  if (PSEUDO_ELEM.has(name)) return false;                // dang legacy :before/:after
  if (name === 'target') return el.__target === true;
  if (name === 'checked') return el.__checked === true || el.checked === true;
  if (name === 'root') return el.ownerDocument && el === el.ownerDocument.documentElement;
  if (name === 'empty') return el.childNodes.length === 0;
  if (name === 'first-child') return !el.previousElementSibling;
  if (name === 'last-child') return !el.nextElementSibling;
  if (name === 'only-child') return !el.previousElementSibling && !el.nextElementSibling;
  if (name.startsWith('not(') && name.endsWith(')'))
    return !matchComplex(el, name.slice(4, -1));
  const nth = name.match(/^nth-child\(([^)]+)\)$/);
  if (nth) return matchNth(el, nth[1]);
  return false;   // :hover :focus :invalid ... -> khong mo phong trang thai, bo qua
}

// Mot "compound" don gian: #id .class tag [attr] :pseudo
const SIMPLEX = /(::?[\w-]+(?:\([^)]*\))?|#[\w-]+|\.[\w-]+|\[[^\]]*\]|[a-zA-Z][\w-]*|\*)/g;

function matchSimple(el, s) {
  if (!el || el.nodeType !== 1) return false;
  SIMPLEX.lastIndex = 0;
  let m, any = false;
  while ((m = SIMPLEX.exec(s))) {
    const t = m[0];
    if (t === '*') { any = true; continue; }
    if (t[0] === '#') { if (el.id !== t.slice(1)) return false; any = true; }
    else if (t[0] === '.') { if (!el.classList.contains(t.slice(1))) return false; any = true; }
    else if (t[0] === '[') { if (!matchAttr(el, t)) return false; any = true; }
    else if (t[0] === ':') { if (!matchPseudo(el, t)) return false; any = true; }
    else { if ((el.tagName || '').toLowerCase() !== t.toLowerCase()) return false; any = true; }
  }
  return any;
}

// Khop day du selector — dac biet la `~` dong vai tro quyet dinh: mỏ neo phai
// la anh em truoc cua .admin thi moi mo duoc view (khong the chon toa do cha).
function matchComplex(el, sel) {
  if (typeof sel !== 'string') return false;
  const parts = parseSel(sel.trim());
  if (!parts.length) return false;
  if (!matchSimple(el, parts[parts.length - 1].simple)) return false;
  let cur = el;
  for (let i = parts.length - 2; i >= 0; i--) {
    const op = parts[i + 1].op, target = parts[i].simple;
    if (op === ' ') {
      let p = cur.parentElement;
      while (p && !matchSimple(p, target)) p = p.parentElement;
      if (!p) return false;
      cur = p;
    } else if (op === '>') {
      const p = cur.parentElement;
      if (!p || !matchSimple(p, target)) return false;
      cur = p;
    } else if (op === '+') {
      const p = cur.previousElementSibling;
      if (!p || !matchSimple(p, target)) return false;
      cur = p;
    } else {
      let p = cur.previousElementSibling;
      while (p && !matchSimple(p, target)) p = p.previousElementSibling;
      if (!p) return false;
      cur = p;
    }
  }
  return true;
}

// Chi so dac ta (a,b,c) — de lay dung quy tac thang theo thu tu cascade thay vi
// "quan thang cuoi cung" (sai voi CSS that: .admin-notice { display:none } o cuoi
// file se "thang" Rule E mac du Rule E co dac ta cao hon nhieu).
function specificity(sel) {
  let s = String(sel);
  s = s.replace(/"[^"]*"|'[^']*'/g, '');                    // bo chuoi
  const attrs = (s.match(/\[[^\]]*\]/g) || []).length;      // [attr] = 1 phan lop
  s = s.replace(/\[[^\]]*\]/g, '');
  const c = (s.match(/::[a-z-]+/gi) || []).length;          // pseudo-element
  s = s.replace(/::[a-z-]+/gi, '');
  const a = (s.match(/#[\w-]+/g) || []).length;
  const d = (s.match(/\.[\w-]+/g) || []).length;
  const pc = (s.match(/:[\w-]+(\([^)]*\))?/g) || []).length; // pseudo-class
  return [a, d + attrs + pc, c];
}
function cmpSpec(x, y) { return x[0] - y[0] || x[1] - y[1] || x[2] - y[2]; }

function displayOf(css, el, doc, targetId) {
  for (const n of doc.querySelectorAll('[id]')) n.__target = (n.id === targetId);
  for (const n of doc.querySelectorAll('input[type=checkbox],input[type=radio]'))
    n.__checked = n.hasAttribute('checked');
  let disp = null, best = null;
  for (const r of rules(css)) {
    if (!r.sel) continue;
    if (r.sel.trim().startsWith('@')) continue;            // bo qua @media / @keyframes
    for (const s of r.sel.split(',')) {
      const t = s.trim();
      if (!t || !matchComplex(el, t)) continue;
      const m = r.body.match(/(^|;|\s)display\s*:\s*([a-z-]+)/);
      if (!m) continue;
      const sp = specificity(t);
      // cang cao cang thang; bang nhau thi sau thang (>=) — dung nhu cascade
      if (!best || cmpSpec(sp, best) >= 0) { best = sp; disp = m[2]; }
    }
  }
  return disp;
}

module.exports = { JSDOM, rules, matchComplex, displayOf };




