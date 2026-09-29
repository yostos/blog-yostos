# Zola 0.23 / tabi v5 移行ログ

ブログ記事化を前提に、移行の判断・手順・実行結果・つまずきを時系列で記録する。

- 作業開始: 2026-09-29
- 作業ブランチ: `refactor/zola-0.23-tabi-v5`

## 1. 背景と移行前の状態

| 項目 | 移行前 | 移行後（予定） |
|---|---|---|
| Zola（ローカル, Homebrew） | 0.22.1 | 0.23.6 |
| Zola（CI: `deploy.yml`, `zola-check-scheduled.yml`） | `zola@0.22.1` | `zola@0.23.6` |
| tabi（submodule） | `2f298c3`（2026-06-26, `v4.1.0-78-g2f298c3`） | v5.0.0 以降の main |

きっかけは「tabi に更新はないか」の確認。`git -C themes/tabi fetch` の結果、
upstream main は現在の submodule から 39 コミット先に進み、`v4.2.0` と `v5.0.0` の 2 リリースが出ていた。

- `v4.2.0`（2026-09-12）: Zola 0.22 系で動く最後のリリース
- `v5.0.0`（2026-09-13）: 破壊的変更。Zola 0.23 への移行（tabi PR #705）。Zola 0.23.6 以上が必須

当初は「まず v4.2.0 に上げ、v5 は別作業」を提案したが、Zola を最新にする方針に決定。
Zola 0.23 では tabi 4.x が動かないため、Zola と tabi v5 を同時に移行する。

## 2. Zola 0.23 の変更点

出典: Zola `CHANGELOG.md`（v0.23.6 タグ）、GitHub Releases。

### 0.23.0（2026-08-05）

CHANGELOG 冒頭に「This is probably the most breaking version of Zola that will happen.」とある。

破壊的変更

- テンプレートエンジン Tera が v2 に更新（Tera 側の MIGRATION.md 参照）
- ショートコードが完全に廃止。代わりに Tera の「コンポーネント」を使う
  - Markdown 本文そのものが Tera でテンプレート処理されるようになった
  - ショートコードとマクロの区別がなくなり、テンプレートでも本文でも同じコンポーネントを使える
  - コンポーネントは衛生的（hygienic）で、明示的に渡した引数にしかアクセスできない（`lang` なども要受け渡し）
- `get_page` / `get_section` が言語コード付きパス（`some.fr.md`）を受け付けなくなった。正規パス + `lang` 引数を使う
- `native-tls` ビルド feature の削除

構文の変化

```text
# インライン（旧）
{{ youtube(id="dQw4w9WgXcQ", autoplay=true) }}
# インライン（新）
{{< youtube id="dQw4w9WgXcQ" autoplay={true} />}}

# ブロック（旧）
{% quote(author="Vincent") %}
A quote
{% end %}
# ブロック（新）
{% <quote author="Vincent"> %}
A quote
{% </quote> %}
```

新機能・その他

- `skip_content_templating`: 特定ファイルの本文テンプレート処理をスキップする設定
- `get_taxonomy_url` の `name` 引数は非推奨。`term` を使う
- `resize_image` に `filter` 引数（サンプリングフィルタ選択）
- ハイライト設定に `data_attr_position`
- シンタックスハイライトの CSS は `static` ではなく出力ディレクトリに生成される
- `reading_time` が言語ごとの読書速度を使うようになった
- セクションにもサブセクション用の `higher` / `lower`
- `@/` 内部リンクで同梱アセットを解決できる（`![](@/blog/article/img.png)`）
- page / section の `hidden` プロパティ（一覧から除外）
- テンプレートから `aliases` を参照可能
- `get_page` / `get_section` の `allow_missing` 引数
- `text_direction` Tera 関数
- `get_image_metadata` に `description` と `created`
- front matter の `include_in_feeds` で個別ページをフィードから除外
- 多言語検索インデックス設定の不整合修正（tabi 作者 welpo による PR）
- Cloudflare Workers へのデプロイ手順がドキュメントに追加

### 0.23.1〜0.23.6

- 0.23.1（08-05）: Docker イメージの証明書欠落修正
- 0.23.2（08-07）: デュアルクラス CSS 生成の修正、脚注のパーマリンク化修正、`get_env` 復活
- 0.23.3（08-11）: Windows 修正、多言語サイトの設定マージ修正、タクソノミー項が空文字に slugify されるとエラーに、elasticlunr の言語リージョン修正
- 0.23.4（08-20）: `get_url` の末尾スラッシュ不具合、sitemap `<lastmod>` の不正日付修正、日付ソートの同値判定を降順パーマリンクに、`cachebust` 結果のキャッシュ
- 0.23.5（09-11）: `date` フィルタに `locale` 引数が復活、PNG リサイズ時の黒縁修正、`get_hash` のキャッシュ、`zola serve` でテンプレート変更時にサイト全体を再ビルド
- 0.23.6（09-12）: Tera 更新で implicit params（暗黙引数）に対応。tabi v5 はこれを必須とする

## 3. tabi の変更点（現在の submodule → v5.0.0 以降）

### v4.2.0 で入った修正のうち、現在の submodule に未反映のもの

- 検索: 結果リスナーのリーク修正、2 回目以降の検索件数表示の修正
- ルートセクションのページネーションで全記事が表示される問題の修正
- OS テーマ切替時に保存済みテーマ設定を尊重
- シリーズ: 逆順ページネーション、`aria-label` の修正
- Atom フィードタイトルの `&` エスケープ
- webmentions: 内容のエスケープ・サニタイズ（セキュリティ修正）、HTML 不正の修正
- taxonomies: カスタムタクソノミー対応改善
- footnotes: バックリンクスクリプト URL 修正
- 英語以外の長い日付で月名をフル表記
- CSP: umami 接続の許可
- socials: xmpp アイコン
- KaTeX 0.18.x、mermaid 12.0.0 への更新

v4.2.0 全体の新機能（一部は v4.1.0 以降の main 経由で既に取り込み済み）: スキップリンク、GitHub 形式アラート、
ToC の UX 改善、言語ごとの日付書式、iine（いいねボタン）、日本語検索対応など。

### v5.0.0（2026-09-13）

- Zola 0.23 への移行（BREAKING）
- 後方互換のためだけに残っていた設定を廃止
  - `footnote_backlinks` → `[markdown].bottom_footnotes = true`
  - `add_src_to_code_block` → 名前付きコードフェンスと `code_block_name_links`
  - `[extra].index_format` → `[search]` と各言語の search テーブルへ
  - `translate_copyright` / `translated_copyright` → `copyright_translations`
- 日付書式は strftime（`%Y`）ではなく UTS-35 パターン（`y`）
- ハイライト設定は `[markdown.highlighting]`、`style = "class"` が必須。Zola が `giallo.css` を生成
- 移行ガイド: tabi リポジトリ `content/blog/upgrading-to-zola-0-23/index.md`

### v5.0.0 以降（main）

- taxonomies: タグ一覧を記事数順にソート（#708）
- KaTeX 0.18.9、CI の ubuntu v26

## 4. 影響範囲の調査

tabi 移行ガイドの grep コマンドで洗い出した結果。

記事本文（`content/` 配下 447 ファイル）のショートコード呼び出し

| 種別 | ショートコード | 件数 |
|---|---|---:|
| インライン | `image` | 297 |
| インライン | `youtube` | 110 |
| インライン | `linkcard` | 19 |
| インライン | `aside` | 5 |
| インライン | `secrets` | 5 |
| インライン | `remote_text` | 4 |
| インライン | `clear` | 4 |
| インライン | `border` | 1 |
| インライン | `full_width_image` | 1 |
| インライン | `multilingual_quote` | 1 |
| インライン | `spoiler` | 1 |
| インライン | `spot` | 1 |
| インライン | `steps` | 1 |
| ブロック | `references` | 63 |
| ブロック | `admonition` | 34 |
| ブロック | `aside` | 24 |
| ブロック | `mermaid` | 17 |
| ブロック | `module` | 9 |

（インライン件数は grep の `{{ name` 出現数。関数呼び出しの誤検出を含む可能性があり、変換時に再確認する）

サイト独自テンプレート（テーマ更新では直らない）

- `templates/shortcodes/`: `image.html`, `linkcard.html`, `module.html`, `spot.html`, `youtube.html` → `templates/components/` へ移植
- `templates/macros/list_posts.html` → コンポーネント化
- 上書きテンプレート: `partials/cards_pages.html`, `partials/header.html`, `partials/home_banner.html`, `partials/nav.html`, `search.html`, `tabi/extend_head.html` → Tera 2 構文へ

`config.toml`

- `long_date_format` / `short_date_format` / `archive_date_format` = `"%Y-%m-%d"` → UTS-35
- `[search]` 内の `index_format`、`[markdown.highlighting]` は既に存在。v5 の要件と照合する
- `build_search_index = false`（Pagefind を別途使用）

CI・ドキュメント・ツール

- `.github/workflows/deploy.yml`, `.github/workflows/zola-check-scheduled.yml`: `zola@0.22.1`
- `README.md`: Zola バッジ・要件が 0.22.1
- `CLAUDE.md`: 記事テンプレート（`{{ image(...) }}`, `{% references() %}`）
- `docs/tabi-shortcodes.md`、`scripts/convert-images.py`、`.claude/settings.json`、記事系スキル

## 5. 作業計画

1. 作業ブランチ作成
2. Homebrew の Zola を 0.23.6 へ
3. tabi submodule を v5.0.0 以降へ
4. 記事のショートコードをスクリプトで一括変換
5. テンプレート・config を移植、CI を更新
6. ドキュメント・ツール・スキルの記法を更新
7. `zola check` / `zola build` で検証、差分確認
8. `/blog-review` → コミット → PR

## 6. 作業ログ

各ステップで実行したコマンド・結果・つまずきを記録する。

### Step 1: 作業ブランチ作成

```bash
git checkout -b refactor/zola-0.23-tabi-v5
```

main（`992c853`）から分岐。

### Step 2: Zola を 0.23.6 へ

```bash
brew upgrade zola
zola --version   # zola 0.23.6
```

- Homebrew の stable は 0.23.6（`brew info zola`: `0.22.1 → stable 0.23.6`）
- `/opt/homebrew/Cellar/zola/` には 0.22.1 と 0.23.6 の両方が残っている（cleanup 前）
- この時点で main の旧構成はローカルでビルドできなくなる。移行完了まで記事の公開作業は止める

つまずき: Step 1〜3 を 1 つのコマンドにまとめて実行しかけ、途中で中断した。
ブランチ作成と `brew upgrade` は完了、tabi 更新は未実行の状態で止まっていた。
以降はステップごとに分けて実行し、ログを取る。

### Step 3: tabi submodule を更新

```bash
git -C themes/tabi fetch origin   # v4.2.0, v5.0.0 タグも取得
git -C themes/tabi checkout --detach origin/main
git -C themes/tabi describe --tags   # v5.0.0-3-gd09ca60
```

- `2f298c3`（v4.1.0-78）→ `d09ca60`（2026-09-24, v5.0.0 + 3 コミット）
- v5.0.0 タグではなく main 先端を採用。v5.0.0 以降はタグ一覧のソート修正と依存更新のみのため

### Step 3.5: 変換前の `zola check`

記事・テンプレート未変換のまま実行した結果。最初に止まるのはサイト独自のショートコードテンプレート。

```text
$ zola check
Checking site...
ERROR Failed to check the site
ERROR error: Found string but expected identifier.
  --> shortcodes/image.html:29:29
   |
29 | {%- if src is starting_with("http") -%}
   |                             ^^^^^^
```

Tera 2 ではテストの引数も名前付きが必須（`is starting_with(pat="http")`）。
Zola 0.23 は `templates/shortcodes/` をまだ読み込み、構文エラーとして検出している。

### 補足: `{{< ... />}}` 構文は意図された変更か

作業中に出た疑問。一次情報で確認した結果、意図された変更である。

- Zola 0.23.0 CHANGELOG: 「shortcodes have been completely removed」。
  本文を Tera で直接テンプレート処理し、ショートコードとマクロの二重構造をやめて Tera のコンポーネントに一本化した
- 新しい呼び出し構文は Tera 2 側の設計。Tera MIGRATION.md に
  「inspired by https://jinjax.scaletti.dev/ ... kind of a mix between Jinja2 and JSX」とある
- `{{ expr }}` は式の出力のまま残るので、コンポーネント呼び出しを `<name ... />` で区別している。
  引数は JSX と同じく文字列はそのまま、それ以外は `{...}` で囲む（`autoplay={true}`）
- Zola 作者自身も「This is probably the most breaking version of Zola that will happen.」と書いている

この変更の副作用として、今回の移行で実際に踏んだもの

- 本文全体がテンプレート処理されるため、コード例中の `${{ secrets.X }}` などを `{% raw %}` で囲む必要がある
- コンポーネント出力が Markdown 変換の前に埋め込まれるため、出力 HTML 内の空行・インデントや、複数行にまたがる `<img` が
  Markdown に解釈されて表示が崩れる（Step 5 以降で対処）

### 確認: linkcard（はてなブログカード）

旧ビルド（Zola 0.22.1 + tabi 2f298c3）と新ビルドで出力を比較。

- 使用 16 記事・19 箇所。記事ごとの件数は新旧で一致
- `<iframe>` は CommonMark の HTML ブロック対象タグなので `<p>` で囲まれない（新旧とも 0 件）
- `src` の URL は、HTML エンティティをデコードすると 19 件すべて同一。
  違いは Tera 1 が `/` を `&#x2F;` にエスケープしていたのに対し、Tera 2 ではそのまま出力する点だけ

youtube / admonition / aside / references はユーザーが表示で問題なしを確認。全ページ比較は行わない。

### Step 4: 自作ショートコードをコンポーネントへ移植

`templates/shortcodes/*.html` を `templates/components/` へ移動（`git mv`）し、各ファイルを
`{% component name(...) %}` 〜 `{% endcomponent name %}` で囲んだ。`templates/shortcodes/` は削除。

| ファイル | 定義 | 主な書き換え |
|---|---|---|
| `image.html` | `image(src: string, @page = {}, alt = "", caption = "", lazy_loading = true, link_to_self = false)` | 下記参照 |
| `module.html` | `module(src: string, @page = {}, alt = "")` | image と同じパス解決 |
| `spot.html` | `spot(geo: string, name = "", address = "", tel = "", access = "")` | 下記参照 |
| `youtube.html` | `youtube(id: string)` | 囲むだけ |
| `linkcard.html` | `linkcard(url: string)` | 囲むだけ |

Tera 2 対応で必要だった書き換え

- `src is starting_with("http")` → `src is starting_with(pat="http")`（テストの引数は名前付き必須）
- `trim_start_matches(pat="./")` → `trim_start(pat="./")`（trim 系フィルタの統合）
- `alt | default(value="")` などは、コンポーネント引数のデフォルト値に置き換え
- `page.colocated_path` → `@page` 暗黙引数と `page.relative_path` から記事ディレクトリを算出（tabi v5 の画像コンポーネントと同じ方式）
- `meta` を最初に `{}` で初期化（Tera 2 は未定義変数へのアクセスで即エラー）

`@page` は Zola 0.23.6 で更新された Tera の implicit params（暗黙引数）。呼び出し側で `page` を渡さなくても、
呼び出し元コンテキストの `page` が自動で入る。

### Step 5: テーマ上書きテンプレートを tabi v5 ベースに作り直し

旧 tabi（`2f298c3`）の元ファイルとの差分からサイト独自のカスタマイズを特定し、
tabi v5 の新ファイルをコピーしてから同じカスタマイズを当て直した。

| ファイル | カスタマイズ内容 |
|---|---|
| `macros/list_posts.html` → `components/list_posts.html` | 一覧サムネイルの `local_image` を記事ディレクトリ基準で解決、「Read more」を「continue」に |
| `partials/cards_pages.html` | カードの `local_image` を記事ディレクトリ基準で解決 |
| `partials/header.html` | `page.extra.noindex` で `noindex, nofollow`、tinyseg（日本語 lunr）の読み込み削除 |
| `partials/home_banner.html` | `header.img_dark` でダークモード用プロフィール画像 |
| `partials/nav.html` | メニューの `new_tab` で別タブ |

tabi v5 本体はマクロを全廃してコンポーネントに移行しており、`macros/list_posts.html` は存在しない。
上書きは `components/list_posts.html` に置く。
tabi v5 でも colocated な `local_image` は解決されないため、上書きは引き続き必要。

Tera 2 の書き方に合わせた点

- `page.extra.noindex` → `page?.extra?.noindex`（セクションには `page` がない。optional chaining）
- 条件付き代入は三項演算子 `a if cond else b` で 1 行に（Tera 2 の新機能）

`templates/search.html`（Pagefind）と `templates/tabi/extend_head.html` は変更不要だった。

### Step 6: config.toml

v5 の要件（`[markdown.highlighting]` + `style = "class"`、`[search]` 内の `index_format`、`bottom_footnotes`）は
すでに満たしていた。変更は日付書式のみ。

```diff
-long_date_format = "%Y-%m-%d"
-short_date_format = "%Y-%m-%d"
-archive_date_format = "%Y-%m-%d"
+long_date_format = "y-MM-dd"
+short_date_format = "y-MM-dd"
+archive_date_format = "y-MM-dd"
```

### Step 7: 記事本文の一括変換

`scripts/migrate-shortcodes-zola-0.23.py` を作成（`--dry-run` あり）。フロントマター（`+++`）以外を変換する。

| 対象 | 変換 |
|---|---|
| `{{ name(a="x", b=true) }}` | `{{< name a="x" b={true} />}}` |
| `{% name(a="x") %}` 〜 `{% end %}` | `{% <name a="x"> %}` 〜 `{% </name> %}`（スタックで入れ子を対応付け） |
| `{{/* ... */}}`（旧エスケープ） | `{% raw %}{{ ... }}{% endraw %}` |
| 上記以外の `{{ }}` / `{% %}` / `{# #}` | `{% raw %}` で囲む |

- 複数行にまたがる呼び出しは 1 行にまとめた（`spot` や `multilingual_quote`）
- 旧 `spot` 呼び出しは第 1 引数の後のカンマが抜けていたが Tera 1 は通していた。スクリプトはカンマ・空白どちらの区切りも受理
- 実行結果: 312 ファイル変更。inline 440 件（image 297、youtube 110、linkcard 19 ほか）、block 147 件（references 63、admonition 34、aside 24、mermaid 17、module 9）、エスケープ 8 件、raw 化したリテラル 14 件

raw で囲んだリテラルの内訳

- GitHub Actions の `${{ secrets.X }}` / `${{ steps.x }}`（コードブロック内）
- `zola-pagefind-search` 記事のテンプレート例 `{% extends %}` / `{% block %}`
- MDX 移行時の残骸 `style={{ clear: 'both' }}`（2 記事）。以前から無効な HTML だが、出力を変えないため raw で保持
- `zola-theme-tabi` 記事の旧記法解説（`{%/* admonition(...) */%}`）。公開時の表示を保つため旧記法のまま表示

`zola-robust-image-shortcode` 記事は `remote_text` で `templates/shortcodes/image.html` を行番号指定で引用していた。
移動で引用元が消えるため、移行前のファイルを記事ディレクトリに `image-shortcode.txt` として保存し、参照先を差し替えた。
行番号（37–43、89–95）はそのまま有効。

### Step 8: ビルドで見つかった問題と修正

1. トップページ（`content/_index.md`）でビルドエラー

   ```text
   error: Component argument `title` (type: `none`) does not match expected type: `string`
    --> tabi/templates/partials/main_page_posts_list.html:7:15
   7 |             {{< page_header title={section.title} />}}
   ```

   ルートセクションに `title` がなく null。tabi v5 の `page_header` は `title: string` の型付き引数なので拒否される。
   公開中サイトでも該当 `<h1>` は空だったため、`title = ""` を明示して同じ出力にした。
   `zola check` はこのエラーを検出せず、`zola build` で初めて出た。

2. `spot` の情報欄がコードブロックとして表示される

   コンポーネントの出力は Markdown 変換の前に埋め込まれる。旧ショートコード時代は変換後に差し込まれていたため問題にならなかった。
   `spot` の出力には空行とインデントがあり、CommonMark では HTML ブロックが空行で終わるため、
   その後の 4 スペース以上インデントされた行がインデントコードブロックになった。
   → 制御タグを `{%- ... %}` にして空行を出さないよう修正。

3. `image` の `<img>` が `<p>` で囲まれる

   `<img` を複数行に分けて出力していた。`img` は CommonMark の HTML ブロック（type 6）の対象タグではなく、
   type 7（完全な開始タグだけの行）にも当たらないため段落扱いになった。
   → `<img ... />` を 1 行で出力するよう修正（`set` ブロックでタグを組み立て `| safe` で出力）。
   `link_to_self` の `<a>` も開始タグを単独行にした。

4. シンタックスハイライトの色が消える

   Zola 0.23 のハイライトはクラス名が番号形式（`z-1`, `z-3` …）に変わった。
   Zola 0.22 は `giallo.css` を `static/` に書き出しており、このリポジトリにも旧形式の `static/giallo.css` がコミットされていた。
   Zola 0.23 は出力ディレクトリに直接生成するが、`static/` の旧ファイルがそれを上書きしていた。
   → `static/giallo.css` を削除。

確認方法: `main` を `git worktree` で展開し、Cellar に残っていた Zola 0.22.1
（`/opt/homebrew/Cellar/zola/0.22.1/bin/zola`）でビルドして新旧の出力を比較した。

新旧で変わるが問題ない差分

- `/` が `&#x2F;` にエスケープされなくなった（Tera 2 の autoescape の変更）
- `<body dir="ltr">`（`text_direction` 関数）
- 読了時間が言語別の速度で計算され、日本語記事で短くなる（例: 3 min → 2 min）
- 脚注のバックリンク JS（`footnoteBacklinks.js`）が不要になり削除
- tabi v5 で `social_icons/xmpp.svg` が追加

ビルド時間の参考値: 新 676ms、旧 6.9s。ただし旧は worktree での初回ビルドで画像処理のキャッシュがなく、同条件の比較ではない。

### Step 9: CI・ドキュメント・ツール

- `.github/workflows/deploy.yml`, `zola-check-scheduled.yml`: `zola@0.23.6`
- `README.md`: バッジ・要件を 0.23.6、ディレクトリ説明を components に
- `CLAUDE.md`: Components 節（新構文、`{% raw %}` の注意）、カバー画像行、references の書き方
- `docs/tabi-shortcodes.md`: 移行スクリプトの変換ロジックで全例を新構文に変換し、全コンポーネントの引数を tabi v5 の定義と照合
- `.claude/commands/`（article-review, blog-review, blog-release）、`.claude/settings.json` のフックのメッセージ
- `scripts/convert-images.py`: 出力を新構文に

過去の作業記録（`tools/convert_mdx.py`, `docs/domain-migration.md`, `docs/pagefind-implementation-plan.md`）は当時の記録として変更しない。

### 移行と無関係に見つかった既存の問題（未対応）

- `2026/07/zero` 記事の pCloud リンクが 404。`zola check` が失敗する（scheduled check は main でも 2026-09-15 から失敗）
- `README.md` の Link Card 節が、`3241072 refactor: simplify linkcard` で廃止された GitHub カード機能を説明したまま → 現在の実装（全 URL をはてなブログカードの iframe で表示）に合わせて修正済み
- MDX 移行時の残骸 `style={{ ... }}`（`samukawa-kangoku`, `universal-audio-plugins`）→ `samukawa-kangoku` は手書きの OSM iframe を `spot` コンポーネント（`geo:35.598602,140.118325?z=15`）に置き換えて解消。`universal-audio-plugins` は未対応

### Step 10: /blog-review

- `module` コンポーネントの本文前後の空行を削除（他コンポーネントと方針をそろえる）。`darktable` 記事の出力が変わらないことを確認
- `mermaid`（17 ブロック / 13 記事）: 図の定義テキストは新旧で完全一致。先頭行のインデントがなくなっただけ
- `zola check`: pCloud リンク切れ 1 件のみ（既存の問題）。`zola build`: 成功（407 ページ、39 セクション）
