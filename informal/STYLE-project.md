# Rules for this text

The rules `STYLE.md` does not fix, for The Seifert--van Kampen theorem, after TauCeti: the library
TauCeti at commit `37f5e9dce5ac83d2825198ac72d7f5d64eb26c85`, and the theorem
`TauCeti.isPushout_fundamentalGroup`. `cf informalize init` wrote this file from formal-companion's template;
the conventions task fills it in, and the editor keeps it. Every drafter, attacker, judge
and editor reads it beside `STYLE.md`.

## Notation

The macros of `notation.sty`, one row each.

| write | for |
|---|---|

## Letters

Each letter keeps one meaning in the whole text.

| letter | meaning |
|---|---|

## Standing hypotheses

One row per key of `hypotheses.json`: the macro, the words it prints, and the Lean binder
it stands for.

| macro | prints | stands for |
|---|---|---|

## Numbers, coercions and junk values

How the text reads natural numbers against integers, the coercions it leaves silent, and
the junk values its statements rely on, each as `sections/00-conventions.tex` states it.

## The reference work

The text cites A. Hatcher, Algebraic Topology, Cambridge University Press, 2002 by number only, through `\fcref`: never a sentence of the work, and never a close paraphrase. `\fcref{<number>}` is for a number the library's docstrings give, `\fcref*{<number>}`, with a dagger, for one inferred from the work's order (`items.json`, each `reference.source`).
