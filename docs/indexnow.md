# IndexNow

Bing Webmaster Tools 向けの IndexNow 連携。
記事公開後に検索エンジンへ新規・更新URLを即座に通知する。

## 仕組み

1. サイトルートにキーファイルを配置（`static/ceaaeaf047f940dcbed3b040f48f1a27.txt`）
2. 記事公開後、IndexNow API に対象URLをPOSTで送信
3. Bing（および IndexNow 対応エンジン）がクロール・インデックスを実施

対応検索エンジン: Bing, Yandex, Seznam, Naver

## スクリプト

`scripts/indexnow.sh` — URLのデプロイ完了を待機してから IndexNow API に送信する。

### 使い方

```bash
# 基本（デプロイ完了を待ってから送信）
./scripts/indexnow.sh https://codedchords.dev/posts/my-article/

# 複数URL
./scripts/indexnow.sh https://codedchords.dev/posts/article1/ https://codedchords.dev/posts/article2/

# デプロイ済みを確認済みならポーリングをスキップ
./scripts/indexnow.sh --no-wait https://codedchords.dev/posts/my-article/
```

### 動作

1. 対象URLに対して HTTP GET でポーリング（15秒間隔、最大5分）
2. 200 応答を確認後、IndexNow API (`https://api.indexnow.org/IndexNow`) に JSON POST
3. レスポンスコードを解釈して結果を表示

### レスポンスコード

| コード | 意味 |
|--------|------|
| 200 | URL submitted and indexed |
| 202 | Accepted, will be processed later |
| 400 | Bad request |
| 403 | Key not valid |
| 422 | Invalid URL |
| 429 | Too many requests |

### 依存

- `curl`
- `jq`

## /article-publish との連携

`/article-publish` の最終ステップ（Step 6）で自動実行される。
git push 後、デプロイ完了を待機してから IndexNow に送信する。

## 参考

- [IndexNow Protocol](https://www.indexnow.org/)
- [Bing Webmaster Tools - IndexNow](https://www.bing.com/indexnow)
