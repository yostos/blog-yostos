+++
title = "「AIを使え」の先にある本当の問題 ── エンジニア育成のパラドックス"
description = """ジュニアポジションがAIに置き換えられる今、\
エンジニアの「判断する力」を育てる場が消えつつあるのに「判断する力」がこれまで以上に求められる。\
30年コードを書き続けてきた筆者が、この育成のパラドックスについて考察します。"""
date = 2026-03-24
[taxonomies]
tags = ["Generative AI", "Career", "Current Affairs"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = """AIを前提とした開発プロセスの設計力には、実務で培った深い判断力が前提となる。\
しかしその判断力を養うジュニアポジション自体がAIに置き換えられ、\
AI依存で既存スキルも失われる。\
組織的な解はまだないが、エンジニア個人としては\
AIを使いつつも自力で開発できる力を意図的に維持し続けることが不可欠です。"""
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<!-- more -->

## はじめに ── 「AIを使わない人は出世できない」の違和感

最近、AI時代のキャリアに関する記事を立て続けて目にしました。AccentureのCEOは「AIを使わない社員は昇進できない」と断言しており、New York Timesはプログラマーの仕事が根底から変わりつつある現場をルポルタージュしています。一方で、AIがジュニアポジションそのものを消滅させているという報道もあります。

どれも的を射ていますが、どれも問題の核心を突いていない気がしています。

ソフトウェアエンジニアとして30年以上コードを書いてきた立場から言えば、「AIを使える人」ではなく、「AIを前提とした開発プロセスを設計できる人」でなければ、もはや価値を発揮できないと考えています。そして、その人材をどう育てるかという問いに、誰もまだ答えを出せていません。

## Accenture CEOの発言 ── 正しいが、すでに一歩遅い

2025年、AccentureのCEOであるJulie Sweetは、AI活用を昇進の条件とする方針を明確に打ち出しました。

<!-- textlint-disable -->

<blockquote cite="https://finance.yahoo.com/news/want-promotion-accenture-ceo-says-063000196.html">
<p>"If you want to get promoted, you've got to do the things that we do."</p>
<footer>— Julie Sweet, CEO of Accenture（2025年、Yahoo Finance）</footer>
</blockquote>

<!-- textlint-enable -->

AIを使わない社員は昇進させない。3年かけて技術を浸透させた上での方針だといいます。Accentureは30億ドル規模のAI投資と8万人のAI人材育成を進めており、経営者としての本気度は疑いようがありません。

しかし、CEOの発言そのものは「AIを使え」という号令です。問題は、AIツールを日常的に「使う」こと自体が、もはやスキルと呼ぶには陳腐化しつつあるということです。ChatGPTにプロンプトを投げて回答を得ることは、すでにエンジニアに限らず多くの人が日常的にやっています。上手なプロンプトを書くことが評価されたのは数年前です。

**問われるべきは「AIを使えるか」ではなく、「AIを組み込んだ開発プロセスを設計できるか」です。**

プロンプトを書く能力ではありません。開発チーム全体のワークフローの中で、どこにAIを配置し、どこに人間の判断を残し、どのような検証プロセスを組むかを設計する能力。それこそが、今後のソフトウェア開発における差別化要因になります。

## New York Timesが描いた現場 ── 「判断する仕事」への転換

2026年3月、Clive ThompsonはNew York Times Magazineで、AIによってプログラマーの仕事がどう変わったかを70人以上の開発者への取材を通じて描きました。

<!-- textlint-disable -->

<blockquote cite="https://www.nytimes.com/2026/03/12/magazine/ai-coding-programming-jobs-claude-chatgpt.html">
<p>"A coder is now more like an architect than a construction worker."</p>
<footer>— Boris Cherny, Head of Claude Code, Anthropic（2026年3月12日、The New York Times Magazine）</footer>
</blockquote>

<!-- textlint-enable -->

開発者の仕事は「コードを書く」から「判断する」へと移行しています。AnthropicのClaude Code責任者であるBoris Cherny自身、コードベースへの貢献の100%をClaudeに書かせているといいます。Googleでは30人必要だったチームが3–6人で済むようになりました。Amazonでは、以前8時間かかったデバッグをAIが15分で完了させました。

ここで重要なのは、生産性が上がったのは単にAIツールを「使った」からではないということです。**AIエージェントをどう配置し、どう監督し、どう検証するかという「開発プロセスの設計」が的確だったからこそ、生産性が劇的に向上しました。**

Googleのプロダクト担当シニアディレクターであるRyan Salvaは、ソフトウェア開発におけるAI活用についてこう語っています。

<!-- textlint-disable -->

<blockquote cite="https://www.nytimes.com/2026/03/12/magazine/ai-coding-programming-jobs-claude-chatgpt.html">
<p>"As an engineer, I care less that the models are really good at producing the right result the first time. I care much more that there are validation steps in place so that it eventually gets the perfect or the right answer."</p>
<footer>— Ryan Salva, Senior Director of Product, Google（2026年3月12日、The New York Times Magazine）</footer>
</blockquote>

<!-- textlint-enable -->

AIの出力を最初から信用するのではなく、検証ステップを設計すること。これはまさに「AIを使う」ではなく「AIを前提とした開発プロセスの設計」の話です。

ただし、ここで見落としてはならない点があります。ソフトウェア開発は、検証という観点ではきわめて恵まれた分野です。ユニットテスト、インテグレーションテスト、CI/CDパイプラインといったテスティングの仕組みが充実しており、「Test First」という手法が業務として浸透して20年以上経っています。つまり、AIの出力を機械的に検証するインフラが、すでに存在しているのです。

それでも、Salvaが言うような「検証ステップを設計する」ことができるエンジニアは限られています。テストを書くことと、何をテストすべきかを設計することは、まったく別の能力です。これだけ検証の仕組みが整った分野ですら、この状況なのです。

## 消えるジュニアポジション ── 育成のパラドックス

ここまでなら「AIを前提とした開発プロセスの設計力を身につけよう」で話は終わります。しかし、CNBCの2025年11月の報道が、もっと根深い問題を突きつけています。

<!-- textlint-disable -->

<blockquote cite="https://www.cnbc.com/2025/11/20/why-ai-may-kill-career-advancement-for-many-young-workers.html">
<p>Companies are replacing entry-level jobs with artificial intelligence — and, in the process, are upending the traditional route to career advancement for many young, white-collar workers.</p>
<footer>— CNBC（2025年11月20日）</footer>
</blockquote>

<!-- textlint-enable -->

New York Timesの記事でも、Stanford Digital Economy LabのErik Brynjolfssonの研究が引用されています。AI露出度の高い職種における若手プログラマーの雇用は2022年以降16%減少した一方、ベテランプログラマーの雇用には有意な減少がありませんでした。

ここに**育成のパラドックス**があります。

「AIを前提とした開発プロセスの設計力」は、高次のスキルです。それは長年の実務経験を通じて、何が良いコードで何が悪いコードかを判断できるようになって初めて身につきます。New York Timesの記事で、Point Health A.I.のエンジニアPia Torainはこう証言しています。

<!-- textlint-disable -->

<blockquote cite="https://www.nytimes.com/2026/03/12/magazine/ai-coding-programming-jobs-claude-chatgpt.html">
<p>"I realized that it was just four months that I was prompting hundreds, 500 prompts a day, that I started to lose my ability to code."</p>
<footer>— Pia Torain, Software Engineer, Point Health A.I.（2026年3月12日、The New York Times Magazine）</footer>
</blockquote>

<!-- textlint-enable -->

わずか4ヶ月のAI依存で、コーディング能力が衰えたといいます。入社2年目の若手エンジニアの証言です。

整理するとこうなります。

1. AIを前提とした開発プロセスの設計力を持つエンジニアが求められている
2. その能力には、実務で培った深い判断力が必須である
3. しかし、判断力を養うためのジュニアポジション自体がAIに置き換えられている
4. さらに、AIに頼りすぎると既存のスキルすら失われる

つまり、**「判断する力」を育てる場が消えつつあるのに、「判断する力」がこれまで以上に求められている**。これが育成のパラドックスです。

もちろん、シミュレーション環境での訓練やAIの出力を教材として活用する新しい学習方法も模索されています。しかし、それらはまだ実証段階であり、従来の「実務を通じた学び」に代わるものとして確立されたとは言えません。

## 30年コードを書いてきた者として

私はエンジニアとして30年以上コードを書いてきました。日本のIT業界では、ある程度の経験を積むとコーディングから離れ、PMやアーキテクトを目指すのが「正しいキャリアパス」とされてきました。コードは単価の安い若手やベンダー、海外リソースが書くもの。上流工程に行くことが「上がり」だという空気です。

私はその空気に抗ってきました。コードが書けないPMやアーキテクトに、本当に正しい判断ができるのか。お客様の業務を理解するのは当然ですが、その前提としてエンジニアとしてのスキルが必要で、それはPowerPointを操る能力ではないはずです。だから意図的に、自分の手でコードを書き続ける仕事が来るように動いてきました。

振り返ると、これは育成のパラドックスに対する、個人レベルでの答えの1つだったのかもしれません。**判断力の源泉となるスキルを、意図的に手放さない。** 組織がどう評価しようと、自分の判断力を支える基盤を維持し続けるという選択です。

New York Timesの記事で、Point Healthの共同創業者Rachel Gollubはこう語っています。

<!-- textlint-disable -->

<blockquote cite="https://www.nytimes.com/2026/03/12/magazine/ai-coding-programming-jobs-claude-chatgpt.html">
<p>"People were all like, 'You're losing all your ability to code.'"</p>
<footer>— Rachel Gollub, Co-founder, Point Health（2026年3月12日、The New York Times Magazine）</footer>
</blockquote>

<!-- textlint-enable -->

新しい抽象化が登場するたびに「能力を失う」と言われてきました。しかし今回の問題は、過去の抽象化とは本質的に異なります。PythonがC言語を置き換えたとき、メモリ管理のスキルは不要になりましたが、代わりにPythonのスキルが求められました。学ぶべき対象が変わっただけです。

今回起きているのは **「スキルを学ぶプロセスそのものの消滅」** です。しかし、組織的な解がまだ見えない以上、個人としてできることは同じなのだろうと思います。AIが書いたコードを判断するために、自分自身がコードを書く力を意図的に維持し続けること。それは30年前にPMへの「上がり」を拒んだのと、構造としては同じ選択です。

だから、この時代にエンジニアを目指す若い人に伝えたいことがあります。AIを使うことは構いません。しかし、自力で開発できる力は必ず身につけてください。会社がその機会を与えてくれることを期待してはいけません。ジュニアポジションが消えているなら、自分で作ればいいのです。個人開発でもOSSへの貢献でも、コードを書く機会はいくらでもあります。会社の育成制度に自分のキャリアを委ねること自体が、もはやリスクです。

## では、どうするか

**組織としては、エンジニア育成の設計そのものを変える必要があります。** ジュニアの仕事が「コードを書く」から「AIの出力を検証する」に変わるなら、検証力を体系的に鍛える仕組みが必要です。「AIを使え」という号令だけでは、中長期的にAIの出力を正しく判断できるエンジニアが枯渇するリスクを孕んでいます。ただし、その具体的な方法論は、正直に言えばまだ誰も確立できていません。

**一方、エンジニア個人としては、答えは明快です。** 前のセクションで書いた通り、自分の手でコードを書く力を維持し続けること。AIを使うことと、AIなしでも書ける力を持つことは矛盾しません。会社の育成制度がこのパラドックスに追いつくのを待っている余裕はないのです。

New York TimesのAnil Dashの言葉が示唆的です。

<!-- textlint-disable -->

<blockquote cite="https://www.nytimes.com/2026/03/12/magazine/ai-coding-programming-jobs-claude-chatgpt.html">
<p>"In coding, L.L.M.s take away the drudgery and leave the human, soulful parts to you."</p>
<footer>— Anil Dash, Programmer and Tech Executive（2026年3月12日、The New York Times Magazine）</footer>
</blockquote>

<!-- textlint-enable -->

コーディングにおいて、LLMは退屈な作業を奪い、人間的で魂のある部分を残してくれる。美しい言葉です。しかし、その「魂のある部分」を担える人間を、どう育てるのでしょうか。退屈な作業を経験せずに、魂のある判断ができるようになるのでしょうか。

この問いに対する答えが、AI時代のソフトウェア開発における最も重要な課題だと、私は考えています。

## References

<!-- textlint-disable -->

{% references() %}

- The New York Times Magazine. "Coding After Coders: The End of Computer Programming as We Know It" `https://www.nytimes.com/2026/03/12/magazine/ai-coding-programming-jobs-claude-chatgpt.html`
- Yahoo Finance. "Accenture CEO says failure to use AI will cost workers a promotion—or their job" `https://finance.yahoo.com/news/want-promotion-accenture-ceo-says-063000196.html`
- CNBC. "Why AI may kill career advancement for many young workers" `https://www.cnbc.com/2025/11/20/why-ai-may-kill-career-advancement-for-many-young-workers.html`

{% end %}

<!-- textlint-enable -->
