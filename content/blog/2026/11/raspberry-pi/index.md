+++
title = "3年落ちのRaspberry Pi 4は家庭内サーバーとして使い物になるか"
description = """
NASを導入してから出番のなかったRaspberry Pi 4を、久しぶりに引っ張り出しました。回線品質の計測、家中の広告ブロック、自分自身の状態の記録まで、手のひらサイズの1台にどこまで任せられるでしょうか。
"""
date = 2026-11-23T04:36:37+09:00
[taxonomies]
tags = ["Gadget", "Hardware"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.avif"
mermaid = true
+++

<!-- textlint-disable -->

{{< image src="cover.avif" alt="Cover" />}}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

<!-- more -->

3年ほど前に自宅でNextCloudを組んでいた[Raspberry Pi 4](https://link.amazon/B00TzKUYX)[^affiliate]を発掘しました。昨年UGREEN NASを導入したので放置されていたものです。もったいないので、再活用することにしました。

[^affiliate]: 当記事は、アフィリエイトリンクを含みます。

## 異音のファンから、ファンレスのアルミケースへ

以前はMiuzeiのファン付きケースを使っていましたが、ファンから異音がするようになっていました。今回はタカチ電機工業のアルミダイキャスト製ケースに替えました。ファンレスですが、上面がヒートシンク形状になっているので、効率よく排熱してくれそうです。

## 24時間動かすサーバーとしての下ごしらえ

まず、OSを最新の状態にしました。続いて、使っていないsnapdと、古いカーネルなど不要になったパッケージを削除しました。このPiはサーバーとして使い、操作もSSHでしか行わないので、デスクトップ環境も要りません。デスクトップのパッケージは残したまま起動ターゲットをCLIに切り替え、単独で起動していたVNCサーバー（wayvnc）も止めました。この時点で、起動直後のメモリ使用量は約330MiBでした。

OSやパッケージの更新は、unattended-upgradesで自動化しました。毎日2時30分に更新を適用し、カーネルの更新などで再起動が必要になったときだけ、3時に再起動します。更新の対象には、Debianのセキュリティ更新に加えて、Raspberry Piのリポジトリと、後述するCaddyとGrafanaのリポジトリも含めました。Pi-hole本体はaptでは更新されないので、これまでどおり手動で`pihole -up`を実行します。


## ポータブルHDDを24時間つなぎっぱなしにする落とし穴

NextCloudで使っていたHDDがそのまま残っていました。
SDカードは細かい書き込みを繰り返すと寿命が縮むので、頻繁に書き込むPi-holeのクエリ履歴とSmokePingの計測データはHDDへ移しました。
ログはlog2ramでRAMに置き、SDカードへの書き戻しは1日1回にしています。

HDDへ移した後にSMARTの値を見ると、ヘッドの退避回数が約30秒に1回、1日に約2,900回のペースで増えていました。2.5インチHDDの退避回数の目安は一般に30万〜60万回なので、このペースでは数か月から半年で達してしまいます。

接続したWD Elementsの3TBはポータブル型のHDDで、ときどきつないでまとめて読み書きする使い方を想定しています。このため、USB給電での省電力と落下時の保護を優先して、こまめにヘッドを退避させる設定（APM 128）で出荷されています。常時つないだまま数十秒おきに書き込む使い方には合いません。そこで、APMを254（ヘッドを退避させない）に変え、HDDを認識するたびにudevルールで設定し直すようにしました。変更後、退避回数はまったく増えていません。


## 自前の認証局で家の中だけHTTPS化する

各サービスの管理画面は、HTTPSで開けるようにしました。自宅と言えどHTTPのままだと、Pi-holeやGrafanaのパスワードが平文でLANに流れてしまいます。公開ドメインとLet's Encryptを使う案も検討しましたが、ドメインの更新やDNSサービスのトークン管理など、外部への依存が残ります。そこで、Pi上に自前のルート認証局（CA）を作り、リバースプロキシのCaddyに証明書を発行させることにしました。

ルート証明書を入れた端末は、そのCAが発行した証明書であれば、どのサイトのものでも信頼します。Piが乗っ取られると、攻撃者は任意のサイトの偽証明書を作れてしまいます。このため、ルート証明書には名前制約を付け、家庭内ネットワーク用に予約されている`home.arpa`（RFC 8375）の名前にしか発行できないようにしました。各サービスには`smokeping.home.arpa`のような名前を付け、Pi-holeのローカルDNSで解決します。ルート証明書はMacとAndroidに入れました。証明書はCaddyが自動で更新し、インターネットへの接続も要りません。

最後に、各サービスへのリンクを並べたトップページを`pi.home.arpa`に置きました。

<!-- textlint-disable -->

{{< image src="top.avif" alt="トップメニュー" caption="pi.home.arpaのトップメニュー" />}}

<!-- textlint-enable -->

## 14階のHome 5Gの回線品質をSmokePingで見張る

<!-- textlint-disable -->

{{< image src="smokeping.avif" alt="SmokePingのグラフ" caption="SmokePingで計測した4つの宛先の遅延" />}}

<!-- textlint-enable -->

自宅では、13階以上での利用を推奨していないHome 5Gを14階で使っています。そこで、自宅からのネットワークの品質をSmokePingで監視しています。SmokePingは、指定した宛先に定期的にpingを送り、遅延とパケットロスの推移をグラフにするツールです。

宛先は、自宅のルーター、Google、Cloudflare DNS（1.1.1.1）、Google DNS（8.8.8.8）の4つです。

```text,name=/etc/smokeping/config.d/Targets
+ Internet
menu = Internet
title = インターネット接続

++ Router
menu = ルーター
title = 自宅ルーター
host = 192.168.1.1

++ Google
menu = Google
title = Google
host = www.google.com

++ Cloudflare_DNS
menu = Cloudflare DNS
title = Cloudflare DNS (1.1.1.1)
host = 1.1.1.1

++ Google_DNS
menu = Google DNS
title = Google DNS (8.8.8.8)
host = 8.8.8.8
```

ルーターを宛先に含めたのは、遅延の原因が家の中にあるのか外にあるのかを切り分けるためです。ルーターまでが速いのに外部の宛先だけが遅ければ、原因は回線から先にあります。外部の宛先を複数にしておけば、遅れているのが1か所だけなのか全部なのかで、相手側の問題か回線の問題かも見分けられます。

## Pi-holeで家中の広告をまとめて減らす

<!-- textlint-disable -->

{{< image src="pihole.avif" alt="Pi-holeのダッシュボード" caption="Pi-holeのダッシュボード" />}}

<!-- textlint-enable -->

Pi-holeは、広告やトラッキングに使われるドメインの名前解決を遮断するDNSサーバーです。家中の端末に表示される広告を、まとめて減らすために導入しました。

インストールには公式のスクリプトを使いました。スクリプトは一度ファイルに保存し、中身を確認してから実行しています。問い合わせ先（上流のDNS）はCloudflareで、ブロックリストはStevenBlackのリスト（約7万6千ドメイン）です。導入後もすぐには家全体に広げず、まずMacだけDNSをPi-holeに向けて試しました。

Pi-holeはDNSとして使い、DHCPには使っていません。端末へのIPアドレスの割り当ては、これまでどおりOrbiのルーターが行います。OrbiのDNS設定をPi-holeに向けると、端末はOrbiに問い合わせ、OrbiがPi-holeに転送します。端末側の設定は何も要りません。このとき、セカンダリDNSは空欄のままにしました。1.1.1.1などを入れると、一部の問い合わせがPi-holeを素通りしてしまうからです。

この構成では、Pi-holeから見ると問い合わせはすべてOrbiから届くので、端末ごとの区別はできません。また、Piが止まると家全体で名前解決ができなくなります。そのため、HDDへ移したのはクエリ履歴だけで、DNSの動作に必要なファイルはSDカードに残してあります。HDDが壊れても、失われるのは統計だけで、名前解決は止まりません。万一Piが止まったときは、OrbiのDNS設定を自動取得に戻せば復旧できます。

最近は、ブログですら「読ませる気があるのか」と疑うほど広告が入っているサイトが多くなりました。Pi-holeを入れてから広告の表示が大幅に減り、ストレスが軽くなりました。

## ファンレスで大丈夫か、Pi自身の状態を記録する

<!-- textlint-disable -->

{{< image src="grafana.avif" alt="Grafanaのダッシュボード" caption="GrafanaのダッシュボードでSoC温度と性能制限を表示" />}}

<!-- textlint-enable -->

Pi自身の状態も記録することにしました。目的は3つあります。

- 短時間の負荷の山と長期の傾向から、ハードウェアの資源が足りているかを評価する
- ファンレスのケースで冷却が足りているかを確かめる
- ADS-B（航空機が発信する位置情報）の受信など、これから追加するサービスを載せられるかを判断する材料にする

記録しているのは次の項目で、記録の間隔は1分です。

- SoCの温度
- 温度や電圧低下による性能制限（スロットリング）の発生
- CPUの使用率、I/O待ち、ロードアベレージ
- メモリとスワップの使用量
- SDカードとHDDの空き容量

収集にはPi上にPrometheusとnode_exporterを仕込みました。データは次の流れでHDDに保存されます。

<!-- textlint-disable -->

{% <mermaid> %}
flowchart LR
    K["Linuxカーネル<br>温度・CPU・メモリ・空き容量"] --> N["node_exporter"]
    V["vcgencmd get_throttled<br>性能制限のフラグ"] --> S["自作スクリプト<br>1分ごとに実行"]
    S --> F["/run のファイル<br>RAM上"]
    F --> N
    N --> P["Prometheus<br>1分ごとに取得"]
    P --> H[("HDD")]
{% </mermaid> %}

<!-- textlint-enable -->

温度、CPU、メモリ、空き容量は、node_exporterがLinuxカーネルから読み取ります。性能制限のフラグはRaspberry Pi固有の情報で、node_exporterでは取得できません。そこで、`vcgencmd get_throttled`の値を小さなスクリプトで1分ごとにファイルへ書き出し、node_exporterのtextfile collectorで読ませています。前回の記録以降に起きた性能制限も、このフラグで検出できます。

このファイルは最新の値だけを持つ受け渡し用で、残しておく必要はありません。そのため、置き場所は再起動で消えるRAM上の`/run`にして、毎分の書き換えでSDカードへ書き込まないようにしました。スクリプトの実行ログも、SDカードには書きません。スクリプトが止まって値が古くなったときは、ファイルの更新時刻から記録の欠損として判別できます。

node_exporterが公開した値は、Prometheusが1分ごとに取得し、HDDに保存します。PrometheusはHDDがマウントされていなければ起動しないので、HDDが外れたときにSDカードへ書き込むことはありません。表示はGrafanaで行い、GrafanaのデータもHDDに置いています。

Grafanaは初期状態だと、使わないデータソースのプラグインまでそれぞれ常駐し、メモリを約755MB使っていました。Prometheus以外の18個のプラグインを無効にしたところ、約386MBまで減りました。

ファンレスのケースですが、起動してから性能制限は一度も起きていません。

## まとめ

NASの導入で出番を失っていたRaspberry Pi 4は、回線の監視、家全体の広告ブロック、自分自身の状態の記録を1台でこなす家庭内サーバーとして復活しました。今では家中の端末で広告が減り、回線の調子もブラウザからいつでも確かめられます。

SmokePingの記録からは、14階のHome 5Gでも回線の品質に大きな問題はなく、昼間にやや遅くなる程度だと分かりました。

Pi-holeは1日に約7千件、問い合わせ全体の約14%をブロックしています。止めているのは画面の広告だけでなく、アプリが裏で送っている計測用の通信にも及びます。

Grafanaで見るPiの温度は40℃台にとどまり、性能制限は一度も起きていません。ファンレスのケースでも、今の負荷なら排熱は足りています。

後継のPi 5も出ていますが、メモリの高騰を受けて、[2026年に入って値上げが続いています](https://www.raspberrypi.com/news/more-memory-driven-price-rises/)。処理性能は上がっていても、この用途ではそれを生かす場面がありません。推奨電源も27Wに上がっています。Pi 4用の3Aの電源のままでは、USB機器への給電が合計600mAに制限されるので、ポータブルHDDのようなUSB給電の機器をつなぐには心許なくなります。この程度の用途なら、Pi 4は意外に良い選択です。

眠っているRaspberry Piがあるなら、新しいモデルを買う前に、まずは家庭内サーバーとして働かせてみてはいかがでしょうか。

---

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_20261123055646237666?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fphysical-computing%2Ftsi-pi046-4%2F%3Frafcid%3Dwsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fphysical-computing%2Ftsi-pi046-4%2F%3Frafcid%3Dwsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/physical-computing/cabinet/tsi-pi046.jpg?_ex=128x128" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_20261123055646237666?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fphysical-computing%2Ftsi-pi046-4%2F%3Frafcid%3Dwsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fphysical-computing%2Ftsi-pi046-4%2F%3Frafcid%3Dwsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >Raspberry Pi4 Model B（4GB）</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px;background: url('//img.yomereba.com/kl.gif') 0 -50px no-repeat;padding: 2px 0 2px 18px;white-space: nowrap;"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_20261123055646237666?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2FRaspberry%2520Pi%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt&m=http%3A%2F%2Fm.rakuten.co.jp%2F" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px;background: url('//img.yomereba.com/kl.gif') 0 0 no-repeat;padding: 2px 0 2px 18px;white-space: nowrap;"><a href="https://www.amazon.co.jp/gp/search?keywords=Raspberry%20Pi&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>
