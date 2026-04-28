+++
title = "DJI Avata 2 シネマティック設定ガイド"
description = """DJI Avata 2でシネマティックな映像を撮るためのカメラ設定とPost Productionの手順をまとめました。\
露出、ホワイトバランス、D-Log M、Gyroflow、SkyGrades LUTまで、実際に使っている設定値を共有します。"""
date = 2026-04-27T16:30+09:00


[taxonomies]
tags = ["Drone"]

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

DJI Avata 2でシネマティックな映像を撮るために、自分が使っているカメラ設定とPost Productionの手順をまとめました。DJI Goggle 3とDJI FPV送信機3を使ったマニュアルモードでの飛行[^1]を前提とし、D-Log MとGyroflowを活用したワークフローです。

海外のAvata 2ユーザーのブログ記事やYouTubeから情報を集めて研究した設定で、現時点での最適解と考えています。

<!-- textlint-disable -->

{{ youtube(id="ogwig1EU4CQ") }}

<!-- textlint-enable -->

## 露出設定

撮影モードはマニュアルモードを使用し、ISOとシャッタースピードも手動で設定します。

ISOはできる限り低く抑えるのが基本で、ISO 100が理想的です。明暗差の大きいエリアを飛行する場合は、Auto ISOに切り替えると露出変化に対応しやすくなります。

シャッタースピードの設定は撮影スタイルによって異なります。いずれもNDフィルター使用時は「180度ルール」を適用し、シャッタースピードを撮影フレームレートの2倍の分母に設定します。

<!-- textlint-disable -->

{% admonition(type="info", title="180度ルールとは") %}
映画撮影で標準的に用いられるシャッター角度の慣習に由来します。フィルムカメラの回転シャッターが180度（半回転）開いている間に露光することから、露光時間がフレーム間隔の半分になります。デジタルカメラでは「シャッタースピード = 1 /（フレームレート × 2）」と換算します。このルールに従うと、人間の目に自然に見える適度なモーションブラーが得られ、映画的（シネマティック）な質感になります。シャッタースピードをこれより速くするとブラーが減りパラパラとした硬い映像に、遅くするとブラーが過剰になり不明瞭な映像になります。
{% end %}

<!-- textlint-enable -->

- **通常のシネマティック撮影**
  - 60FPS / シャッタースピード1/120秒 / NDフィルター使用
  - 60FPSで撮影するのはゴーグルのライブビューがカクつかないため
- **スローモーションを前提とした撮影**
  - 100FPS / シャッタースピード1/200秒 / NDフィルター使用 / 16:9（100FPSは16:9限定）
- **アグレッシブなフリースタイル撮影**
  - 60FPS / NDフィルターなし / 適正露出になるようシャッタースピードを上げて調整

ND濃度は撮影環境の明るさに応じて選びます。私は[K&F ConceptのND/PL複合フィルター（ND8/PL〜ND64/PL）](https://amzn.to/4mT7jZv)を使用しています[^2]。

<!-- textlint-disable -->

{% aside(position="right") %}
PL（偏光フィルター）は水面やガラスなどの反射を抑え、空を濃く・葉の緑を鮮やかに見せる効果がある。NDとの複合フィルターは光量減衰と偏光の両方を1枚で兼ねる。
{% end %}

<!-- textlint-enable -->

| 撮影環境             | 推奨ND  |
| -------------------- | ------- |
| 曇天・薄暮           | ND8/PL  |
| 標準的な屋外         | ND16/PL |
| 晴天                 | ND32/PL |
| 直射晴天・水面反射等 | ND64/PL |

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/g00txg35.9srin05b.g00txg35.9srio327/kaereba_main_202604281230333352?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fkentfaith%2Fsku-2295%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fkentfaith%2Fi%2F10001082%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/kentfaith/cabinet/top/imgrc0102392131.jpg?_ex=128x128" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/g00txg35.9srin05b.g00txg35.9srio327/kaereba_main_202604281230333352?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fkentfaith%2Fsku-2295%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fkentfaith%2Fi%2F10001082%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >限定10％OFFxP5倍!!　 DJI AVATA2 専用 フィルターセット(ND8/PL+ND16/PL+ND32/PL+ND64/PL) ND&amp;PLフィルター 1枚2役 保護フィルター 装着便利 減光量調整 AGC光学ガラス コントラスト強調 ナノコーティング 撥水防汚</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_202604281230333352?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2FKF%2520CONCEPT%2520DJI%2520AVATA2%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt&m=http%3A%2F%2Fm.rakuten.co.jp%2F" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=KF%20CONCEPT%20DJI%20AVATA2&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>

## ホワイトバランス

ホワイトバランスは手動で設定します。オートホワイトバランスは飛行中に色温度が変動し、Post Productionでの補正が困難になるため使用しません。撮影状況に応じた目安は以下のとおりです。

- 晴天：5600K（一般的な基準：5500〜6000K）
- 曇り：6300K以上（一般的な基準：6000〜7000K）
- 日の出・日の入り：5700K（一般的な光源の色温度は3000〜4500Kだが、ここではあえて高めに設定することで暖色を強調し、ゴールデンアワーの雰囲気を演出する意図）

D-Log Mで撮影する場合、ホワイトバランスはPost Productionのカラーグレーディングでも調整可能です。撮影時の設定に迷う場合は、ニュートラルに近い値で撮影しておき、Post Productionで追い込む方法もあります。

## 解像度とフレームレート

解像度は4Kを使用します。フレームレートは60FPSを推奨します（30FPSにするとゴーグルのライブ映像でカクつくことがあります）。スローモーション撮影には4K・100FPSを使用します（16:9限定）。

## カラープロファイル

撮影時に選べるカラープロファイルは、ノーマルカラーとD-Log Mの2種類です。どちらを選ぶかで、撮って出し寄りの運用にするか、Post Productionで追い込むかという方向性が決まります。

- ノーマルカラー：カメラからそのまま使える色合いが得られるが、ダイナミックレンジが狭く、カラーグレーディングの調整幅は限られる
- D-Log M：ダイナミックレンジが大幅に広がり、カラーグレーディングの自由度が高い。扱いやすく、きれいに仕上げやすい

シネマティックな仕上がりを目指す場合はD-Log Mを選択します。後述するSkyGrades LUTもD-Log M向けに設計されているため、このワークフローでは事実上D-Log Mが前提となります。

## 画角と手ぶれ補正

手ぶれ補正はRockSteadyを使用せず、EISをオフにしてGyroflowでPost Production補正します。EISオフ時にジャイロデータが記録され、Gyroflowに通すことでRockSteadyよりもなめらかな仕上がりが得られます。

Gyroflowを使用するための条件は以下のとおりです。

- EIS（電子手ぶれ補正）をオフにする
- FOVをワイドに設定する（ジャイロデータが記録されるのはワイド設定時のみ）

FOVについて、ノーマルは画角が狭すぎるため非推奨です。ウルトラワイドはGyroflowに対応しておらず、歪みも大きくなるため使用しません。

アスペクト比は通常4:3を推奨します。4:3はセンサーの全画角を使うため、Gyroflowの補正マージンが広く取れます。また、16:9や9:16に後からリフレームも可能です。ただし、スローモーション撮影（100FPS）は16:9限定のため、Gyroflowの補正マージンが狭くなる点に注意してください。

## ゲインとExpoチューニング

この項目はカメラ設定ではなく、コントローラーのスティック感度と飛行特性の設定です。一般に「Rate」と呼ばれるものです。

シネマティックな映像には滑らかな飛行操作が不可欠なため、飛行スタイルに応じた調整が必要です。
しかし、個人の感覚に依存するもので最適値は個人差があるため、自分に合う値を探してみてください。

以下は私のシネマティック撮影向け設定例です。

<!-- textlint-disable -->

{{ image(src="./rate.webp") }}

<!-- textlint-enable -->

設定の意図としては、ロールとピッチはある程度の機動性を確保しつつ、中央付近の操作が滑らかになるよう、Expoを高めにしています。ヨーはセンター感度と最大レートを大きく下げ、パン動作が急激にならないよう調整しています。シネマティック撮影ではヨーの滑らかさが映像品質に直結するため、意図して鈍感に設定しています。

## カメラアングル（チルト角）

カメラアングルは飛行速度と映像の見え方に直結します。角度が大きいほど高速で飛行でき、映像のスピード感も増します。一般的な目安は以下のとおりです。

| 飛行スタイル                          | 推奨角度 |
| ------------------------------------- | -------- |
| スローなシネマティック（cinewhoop的） | 10度以下 |
| 通常のシネマティック巡航              | 15〜25度 |
| フリースタイル                        | 25〜35度 |
| レース                                | 45度以上 |

私は**30度**にしています。
マニュアルモードでのダイナミックなシネマティック撮影を前提とし、ダイブや高速巡航を含む積極的な飛行に対応しつつ、シネマティックの範囲に収まる角度として設定しています。その場の飛行スタイルで変更するのもよいでしょう。ただし、慣れない内は決まったアングル角で飛ばすほうが感覚をつかみやすいです。

## その他のカメラ設定

- シャープネス：-2（最低値。インカメラのシャープニングは破壊的処理のため、最低に設定しPost Productionで適用する）
- ノイズリダクション：-2（最低値。インカメラのNRはディテールを潰すため、最低に設定しPost Productionで処理する）
- センターマーカー：オン（画面中央に「X」を表示。隙間やゲートを通過する際の照準に使用）
- グリッドライン：オン（三分割法の構図補助線を表示。映像の構図を意識した撮影に有用）

## 安全設定と機体保護

大前提ですが、Avata2は100g以上の機体のため航空法の遵守が必要です。

- DIPS2.0での機体登録とリモートID搭載
- 認証機体でないため、包括申請による飛行承認が必須
- DIPS2.0での飛行計画通報は必須
- 国土交通省の定める書式にて飛行日誌の作成が必要

映像設定とは直接関係ありませんが、安全な飛行のために以下の設定を推奨します。

- **RTH高度**：屋外では周囲の障害物より高い高度を設定する
- **電波ロスト時の動作**：屋外でRTHが可能な環境ではRTH、屋内などRTHが適さない環境ではホバリングに設定する
- **最大高度**：日本の航空法では150m未満の制限があるため、120mに設定する

<!-- textlint-disable -->

{% aside(position="right") %}
150m以上の飛行は包括申請の対象外で個別申請が必要となるため、一般的な飛行では150m未満に収める必要がある。
{% end %}

<!-- textlint-enable -->

また、以下のアクセサリの装着を推奨します。

- **NDフィルター**：露出調整だけでなく、レンズ保護としても有効
- **ジンバルバンパー**：墜落時のジンバルとカメラへのダメージを軽減する
- **モーターカバー**: 砂浜などでの撮影時モーターへの砂やゴミの侵入を防止する
- **プロペラガード**：屋内や近接飛行時の衝突ダメージを軽減する

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/g00togv5.9srin901.g00togv5.9sriof57/kaereba_main_202604281233494878?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fvanvenus%2Fvan-0d44tp29d%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fvanvenus%2Fi%2F10016617%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/vanvenus/cabinet/root_sniper_folder/sniper_folder_00031/imgrc0097362674.jpg?_ex=128x128" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/g00togv5.9srin901.g00togv5.9sriof57/kaereba_main_202604281233494878?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fvanvenus%2Fvan-0d44tp29d%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fvanvenus%2Fi%2F10016617%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >Avata 2 バンパー DJI Avata 2 適用 ジンバルプロテクター Avata 2 ジンバル バンパー フロント レンズ保護バーアルミ合金製 衝突防止 安全飛行 DJI Avata 2 アクセサリー用 (レッド)</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_202604281233494878?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2FAvata%2520%25E8%25A1%259D%25E7%25AA%2581%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt&m=http%3A%2F%2Fm.rakuten.co.jp%2F" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=Avata%20%E8%A1%9D%E7%AA%81&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/g00togv5.9srin901.g00togv5.9sriof57/kaereba_main_202604281233025454?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fvanvenus%2Fvan-0d2dlx3jw%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fvanvenus%2Fi%2F10016624%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/vanvenus/cabinet/root_sniper_folder/sniper_folder_00031/imgrc0097362772.jpg?_ex=128x128" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/g00togv5.9srin901.g00togv5.9sriof57/kaereba_main_202604281233025454?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fvanvenus%2Fvan-0d2dlx3jw%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fvanvenus%2Fi%2F10016624%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >LINGHUANG Avata 2 モーターカバーDJI Avata 2 モーター保護カバー ホコリや水分の侵入防止 アルミ合金製 dji avata2 アクセサリー対応 (4個入 赤)</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_202604281233025454?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2FAvata%2520%2520LINGHUANG%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt&m=http%3A%2F%2Fm.rakuten.co.jp%2F" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=Avata%20%20LINGHUANG&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>

<div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/g00uvo95.9srinb32.g00uvo95.9srio911/kaereba_main_202604281234561111?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Frikutonashop%2Frikutcqgg0%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Frikutonashop%2Fi%2F10008702%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/rikutonashop/cabinet/202604161849_17/rikutcqgg0_1.jpg?_ex=128x128" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/g00uvo95.9srinb32.g00uvo95.9srio911/kaereba_main_202604281234561111?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Frikutonashop%2Frikutcqgg0%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Frikutonashop%2Fi%2F10008702%2F&rafcid=wsc_i_is_c7c582dc-0853-4585-9176-66e2a26d9c5b" target="_blank" >DJIAvata360バンパープロペラガードプラスチック機体保護保護カバー保護ガードプロペラ保護防振耐衝撃安全飛行保護装置軽量耐久性衝突防止リング取り付けが簡単</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;"></div><div class="kaerebalink-link1" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/kaereba_main_202604281234561111?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2Favata%2520%25E3%2583%2597%25E3%2583%25AD%25E3%2583%259A%25E3%2583%25A9%25E3%2582%25AC%25E3%2583%25BC%25E3%2583%2589%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt&m=http%3A%2F%2Fm.rakuten.co.jp%2F" target="_blank" >楽天市場</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=avata%20%E3%83%97%E3%83%AD%E3%83%9A%E3%83%A9%E3%82%AC%E3%83%BC%E3%83%89&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=yostosweb-22" target="_blank" >Amazon</a></div></div></div><div class="booklink-footer" style="clear: left"></div></div>

## Post Productionの全体の流れ

Post Productionでは、次のような流れになります。なお、DaVinci Resolveを前提としています。

1. Timelineの設定と編集
2. Gyroflowでのぶれ補正
3. モーションブラーの付加
4. カラーグレーディング

以下、それぞれの工程について説明します。

### Timelineの設定と編集

まずDaVinci ResolveのProject SettingにてTimelineの設定を行ないます。
DJI Avata 2はUltra HD(UHD)で動画記録しているので、TimelineもUHDにしておきます。

Frame Rateについて以下を参考に設定してください。

- アクション感のあるシャープな映像にしたいケース：60FPS
- 自然なモーションブラーのある映像にしたいケース：30FPS
- シネマティックな映像にしたいケース：24FPS

### Gyroflowによる手ぶれ補正

すべての素材に対して、まずGyroflowで手ぶれ補正を適用します。EISオフ・FOVワイドで撮影した素材にはジャイロデータが記録されており、
Gyroflowに通すことでRockSteadyよりもなめらかな補正が得られます。

Gyroflowのパラメータ設定には、[gyrotriage](/blog/2026/03/gyrotriage/)の記事を参照してください。

### モーションブラー（RSMB）

Gyroflow適用後、映像の仕上がりに応じてフレームレートとモーションブラーの処理を変えます。
撮影は基本的には4K 60FPSで録画します。しかし、映像の目的により出力する映像のFPSを変更するケースがあります。

アクションを狙った映像であればそのまま60FPSで取得すればよいのですが、仕上がりの想定によってはFPSを落としたい場合があります。

しかし、60FPSで撮影した素材は180度ルールに従った1/120秒のモーションブラーしか持ちません。これでは、30FPSや24FPSに変換しただけではブラーが不足します。

30FPSや24FPSで映像を出力したい場合は、RSMB（ReelSmart Motion Blur）でブラーを足します。
このツールは、フレーム間のモーションベクトルを解析してブラーを合成するOFXプラグインで、DaVinci ResolveのEditページで直接適用できます。

### カラーグレーディング

D-Log Mで撮影した場合は、LUTを適用してカラーグレーディングを行います。推奨は[Film Poets SkyGrades Collection](https://www.thefilmpoets.com/edu/store/dji-avata-2-d-log-m-skygrades-collection/)（Natural + Cinemaのセット）です。

SkyGradesが優れている理由は以下のとおりです。

- DJI機種ごとのD-Log Mカラーサイエンスに合わせて個別設計されており、汎用LUTにありがちな色の破綻が起きにくい
- D-Log Mのフラットなガンマカーブを数学的に補正し、ダイナミックレンジを最大限維持したまま自然な色を再現する
- 過度に彩度を上げない設計で、緑の色被りなどDJI特有の問題を補正する
- NaturalとCinemaの2種類をブレンドすることで、自然な色味からシネマティックな色味まで1つのワークフローでカバーできる

DaVinci Resolveでの適用手順は以下のとおりです。

1. Node 1にSkyGrades Natural LUTを適用
2. シリアルNode 2を追加しSkyGrades Cinema LUTを適用
3. 各ノードのKey Output Gainを調整して、Naturalの補正強度とCinemaのスタイル強度をそれぞれ好みに合わせる（FCPの公式ガイドではMix 0.5を起点に紹介されている）

## 作例

冒頭で紹介した映像は、千葉県・根本海水浴場で撮影しました。安全マージンを優先して高度を高めに取っています。

[^1]: 著者は二等無人航空機操縦士のライセンスを取得し、目視外飛行の限定解除と包括飛行申請をしたうえでマニュアルモードでのFPV飛行を実施している。これらを取得していない場合は、補助者の配置または個別の飛行許可・承認が必要となる。

[^2]: 本記事には広告（アフィリエイト）リンクが含まれます。
