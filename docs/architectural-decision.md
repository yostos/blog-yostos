# Architectural Decision Records

## ADR-0001: サイト内検索にPagefindを採用

- **Status**: Accepted
- **Date**: 2026-02-25
- **Deciders**: yostos

### Context

本ブログ（Zola + tabiテーマ）は日本語コンテンツが主で、
記事数は255件を超えている。
Zolaの組み込み検索（elasticlunr.js）は
日本語のトークナイズに対応しておらず、
`config.toml` で `build_search_index = false` としている。

読者が目的の記事を効率的に見つけるため、
日本語対応のサイト内検索が必要になった。

### Decision

静的検索ライブラリ **Pagefind** を採用する。

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| Zola組み込みelasticlunr | 日本語トークナイズ非対応。elasticlunr自体がメンテナンス停止状態 |
| Algolia | SaaS依存。無料枠制限（月10,000リクエスト）。検索クエリが外部送信されプライバシー懸念 |
| Meilisearch | サーバー常時稼働が必要で静的サイトと根本的に不適合 |
| Fuse.js | 全インデックスをクライアントにDLする設計。記事数増加に伴いパフォーマンス劣化 |
| Google Programmable Search Engine | 無料版は広告表示。サービス縮小中。プライバシー問題 |

### Rationale

- **日本語対応**: extended版でCJKセグメンテーション対応。
  検索クエリ側は `Intl.Segmenter` で自動分割
- **静的サイトとの親和性**: ビルド時にインデックスを
  静的ファイルとして生成。外部サービス不要
- **軽量**: インデックスはチャンク分割され、
  検索時に必要な部分のみ転送
- **導入の容易さ**: `zola build` 後に
  `npx pagefind --site public` を追加するのみ
- **テーマ統合**: CSS Custom Propertiesで
  ダークモード対応可能。`templates/` への
  オーバーライドで `themes/` は編集不要
- **ライセンス**: MIT License。プロジェクトのMITと互換
- **プライバシー**: 完全クライアントサイド動作。
  GoatCounter採用の設計思想と一致
- **コスト**: ゼロ

### Known Limitations

- 日本語のステミング非対応
  （「走る」で「走った」はヒットしない）
- CJKのサブストリングマッチに限界あり
  （Pagefind Issue #987で改善議論中）
- 単語単位の完全一致検索は安定動作しており、
  現在の規模では実用上十分と判断

### Consequences

- デプロイワークフローに `npx pagefind` ステップを追加
- 検索UIのテンプレートオーバーライドを `templates/` に作成
- `static/custom.css` にPagefind用のスタイル調整を追加

---

## ADR-0002: 新規記事投稿時のBluesky自動投稿にGitHub Actionsを採用

- **Status**: Accepted
- **Date**: 2026-03-18
- **Deciders**: yostos

### Context

ブログ記事を投稿した後、Blueskyに記事リンクとdescriptionを手動で投稿している。
この手作業を自動化し、新規記事の公開時のみBlueskyへ自動投稿したい。

要件:
- 新規記事の投稿時のみ発動（更新時は対象外）
- 記事のURL、title、descriptionをBlueskyに投稿
- リンクカード（OGPプレビュー）を含める

### Decision

**GitHub Actions** を採用し、mainブランチへのpush時に新規記事を検出してBluesky AT Protocol APIで投稿する。

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| Cloudflare Worker + Deploy Hook | 「新規記事かどうか」の判定に状態管理（KV等）が必要。git diffが使えずロジックが複雑化 |
| Claude Code Hook（ローカル） | ローカル実行依存。別マシンからの投稿時に動作しない。CI/CDとの整合性も課題 |
| IFTSS / Zapier等の外部サービス | RSSフィード監視ベースのため遅延が発生。SaaS依存でコスト・プライバシー懸念 |

### Rationale

- **新規記事の正確な判定**: `git diff --name-status HEAD~1` で `A`（Added）ステータスの `content/**/index.md` を検出することで、新規投稿のみを確実に判別できる
- **既存ワークフローとの統合**: `/article-publish` スキルがcommit & push to mainを行うため、GitHub Actionsのトリガーと自然に連携する
- **シークレット管理**: BlueskyのアプリパスワードをgitHub Secretsで安全に管理できる
- **可視性**: 実行ログ・失敗通知がGitHub上で確認でき、デバッグが容易
- **コスト**: パブリックリポジトリのため無料枠で十分対応可能

### Technical Approach

- **API**: Bluesky AT Protocol（`com.atproto.server.createSession` → `com.atproto.repo.createRecord`）
- **投稿形式**: `app.bsky.feed.post` に `app.bsky.embed.external` でリンクカードを埋め込み
- **記事情報の取得**: frontmatter（TOML形式）からtitle, descriptionを抽出
- **URL生成**: ドメイン `codedchords.dev` + 記事パスから構築

### Consequences

- `.github/workflows/bluesky-post.yml` ワークフローを新規作成
- GitHub Secretsに `BLUESKY_IDENTIFIER` と `BLUESKY_APP_PASSWORD` を登録
- 投稿スクリプトを `scripts/` に配置

---

## ADR-0003: タグセットの定義ファイルにTOML、ベクターファイルにJSONを採用

- **Status**: Accepted
- **Date**: 2026-08-29
- **Deciders**: yostos

### Context

タグ体系を2層構造（first layer / second layer）に再編するにあたり、
タグセットをファイルとして管理する必要が生じた。
ファイルが満たすべき要件は以下の通り。

1. first layerとsecond layerの所属関係を表現できる
2. second layerごとにタグ名と説明を保持できる
3. second layerごとに全記事から抽出したベクター値を保持できる
4. タグ追加は人手で行い、その際ベクター値には初期値をセットする
5. ベクター値を定期的に更新できる

要件2と要件3では、扱うデータの性質が根本的に異なる。
タグ名と説明は人間が書き人間が読むテキストだが、
ベクター値はVoyage AIが生成する1024次元の浮動小数点配列で、
人間が読む意味を持たない。
埋め込みモデルの選定はADR-0004を参照。

### Decision

タグセットを2ファイルに分割し、
定義ファイル `data/tagset.toml` を **TOML**、
ベクターファイル `data/tag-vectors.json` を **JSON** とする。

### Alternatives Considered

比較は「定義ファイルの形式」と「1ファイルに統合するか分割するか」の
2軸で行った。

#### 定義ファイルの形式

| 候補 | 不採用理由 |
|------|------------|
| YAML | インデントで階層を表現するため、タグ追加時のインデント誤りが検出されずに意味が変わる。真偽値・数値への暗黙の型変換があり、`Go` `No` のような短いタグ名で予期しない解釈が起こりうる。リポジトリ内でYAMLは `pagefind.yml` のみで、設定ファイルの主流ではない |
| JSON | コメントを書けないため、タグの追加基準や判断の経緯をファイル内に残せない。末尾カンマを許さず、手編集でのタグ追加時に構文エラーを起こしやすい |
| CSV / TSV | 説明文に読点・カンマを含むためクォート処理が必要になり、手編集の容易さという唯一の利点が失われる。コメントも書けない |
| Markdownの表 | 人間には読みやすいが、機械可読な構造ではなく、スクリプトからの解析に独自パーサが必要になる |

#### ファイル構成

| 候補 | 不採用理由 |
|------|------------|
| TOML 1ファイルに統合（ベクターも含める） | 1024個の浮動小数点数を配列で持つとタグ1件が数万文字の1行になり、手編集ファイルとしての可読性が完全に失われる。ベクター再計算のたびに全行が書き換わり、Gitの差分でタグ定義の変更が埋没する |
| JSON 1ファイルに統合 | 上記に加え、コメント不可・手編集の脆弱性というJSONの欠点をタグ定義側にも持ち込むことになる |

### Rationale

定義ファイルにTOMLを選んだ理由。

- **既存リポジトリとの一貫性**: 記事のfrontmatter、`config.toml`、
  `wrangler.toml` がいずれもTOMLであり、
  このリポジトリで設定を書く際の標準形式になっている。
  タグ定義だけ別形式にする理由がない
- **手編集の安全性**: 階層をインデントではなく
  `[[layer2]]` と `parent` キーで明示するため、
  空白の過不足で構造が壊れない。要件4の
  「人手でタグを追加する」に直接効く
- **コメントが書ける**: タグを追加した理由や
  廃止したタグの経緯をファイル内に残せる
- **Zolaからの参照**: Zolaの `load_data` はTOMLを直接パースできるため、
  将来テンプレートからタグ体系を参照する余地を残せる
- **パーサの入手性**: Python 3.11以降は `tomllib` が標準ライブラリで、
  この環境（Python 3.14）では追加依存なしに読める

ベクターファイルにJSONを選んだ理由。

- 機械が生成し機械が読むファイルであり、
  可読性・コメント・手編集耐性というTOMLの利点がいずれも意味を持たない
- 数値配列の表現に最も素直で、
  PythonとNode.jsの双方が標準機能で読み書きできる

### Known Limitations

- TOMLの `[[layer2]]` はタグ数に比例して記述が縦に長くなる。
  タグ数が100を超える規模では見通しが悪化するが、
  現状の想定規模では問題にならない
- タグ名の重複やfirst layerへの誤った所属は
  フォーマット自体では防げないため、検証は別途スクリプトで担保する
- ベクター再計算時にJSONの全行が書き換わり、
  Gitの差分は大きくなる。定義ファイルを分離したことで
  タグ定義側の差分は汚染されない

### Consequences

- `data/tagset.toml` と `data/tag-vectors.json` を新規作成する
- 2ファイル間の整合性（定義にあるタグのベクターが存在するか）を
  検証する手段が別途必要になる

本ADRの決定時点では埋め込みモデルが未確定で、
Voyage AIの利用と1024次元を前提として記述していた。
その前提はADR-0004で `voyage-4`（`output_dimension` 1024）として
正式に決定され、次元数の想定は変わっていない。

---

## ADR-0004: タグ推薦の埋め込みモデルにVoyage AIのvoyage-4を採用

- **Status**: Accepted
- **Date**: 2026-08-30
- **Deciders**: yostos

### Context

タグ推薦は、記事本文のベクターと第2層タグのcentroidとの
コサイン類似度で候補を出す（`docs/tag-rule.md` の項目5）。
そのベクターを生成する埋め込みモデルを決める必要がある。

当初からVoyage AIを前提に `docs/tag-rule.md` を書いていたが、
選定理由がどの文書にも残っていなかった。
無料枠と価格が決め手だったが根拠を確認できないため、
ゼロベースで再調査し、実測した上で決め直した。

モデルが満たすべき要件は以下の通り。

1. 日本語の記事本文とタグ説明文を同じ空間に写像できる
2. 出力次元を選べる（`tag-vectors.json` をリポジトリに置くため）
3. 388記事・47タグの規模で、継続的な再算出コストが小さい
4. 管理するAPIキーを増やしすぎない

### Decision

**Voyage AIの `voyage-4`** を採用する。
`output_dimension` は **1024**、`input_type` は `document` とする。

### Alternatives Considered

Anthropicは自社の埋め込みモデルを提供していない。
公式ドキュメントに "Anthropic does not offer its own embedding model" と明記され、
Voyage AIが案内されている。したがって候補はOpenAI・Google・Voyageの3社となる。

全388記事を埋め込み、タグごとにcentroidを作り、
leave-one-outで正解タグの順位を測った。実際の運用設計そのものである。

| モデル | 次元 | 正解1位 | 上位3位内 | 第1層一致 | 単価/1M | 無料枠 |
|---|---:|---:|---:|---:|---:|---|
| voyage-4-large | 1024 | 75.5% | 89.2% | 88.9% | $0.12 | 200M |
| openai text-embedding-3-large | 3072 | 75.5% | 89.4% | 88.1% | $0.13 | なし |
| voyage-4-lite | 1024 | 75.3% | 88.9% | 88.1% | $0.02 | 200M |
| voyage-4 | 1024 | 75.0% | 88.9% | 88.9% | $0.06 | 200M |
| voyage-4 | 2048 | 74.7% | 88.7% | 89.2% | $0.06 | 200M |
| openai text-embedding-3-large | 1024 | 74.2% | 89.9% | 87.1% | $0.13 | なし |
| gemini-embedding-2 | 1024 | 72.2% | 87.6% | 86.6% | $0.20 | あり |
| openai text-embedding-3-small | 1536 | 71.6% | 89.9% | 84.3% | $0.02 | なし |
| gemini-embedding-001 | 1024 | 71.1% | 87.6% | 87.1% | $0.15 | あり |

不採用の理由は以下の通り。

| 候補 | 不採用理由 |
|------|------------|
| OpenAI `text-embedding-3-large` | 3072次元でなければ最高精度が出ない。1024に落とすと75.5%から74.2%へ下がる。`tag-vectors.json` を3倍に膨らませるか精度を落とすかの二択になる |
| OpenAI `text-embedding-3-small` | 1536次元で正解1位71.6%、第1層一致84.3%と、測定した中で最も低い |
| Google `gemini-embedding-2` / `-001` | 精度が3ポイント低い。無料枠は「Used to improve our products: Yes」であり、有料に切り替えると単価は最も高い。`-001` が既に `-2` に置き換わりつつあり、モデル更新のたびに全タグの再算出を迫られる |
| Voyage `voyage-4-large` | 精度は最上位だが単価が2倍で、1リクエストあたりのトークン上限が120K（`voyage-4` は320K）と低い。差の0.5ポイントは誤差の範囲 |
| Voyage `voyage-4-lite` | `voyage-4` との差0.3ポイントは誤差の範囲。無料枠があるため単価差も実質的に効かない |
| Voyage `voyage-3.5` | 「Older models」に分類され、無料枠の対象外。単価は `voyage-4` と同じ$0.06で、選ぶ理由がない |

### Rationale

- **1024次元での精度**: これが決め手になった。`tag-vectors.json` の
  サイズは次元に比例する。OpenAIの3-largeは3072次元でしか最高精度に
  届かないが、Voyageは1024で同じ水準を保つ
- **無料枠**: 200Mトークンが全アカウントに付く。全388記事1回の
  埋め込みは193Kトークンだったため、無料枠だけで約1000回の
  再算出に相当する。当初の選定理由がここで裏づけられた
- **正規化済み**: 出力は長さ1に正規化されているため、
  コサイン類似度を内積で計算できる
- **Anthropicの案内先**: 自社モデルを持たないAnthropicが案内する
  事業者であり、当初の選定とも整合する

### Technical Approach

- **エンドポイント**: `POST https://api.voyageai.com/v1/embeddings`
- **認証**: `Authorization: Bearer $VOYAGE_API_KEY`
- **リクエスト**: `input`（文字列または配列）、`model`、
  `input_type`、`output_dimension`、`truncation`
- **制約**: 配列は最大1,000件。1リクエストあたり `voyage-4` で
  320Kトークンまで。コンテキスト長は32,000トークン
- **レート制限**: Tier 1（支払い方法の登録で到達）で
  `voyage-4` は8M TPM / 2,000 RPM
- **`input_type`**: 記事とタグを対称に比較するため双方に `document`
  を指定する。`null` との差は実測で0.8ポイント（`document` が上）
- **centroidの算出**: そのタグを持つ記事のベクターを平均し、
  再度L2正規化する。正規化を省くと、記事数の多いタグが
  長さの違いで有利になる

キーは環境変数 `VOYAGE_API_KEY` から読む。
`scripts/generate-cover.sh` が `OPENAI_API_KEY` を扱う方式に揃え、
引数では受け取らず、未設定なら処理に入る前に終了する。
ベクター算出はローカルで実行するため、
GitHub Actionsのシークレットには登録しない。

### Known Limitations

- 支払い方法を登録するまではTier 1に到達せず、
  数リクエストで429が返る。実際に発生した
- 測定は388記事のleave-one-outで、標準誤差は約2ポイント。
  上位4モデルの差はこの範囲に収まり、統計的には区別できない。
  `voyage-4` を選んだのは精度が有意に高いからではなく、
  1024次元・無料枠・上限の余裕を合わせた総合判断である
- 管理するAPIキーが1つ増える。OpenAI・Googleのキーは
  既に手元にあり、その点では両社が有利だった
- 埋め込みモデルを変更した場合は全タグの再算出が必要になる。
  `tag-vectors.json` の `model` と `dim` はその判定のために持つ

### Consequences

- `VOYAGE_API_KEY` を環境変数として保持する
- `data/tag-vectors.json` の `model` は `voyage-4`、`dim` は1024となる
- `docs/tag-rule.md` の `voyage-3.5` / `input_type` の記述を更新する
