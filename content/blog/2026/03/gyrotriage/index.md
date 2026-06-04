+++
title = "gyrotriage — DJIドローン映像のブレを診断し、Gyroflowのパラメータを自動推定するツール"
description = """\
Gyroflowのパラメータ調整に毎回悩んでいませんか。\
gyrotriageはDJIドローンのMP4ファイルからブレを診断し、\
DaVinci ResolveのGyroflow OpenFXプラグインに入力するパラメータを自動で推定するCLIツールです。\
導入方法から使い方、出力の読み方までを解説します。\
"""
date = 2026-03-07T22:00:00+09:00
updated = 2026-06-04
[taxonomies]
tags = ["Drone", "Software"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="gyrotriage HUD出力例") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

<!-- more -->

> **（2026-06-04更新）** 本記事は当初、Gyroflowスタンドアロンアプリ向けの5つのパラメータを推奨する内容でした。その後、実運用のワークフローがDaVinci Resolve上のGyroflow OpenFXプラグインで完結することを踏まえ、推奨対象をプラグイン版「Adjust parameters」に一本化しました。以下では旧スタンドアロンアプリ版の記述に取り消し線を引き、新しい内容を併記しています。

## Gyroflowのパラメータ調整は面倒である

DJI NeoやAvataシリーズでFPV撮影をしている方なら、Gyroflowでの後処理は日常的な作業だと思います。EISをオフにして撮影し、Gyroflowでスタビライズする。この流れ自体は確立されていますが、問題はGyroflowのパラメータ調整です。

~~Gyroflowには主に5つの調整パラメータがあります。~~

DaVinci ResolveなどでGyroflow OpenFXプラグインを使う場合、調整の中心になるのは「Adjust parameters」パネルのSmoothnessとZoom limitです。スタンドアロンアプリ版にあった細かなパラメータはプラグインのUIには現れず、`.gyroflow` プロジェクト側に焼き込まれます（2026-06-04更新）。

| パラメータ                              | 意味                                                                          |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| Smoothness (1〜300)                     | スムージングの強度。高いほどブレを強く除去するが、意図した動きも鈍る          |
| ~~Max smoothness (s)~~                  | ~~突発的なブレに対する最大補正量~~（プラグイン版では非対応）                  |
| ~~Max smoothness at high velocity (s)~~ | ~~高速旋回時の補正上限。短くすると旋回への追従性が上がる~~（プラグイン版では非対応） |
| Zoom limit (%)                          | 安定化で生じる黒縁を隠すためのズーム上限                                      |
| ~~Zooming speed (s)~~                   | ~~Dynamic zoomingのFOV遷移速度~~（プラグイン版では非対応）                    |
| FOV                                     | 画角。算出対象外でベースライン1.0を提示                                       |

プラグインのSmoothnessは1〜300のスケール（デフォルト50）で、gyrotriageが従来出力していた百分率の値をそのまま入力できます。強く設定すればブレは消えますが、意図したカメラワークまで平滑化されたり、クロップで解像度が落ちたりします。適切な値はクリップごとに異なるため、毎回プレビューを見ながら試行錯誤することになります。

1本2本ならまだしも、フライト後に何十本ものクリップを処理するときは正直つらい作業です。

## gyrotriageでパラメータ推定を自動化する

<!-- textlint-disable -->

{{ linkcard(url="https://github.com/yostos/gyrotriage") }}

<!-- textlint-enable -->

そこで作ったのが **gyrotriage** です。DJIドローンのMP4ファイルを渡すだけで、埋め込まれたモーションデータを解析し、ブレの度合いをスコアリングしつつ、~~Gyroflowの5つのパラメータ~~Gyroflow OpenFXプラグイン（DaVinci Resolve等）に入力するパラメータを自動で推定します。

考え方はシンプルです。パイロットが意図したカメラワーク（パン・チルト・旋回）と除去したいブレ（風や機体振動）では、動きの周波数帯域が異なります。ゆっくりしたパンは1Hz以下の低周波、プロペラ振動は20Hz以上の高周波に現れます。この境界を信号処理で自動検出し、Gyroflowの内部ロジックに合わせてパラメータに変換しています。

## インストール

macOSの場合はHomebrewでインストールできます。

```bash
brew install gyrotriage
```

Rustの開発環境がある場合はcargoからもインストールできます。

```bash
cargo install --path .
```

## 使い方

基本的な使い方はMP4ファイルを渡すだけです。

```bash
gyrotriage DJI_0001.MP4
```

以下のようなテキスト出力が得られます。

```
File:        DJI_20260228080801_0003_D.MP4
Duration:    30.3s (60593 samples @ 2000Hz)
Score:       100 / 100
Level:       SEVERE
RMS:         34.8 °/s
Peak:        644.0 °/s
Pitch:       avg=1.4°/s  std=2.2°/s  max=47.9°/s
Roll:        avg=11.7°/s  std=13.5°/s  max=251.1°/s
Yaw:         avg=3.3°/s  std=4.4°/s  max=89.0°/s
---
Gyroflow plugin (Adjust parameters):
  Smoothness:           21
  Zoom limit:           118
  FOV:                  1.000
  Integration method:   None
  Lens correction:      100
```

末尾の「Gyroflow plugin (Adjust parameters)」ブロックが、Gyroflow OpenFXプラグインの「Adjust parameters」パネルにそのまま入力できる推奨値です。~~最後の2行がGyroflowに入力する推定パラメータです。~~ このうちSmoothnessとZoom limitはモーション解析から算出した値、Integration methodとLens correctionはDJI機の特性に基づく固定推奨です。この値をプラグインのパネルに入力すれば、そこから微調整を始められます（2026-06-04更新）。

なお旧スタンドアロンアプリ版では、末尾の出力が ~~`Gyroflow: smoothness=21% max=0.300s max@hv=0.030s zoom_limit=118% zooming_speed=2.6s`~~ という5値の形式でした。

## HUD表示で直感的にブレを把握する

`--visual` オプションを付けると、ブレの特性をHUD風のグラフィックで表示します。

```bash
gyrotriage DJI_0001.MP4 --visual
```

冒頭のカバー画像がHUD出力の実例です。画面には以下の情報が表示されます。

- **スコアゲージ**: ブレの重大度を0〜100で表示（STABLE / MILD / MODERATE / SEVEREの4段階）
- **レーダーチャート**: Pitch・Roll・Yawの3軸でブレの偏りを可視化
- **ライングラフ**: 合成角速度と各軸の角速度の時系列変化
- **推定パラメータ**: ~~Gyroflowに入力する5つの値~~Gyroflow OpenFXプラグインに入力する推奨値

数値だけでは分かりにくい「このクリップはRoll方向のブレが支配的」「後半に激しいブレが集中している」といった特性が一目で把握できます。Gyroflowプラグインを適用する前に、どのクリップにどの程度の処理が必要かをトリアージするのに役立ちます。

HUD画像はPNGファイルとしても出力できます。

```bash
gyrotriage DJI_0001.MP4 --output-image shake.png
```

WezTermやiTerm2などSixel/iTerm2プロトコルに対応したターミナルでは `--visual` でインライン表示されます。非対応のターミナルでは `--output-image` でファイル出力してください。

テキストのみの環境向けには `--sparkline` オプションもあります。

```bash
gyrotriage DJI_0001.MP4 --sparkline
```

## スコアの読み方

gyrotriageはブレの重大度を0〜100のスコアで表示します。

| レベル   | スコア  | 目安                             |
| -------- | ------- | -------------------------------- |
| STABLE   | 0〜25   | ブレはほぼなし。スタビライズ不要 |
| MILD     | 26〜50  | 軽微なブレ。スタビライズは任意   |
| MODERATE | 51〜75  | 目に見えるブレ。Gyroflow推奨     |
| SEVERE   | 76〜100 | 激しいブレ。Gyroflow必須         |

DJI Air 3Sのような3軸ジンバル搭載機ではほぼSTABLEになりますが、DJI Neoのような1軸ジンバル機やAvataシリーズでアクロバティックな飛行をした場合はMODERATE〜SEVEREになることが多いです。

## 推定パラメータの使い方

~~出力された5つのパラメータはGyroflowのUIに直接入力できます。~~出力された推奨値はGyroflow OpenFXプラグインの「Adjust parameters」パネルに直接入力できます（2026-06-04更新）。

1. ~~Gyroflowでクリップを開く~~DaVinci ResolveのタイムラインでクリップにGyroflowプラグインを適用する
2. 出力された値をそれぞれのスライダーに入力する
3. プレビューで確認し、必要に応じて微調整する

このとき、Integration methodはNone、Lens correctionは100、FOVは1.0を起点にします。DJI機はクォータニオンを記録済みなので再積分が不要で、正しいレンズプロファイルを読み込めばフル補正で問題ないためです。

推定値はあくまで調整の出発点です。ブレが残っている場合はSmoothnessを上げる、カメラワークが鈍く感じる場合はSmoothnessを下げる、といった微調整で仕上げてください。ゼロからスライダーを動かして探るよりも、妥当な出発点があるだけで調整時間は大幅に短縮できます。

## 対応機体と撮影条件

モーションデータがMP4へ埋め込まれるDJI機種に対応しています。ただし撮影時の設定次第ではモーションデータが記録されないため、注意が必要です。

| 機体                | 条件                                 |
| ------------------- | ------------------------------------ |
| DJI Avata / Avata 2 | EIS（Rocksteady）オフ、FOV Wide      |
| DJI Neo / Neo2      | アスペクト比4:3（EISは自動的にオフ） |

Avataシリーズの場合、Rocksteadyをオンにしているとモーションデータが記録されません。Gyroflowで後処理する前提なら、撮影時はRocksteadyオフ・FOV Wideで撮影してください。

DJI Neoの場合、16:9で撮影するとモーションデータが記録されません。4:3で撮影する必要があります。

DJI Air 3Sなど3軸ジンバル搭載機はGyroflow自体を必要としないケースが多く、対象外としています。

## 実際の効果

gyrotriageで推定したパラメータを微調整なしでそのままGyroflow OpenFXプラグインに適用した映像（右）と、オリジナルの未処理映像（左）の比較です。

<!-- textlint-disable -->

{{ youtube(id="uEInUgQIBrs") }}

<!-- textlint-enable -->

## 注意事項

- 推定値は信号処理に基づく客観的な算出であり、映像の主観的な品質評価は含まない
- 非常にゆっくりしたブレ（0.3Hz未満）は意図した動きと区別できない
- GyroflowのDefaultアルゴリズムを前提としており、Plain 3Dや軸別モードでは推定値の解釈が異なる
- 極端に短いクリップ（2秒未満）では推定精度が低下する
- 商用空撮など業務用途では、必ずGyroflowのプレビューで結果を検証すること

<!-- textlint-disable -->

{% references() %}

- [Gyroflow](https://gyroflow.xyz/). 「Gyroflow - Video stabilization using gyroscope data」

{% end %}

<!-- textlint-enable -->
