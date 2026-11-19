+++
title = "nginxとphpの重大修正が同日に! エンジニアはパッチ祭りな夜"
description = """
Webを支えるnginxとPHPで、重大な脆弱性をふさぐ更新が同じ日に重なりました。PHPの修正版が出るのは23時ごろです。明日の朝もいつもどおりサイトを使えるように、エンジニアは今夜、何をするのでしょうか。
"""
date = 2026-11-19

[extra]
social_media_card = "ogp.webp"
local_image = "cover.avif"

[taxonomies]
tags = ["Tech", "Security"]
+++

<!-- textlint-disable -->

{{< image src="cover.avif" alt="Cover" />}}

<!-- textlint-enable -->

今日の未明、Webサーバーのnginxで、認証なしで外部からコードを実行される恐れのある脆弱性の修正版が公開されました。そして今夜23時から23時30分の間には、PHPの重大なセキュリティリリースが予定されています。時刻はいずれも日本時間です。

Webの裏側を支える2つのソフトウェアの修正が、同じ日に重なりました。サーバーを預かるエンジニアにとっては、影響の確認と更新が重なる一日です。

## nginx：10年以上前から潜んでいたHTTP/2の穴

nginxはWebサーバーのソフトウェアです。[Netcraftの2026年9月の調査](https://www.netcraft.com/blog/september-2026-web-server-survey)では、Webサーバーをコンピューターの台数で数えると、nginxが44%を占め、Apacheを抜いて首位です。

11月19日未明、nginxは[1.31.9（mainline）](https://github.com/nginx/nginx/releases/tag/release-1.31.9)と[1.30.7（stable）](https://github.com/nginx/nginx/releases/tag/release-1.30.7)を公開しました。脆弱性の修正はmainlineが10件、stableが9件です。

<!-- textlint-disable -->

{% <aside position="right"> %}
Criticalとは、最悪の深刻度。今夜中修正すべきというレベル。
{% </aside> %}

<!-- textlint-enable -->

なかでも注意が必要なのはCVE-2026-123007です。Webの通信方式の1つであるHTTP/2で、通信量を調整する処理（フロー制御）に不具合があります。この不具合でメモリが壊れると、通信を処理するnginxのプロセスは異常終了することがあります。メモリの配置を毎回変える防御機能（ASLR）を無効にしているか、攻撃者がこの防御を回避できる場合は、認証なしにサーバー上で任意のコードを実行される恐れもあります。[Ubuntuの脆弱性情報](https://ubuntu.com/security/CVE-2026-123007)には、CVSS v4.0で9.2（**Critical**）と記載されています。nginxの[公式アドバイザリ](https://nginx.org/en/security_advisories.html)では、2015年に公開された1.9.5から影響を受けるとされています。HTTP/2の処理には、もう1件、解放済みのメモリを使ってしまう不具合（CVE-2026-123633）も見つかっています。

CVE-2026-123007の対象は、影響を受けるバージョンのnginx自体がHTTP/2を受け付けている構成です。この条件に該当すれば、静的ファイルだけを配信するサーバーも影響を受けます。今回の更新には、HTTP/3やメールプロキシなどの修正も含まれます。

nginxは、自分で「Webサーバーとして入れた」覚えがない場所にもよく入っています。

- 公開WebサイトのWebサーバー
- アプリケーションの前に置くリバースプロキシやロードバランサー（通信の取り次ぎや振り分けを行う仕組み）
- KubernetesのIngress（外部からの通信をクラスター内に振り分ける入口）
- コンテナイメージに同梱されたnginx
- アプライアンス製品やクラウドサービスの内部

今回厄介なのは、こうした「見えないnginx」まで洗い出す必要があることです。

## PHP：PHP2Shellの翌月にまたCRITICAL

PHPは10月にも、認証なしで外部からコードを実行できる2件の脆弱性（[PHP2Shell](@/blog/2026/10/php2shell-critical-rce/index.md)、CVE-2026-109618とCVE-2026-109619）を修正したばかりです。こちらは実際に悪用され、米国CISAの「悪用が確認された脆弱性」の一覧にも載りました。その後に書いた「[PHP2Shell収束後に検討すべき「情報発信サイトの脱CMS」](@/blog/2026/10/after-php2shell-leaving-cms/index.md)」では、パッチを当ててもPHPが動き続ける限り次の脆弱性は防げないと指摘しました。

その騒ぎが収まらないうちに、PHPの開発チームは11月18日、[次のセキュリティリリースを予告](https://www.php.net/archive/2026.php)しました。公開は今夜23時から23時30分の間です。サポート中のすべてのバージョンが対象で、含まれる問題の深刻度は最高で**CRITICAL**とされています。PHPによると、CRITICALの問題の影響を受けるのは、標準でない設定や珍しい構成に限られます。詳細と修正版のバージョン番号は、リリースと同時に公表される予定です。

これとは別に、PHPは[10月23日付の個別告知](https://www.php.net/archive/2026.php#2026-10-23-1)で、ファイルアップロードの進み具合を記録する機能（session upload progress）に、外部からコードを実行される恐れがあると公表しました（CVE-2026-115560）。影響を受けるのは、この機能が有効で、利用者のログイン状態などを記録する「セッション」のデータ形式を特定の組み合わせで実行時に切り替える構成です。この問題の詳細は次回のリリースで公表される予定です。それまでの暫定策として、PHPは`session.upload_progress.enabled = 0`でこの機能を止める方法を案内しています。

## 深夜のパッチ祭り

2つの修正は、どちらも最悪の深刻度の問題を含みます。影響のあるサービスを預かる担当者には、今夜中の対応が求められます。

| 項目 | nginx | PHP |
|---|---|---|
| 修正版の公開 | 11/19未明（公開済み） | 11/19 23:00〜23:30（予定） |
| 最高の深刻度 | CVSS v4.0で9.2（Critical） | CRITICAL |
| 更新の目安 | 今夜中 | 修正版の公開後、今夜中 |

多くのエンジニアは、この2つの修正を今夜中に当てるよう求められているはずです。PHPの公開は23時ごろですから、作業は深夜に及ぶでしょう。

問題が起きたときに元へ戻せるようにバックアップを取り、パッチ（修正プログラム）を当て、サービスがいつもどおり動くかを確かめます。nginxが多くのシステムに関わっていれば、更新の影響が及ぶシステムを1つずつ検証する必要があります。PHPの更新がアプリケーションの動作に影響する場合は、その仕組みを知るアプリケーションの担当者による対応も必要です。

Webを支える2つのソフトウェアで、重大な修正への対応が同じ日に重なるのですから、尋常ではありません。

## まとめ

nginxでは、2015年に公開されたバージョンにまで影響する脆弱性が見つかりました。PHPは2か月続けてCRITICALの修正を出します。Webを支える基盤のソフトウェアにも重大な脆弱性はまだ眠っていて、それがいつ見つかるかは誰にも選べません。

PHP2Shellの発見には生成AIが使われました。[10月の記事](@/blog/2026/10/after-php2shell-leaving-cms/index.md)でも書いたとおり、生成AIの活用が広がるにつれて、今後は脆弱性の発見頻度も大幅に上がっていくはずです。重要なソフトウェアの重大な修正が同じ日に重なる今夜のような事態も、これから増えていくでしょう。こうした夜が来ることを前提に、どこで何が動いているかを把握し、修正をすぐに当てて確かめられる体制を整えておくことが、Webサービスを動かし続ける条件になりつつあります。

## References

<!-- textlint-disable -->

{% <references> %}

- [nginx](https://github.com/nginx/nginx/releases/tag/release-1.31.9). 「nginx 1.31.9（mainline）のリリースノート」
- [nginx](https://github.com/nginx/nginx/releases/tag/release-1.30.7). 「nginx 1.30.7（stable）のリリースノート」
- [nginx](https://nginx.org/en/security_advisories.html). 「nginx security advisories」
- [CERT-EU](https://www.cert.europa.eu/publications/security-advisories/2026-022/pdf). 「nginxセキュリティ勧告（11月18日）」
- [PHP](https://www.php.net/archive/2026.php). 「PHP公式ニュースアーカイブ（11月18日のリリース予告）」
- [PHP](https://www.php.net/archive/2026.php#2026-10-23-1). 「セッションアップロード進捗に関する告知（10月23日）」
- [nginx](https://nginx.org/en/docs/control.html#upgrade). 「公式の無停止更新手順」

{% </references> %}

<!-- textlint-enable -->
