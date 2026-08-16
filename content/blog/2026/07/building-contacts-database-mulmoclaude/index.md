+++
title = "住所録をMulmoClaudeでさくっと作る"
description = """
20年使ってきた住所録アプリPowerAddressが、FileMakerの仕様変更とmacOSの対応終了が重なって使えなくなろうとしています。\
CSVを読み込ませて要件を伝えるだけで、スキーマ定義からカンバン表示まで住所録を作ってくれたAIアシスタントMulmoClaudeへの移行を紹介します。\
"""
date = 2026-07-28T05:10:06+09:00
[taxonomies]
tags =[ "Generative AI","Claude" ]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = """\
FileMaker製住所録アプリPowerAddressの終了アナウンスを受け、住所録をMulmoClaudeに移行しました。\
CSVを読み込ませて要件を伝えるだけで、スキーマ定義・カンバン表示・自動化までMulmoClaudeが構築してくれました。\
郵便番号データベースの月次自動更新とレコードの不整合チェックも、要件を伝えるだけでMulmoClaudeが設定しました。\
"""
+++

<!-- textlint-disable -->

{{ image(src="cover.webp",alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

## 愛用した住所録アプリ PowerAddressが動かなくなる

わが家では、20年に渡って年賀状の住所録管理をPowerAddressを使用して管理しています。

毎年のようにアップグレードが必要な一般的な宛名書きアプリと比べると、
住所録管理に特化しているため、機能的に見劣りする部分はありました。
しかし、郵便番号から住所補完や年賀状の履歴管理、宛名の印字など基本的な機能は
揃っており、私には十分でした。
何より、アップグレード料金が発生することなく長年使えている点が気に入っていました。

ところが、2026年5月に「v5.1が最後のバージョン、Macアプリ版は注意が必要」というアナウンスがPowerAdress
の公式サイトでなされています。

<!-- textlint-disable -->

{{ aside(text="FileMakerは、Apple傘下のClaris社が開発するデータベース構築ツール", position="right") }}

<!-- textlint-enable -->

PowerAddressはFileMakerで作成され、FileMakerのランタイム作成機能(アプリ版を作成する機能)を利用して、
Windows版とMac版がリリースされています。

ところが、FileMakerは2020年のFileMaker 19からランタイム作成機能を完全に削除しました。
このため、アプリ版のPowerAddressの開発が不可能となり、2020年にリリースされたPowerAddress v5.1が最後のバージョンとアナウンスされました。

さらにPowerAddress Mac 5.1のランタイムはIntelベースです。AppleはIntelアプリを動かすRosetta 2
2027年リリース予定のmacOS 28からは未サポートになるとアナウンスしており、そうなると、PowerAddress Mac版は起動すらできなくなります。

## 住所録の移行先の検討

もう来年に迫っているので、移行先を検討してみました。

PowerAddressの公式アナウンスではFileMaker版やFileMakerテンプレート版への移行も案内されていました。
いずれもFileMaker本体の購入が必要です。
現在のFileMakerはサブスクリプションモデルで月額2,000円以上かかり、年賀状シーズンくらいしか使わない住所録管理としてはコストが見合いません。
更にPowerAddressの開発自体は終了するようなので、移行したところで将来はありません。

しまうまプリントとなど他社のクラウド連絡先サービスも候補にしました。
宛名印刷サービスとして使う分には大変便利ですが、
住所録のマスター管理を移管すると、サービス停止による住所録の消失リスクがあります。
個人情報を長期にわたって安全に保管することを考えると、クラウドに預けず手元で管理できる方法が必要だと判断しました。

いろいろ検討した結果、[MulmoClaude](https://github.com/receptron/mulmoclaude)へ移行することにしました。

[MulmoClaude](https://github.com/receptron/mulmoclaude)は、マイクロソフトでWindows 95、Windows 98、
Internet Explorer 3.0/4.0のチーフアーキテクトを勤めた中島聡氏がオープンソースで開発するAIアシスタントです。
最近私もほぼ日々の生活で全面的に利用するようになりました。

このMulmoClaudeにスキーマ駆動のコレクションを管理する機能があるため、住所録程度であれば十分対応できます。
MulmoClaudeはClaude Code CLIをバックエンドに利用するため、多少の準備は必要です。
とはいえ、以前に比べれば非エンジニアでも十分に扱えるところまでハードルは下がっていると感じています。

## MulmoClaudeで住所録を作る

実施したことは、PowerAddressから出力したCSV形式の住所録を読み込ませて、
「これを取り込む為のスキーマを定義して取り込んで」と依頼しただけです。

取り込まれたデータの不要な項目を削除したり、属性をtextからenumに変更したりして調整しました。
これだけで、後述のフィルタリングやカンバン表示にも対応する、使いやすいコレクションへと仕上がりました。

<!-- textlint-disable -->

{{ image(src="table.webp",alt="住所録テーブル表示",caption="住所録テーブル表示" )}}

<!-- textlint-enable -->

MulmoClaudeでは属性がenumのフィールドがあればカンバン方式で表示可能なので、
これを利用して50音でフィルタリングするPowerAddressの機能を疑似的に再現できました。

<!-- textlint-disable -->

{{ image(src="kanban.webp",alt="住所録カンバン表示",caption="住所録カンバン表示" )}}

<!-- textlint-enable -->

各レコードは、郵便番号データベースからの住所補完や連名管理も可能です。

<!-- textlint-disable -->

{{ image(src="record.webp",alt="住所録レコード表示",caption="住所録レコード表示" )}}

<!-- textlint-enable -->

自動化についても「郵便番号データベースを月次で自動更新して、レコードの不整合があればチェックしてほしい」と要件を伝えただけで、
必要なスケジュール設定やスクリプトはMulmoClaudeが自分で作成してくれました。

## まとめ

20年使い続けたPowerAddressの終了は残念でしたが、住所録という個人情報は手元で管理し続けるという方針は変えずに済みました。
私がCSVを読み込ませて要件を伝えただけで、スキーマ定義からカンバン表示、月次の自動更新まで一通りMulmoClaudeが作ってくれたのは想像以上でした。

現在はFastmailカレンダーと連動したスケジュール管理やTODO管理、資産ダッシュボード、趣味の音楽ノウハウのWiki管理などもMulmoClaudeで行なっています。
個人レベルのちょっとしたデータ管理であれば、専用アプリを探さなくてもAIアシスタントに任せられる場面は今後も増えていきそうです。
