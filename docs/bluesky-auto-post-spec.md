# Bluesky自動投稿 仕様書

## 概要

新規ブログ記事がmainブランチにpushされた際、GitHub Actionsにより
Blueskyへ記事リンクとdescriptionを自動投稿する。

## トリガー条件

- **イベント**: `push` to `main`
- **パスフィルター**: `content/**` 配下の変更を含むこと
- **新規記事判定**: `git diff --name-status HEAD~1 HEAD` の出力で
  `A`（Added）ステータスかつ `content/**/index.md` に一致するファイルが存在すること
- 記事の更新（`M` ステータス）や削除（`D` ステータス）では投稿しない
- 1回のpushで複数の新規記事が追加された場合、それぞれに対して投稿する

## 記事情報の抽出

frontmatter（TOML形式、`+++` で囲まれた領域）から以下を抽出する:

| フィールド | 用途 | 必須 |
|-----------|------|------|
| `title` | リンクカードのタイトル | Yes |
| `description` | リンクカードの説明文 | Yes |
| `[taxonomies].tags` | ハッシュタグ生成 | No |
| `[extra].social_media_card` | OGP画像（リンクカードのサムネイル） | No |

TOML複数行文字列（`"""\..."""`）の行継続バックスラッシュ `\` は除去して
単一行に結合する。

## URL生成

記事のURLは以下のルールで生成する:

```
https://codedchords.dev/{content/ からの相対パスでindex.mdを除いたもの}
```

例:
- `content/blog/my-article/index.md` → `https://codedchords.dev/blog/my-article/`

## Bluesky投稿フォーマット

### テキスト本文

```
📝 Just published:

#blog {tags → #ハッシュタグ（最大5個）}
```

- descriptionはリンクカード側で表示されるため、テキスト本文には含めない
- 投稿文字数はBlueskyの上限（300 grapheme）に収める
- 300 graphemeを超える場合はハッシュタグを末尾から削減
- ハッシュタグはタグ名をそのまま `#` 付きで使用（スペースを含むタグはスキップ）
- `#blog` は固定で常に付与する

### リンクカード（embed.external）

`app.bsky.embed.external` を使用してリンクカードを埋め込む:

| フィールド | 値 |
|-----------|-----|
| `uri` | 記事URL |
| `title` | frontmatterのtitle |
| `description` | frontmatterのdescription |
| `thumb` | OGP画像のblobリファレンス（`uploadBlob` で取得） |

Bluesky側はURLからOGPを自動取得しないため、OGP画像は
`com.atproto.repo.uploadBlob` でアップロードし、返却されたblob
リファレンスを `thumb` に設定する。画像が存在しない場合は
`thumb` を省略し、画像なしのリンクカードとなる。

## Bluesky API仕様

### 認証

1. `com.atproto.server.createSession` でセッションを作成
   - **Endpoint**: `POST https://bsky.social/xrpc/com.atproto.server.createSession`
   - **Body**: `{ "identifier": "<handle>", "password": "<app-password>" }`
   - **Response**: `accessJwt`, `did` を取得

### 投稿

2. `com.atproto.repo.createRecord` で投稿を作成
   - **Endpoint**: `POST https://bsky.social/xrpc/com.atproto.repo.createRecord`
   - **Headers**: `Authorization: Bearer <accessJwt>`
   - **Body**:

```json
{
  "repo": "<did>",
  "collection": "app.bsky.feed.post",
  "record": {
    "$type": "app.bsky.feed.post",
    "text": "<投稿テキスト>",
    "createdAt": "<ISO8601>",
    "facets": [ "<リンク・ハッシュタグのfacet>" ],
    "embed": {
      "$type": "app.bsky.embed.external",
      "external": {
        "uri": "<記事URL>",
        "title": "<title>",
        "description": "<description>",
        "thumb": "<blob reference from uploadBlob>"
      }
    }
  }
}
```

### Facets

テキスト内のURL・ハッシュタグに対してfacetを設定する:

- **ハッシュタグfacet**: テキスト中の `#tag` に `app.bsky.richtext.facet#tag` を適用
- facetの `byteStart` / `byteEnd` はUTF-8バイト位置で指定する

## GitHub Secrets

| Secret名 | 内容 |
|----------|------|
| `BLUESKY_IDENTIFIER` | Blueskyのハンドル（例: `yostos.bsky.social`） |
| `BLUESKY_APP_PASSWORD` | Blueskyのアプリパスワード |

## ファイル構成

```
.github/workflows/bluesky-post.yml   # GitHub Actionsワークフロー
scripts/bluesky-post.sh              # 投稿スクリプト本体
```

## エラーハンドリング

- API認証失敗: ワークフローをfailにしてGitHub通知に委ねる
- 投稿失敗（4xx/5xx）: エラーレスポンスをログに出力しワークフローをfailにする
- frontmatter解析失敗: エラーログを出力しスキップ（他の記事があれば続行）
- 新規記事なし: 正常終了（ログに "No new articles found" を出力）

## 将来の拡張（スコープ外）

- 投稿済み記事の重複投稿防止（冪等性の担保）
- 投稿内容のカスタマイズ（記事側のfrontmatterで制御）
