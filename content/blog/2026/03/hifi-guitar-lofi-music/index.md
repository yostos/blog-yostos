+++
title = "ギターはHiFi化し、音楽はLoFi化している — Billboard Hot 100の音響分析で検証する"
description = """
近年ギターはアンプシミュレーターの普及でHiFi化する一方、
ヒット曲はLoFi化しているという説をデータで検証しました。
Billboard Hot 100のトップ5曲（2000〜2024年）を音響分析した結果、
スペクトル指標が一貫して低下し、音楽のLoFi化は事実であることがわかりました。
"""
date = 2026-03-04

[taxonomies]
tags = ["Creative", "Guitar"]

[extra]
social_media_card = "ogp.webp"
local_image = "/blog/2026/03/hifi-guitar-lofi-music/cover.webp"
tldr = "Billboard Hot 100トップ5曲（2000〜2024年、計125曲）をlibrosaで音響分析した結果、スペクトル重心・ロールオフ・帯域幅・ゼロ交差率のすべてが一貫して低下しており、ヒット曲のLoFi化は数値で裏付けられました。"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover画像") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

## ギターのHiFi化と音楽のLoFi化

ギタリストの間でよく聞く話があります。近年、真空管アンプとギターキャビネットの組み合わせに代わってアンプシミュレーターが急速に普及しました。従来のギターアンプはスピーカーの周波数特性によって5kHz付近から高域が自然にロールオフし、いわゆる「ギターらしい音」が作られていました。アンプシミュレーターもIR（インパルスレスポンス）でキャビネットの特性を忠実に再現できますが、IRの選択やEQの自由度は従来のアンプとは比較にならないほど高く、FRFRスピーカーやDAWへのライン出力など、従来のギタースピーカーの制約を受けない再生環境も広がっています。結果として、ギターの音はかつてないほどHiFi化しているというのです。

PolyphiaのTim Hensonはその象徴的な存在です。Neural DSPのプラグインを駆使した彼のトーンは、従来のギタースピーカーでは再現できないほどクリアで広帯域な音色を持っています。

一方で、音楽全体を見るとLoFi Hip HopやチルウェイブなどLoFiを志向するジャンルが台頭し、ヒット曲の音作りもウォームで暗い方向に向かっているといわれます。

ギターはHiFi化し、音楽はLoFi化している。これは本当なのでしょうか。「なんとなくそう感じる」ではなく、データで検証してみたくなりました。

## 分析手法

当初は日本のヒットチャートでも同様の分析を試みましたが、オリコンやBillboard Japanの年間チャートは握手会チケットとしてCDを売りさばくアイドルの大量ランクインに支配されており、音楽的なトレンドを反映したデータとしては使い物になりませんでした。そこで対象を米国のBillboard Hot 100に絞っています。

Billboard Year-End Hot 100のトップ5曲を2000年から2024年まで、計125曲を対象としました。各楽曲の音源を取得し、Pythonの音響分析ライブラリlibrosaで以下の6つの音響特徴量を抽出しました。

- **RMS Loudness (dB)**: 音圧（音量感）
- **Spectral Centroid (Hz)**: スペクトル重心（音の明るさ）
- **Spectral Rolloff (Hz)**: エネルギーの85%が集中する周波数上限
- **Spectral Bandwidth (Hz)**: スペクトルの広がり
- **Tempo (BPM)**: テンポ
- **Zero Crossing Rate**: ゼロ交差率（テクスチャのノイジーさ）

このうち、Spectral Centroid、Spectral Rolloff、Spectral Bandwidth、Zero Crossing Rateの4指標がLoFi化の指標として機能します。値が低いほど高周波成分が少なく、ウォームで暗い音色、つまりLoFi的な音になります。

分析に使用したコードは[GitHub](https://github.com/yostos/music-trend-analysis)で公開しています。

<!-- textlint-disable -->

{{ linkcard(url="https://github.com/yostos/music-trend-analysis")}}

<!-- textlint-enable -->

## RMS Loudness — 音圧は上がり続ける

<!-- textlint-disable -->

{{ image(src="rms_db.webp", alt="RMS Loudness (dB) の推移") }}

<!-- textlint-enable -->

<figure style="float: right; margin: 0 0 1rem 1.5rem;">
<table>
<thead><tr><th>期間</th><th>平均RMS (dB)</th></tr></thead>
<tbody>
<tr><td>2000-2004</td><td>-16.71</td></tr>
<tr><td>2005-2009</td><td>-15.46</td></tr>
<tr><td>2010-2014</td><td>-16.25</td></tr>
<tr><td>2015-2019</td><td>-13.89</td></tr>
<tr><td>2020-2024</td><td>-13.29</td></tr>
</tbody>
</table>
</figure>

年との相関はr=0.319（正の相関）で、年が進むほど音圧が上昇しています。いわゆる「ラウドネス・ウォー」（音圧競争）の傾向が数値で裏付けられました。

2000年代前半は-16〜-17dBだった平均音圧が、2020年代には-13dB付近まで上昇しています。Spotifyのラウドネスノーマライゼーション（-14 LUFS）が導入されてもなお、マスタリング段階で音圧を上げる傾向は続いています。

2010-2014年に一度平均が下がっているのが興味深い点です。Adeleの"Rolling in the Deep"(-20.71dB)やGotyeの"Somebody That I Used to Know"(-25.77dB)など、ダイナミクスを活かした楽曲がヒットした時期と一致します。

<div style="clear: both;"></div>

## Spectral Centroid — 音の「明るさ」は低下

<!-- textlint-disable -->

{{ image(src="spectral_centroid.webp", alt="Spectral Centroid (Hz) の推移") }}

<!-- textlint-enable -->

<figure style="float: right; margin: 0 0 1rem 1.5rem;">
<table>
<thead><tr><th>期間</th><th>平均 (Hz)</th></tr></thead>
<tbody>
<tr><td>2000-2004</td><td>3,095</td></tr>
<tr><td>2005-2009</td><td>3,160</td></tr>
<tr><td>2010-2014</td><td>3,038</td></tr>
<tr><td>2015-2019</td><td>2,661</td></tr>
<tr><td>2020-2024</td><td>2,611</td></tr>
</tbody>
</table>
</figure>

スペクトル重心は周波数スペクトルの「重心」で、音の「明るさ」に対応します。値が高いほど高周波成分が多くキラキラした音（HiFi寄り）、低いほど暗く丸い音（LoFi寄り）です。

年との相関はr=-0.327（負の相関）で、2000年代の3,000〜3,200Hz付近から2020年代には2,600Hz付近まで低下しました。ヒット曲の音色が確実に「暗く」「丸く」なっています。

<div style="clear: both;"></div>

## Spectral Rolloff — エネルギーの分布が低域にシフト

<!-- textlint-disable -->

{{ image(src="spectral_rolloff.webp", alt="Spectral Rolloff (Hz) の推移") }}

<!-- textlint-enable -->

<figure style="float: right; margin: 0 0 1rem 1.5rem;">
<table>
<thead><tr><th>期間</th><th>平均 (Hz)</th></tr></thead>
<tbody>
<tr><td>2000-2004</td><td>6,492</td></tr>
<tr><td>2005-2009</td><td>6,662</td></tr>
<tr><td>2010-2014</td><td>6,387</td></tr>
<tr><td>2015-2019</td><td>5,541</td></tr>
<tr><td>2020-2024</td><td>5,475</td></tr>
</tbody>
</table>
</figure>

全エネルギーの85%が集中する周波数の上限を示す指標です。年との相関はr=-0.319（負の相関）で、2000年代の6,500Hz前後から2020年代には5,500Hz前後に低下しました。楽曲のエネルギーが高周波帯から低〜中周波帯にシフトしていることがわかります。

<div style="clear: both;"></div>

## Spectral Bandwidth — 帯域幅は縮小

<!-- textlint-disable -->

{{ image(src="spectral_bandwidth.webp", alt="Spectral Bandwidth (Hz) の推移") }}

<!-- textlint-enable -->

<figure style="float: right; margin: 0 0 1rem 1.5rem;">
<table>
<thead><tr><th>期間</th><th>平均 (Hz)</th></tr></thead>
<tbody>
<tr><td>2000-2004</td><td>3,540</td></tr>
<tr><td>2005-2009</td><td>3,621</td></tr>
<tr><td>2010-2014</td><td>3,517</td></tr>
<tr><td>2015-2019</td><td>3,201</td></tr>
<tr><td>2020-2024</td><td>3,203</td></tr>
</tbody>
</table>
</figure>

スペクトルの「広がり」を示す指標で、年との相関はr=-0.316（負の相関）です。2000年代の3,500〜3,600Hzから2020年代の3,200Hzへ約10%縮小しました。

近年のヒット曲はボーカル、808ベース、シンプルなシンセパッドなど少数の要素で構成されることが多く、バンドサウンドのように広帯域を埋め尽くすプロダクションが減ったことと整合します。音作りが「フルバンド」から「焦点を絞った」方向へ変化しているのです。

<div style="clear: both;"></div>

## Tempo — 明確な傾向は見られない

<!-- textlint-disable -->

{{ image(src="tempo.webp", alt="Tempo (BPM) の推移") }}

<!-- textlint-enable -->

<figure style="float: right; margin: 0 0 1rem 1.5rem;">
<table>
<thead><tr><th>期間</th><th>平均 (BPM)</th></tr></thead>
<tbody>
<tr><td>2000-2004</td><td>106.7</td></tr>
<tr><td>2005-2009</td><td>126.9</td></tr>
<tr><td>2010-2014</td><td>121.5</td></tr>
<tr><td>2015-2019</td><td>130.3</td></tr>
<tr><td>2020-2024</td><td>123.2</td></tr>
</tbody>
</table>
</figure>

テンポは年との相関がr=0.193と弱く、他の指標ほど明確な傾向は見られません。年ごとのばらつきが大きく、LoFi化とは独立した指標といえます。なお、librosaのビートトラッキングには倍テンポ・半テンポの誤検出が起こりうる点には留意が必要です。

<div style="clear: both;"></div>

## Zero Crossing Rate — 最も強い相関を示した指標

<!-- textlint-disable -->

{{ image(src="zero_crossing_rate.webp", alt="Zero Crossing Rate の推移") }}

<!-- textlint-enable -->

<figure style="float: right; margin: 0 0 1rem 1.5rem;">
<table>
<thead><tr><th>期間</th><th>平均</th></tr></thead>
<tbody>
<tr><td>2000-2004</td><td>0.06102</td></tr>
<tr><td>2005-2009</td><td>0.05974</td></tr>
<tr><td>2010-2014</td><td>0.05657</td></tr>
<tr><td>2015-2019</td><td>0.04951</td></tr>
<tr><td>2020-2024</td><td>0.04761</td></tr>
</tbody>
</table>
</figure>

ゼロ交差率は信号がゼロを横切る頻度で、高周波成分やノイズの多さを反映します。年との相関はr=-0.343で、今回の分析で最も強い相関を示しました。

2000年代前半の0.061から2020年代の0.048へ、約22%低下しています。シンバル、ハイハット、ギターのディストーションといった高域成分が減り、クリーンなボーカル、サブベース、ソフトなシンセパッドが主体のプロダクションへ移行していることを如実に示しています。

Post Maloneの"Rockstar"(0.0262)が最小値であることは象徴的です。トラップの特徴である808ベースとオートチューンボーカルの組み合わせが、いかにスムーズなテクスチャを生むかがわかります。

<div style="clear: both;"></div>

## ジャンルの変遷と音響特性の対応

| 時期      | 主流ジャンル          | 音響的特徴                         |
| --------- | --------------------- | ---------------------------------- |
| 2000-2004 | Pop, R&B, Rock        | 広帯域、中程度の音圧               |
| 2005-2009 | Pop, Hip-Hop, EDM前夜 | 帯域やや広、テンポ上昇             |
| 2010-2014 | EDM Pop, Indie Pop    | ばらつき大、ダイナミクスのある曲も |
| 2015-2019 | Hip-Hop/Trap, Pop     | 帯域縮小、音圧上昇、ダーク化       |
| 2020-2024 | Hip-Hop, Pop, Country | 低域集中、高音圧、スムーズ         |

スペクトル指標の変化はジャンルの変遷とよく対応しています。ロックバンドやポップのシンセサウンドが支配的だった2000年代から、ベースとキックを中心としたヒップホップ/トラップのプロダクションが主流になった変化が、数値にそのまま表れています。

## 考察：LoFi化の背景

分析結果をまとめると、スペクトル系の3指標（Centroid、Rolloff、Bandwidth）とゼロ交差率がすべて負の相関を示しており、米国のヒット曲は25年間で「HiFi」から「LoFi」方向へ明確にシフトしたといえます。

ここでいうLoFiは「音質の劣化」ではありません。808ベースとオートチューンボーカルで構成されるトラップは、制作環境としては極めてHiFiです。しかし結果として出力される楽曲のスペクトル特性は、高周波成分を抑えたウォームでダークな方向に向かっています。これがプロデューサーの意図的な音色設計なのか、ヒップホップやトラップというジャンル固有の音響特性が結果的にそうなったのかは、この分析だけでは区別できません。ただ、ジャンルの変遷そのものが時代の嗜好を反映しているのは確かです。

冒頭の問いに戻ると、「ギターはHiFi化し、音楽はLoFi化している」という仮説のうち、少なくとも後半はデータで裏付けられました。ギターがアンプシミュレーターで広い周波数帯域を手に入れた一方で、音楽全体はむしろ帯域を絞る方向に進んでいるのは、なかなか皮肉な状況です。

<!-- textlint-disable -->

{% admonition(type="warning", title="分析の限界") %}

今回の分析にはいくつかの制約があります。

- 各年5曲というサンプルサイズは統計的に小さく、個別の曲の影響を受けやすい。トップ5には特定のジャンルが偏る可能性がある
- 音源の取得元や圧縮形式によっては高域が劣化している可能性があり、特に古い楽曲ほどソースの品質にばらつきがある
- librosaのビートトラッキングによるテンポ推定は、特にヒップホップやトラップでハーフタイム/ダブルタイムの誤判定が起こりやすい
- RMSはLUFSとは異なる指標であり、厳密なラウドネス比較には向かない

{% end %}

<!-- textlint-enable -->

より精度の高い分析には、サンプル数の拡大やオフィシャル音源の使用が望ましいでしょう。とはいえ、125曲のデータで一貫した傾向が出ている点は注目に値します。

<!-- textlint-disable -->

{% references() %}

- [GitHub](https://github.com/yostos/music-trend-analysis). 「music-trend-analysis — 分析コード」
- [librosa](https://librosa.org/). "librosa: Audio and Music Signal Analysis in Python"
- [Billboard](https://www.billboard.com/). "Year-End Hot 100 Songs"

{% end %}

<!-- textlint-enable -->
