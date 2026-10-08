# INSTRUCTION — Hướng dẫn làm việc với dự án "Nhà Sách Skibidus"

> Tài liệu này mô tả **cách làm việc** với codebase: quy tắc, cấu trúc, kỹ thuật
> được phép dùng và quy trình kiểm tra. Yêu cầu sản phẩm (phải làm gì, còn thiếu gì)
> xem `PRD.md`. Nguyên tắc dưới đây cao hơn mọi sáng kiến cá nhân.

## 1. Ràng buộc cứng (không được phá)

- **Chỉ HTML + CSS.** Cấm tuyệt đối: file `.js`, thẻ `<script>`, thuộc tính sự kiện
  (`onclick=…`), code PHP, backend, cơ sở dữ liệu, `fetch`/`XMLHttpRequest`,
  `localStorage`, CDN JavaScript, thư viện ngoài.
- `tools/build.py` (Python 3) là script phát triển: chạy lúc sinh trang, **không bao giờ**
  chạy trên trình duyệt và không được đưa vào trang.
- **Không có dữ liệu thật.** Mọi "chức năng" là giao diện mô phỏng: `form` + anchor,
  HTML5 validation, hiện/ẩn bằng `:target`, `radio`/`checkbox`/`<details>` thuần CSS.
- **Giảng viên chấm trên Chrome, mở file trực tiếp** (`file://…/index.html`) từ laptop.
  Vì vậy đường dẫn tương đối phải đúng ở mọi thư mục con, không có URL tuyệt đối
  (`/assets/…`), không có ảnh/CSS hỏng (404 trong Console là lỗi).
- Tiếng Việt phải đủ dấu ở mọi trang — lỗi font = lỗi nghiệm thu.

## 2. Cấu trúc thư mục

| Đường dẫn | Vai trò |
|---|---|
| `index.html` | Trang chủ, **file HTML duy nhất ở thư mục gốc** |
| `books/book-<slug>.html` | 26 trang chi tiết sách — **sinh bởi `tools/build.py`** |
| `categories/the-loai*.html` | 10 trang thể loại, phân trang thật — **sinh bởi `tools/build.py`** |
| `shop/cart.html`, `shop/checkout.html` | Giỏ hàng, thanh toán (viết tay) |
| `search/search.html` | Tìm kiếm cơ bản + nâng cao + phân trang (viết tay) |
| `account/login.html` | Đăng nhập người mua (viết tay) |
| `admin/admin*.html` | Khu quản trị: dashboard, đơn hàng, kho sách, khách hàng, form con |
| `info/contact.html` | Liên hệ + FAQ |
| `assets/css/*.css` | 14 file CSS theo trang — thứ tự nạp trong `assets/css/README.md` |
| `assets/images/` | `logo.png`, `books/` (bìa), `hero/`, `reviews/`, `promo.jpeg` |
| `tools/build.py` | Sinh trang tĩnh từ khối `DATA` |
| `BienBanDanhGia_Web1_2025-caoth.doc` | Biên bản đánh giá = đề bài + thang điểm |

## 3. Thứ tự nạp CSS

`reset → base → components → layout → <trang> → compat` — **`compat.css` luôn cuối cùng**.

Bảng 14 file, ý nghĩa và trang nào nạp file nào: đọc **`assets/css/README.md`** trước khi
đụng CSS. Thêm file CSS mới phải chèn đúng vị trí trong bảng đó để cascade vẫn đúng
(file sau ghi đè file trước).

Mỗi trang chỉ nạp bộ của mình (trang sách nạp `book.css`, không nạp `home.css`). Trang
cần class của trang khác thì nạp thêm file đó (ví dụ `cart.html` nạp thêm `book.css` vì
dùng `.breadcrumb`, `.qty`; `checkout.html` nạp cả `cart.css` vì dùng `.cart-summary`).

## 4. File sinh tự động — quy tắc số 1

`books/*.html`, `categories/*.html` và hai khối đánh dấu `BEGIN/END` trong `index.html`
do `tools/build.py` sinh ra:

```bash
python3 tools/build.py
```

- **Không sửa tay** các file này — lần chạy sau ghi đè và mất thay đổi.
- Thêm/sửa sách, thể loại: sửa khối `DATA`, `CATEGORIES`, `FEATURED`, `COVERS` trong
  `build.py` rồi chạy lại. Script có `assert` (trùng slug, thiếu ảnh bìa, giá cũ ≤ giá bán,
  sai thể loại, sai số điểm nổi bật) nên lỗi lộ ra ngay trước khi ghi file.
- `COVERS` phải khai kích thước thật của ảnh (dùng cho `width`/`height`, tránh nhảy bố cục).
- `PER_PAGE = 3` sách/trang thể loại — đổi ở đó, đừng sửa tay HTML sinh ra.

## 5. Kỹ thuật tương tác thuần CSS (dùng thống nhất cả dự án)

| Tính năng | Cách làm | Ví dụ có sẵn |
|---|---|---|
| Thông báo sau khi submit | `<form action="#id">` + CSS `:target` (`.notice`, `.login__notice`, `.admin-notice`) | mọi trang |
| Hành động nguy hiểm (xoá, đăng xuất) | Xác nhận **2 bước**: link mở khối `.confirm`, nút thật mới trỏ tới kết quả | `shop/cart.html`, `admin/admin.html` |
| Hiện/ẩn menu, cột admin | `<input type="checkbox">` + `<label>` | header mọi trang, `admin/admin.html` |
| Mở/đóng nhóm bộ lọc | `<details>/<summary>` | `search/search.html` |
| Chọn 1 trong nhiều (thanh toán, tab, bước) | `<input type="radio">` + `<label>` | `shop/checkout.html` |
| Kiểm tra dữ liệu nhập | HTML5: `required`, `type`, `pattern`, `minlength`, `autocomplete` | `account/login.html`, `shop/checkout.html` |
| Nút không khả dụng | class `.pagination__link--disabled` + `aria-hidden` | `search/search.html` |
| Trạng thái chỉ đi **xuôi** | chỉ render `radio` cho bước kế tiếp, hoặc `:checked` + `disabled` cho bước sau | **chưa có — cần làm cho trạng thái đơn hàng** |

**Không dùng `:has()`** — `admin.css` đã ghi lý do: phải chạy trên Firefox ESR 115.

Giới hạn của HTML thuần phải chấp nhận: không đọc được nội dung file người dùng chọn
(`input[type=file]`), không lọc/sắp dữ liệu thật, không lưu đơn hàng — tất cả chỉ mô phỏng
bằng giao diện tĩnh. Cách mô phỏng từng yêu cầu xem `PRD.md` mục 9.

## 6. Quy ước markup

- `<html lang="vi">`, mã hoá UTF-8, **indent bằng tab**.
- Mỗi trang có: `<title>` theo mẫu `<Tên trang> - Nhà Sách Skibidus`, `meta description`,
  favicon `../assets/images/logo.png`, `skip-link`, `header` + `footer` đầy đủ.
- Link tương đối: trang trong thư mục con bắt đầu bằng `../` (trang ở gốc dùng `./`).
- Ảnh: luôn có `alt` mô tả, `width`/`height` thật, `loading="lazy"` với ảnh ngoài viewport.
- Icon trang trí: `aria-hidden="true"`. Khối ẩn mặc định `visibility: hidden`, chỉ `:target`
  mới hiện (không `display:none` nếu cần giữ chỗ).
- Đúng một `<h1>` mỗi trang; `form` có `label`/`fieldset`+`legend`; bảng có `th scope="col"`.

## 7. Font & màu

- `--font-heading` phải chứa đủ dấu tiếng Việt: **`"Times New Roman", Times, serif`**.
  **Tuyệt đối không đưa Georgia vào đầu stack** (thiếu dấu tiếng Việt → chữ trộn font,
  mỗi trình duyệt chọn font thay thế khác nhau). Chi tiết: `assets/css/README.md`.
- Không dùng `-webkit-font-smoothing: antialiased` (Firefox bỏ qua → chữ lệch độ đậm).
- Màu lấy biến ở `base.css` (`--color-accent`, `--color-sale`, `--color-success`…),
  không hardcode màu mới khi đã có biến tương ứng.

## 8. Thêm trang mới — checklist

1. Chép khung trang cùng loại (giữ nguyên header/footer/khối `notice`).
2. Nạp đúng bộ CSS theo `assets/css/README.md`, `compat.css` luôn cuối.
3. Sửa toàn bộ link `../` cho đúng thư mục; thêm vào menu/sidebar nếu cần.
4. Trang admin: giữ các `<span class="admin-target" id="…">` để sidebar điều hướng được,
   giữ nguyên cấu trúc `admin-sidebar` / `admin-main`.
5. Mở bằng Chrome và làm mục 9.

## 9. QA trước khi commit

```bash
python3 tools/build.py     # chạy sạch, không assert
git status --short         # chỉ có file mình chủ đích sửa
grep -rn "<script\|onclick" --include="*.html" .   # phải rỗng
```

Trên Chrome mở `file://…/index.html`:

- [ ] Console không có lỗi (ảnh/CSS 404…).
- [ ] Mọi link bấm được, không có href chết ngoài mục đích mô phỏng.
- [ ] Tiếng Việt đủ dấu, heading không trộn font.
- [ ] Submit form hiện đúng khối `:target`; để trống ô bắt buộc hiện lỗi validation.
- [ ] Breakpoint 1080 / 980 / 640 px không vỡ bố cục (kể cả trang admin có sidebar).
- [ ] Không có thẻ `<script>` hay thuộc tính `on*` lọt vào file.

## 10. Git

- Message theo thói quen hiện tại: ngày `dd-mm-yyyy` hoặc mô tả ngắn gọn.
- Một commit một chủ đề (trang mới / sửa CSS / sinh lại trang bằng `build.py`).
- Không commit file tạm, `.vscode/` (đã nằm trong `.gitignore`).
