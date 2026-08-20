# OGP画像自動生成ツール

## 概要

記事ごとにOGP画像（`ogp.webp`）を自動生成するNode.jsスクリプト。
テンプレート画像の上に記事タイトル・タグをオーバーレイして合成する。

## 出力仕様

| 項目 | 値 |
|------|-----|
| ファイル名 | `ogp.webp` |
| 出力先 | 各記事ディレクトリ（`content/blog/YYYY/MM/slug/`） |
| サイズ | 1200×630px |
| フォーマット | WebP（quality: 85） |

## テンプレート画像

すべてのOGP画像は固定のテンプレート画像を背景として使用する。

- パス: `scripts/images/ogp-template.png`（1200×630px）
- テンプレートに含まれる固定要素（スクリプトでは描画しない）:
  - 上下の水色ライン
  - 左下: Blueskyアイコン + 著者名
  - 右下: Coded Chordsロゴ + URL
- 記事個別の画像（cover.webp等）は背景に使用しない

## オーバーレイレイアウト

スクリプトが描画するのはタイトルとタグのみ。
テンプレート上部の白い余白エリアに配置する。

```
┌═══════════════════════════════════════════════════┐  テンプレート固定: 水色ライン
│                                                   │
│  記事タイトル                                      │  ← オーバーレイ（上端 80px、左端 60px）
│  （最大3行、折り返し対応）                          │
│                                                   │
│  #tag1  #tag2  #tag3  #tag4                       │  ← オーバーレイ（タイトル下 20px）
│                                                   │
│                                                   │
│  [BSky] TOSHIYUKI YOSHIDA    [Logo] codedchords   │  テンプレート固定: 著者名・ロゴ
└═══════════════════════════════════════════════════┘  テンプレート固定: 水色ライン
```

### オーバーレイ要素のスタイル

| 要素 | フォント | サイズ | 色 | 備考 |
|------|---------|--------|-----|------|
| タイトル | IBMPlexSansJP-Medium | 48px | `#1a1a1a` | 行間 1.4、最大3行、左寄せ |
| タグ | BerkeleyMono-Medium | 20px | `#4a9ece` | `#` プレフィックス付き、横並び、最大4つ |

### マージン

| 項目 | 値 |
|------|-----|
| タイトル左端 | 80px |
| タイトル上端 | 100px |
| タイトル右端マージン | 80px（折り返し幅 = 1040px） |
| タグとタイトルの間 | 20px |
| タグ間のスペース | 16px |

## フォント

| フォント | 用途 | 配置ファイル名 | ライセンス |
|---------|------|--------------|----------|
| BerkeleyMono-Medium | ラテン文字・タグ | `BerkeleyMono-Medium.otf` | 有償 |
| IBMPlexSansJP-Medium | 日本語タイトル | `IBMPlexSansJP-Medium.otf` | OFL 1.1 |

IBM Plex Sans JP はラテン文字のフォールバックも兼ねる。

### 配置先とリポジトリ管理

- 配置先: `scripts/fonts/`
- **このディレクトリは `.gitignore` 対象。リポジトリに含めない**（有償フォントを含むため）
- したがって **clone しただけでは OGP 生成は動かない**。新規環境では各自でフォントを入手し、
  上表のファイル名どおりに配置する必要がある
- `generate-ogp.mjs` はファイル名を完全一致で参照するため、名前を変えてはいけない

### フォント形式の制約

satori（内部で opentype.js を使用）が読めるのは **静的な TrueType / CFF アウトライン**のみ。
次のファイルは配置しても `Font doesn't contain TrueType or CFF outlines.` で失敗する。

| 使えないもの | 理由 |
|------------|------|
| `.woff2` | satori は woff2 を解凍できない |
| バリアブルフォント（`CFF2` + `fvar`） | opentype.js が CFF2 を解釈できない |

- `static/fonts/` にある Berkeley Mono は Web 配信用の woff2 なので**流用できない**
- Berkeley Graphics が配布する `Berkeley Mono Variable.otf` は CFF2 バリアブルのため**使えない**
- どうしても woff2 しか手元にない場合は `woff2_decompress`（Homebrew の `woff2`）で
  sfnt に戻せる。出力ファイル名は機械的に `.ttf` になるが、中身が `OTTO` ヘッダの CFF なら
  `.otf` にリネームしてよい

### 入手先

**Berkeley Mono**（有償・要ライセンス購入）

Berkeley Graphics のダウンロードページから **desktop 版（OTF）** を取得する。
配布パッケージにはウェイト構成の異なる複数のバリアントがあり、
**Medium を含まないもの（Regular / Oblique / Bold / Bold-Oblique の4ウェイトのみ）がある**。
`BerkeleyMono-Medium.otf` が含まれるパッケージを選ぶこと。

**IBM Plex Sans JP**（無償・OFL 1.1）

https://github.com/IBM/plex から取得し、
`fonts/complete/otf/hinted/IBMPlexSansJP-Medium.otf` を使う。
`~/Library/Fonts` などに入っている `.ttf` 版でも satori は読めるが、
スクリプトが `.otf` の名前を要求するため OTF 版を使うのが素直。

### 検証方法

配置後、以下で読み込みを確認する。フォントに問題があればここでエラーになる。

```bash
npm run ogp:dry-run
```

## タグの取得

- frontmatter の `[taxonomies]` セクションから `tags` 配列を取得
- 最大 **4つ** まで表示（5つ以上ある場合は先頭4つを使用）
- 各タグの先頭に `#` を付与して表示

## コマンド

```bash
npm run ogp           # OGP画像を生成（既存はスキップ）
npm run ogp:dry-run   # 対象確認のみ（実際には生成しない）
npm run ogp -- --force   # 全記事を強制再生成
```

## ファイル構成

```
scripts/
  generate-ogp.mjs       # メイン生成スクリプト
  ogp-template.mjs       # satori用オーバーレイテンプレート
  images/
    ogp-template.png      # テンプレート背景画像（1200×630px）
  fonts/                  # フォント配置ディレクトリ（gitignore対象）
    BerkeleyMono-Medium.otf
    IBMPlexSansJP-Medium.otf
```

## 技術スタック

| パッケージ | 用途 |
|-----------|------|
| satori | JSX-likeオブジェクトからSVGオーバーレイを生成 |
| @resvg/resvg-js | SVGをPNGに変換（Rust製） |
| sharp | テンプレート画像との合成、WebP変換 |
| glob | 記事ディレクトリの走査 |

## 処理フロー

1. `scripts/fonts/` からフォントファイルを読み込み（1回のみ）
2. `scripts/images/ogp-template.png` をテンプレートとして読み込み
3. `content/blog/` 以下の全 `index.md` を走査
4. 各記事について:
   a. `ogp.webp` が既存ならスキップ（`--force` 時は上書き）
   b. frontmatter から `title` と `tags` を正規表現で抽出
   c. satori でオーバーレイSVGを生成（タイトル + タグ最大4つ）
   d. resvg でSVGをPNGに変換
   e. sharp でテンプレート画像にオーバーレイを合成
   f. WebP（quality: 85）で出力

## frontmatter との連携

記事の frontmatter に以下の設定が必要:

```toml
[taxonomies]
tags = ["タグ1", "タグ2"]

[extra]
social_media_card = "ogp.webp"
```

## セットアップ（新規環境）

`scripts/fonts/` は `.gitignore` 対象のため、clone 後に必ず以下の手順が必要になる。

1. `npm install`（依存パッケージのインストール）
2. `scripts/fonts/` を作成し、以下のフォントを配置（入手先は「フォント」の節を参照）
   - `BerkeleyMono-Medium.otf`
   - `IBMPlexSansJP-Medium.otf`
3. `npm run ogp:dry-run` で読み込みを確認
