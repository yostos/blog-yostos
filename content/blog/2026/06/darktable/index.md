+++
title = "GR IV Monochromeから始めるdarktable現像術"
description = """
RAW 現像に、無料でありながら高機能な darktable を選びました。RICOH GR IV Monochrome を手にしたのがきっかけです。とっつきにくいツールですが、その核心は scene-referred ワークフローにあります。本稿では、この考え方に沿ってモノクロ写真をどう現像していくのかを、実際の操作画面とともに、本当に使うモジュールだけに絞って解説します。
"""
date = 2026-06-12T09:46:20+09:00
[taxonomies]
tags = ["Creative", "Photography"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

{{ image(src="cover.webp",alt="Cover") }}

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

<!-- more -->

[RICOH GR IV Monochrome](@/blog/2026/05/gr-iv-monochrome/index.md) を手に入れました。モノクロ専用機です。買うべき理由や撮影時の設定は別記事にまとめましたが、本稿はその続きにあたります。このカメラを手にしたのを機に、長らく惰性で使ってきたRAW現像アプリを一度見直すことにしました。撮ったあとの工程、つまり選定の記録と、最終的に選んだdarktableをモノクロ前提でどう使っているかのメモです。

## RAW現像アプリの選定

これまで使ってきたのは、市川ソフトラボラトリーのSILKYPIXでした。ただ、選んで使い続けてきたというより惰性です。今回そのまま使えなかったのは、GR IV Monochromeに対応していないからです。SILKYPIXは未対応のカメラ・レンズのRAWファイルをそもそも開けません。加えてMac版はWindows版から数年遅れたまま放置されており、現像も遅いと、見直す理由はそろっていました。

候補としていちばん有力だったのはAdobeのLightroom Classicです。操作は直感的で非常に使いやすく、RAWファイルのライブラリ構成を自分で管理でき、Lightroomが勝手に干渉してこないのも気に入っています。ただし、使うには悪名高いAdobeのサブスクリプションが要ります。そこだけがどうしても引っかかりました。

結局、無料でありながら高機能なdarktableを使うことにしました。

## darktable

darktableは高機能なのですが、Lightroomのように機能が整理されておらず、最初は取っ付きにくいツールです。モジュールの数も多く、全部を理解しようとすると挫折します。そこで、モノクロ前提で本当に使うモジュールだけを絞り込みました。現像はおおむね次の順序で進めます。

1. `lens correction`（必須）— Lensfunデータベースを使い、歪曲と周辺減光を補正する
2. `exposure`（必須）— 主要被写体の中間調を適正にする(白飛び・黒つぶれは無視)
3. `sigmoid`（必須）— ダイナミックレンジを表示レンジへ圧縮する(filmic rgb / agxでも可)
4. `denoise (profiled)`（オプション）— ノイズを抑える
5. `rotate and perspective`（オプション）— 傾いた水平を出す(必要ならパースも整える)
6. `retouch`（オプション）— ゴミや不要物を消す
7. `tone equalizer`（オプション）— 明暗の局所コントラストを足す
8. `diffuse or sharpen`（オプション）— 仕上げにシャープ化する(旧来のsharpenでも可)
9. `crop`（オプション）— 最後に構図をトリミングする

この流れの前提になっているのが、darktableが標準で採るscene-referredワークフローです。これは、センサーが捉えた光の量(リニアな値)をできるだけそのまま保ったまま現像を進め、モニタ表示に合わせた明暗の調整は最後にまとめて行う、という考え方です。明るさの情報を途中で切り詰めず、広いダイナミックレンジのまま持ち越して、いちばん最後にトーンマッピング(`sigmoid` など)で表示レンジへ圧縮します。

この前提があるので、作業は自然と二段構えになります。`exposure` では主要被写体の中間調だけを合わせ、白飛び・黒つぶれはあえて気にしません。広い階調はあとで `sigmoid` がまとめて表示レンジに収めてくれるからです。本稿のモジュール選定も、この流れに沿っています。

なお、darktableのモジュールは画面に並んだ順ではなく、内部で決められたパイプライン順に適用されます。上の並びはそのパイプライン順ではなく、darktable公式マニュアルが薦める作業順(最初にlens correction、次に基礎となる露出とトーンマッピング、続いて各種補正、最後に構図の仕上げ)に沿っています。

### lens correction

{% module(src="./lens-correction.webp", alt="darktableのlens correctionモジュール") %}

`lens correction` を有効にすると、Lensfunデータベースを参照して歪曲と周辺減光を自動補正します。GRの単焦点にもわずかな樽型の歪曲と周辺減光があり、これをまず取り除いておきます。

{% end %}

6月12日時点では、Lensfunの公式データベースにRICOH GR IV Monochromeはまだ登録されていません。ただしGR IV(カラー機)は登録済みで、Monochromeのレンズ(光学系)はGR IVとまったく同じです。違いはセンサー前のカラーフィルターの有無だけなので、補正すべき歪曲・周辺減光のデータは共通して使えます。

問題は、MonochromeがEXIFに記録するカメラ名がGR IVとは別の文字列で、公式データベースのGR IVエントリに自動マッチしないことだけです。そこで、ユーザー領域のLensfunデータベースにMonochrome用のカメラ定義を1つだけ追加し、マウントをGR IVと同じ `ricohGRIV` にして既存のレンズ補正データを流用します。

darktableは `~/.local/share/lensfun/` 配下に置いたXMLを読み込みます。ここは公式データベースの更新では上書きされない領域です。次のファイルを置きます。

```xml,name=ricoh-gr-iv-monochrome.xml
<lensdatabase version="1">
  <camera>
    <maker>Ricoh Imaging Company, Ltd.</maker>
    <maker lang="en">Ricoh</maker>
    <model>Ricoh GR IV Monochrome</model>
    <model lang="en">GR IV Monochrome</model>
    <mount>ricohGRIV</mount>
    <cropfactor>1.53</cropfactor>
  </camera>
</lensdatabase>
```

`<model>` は実機がEXIFに書き込むモデル名と一致させる必要があります。手元の値は `exiftool` で確認できます。darktableを再起動すると、スクリーンショットのようにcamera欄へ「Ricoh, GR IV Monochrome」が現れ、lens欄にはGR IVの固定レンズ補正がそのまま当たります。

### exposure

{% module(src="./exposure.webp", alt="darktableのexposureモジュール") %}

scene-referredワークフローの起点です。前述のとおり、ここでは主要被写体の中間調が適正になるよう露出だけを決め、白飛びや黒つぶれは気にしません。スライダーを動かして、見せたい部分の明るさを合わせます。

{% end %}

### sigmoid

{% module(src="./sigmoid.webp", alt="darktableのsigmoidモジュール") %}

scene-referredな広いダイナミックレンジを、モニタが表示できる範囲へ圧縮するトーンマッピングです。darktableではfilmic rgbやagxと同じ役割を担い、`sigmoid` はそのなかでも素直に効きます。基本はcontrastで圧縮の強さを、skewでシャドウ側とハイライト側のどちらを持ち上げるかを決めるだけです。モノクロではprimaries(色の扱い)の各パラメータは結果に影響しないので、触る必要はありません。

{% end %}

### denoise (profiled)

{% module(src="./denoise.webp", alt="darktableのdenoise (profiled) モジュール") %}

高感度で撮った暗所のカットなどで、輝度ノイズのザラつきが気になるなら使います。

センサーごとに測定されたノイズの統計プロファイルを参照してノイズを除去するモジュールです。モノクロは輝度ノイズがそのまま見えるぶん、ザラつきが目立ちやすいので、気になるカットで抑えます。低感度で破綻がなければ飛ばして構いません。

{% end %}

### rotate and perspective

{% module(src="./rotate.webp", alt="darktableのrotate and perspectiveモジュール") %}

水平が傾いてしまったカットや、建築物の垂直を立て直したいときに使います。GRはノーファインダー撮影が多く、水平も傾きやすいカメラです。

rotationスライダーで角度を調整するか、画像上で水平にしたい線をドラッグして指定すると、その線が水平(または垂直)になるよう自動で回転します。パースの崩れを直したいときは、隠れているlens shiftやshearのコントロールも使えますが、スナップ中心の用途なら水平出しだけで十分です。

{% end %}

### retouch

{% module(src="./retouch.webp", alt="darktableのretouchモジュール") %}

センサーのゴミや、写り込んだ不要物が目立つときに使います。

ヒーリングやクローンで対象を周囲になじませて消すモジュールです。モノクロは小さなゴミも意外と目立つので、気になるときだけ使い、なければ飛ばします。

{% end %}

### tone equalizer

{% module(src="./tone-equalizer.webp", alt="darktableのtone equalizerモジュール") %}

特定の明るさ帯だけを覆い焼き・焼き込みしたいときに使います。たとえばシャドウだけ持ち上げたいが全体は明るくしたくない、といった局所的な明暗調整に向きます。

露出帯(-8EV〜0EV)ごとに明るさを持ち上げ・押し下げでき、全体ではなく狙った帯だけに局所コントラストを足せます。

{% end %}

### diffuse or sharpen

{% module(src="./diffuse-or-sharpen.webp", alt="darktableのdiffuse or sharpenモジュール") %}

仕上げに解像感を一段上げたいときに使うシャープ化モジュールです。

偏微分方程式ベースで、プリセット(sharpen demosaicingなど)から選ぶと扱いやすくなります。軽く整える程度なら、旧来の `sharpen` モジュールでも十分です。

{% end %}

### crop

{% module(src="./crop.webp", alt="darktableのcropモジュール") %}

周辺の不要な部分を切り落として構図を整えたいときに使います。

darktableは露出やトーンの調整を画面全体に対して効かせるので、トリミングは仕上げの段階に回します。アスペクト比は自由(freehand)のまま、不要な周辺を切り落として構図を決めます。

{% end %}

## References

{% references() %}

- [darktable user manual](https://docs.darktable.org/usermanual/development/en/). darktable公式ユーザーマニュアル
- [darktable user manual](https://docs.darktable.org/usermanual/development/en/overview/workflow/process/).「the pixelpipe and module order」scene-referredワークフローと処理の流れ
- [darktable user manual](https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/lens-correction/).「lens correction」モジュール
- [darktable user manual](https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/rotate-perspective/).「rotate and perspective」モジュール
- [darktable user manual](https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/crop/).「crop」モジュール
- [darktable user manual](https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/sigmoid/).「sigmoid」モジュール
- [Lensfun](https://lensfun.github.io/). レンズ補正データベースのプロジェクトサイト([GitHub リポジトリ](https://github.com/lensfun/lensfun))
- [discuss.pixls.us](https://discuss.pixls.us/t/darktable-4-8-location-of-lensfun-database-for-personal-use/44682).「darktable 4.8 location of lensfun database for personal use」ユーザー領域へのLensfunデータ追加方法

{% end %}

