+++
title = "Claude Codeのディスカウントを得る - Developer Partner Program"
description = "Claude Code APIの利用料割引が可能となるDeveloper Partner ProgrameがAnthropicより発表されました。今後のモデル改善のためのプログラムで参加するとClaude 3.5 Sonnet および Claude 3.7Sonnet モデルの Claude Code 入力トークンが30%割引になる可能性があります。"
date = 2025-05-02
aliases = ["/articles/2025/05/02/anthropics-developer-partner-program"]

[taxonomies]
tags = ["Tech", "Generative AI"]
+++

Claude Code APIの利用料割引が可能となるDeveloper Partner ProgrameがAnthropicより発表されました。今後のモデル改善のためのプログラムで参加するとClaude 3.5 Sonnet および Claude 3.7Sonnet モデルの Claude Code 入力トークンが30%割引になる可能性があります。

## Anthropic's Developer Partner Programのポイント

Anthropic の Claude は基本的にユーザーの入力をトレーニングに使用しませんが、
この [Anthropic's Developer Partner Program](https://support.anthropic.com/en/articles/11174108-about-the-development-partner-program) では、Anthropic のサービスやモデルトレーニングを改善
するために、Claude Code セッションを自主的に Anthropic と共有することになります。

その代わりに、Claude 3.5 Sonnet と Claude 3.7 Sonnet の Claude Code 入力トークンに対して、
標準 API 価格から 30%オフを受けることができます。具体的には次の通りです。

- 標準入力: 100 万トークンあたり-$0.9
- キャッシュ書き込み: 100 万トークンあたり-$1.125
- キャッシュ読み取り: 100 万トークンあたり-$0.09

利用するに当たっては、次のような注意点があります。

- Anthropic のファーストパーティ API からの Claude Code の入出力トークンのみが共
  有され、Claude アプリや Claude Code 以外の API 呼び出しには適用されない。
  つまり、Amazon Bedrock などを経由するとプログラムは適用されず割引の対象外である
- データは最大 2 年間安全に保存される。モデルトレーニングに使用されるデータは
  他の顧客情報と関連付けらない
- この設定は組織内のすべてのメンバーに適用される
- プログラムに登録した場合、組織内のすべてのメンバーに通知される
- いつでもプログラムから離脱可能だが、以前に共有されたデータは削除不可
- 割引は請求後 2025 年 7 月 31 日まで適用され、プログラムを離脱すると終了する

## プログラムへの参加方法

Anthropic の Console の設定(Claude の設定画面でないことに注意)から、
「Privacy Controls」を開いて「Join our Development Partner Program to help improve Claude」
で「Join」ボタンを押すだけです。

離脱時は、「Leave」ボタンが現れるので、押すとプログラムを離脱できます。

ただし、すべてのアカウントがこのプログラムの対象ではないようです。
アカウントが対象でない場合は、上記の参加オプションが表示されません。

## まとめ

どれくらいの人が Claude Code を使っているわかりませんが、GitHub Copilot のよう
「コード入力支援」を超え Claude Code は優れた開発者とペアプログラミングしているような
錯覚に陥るほど生産性が上がります。

このため、Claude Code の利用料が 30%の割引となるのは魅力的です。
参加をためらうとしたら、「自身のコンテンツが学習に利用される」という
プライバシーの点でしょう。業務で利用している場合は、成果物が他社に共有される
ことになるためハードルが高そうです。

私自身は個人の活動で利用なので、プライバシーの観点での懸念はありません。
自身の Claude Code セッションを共有することで Claude のコーディング能力向上に
寄与し、AI によるコーディング支援技術の発展できることはモチベーションにも繋が
ります。
更に割引まで恩恵を受けることができるならば参加しない理由はないため、即座に参加しました。
