# Earlier site work recovered — 4 October 2026

Two earlier states matter. The published readability pass `4ce422f7` (25 September, 23:14 BST) remains an ancestor of current main and the publication branch. A **later saved follow-on state**, `07f02292` / index `5cbd50ed` (26 September, 19:13 BST), contains further real reader changes that were missing from the current publication. Its saved working and index trees are identical.

The exact saved state is now anchored by `refs/preserved/essay-reader-follow-on-20260926`. Seven relevant source files are retained under `.legacy-earlier-site-work/`; [the exact reader follow-on patch](RECOVERED-QUARTZ-FOLLOW-ON.patch) and [the earlier implementation plan](RECOVERED-ESSAY-READABILITY-PLAN-2026-09-25.md) are retained beside this return. No full-tree restore is appropriate: current hero, source recovery, publisher, routes and foundation anchor must remain.

| Earlier concern | Published pass/current baseline | Saved follow-on recovered | Current work |
| --- | --- | --- | --- |
| Native graph, tree, search and backlinks | Retained native Quartz from `ffd06eaa` | Same native basis | Preserve and make accessible at reader widths |
| Metadata removal | Applied to reading layouts and folder lists | Preserved | Preserve |
| Night skin and reading spacing | Earlier CSS still present | Same CSS | Repair density, doubled padding and actual grid |
| Sidebar controls | Component existed but was not exported or mounted | Exported and mounted in both layouts | Recover wiring; fix wrong grid selector and implement usable mobile drawers |
| Shorter explorer labels | Plan only; native no-op mapFn | Actual display-name mapFn in both layouts | Recover without changing addresses |
| Graph tags and filtering | Plan plus inert CSS | Local tags default-off; global namespace filter, persistence and actual data filtering | Recover and verify actual graph behaviour |
| Tablet graph placement | Native layout puts tools below long body | Not fixed | Provide visible right tools or an accessible drawer |

The published pass's tests exercised metadata and spacing. The saved follow-on adds checks for visible controls, names and filter state; it still does not prove rail clicks change the grid or that mobile users can access both rails. Real production baseline captures show zero controls, graph placement thousands of pixels below the introduction at 900/1100px, and horizontal overflow at 900/1100/390px.

The earlier home replacement `d68aef80` is a separate change. It remains rejected by the current author instruction. The restored genuine hero and its developed copy stay in place, with Library and Essay in the header and established landing spaces. The superseded React essay shell remains recoverable but unbuilt; its graph was a link list, and native Quartz remains the reader basis.

The exact saved implementation has been recovered and improved in source `73a06f0e108dfb417ea42ac50130a6b681bd5e58`, now deployed to the existing O:I site. The immutable build passes all 12 real reader cases across both hosting bases, including repeated Search and preview uniqueness; the unchanged 15-case host smoke and exact-head 19-gate native landing tier also pass. `EARLIER-SITE-WORK-RECOVERY.json` binds both the first published-pass comparison and this correction from the saved follow-on source; `PUBLICATION-RETURN.md` retains the current delivery and remaining CI standing.
