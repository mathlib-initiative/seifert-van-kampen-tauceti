# Mathematical scope and review notes

The current item numbers, titles, declarations, and specializations live in
[items.json](items.json). The source inventory in
[declarations.json](declarations.json) is pinned to the dependency closure of
`TauCeti.isPushout_fundamentalGroup`. This note explains the editorial choices
rather than maintaining a second copy of the item table.

## Structure

| Section | Role in the proof |
| --- | --- |
| 1. Paths and subdivisions | A Lebesgue number, path subdivision, and reassembly of subpath classes |
| 2. Gluing fundamental groupoids | Generation by a cover and the unique extension of compatible local functors |
| 3. Fundamental groups of a cover | Generation by subspace groups, using connecting paths and basepoint transport |
| 4. Seifert–van Kampen | Vertex-group functors, descent, restriction and uniqueness, and the pushout |

## Specializations and combined statements

- Lemma 1.1 uses an open cover of a compact Euclidean subspace `K`, with
  balls taken in `K`. The linked TauCeti result allows general pseudometric
  spaces and neighborhood covers. The applications use the interval and the
  parameter square.
- Proposition 1.2 assumes an open cover of `X`. Its linked Lean theorem permits
  the more general neighborhood condition along the path. The proof uses the
  preimages of the open cover; the generation and gluing arguments apply it
  to the interiors of their cover members.
- Definition 2.2 combines the gluing construction with its restriction and
  uniqueness theorems. The two-set construction and its restriction theorems
  remain source helpers rather than separate numbered statements.
- Theorem 4.3 combines the descent construction, both restriction equations,
  and uniqueness into one unique-extension statement with a monoid target.
  Its four key Lean declarations jointly establish the statement; the two
  pointwise restriction lemmas remain helpers. The final pushout in Theorem 4.4
  is in the category of groups and follows by taking the target to be a group.

The broader cover hypothesis in Sections 2 and 3 says that the interiors of
the cover members cover `X`; it does not require the members themselves to
be open. In generation arguments, the notation for a subspace groupoid can
denote its image. This is not a global identification: inclusion can identify
distinct path classes, and gluing uses the actual subspace groupoids.

## Helpers and review status

Routine path restriction, endpoint transport, concatenation formulas, and
clipped subdivision machinery remain in the source inventory without separate
numbered statements. Their roles are recorded in `items.json`. In particular,
the removed path-restriction notation is not a notion link.

The references to Hatcher's Theorem 1.20 are grounded in the Lean module
docstrings and attached to the relevant strands of the argument.
`items.json` records each reference's provenance; no reference number is
inferred from an unverified source.

The proof excerpts and their context are checked against pinned Lean bytes.
That check does not establish the mathematical correspondence. The exported
proof links retain their agent-authored provenance and require human review.
