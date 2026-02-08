# OGP画像自動生成スクリプト 実装記録

## 概要

記事ごとにOGP画像（`ogp.webp`）を自動生成するNode.jsスクリプトを実装した。

## 最終仕様

| 項目 | 内容 |
|------|------|
| 出力ファイル名 | `ogp.webp` |
| 出力先 | 各記事ディレクトリ（`content/blog/YYYY/MM/slug/`） |
| 画像サイズ | 1200×630px |
| 画像フォーマット | WebP（quality: 85） |
| 画像選択ロジック | 記事フォルダ内の最大ファイルサイズの画像 |
| サイズ基準 | 1200×630未満ならデフォルト画像を使用 |
| 既存ogp.webp | スキップ（`--force`で上書き可能） |
| デフォルト画像 | `static/images/coded-chords.webp` |
| フォント | ローカルフォント（`scripts/fonts/`に配置、gitignore対象） |

## オーバーレイ仕様

すべてのOGP画像に以下の情報をオーバーレイする：

```
┌─────────────────────────────────────────────────┐
│  Coded Chords                                   │  ← 左上（ブログ名）
│                                                 │
│                                                 │
│  ┌───────────────────────────────────────┐      │
│  │  記事タイトル                         │      │  ← 下部（半透明背景）
│  │  （複数行対応）                       │      │
│  └───────────────────────────────────────┘      │
│                          Toshiyuki Yoshida      │  ← 右下（著者名）
└─────────────────────────────────────────────────┘
```

- **ブログ名**: 白文字、28px、太字、ドロップシャドウ
- **タイトル**: 白文字、42px、半透明黒背景ボックス（rgba(0,0,0,0.6)）
- **著者名**: 白文字、24px、opacity 0.9、ドロップシャドウ

---

## 実装ステップ詳細

### Step 1: 依存パッケージのインストール

```bash
npm install -D sharp satori gray-matter glob @resvg/resvg-js
```

**結果**: 41パッケージ追加。後にgray-matterは使用せず（下記参照）。

---

### Step 2: フォントの配置

Google FontsからNoto Sans JP（Regular）をダウンロードし、
`scripts/fonts/NotoSansCJKjp-Regular.otf`（16MB）として配置。

**後の変更**: ユーザーがカドマ-R.otf（有償フォント）に置き換え。
スクリプトは任意の.ttf/.otfファイルを自動検出するよう修正。

---

### Step 3: scripts/generate-ogp.mjs 作成

メインの生成スクリプトを作成。

**機能**:
- `content/blog/**/**/index.md`を全取得
- 各記事のfrontmatterからタイトルを抽出
- 記事内の画像から最大サイズを選択
- 1200×630以上なら記事画像を使用、未満ならデフォルト画像を使用
- satoriでSVGオーバーレイを生成、sharpで合成

---

### Step 4: scripts/ogp-template.mjs 作成

satori用のJSX-likeテンプレートを作成。

---

### Step 5: package.json にスクリプト追加

```json
{
  "scripts": {
    "ogp": "node scripts/generate-ogp.mjs",
    "ogp:dry-run": "node scripts/generate-ogp.mjs --dry-run"
  }
}
```

---

### Step 6: 動作確認（dry-run）

```bash
npm run ogp:dry-run
```

**結果**: 236記事を確認。画像使用=59、デフォルト=177、エラー=0。

---

### Step 7: 一括実行

```bash
npm run ogp
```

**最終結果**: 画像使用=60、デフォルト=176、エラー=0。

---

### Step 8: frontmatter更新

`scripts/add-ogp-frontmatter.mjs`を作成し、全記事に以下を追加：

```toml
[extra]
social_media_card = "ogp.webp"
```

**結果**: 236記事すべて更新完了。

---

### Step 9: CLAUDE.md更新

新規記事テンプレートにOGP設定を追記、
Common Commandsに`npm run ogp`を追加。

---

## 発生した問題と解決策

### 問題1: TOML日付パースエラー

**症状**:
```
Expected "T" but "\n" found at line X
```

**原因**:
Zolaのfrontmatterは`date = 2024-12-25`形式を使用するが、
厳密なTOMLパーサーは`date = 2024-12-25T00:00:00`を期待する。

**解決策**:
gray-matter + tomlパーサーの使用を断念し、
正規表現でtitleフィールドのみを抽出する方式に変更。

```javascript
// +++で囲まれたfrontmatter部分を抽出
const fmMatch = content.match(/^\+\+\+\n([\s\S]*?)\n\+\+\+/);
// title = "..." を抽出
const match = frontmatter.match(/^title\s*=\s*"([^"]*)"/m);
```

---

### 問題2: エスケープされた引用符の処理

**症状**:
`title = "Movie \"Under Ninja\""`のようなタイトルが
`Movie `で切れてしまう。

**原因**:
正規表現`/^title\s*=\s*"([^"]*)"/m`がエスケープを考慮していない。

**解決策**:
エスケープシーケンスを考慮した正規表現に修正：

```javascript
const doubleQuoteMatch = frontmatter.match(/^title\s*=\s*"((?:[^"\\]|\\.)*)"/m);
if (doubleQuoteMatch) {
  return doubleQuoteMatch[1].replace(/\\"/g, '"');
}
```

---

### 問題3: satori display:flexエラー

**症状**:
```
Expected <div> to have explicit "display: flex" set
```

**原因**:
satoriは複数の子要素を持つdivに明示的な`display: flex`が必要。

**解決策**:
テンプレート内のすべての親divに`display: 'flex'`を追加。

---

### 問題4: メモリ不足

**症状**:
```
FATAL ERROR: Reached heap limit Allocation failed -
JavaScript heap out of memory
```

**原因**:
フォントファイル（16MB）を各記事ごとにロードしていた。
236記事 × 16MB = 3.7GB以上のメモリ消費。

**解決策**:
フォントをmain()で一度だけロードし、
各関数にパラメータとして渡すよう修正。

```javascript
// 修正前（各記事でロード）
async function createOgpWithOverlay(title, outputPath) {
  const fontData = await fs.readFile(fontPath);  // ← 毎回16MB読込
  ...
}

// 修正後（事前に一度だけロード）
async function main() {
  const fontData = await fs.readFile(fontPath);  // ← 一度だけ
  for (const articleDir of articleDirs) {
    await createOgpWithOverlay(title, ogpPath, fontData);
  }
}
```

---

### 問題5: 記事画像にオーバーレイがない

**症状**:
記事に画像がある場合、画像がそのままリサイズされるだけで
タイトルなどのオーバーレイがない。

**原因**:
当初の仕様では「記事画像はリサイズのみ」と解釈していた。

**解決策**:
ユーザーの要望により、記事画像使用時も
デフォルト画像と同様のオーバーレイを適用するよう修正。

```javascript
async function createOgpFromImage(imagePath, outputPath, title, fontData) {
  // オーバーレイSVGを生成
  const template = createOverlayTemplate({
    title,
    author: DEFAULT_AUTHOR,
    blogName: BLOG_NAME,
  });
  const svg = await satori(template, { ... });
  const overlayPng = resvg.render().asPng();

  // 元画像にオーバーレイを合成
  await sharp(imagePath)
    .resize(OGP_WIDTH, OGP_HEIGHT, { fit: 'cover' })
    .composite([{ input: overlayPng, top: 0, left: 0 }])
    .webp({ quality: 85 })
    .toFile(outputPath);
}
```

---

### 問題6: ブログ名の追加

**症状**:
オーバーレイにブログ名「Coded Chords」が含まれていない。

**解決策**:
テンプレートにブログ名を左上に表示するよう追加。
`ogp-template.mjs`に`BLOG_NAME`定数を追加し、
テンプレート内で使用。

---

### 問題7: フォントファイルの管理

**症状**:
ユーザーがNoto Sans JPを有償フォント（カドマ-R.otf）に置き換えたが、
スクリプトが`NotoSansJP-Regular.ttf`を探してエラー。

**解決策**:
1. フォントファイル名をハードコードせず、
   `scripts/fonts/`内の`.ttf`または`.otf`を自動検出：

```javascript
async function findFontFile() {
  const files = await fs.readdir(FONTS_DIR);
  const fontFile = files.find((f) =>
    FONT_EXTENSIONS.includes(path.extname(f).toLowerCase())
  );
  if (!fontFile) {
    throw new Error(
      `フォントが見つかりません。scripts/fonts/ に .ttf または .otf を配置してください。`
    );
  }
  return path.join(FONTS_DIR, fontFile);
}
```

2. `scripts/fonts/`を`.gitignore`に追加し、
   有償フォントがリポジトリにコミットされないようにした：

```gitignore
# OGP generation fonts (use local fonts)
scripts/fonts/
```

---

## 最終ファイル構成

```
scripts/
  generate-ogp.mjs       # メインスクリプト（342行）
  ogp-template.mjs       # オーバーレイテンプレート（120行）
  add-ogp-frontmatter.mjs # frontmatter更新スクリプト（80行）
  fonts/                 # フォント配置ディレクトリ（gitignore対象）
    *.ttf or *.otf       # 任意の日本語フォント
```

---

## 運用方法

### 初回セットアップ（新規環境）

1. 依存パッケージのインストール：
   ```bash
   npm install
   ```

2. 日本語フォントを配置：
   ```bash
   # scripts/fonts/ に .ttf または .otf ファイルを配置
   # 例: Noto Sans JP, カドマ, 源ノ角ゴシック等
   ```

### 通常運用

```bash
# 新規記事のOGP画像を生成（既存はスキップ）
npm run ogp

# 対象確認のみ（実際には生成しない）
npm run ogp:dry-run

# 全記事を強制再生成
npm run ogp --force
```

### 新規記事作成時

1. 記事を作成（`content/blog/YYYY/MM/slug/index.md`）
2. frontmatterに以下を追加：
   ```toml
   [extra]
   social_media_card = "ogp.webp"
   ```
3. `npm run ogp`を実行

---

## 依存パッケージ

```json
{
  "devDependencies": {
    "@resvg/resvg-js": "^2.6.2",
    "glob": "^11.0.1",
    "satori": "^0.12.1",
    "sharp": "^0.33.5"
  }
}
```

---

## 参考情報

- **satori**: Vercel製のSVG生成ライブラリ。JSX-likeオブジェクトからSVGを生成。
- **sharp**: 高速な画像処理ライブラリ。リサイズ、合成、形式変換に使用。
- **@resvg/resvg-js**: Rust製SVGレンダラー。SVGをPNGに変換。
- **Zola**: Rust製静的サイトジェネレーター。TOMLフロントマターを使用。
