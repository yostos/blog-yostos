+++
title = "ターミナルのフォントを整える(2026年版)"
description = """
WezTerm のフォント設定を、欧文 Berkeley Mono、全角 更紗ゴシック、アイコン Symbols Nerd Font Mono の3段構成に組み直しました。
セル幅を実測して scale を決め、全角が正確に2セルへ収まる状態にしています。
"""
date = 2026-09-07T13:04:27+09:00
[taxonomies]
tags = ["Tech", "Font"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.avif"
+++

<!-- textlint-disable -->

{{ image(src="cover.avif", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

ターミナルの欧文フォントには、[以前の記事](/blog/2024/12/berkeley-mono/)で書いたとおり
[Berkeley Mono](https://berkeleygraphics.com/typefaces/berkeley-mono/) を使い続けています。
ただしBerkeley Monoは日本語のグリフを持たないため、日本語は別のフォントにフォールバックさせる必要があります。
このフォールバックの設定を、思いつきで書くのではなく実測して組み直しました。

<!-- more -->

## WezTerm のフォント設定の最終構成

結論を先に書くと、欧文がBerkeley Mono、全角が更紗ゴシック、アイコンがSymbols Nerd Font Monoという
3段構成に落ち着きました。全角文字がちょうど2セルに収まり、`①` のような文字がセルからはみ出さず、
太字と斜体のすべての組み合わせが合成ではなく実フェイスで描かれる状態です。

| 役割     | フォント                      | 指定            |
| -------- | ----------------------------- | --------------- |
| 欧文     | Berkeley Mono（静的版）       | セル幅 0.600 em |
| 全角     | 更紗ゴシック（Sarasa Term J） | `scale = 1.2`   |
| アイコン | Symbols Nerd Font Mono 3.5.1  | 指定なし        |

`font_size` は20.0です。ターミナルは文字を等幅のマス目に並べて表示します。
欧文1文字がマス目1つ、日本語1文字はマス目2つにちょうど収まらないと表示が崩れるため、
サイズは自由に選べません。20.0はその条件を満たす値です。詳しくは後述します。

## 文字の送り幅をどう測ったか

ターミナルのフォント設定は、見た目で判断すると微妙なズレを見逃します。
そこで2つの道具で数値を取りました。測る対象は送り幅、
つまり1文字を描いたあと次の文字の位置までカーソルが進む距離です。

ひとつはfontToolsです。フォントファイルそのものを読み、`hmtx` テーブルから
送り幅を取り出します。フォントと文字を並べて一度に測りました。

```python,name=probe.py
from fontTools.ttLib import TTFont
from pathlib import Path

# ttc は fontNumber でフェイスを選ぶ。220 は Sarasa Term J Regular
FONTS = [
    ("Berkeley Mono Regular", "BerkeleyMono-Regular.otf", 0),
    ("Sarasa Term J Regular", "Sarasa-SuperTTC.ttc", 220),
]
CHARS = [("A", 0x41), ("あ", 0x3042), ("①", 0x2460)]

for label, name, index in FONTS:
    f = TTFont(Path.home() / "Library/Fonts" / name, fontNumber=index, lazy=True)
    upem = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    cols = []
    for char, cp in CHARS:
        gid = cmap.get(cp)
        adv = f"{f['hmtx'][gid][0] / upem:.3f} em" if gid else "-"
        cols.append(f"{char} {adv:>8}")
    print(f"{label:24}" + "  ".join(cols))
```

```text
Berkeley Mono Regular   A 0.600 em  あ        -  ①        -
Sarasa Term J Regular   A 0.500 em  あ 1.000 em  ① 0.500 em
```

emは文字サイズを1とした単位なので、この値はフォントサイズに左右されない設計値です。
Berkeley Monoは 'A' を0.600 emで送り、日本語のグリフは持ちません。
更紗ゴシックは半角が0.500 em、全角が1.000 emで、`①` は半角側です。
2つのフォントは幅の基準そのものが違う、というのがここで分かります。

もうひとつはWezTerm自身の `ls-fonts` です。こちらは「設定を与えたときに実際にどのファイルの
どのフェイスが選ばれ、送り幅がいくつになるか」を返します。`--codepoints` には
調べたい文字をUnicodeのコードポイントで渡します。`3042` はU+3042、ひらがなの「あ」です。

```bash,name=check.sh
wezterm --config-file ./test.lua ls-fonts --codepoints 3042
```

```text
0 あ \u{3042} x_adv=24 cells=2 glyph=10207 wezterm.font("Sarasa Term J", ...)
```

読み方はこうです。「あ」は更紗ゴシックから取られ、送り幅を表す `x_adv` は24ピクセル、
占める幅は `cells=2` で2セル。このときのセル幅は12ピクセルなので、送り幅はちょうど2倍で、
全角がセル2つに過不足なく収まっています。ここがズレていると日本語混じりの表や罫線が崩れます。

フォントファイルの設計値と、WezTermが実際に採用する値は一致しないことがあるため、
この2つを突き合わせる必要がありました。

## 全角を正確に2セルへ

更紗ゴシックは半角0.500 em、全角1.000 emという厳密なグリッドを持っています。
一方Berkeley Monoのセル幅は0.600 emです。セルの幅はBerkeley Monoに合わせるため、
全角が収まるべき2セルは1.200 emになります。更紗ゴシックの全角は1.000 emなので、
そのまま並べると0.200 em足りません。

WezTermの `scale` は、フォールバックさせるフォントを何倍で描くかを指定します。
0.500 × 1.2 = 0.600なので、`scale = 1.2` にすれば更紗ゴシックの半角がBerkeleyのセル幅と一致し、
全角はその2倍になります。総当たりで確認しました。

| scale | セル幅 | `あ`（要24） | `①`（要12） |
| ----- | ------ | ------------ | ----------- |
| 1.1   | 12     | 22           | 11          |
| 1.15  | 12     | 23           | 12          |
| 1.2   | 12     | **24**       | **12**      |
| 1.25  | 12     | 25           | 13          |

ここで厄介なのが、WezTermがセル幅を整数に丸めることです。
`0.600 × font_size` が整数から離れると、丸めの誤差でグリッドが崩れます。
`font_size` を振って確かめたところ、成立するサイズは限られていました。

| font_size | セル幅 | `あ` | `①` | 判定          |
| --------- | ------ | ---- | --- | ------------- |
| 16.0      | 10     | 19   | 10  | 全角が1px不足 |
| 18.0      | 11     | 22   | 11  | ぴったり      |
| 19.0      | 11     | 23   | 12  | 1px超過       |
| 20.0      | 12     | 24   | 12  | ぴったり      |
| 21.0      | 13     | 25   | 13  | 全角が1px不足 |
| 22.0      | 13     | 26   | 13  | ぴったり      |
| 24.0      | 14     | 29   | 15  | 1px超過       |

`font_size = 20.0` を選んでいるのはこのためです。18.0と22.0も使えますが、
21.0や24.0に動かすと桁がずれます。⌘+ と ⌘− でサイズを変える運用をしていると
崩れる場面があるので、この事情は設定ファイルにコメントとして残しました。

## Ambiguous 幅と漢字カバレッジ

日本語フォントなら何でもよいわけではありません。決定的なのはEast Asian Ambiguous、
つまり半角と全角のどちらとも解釈しうる文字の扱いです。
`①②③`、`◆`、`※` あたりが該当します。

macOS標準のヒラギノ角ゴシックはこれらを全角で設計しているため、
セル幅12に対して送り幅が13.75になりました。
25パーセントはみ出して隣の文字と干渉します。しかもこれは `scale` を振っても変わりませんでした。

更紗ゴシック（Sarasa Term J）は、Ambiguousを半角として設計した系統です。
`①` と `◆` はどちらも0.500 emで、`scale = 1.2` を掛けてちょうど1セルに収まります。
同じ更紗ゴシックでも "Mono" 系統はAmbiguousが全角なので、ターミナルには "Term" を選ぶ必要があります。

漢字のカバレッジも測りました。ここは数え方に注意が必要です。

| フォント             | JIS X 0208 | JIS X 0213 | Unicode CJK統合漢字 |
| -------------------- | ---------- | ---------- | ------------------- |
| Sarasa Term J        | 100 %      | 100 %      | 100 %               |
| ヒラギノ角ゴ Sans W3 | 100 %      | 85.3 %     | 51.3 %              |

ヒラギノの51.3パーセントという数字は一見すると低く見えますが、
UnicodeのCJK統合漢字ブロックは日本語・簡体字・繁体字・韓国・ベトナムの漢字を
すべて含む集合なので、日本語フォントの評価軸としては適切ではありません。
PythonのShift_JISコーデックで判定したところ、ヒラギノに無い1万225字のうち
JIS X 0208に含まれるものは0字でした。常用漢字と人名用漢字は完全にカバーしています。

なおmacOS全体では、標準フォントを合わせるとCJK統合漢字を100パーセント表示できます。
ただし日本語フォントに無い字はHiragino Sans GB（簡体字）やHeiti TC（繁体字）に落ちるため、
表示はされても字形が中国字体になります。更紗ゴシックを使うと、この落下自体が起きません。

## Nerd Font はシンボル専用フォントで足りる

以前はNerd Fontのアイコンを、パッチ済みの日本語フォントから取っていました。
しかしアイコンのためだけに日本語フォントを1本抱えるのは無駄です。
[nerd-fonts](https://github.com/ryanoasis/nerd-fonts) には
シンボルだけを収録したフォントがあり、Homebrewから入ります。

```bash
brew install --cask font-symbols-only-nerd-font
```

実はWezTermにはSymbols Nerd Font Monoが同梱されていて、
何もしなくてもフォールバック連鎖の末尾に入っています。
アイコンの解決先を29点サンプリングしたところ、23点が内蔵フォントで解決し、
Powerlineの区切りはWezTerm自身が描画していました。
豆腐になったのは `U+E6B5` と `U+EC1E` の2点だけです。

つまり多くの場合は内蔵で足ります。それでも単体版を入れたのは、
内蔵版が古いビルドで上記2点が欠けていたためです。
インストール版がCoreText経由で優先されることと、欠けていた2字が埋まることは確認しました。

## 更紗ゴシックとは

更紗ゴシックはRenzhi Li（Belleve Invis）氏によるOFL-1.1のフォントです。
[Iosevka](https://typeof.net/Iosevka/) の作者でもあります。

中身を知っておくと判断しやすくなります。フォントファイルの著作権表記はこうなっています。

```text
Copyright (c) 2015-2025, Renzhi Li (aka. Belleve Invis, belleve@typeof.net).
Portions Copyright (c) 2016 The Inter Project Authors.
Portions Copyright (c) 2014-2021 Adobe Systems Incorporated.
Portions Copyright (c) 2012 Google Inc.
```

Adobeが源ノ角ゴシック（Source Han Sans）、GoogleがNoto Sans CJKです。
つまり更紗ゴシックの漢字とかなは源ノ角ゴシックそのもので、
作者の仕事はIosevkaの欧文と合成し、半角と全角を厳密に1:2のグリッドへ再設計することでした。
今回の構成では欧文をBerkeley Monoが担当するので、更紗ゴシックは実質的に
「ターミナル用に幅を再設計した源ノ角ゴシック」として働いています。

Iosevka自体もコード用のフォントとしては高く評価されています。文字幅が狭いので、老眼にはつらいのですが多くの情報を表示できるので好まれているようです。

"J" は日本語字形を意味します。同じ更紗ゴシックでもSCを選ぶと漢字が中国字形になるため、
日本語環境ではJを選ぶ必要があります。

ウェイトは5段（200 / 300 / 400 / 600 / 700）で、それぞれにイタリックがあり、
合計10面すべてが実フェイスです。nameID 1では
`Sarasa Term J Light` のように枝番のファミリ名に分かれていますが、
nameID 16のタイポグラフィックファミリは10面とも `Sarasa Term J` で共通なので、
ファミリ名は変えずに `weight` を指定するだけで切り替わります。
日本語フォントにイタリックがあるのは珍しく、ヒラギノはW0からW9まで10段のウェイトを持ちながら
イタリックを1面も持ちません。ターミナルでは斜体をコメントの表示に使うので、ここは実用差になります。

供給元について書いておくと、フォントは実行ファイルではなく、
ネットワークアクセスとテレメトリのいずれも持ちません。理論上の懸念はTrueTypeのヒンティング命令ですが、
更紗ゴシックのヒンティングはttfautohintによる自動生成で、
macOSのCoreTextはフォント解析をサンドボックス下で行います。
GitHub Releasesから手動でダウンロードするとチェックサムの検証がないため、
Homebrewのcask経由に切り替えました。

```bash
brew install --cask font-sarasa-gothic
```

ライセンスはOFL-1.1で、撤回できません。一度入手したものを後から使えなくされることは
原理的にないという点は、単一ベンダーの商用フォントより安心できる部分です。

## WezTerm の設定

設定の該当部分です。`font_rules` は指定したフォントで丸ごと置き換わる仕様なので、
太字と斜体でも同じ3段を組み直す必要があります。ここを怠ると、
太字の日本語やアイコンがフォールバックから外れます。

```lua,name=wezterm.lua
local function font_stack(weight, italic)
 return wezterm.font_with_fallback({
  { family = "Berkeley Mono", weight = weight, style = italic and "Oblique" or "Normal" },
  -- Sarasa は Oblique を持たず Italic
  { family = "Sarasa Term J", weight = weight, style = italic and "Italic" or "Normal", scale = 1.2 },
  { family = "Symbols Nerd Font Mono" },
 })
end

config.font = font_stack(400, false)

config.bold_brightens_ansi_colors = true
config.font_rules = {
 { intensity = "Bold", font = font_stack(700, false) },
 { italic = true, font = font_stack(400, true) },
 { italic = true, intensity = "Bold", font = font_stack(700, true) },
}
```

`font_size = 20.0` は別のテーブルで設定しています。
なぜこの値なのか、なぜ `scale` が1.2なのかは、忘れた頃に自分を助けるので
実測値ごとコメントとして設定ファイルに残しました。

## まとめ

設定の結果、送り幅を検証すると次のようになります。

```text
A      x_adv=12  cells=1   1セルぴったり
あ 漢  x_adv=24  cells=2   2セルぴったり
① ◆   x_adv=12  cells=1   1セルぴったり
```

日本語混じりの表や罫線が崩れなくなり、`①` のような記号が隣の文字と重ならなくなりました。太字と斜体は、欧文がBerkeley Monoの設計どおりのOblique、和文が更紗ゴシックの実イタリックで描かれます。合成は発生していません。アイコンのために日本語フォントを抱える必要もなくなりました。

この記事の原稿をエディタで開いた画面です。日本語と欧文が混ざっても、文字がマス目からはみ出さずに並んでいます。

<!-- textlint-disable -->

{{ image(src="wezterm.webp", alt="日本語と欧文が混在する原稿をWezTermで表示した画面",caption="日本語と欧文が混在する原稿をWezTermで表示した画面") }}

<!-- textlint-enable -->

和文を1.2倍で描いているため日本語が欧文よりやや大きく見えますが、個人的にはこちらの方が読みやすく感じています。また欧文がまとまって見えるので、コード交じりの文章も見やすくなりました。

## References

<!-- textlint-disable -->

{% references() %}

- [Berkeley Graphics](https://berkeleygraphics.com/typefaces/berkeley-mono/). "Berkeley Mono Typeface"
- [Sarasa Gothic](https://github.com/be5invis/Sarasa-Gothic). 「更紗ゴシック」
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts). "Iconic font aggregator"
- [WezTerm](https://wezterm.org/config/fonts.html). "Font Configuration"
- [Adobe Type Tools](https://github.com/adobe-fonts/source-han-sans). "Source Han Sans"

{% end %}

<!-- textlint-enable -->
