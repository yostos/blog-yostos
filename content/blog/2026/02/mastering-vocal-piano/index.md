+++
title = "Process.audio Decibelに乗り換えた — Spotifyターゲットの測定と調整"
description = """
iZotopeのサブスクリプション値上げを機に、
Process.audio Decibelへ乗り換えました。
Spotifyプリセットのターゲット
（LUFS-I、True Peak、LRA）の意味と、
メーターの読み方、測定結果から
リミッターをどう調整するかを
実際のセッションで解説します。
"""
date = 2026-02-23
[taxonomies]
tags = ["Music", "Music Production"]
[extra]
social_media_card = "ogp.webp"
+++

<!-- textlint-disable -->

{{ image(src="./cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

## はじめに

先日Waves L4 Ultramaximizerを導入して、
マスタリングのツールチェインが
揃ってきたところでした。
そこにiZotopeからサブスクリプション変更の
メールが届きました。
Music Production Suite Proが
iZotope Proへ移行し、据え置き期間の後は
月額25ドル（年額250ドル）になるという内容です。

iZotope Insight 2は優れたメーターですが、
サブスクリプションに依存している点は
以前から気になっていました。
これを機にProcess.audio Decibelへ
乗り換えることにしました。

今回は女性ボーカルとピアノだけの
シンプルな構成の楽曲で、
実際にDecibelを使ってマスタリングしています。
ピアノはRavel、ヴォーカルはSynthesizer Vです。
プラグインはUADxを中心に、最終段のリミッターには
L4 Ultramaximizerを使っています。

<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/soundcloud%253Atracks%253A2271481283&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe><div style="font-size: 10px; color: #cccccc;line-break: anywhere;word-break: normal;overflow: hidden;white-space: nowrap;text-overflow: ellipsis; font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;font-weight: 100;"><a href="https://soundcloud.com/yostos" title="Yostos" target="_blank" style="color: #cccccc; text-decoration: none;">Yostos</a> · <a href="https://soundcloud.com/yostos/homura" title="Homura" target="_blank" style="color: #cccccc; text-decoration: none;">Homura</a></div>

## シグナルチェイン

ボーカルはPultec EQで周波数を整えてから
1176 Rev Aで軽くコンプレッションをかけ、
Pure Plate Reverbを薄めにセンドしています。
ピアノは左手と右手を別トラックにして、
客席目線でR30/L30にパンニングしました。
右手はEQP-1Aで高域に空気感を足し、
左手はHLF-3Cで高域をカットして棲み分けを
作っています。
コンプレッションは両方ともLA-2Aで、
ピアノのダイナミクスを壊さない穏やかな設定です。
リバーブはボーカルのプレートとは別に、
Lexicon 224のホールを使って空間を分けています。

マスターバスはPultec MEQ-5で中域を微調整し、
SSL G Bus Compressorで軽くグルーをかけてから、
Ampex ATR-102でテープサチュレーションを
加えています。
最終段のリミッターにはL4 Ultramaximizerを
Ceiling -1.1dB、Threshold -1.5dBで使い、
True PeakモードをON、Oversamplingは16xに
しています。
Ceilingを-1.0dBではなく-1.1dBにしたのは、
DecibelのTrue Peak測定が厳格で
-1.0dBだとギリギリ超えることがあったためです。
ピアノはダイナミックピークが大きい楽器なので、
無理にリミッティングで潰さず
ダイナミクスを活かすことを優先しました。

## Decibelによるメータリング

Decibelはストリーミングプラットフォームごとの
プリセットを持つメータリングプラグインです。
今回はSpotifyプリセットを使いました。

<!-- textlint-disable -->

{{ image(src="decibel-spotify-preset.png", alt="Decibel Spotifyプリセット") }}

<!-- textlint-enable -->

Spotifyプリセットでは
次の3つのターゲットが設定されています。

- **LUFS-I Target: -14.0** —
  楽曲全体の平均ラウドネス。
  LUFSはITU-R BS.1770に基づく
  ラウドネスの国際規格で、
  Integratedは楽曲を通して再生したときの
  平均を指す。
  Spotifyはこの値を基準に
  ノーマライゼーションを行うため、
  -14 LUFSより大きい音源は再生時に
  音量が下げられ、
  小さい音源は上げられる。
- **True Peak Max: -1.0 dBTP** —
  サンプル間ピークの上限。
  デジタル信号をアナログに変換する際、
  サンプル値そのものではなく
  DAC再構成後の波形にピークが現れる。
  -1.0 dBTPのマージンは
  OggやAACへのコーデック変換で
  クリッピングが発生しないための
  安全域である。
- **LRA Max: 10.0** —
  Loudness Range（ラウドネスレンジ）の
  上限。
  楽曲内の静かな部分と大きな部分の差を
  統計的に測定した値で、
  プレイリスト再生で前後の曲と
  音量差が開きすぎないよう
  上限は10 LUとされている。

これらのターゲットに対する達成状況を、
Decibelは複数のメーターで同時に表示します。
次のスクリーンショットは
L4 Ultramaximizerを外した状態で
楽曲全体を再生した結果です。

<!-- textlint-disable -->

{{ image(src="decibel-full-view.webp", alt="Decibel全体表示（L4なし）") }}

<!-- textlint-enable -->

左のSuper MeterにはIntegrated LUFS、
TRUEDYN、TRUEPEAK MAXが
まとめて表示されています。
中央のTarget Validatorでは
LUFS-Iが青字でPASS、
TRUE PEAKが赤字でFAILです。
右側のLUFS Meterは
Momentary（400ミリ秒）、
Short-term（3秒）、
Integrated（全体平均）の
3種類のラウドネスを棒グラフで表示し、
青い破線がターゲットラインです。
下部のLUFS Histogramでは
時系列のラウドネス推移を確認でき、
ピンクのマーカーが
True Peak超過の箇所を示しています。

この結果を見て何をするかが重要です。
ミックスの段階でLUFS-Iは
すでにターゲットに達している一方、
True Peakが-0.9 dBTPと
わずかに基準を超えています。
それぞれのターゲットに対する
アクションは次の通りです。

- **True Peak FAIL** →
  L4のCeilingで制御する。
  Ceilingはリミッターの出力上限なので、
  -1.0 dBTP以下に設定すれば
  True Peakはそこで止まる。
  今回は-1.1dBに設定した。
  DecibelのTrue Peak測定が厳格で
  -1.0dBだとわずかに超えることがあったためである。
- **LUFS-Iが低すぎる場合** →
  L4のThresholdを下げる。
  Thresholdを下げるとリミッターが
  より多くのピークを抑えるため、
  相対的に平均ラウドネスが上がる。
  今回はミックスの時点で-14.0 LUFSに
  達していたので、
  Thresholdは-1.5dBと浅い設定で済んでいる。
- **LRAが大きすぎる場合** →
  バスコンプレッサーやリミッターで
  ダイナミクスの幅を狭める。
  今回のTRUEDYNは11.5 dBで
  LRA Max 10.0を超えているが、
  ピアノのダイナミクスを優先して許容した。

同じネットワークにいるiPadやiPhone、
Androidデバイスにメーター画面を
リアルタイム表示できるのも便利です。
Decibel Displayという無料アプリを入れて
IPアドレスを指定するだけで、
手元のタブレットが
メーターディスプレイになります。

L4を適用した最終測定値は次の通りです。

- Integrated LUFS: -14.0
- True Peak MAX: -1.0 dBTP
- TRUEDYN: 11.5 dB

すべてのターゲットを満たしています。

Logic Proからのバウンスは24bit AIFFで行い、
L4のDither設定も24bitに合わせています。
32bit floatでバウンスすると
L4のディザリングが無意味になるので、
ビット深度を揃えることが重要です。
FLAC変換には`ffmpeg -c:a flac`だけで
変換しています。

## まとめ

Process.audio Decibelの導入で、
L4 Ultramaximizerと合わせて
マスタリングのツールチェインが整ってきました。
ラウドネスメーターとリミッターが揃ったことで、
「測定→調整→確認」のワークフローが
スムーズに回っています。

女性ボーカルとピアノという
シンプルな編成だからこそ、
ダイナミクスの扱い方や周波数の棲み分けが
そのまま音に出ます。
リミッターで潰すのではなく、
演奏のニュアンスを活かす方向で
マスタリングできたのは良かったと思います。

## 参考リンク

- [Process.audio Decibel](https://process.audio/en/products/decibel)
- [Waves L4 Ultramaximizer](https://www.waves.com/plugins/l4-ultramaximizer)
- [Universal Audio](https://www.uaudio.com/)
