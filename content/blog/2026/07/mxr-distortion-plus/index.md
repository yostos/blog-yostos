+++
title = "原点回帰 - 歪みはMXR Distortion+"
description = """
エフェクターボードをどこまで削れるか試してきた延長で、今度は歪みそのものを原点まで遡ってみることにしました。オペアンプ1個とダイオード2本しか持たないMXR Distortion+を購入し、回路を確かめながら高中正義が『Saudade』で使ったというセッティングを実際に試しています。
"""
date = 2026-07-17T14:45:52+09:00
[taxonomies]
tags = ["Guitar Pedals"]
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

[前回の記事](/blog/2026/06/guitar-effectors/)で、高機能なエフェクターを次々と手放してシンプルな構成に行き着いた話を書きました。
その後、[Xotic Soul Driven](/blog/2026/07/soul-driven/)を買い足したのですが、どうもしっくりきません。
ちょっと悩んでもっと単純な原点まで遡ることして、今更まさかのMXR Distortion+ (M104) を購入しました。

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/g00s2rs5.9srinf7e.g00s2rs5.9sriofc7/kaereba_main_20260721173617837?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjeugia%2F0710137014220-77%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fjeugia%2Fi%2F10048656%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/jeugia/cabinet/km/mxrm104.jpg?_ex=128x128" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/g00s2rs5.9srinf7e.g00s2rs5.9sriofc7/kaereba_main_20260721173617837?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjeugia%2F0710137014220-77%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fjeugia%2Fi%2F10048656%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >MXR M104 Distortion+ギターエフェクター ディストーション</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_20260721173617837?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2FDistortion%2520%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt&m=http%3A%2F%2Fm.rakuten.co.jp%2F" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=Distortion%20&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>

## MXR Distortion+の回路的な特徴

MXR Distortion+は「オペアンプ1個+クリッピングダイオード2本」という、歪みペダルとしては極めてシンプルな回路を持っています。1MΩの「Distortion」ポットがオペアンプの帰還ループを可変制御し、最大で約46dBという大きなゲインを作ります。オペアンプ出力後段には、ダイオード2本を逆並列に接続したハードクリッピング回路があり、波形の頭を潰して歪みを作る構成です。"Distortion"というネーミングの割に歪まないためオーバードライブだという人がいますが、ハードクリッピングなので回路的に見れば「ディストーション」です。

クリッピングダイオードは、1970年代のスクリプトロゴ機から現行のM104まで一貫してゲルマニウムダイオード(1N270または1N60系)です。順方向電圧が0.3〜0.45Vと低く、ソフトな飽和特性を持つため、角の丸いマイルドな歪みになります。Dunlop公式のM104マニュアルには"Organic, germanium-powered clipping"と明記されており、現行品もゲルマニウムダイオードであることは一次資料で確認できます[^mxr-dunlop]。

<!-- textlint-disable -->

{% admonition(type="warning", title="「現行品はシリコンダイオード」という誤情報に注意") %}
購入前に調べていて気になったのは、「現行品はシリコンダイオード(1N4148等)に変更されている」という記述が一定数出回っている点です。しかしメーカー公式マニュアルの記載と食い違うため、DIYクローンや改造記事の情報が、いつの間にか「現行品の標準仕様」であるかのように広まったものと考えられます。この手の製品仕様は、可能な限りメーカー公式の一次資料に当たるのが安全だと感じました。

これを信じて「スクリプト版でなければ本物でない」や「ヴィンテージでなければDistortion+の音は出ない」などと言われることがあります。
音は違うと思いますが、そもそもヴィンテージは個体差が激しいエフェクターなので、個人的には現行品で十分だと思います。

電源はオリジナルが9V電池駆動のみだったのに対し、現行M104はDCジャック(センターマイナス9V)にも対応し、赤色LEDインジケーターとトゥルーバイパスを備えており使い勝手もよくなっています。
{% end %}

<!-- textlint-enable -->

本機にはトーン回路がありません。イコライザーの類は一切なく、音色調整はギター側のボリューム/トーンとアンプ側のEQに委ねる設計です。

## 現代のディストーションとの違い

MXR Distortion+の設計は、現代の一般的なディストーションと比べると際立ってシンプルです。主な違いを表にまとめます。

| 観点             | MXR Distortion+                                                                                                | 現代の一般的なディストーション                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 回路段数         | オペアンプ1段+ダイオードクリッピングのみ                                                                       | 複数段のゲイン/クリッピング段を重ねることが多い                                       |
| トーン/EQ        | なし(素通し)                                                                                                   | Tone、あるいはBass/Mid/Trebleなど独立したEQ回路を持つものが多い                       |
| ゲインの効き方   | ポットの可変幅は大きいが単段クリッピングのため早期に頭打ちになり、聴感上の飽和感は控えめ                       | 複数段のクリッピング/ブースト段を重ね、より深く複雑な飽和感やサスティーンを作り込める |
| クリッピング方式 | ハードクリッピング(ゲルマニウムダイオード)                                                                     | ハードクリッピング(シリコンダイオードやLEDクリッピング、多段クリッピングなど多様)     |
| 出力段           | クリッピング後にパッシブなOutputポットのみで、メイクアップゲインを持たない(古典的な歪みエフェクターでは一般的) | クリッピング後に能動的なゲイン段を追加し、音量低下を補うものが多い                    |
| 実際の使われ方   | アンプ側の歪みに足して「ブースト+荒さ」を加える運用が定番                                                      | 単体でクリーンアンプから完成された歪みサウンドを作る設計が主流                        |

同じハードクリッピング方式のBoss DS-1とは仕組みこそ近いものの、使用ダイオードがDS-1はシリコン、Distortion+はゲルマニウムと異なり、DS-1のほうが角の立った硬い歪みになります。加えてDS-1はTone回路で中域を削ったスクープ系のモダンな音も作れますが、Distortion+はノブがない分、常に同じ帯域感で鳴り続けます。

## MXR Distortion+の一般的な使い方

現代のディストーションほど歪まない為、単体ではなく**少し歪ませたアンプ**に歪みを足すために使うのが一般的です。

Distortion+は、かなり音量が下がります。
従って、**Outputつまみはとにかく最大**に設定します。

その上でクランチが欲しいときはDistortionを低めに、リードで前に出したいときは3時以上に上げます。
これで70年代的なハードロックの音が得られます。

本機にトーン回路がないため、Distortion+自体の設定は以上で完結します。
音色はギターのボリューム/トーンノブ、アンプのEQ、後段のペダルで追い込む前提になります。ギターボリュームを絞ると歪みが素直にクリーンアップする特性があるため、ギター側の操作との相性がよいのも特徴です。
可能であれば、RC Boosterのようなクリーンブース
ターを後に置くとよいかも知れません。音量を補正しアンプをプッシュできイコライジング補正も可能になります。

## 高中正義と『Saudade』のセッティング

高中正義さんは、少なくとも1980年代前半まではMXR Distortion+のユーザーだったとされています。ライブではブギー(Mesa/Boogie)系アンプ自体を歪ませて使うこともあったようですが、アルバム『Saudade』については本人がインタビューで次のように証言しています[^saudade-score]。

> 僕の場合ジム・ケリー(Jim Kelly)のナチュラル・オーバー
> ドライブは活用しない。ヴォリューム「3〜4」ぐらいでオーバードライブは全てDistortion+。あと、コンプレッサーもかか
> ってるけど。つまりDistortion+Compressorのオーヴァードライブサウンド。MXRのDyna Compはストラトでマイルドなト
> ーンが欲しい時くらいで、メインはOrange Squeezerの方。

クリーンアンプに対してDistortion+単体でオーバードライブを作るというのは、前章で触れた「アンプ側を軽くドライブさせた状態で使う」という一般的な定番とは異なるアプローチです。ただ、前段にOrange Squeezerを置いているので、そこでゲインを稼いでいるのかもしれません。

手元にはOrange Squeezerのクローンである[Henretta Engineering Orange Whip Compressor](/blog/2026/06/guitar-effectors/)があったので、同じ順番(Orange Whip Compressor→Distortion+-> クリーンにセッティングしたSimplifier MK-II)で試してみました。

結果は本当に『Saudade』の頃のあの音に近いと感じました。カバー演奏「A Fair Wind」は以下でお聞きください。

<!-- textlint-disable -->

{{ youtube(id="EpUqd7L04ic") }}

<!-- textlint-enable -->

演奏はYAMAHA SG-175で前半はリアピックアップ、後半はフロントピックアップです。

ゲルマニウムダイオードの柔らかい飽和特性と、
Orange Squeezer系のナチュラルなサステイン/コンプレッションとブーストの組み合わせによって、
あの時代の高中サウンドに近いオーバードライブが得られることを、身をもって確認できました。

## まとめ

MXR Distortion+は、オペアンプ1個とダイオード2本しか持たないミニマルな回路にもかかわらず、半世紀近く現役であり続けているペダルです。トーン回路がない不便さは確かにありますが、その分だけ反応が直接的で、アンプ自体を歪ませているような開放感があります。

私がギターを始めた頃は、多くの憧れのギタリストがMXR Distortion+を使っていましたが、当時は
BOSSのペダルの4〜5倍の価格と高嶺の花でとても手が出ませんでした。今ではBOSSの技シリーズよりもリーズナブルとなり気軽に購入できるようになりました。

「古くさいペダル」だとスルーしていましたが、今なら当時のあの音を自分の手で再現できることに、価値を感じています。結局、人はティーンのころ聞いたあの音が最高なのだから。

[^mxr-dunlop]: MXRは1972年、Keith BarrとTerry Sherwoodが設立した独立ブランドでしたが、1987年、Jim Dunlopに買収されています。

[^saudade-score]: 高中正義『SAUDADE』バンド・スコア. シンコーミュージック, 1982年10月20日発行, ISBN4-401-15179-8。付録のインタビュー記事より引用。

## References

<!-- textlint-disable -->

{% references() %}

- 高中正義『SAUDADE』バンド・スコア. シンコーミュージック, 1982年10月20日発行, ISBN4-401-15179-8
- [MXR M104 Distortion+ 公式マニュアル(Dunlop, PDF)](https://www.jimdunlop.com/content/manuals/M104.pdf). "Organic, germanium-powered clipping"と明記。現行M104がゲルマニウムダイオードであることの一次資料
- [ElectroSmash](https://www.electrosmash.com/mxr-distortion-plus-analysis). "MXR Distortion + Circuit Analysis"
- [Wampler DIY](https://wamplerdiy.com/blogs/news/mxr-distortion-pedal-circuit-analysis). "MXR Distortion + pedal circuit analysis"
- [SmallAxeMusic.com](https://smallaxemusic.com/blogs/news/vintage-mxr-debate-script-versus-block-logo). "Vintage MXR Debate: Script versus Block logos"
- [Crave Guitars](https://www.craveguitars.co.uk/home/features/effects/feature-1975-mxr-distortion/). "Feature – 1975 MXR Distortion +"
- [ToneHome](https://www.tonehome.de/mxr-innovations/distortion/). "MXR Innovations Distortion+"。ヴィンテージ個体の解析でゲルマニウムダイオード使用を確認

{% end %}

<!-- textlint-enable -->
