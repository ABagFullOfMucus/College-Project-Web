// Kiem tra THUC TE: khi 1 .confirm/.admin-notice tro thanh :target, co THUC SU
// hien thi khong? Phai di qua TOAN BO ancestor vi .admin-view { display:none }
// co the nuot mat no. Dung displayOf (co chi so dac ta) chu khong theo thu tu
// khop — neu theo thu tu thi .admin-notice{display:none} o cuoi file se bao sai.
const fs = require('fs');
const path = require('path');
const { JSDOM, displayOf } = require('./domcss.js');

const ROOT = path.join(__dirname, '..');
let pass = 0, fail = 0;
const bad = [];

function visibleAt(css, el, doc, targetId) {
  let cur = el;
  while (cur && cur.nodeType === 1) {
    if (displayOf(css, cur, doc, targetId) === 'none')
      return { ok: false, blockedBy: cur.className || cur.tagName };
    cur = cur.parentElement;
  }
  return { ok: true, blockedBy: null };
}

const pages = ['admin.html', 'admin-book-new.html', 'admin-stock-import.html',
  'admin-promo-send.html', 'admin-order-new.html',
  'cart.html', 'checkout.html', 'index.html'];

function cssFor(names) {
  return names.map(n => {
    const p = path.join(ROOT, 'assets/css', n + '.css');
    return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '';
  }).join('\n');
}

function check(page) {
  const html = fs.readFileSync(path.join(ROOT, page), 'utf8');
  const doc = new JSDOM(html).window.document;
  const css = cssFor(['base', 'layout', 'components', 'home', 'product',
    'cart', 'checkout', 'admin', 'admin-data']);

  const items = [...doc.querySelectorAll('.confirm, .admin-notice, .notice')];
  if (!items.length) { console.log('  [skip] ' + page + ' khong co .confirm/.notice'); return; }

  for (const c of items) {
    // Id co truc tiep tren the, hoac da duoc chuyen thanh bo sua doi class
    // (--xxx) keo theo mỏ neo o dau trang. Chi tinh bo sua doi khi thuc su
    // co mỏ neo cung id, de khong hieu nham class style nhu .notice--success.
    const ids = [];
    if (c.id) ids.push(c.id);
    for (const cl of [...c.classList]) {
      const k = cl.lastIndexOf('--');
      if (k < 0) continue;
      const m = cl.slice(k + 2);
      if (m && doc.getElementById(m)) ids.push(m);
    }
    if (!ids.length) {
      fail++; bad.push(page + ': ' + (c.className || c.tagName) + ' khong co id/mo doi');
      continue;
    }

    for (const id of ids) {
      const off = visibleAt(css, c, doc, '');
      if (off.ok) { fail++; bad.push(page + ' #' + id + ': KHONG target ma van hien thi'); }
      else pass++;

      const on = visibleAt(css, c, doc, id);
      if (on.ok) pass++;
      else { fail++; bad.push(page + ' #' + id + ': target nhung BI AN boi ancestor .' + on.blockedBy); }
    }
  }
  console.log('  ' + page + ': ' + items.length + ' confirm/notice');
}

console.log('=== Kiem tra hien thi thuc te cua cac .confirm ===');
for (const p of pages) {
  if (!fs.existsSync(path.join(ROOT, p))) { console.log('  [thieu] ' + p); continue; }
  check(p);
}

console.log('=== View Cai dat khi dang xac nhan ===');
{
  const doc = new JSDOM(fs.readFileSync(path.join(ROOT, 'admin.html'), 'utf8')).window.document;
  const css = cssFor(['base', 'layout', 'components', 'admin']);
  const view = doc.querySelector('.admin-view--cai-dat');
  for (const id of ['xac-nhan-luu', 'xac-nhan-khoi-phuc']) {
    const r = visibleAt(css, view, doc, id);
    if (r.ok) pass++;
    else { fail++; bad.push('admin.html: view Cai dat BI DONG khi #' + id + ' la :target'); }
    console.log('  #' + id + ': view Cai dat ' + (r.ok ? 'CON MO' : 'BI DONG (ancestor .' + r.blockedBy + ')'));
  }
}

console.log('\n=== ' + pass + ' OK, ' + fail + ' LOI ===');
for (const b of bad) console.log('  X ' + b);
process.exit(fail ? 1 : 0);
