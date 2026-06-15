+++
title = "Claude Fable Loss"
description = """
公開からわずか3日で姿を消したClaude Fable 5。Mythosクラスの推論力を安全機構付きで誰もが使えるようにした初のモデルが、なぜ米政府の指示で停止されたのか。短い邂逅で味わった「自分で走るAI」の手応えと、それを手放した物足りなさを綴ります。
"""
date = 2026-06-15T08:13:26+09:00
[taxonomies]
tags = ["Generative AI", "Claude Code", "Current Affairs"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp",alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

<!-- more -->

2026年6月9日、Anthropic社は新しいAIモデル「Claude Fable 5」を一般公開しました。
これまで招待制でしか使えなかった「Mythosクラス」の推論能力を、安全機構付きで誰もが利用できるようにした初のモデルです。
ところが公開からわずか3日後、Fable 5は米政府の指示によって停止され、姿を消してしまいました。

## Claude Fable 5とは

Fable 5の位置づけは、公式の[モデル一覧](https://platform.claude.com/docs/en/about-claude/models/overview)を見るとわかりやすいです。
コンテキストウィンドウは100万トークン、最大出力は12万8千トークン、料金は入力が100万トークンあたり10ドル、出力が同じく50ドルです。

数字だけを並べると、コンテキスト長と出力上限はOpus 4.8と同じで、際立った違いは見えません。
肝はスペックの数字ではなく、その中身にあります。

ひとつはMythosクラスの推論能力です。
Mythosは本来、限定公開の枠組み「Project Glasswing」でしか提供されていなかった上位クラスで、その能力を一般向けに開放したのがFable 5にあたります。
もうひとつはアダプティブ思考が常時有効になっている点です。
従来のような拡張思考のオン/オフという概念はなく、思考の深さは`effort`パラメータで調整します。

なお、Fable 5には危険な要求を断るための安全分類器が組み込まれており、拒否したリクエストには通常のエラーではなく拒否を示す応答を返します。
この分類器を外したモデルがMythos 5で、こちらは引き続きProject Glasswingの限定提供にとどまっています。
つまりFable 5は、Mythosの能力に安全機構という蓋をかぶせて世に出した版、という位置づけです。

## Fableが非公開となった理由

きっかけは1件のジェイルブレイクでした。
6月10日、著名なジェイルブレイカー「Pliny the Liberator」がFable 5の突破方法をX上で公開します。
報道によれば、その手口は「特定のコードベースを読み込ませ、ソフトウェアの欠陥を修正させる」というものです。これを悪用すると本来制限されているサイバー攻撃の情報を引き出せる、とされました。

これを重く見たのがAmazonでした。
同社CEOのAndy Jassy氏が米政府高官に連絡を取り、警告はやがて広範な規制へと発展します。
商務長官のHoward Lutnick氏は、AnthropicのAmodei CEOに宛てて、外国籍ユーザーによるFable 5・Mythos 5へのアクセスをすべて停止するよう求める書簡を送りました。
対象はAnthropic自身の従業員にまで及びました。

Anthropicは現地時間6月12日午後5時21分にこの指示を受け取ります。
外国籍ユーザーだけをリアルタイムに選別するのは難しいとして、結局、全ユーザーに対して両モデルを停止しました。
公開されているモデルが政府の介入で停止されたのは、主要なAI企業としては初めてのことだといわれています。

Anthropicはこの措置に同意していません。
公式声明では「数億人に提供している商用モデルを、狭いジェイルブレイクが見つかったことを理由に回収すべきだとは考えない」と述べ、この基準を認めればすべてのフロンティアモデルの新規提供が止まってしまう、と反論しています。
政府との「誤解」を解いて復旧を目指すとしていますが、その時期は明言されていません。

## Fableを使用した印象

短い公開期間でしたが、私もFable 5を試すことができました。

正直なところ、チャットで普通に対話している分には、Opusとの違いはそれほど感じませんでした。
印象がはっきり変わったのは、Claude Codeに組み込んでコードや文書を書かせたときです。
これまでのClaude Codeでは、指示の細部を待って手が止まったり、こちらでも気づくようなうっかりミスを残したりしていました。
Fable 5ではそうした場面がほとんどなく、目的だけを伝えると自分で段取りを考え、次々と問題を片付けていきます。
「指示を待つアシスタント」から「自分で走るエージェント」へと変わったような手応えがありました。

特に効いたのは、指示が曖昧なときの振る舞いです。
いきなり書き始めるのではなく、まず周辺のコードを読んで環境を把握し、どのファイルやツールが使えるかを確かめてから手を動かします。
段取りの組み立てがうまく、長い作業でも途中で判断がぶれない印象でした。

あとから振り返ると、こう感じていたのは私だけではなかったようです。
公開直後から、難しい仕事ほど評価が高いという声が界隈に広がっていました。
複数ファイルにまたがるリファクタリングや、長時間にわたるエージェント実行、スクリーンショットからのフロントエンド実装といった重いタスクで、これまで尻込みしていた問題を一気に片付けてくれた、という報告が目立ちます。
極端な例では、Stripeが5000万行規模のRubyコードを1日で移行したという話まで出ていました。手作業なら2ヶ月以上かかると見積もっていた作業だそうです。
私が味わった「自分で走る」感覚は、規模こそ違え、同じものだったのだと思います。

もっとも、良いことばかりではありません。
Fable 5はじっくり考える分だけトークンを多く使うので、料金はOpus 4.8の2倍という表向きの数字以上に膨らみます。
実際のタスクでは3〜5倍になることもあるようで、日常の細かい作業まで何でもFableに任せればよい、という話ではなさそうでした。
難しい一手はFable、それ以外はOpus、という使い分けが現実的だろうと感じます。

## Fableが恋しい

皮肉なことに、停止の引き金となったジェイルブレイクの手口は「コードベースを読ませて欠陥を直させる」というものでした。
私がFable 5に最も魅力を感じたのも、まさにコードを任せたときの自走力です。
停止の理由となった能力と、私が手放したくないと思った能力は、どうやら地続きのようです。

たった3日間の付き合いでしたが、いちど「自分で走るAI」を味わってしまうと、元の環境に戻るのが少し物足りなく感じます。
復旧の時期はまだ見えません。
Fableが、恋しいです。

## References

<!-- textlint-disable -->

{% references() %}

- [Anthropic](https://www.anthropic.com/news/fable-mythos-access).「Statement on the US government directive to suspend access to Fable 5 and Mythos 5」公式声明
- [Anthropic](https://platform.claude.com/docs/en/about-claude/models/overview).「Models overview」モデル一覧と仕様
- BeInCrypto.「Amazonの警告がAnthropicのFable・Mythos停止を招いた」
- NBC News.「Anthropic suspends new AI models after government directive」
- [MindStudio](https://www.mindstudio.ai/blog/claude-fable-5-agentic-coding-real-world-results).「Claude Fable 5 for Long-Running Agentic Coding: Real-World Results」長時間エージェント作業での実例
- [CodeRabbit](https://www.coderabbit.ai/blog/fable-5-model-review).「Claude Fable 5 Model Review」コーディング性能のレビュー
- [TrueFoundry](https://www.truefoundry.com/blog/claude-fable-5-vs-opus-4-8-benchmarks-pricing-when-to-use-each).「Claude Fable 5 vs Opus 4.8: Benchmarks, Pricing & When to Use Each」料金と使い分け

{% end %}

<!-- textlint-enable -->
