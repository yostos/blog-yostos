+++
title = "Xotic Soul Driven - TS系とBD-2のハイブリッド"
description = """
TS系のPPSE Classicでは出しづらい、エッジの効いたゲイン高めの音が欲しくてXotic Soul Drivenを購入しました。回路をトレースすると前段はTS系、後段はBOSS BD-2 Blues Driverを流用した構成で、実際に弾き比べてもPPSE Classicとは違うキャラクターを持つ歪みでした。回路の構造と実際の音の特徴を整理します。
"""
date = 2026-07-03T13:25:59+09:00
[taxonomies]
tags = ["Creative", "Guitar"]
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

オーバードライブとしてTS系のPPSE Classicをずっと愛用していますが、もう少しエッジの効いたゲイン高めの音が欲しくなり、Xotic Soul Drivenを購入しました。

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/g00u8zu5.9srin566.g00u8zu5.9srio8a9/kaereba_main_202607031346328136?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fikeshibu%2F512426%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fikeshibu%2Fi%2F10022261%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/ikeshibu/cabinet/426/512426-01.jpg?_ex=128x128" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/g00u8zu5.9srin566.g00u8zu5.9srio8a9/kaereba_main_202607031346328136?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fikeshibu%2F512426%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fikeshibu%2Fi%2F10022261%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >Xotic Soul Driven</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_202607031346328136?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2FSOul%2520Driven%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt&m=http%3A%2F%2Fm.rakuten.co.jp%2F" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=SOul%20Driven&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>

## Soul Driven を購入した訳

現在エフェクターボードには、ディストーションにはBOSS DS-1W、ファズやコンソール的な飽和感が必要な場合はBroadcast AP-II、オーバードライブには
Vin-Antique PPSE Classicを使用しています。

Vin-Antique PPSE Classicは、TS本家同様の対称クリッピングをベースに、ハイが詰まらずクラシカルな質感を持つオーバードライブです。
ただPPSE ClassicはGainを上げてもTS系らしい上品さの範囲に留まり、もう少しエッジの効いた、ゲインに余裕のある音を求める場面がありました。
少しエッジの効いた歪みとして目をつけたのがXotic Soul Drivenでした。

## Soul Driven とは

Xotic Soul Drivenは2016年に発売されたオーバードライブ/ブーストペダルです。ジャズ/フュージョン系ギタリストのAllen Hindsが数年にわたってXoticと共同開発したシグネチャーモデルで、当初は「AH」名義の限定モデル(青筐体、1500台)として登場し、完売後にレギュラーライン化されました(クロム筐体、中身は同一とされます)。

回路の実機トレースを公開しているAion FXの記事によれば、Soul Drivenは前段と後段で異なる2つの回路を組み合わせた構成になっています。

前段はTube Screamer系のクリッピング段です。オペアンプの帰還ループに1N914とBAT46のダイオードを直列に配置しており、TS808/TS9よりクリップの閾値が高めに設定されています。ここにTimmyのBassコントロールやZendriveのVoiceコントロールに近い可変ハイパスフィルターが組み合わされています。

後段はBOSS BD-2 Blues Driverの回路をほぼそのまま流用した構成です。Aion FXの記事では「ほぼ逐語的に流用」と明記されており、変更点は次の4点に留まります。

- Bass抵抗値: BD-2の固定6.8kΩに対し、内部DIPスイッチで18k/28k/33k/43kΩの4段階に可変
- 出力抵抗: BD-2の1kΩに対し470Ω(Aion FXいわく音への実質的な影響はほぼ無し)
- Toneポット: BD-2の10kBに対し250kB
- Volume段の配置: EQより前段という点はBD-2と同じ(ノイズ面で軽微な設計上の指摘あり)

Aion FXは別記事(SL Driveのトレース記事)で、Soul Drivenを「half Tube Screamer and half Blues Driver」と表現しています。前段はTS系、後段はBD-2という組み合わせは、的確な要約だと思います。

なお、BD-2はGainが2連ポットになっており、クリッピング前とクリッピング後の2つのブースト段を同じノブで同時に持ち上げる設計です。これによってGainを上げていくと歪みと音量感が急激に立ち上がる、BD-2特有の効き方が生まれます。ただしSoul Drivenの前段は単一オペアンプの帰還ループでゲインを作る一般的なTS型のクリッピング段で、BD-2のデュアルポット構成とは異なります。Soul DrivenのGainの効き方は、BD-2の「2段連動」ではなくTS系の単段クリッピングのゲインだと考えたほうが実態に近いはずです。

コントロールはGain、Tone、Volume、Mid Boost(ブースト量ではなく持ち上げる帯域を選ぶノブ)の4つに加え、内部DIPスイッチでBassブースト量を4段階(flat/+2.4dB/+3.6dB/+6dB @125Hz)に切り替えられます。

このトレースはAion FXによる実機分解の一次資料に基づくもので、DIYコミュニティでもレイアウトのエラーチェックが行われています。ただしこれは複数の独立した解析が一致したという意味ではなく、あるビルダーが作成したレイアウトを別のビルダーが実機と照合してエラーがないことを確認した、という程度の検証である点は留意しておきます。

## Soul Drivenの音の特徴

PPSE Classicとの比較では、Soul Drivenのほうが低域までしっかり出て一段攻撃的な音です。
同じくXoticのBB Preampと比べるとBB Preampが温かく優しい歪みなのに対しSoul Drivenはミッドが削れてローが強く、
ややドンシャリでアグレッシブな歪みです。

ただ、Gainを12時以降まで上げてもあまり変わらず、倍音とコンプ感がじわりと足されていく感覚です。
エッジが立っている割にナチュラルで上品な印象です。Mid Boostのつまみの調整でかなり音の印象が変わります。

こちらの方が自分の求めていた音のイメージに近いと感じました。

## まとめ

PPSE ClassicとSoul Drivenの前段は、ともにTS系のクリッピング回路という点で確かに近い系統です。ただSoul Drivenの後段にはBD-2由来のブースト段があり、これがゲインの余裕とローの量感、そしてミッドが削れてエッジが立つキャラクターを生んでいます。実際に弾き比べても、PPSE Classicでは出しづらかった「エッジの効いたゲイン高めの音」がしっかり出ており、狙い通りの選択だったと言えそうです。

ボードのDrive枠はPPSE ClassicかSoul Drivenかを排他選択する構成になっているので、曲や場面に応じて使い分けていくつもりです。

## References

{% references() %}

- [Aion FX](https://aionfx.com/news/tracing-journal-xotic-soul-driven-boost-overdrive/).「Tracing Journal: Xotic Soul Driven — Boost/Overdrive」実機トレース記事
- [Aion FX](https://aionfx.com/news/tracing-journal-xotic-sl-drive/).「Tracing Journal: Xotic SL Drive」Soul Drivenの回路構成についての言及

{% end %}
