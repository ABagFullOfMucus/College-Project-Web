# PRD — Nhà Sách Skibidus (Website bán sách)

> Product Requirements Document. Nguồn: `BienBanDanhGia_Web1_2025-caoth.doc` (đề bài
> + thang điểm) và hiện trạng codebase. Cách làm việc, quy tắc kỹ thuật: `INSTRUCTION.md`.
> Từ ngữ tiếng Anh (done/partial/missing) giữ nguyên cho ngắn gọn.

## 1. Bối cảnh & mục tiêu

- Học phần **Lập trình web và ứng dụng nâng cao**, đề tài website bán sản phẩm (sách).
- Sản phẩm cần giao: giao diện **người dùng cuối** + giao diện **quản trị**, chấm **12đ**
  (hai nhóm lớn 5.0 mỗi nhóm, các mục con 0.25 – 1.0 theo cột điểm của biên bản).
- Mục tiêu: phủ đủ mọi dòng trong biên bản bằng giao diện thuần HTML/CSS, không lỗi UI
  khi mở trực tiếp `index.html` trên Chrome.

## 2. Ràng buộc cứng

1. Chỉ HTML + CSS. Không JS/PHP/backend/CSDL (xem `INSTRUCTION.md` mục 1).
2. Không có trang thanh toán trực tuyến (biên bản: "KHÔNG yêu cầu trang thanh toán").
3. Mọi dữ liệu là dữ liệu mẫu tĩnh; "lưu", "lọc", "thống kê" là mô phỏng giao diện.
4. Chấm trên Chrome từ file; mọi lỗi font tiếng Việt, lỗi asset đều bị tính lỗi.
5. Admin phải tách biệt người dùng: URL khu quản trị khác URL người dùng thường.

## 3. Phạm vi

**Trong phạm vi:** trang chủ, thể loại (phân trang), chi tiết sách, tìm kiếm cơ bản/nâng cao,
đăng nhập, đăng ký, giỏ hàng, thanh toán, xác nhận đơn, lịch sử mua; khu admin: đăng nhập,
quản lý user, thêm/sửa/xoá sản phẩm, quản lý & lọc đơn hàng, thống kê.

**Ngoài phạm vi:** cổng thanh toán thật, gửi mail thật, xác thực phiên đăng nhập thật,
lọc kết quả tìm kiếm thật, đồng bộ dữ liệu giữa các trang.

## 4. Luồng chính

1. **Mua hàng:** Trang chủ → Thể loại (phân trang) → Chi tiết sách → Giỏ hàng *(bắt buộc đăng nhập, hiển thị thông tin người đăng nhập)* → Chọn địa chỉ (có sẵn hoặc nhập mới) + hình thức chi trả → Đặt hàng → Xem/lưu đơn hàng → Xem lịch sử mua (nhóm theo đơn).
2. **Tài khoản:** Đăng nhập / Đăng ký người mua.
3. **Quản trị:** Đăng nhập tại URL riêng → Tổng quan → Đơn hàng (lọc, cập nhật trạng thái xuôi, thống kê) → Kho sách (thêm/sửa/xoá) → Khách hàng (thêm/sửa/khóa).

## 5. Yêu cầu người dùng cuối (RF-UE)

| Mã | Yêu cầu (theo biên bản) | Tiêu chí chấp nhận | Trạng thái |
|---|---|---|---|
| RF-UE-01 | Hiển thị sản phẩm theo phân loại | 6 thể loại, mỗi thể loại 1 trang danh sách, link từ trang chủ và `categories/the-loai.html` | **DONE** — `categories/*.html` |
| RF-UE-02 | Hiển thị chi tiết sản phẩm | Trang chi tiết có ảnh, giá/giá cũ, điểm, mô tả, thông số, thêm vào giỏ | **DONE** — 26 trang `books/*.html` |
| RF-UE-03 | Tìm kiếm cơ bản theo tên (tương đối) | Ô tìm kiếm ở header mọi trang + trang `search` lớn, có kết quả hiển thị | **DONE** — giao diện đủ; mỗi từ khoá gợi ý mở 1 trang kết quả tĩnh khớp truy vấn (`search-kynangsong/vanhoc/nguyennhatanh/laptrinh.html`), dữ liệu lấy từ `tools/build.py` |
| RF-UE-04 | Tìm kiếm nâng cao (tên + phân loại + khoảng giá) | Cùng 1 form: ô từ khoá, checkbox thể loại, 2 ô giá `gia-tu`/`gia-den`, nút Tìm kiếm | **DONE** — đủ bộ lọc trên mọi trang search; trang mẫu `search-laptrinh.html` thể hiện sẵn thể loại Công nghệ được tick + khoảng giá 100.000đ–150.000đ |
| RF-UE-05 | Hiển thị phân trang cho danh mục & kết quả tìm kiếm | Thanh `1 2 3 … Trước/Sau`, số trang/tổng số hiển thị | **DONE** — phân trang thật ở thể loại; trang kết quả mẫu dùng thanh 1 trang (Trước/Sau `disabled`), đúng bản tĩnh |
| RF-UE-06 | Đăng ký làm người mua hàng (giao diện end-user) | Trang đăng ký: họ tên, email, SĐT, mật khẩu, xác nhận; validation HTML5; báo thành công | **DONE** — `account/register.html`: form HTML5 validation + thông báo `:target`, link 2 chiều với `login.html` |
| RF-UE-07 | Giỏ hàng | (a) yêu cầu đăng nhập và **tự hiển thị thông tin người đăng nhập**; (b) chọn địa chỉ của tài khoản **hoặc** nhập địa chỉ mới; (c) chọn hình thức chi trả **Trực tuyến / Tiền mặt** | **DONE** — khối “đang đăng nhập” ở `cart.html` + `checkout.html`; chọn địa chỉ đã lưu / nhập mới bằng CSS `:checked`; chi trả diễn đạt đúng Trực tuyến / Tiền mặt |
| RF-UE-08 | Hiển thị và lưu đơn hàng khi kết thúc giao dịch | Sau khi đặt hiện trang/thông báo đơn hàng có mã, danh sách hàng, tổng tiền, trạng thái | **DONE** — `shop/order-confirmation.html`: đơn SKB-2026-0841 đã lưu, đủ thông tin + link lịch sử mua |
| RF-UE-09 | Lịch sử mua hàng, **nhóm theo đơn hàng** | Trang danh sách đơn của tôi: mỗi đơn 1 khối (mã, ngày, trạng thái, tổng, link chi tiết) | **DONE** — `account/orders.html`: 3 đơn, mỗi đơn 1 khối (mã, ngày, trạng thái, sách trong đơn, tổng) |

## 6. Yêu cầu quản trị (RF-AD)

| Mã | Yêu cầu (theo biên bản) | Tiêu chí chấp nhận | Trạng thái |
|---|---|---|---|
| RF-AD-01 | Đăng nhập & đăng xuất, **URL khác người dùng bình thường** | Trang `admin/…` riêng cho đăng nhập; đăng xuất khỏi admin về trang đăng nhập admin | **DONE** — `admin/admin-login.html` (URL riêng) + toàn bộ nút Đăng xuất của 9 trang admin trỏ về đó |
| RF-AD-02 | Quản lý user: thêm/đăng ký, sửa, **khóa/mở user** | Bảng user có nút Thêm, Sửa, Khóa/Mở (trạng thái hiện trên bảng) | **DONE** — nút “Thêm user” → `admin/admin-user-new.html`; nút “Khóa” + xác nhận 2 bước trong bảng Khách hàng |
| RF-AD-03 | Thêm sản phẩm: đúng phân loại, upload hình, **hiển thị hình trước khi thêm** | Form chọn thể loại (dropdown đúng 6 thể loại), `input[type=file]` ảnh, khung xem trước | **DONE** — `admin-book-new.html`: dropdown 6 thể loại + `input[type=file]` + khung `.cover-preview` (CSS không đọc được file nên preview hiển thị ảnh mẫu) |
| RF-AD-04 | Sửa sản phẩm: hiển thị đúng thông tin trước khi sửa (đặc biệt phân loại & hình) | Form điền sẵn tên/giá/mô tả, dropdown đúng thể loại đang chọn, hiện ảnh bìa hiện tại | **DONE** — `admin-book-edit.html` |
| RF-AD-05 | Xoá sản phẩm: **đã bán → ẩn** khỏi web; **chưa bán → hỏi lại rồi xoá** | Nút Xoá + khối `.confirm` 2 bước; nhánh "đã bán" chỉ có tuỳ chọn ẩn sản phẩm, không có xoá thật | **DONE** — Kho sách: hàng đã bán → confirm “Ẩn khỏi gian sách”; hàng Chưa bán (Nhà Giả Kim) → confirm “Xác nhận xoá” |
| RF-AD-06a | Cập nhật trạng thái đơn hàng, **chỉ đi xuôi** (chưa xác nhận → đã xác nhận → đã giao/thành công/huỷ) | Không chọn được trạng thái phía sau; trạng thái cũ bị khoá | **DONE** — `admin-order-edit.html`: dãy radio `.status-flow`, trạng thái hiện tại và chưa tới đều `disabled` |
| RF-AD-06b | Lọc đơn: tình trạng / **khoảng thời gian (từ ngày – đến ngày)** / địa điểm giao (quận, huyện, thành phố) | 3 nhóm lọc có trong 1 form, có ô `type=date` từ–đến, dropdown quận/huyện/TP | **DONE** — ô Từ ngày / Đến ngày (`type=date`) + select Thành phố + Quận/Huyện trong form lọc đơn |
| RF-AD-06c | Thống kê: nhập **khoảng thời gian** → **5 khách mua cao nhất**, liệt kê **từng đơn (có link xem chi tiết)**, **tính tổng mua**, **sắp xếp giảm dần** | Form nhập từ ngày – đến ngày → bảng top 5 kèm cột tổng, mỗi đơn link sang chi tiết, thứ tự giảm dần | **DONE** — panel Thống kê trong `admin.html`: nhập khoảng thời gian → top 5 giảm dần, từng đơn có link chi tiết, cột Tổng mua |

> Ghi chú điểm: biên bản chấm từng mục (0.25 – 1.0), hai nhóm lớn 5.0, tổng cộng 12 điểm.

## 7. Yêu cầu phi chức năng (NFR)

| Mã | Yêu cầu |
|---|---|
| NFR-01 | Thuần HTML/CSS, không tài nguyên ngoài (font/icon/JS CDN) |
| NFR-02 | Hoạt động tốt khi mở bằng `file://` trên Chrome, không lỗi Console |
| NFR-03 | Tiếng Việt đủ dấu ở mọi trang; heading dùng `--font-heading` (Times New Roman), không trộn font |
| NFR-04 | Responsive ở 1080 / 980 / 640 px, kể cả trang admin có sidebar |
| NFR-05 | Ảnh có `alt` + `width`/`height`; có `skip-link`, `label`, `aria-*` đúng vai trò |
| NFR-06 | Thứ tự nạp CSS đúng bảng trong `assets/css/README.md`, `compat.css` cuối cùng |
| NFR-07 | Dữ liệu mẫu nhất quán giữa các trang (tên sách, giá, mã đơn `SKB-…`) |

## 8. Ma trận biên bản ↔ trang

| Hạng mục biên bản | Trang hiện tại |
|---|---|
| Sản phẩm theo phân loại, chi tiết, phân trang | `index.html`, `categories/*.html`, `books/*.html` |
| Tìm kiếm cơ bản / nâng cao | `search/search.html` (+ ô tìm ở header mọi trang) + 4 trang kết quả mẫu `search/search-kynangsong|vanhoc|nguyennhatanh|laptrinh.html` |
| Đăng ký người mua | *(thiếu — cần `account/register.html`)* |
| Giỏ hàng, địa chỉ, hình thức chi trả | `shop/cart.html`, `shop/checkout.html` |
| Đơn hàng khi kết thúc, lịch sử mua | `shop/checkout.html#dat-hang-thanh-cong` *(thiếu trang đơn/history)* |
| Đăng nhập & đăng xuất admin (URL riêng) | *(thiếu — cần `admin/admin-login.html`)* |
| Quản lý user (thêm/sửa/khóa) | `admin/admin.html#khach-hang`, `admin/admin-customer-edit.html` |
| Thêm/sửa/xoá sản phẩm | `admin/admin-book-new.html`, `admin/admin-book-edit.html` *(thiếu xoá)* |
| Quản lý đơn hàng, lọc, thống kê | `admin/admin.html#don-hang`, `admin/admin-order-edit.html` |

## 9. Khoảng trống & backlog (việc cần làm tiếp), ưu tiên giảm dần

> **Cập nhật sau khi triển khai:** toàn bộ mục **1–13 đã hoàn thành**. Mục 12 dựng
> 4 trang kết quả mẫu (`search/search-kynangsong.html`, `search-vanhoc.html`,
> `search-nguyennhatanh.html`, `search-laptrinh.html`) với dữ liệu lấy từ
> `tools/build.py`; chip gợi ý và form tìm/lọc ở `search.html` trỏ sang các trang
> mẫu. Mục 13 đã xoá file trùng `admin/admin-sach-moi.html` và gỡ link chết
> trong `admin-book-new.html`.

| # | Việc | RF | Ưu tiên | File liên quan | Cách làm trong giới hạn thuần CSS |
|---|---|---|---|---|---|
| 1 | Trang **đăng ký người mua** | UE-06 | **P0** | mới `account/register.html`, sửa `login.html` (bỏ notice "chưa mở") | Form HTML5 validation + `action="#dang-ky-thanh-cong"` hiện notice `:target` |
| 2 | **Lịch sử mua hàng** nhóm theo đơn | UE-09 | **P0** | mới `account/orders.html` (+ `account/order-detail.html` nếu cần) | Mỗi đơn 1 `<article>` khối `.order-card` (mã, ngày, trạng thái, tổng, danh sách sách) |
| 3 | **Đăng nhập admin URL riêng** | AD-01 | **P0** | mới `admin/admin-login.html`; sửa toàn bộ link logout `admin/*.html` về nó | Form đăng nhập mô phỏng, `action="#dang-nhap-thanh-cong"` → vào `admin.html`; tách biệt `account/login.html` |
| 4 | **Trạng thái đơn chỉ đi xuôi** | AD-06a | **P0** | `admin/admin-order-edit.html`, CSS `admin-data.css` | Thay `<select>` bằng dãy `radio` chỉ bật bước kế tiếp; bước đã qua `disabled` + nhãn "đã giao/không quay lui" |
| 5 | **Thống kê top 5 khách** theo khoảng thời gian | AD-06c | **P0** | mới khối trong `admin/admin.html` (vd. `#thong-ke`) hoặc trang `admin/admin-stats.html` | Form `từ ngày – đến ngày` `type=date` + bảng 5 dòng giảm dần, mỗi dòng liệt kê đơn có link `admin-order-edit.html`, cột Tổng mua |
| 6 | **Xoá sản phẩm** theo quy tắc đã bán/ chưa bán | AD-05 | **P1** | `admin/admin.html` (bảng Kho sách) | Nút Xoá → khối `.confirm` 2 bước; nhánh "đã bán" chỉ có nút "Ẩn khỏi web" (không có xoá thật), nhánh "chưa bán" có "Xác nhận xoá" |
| 7 | **Bộ lọc đơn hàng**: ô `từ ngày – đến ngày` + địa điểm (quận/huyện/TP) | AD-06b | **P1** | `admin/admin.html#don-hang` | Thêm 2 ô `type=date` + `select` thành phố/quận vào form lọc sẵn có (`#da-loc`) |
| 8 | **Quản lý user**: thêm user, khóa/mở | AD-02 | **P1** | `admin/admin.html#khach-hang`, mới `admin/admin-user-new.html`, sửa `admin-customer-edit.html` | Nút "Thêm user" → form; cột Trạng thái + link Khóa/Mở điều hướng `:target` |
| 9 | Giỏ hàng: **hiển thị người đang đăng nhập** + chọn địa chỉ có sẵn | UE-07 | **P1** | `shop/cart.html`, `shop/checkout.html` | Khối "Đăng nhập tài khoản: Nguyễn Văn A" + radio "Địa chỉ đã lưu / Nhập địa chỉ mới" (ẩn ô nhập bằng `:checked`) |
| 10 | Trang **xác nhận & lưu đơn hàng** riêng | UE-08 | **P1** | mới `shop/order-confirmation.html` | Giữ nguyên mã đơn, liệt kê hàng + tổng, nút "Xem lịch sử mua" → `account/orders.html` |
| 11 | **Upload ảnh có xem trước** | AD-03 | **P2** | `admin/admin-book-new.html` | CSS không đọc được file đã chọn → khung preview hiển thị ảnh mẫu + ghi chú "ảnh sẽ hiển thị tại đây"; trình bày như 1 bước có điều kiện |
| 12 | Kết quả **tìm kiếm & phân trang** giống thật hơn | UE-03/04/05 | **P2 — DONE** | `search/search*.html` (4 trang mẫu mới + hub đã nối chip/form) | Mỗi chip gợi ý mở 1 trang kết quả tĩnh khớp truy vấn; bộ lọc thể hiện đúng trạng thái đã chọn |
| 13 | Gộp trang trùng lặp `admin-book-new` / `admin-sach-moi` | — | **P2 — DONE** | `admin/` | Đã xoá `admin-sach-moi.html`, gỡ link chết trong `admin-book-new.html` |

## 10. Tiêu chí nghiệm thu (checklist chấm)

**Người dùng cuối**
- [ ] Vào được sản phẩm qua phân loại; xem chi tiết đủ thông tin; phân trang đi được trang 2.
- [ ] Ô tìm kiếm cơ bản và bộ lọc nâng cao (tên + thể loại + khoảng giá) hiển thị trên 1 trang.
- [ ] Có trang đăng ký, validation bắt lỗi, submit hiện thông báo thành công.
- [ ] Vào giỏ hàng khi "đã đăng nhập" thấy thông tin người mua; checkout chọn được địa chỉ
      có sẵn hoặc nhập mới; chọn được hình thức chi trả Trực tuyến / Tiền mặt (không có trang thanh toán).
- [ ] Đặt hàng hiện đơn hàng có mã + tổng tiền; mở được lịch sử mua, các đơn được nhóm rõ.

**Quản trị**
- [ ] Đăng nhập admin ở URL khác người dùng thường; đăng xuất về đúng trang đăng nhập admin.
- [ ] Thêm/sửa/khóa user; thêm sản phẩm đúng phân loại có ảnh xem trước; sửa sản phẩm thấy đúng dữ liệu cũ.
- [ ] Xoá sản phẩm: đã bán → chỉ cho ẩn; chưa bán → hỏi lại rồi xoá.
- [ ] Đơn hàng lọc được theo trạng thái, từ–đến ngày, địa điểm; trạng thái chỉ cập nhật xuôi.
- [ ] Thống kê: nhập khoảng thời gian → top 5 khách giảm dần, mỗi đơn có link chi tiết, có tổng mua.

**Kỹ thuật**
- [ ] Dùng `INSTRUCTION.md` mục 9 (QA trước khi commit) — không lỗi Console, không lỗi font, responsive.

## 11. Phụ lục — tồn kho trang hiện tại

- 1 trang gốc: `index.html` · 26 trang sách · 10 trang thể loại (sinh bằng `tools/build.py`).
- Viết tay: `shop/cart.html`, `shop/checkout.html`, `shop/order-confirmation.html`,
  `search/search.html` (+ 4 trang kết quả mẫu `search-kynangsong|vanhoc|nguyennhatanh|laptrinh.html`),
  `account/login.html`, `account/register.html`, `account/orders.html`,
  `info/contact.html`, 10 file `admin/*.html` (đã gộp trùng lặp, còn 9 + `admin-login.html` + `admin-user-new.html`).
- 14 file CSS + 1 `README.md` trong `assets/css/`.
- Ảnh: 30 bìa sách, 1 hero, 3 avatar đánh giá, logo, promo.
