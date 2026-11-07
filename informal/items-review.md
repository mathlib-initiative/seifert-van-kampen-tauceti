# The item table, for the maintainer

The source inventory records the dependency closure of `TauCeti.isPushout_fundamentalGroup` at commit
`37f5e9dce5ac83d2825198ac72d7f5d64eb26c85`: 32 scope members, 21 selected items in 6 sections, 25 of
the members as key declarations and 7 as helpers. The ids are provisional and contiguous
within each section, in reading order.

The six sections run from the interval and path lemmas, through the fundamental groupoid and
the one-object category of a vertex group, to the two halves of the theorem: gluing functors
over a cover (existence) and generation by a cover (uniqueness), and then the based theorem
itself.

## Items

| id | kind | title | key declarations | reference | source | departures |
|---|---|---|---|---|---|---|
| 1.1 | lemma | A Lebesgue number for a family of neighborhoods | `TauCeti.lebesgue_number_lemma_of_metric_of_mem_nhds` | — | — | the members of the family need not be open, only neighborhoods of the points they cover |
| 1.2 | definition | Subdivision points of an interval | `Set.Icc.coe_addNSMul` | — | — | the minimum formula is used as a definition; the related Lean lemma identifies it with Mathlib's interval-valued construction for nonnegative steps |
| 1.3 | proposition | Subdividing a path along a family of sets | `Path.exists_monotone_range_subpath_subset` | — | — | — |
| 1.4 | lemma | Cutting a path class at an intermediate parameter | `Path.Homotopic.Quotient.subpath_cast_trans` | — | — | — |
| 2.1 | lemma | The fundamental groupoid of a path-connected space | `FundamentalGroupoid.nonempty_hom` | — | — | — |
| 2.2 | lemma | An injective map is injective on objects | `ContinuousMap.fundamentalGroupoid_map_obj_injective` | — | — | — |
| 2.3 | lemma | Recasting the endpoints of a path class | `Path.Homotopic.Quotient.cast_mem_arrows_iff` | — | — | — |
| 2.4 | lemma | The image of the class of a loop | `TauCeti.FundamentalGroup.map_fromPath` | — | — | — |
| 3.1 | definition | The functor picking out a chosen object | `TauCeti.Groupoid.singleObjFunctor` | — | — | — |
| 3.2 | definition | The functor induced by a homomorphism out of a vertex group | `TauCeti.Groupoid.functorOfEndHom` | — | — | — |
| 4.1 | theorem | Covers generate the fundamental groupoid | `TauCeti.FundamentalGroupoid.iSup_im_map_subtypeVal_eq_top` | Theorem 1.20 | module docstring | the members need not be open and nothing is assumed connected |
| 4.2 | definition | Gluing functors out of fundamental groupoids | `TauCeti.FundamentalGroupoid.glue` | Theorem 1.20 | module docstring | the target is an arbitrary category; the members need not be open and nothing is assumed connected |
| 4.3 | proposition | The glued functor restricts to the given functors | `TauCeti.FundamentalGroupoid.map_subtypeVal_comp_glue` | — | — | — |
| 4.4 | definition | Gluing two functors out of fundamental groupoids | `TauCeti.FundamentalGroupoid.glueTwo` | — | — | the two subsets need not be open, only their interiors cover; nothing is assumed connected |
| 4.5 | proposition | The functor glued from two restricts to each of them | (a) `TauCeti.FundamentalGroupoid.map_subtypeVal_comp_glueTwo_left`; (b) `TauCeti.FundamentalGroupoid.map_subtypeVal_comp_glueTwo_right` | — | — | — |
| 5.1 | theorem | Covers generate the fundamental group | `TauCeti.FundamentalGroup.iSup_range_map_subtypeVal_eq_top` | Theorem 1.20 | module docstring | the members need not be open; every intersection of two members is path connected, which for a member with itself is the member |
| 5.2 | corollary | Two sets generate the fundamental group | `TauCeti.FundamentalGroup.range_map_subtypeVal_sup_eq_top` | — | — | the two subsets need not be open, only their interiors cover |
| 6.1 | definition | The homomorphism out of the fundamental group of the space | `TauCeti.vanKampenDesc` | — | — | the target is only a monoid; the two subsets need not be open |
| 6.2 | proposition | The induced homomorphism restricts to the given ones | (a) `TauCeti.vanKampenDesc_map_left`, `TauCeti.vanKampenDesc_comp_map_left`; (b) `TauCeti.vanKampenDesc_map_right`, `TauCeti.vanKampenDesc_comp_map_right` | — | — | each equality is stated both element by element and as an equality of homomorphisms |
| 6.3 | proposition | Uniqueness of the induced homomorphism | `TauCeti.vanKampen_hom_ext` | — | — | the target is only a monoid; the two subsets need not be open |
| 6.4 | theorem | The based Seifert--van Kampen theorem | `TauCeti.isPushout_fundamentalGroup` | Theorem 1.20 | module docstring | the two subsets need not be open; the basepoint of the intersection is the basepoint of the space |

Every reference number is `Theorem 1.20`, and each is grounded in the module docstring of the
file the item comes from: the references list of
`TauCeti/AlgebraicTopology/FundamentalGroupoid/CoverGeneration.lean` and of
`TauCeti/AlgebraicTopology/FundamentalGroupoid/Glue.lean` names Section 1.2 and the proof of
Theorem 1.20, that of `TauCeti/AlgebraicTopology/FundamentalGroup/CoverGeneration.lean` names
Theorem 1.20 and the surjectivity of the canonical map, and that of
`TauCeti/AlgebraicTopology/FundamentalGroup/VanKampen/Basic.lean` names Theorem 1.20 and
Example 1.21. Items 4.3, 4.4, 4.5, 5.2 and 6.1 to 6.3 are steps inside those same files; the
number is cited once per strand, on the statement the strand is named for, rather than on every
item of the strand. No number is inferred, so the text prints no dagger. Example 1.21 is the
free-product case of the theorem, which the closure of this theorem does not reach, so it is
cited nowhere.

## Scope members that are no key declaration

The six routine path constructions and lemmas below are helpers on 1.3. The
paper introduces notation and uses their elementary properties implicitly;
their presence in the source inventory does not require separate statements.

- `Path.codRestrict`: linked from the notation $\gamma^S$ in the local prose.
- `Path.codRestrict_coe`: the pointwise formula for that construction.
- `Path.map_codRestrict`: recovering the ambient path under inclusion.
- `Path.trans_apply_of_le` and `Path.trans_apply_of_ge`: the two formulas in
  the definition of concatenation.
- `Path.subpath_apply_mem`: containment of a subpath in the original segment.
- `TauCeti.Groupoid.functorOfEndHom_map` (helper on 3.2): it states the formula for the value
  of the induced functor on a morphism, which is the content of the definition in 3.2.

## Notes on the shape of the table

- Items 4.5 and 6.2 have parts because the library splits a single statement by side:
  the two subsets of the cover and the two given homomorphisms.
- Item 6.2 carries two key declarations per part: the library states each restriction both
  element by element and as an equality of homomorphisms, and the two are the same statement.
- No statement in the closure relies on a junk value, so every `junk` list is empty. The
  statements do use coercions out of subtypes and out of the unit interval, which the
  local notation leaves implicit; item 1.2 is the one place where a coercion carries the
  content of the statement.
- The target of the descent in 6.1 to 6.3 is a monoid, not a group, while the pushout in 6.4 is
  taken in the category of groups. The text should say this where it states 6.1, since a reader
  expecting the usual statement will expect a group.
- `TauCeti.FundamentalGroup.iSup_range_map_subtypeVal_eq_top` (5.1) and
  `TauCeti.FundamentalGroupoid.iSup_im_map_subtypeVal_eq_top` (4.1) state their covering
  hypothesis as "every point has some member as a neighborhood"; 4.4, 5.2 and 6.1 to 6.4 state
  it as "the interiors of the two subsets cover the space". The items follow their own
  signatures rather than converting one form into the other.
