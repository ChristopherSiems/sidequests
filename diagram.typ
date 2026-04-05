#import "@preview/fletcher:0.5.8" as fletcher: diagram, edge, node
#import fletcher.shapes: cylinder, diamond, ellipse

#set page(width: auto, height: auto, margin: 1cm)

#diagram(
  node-stroke: .048em,
  node-shape: ellipse,

  node((0, 0), [client], shape: ellipse, name: <client>),
  node((4, 0), [server], shape: ellipse, name: <server>),
  node((8, 0), [database], shape: cylinder, name: <database>),
  node((4, 2), [Clark Engage \ and other sources], shape: rect, name: <engage>),
  node((8, 2), [local LLM], shape: diamond, name: <llm>),

  edge(
    <client>,
    <server>,
    "->",
    [1. free time and location],
    label-side: right,
  ),
  edge(
    <server>,
    <database>,
    "->",
    [2. request relevant quests],
    label-side: right,
  ),
  edge(<database>, <server>, "->", [3. return relevant quests], bend: -20deg),
  edge(<server>, <client>, "->", [4. propose quest], bend: -20deg),
  edge(
    <server>,
    <engage>,
    "->",
    [a. scrape events \ (daily cron job)],
    label-side: right,
  ),
  edge(<engage>, <llm>, "->", [b. derive quest from event], label-side: right),
  edge(<llm>, <database>, "->", [c. update database], label-side: right),
)
