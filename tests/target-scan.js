// Quet toan bo: moi phan tu nao bi :target anh huong den display, va khi tro
// thanh :target co THUC SU hien thi duoc khong (tinh ca toan bo ancestor).
// Cung nghiep vu 2: moi phan tu NAM TRONG mot .admin-view, khi tro thanh :target
// phai giup view do van mo — neu khong, chinh no bi cha display:none nuot mat.
// Exit 1 neu con phan tu loi => day la cong ngat nghiem ngat (regression gate).
const fs = require('fs');
const path = require('path');
const { JSDOM, displayOf } = require('./domcss.js');

const ROOT = path.join(__dirname, '..');
const ROOT_CSS = path.join(ROOT, 'assets/css');

function allCss() {
  return fs.readdirSync(ROOT_CSS)
    .filter(f => f.endsWith('.css'))
    .map(f => fs.readFileSync(path.join(ROOT_CSS, f), 'utf8'))
    .join('\n');
}

function visibleIn(css, el, doc, targetId) {
  let cur = el;
  while (cur && cur.nodeType === 1) {
    if (displayOf(css, cur, doc, targetId) === 'none')
      return { ok: false, by: cur.className || cur.tagName };
    cur = cur.parentElement;
  }
  return { ok: true, by: null };
}

const page = process.argv[2] || 'admin.html';
const css = allCss();
const dom = new JSDOM(fs.readFileSync(path.join(ROOT, page), 'utf8'));
const doc = dom.window.document;

console.log('=== ' + page + ': cac phan tu bi :target anh huong ===');
let broken = 0, ok = 0;
for (const el of doc.querySelectorAll('[id]')) {
  const id = el.id;
  const d0 = displayOf(css, el, doc, '');
  const d1 = displayOf(css, el, doc, id);
  if (d0 === d1) continue;                    // khong dung :target de mo/ren
  const v = visibleIn(css, el, doc, id);
  const tag = el.tagName.toLowerCase();
  const cls = (el.className && typeof el.className === 'string')
    ? '.' + el.className.split(/\s+/)[0] : '';
  console.log(`  ${v.ok ? 'OK  ' : 'BROKEN'} #${id}  <${tag}${cls}>  ${d0} -> ${d1}`
    + (v.ok ? '' : `   (bi an boi .${v.by})`));
  if (v.ok) ok++; else broken++;
}

console.log('\n=== view co van mo khi phan tu ben trong no la :target ? ===');
for (const el of doc.querySelectorAll('[id]')) {
  const view = el.closest ? el.closest('.admin-view') : null;
  if (!view) continue;
  const v = visibleIn(css, view, doc, el.id);
  const cls = typeof el.className === 'string' ? el.className.split(/\s+/)[0] : '';
  if (v.ok) { ok++; console.log(`  OK     #${el.id} -> ${cls}`); }
  else {
    broken++;
    console.log(`  BROKEN #${el.id} -> view .${view.className.replace('admin-view ', '')} BI DONG`);
  }
}

console.log(`\n  => ${ok} OK, ${broken} BROKEN`);
process.exit(broken ? 1 : 0);
