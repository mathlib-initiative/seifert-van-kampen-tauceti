# Editorial guide for this text

Read this alongside [STYLE.md](STYLE.md). These choices apply to the
Seifert–van Kampen exposition and its pinned TauCeti sources. The current
numbered statements and their source relationships are recorded in
[items.json](items.json).

## Audience and structure

Assume basic point-set topology and familiarity with categories, groupoids,
paths, and monoid homomorphisms. Explain the constructions and deductions
that carry the proof. Routine endpoint transports, path restriction followed
by inclusion, and pointwise concatenation formulas need no separate lemmas.

Keep the introduction to one sentence describing the account of TauCeti's
proof. Introduce spaces, subsets, basepoints, and specialized notation where
they are needed. Combine related setup into connected prose, vary section
openings, and avoid repeating inclusion notation. Do not maintain a separate
catalogue of variables.

The sections advance the argument in this order:

1. State the Lebesgue number lemma, introduce path notation, subdivide a path,
   and motivate the subpath-class identity as reassembly of the subdivision.
2. Introduce fundamental groupoids and induced functors, then generation and
   gluing over a cover.
3. Introduce fundamental groups and prove generation by subspace groups.
4. Introduce the vertex-group functors beside their use in descent, then prove
   the restriction equations, uniqueness, and the pushout.

Give actual proofs or concise proof sketches: constructions, equations, and
the deduction of the conclusion. A description of the intended strategy is
not a proof. Use earlier numbered results explicitly, without restating their
immediate special cases as new definitions or propositions.

## Notation

Keep shared notation in [notation.sty](notation.sty).

| Macro | Meaning |
| --- | --- |
| `\N`, `\Z`, `\R` | Natural numbers, integers, real numbers |
| `\cint{a}{b}`, `\uI` | Closed interval and unit interval |
| `\intr A`, `\ball{x}{\rho}` | Interior and open ball |
| `\incl{S}`, `\inclin{S}{T}` | Inclusion into the ambient space or into `T` |
| `\ptrans` | Path concatenation and composition of homotopy classes |
| `\subpath{\gamma}{r}{s}` | Affinely parametrized subpath |
| `\pcls{\gamma}` | Homotopy class |
| `\fgpd{X}`, `\fgpd{f}` | Fundamental groupoid and induced functor |
| `\fgrp{X}{x}` | Fundamental group at a basepoint |
| `\End(w)`, `\sobj{M}` | Endomorphism monoid and one-object category |
| `\im`, `\gen{\dots}` | Image and generated subgroup or subgroupoid |

Use $f_*$ for an induced fundamental-group homomorphism and $(\iota_S)_*$
for an inclusion-induced homomorphism. Reserve $\Pi_1(f)$ for the groupoid
functor, explaining its action on points and path classes at first use.

Introduce a path $\gamma$ before its notation. Define its subpath directly by
$\gamma_{[r,s]}(t)=\gamma((1-t)r+ts)$, from $\gamma(r)$ to $\gamma(s)$.
No separate notation is needed for regarding a path as a path in a subspace.
Leave subtype coercions and endpoint renaming implicit.

Keep a letter's meaning fixed within an argument; a later section can
reintroduce it. Prefer notation that makes the Lean correspondence recognizable
without putting Lean syntax in the text. In the group-generation proof, use
$H$ for the generated subgroup, $S$ for the subgroupoid obtained by basepoint
transport, and $i_0$ for the chosen cover index.

When discussing generation, $\Pi_1(U_i)$ may denote its image in $\Pi_1(X)$
after a short convention. Do not identify them globally: the inclusion functor
need not be faithful, and gluing needs the actual subspace groupoids.

## Hypotheses and specialization

Use the hypothesis macros from [hypotheses.json](hypotheses.json), whose
printed wording is defined in `notation.sty`:

| Macro | Printed assumption |
| --- | --- |
| `\hypCoverTwo` | The interiors of $A$ and $B$ cover $X$ |
| `\hypCoverFamily` | The interiors of the $U_i$ cover $X$ |
| `\hypPathConnected` | $A$, $B$, and $A\cap B$ are path connected |
| `\hypBasepoint` | $x$ lies in $A$ and in $B$ |

In Sections 2 and 3, place the family-cover assumption once in the opening
prose of an `fcassumptions` block. In Section 2 it follows the introduction of
the fundamental groupoid. End the block before unrelated results. The cover
condition is equivalent to Lean's assertion that each point has some cover
member as a neighborhood. State indexed basepoint and pairwise
path-connectedness assumptions separately.

Keep mathematical hypotheses faithful to the declarations, recording deliberate
specializations in `items.json`:

- Lemma 1.1 uses an open cover of a compact Euclidean subspace $K$, with balls
  $B_K(z,\rho)$ taken in $K$. Specialize TauCeti's pseudometric theorem to the
  space $K$ and its whole compact subset. Define “Lebesgue number” immediately
  after the lemma, outside its statement.
- Proposition 1.2 uses a path $\gamma:[0,1]\to X$ and an open cover $(U_i)$ of
  $X$. Its proof uses $c_i=\gamma^{-1}(U_i)$ and compactness of the interval.
  Do not introduce auxiliary neighborhoods or an interior condition in this
  statement. Lean uses interiors for its broader theorem; here they equal
  the preimages.
- Both specializations retain the `broadMatch` relation to their more general
  Lean statements. Sections 2 and 3 keep the broader cover condition and
  apply Proposition 1.2 to $(\operatorname{int} U_i)$.
- For homotopies, pull that open cover back to the parameter square. Under the
  Euclidean metric choose the grid by cell diameter; Lean uses the equivalent
  maximum metric. Do not introduce ambient open extensions.

In Proposition 1.2 choose intervals of length at most half the Lebesgue radius,
matching Mathlib's subdivision helper. Do not claim that helper chooses spacing
$1/N$. Introduce equal subdivisions $t_k=k/N$ in the gluing proof where needed.
Natural numbers start at zero, and subdivisions are nondecreasing rather than
strictly increasing. Retain conventions that affect meaning, including the
nonemptiness of path-connected subsets.

## Proof tags and reading notes

Use `\leanref` for numbered statement links. The `proofpassage` environment
formats a proof without linking its whole body. Use `\proofstep` for a selected
sentence and `\proofequation` for an individual displayed equation.

Every marked step must match its entry in `proofsteps.json`. Usually it points
to one exact Lean range; a short explicit helper chain can have several.
Separate deductions when their source locations differ. Show where an earlier
result is invoked, not only the declaration of that result.

Keep the visible excerpt note to one short mathematical sentence. Put Lean
helper names, tactic explanations, and implementation details in the existing
collapsible “Reading the Lean notation” notes. Do not duplicate the title or
the printed sentence in explanatory prose.

Mark notions only where a link helps understand the argument. Use descriptive
viewer labels such as “Inclusion map”; use LaTeX in a label when notation helps.
Do not insert prose merely to host a notion tag. Retain useful notion links
once, choosing constants from `declarations.json`.

Keep the first page free of tags for nondecreasing sequences, the unit interval,
compactness, metric balls, subgroupoids, and their images. Never link “generate”
to the generic `iSup` operator. The elementary `Path.codRestrict` construction
needs no separate notation or link. Unused declarations can stay in the inventory.

## The gluing and descent arguments

Definition 2.2 characterizes the unique gluing functor by its restriction
equations. Begin its proof with uniqueness from generation. Settle the object
assignment using compatibility, then say explicitly that it remains to define
the morphism values and verify identities and composition.

Introduce $L_N(\gamma)$ as the composite of the local path-class images before
its common value $L(\gamma)$. Say which composite is unchanged under refinement.
Compare sufficiently large $N$ and $N_0$ through the common refinement with
$NN_0$ pieces. Refer to the compatibility square by a proper star.

For homotopy invariance, write $\gamma_j(t)=H(j/N,t)$. Show the parameter grid,
its image under $H$, and a magnified cell. Make clear that
$\alpha,\mu,\beta,\lambda$ are paths in $U_i\subseteq X$, not in the parameter
square. Identify the shared-edge equality explicitly.

Illustrate passage across a row by successive routes, replacing the top and
right sides of one cell by its left and bottom sides. Each replacement
preserves the composite; the constant outer sides give identities.
Use equations to obtain $L_N(\gamma_j)=L_N(\gamma_{j+1})$ and then
$L(\gamma)=L(\delta)$. Avoid vague descriptions such as “the squares fit together”
and omit routine metric bookkeeping. Link the cell relation, row argument, and
final deductions separately.

Do not give the gluing restriction equations or two-set specialization separate
numbered statements. In Corollary 4.3, apply 4.2 and 2.2 directly. Focus its
proof on compatible connecting paths and equality of the local functors on the
intersection; do not repeat the formula from 4.2.

## References

Cite Hatcher's *Algebraic Topology* by result number through `\fcref`, without
copying or closely paraphrasing its prose. Use an unstarred reference for a
number given by a Lean docstring; `items.json` records this provenance.
The current references to Theorem 1.20 are in 2.1, 2.2, 3.1, and 4.6.
Do not infer a new reference number without checking its source.

The item table records no junk-value behavior requiring a printed caveat.
Keep universe variables, typeclass syntax, and other Lean bookkeeping out of
the mathematical text.
