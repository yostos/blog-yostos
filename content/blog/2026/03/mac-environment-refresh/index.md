+++
title = "Mac環境のリフレッシュ"
description = """\
無為がループした一年で放置していたMac環境をリフレッシュしました。\
MacPawのGUIツールをCLIへ移行し、メニューバーをmacOS Tahoe標準機能で整理し、\
ArcからSafariへ乗り換えた記録です。\
"""
date = 2026-03-17T15:34:11+09:00
[taxonomies]
tags = ["Tech", "Application"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

見送っていたMac環境のリフレッシュを実施しました。

## MacPaw関連ソフトウェアの見直し

MacPaw[^1]の次の2つのソフトウェアを使用していました。

- **CleanMyMac X**: macOSのメンテナンス・ユーティリティ
- **Gemini 2**: 重複ファイル削除ツール

いずれもサブスクリプションが中心ですが、私は2022年にロシアのウクライナ侵攻が起こった際に支援のつもりでLifeTimeの買い切りで購入しています。コストも発生せず、どちらも便利なツールです。

しかし、常駐して僅かですがリソースを食っているのが気になっていました。
今回はどちらもアンインストールして、CLI代替ツールに移行しました。

[^1]: Macのユーティリティ系ソフトウェアを開発・販売しているウクライナのベンダー

## Mole — macOSクリーンアップツール

<!-- textlint-disable -->

{{ linkcard(url="https://github.com/tw93/mole") }}

<!-- textlint-enable -->

macOSのクリーンナップと最適化に特化したコマンドラインツールです。
CleanMyMac、AppCleaner、DaisyDisk、iStat Menusなどの機能を1コマンドでカバーしていると謳っています。

```bash
mo clean      # キャッシュ・ログ・ブラウザ残骸の削除
mo uninstall  # アプリの完全アンインストール
mo optimize   # キャッシュ再構築・サービスリフレッシュ
mo analyze    # ディスク使用量の可視化
mo status     # CPU/GPU/メモリ/ディスク/ネットワークのリアルタイム監視
mo purge      # 開発プロジェクトのビルド成果物削除
mo installer  # Downloads内の.dmg/.pkgの整理
```

結構危険な処理をするツールですが、いずれも`--dry-run`オプションがサポートされており、実際に削除する前に検証できます。

実際、CleanMyMac Xで使用していた機能のうちマルウェアスキャン以外はほぼカバーされています。
マルウェアスキャンについては、macOS標準のXProtectとGatekeeperがかなり優秀なので、基本的に追加のスキャナは不要と判断しました。

## Czkawka（チカフカ） — 不要ファイル検出ツール

<!-- textlint-disable -->

{{ linkcard(url="https://github.com/qarmin/czkawka") }}

<!-- textlint-enable -->

主に重複ファイルの削除に使用していたGemini 2の代替です。名前はポーランド語で「しゃっくり」を意味します。

[rmlint](https://github.com/sahib/rmlint)も検討しましたが、rmlintはバイト単位での重複判定のみで、Gemini 2のように画像の類似性による重複判定には対応していません。

その点Czkawkaは、パーセプチュアルハッシュによる類似画像検出をサポートしています。GUI版もありますが、安定のCLI版を使っています。

```bash
# 重複ファイル検出: -d 検索先 -e 除外先 -m 最小25B -s hash比較 -D aeo(最古以外を削除)
czkawka_cli dup -d ~/Documents -e ~/Documents/Archive -m 25 -x 7z rar IMAGE -s hash -f results.txt -D aeo

# 空フォルダ検出: 複数ディレクトリ指定可
czkawka_cli empty-folders -d ~/Documents ~/Downloads -f results.txt

# 巨大ファイル検出: -n 上位25件 -x VIDEO拡張子を除外
czkawka_cli big -d ~/Documents -e ~/Documents/Archive -n 25 -x VIDEO -f results.txt

# 類似画像検出: パーセプチュアルハッシュで視覚的に似た画像を検出
czkawka_cli image -d ~/Pictures -e ~/Pictures/Wallpapers -f results.txt

# 壊れたシンボリックリンク検出
czkawka_cli symlinks -d ~/Projects -e ~/Projects/.git -x jpg -f results.txt

# 破損ファイル検出: ヘッダが壊れたファイル等を検出
czkawka_cli broken -d ~/Downloads -f results.txt
```

重複ファイル、類似画像、空ファイル・フォルダ、一時ファイル、破損ファイル、拡張子不一致、不正ファイル名など、Gemini 2以上に多彩な検出機能を備えています。

なお、SenseiとCocktailは引き続き使用しています。Senseiはハードウェア情報やSSDのTrim管理に、CocktailはmacOSの定期メンテナンスタスクの自動実行に、それぞれ役割が明確なので残しました。

## メニューバーの整理

MacBookでメニューバーにたくさんアイコンが並ぶと、ノッチの裏に隠れて見えなくなる問題があります。この対策としてメニュー表示管理ツールを使用していました。

Bartenderから数年前に[Ice](https://github.com/jordanbaird/Ice)へ移行しましたが、macOS Tahoeではメニュー構造が変わった影響で動作が不安定になっていました。

代替として次のようなツールがありますが、いずれも新しいmacOSのメニュー構造の変更に対応しきれていないようでした。

- Hidden Bar
- Bartender 5（有料）
- Vanilla
- iBar

しかし、macOS Tahoeではメニューバーのカスタマイズ機能が大幅に強化されました。「システム設定 > メニューバー > メニューバーの操作」から、次の操作が可能になっています。

- アプリごとにメニューバーへの表示のオン・オフを制御
- Apple純正機能はコントロールセンターへ移動可能
- Command+ドラッグでアイコンの並び替え

サードパーティ製ツールのように表示の動的な切り替えやレイアウト変更には対応していませんが、常駐アイコンの大半を整理できました。もうサードパーティ製ツールは不要です。

## ブラウザArcの代替

数年前に彗星のごとく登場したArcを愛用していましたが、2025年5月にThe Browser Companyが開発終了を発表しました。理由は「ほとんどの人にとってArcは違いが大きすぎて学習コストに見合わなかった」という"novelty tax"問題とのことです。後継としてAIブラウザ「Dia」の開発に注力するとされていますが、Arc自体はセキュリティ修正のみのメンテナンスモードに入っています。

当初はGoogle Chrome + Side Space拡張機能でほぼArcと同等のことができるかと試していました。しかし、Arcの全機能を再現しようとすると拡張の組み合わせが増えるばかりで、本末転倒だと気づきました。

結局、Safariに落ち着いています。iCloudとの連携、省電力性能、macOS標準のパスキー対応など、Apple製品で統一している環境であれば素直にSafariが最適という結論です。

## まとめ

GUIの常駐アプリをCLIに置き換え、メニューバーをOS標準機能で整理し、ブラウザもSafariに一本化しました。

やっとメニューバーが整理でき、`mo clean`一発でMacのクリーンナップもできる。そういう小さな快適さの積み重ねで、深呼吸できた心地がします。ゴミの山は鼻をつまんで走り抜けるに限ります。

## References

<!-- textlint-disable -->

{% references() %}

- [GitHub - tw93/mole](https://github.com/tw93/mole). "Mole - Deep clean and optimize your Mac"
- [GitHub - qarmin/czkawka](https://github.com/qarmin/czkawka). "Multi functional app to find duplicates, empty folders, similar images etc."
- [Sensei — Cindori](https://cindori.com/sensei). 「Mac Performance Monitor & Cleaner」
- [Cocktail — Maintain](https://www.maintain.se/cocktail/). 「A perfect mixture for macOS」
- [Apple Support](https://support.apple.com/guide/mac-help/change-menu-bar-settings-mchlad96d366/mac). "Change Menu Bar settings on Mac"
- [Engadget](https://www.engadget.com/ai/the-browser-company-stops-active-development-of-arc-in-favor-of-new-ai-focused-product-153045276.html). "The Browser Company stops active development of Arc in favor of new AI-focused product"

{% end %}

<!-- textlint-enable -->
