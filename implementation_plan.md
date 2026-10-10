> **Status: IMPLEMENTED (10/10/2026).** All steps of the Implementation Order were
> executed and passed every static check in the Testing section (broken images: 0,
> broken links: 0, duplicate ids: 0, CSS↔ID contracts: clean, script tags: 0).
> Manual browser verification of the new pages remains to be done by the reviewer.
> One deviation from the original draft is documented at the top of [Functions](#functions):
> filters use hidden radios + `:checked` instead of `:target` anchors so they can
> compose with the `:target` pagination.
>
> **Post-implementation additions (same day):** (1) admin table fixes in
> `admin-data.css` — `.admin-table th:first-child { width: 34% }`, `.cell-book`
> flex-shrink + `overflow-wrap` rules, and `overflow-wrap: break-word` on
> `.admin-table td` to stop long emails/titles overflowing into neighbouring
> columns in `#khach-hang` and the stock table. (2) A "Gửi phản hồi" feedback form
> section appended to `info/khuyen-mai.html` (reuses the `.contact-*` form kit from
> `contact.css`, `:target` success notice `#da-gui-phan-hoi`, no new CSS needed).