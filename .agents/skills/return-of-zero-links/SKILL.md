---
name: return-of-zero-links
description: Use when adding or auditing links between field pages, rooms, arguments, and the essay for The Return of Zero.
---

# Link Return of Zero Field Pages

The local graph is a reading surface, not a generated index. The craft lives in how links are written into pages; the graph follows.

## When to use

- Adding relations to a new field page, room movement, or argument node.
- Auditing whether a page's neighborhood matches its declared relations.
- Generating the post-hoc MOC/intents layer after written links exist.

Do not use to infer links from vocabulary or shared keywords; inferred links are not declared relations.

## Steps

1. **Name the relation from the vocabulary.** Pick one of the 13 declared relations:

   `derives`, `grounds`, `defines`, `historicises`, `sources`, `qualifies`, `tests`, `figures`, `embodies`, `extends`, `compares`, `presages`, `returns-to`.

   The prose around the link must let a reader recover which relation is being used. *Done when every link is tagged by one relation word in the surrounding sentence.*

2. **Choose the right grain.** Use page-level links for general relations. Use block anchors (`^roz-s03-m27-claim04`) when the argument demands entry at claim level. *Done when the link lands at the smallest unit the relation needs.*

3. **Write the inverse route.** The essay's §5 and each room's movements carry prose-framed return links to their field records. The backlinks pane completes the loop only when the forward link is written first. *Done when the target can be reached from its consumer and back.*

4. **Preserve naming discipline.** Filename is identity. A new live node that replaces a legacy stub must declare its own title as an alias, or the frozen stub keeps capturing the link. *Done when every link resolves to a real home, not a hub or alias without content.*

5. **Run link hygiene.** Validate with:
   ```bash
   python3 tools/okf-workspace.py --project-root . doctor --json
   python3 tools/okf-workspace.py --project-root . dangling
   ```
   *Done when no dangling targets or invalid exact heading anchors remain.*

6. **Aggregate MOC/intents only after links exist.** Once the written map is stable, generate contents lists extended to intents — what a file implicates, not what it mentions. This layer is navigation-only; it never precedes authorship. *Done when the MOC is a mirror of the written graph, not its substitute.*

## Minigraph target

A well-written page has exactly the neighborhood its actual operation requires. There is **no numerical target** for link degree. Count is evidence for audit, never a quota: three necessary declared relations are better than seven padded ones, while a genuinely transverse page may require more relations than a narrow leaf. If the local graph is unreadable, inspect whether the prose has named real relations at the right grain rather than deleting or adding links merely to hit a number.

## Common mistakes

- Adding a link without naming its relation in the prose.
- Linking to a hub page that does not itself resolve to a real home.
- Generating an index or MOC before the written links exist.
- Treating every mention as a link; only implicating relations earn a link.
- Adding or deleting relations to satisfy an arbitrary numerical quota.
