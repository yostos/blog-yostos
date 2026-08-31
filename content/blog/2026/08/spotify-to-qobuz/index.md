+++
title = "SpotifyからQobuzへ、音楽を聴く時間を取り戻す"
description = """\
音楽を聴くつもりでSpotifyを開き、気がつくとPodcastばかり聞いていました。\
レコメンドに流されるのではなく、自分で選んで音楽を楽しみたいと思い、ハイレゾ配信のQobuzに移りました。\
エディトリアルの厚みと音質、そして再生環境の制約について書きました。\
"""
date = 2026-08-15T07:00:00+09:00
[taxonomies]
tags = ["Entertainment", "Listening"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = """
- SpotifyだとPodcastばかり聞いてしまうので、Qobuzに乗り換えた
- Qobuzはレビューや特集記事が前面に出る作りで、音楽雑誌からレコードを買っていた時代を彷彿とさせる
- Qobuzのハイレゾ音源の音質は高いが、差が出るのは有線接続とDACを用意した場面に限られる
- 3年前に買ったウォークマンNW-A300を再生環境に
"""
mermaid = true
+++

<!-- textlint-disable -->

{{ image(src="cover.webp",alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

最近、SpotifyでPodcastばかり聞いていて音楽をほとんど聞いていないことに気付きました。
これはさすがに違うだろうと、Spotifyから[Qobuz](https://www.qobuz.com/)に一度乗り換えをすることにしました。

## Qobuzとは

そこでQobuzを試しはじめました。フランス発のハイレゾ配信サービスで、日本版は2024年10月23日にプレオープン、翌24日に正式ローンチしています。Qobuzは日本でのハイレゾ配信をリードしてきたe-onkyo musicを統合する形で日本でのサービスを開始しました。

Qobuzを開いてまず感じたのは、静かだということでした。ホーム画面が「あなたのために」を主張してきません。代わりに並んでいるのは、新譜のレビュー、ジャンルごとの特集記事、編集部が選んだアルバムといった、人間が書いたものです。

Qobuzは自らを「音楽メディア」に近い立ち位置として打ち出しています。アルバムのページにはライナーノーツやクレジットが載っていて、誰が演奏し、誰がミックスしたのかを読めます。読んでから聴くか、聴いてから読むかは自分で決めます。

この違いは大きいと感じました。Spotifyのレコメンドは、私の再生履歴を元に私が次に何を聴きたいかを推測して差し出してくれます。
便利ですが、そこには私の意志がなく惰性的な聴き方になりがちです。
一方でQobuzのレビューや特集は、読んで判断する手間を要求してきます。その手間こそが音楽を能動的に聴くということなのだと、しばらく使って気づきました。

昔「ミュージック・マガジン」や「FM fan」を読んで、アルバムを買っていた頃の感覚に近いかもしれません。
ジャケットと評論を頼りに、外れを引くことも込みで選んでいたあの感じです。
好みの音楽を聴くという点で効率は悪いのですが、昔見つけて聴き始めた音楽のほうが記憶に残っています。

また、e-onkyoを買収したことから分かるように、Qobuzはサブスクリプションとは別に楽曲のダウンロード販売を持っています。
配信が終わっても手元に残る形で買えるのは、ストリーミング一本の環境にはない選択肢です。

## Qobuzの音質について

Spotifyも2025年9月からPremium会員向けにロスレス配信を始めています。追加料金なしで最大24bit/44.1kHzのFLACが聴けるようになったので、音質だけを理由に他へ移る必然性はかなり薄くなりました。

それでも、上限には差があります。

| 項目         | Spotify Premium | Qobuz Studio               |
| :----------- | :-------------- | :------------------------- |
| ロスレス形式 | FLAC            | FLAC                       |
| 最大スペック | 24bit/44.1kHz   | 24bit/192kHz               |
| 月額（個人） | 1,080円         | 1,480円（年額は1,280円）   |
| カタログ     | 1億曲以上       | 1億曲以上                  |
| 楽曲の購入   | 不可            | 可（ダウンロード販売あり） |

Spotifyのロスレスは、サンプリング周波数がCDと同じ44.1kHzで頭打ちです。JEITAの定義ではサンプリング周波数か量子化ビット数のどちらかがCDを超えていればハイレゾなので、24bit/44.1kHzもハイレゾには違いありません。ただし配信元が192kHzで用意している音源を、そのサンプリング周波数のまま受け取ることはできません。Qobuzは最大192kHzまで扱うので、ハイレゾ音源をハイレゾのまま再生できます。

ただし、この差が耳に届く条件はかなり限られます。BluetoothやAndroidのオーディオ経路で聴いている限り、途中で必ず圧縮が入るので、44.1kHzと192kHzの区別はつきません。ハイレゾの恩恵を受けるには、有線接続とDACを用意して、そこまでのデータ経路を切らさない必要があります。Spotifyもこの点は同じで、ロスレスに対応するのはSpotify Connectの対応機器や有線環境に限られます。

正直なところ、日常のリスニングでハイレゾの差が出る場面は、そう多くありません。移動中はほぼ意味がないと言っていいでしょう。きちんとしたオーディオ機材がないと、音の違いはそれほど分かりません。それでも腰を据えて聴くときに上限が高いことには意味があると考えています。カタログの多くはCD音質のままですが、ハイレゾで用意されているアルバムに当たったときの情報量は、やはり違います。

## 再生環境としてのウォークマン

折角なのでハイレゾで聞こうと、数年前に購入したSONYウォークマンNW-A300を引っ張り出してきました。
中身はAndroidですが、44.1kHz系と48kHz系のデュアルクロックとフルデジタルアンプ「S-Master HX」により、ハイレゾ音源を本来のサンプリング周波数系統のまま再生が可能です。[^1]

[^1]: 有線でPCM 384kHz/32bitまで対応、ただし352.8kHz以上はダウンコンバート、DSDはLPCM変換再生

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/g0000015.9srin702.g0000015.9srio330/kaereba_main_202608141730133457?pc=https%3A%2F%2Fproduct.rakuten.co.jp%2Fproduct%2F-%2F6f3ecffd12edd56d4e6e7c258af710bd%2F&m=http%3A%2F%2Fm.product.rakuten.co.jp%2Fproduct%2F6f3ecffd12edd56d4e6e7c258af710bd%2F&rafcid=wsc_i_ps_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://r.r10s.jp/g/gran_img/im/PEZ/XHG/AMN/W9S/52aa52ad78d7393de1b3c5cd4f210dad.jpg?_ex=320x320" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/g0000015.9srin702.g0000015.9srio330/kaereba_main_202608141730133457?pc=https%3A%2F%2Fproduct.rakuten.co.jp%2Fproduct%2F-%2F6f3ecffd12edd56d4e6e7c258af710bd%2F&m=http%3A%2F%2Fm.product.rakuten.co.jp%2Fproduct%2F6f3ecffd12edd56d4e6e7c258af710bd%2F&rafcid=wsc_i_ps_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >SONY ウォークマン NW-A306 HC</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/g0000015.9srin702.g0000015.9srio330/kaereba_main_202608141730133457?pc=https%3A%2F%2Fproduct.rakuten.co.jp%2Fproduct%2F-%2F6f3ecffd12edd56d4e6e7c258af710bd%2F&m=http%3A%2F%2Fm.product.rakuten.co.jp%2Fproduct%2F6f3ecffd12edd56d4e6e7c258af710bd%2F&rafcid=wsc_i_ps_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=NW-A306&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>

3.5mmの4極ケーブルをつないで、ちょっとよいイヤフォンで聞いています。
Bluetoothを挟まないので、Qobuzのハイレゾ音源をそのまま鳴らせます。条件は、次の通りです。

- 設定で「ハイレゾストリーミング」をONにする(OFFでは通常のAndroidオーディオ経路として48 kHz / 16 bitに制限)
- 音量設定で「メディアの音量」を最大にしておく。ヘッドフォン音量は「音量」で調整する

<!-- textlint-disable -->

{% aside(position="right") %}
**DSEE**: 圧縮で失われた高音域や細かな音を補完してハイレゾ相当まで引き上げるソニーの技術。有線接続なら最大192kHz/32bitまで拡張
{% end %}

<!-- textlint-enable -->

ウォークマンは再生アプリの「W.ミュージック」と「音質設定」アプリを分けていて、
ハイレゾストリーミングをオンにしていれば音質設定は「W.ミュージック」以外のアプリの再生にも共通で効きます。
「音質設定」アプリを使うと、ClearAudio+技術で、イコライザーやDSEEといった項目を自分で詰めるかわり、出力する音に合わせてソニーが最適と考える設定を自動で当ててくれる機能が使えます。

この設計としては筋がよく、Qobuzで聴いていてもその恩恵を受けられるのでまずまずの音で聴けます。

DACを持ち歩くよりお手軽ですが、現状のウォークマンには難点もあります。

私がNW-A300を購入したのは3年前の2023年ですが、そこから新機種が出ていません。後継機の発表はなく実質的にソフトウェアアップデートで延命している状態です。折角Androidベースにしたのに、3年以上新機種発表されないのはなかなか厳しい話です。

個人的には専用ハードをやめてAndroidベースへ移したのが失敗だったのではないかと思います。

- ストリーミングで聴く人はそれほど音質に拘りがないからウォークマンをわざわざ買ったりしない
- 汎用的なAndroid機ベースの為、「よい音」で聴くためには「ハイレゾストリーミングの設定」やマスターボリュームとは別の「メディアの音量」の最適化が必要
- OSもAndroid依存。SONYは更新を続けており、Android 12から13へのバージョンアップやセキュリティパッチの提供もあるが、現在最新のAndroid 15に追いついていない
- 折角使い勝手向上のためハードウェアボタンを用意したが、Androidの操作系と齟齬が出てわかりにくい(例:ロックスイッチを入れてもAndroidの画面を操作できてしまう)

ウォークマンは「カセットテープ」という当時のメディアで新しい音楽体験を提案した商品でした。
現在は専用機を名乗りながら、現代のストリーミングにふさわしいハードウェアを用意できず、中途半端な作り込みのまま製品を出し続けているように思います。

ウォークマンが属するエレクトロニクス系のセグメント（現在のET&S分野）の売上を並べてみました。

<!-- textlint-disable -->

{% mermaid() %}
xychart-beta
title "ソニー ET&S分野の売上高（兆円）"
x-axis [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
y-axis "売上高（兆円）" 0 --> 4
bar [3.01, 3.54, 3.37, 3.00, 2.38, 2.60, 2.32, 1.99, 2.07, 2.34, 2.48, 2.45, 2.41, 2.26]
{% end %}

<!-- textlint-enable -->

ピークだった2013年度の3兆5,399億円から、2025年度は2兆2,605億円まで落ちています。同じ期間にグループ全体の売上は7兆7,673億円から12兆4,796億円へ6割増えているので、この分野だけが縮んだことになります。売上構成比は18%、営業利益では11%です。

いまソニーを支えているのはゲームと音楽です。2025年度の音楽分野は売上2兆1,201億円に対して営業利益4,470億円、利益率21.1%でした。売上はET&S分野とほぼ同じなのに、利益は約2.8倍です。しかもその中身は原盤や楽曲の権利をストリーミング各社にライセンスする商売なので、私がQobuzに払った金の一部もここに入ります。聴かれさえすれば、どの機械で聴かれようと関係ありません。

「オーディオ機器メーカー」としてのSONYが凋落しているのは、こういうところなのだろうと私は思っています。

## おわりに

それでも、Qobuzを開くようになってから音楽を聴いている時間は明らかに増えました。
理由は音質ではなく、アプリを開いたときにPodcastが目に入らないという、それだけのことのような気もします。

結局のところ、サービスを変えたというより、自分の聴き方を変えたかったのだと思います。
何を聴くかを自分で決め、そのために少し不便なほうを選ぶというのもアリかなと思います。
Spotifyとは月額数百円の差があるので、しばらくこの状態で過ごしてみてあらためて判断するつもりです。

## References

<!-- textlint-disable -->

{% references() %}

- ソニー. [ウォークマン NW-A300シリーズ](https://www.sony.jp/walkman/products/NW-A300_series/)
- ソニー. [ハイレゾストリーミング機能を使う（NW-A300シリーズ）](https://www.sony.jp/support/walkman/guide/nw-a300s/contents/TP1000735012.html)
- ソニーグループ. [投資家情報](https://www.sony.com/ja/SonyInfo/IR/)

{% end %}

<!-- textlint-enable -->
