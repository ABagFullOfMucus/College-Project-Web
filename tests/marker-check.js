// marker-check.js — kiem tra hop dong cua kien truc "mỏ neo" (Option C):
// moi noi dung bi bat bang :target deu co mot <span class="admin-target" id=...>
// o DANG TRUOC .admin, va khi mỏ neo duoc nhắm thay:
//   (a) phan tu that THUC SU hien thi (khong bi ancestor display:none nuot),
//   (b) view chua no van MO,
//   (c) tong-quan dung lai (tru khi chinh no nam trong tong-quan),
//   (d) mỏ neo va id deu duy nhat.
const fs = require('fs');
const path = require('path');
const { JSDOM, displayOf } = require('./domcss.js');

const ROOT = path.join(__dirname, '..');
const CSSDIR = path.join(ROOT, 'assets/css');
const CSS = fs.readdirSync(CSSDIR).filter(f => f.endsWith('.css'))
  .map(f => fs.readFileSync(path.join(CSSDIR, f), 'utf8')).join('\n');

let pass = 0, fail = 0;
const bad = [];
const ok = () => pass++;
const no = m => { fail++; bad.push(m); };

function visibleAt(el, doc, targetId) {
  let cur = el;
  while (cur && cur.nodeType === 1) {
    if (displayOf(CSS, cur, doc, targetId) === 'none')
      return { ok: false, by: cur.className || cur.tagName };
    cur = cur.parentElement;
  }
  return { ok: true, by: null };
}

const REVEALED = '.admin-notice, .confirm, .order-detail-row, .notice';

// Id mỏ neo cua 1 phan tu: id truc tiep, hoac bo sua doi class --xxx
// (chi tinh khi thuc su co mỏ neo cung id).
function anchorId(el, doc) {
  if (el.id) return el.id;
  for (const cl of [...el.classList]) {
    const k = cl.lastIndexOf('--');
    if (k < 0) continue;
    const m = cl.slice(k + 2);
    if (m && doc.getElementById(m)) return m;
  }
  return null;
}

const PAGES = ['admin.html', 'admin-book-new.html', 'admin-stock-import.html',
  'admin-promo-send.html', 'admin-order-new.html',
  'cart.html', 'checkout.html', 'index.html'];

console.log('=== 1. Phan tu dieu khien boi mỏ neo / :target ===');
for (const p of PAGES) {
  const fp = path.join(ROOT, p);
  if (!fs.existsSync(fp)) { console.log('  [thieu] ' + p); continue; }
  const doc = new JSDOM(fs.readFileSync(fp, 'utf8')).window.document;
  const list = [...doc.querySelectorAll(REVEALED)].filter(el => anchorId(el, doc));
  console.log('  ' + p + ': ' + list.length + ' phan tu dieu khien duoc mỏ neo');
}

console.log('\n=== 2. admin.html: tung phan tu that co hien len duoc khong ? ===');
{
  const doc = new JSDOM(fs.readFileSync(path.join(ROOT, 'admin.html'), 'utf8')).window.document;
  const tq = doc.querySelector('.admin-view--tong-quan');
  const list = [...doc.querySelectorAll(REVEALED)].filter(el => anchorId(el, doc));
  console.log('  ' + list.length + ' phan tu that co mỏ neo');

  for (const el of list) {
    const id = anchorId(el, doc);
    const label = '<' + el.tagName.toLowerCase() + '.' + String(el.className).split(/\s+/)[0] + '>';

    // (0) id/mỏ neo ton tai va dung vi tri:
    //   - id dung truc tiep tren phan tu that (vd #bao-cao) -> hop le
    //   - id dung tren mỏ neo o dau trang -> phai nam TRUOC .admin
    const mk = doc.getElementById(id);
    if (!mk) no(label + ': thieu #' + id);
    else if (mk === el) ok();
    else if (mk.classList.contains('admin-target')) {
      ok();
      const adm = doc.querySelector('.admin');
      // 4 = DOCUMENT_POSITION_FOLLOWING: .admin nam SAU mỏ neo
      if (!(mk.compareDocumentPosition(adm) & 4))
        no(label + ': mỏ neo #' + id + ' khong nam truoc .admin');
      else ok();
    } else no(label + ': #' + id + ' nam sai vi tri (khong phai mỏ neo cung khong phai chinh no)');

    // (1) luc chua co :target -> phai AN
    if (visibleAt(el, doc, '').ok) no(label + ': khong target ma van hien thi');
    else ok();

    // (2) khi mỏ neo la :target -> PHAI hien thi
    const on = visibleAt(el, doc, id);
    if (on.ok) ok();
    else no(label + ': mỏ neo #' + id + ' duoc nhắm nhung bi an boi .' + on.by);

    // (3) view chua no van mo
    const view = el.closest ? el.closest('.admin-view') : null;
    if (view) {
      if (visibleAt(view, doc, id).ok) ok();
      else no(label + ': view chua no BI DONG khi #' + id + ' la :target');
      // (4) tong-quan: nam TRONG tong-quan thi phai mo; nam view khac thi phai dung
      if (view === tq) ok();
      else if (tq && !visibleAt(tq, doc, id).ok) ok();
      else if (tq) no(label + ': mỏ neo #' + id + ' de .admin-view--tong-quan MO song song');
    } else ok();
  }
}

console.log('\n=== 3. Khong con id trung lap ===');
{
  const doc = new JSDOM(fs.readFileSync(path.join(ROOT, 'admin.html'), 'utf8')).window.document;
  const seen = new Map();
  for (const n of doc.querySelectorAll('[id]'))
    seen.set(n.id, (seen.get(n.id) || 0) + 1);
  const dup = [...seen].filter(([, c]) => c > 1);
  dup.forEach(([id, c]) => no('id trung lap #' + id + ' (' + c + ' lan)'));
  if (!dup.length) ok();
  console.log('  ' + seen.size + ' id duy nhat' + (dup.length ? ', ' + dup.length + ' trung' : ''));
}

console.log('\n=== 4. 9 o nhan bao quan dieu khien van lien ket duoc ===');
{
  const doc = new JSDOM(fs.readFileSync(path.join(ROOT, 'admin.html'), 'utf8')).window.document;
  const labels = [...doc.querySelectorAll('label.field__label')];
  let nested = 0;
  for (const lb of labels) {
    const ctl = lb.querySelector('input, select, textarea');
    if (lb.htmlFor) { if (doc.getElementById(lb.htmlFor)) ok(); else no('label for="' + lb.htmlFor + '" thieu dieu khien'); }
    else if (ctl) { nested++; ok(); }
    else no('label khong co dieu khien: ' + lb.textContent.trim().slice(0, 30));
  }
  console.log('  ' + labels.length + ' nhan, ' + nested + ' la label ngam (khong can id)');
}

console.log('\n=== ' + pass + ' OK, ' + fail + ' LOI ===');
for (const b of bad) console.log('  X ' + b);
process.exit(fail ? 1 : 0);
