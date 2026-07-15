+++
title = "CLIエージェント時代のMCP設計論：Fastmailのウィジェット実装から考える「フォールバック」の重要性"
description = """
「今日の予定と未読メールをまとめて」とAIに頼むだけで、実際のメールボックスが動く時代になりました。
愛用しているFastmailでも2026年4月に公式MCPサーバーが公開され、生成AIからの利用が簡単にできるようなりました。
2ヶ月使い込んで見えてきたのは、便利さの一方MCPの挙動についてひとつの技術的な課題でした。
"""
date = 2026-07-15T14:04:12+09:00
[taxonomies]
tags =[ "Generative AI" ]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = """
- Fastmail公式MCPサーバーが4月にリリースされ、生成AIを通じて自然言語でメール・カレンダー・連絡先・ノートを操作可能となった
- 一部のツールはユーザーの確認が前提となっており、MCP Appsという仕組みに基づいて実装されているが、claude.aiのようなブラウザのレンダリングを前提とするクライアントでは機能するが、Claude Codeでは上手く機能しない
- MCPにはelicitationというテキストベースの確認機構も標準化されており、Claude Codeは対応済みだが、Fastmailがそれをフォールバックとして使っていないことが、この非対称性の直接の原因になっている
"""
+++

{{ image(src="cover.webp",alt="Cover") }}

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

<!-- more -->

2026年4月22日、National Email Dayに合わせて、私がメインの個人メールとして利用しているFastmailが公式MCP[^1]サーバーを発表しました（[An MCP server for Fastmail — National Email Day | Fastmail Blog](https://www.fastmail.com/blog/an-mcp-server-for-fastmail/)）。
エンドポイントは `https://api.fastmail.com/mcp`です。
Claude・ChatGPTなど任意のAIクライアントから、自然言語で「明日の予定は？」「Sarahへの返信を下書きして」「歯医者の住所を教えて」といった操作を、実際のメール・連絡先・カレンダーに対して実行できるようになりました。

[^1]: Model Context Protocolの略。AIモデルと外部のデータソースやツールを安全に接続するための標準的なプロトコル

この記事は2ヶ月ほど、Fastmail MCPを利用した評価をまとめたものです。

## Fastmail MCPで何ができるか？

接続はOAuthで認可し、アクセス権限は次の3段階から選択するようになっています。

- **read-only**: メール・連絡先・カレンダーの閲覧のみ
- **write**: 下書き保存、連絡先・予定の編集
- **send**: メール送信

Fastmailが強調したのは、受信箱にチャットボットを組み込んだり、メールをモデルに流してもいないことです。
生成AIへのインターフェイスとして、MCPの入り口だけ用意しユーザー自身がアクセスできるAIツールを選ぶという姿勢です。
MCPというオープン標準に乗ることで、特定ベンダーへのロックインを避けているわけです。

Fastmail MCPサーバーは、メール・カレンダー・連絡先・ノートの4領域にわたるツール群を提供しており、
アクセス権限（read-only / write / send）に応じて呼び出せる範囲が変わります。

以下が、MCPで呼び出し可能なツール一覧です。

<!-- textlint-disable -->
<details>
<summary><strong>ツール一覧（メール・カレンダー・連絡先・ノート）</strong></summary>

**メール**

- `search_email` — 条件を指定してメールを検索
- `read_email` — 個別メールの本文・ヘッダーを取得
- `read_thread` — スレッド単位でメールをまとめて取得
- `draft_email` — 送信せず下書きとして保存（新規作成・返信・転送に対応、返信は`mode: reply`＋`emailId`でスレッドヘッダーや引用を自動処理、`replyAll`で全員返信も可能。本文はMarkdown入力に対応しており、送信時にHTML＋プレーンテキストへ自動変換される）
- `send_email` — メールを即座に送信（send権限が必要）
- `update_email` — 既読/未読・フラグなどメールの状態を更新
- `archive_email` — メールをアーカイブ
- `delete_email` — メールを削除
- `upload_attachment` — 添付ファイルをアップロード
- `list_folders` — フォルダ一覧を取得
- `list_identities` — 送信元として使える送信アイデンティティ（差出人アドレス）一覧を取得

**カレンダー**

- `list_calendars` — カレンダー一覧を取得
- `search_events` — 予定を検索
- `create_event` — 予定を直接作成（確認なしでコミット）
- `compose_event` — 予定の作成・編集をウィジェットとしてステージングし、ユーザーの確認後にコミット（`id`を渡せば既存イベントの編集、省略すれば新規作成）
- `update_event` — 既存の予定を直接更新（確認を挟まない）
- `delete_event` — 予定を削除
- `rsvp_event` — 招待された予定に出欠回答

**連絡先**

- `search_contacts` — 連絡先を検索（メール作成前のアドレス特定などに利用）
- `create_contact` — 連絡先を新規作成
- `update_contact` — 連絡先を更新
- `delete_contact` — 連絡先を削除

**ノート**

- `search_notes` — ノートを検索
- `read_note` — ノートを取得
- `create_note` — ノートを新規作成
- `update_note` — ノートを更新
- `delete_note` — ノートを削除
- `add_to_note` — 既存ノートに追記
- `set_memo` — メモ欄の内容を設定

</details>
<!-- textlint-enable -->

こうしたツールを組み合わせると、たとえば次のような使い方ができます。

- 朝、Claudeに「今日の予定と未読メールをまとめて」と頼むと、fastmailからカレンダーと直近の未読メールを読んで、1日の見通しをサマリーしてくれる
- ChatGPTに「山田さんからの問い合わせに返信案を作って」と頼むと、連絡先からアドレスを確認したうえで返信の下書きを作成し、送信前に内容を確認できる
- Claudeに「来週火曜の14時に田中さんとのミーティングを入れて」と頼むと、田中さんを出席者とした予定を登録できる
- Claudeに「鈴木さんとの一連のメールのやりとりを確認して、鈴木さんの質問とその回答を1つのノートにまとめて」と頼むと、メールのやりとりを読み込んだうえで、要点を新しいノートとして作成する

ここまでがFastmail MCPで実現できることの紹介です。ここから先は、この2ヶ月の運用で見えてきた設計上の課題を掘り下げます。

## Fastmail MCPのConfirmationの仕組み

Fastmail MCPには、AIエージェントが提案した操作をそのまま確定させず、いったんユーザーの確認を挟んでから反映する仕組みが用意されています。エージェントが意図と異なる内容で操作したり、そのまま実行してしまったりするリスクを抑えるためです。対象となる操作の内容を「ウィジェット」としてチャットUI上にステージングし、ユーザーがボタン操作で確認・修正してから初めて確定します。

たとえばカレンダーの予定作成・編集には、2つの経路が用意されています。`create_event`と`update_event`は呼び出すと即座に予定表へ反映され、参加者を招待する場合はその場で招待メールが送信されます。一方`compose_event`は、予定の内容をいったんこのウィジェットにステージングし、ユーザーが確認・修正してから初めてカレンダーに反映されます。

Fastmail MCPのツール群の中で、実際にこの確認の仕組みを使うのは次の4つです。

- `compose_event` — 予定の作成・編集
- `delete_event` — 予定の削除
- `delete_contact` — 連絡先の削除
- `delete_note` — ノートの削除

これらのツールは、呼び出した時点では何もコミットされません。ステージングされた内容がウィジェットとして表示され、ユーザーがボタン操作で確認・修正してから初めて確定します。ツール自身の説明にも「成功はウィジェットが表示されたことを意味するのであって、削除が確定したことを意味しない」という趣旨の注記があり、実行結果を判定するにはウィジェットの応答を読み取るか、削除後に検索し直して存在を確認する必要があります。

一方、次のツールは確認を挟まず直接コミットします。

- `create_event` / `update_event` — 予定の直接作成・更新（参加者への招待・変更通知メールもその場で送信される）
- `rsvp_event` — 招待への出欠回答
- `create_contact` / `update_contact` — 連絡先の直接作成・更新
- `update_note` / `add_to_note` / `set_memo` — ノート・メモの内容変更

Fastmail MCPサーバー自身のツール説明にも「対話的なカレンダー操作では`compose_event`を優先し、ユーザーが確認できない場合にのみ`update_event`のような直接コミット系を使うべき」という指示が書かれています。つまりFastmail自身が、確認フローの有無をクライアント側の対話能力に委ねていることを認識しているわけです。

なお、メールに関するツールにはウィジェットによる確認が1つも用意されていません。メール送信（`send_email`）は`send`権限自体が`read-only`／`write`とは別に明示的な許可を必要とする仕組みになっているため、confirmation UIは用意されていないのでしょう。

<!-- textlint-disable -->

{% aside(position="right") %}
claude.aiはWeb版のClaudeを指します。
{% end %}

<!-- textlint-enable -->

この仕組みには、見過ごせない課題があります。
このウィジェットによる確認は、claude.aiでは上手く動作しますが、Claude Codeでは機能しません。
同じFastmail MCPサーバー、同じツール定義に接続していても、
確認フローが機能するかどうかがクライアント次第で変わってしまう、という非対称性が発生してしまっています。

なぜこのような差が生まれるのか、標準化の状況を整理します。

## 確認メカニズムの標準化とCLIの対応状況

AIエージェントは、メール・カレンダー・連絡先といった、取り消しにくい実世界のデータを操作します。そのため、操作を確定する前にユーザーへ確認や追加入力を求める手段を、プロトコルレベルでどう用意するかは、MCP自体にとっても大きな課題でした。この課題に対して、MCPには現在2つの標準機構が用意されています。大まかに言うと、elicitationは会話の中でフォームに答えてもらう方式、MCP Appsは画面上にアプリの小さな操作画面を表示する方式です。

- 2025年6月にMCP仕様へ追加され、同年11月にURLモードが拡張された「[elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation)（誘発）」。
  サーバーがユーザーに入力や確認を求める際、JSON Schemaで定義したフォーム（文字列・数値・真偽値・選択肢など）を送り、
  クライアントが対話ダイアログを表示してユーザーの回答を返す、という仕組みが定義された。
  iframeやHTMLレンダリングを必要とせず、accept（承認）・decline（拒否）・cancel（取り消し）の3種類の応答が標準化されている。
- 2025年11月にAnthropicとOpenAIが共同で提案した「[MCP Apps](https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/)」という拡張仕様（SEP-1865）。サンドボックス化されたiframe内でHTMLを描画し、複雑なユーザー入力や確認操作をチャットUI上で完結させるための仕組みで、Fastmailの`compose_event`が使っているウィジェットもこれに基づいている。

この2つの標準は、CLI環境への対応状況が対照的です。Claude Code CLIはelicitationに対応しており、フォームモードのダイアログはターミナル上に自動的に表示され、設定なしにユーザーの回答をサーバーへ返せます。一方MCP Appsは、サンドボックス化されたiframeでHTMLを描画する設計が前提になっており、そもそもブラウザのようなレンダリング環境を必要とします。ターミナル上で動くClaude Codeには、この種のレンダリング面が存在しません。これはAnthropicがClaude Codeへの対応を怠っているのではなく、CLI/エージェント実行環境全般が構造的に抱える制約です。

## 非対称性の正体：Fastmailの実装選択

MCP Appsは任意拡張であり、公式ブログは義務ではなく推奨として次のような指針を明記しています。

> Servers should provide text-only fallback for all UI-enabled tools and return meaningful content even when UI is unavailable, so they can serve both UI-capable and text-only hosts.

UIに対応していないクライアントのためにも、意味のあるテキストベースのフォールバックを用意すべきだ、という趣旨です。

つまり、Fastmailの場合、`compose_event`のような確認操作を、
MCP Appsのウィジェットではなくelicitationの仕組みにfallbackするように実装していれば、
claude.aiとClaude Codeのどちらでも確認自体は機能したはずです[^2]。前節で見た非対称性の実体は、MCPやClaude Codeの限界ではなく、Fastmailがどちらの確認機構を選んだかという実装判断にあります。

[^2]: ただしelicitationのform modeは仕様上オブジェクト配列の編集を想定しておらず、`compose_event`ウィジェットと全く同じ編集体験になるとは限らない。

ところがFastmail MCPが実際に提供しているフォールバックは、「ホストの`read-widget-context`ツールで結果を読み取るか、`search_events`で存在を確認する」という、確認手段の代替にとどまります。
ユーザーの確認そのものを完了させる、elicitationのようなテキストベースの経路は用意されていません。結果としてMCP Appsに対応していないクライアントでは、ステージングされた操作が確定されないまま残るか、エージェントが`update_event`のような直接コミット系ツールに頼らざるを得なくなります。

この記事で見てきた非対称性は、MCPというプロトコルが未成熟だから起きているのでも、Claude Codeが対話UIに対応していないから起きているのでもありません。MCPにはすでにelicitationとMCP Appsという2つの標準機構があり、Claude Codeはelicitationに正しく対応しています。Fastmailが、両方のクライアントで機能するelicitationをフォールバックとして使わず、片方のクライアントにしか効かないMCP Appsのウィジェットだけに頼ったことが、非対称性の直接の原因です。

Fastmail、および同様の設計を選ぶ他のMCPサーバーに対して考えられる改善の方向性は、次の通りです。

- `compose_event`や`delete_event`のような操作に、MCP Appsのウィジェットに加えてelicitationベースのテキスト確認フローをフォールバックとして実装する
- クライアントがMCP Apps・elicitationのどちらに対応しているかを見て、対応する機構へ自動的に切り替える
- ツール説明文で「確認できない場合は直接コミット系を使え」とエージェントに指示するのではなく、プロトコルが提供する確認機構を正しく使い分けることで、直接コミットへのフォールバック自体を避ける

Fastmail MCPはリリースされたばかりの機能であり、こうした設計上の判断の是非が表面化するのはむしろ健全なことです。MCPエコシステムには必要な標準がすでに揃っており、あとはツール提供側がそれを正しく使い分けるかどうかにかかっています。

## まとめ

ここまで見てきた非対称性は、誰にとっても等しく問題になるわけではありません。claude.aiやChatGPTのようなMCP Apps対応クライアントから使う分には、ウィジェットが正しくレンダリングされ、確認・修正・確定が意図通りに機能するため、実用上の支障はないはずです。

<!-- textlint-disable -->

{% aside(position="right") %}
MulmoClaudeは中島聡氏が開発するClaude Codeを利用したローカルAIアシスタント育成プラットフォーム
{% end %}

<!-- textlint-enable -->

私自身の利用実態で言えば、日常的なやりとりのほとんどをClaude Codeで行っています。特に[MulmoClaude](https://github.com/receptron/mulmoclaude)をClaude Code CLIをバックエンドにしたアシスタントとして使う場面が多く、これもMCP Appsが前提とするブラウザ内蔵のレンダリング環境を持たない実行環境です。Claude Code自体はelicitationに対応していますが、MulmoClaudeがそれを自分のWeb UIへどこまで橋渡ししているかは未確認で、同じ制約を抱えている可能性があります。

実際、Claude Codeで`compose_event`を使って予定を追加したつもりが、ステージングされたウィジェットの確認が反映されないまま止まっており、予定自体が入っていなかったために予定を丸ごと飛ばしてしまったことがあります。

そのため、この記事で取り上げた非対称性は、私にとっては理論上の課題ではなく、日常的にツールの使い勝手を制限している具体的な制約です。ただしその原因は、MCPというプロトコルの限界ではなく、Fastmailが既存の解決策であるelicitationを今のところ使っていないという、一企業の実装判断にあります。
