#import "theme.typ": *
#show: theme

// This is an instructional starter, not an empirical presentation.
#title-slide(config: config-page(footer: source-footer), extra: [
  *A source-grounded research question*

  Replace this text with exact paper titles, authors, versions, and publication status.
  #cite[Replace with verified source references.]
])
#speaker-note[
  第 1 页｜开场

  介绍研究问题及选文理由。这里是模板说明，不是论文结论。
]

== Research questions

#table(
  columns: (1fr, 1.5fr, 1.5fr),
  [*Study*], [*Question*], [*Evidence*],
  [Short paper title], [Authors' actual research question], [Task, manipulation, and outcome],
)
#cite[Replace with source sections and pages.]
#speaker-note[
  第 2 页｜选文与问题

  说明每篇论文提供什么证据。不要为了叙事流畅而创造共同机制。
]

== Study / Problem and approach

#twocol[
  *Problem*
  - State the authors' question.
  - Define the measured phenomenon.
][
  *Approach*
  - Explain the task and comparison.
  - Identify controls and outcome units.
]
#cite[Replace with Methods section and page.]
#speaker-note[
  第 3 页｜问题与方案

  先解释 task、实验条件和 metric，再进入结果。复杂设计应拆成更多页面。
]

== Study / Results

*Insert an original, provenance-tracked figure here.*

- State only the result supported by that figure.
- Preserve the task, model, units, and relevant uncertainty.
- Separate the authors' interpretation from the observation.

#cite[Replace with original figure number, panel, and page.]
#speaker-note[
  第 4 页｜读图

  按顺序解释坐标轴、单位、颜色、分母与实验条件，再说明结果支持什么，以及不能推出什么。
]

== Authors' conclusions and scope

- Attribute each conclusion to its authors.
- State the tested scope and authors' limitations.
- Do not invent a unified causal mechanism.

#cite[Replace with Discussion and Conclusion locations.]
#speaker-note[
  第 5 页｜结论与范围

  分别总结作者的结论及适用范围。只有用户给出时长限制时才安排时间表。
]
