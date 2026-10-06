+++
title = "Logic ProのAIFファイルをラウドネス正規化してFLACに変換するスクリプト"
description = """
Logic Proでバウンスした音声ファイルをFLACに変換する際、
ffmpegのloudnormフィルタによる2パス処理を自動化する
Bashスクリプトを作成しました。測定と適用を一度のコマンドで
完結させ、手作業を排除して作業効率を大幅に向上させます。
"""
date = 2026-01-14
updated = 2026-10-06

[taxonomies]
tags = ["Tech", "CLI"]
[extra]
social_media_card = "ogp.webp"
+++

<!-- textlint-disable -->

{{< admonition type="info" text="この記事の公開後、Waves L4 Ultramaximizerでマスタリングするようになり、現在はこのスクリプトを使っていません。理由と、それでもこのスクリプトが役に立つ場面を末尾の追記にまとめました。" />}}

<!-- textlint-enable -->

## 背景

Logic Proでバウンスした音声ファイル(Aiff)をFLACに変換する際、適切な音量に正規化する必要があります。ffmpegの`loudnorm`フィルタを使うと高品質なラウドネス正規化が可能ですが、最良の結果を得るには2パス処理が推奨されます。

この2パス処理は以下のような手順です。

1. 1回目の実行で音声のラウドネス値を測定
2. 測定された値を確認し、手動で2回目のコマンドにコピー
3. 2回目の実行で測定値を使用して正規化を適用

毎回この作業を手動で行うのは面倒なので、自動化するスクリプトを作成しました。

## スクリプトの内容

以下は公開後に改訂したコードです。改訂の内容は末尾の追記にまとめました。[Gist](https://gist.github.com/yostos/004e57e4a905f933e227aa183e3a8fec)でも公開しています。

```bash,name=aif2flac.sh
#!/bin/bash

# Script to convert AIF files to FLAC
# By default, performs pure format conversion without any audio processing,
# then verifies that the FLAC decodes back to bit-identical PCM.
# Use -n/--normalize to apply EBU R128 loudness normalization; that mode
# refuses to run unless it can be done as a pure gain change (linear mode).
#
# Copyright (c) 2026 yostos
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

set -e

VERBOSE=false
NORMALIZE=false
VERIFY=true
ALLOW_DYNAMIC=false

# Loudness targets. Used for BOTH the measurement pass and the encoding pass;
# they must match, otherwise loudnorm's target_offset is computed against a
# different target than the one actually applied.
TARGET_I=-14
TARGET_TP=-1
TARGET_LRA=11

usage() {
    echo "Usage: $0 [-v|--verbose] [-n|--normalize] [--no-verify] [--allow-dynamic] <input_file.aif>"
}

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -n|--normalize)
            NORMALIZE=true
            shift
            ;;
        --no-verify)
            VERIFY=false
            shift
            ;;
        --allow-dynamic)
            ALLOW_DYNAMIC=true
            shift
            ;;
        -h|--help)
            usage
            echo ""
            echo "Options:"
            echo "  -v, --verbose      Show detailed ffmpeg output"
            echo "  -n, --normalize    Apply EBU R128 loudness normalization (two-pass)"
            echo "      --no-verify    Skip the bit-exactness check in conversion mode"
            echo "      --allow-dynamic  Permit loudnorm's dynamic mode (alters dynamics)"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "By default, performs pure format conversion (AIF -> FLAC) without"
            echo "any audio processing, and verifies the result is bit-identical to"
            echo "the source. Use -n to apply loudness normalization."
            echo ""
            echo "Normalization is only performed when loudnorm can run in linear"
            echo "mode (a single constant gain). If the requested target cannot be"
            echo "reached without compression/limiting, the script aborts instead of"
            echo "silently degrading the audio. Use --allow-dynamic to override."
            exit 0
            ;;
        -*)
            echo "Error: Unknown option $1"
            usage
            exit 1
            ;;
        *)
            INPUT_FILE="$1"
            shift
            ;;
    esac
done

if [ -z "$INPUT_FILE" ]; then
    usage
    echo "Use -h or --help for more information"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found"
    exit 1
fi

# Generate output filename (change extension to .flac)
OUTPUT_FILE="${INPUT_FILE%.*}.flac"

# Run ffmpeg, capturing output so errors can be reported.
# NOTE: `set -e` aborts the shell on a failing command substitution before the
# next line runs, so $? must be captured with `set +e` around the assignment.
FFMPEG_OUTPUT=""
FFMPEG_EXIT_CODE=0
run_ffmpeg() {
    if [ "$VERBOSE" = true ]; then
        # Tee to a temp file so the output is still available for the
        # post-encode checks below while being shown live.
        local tmplog
        tmplog=$(mktemp)
        set +e
        ffmpeg "$@" 2>&1 | tee "$tmplog"
        FFMPEG_EXIT_CODE=${PIPESTATUS[0]}
        set -e
        FFMPEG_OUTPUT=$(cat "$tmplog")
        rm -f "$tmplog"
    else
        set +e
        FFMPEG_OUTPUT=$(ffmpeg -hide_banner "$@" 2>&1)
        FFMPEG_EXIT_CODE=$?
        set -e
    fi
    if [ $FFMPEG_EXIT_CODE -ne 0 ]; then
        echo "Error during encoding (exit code: $FFMPEG_EXIT_CODE)"
        [ -n "$FFMPEG_OUTPUT" ] && echo "$FFMPEG_OUTPUT"
        exit 1
    fi
}

# Decode both files to a common 32-bit format and compare hashes.
# `-f md5` alone defaults to pcm_s16le, which would compare only the top 16
# bits and report a false match, so the codec must be pinned explicitly.
verify_lossless() {
    local src="$1" dst="$2" a b
    echo "=== Verifying bit-exactness... ==="
    set +e
    a=$(ffmpeg -v error -i "$src" -c:a pcm_s32le -f md5 -)
    local rc_a=$?
    b=$(ffmpeg -v error -i "$dst" -c:a pcm_s32le -f md5 -)
    local rc_b=$?
    set -e
    if [ $rc_a -ne 0 ] || [ $rc_b -ne 0 ]; then
        echo "Error: verification failed to decode one of the files"
        exit 1
    fi
    if [ "$a" = "$b" ]; then
        echo "  OK: output is bit-identical to the source (${a#MD5=})"
    else
        echo "  FAILED: output does NOT match the source"
        echo "    source: ${a#MD5=}"
        echo "    output: ${b#MD5=}"
        echo "  The FLAC encoder supports 16- and 24-bit only; a 32-bit float"
        echo "  source cannot be stored losslessly and will fail this check."
        exit 1
    fi
    echo
}

if [ "$NORMALIZE" = true ]; then
    # === Loudness normalization mode (two-pass) ===

    # Detect input sample rate so it is preserved through the loudnorm filter.
    # loudnorm operates internally at 192kHz in dynamic mode and would
    # otherwise force the output to 192kHz, so pin the output rate explicitly.
    INPUT_SR=$(ffprobe -v error -select_streams a:0 \
        -show_entries stream=sample_rate -of csv=p=0 "$INPUT_FILE")
    if [ -z "$INPUT_SR" ]; then
        echo "Error: Could not determine input sample rate"
        exit 1
    fi

    echo "=== Step 1: Measuring loudness... ==="
    echo

    # Measure with the same targets used for encoding.
    LOUDNESS_JSON=$(ffmpeg -i "$INPUT_FILE" \
        -af "loudnorm=I=$TARGET_I:TP=$TARGET_TP:LRA=$TARGET_LRA:print_format=json" \
        -f null - 2>&1 | grep -A 12 "Parsed_loudnorm")

    # Extract required values from JSON
    MEASURED_I=$(echo "$LOUDNESS_JSON" | grep '"input_i"' | awk -F'"' '{print $4}')
    MEASURED_TP=$(echo "$LOUDNESS_JSON" | grep '"input_tp"' | awk -F'"' '{print $4}')
    MEASURED_LRA=$(echo "$LOUDNESS_JSON" | grep '"input_lra"' | awk -F'"' '{print $4}')
    MEASURED_THRESH=$(echo "$LOUDNESS_JSON" | grep '"input_thresh"' | awk -F'"' '{print $4}')
    TARGET_OFFSET=$(echo "$LOUDNESS_JSON" | grep '"target_offset"' | awk -F'"' '{print $4}')

    if [ -z "$MEASURED_I" ] || [ -z "$MEASURED_TP" ] || \
       [ -z "$MEASURED_LRA" ] || [ -z "$MEASURED_THRESH" ]; then
        echo "Error: Could not parse loudnorm measurement output"
        exit 1
    fi

    echo "Measurement results:"
    echo "  Input Integrated: $MEASURED_I LUFS"
    echo "  Input True Peak:  $MEASURED_TP dBTP"
    echo "  Input LRA:        $MEASURED_LRA LU"
    echo "  Input Threshold:  $MEASURED_THRESH LUFS"
    echo "  Target Offset:    $TARGET_OFFSET LU"
    echo

    # Predict whether loudnorm can stay in linear mode (constant gain, no
    # compression, no limiting, no 192kHz resample round-trip). It falls back
    # to dynamic mode when the gain would push the true peak past the ceiling,
    # when the threshold is unmeasurable, or when measured_LRA is exactly 0
    # (loudnorm reads 0 as "not supplied" and disables linear mode).
    LINEAR_CHECK=$(awk -v i="$MEASURED_I" -v tp="$MEASURED_TP" \
                       -v lra="$MEASURED_LRA" -v th="$MEASURED_THRESH" \
                       -v ti="$TARGET_I" -v ttp="$TARGET_TP" 'BEGIN {
        offset_tp = tp + (ti - i);
        max_i     = ti - (offset_tp - ttp);
        ok = (lra > 0) && (th > -70) && (offset_tp <= ttp);
        printf "%d %.2f %.2f", ok, offset_tp, max_i;
    }')
    LINEAR_OK=$(echo "$LINEAR_CHECK" | awk '{print $1}')
    PREDICTED_TP=$(echo "$LINEAR_CHECK" | awk '{print $2}')
    MAX_LINEAR_I=$(echo "$LINEAR_CHECK" | awk '{print $3}')

    if [ "$LINEAR_OK" != "1" ] && [ "$ALLOW_DYNAMIC" != true ]; then
        echo "Error: this file cannot be normalized to $TARGET_I LUFS by gain alone."
        if awk -v l="$MEASURED_LRA" 'BEGIN {exit !(l <= 0)}'; then
            echo "  Measured LRA is 0.00 LU, which loudnorm treats as unset and"
            echo "  which forces its dynamic (compressing) mode."
        elif awk -v t="$MEASURED_THRESH" 'BEGIN {exit !(t <= -70)}'; then
            echo "  Measured threshold ($MEASURED_THRESH LUFS) is too low to measure reliably."
        else
            echo "  The required gain would raise true peak to $PREDICTED_TP dBTP,"
            echo "  above the $TARGET_TP dBTP ceiling, so loudnorm would silently switch"
            echo "  to its dynamic mode and apply compression and limiting."
            echo "  The loudest linear-safe target for this file is $MAX_LINEAR_I LUFS."
        fi
        echo "  Aborting to leave the master untouched."
        echo "  Convert without -n, or pass --allow-dynamic to override."
        exit 1
    fi

    if [ "$LINEAR_OK" = "1" ]; then
        echo "Linear (gain-only) normalization is possible; predicted output true peak: $PREDICTED_TP dBTP"
    else
        echo "WARNING: --allow-dynamic given; loudnorm will compress and limit this file."
    fi
    echo

    echo "=== Step 2: Encoding to FLAC with normalization... ==="
    echo

    # Encode to FLAC using measured values.
    # Note: in linear mode loudnorm ignores `offset` and recomputes it from the
    # measured values; it is passed for the --allow-dynamic path.
    run_ffmpeg -y -i "$INPUT_FILE" \
        -af "loudnorm=I=$TARGET_I:TP=$TARGET_TP:LRA=$TARGET_LRA:measured_I=$MEASURED_I:measured_TP=$MEASURED_TP:measured_LRA=$MEASURED_LRA:measured_thresh=$MEASURED_THRESH:offset=$TARGET_OFFSET:linear=true:print_format=summary" \
        -ar "$INPUT_SR" -c:a flac -compression_level 8 "$OUTPUT_FILE"

    if [ "$VERBOSE" != true ]; then
        echo "$FFMPEG_OUTPUT" | grep -A 15 "Input Integrated:" | grep -v "^\[" | grep -v "^$" || true
        echo
    fi

    # Confirm loudnorm actually stayed linear; it downgrades silently.
    if echo "$FFMPEG_OUTPUT" | grep -q "Normalization Type:[[:space:]]*Dynamic"; then
        if [ "$ALLOW_DYNAMIC" != true ]; then
            echo "Error: loudnorm fell back to dynamic mode despite the pre-flight check."
            echo "  The output has been compressed and limited; removing it."
            rm -f "$OUTPUT_FILE"
            exit 1
        fi
        echo "WARNING: dynamic mode was used; dynamics have been altered."
    fi
else
    # === Pure conversion mode (default) ===
    echo "=== Converting to FLAC... ==="
    echo

    # No filters and no -sample_fmt: ffmpeg carries 16-bit through as 16-bit
    # and 24-bit through as 24-bit. -compression_level only trades encode time
    # for file size; the decoded samples are identical at every level.
    run_ffmpeg -y -i "$INPUT_FILE" -c:a flac -compression_level 8 "$OUTPUT_FILE"

    if [ "$VERIFY" = true ]; then
        echo
        verify_lossless "$INPUT_FILE" "$OUTPUT_FILE"
    fi
fi

echo
echo "=== Completed ==="
echo "Output file: $OUTPUT_FILE"

# Display file sizes
if command -v du &> /dev/null; then
    INPUT_SIZE=$(du -h "$INPUT_FILE" | awk '{print $1}')
    OUTPUT_SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
    echo "Input file:  $INPUT_SIZE"
    echo "Output file: $OUTPUT_SIZE"
fi
```

## 使い方

AIFファイルのパスを引数に指定して実行します。オプションを付けなければ、ラウドネスには手を加えずFLACに変換し、変換後の音声が元のファイルとビット単位で一致するかを検証します。

```bash
./aif2flac.sh input.aif
```

ラウドネス正規化をする場合は`-n`オプションを付けます。

```bash
./aif2flac.sh -n input.aif
```

ほかのオプションは次のとおりです。出力ファイルは同じディレクトリに`.flac`拡張子で保存されます。

- `-v`: ffmpegの詳細な出力を表示する
- `--no-verify`: 変換後の一致検証を省く
- `--allow-dynamic`: `loudnorm`のダイナミックモードでの処理を許可する（音のダイナミクスが変わる）

## loudnormフィルタについて

ffmpegの`loudnorm`フィルタは、EBU R128規格に基づいたラウドネス正規化を行うためのフィルタです。単純な音量の増減ではなく、人間の聴覚特性を考慮した知覚的な音量の均一化を実現します。

このスクリプトでは以下のパラメータを使用しています。

- `I=-14`: 目標のIntegrated Loudness（LUFS単位）
- `TP=-1`: True Peak値の上限（dBTP単位）
- `LRA=11`: Loudness Range（LU単位）

`I=-14 LUFS`は、Spotify、YouTube Music、Apple Musicなどの主要なストリーミングサービスが採用している標準的なラウドネス基準です。世間一般で広く使われているこの基準を参考にすることで、適切な音量バランスを保つことができます。

1パス処理では入力音声の特性を考慮せずに正規化するため、音質劣化の可能性があります。2パス処理では、1回目で測定した入力音声の実際の値を2回目の処理に使用することで、より正確で高品質な正規化が可能になります。

## まとめ

Logic Proから書き出した音声ファイルをFLACに変換する際の2パス処理を自動化することで、手動でパラメータをコピーする手間がなくなり、作業効率が大幅に向上しました。

今後は、複数ファイルの一括処理や、ターゲットラウドネス値のカスタマイズなどの機能を追加するかもしれません。

## 追記: L4 Ultramaximizer導入後にこのスクリプトをやめた理由と残る価値

この記事を書いた後、Logic ProのマスターにWaves L4 Ultramaximizerを入れ、ラウドネスとLRAをマスタリングの段階で作り込むようになりました。そうなると、このスクリプトがやっていることは「最終的に音量を-14 LUFSに合わせる一律のゲイン調整」だけになり、LRAの調整としてはほぼ意味がありません。場合によっては、マスタリングの結果を壊すおそれもあります。

理由は`loudnorm`の動作にあります。2パスで`linear=true`を指定した場合、次の2つの条件を両方満たすときだけ、単純な一律ゲイン変更（線形モード）になります。

- 入力のLRAが指定値（`LRA=11`）以下である
- ゲインを変えた後のTrue Peakが-1 dBTP以下に収まる

L4で仕上げた音源ならLRAはたいてい11 LU以下なので、`LRA=11`は条件の判定に使われるだけで、LRAそのものは変わりません。一方で条件を満たさない場合、`loudnorm`は何も言わずにダイナミックモードへ切り替わり、独自のコンプレッションとリミッティングをかけます。これはL4での作業と二重処理になります。

そのため現在は、ラウドネスには手を加えず、形式だけを変換しています。FLACは可逆圧縮なので、L4で仕上げた結果がそのまま残ります。

```bash
ffmpeg -i xxxx.aiff -c:a flac -compression_level 8 xxxx.flac
```

マスタリング済みの音源に使う理由はなくなりましたが、このスクリプトの価値がまったくなくなったわけではありません。次のような場面では今でも役に立ちます。

- リミッターを通していないバウンスやラフミックスを、手早く-14 LUFS前後にそろえたいとき
- 形式変換の結果が元の音声とビット単位で一致するかを確かめたいとき
- `loudnorm`の2パス処理を自動化する方法の例として参照したいとき

なお、スクリプトは公開後に次のように改訂しています。記事中のコードは改訂後のものです。

- 既定ではラウドネス正規化をせず、形式だけを変換する。変換後は、元のファイルとFLACをそれぞれデコードしたPCMのハッシュを比べ、ビット単位で一致するかを検証する
- 正規化は`-n`を付けたときだけ行う。測定値から線形モードで処理できないと見込んだ場合は、出力を作らずに中止する
- 正規化の後、サマリーの`Normalization Type`が`Dynamic`になっていれば、出力ファイルを削除してエラーで終了する
- 出力のサンプルレートを`-ar`で入力と同じ値に固定する。ダイナミックモードでは出力が192 kHzにアップサンプリングされるため
- FLACの圧縮レベルを最大の8にする。圧縮レベルで変わるのはエンコード時間とファイルサイズだけで、デコードした音声は同じになる
