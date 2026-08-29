+++
title = "Claude が Claude を設計する時代に私たちは何を考えるべきか"
description = """
Anthropic CEOが語った「エンジニアはもうコードを書かない」という現実。Claudeが次のClaudeを設計するフィードバックループの加速と、AI Safetyの時間的猶予について考えます。
"""
date = 2026-04-09T07:23:22+09:00
[taxonomies]
tags = ["Tech", "Generative AI"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

{{ image(src="cover.webp",alt="Cover") }}

ここ数日Claudeを起動するとほぼ毎日のようにアップデートが走ってるなと思っていましたが、
Anthropic CEOの発言を聞いて納得です。

## ClaudeはClaude自身が開発している？

以下はAnthropic CEOのDario Amodeiの発言です。

<blockquote class="twitter-tweet" data-media-max-width="560"><p lang="en" dir="ltr">Anthropic CEO: <br><br>“ I have engineers within anthropic who don’t write any code, they just let Claude write the code and they edit it and look it over”<br><br>“At anthropic writing code means designing the next version of Claude it self, so we essentially have Claude designing the next… <a href="https://t.co/kK8D7JlKzB">https://t.co/kK8D7JlKzB</a> <a href="https://t.co/ygIvHkKNHf">pic.twitter.com/ygIvHkKNHf</a></p>&mdash; CG (@cgtwts) <a href="https://twitter.com/cgtwts/status/2038234212160119034?ref_src=twsrc%5Etfw">March 29, 2026</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

> I have engineers within Anthropic who say, "I don't write any code. I don't write any code anymore.
> I just let Claude write the code and I edit it or I look it over." And of course, at Anthropic,
> writing code means designing the next version of Claude itself. So we essentially have Claude
> designing the next version of Claude itself, not completely, not in all ways, but in many ways.
> That loop starts to close very fast. And so I look at this and I say, "Wow, this is exciting.
> It's incredible what we can do with the world. But also, it's really speeding up a lot. And I'm just
> not sure we have that much time."

Anthropicのエンジニアはすでにコードを書くことをせず編集や確認のみで、Claude自身が次のClaudeを設計し開発しているという発言です。
しかも、<q>That loop starts to close very fast</q>（このループは非常に速く閉じつつある）ということです。
事実、52日間で50以上の新機能が追加されたと報じられています。

## AI Safetyへの懸念

Darioの発言は「私たちに残された時間がそれほど多くないのではないか」で終わっています。

これは、AIが人類の存在を脅かすというような極端な話ではなく、安全な形でAIを社会に統合するための制度設計・技術的安全策・国際的な合意形成などに使える時間のことを指していると思います。

ClaudeがClaude自身を設計するというフィードバックループが閉じると、AIの能力向上が自己加速的になります。
これまでは人間がAIの安全性やガバナンスの枠組みを整えていましたが、このフィードバックループでAIの開発がどんどん加速していった場合にAIの能力が想定されているガードレールの先に行ってしまうかもしれないということでしょう。

Anthropicが「Responsible Scaling Policy」を掲げ安全性研究へ力を入れているのも、AIが十分に高度になったとき悪用されたり意図しない動作をしたりするリスクに対して社会やルールがまだ追いついていないという問題意識からでしょう。そして、フィードバックループによりその危機感は高まっているということです。

## まとめ

Darioの発言で印象的なのは、AIがAI自身を設計するというループがすでに回り始めているという点です。これは未来の話ではなく、今Anthropicの中で起きていることです。自分自身を振り返っても、昨年Claude Codeを本格的に使い出してからは構想・仕様・アーキテクチャまでが自分の仕事で、設計以降はClaude Codeへ任せるようになりました。開発の現場はすでに変わっています。

問題は、このフィードバックループが閉じるほどAIの進化が加速し、安全策や社会制度を整える時間が縮んでいくことです。技術の恩恵を享受しながらも、そのスピードに見合ったガードレールをどう引くのか。AIを使う側の一人として、この問いを意識し続けることが大事だと感じています。
