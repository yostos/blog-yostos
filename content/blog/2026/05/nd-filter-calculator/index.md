+++
title = "NDフィルターを計算で選ぶ - DJIドローン向け計算ツール"
description = """晴天下のドローン撮影でNDフィルターを勘で選んでいませんか。\
計測したシャッタースピードを入力するだけで適正なND濃度を返す計算ツールを記事内に用意しました。"""
date = 2026-05-19


[taxonomies]
tags = ["Creative", "Aerial Videography"]

[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

## ドローンNDフィルター計算ツール

実測したシャッタースピード（SS）から推奨フィルターを返します。PLフィルターとNDフィルターセット（ND8/ND16/ND32/ND64）を所有している前提です。

<div class="nd-calc">
  <div class="nd-calc__form">
    <div class="nd-calc__field">
      <label for="nd-ss">実測シャッタースピード</label>
      <input type="text" id="nd-ss" value="1/2000" autocomplete="off" inputmode="text">
      <small>例: 1/2000、2000、0.0005</small>
    </div>
    <div class="nd-calc__field">
      <label for="nd-fps">撮影フレームレート</label>
      <select id="nd-fps">
        <option value="60">60fps（標準シネマティック / 目標SS 1/120）</option>
        <option value="120">120fps（スローモーション / 目標SS 1/240）</option>
        <option value="24">24fps（フィルムルック / 目標SS 1/48）</option>
        <option value="50">50fps（PAL / 目標SS 1/100）</option>
      </select>
    </div>
    <div class="nd-calc__field">
      <label for="nd-ev">目的露出補正（EV）</label>
      <input type="number" id="nd-ev" value="0" step="0.1" inputmode="decimal">
      <small>既定はEV0。ETTRなどの運用方針は本文「露出補正（EV）の扱い」を参照。</small>
    </div>
    <button type="button" id="nd-calc-btn">計算する</button>
  </div>
  <output id="nd-result" class="nd-calc__result" aria-live="polite"></output>
</div>

<style>
.nd-calc {
  border: 1px solid var(--divider-color, #d7d7d7);
  background: var(--bg-1, #f7f7f7);
  border-radius: 8px;
  padding: 1.2rem 1.4rem;
  margin: 1.5rem 0;
  font-family: var(--sans-serif-font, sans-serif);
}
.nd-calc__form { display: grid; gap: 0.9rem; }
.nd-calc__field { display: grid; gap: 0.3rem; }
.nd-calc__field label { font-weight: 600; font-size: 0.95rem; color: var(--text-color, #222); }
.nd-calc__field input,
.nd-calc__field select {
  padding: 0.55rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--divider-color, #ccc);
  border-radius: 4px;
  background: var(--bg-2, #fff);
  color: var(--text-color, #222);
  font-family: inherit;
}
.nd-calc__field small { color: var(--meta-color, #666); font-size: 0.82rem; }
.nd-calc button {
  padding: 0.65rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  background: var(--primary-color, #087E96);
  color: var(--background-color, #fff);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  justify-self: start;
}
.nd-calc button:hover { opacity: 0.9; }
.nd-calc__result {
  display: block;
  margin-top: 1rem;
  padding: 0.95rem 1.1rem;
  border-radius: 6px;
  background: var(--bg-2, #fff);
  border-left: 4px solid var(--primary-color, #087E96);
  font-size: 0.95rem;
  line-height: 1.65;
  color: var(--text-color, #222);
}
.nd-calc__result:empty { display: none; }
.nd-calc__result .nd-calc__rec {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: var(--text-color-high-contrast, #111);
}
.nd-calc__result .nd-calc__warn {
  color: #c0392b;
  font-weight: 600;
}
.nd-calc__result p { margin: 0.3rem 0; }
.nd-calc__result dl {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 0.25rem 1rem;
  margin: 0.5rem 0 0 0;
}
.nd-calc__result dt { color: var(--meta-color, #666); font-weight: 500; }
.nd-calc__result dd { margin: 0; }
</style>

<script>
(function () {
  function parseSS(input) {
    if (typeof input !== 'string') return NaN;
    var s = input.trim();
    if (!s) return NaN;
    if (s.indexOf('/') >= 0) {
      var parts = s.split('/');
      var num = parseFloat(parts[0]);
      var den = parseFloat(parts[1]);
      if (!isFinite(num) || !isFinite(den) || num === 0 || den === 0) return NaN;
      return den / num;
    }
    var n = parseFloat(s);
    if (!isFinite(n) || n <= 0) return NaN;
    return n >= 1 ? n : 1 / n;
  }
  function ssLabel(denom) {
    if (denom >= 1) {
      var d = denom >= 10 ? Math.round(denom) : Math.round(denom * 10) / 10;
      return '1/' + d;
    }
    return (1 / denom).toFixed(2) + 's';
  }
  function fmtSigned(x, digits) {
    digits = digits == null ? 2 : digits;
    var v = x.toFixed(digits);
    if (x >= 0 && v.charAt(0) !== '-') return '+' + v;
    return v;
  }
  function calc() {
    var ssInput = document.getElementById('nd-ss').value;
    var fps = parseFloat(document.getElementById('nd-fps').value);
    var evInput = parseFloat(document.getElementById('nd-ev').value);
    var ev = isFinite(evInput) ? evInput : 0;
    var out = document.getElementById('nd-result');
    var measured = parseSS(ssInput);
    if (!isFinite(measured) || measured <= 0) {
      out.innerHTML = '<p class="nd-calc__warn">入力を解釈できませんでした。例: 1/2000、2000、0.0005</p>';
      return;
    }
    var PL_STOPS = 1.5;
    var targetDenom = 2 * fps;
    var stops = Math.log2(measured / targetDenom) - ev;
    var html = '';
    if (stops > 6.5) {
      var shortBy = (stops - 6).toFixed(2);
      html += '<p class="nd-calc__warn">ND64/PL（6段）でも約 ' + shortBy + ' 段不足します</p>';
      html += '<p>K&Fセットの減衰能力を超えています。光量が落ち着くまで待つか、撮影モードや時間帯を変更する判断材料にしてください。</p>';
      html += '<dl>';
      html += '<dt>必要段数</dt><dd>' + stops.toFixed(2) + ' 段</dd>';
      html += '</dl>';
    } else if (stops >= 2.25) {
      var rounded = Math.max(3, Math.min(6, Math.round(stops)));
      var ndVal = Math.pow(2, rounded);
      var err = stops - rounded;
      var errLabel = err > 0.05 ? 'やや明るめ（グレーディングで微調整、許容範囲内）'
                   : err < -0.05 ? 'やや暗め（ISOを200程度に微増するか、グレーディングで持ち上げ）'
                   : 'ほぼ適正';
      html += '<p class="nd-calc__rec">推奨: ND' + ndVal + '/PL（' + rounded + '段）</p>';
      html += '<dl>';
      html += '<dt>実測SS</dt><dd>' + ssLabel(measured) + '</dd>';
      html += '<dt>目標SS</dt><dd>' + ssLabel(targetDenom) + '（' + fps + 'fps）</dd>';
      html += '<dt>必要段数</dt><dd>' + stops.toFixed(2) + ' 段</dd>';
      html += '<dt>露出誤差</dt><dd>' + fmtSigned(err) + ' 段（' + errLabel + '）</dd>';
      html += '</dl>';
    } else {
      var plErr = stops - PL_STOPS;
      var plLabel = plErr > 0.2 ? 'やや明るめ（グレーディングで微調整、許容範囲内）'
                  : plErr < -0.2 ? 'やや暗め（ISOを200程度に微増するか、グレーディングで持ち上げ）'
                  : 'ほぼ適正';
      html += '<p class="nd-calc__rec">推奨: PLフィルター（実効約' + PL_STOPS.toFixed(1) + '段）</p>';
      html += '<dl>';
      html += '<dt>実測SS</dt><dd>' + ssLabel(measured) + '</dd>';
      html += '<dt>目標SS</dt><dd>' + ssLabel(targetDenom) + '（' + fps + 'fps）</dd>';
      html += '<dt>必要段数</dt><dd>' + fmtSigned(stops) + ' 段</dd>';
      html += '<dt>露出誤差</dt><dd>' + fmtSigned(plErr) + ' 段（' + plLabel + '）</dd>';
      html += '</dl>';
    }
    out.innerHTML = html;
  }
  document.getElementById('nd-calc-btn').addEventListener('click', calc);
  var ssEl = document.getElementById('nd-ss');
  ssEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); calc(); }
  });
  var evEl = document.getElementById('nd-ev');
  evEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); calc(); }
  });
  document.getElementById('nd-fps').addEventListener('change', calc);
  calc();
})();
</script>

### 使い方

1. 撮影モードをManualにし、ISO 100を固定する
2. 撮影シーンに対し、SSを手動で動かして露出メーターが0になる値を読む（EV0起点。ツールのEV欄の既定値0と整合）
3. そのSS値、撮影フレームレート、目的の露出補正をツールに入力し、推奨フィルターを装着する
4. SSを180度ルールの目標値（60fpsなら1/120など）に変更して本撮影する

## これは何か？

DJI Avata 2やAir 3Sには絞りがなく、露出はシャッタースピードとISOしか調整できません。シネマティック撮影では180度ルール（シャッタースピード = 1/(2 × フレームレート)）に従ってシャッタースピードを固定し、ISOも100に張り付けたいので、明るい屋外では物理的に減光するNDフィルターが必須になります。

[前回のシネマティック設定ガイド](/blog/2026/04/dji-avata2-cinematic/)では撮影環境（曇天・晴天など）から大まかな目安を表で示しました。実際の現場ではこの目安だけでは判断に迷うことがあります。たとえば「薄雲がかかった晴天」や「日陰と日向の中間」のように、目安表で隣り合うND同士のどちらを選ぶべきか曖昧な場面です。

そこで本ツールでは、機体のオートシャッタースピードで実測したSS値からNDを逆算し推奨フィルターを提示します。

私は、Avata 2はレンズ保護も兼ねて常時何らかのフィルターを装着する運用にしているため、[K&F CONCEPT DJI Avata 2 用 NDフィルター セット(ND8、ND16、ND32、ND64)](https://amzn.to/4uOAAr0)に加え、[PLフィルター](https://amzn.to/4uVFJxk)も用意しておき、減光が1〜2段で足りる明るすぎないシーンではPLフィルターを装着します。本記事のツールもこの組み合わせを前提に推奨を返します。

## 計算の手順と式

ツールは入力された3値（実測SS、フレームレート、目的EV補正）から、次の手順で推奨フィルターを決定しています。

1. **実測SSを分母値に変換**: `1/2000`、`2000`、`0.0005` のいずれの形式も同じ2000として解釈する
2. **目標SS分母を算出**: 180度ルールにより `2 × fps`（60fpsなら120、24fpsなら48）
3. **必要減衰量（段数）を計算**: `log2(実測SS分母 ÷ 目標SS分母) − 目的EV`
4. **必要段数から推奨フィルターを決める**:
    - `必要段数 < 2.25`: PLフィルター（実効約1.5段）
    - `2.25 ≤ 必要段数 ≤ 6.5`: `round(必要段数)` を3〜6にクランプし `2^round` を選ぶ（ND8 / ND16 / ND32 / ND64）。境界2.25と6.5でも所持外（ND4 / ND128）にならない
    - `必要段数 > 6.5`: ND64でも足りないため警告
5. **露出誤差を算出**: `必要段数 − 適用段数`（正値=明るめ、負値=暗め）

数式としてまとめると次のようになります。

```text
必要段数 = log2(実測SSの分母 ÷ 目標SSの分母) − 目的EV
推奨ND値 = 2 ^ round(必要段数)  (2.25 ≤ 必要段数 ≤ 6.5 のとき)
露出誤差 = 必要段数 − 適用段数
```

ステップ4で `round` を使っているのは、隣接する2つのフィルターの中間に落ちたとき**濃いほうのフィルター**を選ぶためです（JavaScriptの `Math.round` は0.5を大きい側に丸めます）。

濃いほうを選んで画像が暗めに転んだ場合、明るさを足す手段は限られます。180度ルールでSSは固定、機体に絞りもないため、選択肢はISOを1段上げる（たとえば100 → 200）かグレーディングで持ち上げるかのほぼ二択です。ISOを上げると1/1.3インチの小型センサーではノイズが乗りますが、ハイライトを飛ばすと完全には取り戻せないことを考えれば、明側に外して白飛びさせるよりは暗側に外したほうが安全側だと判断しています。

なお、Air 3Sのワイド側（24mm, F1.8）とテレ側（70mm, F2.8）は約1.3段の明るさ差があります。本ツールはどちらのレンズで測ったかを区別しないため、ワイド側で測ったSSを入力した場合、テレ側で実際に使うNDは推奨値より1段薄めに見積もるのが安全です。

## 露出補正（EV）の扱い

D-Log MにおけるEV補正の扱いについて、コミュニティでも一致した「定番値」は存在しません。共通しているのは「ハイライトをクリップさせない」という原則のみで、具体的なEV値は撮影者やシーンで分かれます。

- **EV0 起点でゼブラ/ヒストグラムを監視**: 最も無難な定石。空がフレームインしたらゼブラで白飛びを確認し、必要に応じてSS（撮影前なら）またはNDを濃いほうへ振る。
- **ETTR で +0.3〜+0.7**: シャドウSN比を稼ぐ派。クリップ手前まで露出を上げてグレーディングで戻す。
- **アンダーに振る派は少数**: D-Log Mのアンダー耐性が弱く、シャドウを持ち上げるとノイズが目立つため、暗め寄りに固定する運用は推奨されない。

計算式は「測定したときのEV値 = 最終的に得たいEV値」であれば変わりません。EV0で測りながら最終露出だけ別のEVにしたい場合（たとえばETTRで +0.3にしたい）は、ツールの「目的露出補正」欄に差分を入れてください。ツール側の既定値はEV0にしています。

## 使用上の注意点

- **K&FのND/PLセットはNDとPLの複合タイプ**である。ND値の表記にPLの減衰も含まれており、メーカー仕様の表記に従った使用で、PL分を別途加算する必要がない。
- **本ツールではPLフィルターを約1.5段の「弱いND」として扱う**。偏光効果（空・水面の反射抑制など）は本ツールのスコープ外である。
- **必要段数がND64/PL（6段）を超える場合**は警告が出る。現場で取れる対応は次の3つである。
    - **光量変化や撮影位置の変更を待つ／変える**: 日陰へ移すか、アングルを変える。
    - **露出補正をマイナス方向に振る**: 目的EVを -1程度まで下げて必要段数を減らす。グレーディングで持ち上げる前提だが、D-Log Mはアンダー耐性が弱いためシャドウノイズの代償がある。
    - **180度ルールを崩して SS を上げる**: モーションブラーが減ってシネマティックな質感は失われるが、撮影自体は成立する。
- **Avata 2の4K/100fps は画角がクロップ**される。私は通常飛行では使わず、本ツールも60fpsを既定値にしている。

[K&F ConceptのDJI Avata 2用フィルターセット](https://amzn.to/4mT7jZv)は前回の記事で紹介したものをそのまま使っています。[PLフィルター](https://amzn.to/4uVFJxk)も同社のものを別途追加しています。
