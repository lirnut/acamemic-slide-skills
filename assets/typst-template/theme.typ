#import "@preview/sci-brain-slides:0.1.0": *

#let deck = setup(
  theme: "academic",
  text-size: 22pt,
  sizes: (large: 30pt, caption: 13pt, chrome: 11pt),
)
#let (twocol, spread) = deck.layouts
#let cite(body) = [#metadata(body)<slide-source>]
#let source-footer = context {
  let current-page = here().page()
  let sources = query(<slide-source>).filter(it =>
    it.location().page() == current-page
  )
  if sources.len() > 0 {
    set align(left)
    text(size: 13pt, fill: rgb("555555"), sources.last().value)
  }
}

#let theme(body) = {
  show: deck.theme.with(
    font: "Noto Sans",
    lang: "en",
    footer: source-footer,
    config-page(
      width: 960pt, height: 540pt,
      margin: (top: 91pt, bottom: 54pt, x: 44pt),
      footer-descent: 10pt,
    ),
    config-info(title: [Research presentation], author: none),
  )
  set par(leading: .45em, spacing: 12pt)
  set block(above: 12pt, below: 12pt)
  set align(horizon)
  set list(indent: 0pt, body-indent: .8em, spacing: .55em)
  set figure(numbering: none, gap: 8pt)
  show figure.caption: set text(size: 13pt, fill: rgb("555555"))
  set table(inset: 10pt, stroke: .5pt + rgb("BBBBBB"))
  show table: set text(size: 18pt)
  body
}
