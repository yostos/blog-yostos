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

---

## ADR-0005: Atomフィードを全記事配信のまま維持する

- **Status**: Accepted
- **Date**: 2026-08-30
- **Deciders**: yostos

### Context

本ブログは `config.toml` で `generate_feeds = true`、
`full_content_in_feed = true` とし、`feed_limit` は未設定である。
Zolaの既定では `feed_limit` 未設定は全件配信を意味するため、
`/atom.xml` には全381件が全文で入っている（非圧縮で4.6MB）。
`taxonomies = [{name = "tags", feed = true}]` により
タグ別フィード54本も同じ条件で生成される。

投稿ペースは直近12ヶ月で215本、月約18本である。
フィードサイズが大きいことを懸念し、
`feed_limit` で直近N件に絞るべきかを検討した。

### Decision

`feed_limit` を設定せず、全記事配信・全文配信を維持する。

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| `feed_limit = 20` | 月18本ペースでは約1ヶ月分しかカバーできず、長期間フィードを取得しなかった読者が記事を取りこぼす |
| `feed_limit = 50` | 約2.8ヶ月分をカバーし取りこぼしリスクは下がるが、後述の実測どおり解決すべき問題自体が存在しなかった |
| `full_content_in_feed = false` | サイズは大きく減るが、全文配信は読者体験として明確に上位。件数より先に削る対象ではない |

### Rationale

2026-08-30 に `https://codedchords.dev/atom.xml` を実測した結果:

| 条件 | 転送量 |
|------|-------:|
| `Accept-Encoding: br` | 948,343 bytes |
| `Accept-Encoding: gzip` | 1,040,366 bytes |
| `Accept-Encoding: identity` | 4,631,976 bytes |
| `If-None-Match` 付き | 304 / 0 bytes |

- **帯域は問題にならない**。Cloudflareがbrで圧縮して配信し、
  実転送量は非圧縮の約1/5の948KBである
- **条件付きGETが機能している**。ETagが付与されており、
  `If-None-Match` 付きのリクエストは304・転送0バイトを返す。
  `cf-cache-status` も HIT である。
  まともなフィードリーダーは条件付きGETを行うため、
  巡回されても通常は0バイト、更新のあった回のみ本体が流れる
- 月18本ペースで本体が流れる回数は月18回程度、
  購読者1人あたり月17MB程度にとどまる。
  Workers Static Assetsは帯域無料でリクエスト課金のため、
  コストにも影響しない
- 将来の成長も圧縮後で年500KB前後。
  Workers Static Assetsの個別ファイル上限25MiBは、
  非圧縮の4.6MBで見ても8年程度先である
- 制限を入れないことで、
  長期間フィードを取得しなかった読者が
  記事を取りこぼさないという性質を恒常的に維持できる

### Known Limitations

- 新規購読者は初回取得で381件を未読として取り込む。
  MinifluxやNetNewsWire等は全エントリを未読で登録するため、
  条件付きGETでもキャッシュでも解決しない。
  ただし購読者1人につき一度きりの体験であり、
  取りこぼしゼロという恒常的な利点とは釣り合わないと判断した
- サイズ上限のある変換サービス（RSS-to-Email等）を
  経由してフィードを配信する場合には制限が必要になる。
  現在そのような利用はない
- `feed_limit` は全フィード共通の設定で、
  トップ・セクション・タグの54本すべてに一律で効く。
  フィードごとに件数を変えることはできない

### Consequences

- `config.toml` は変更しない
- 記事数の増加に伴いフィードは年2.6MB（非圧縮）増える。
  25MiBに近づいた時点で本ADRを再検討する

---

## ADR-0006: タグ推薦のベクターを記事centroidからタグ名の埋め込みに変更

- **Status**: Accepted
- **Date**: 2026-08-31
- **Deciders**: yostos

### Context

ADR-0004 で採用した方式では、`data/tag-vectors.json` に第2層タグごとの
centroid を保持していた。そのタグを持つ全記事を埋め込み、平均して
L2再正規化した値である。推薦は記事本文のベクターとの
コサイン類似度で行っていた。

この方式には2つの制約があった。

1. **タグを1つ追加するだけで全記事の再算出が要る。** centroid は
   記事から作るため、`tagset.toml` を編集するたびに全388記事を
   埋め込み直す必要があった。1回あたり542Kトークン・7秒
2. **記事0件のタグを推薦できない。** 平均を取れないため `vector` が
   `null` になり、候補から外れる。そのタグが付くまで推薦されず、
   推薦されないから記事も付かないという循環が生じる

タグ名そのものを埋め込む方式に変えれば、両方が解消する。
記事を参照しないため再算出は `tagset.toml` の編集時だけになり、
記事0件のタグも同じようにベクターを持てる。

精度を落とさずに移行できるかを実測で確認した。

### Decision

`data/tag-vectors.json` の `vector` を、**第2層タグ名そのものを
埋め込んだ値**に変更する。`schema_version` を2に上げ、
`vector_source` フィールドに `tag_name` を記録する。

推薦は次の手順で行う。

1. 記事を読み、内容を表す英単語を5つ選ぶ。既存のタグ一覧は参照しない
2. 5語を半角スペースで連結し、1つの文字列として埋め込む
3. 各タグのベクターと内積を取り、最上位のタグとその親を frontmatter に書く

あわせてタグ名の付け方に基準を設け、タグセットを調整する。

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| 記事centroidを維持 | 精度は最も高いが、上記2つの制約が残る。タグ新設のたびに全記事の再算出が必要 |
| 5語を1語ずつタグと突き合わせ、最も近い組を採る | 提案時の原案。実測で第2層1位47.5%と、centroid方式の75.0%から大きく落ちた |
| タグ名に説明文を連結して埋め込む | 実測で数ポイント改善したが、説明文は日本語・単語は英語で語彙が混ざる。タグ名だけで基準を満たせたため採らなかった |
| centroidと定義ベクターの加重平均 | 精度は維持できたが、centroidを持つ以上、再算出の制約が残る |
| 記事全文をそのまま照合に使う | タグ名ベクターと組み合わせた場合、5語連結より精度が低かった |

### Rationale

**タグ名だけで照合が成立するのは、埋め込みモデルが事前学習で
一般的な言語知識を持っているためである。** モデルは Wikipedia や書籍、
Web 上の膨大なテキストから「どの語がどの文脈で一緒に使われるか」を学習し、
意味の近い語が近い座標に並ぶベクトル空間を内部に持っている。
`Cloud` という文字列を渡せば、「空に浮かぶ雲」だけでなく
「IT のクラウドインフラ」という意味合いを含む座標が返り、記事から選んだ
`infrastructure` や `serverless` も同じ空間の近い位置に来る。
このブログで `Cloud` タグが過去どう使われてきたかをモデルが知らなくても、
世間一般でそれらが近い概念であるという知識だけで照合できる。

centroid が「このブログでの使われ方」を表すのに対し、
タグ名のベクターは「世間一般でのその語の意味」を表す。
移行とは、タグの意味の拠り所を前者から後者へ移すことである。

**移行の可否は実測で判断した。** 検証は3つの期間で行い、
正解は著者が付けた既存のタグとした。

| 期間 | 記事数 | 第2層1位 | 上位3以内 | 第1層 |
|---|---:|---:|---:|---:|
| 2026-03〜05 | 73 | 71.2% | 89.0% | 91.8% |
| 2026-04〜06 | 61 | 75.4% | 93.4% | 88.5% |
| 直近（2026-05-29〜08-29） | 50 | 76.0% | 88.0% | 92.0% |

旧方式（記事全文と centroid の照合、leave-one-out）は
第2層1位75.0%、上位3以内88.9%、第1層88.9%だった。
標準誤差は各期間5〜7ポイントで、いずれの指標も同水準に収まっている。

移行の過程で2つの発見があった。どちらも設計に反映している。

- **5語は連結しなければならない。** 1語ずつタグと突き合わせて
  最も近い組を採ると、残り4語が捨てられる。「演奏」と「機材」のように
  複数語の組み合わせでしか表せない意味が失われ、記事の題材語が
  タグ名と字面で一致した時点で勝敗が決まってしまう。実測で
  47.5%対77.5%と30ポイントの差がついた
- **タグ名の付け方が精度を直接左右する。** モデルが持つのは一般的な
  言語知識だけであり、このブログ固有の用法は知らない。したがって
  名前が説明文を言い当てていなければ推薦は成立しない。
  当初のタグセットには、語義から中身が読めない名前（連載名、抽象語、
  形式を指す語）や、意味の違いが記事の立場によるもので語義には
  現れない対が含まれていた。centroid はそれを記事の内容から
  区別できていたが、タグ名では区別できない

後者への対処として、タグ名の基準を `docs/tag-rule.md` に定め、
タグセットを調整した。

| | 調整前 | 調整後 |
|---|---:|---:|
| 第2層タグ数 | 47 | 36 |
| 最大類似度 | 0.937 | 0.837 |
| 0.85以上のペア | 4 | 0 |
| 0.80以上のペア | 22 | 6 |
| うち親が異なるもの | 10 | 0 |

改名・統合・廃止の3つの型で整理し、延べ141記事のタグを更新した。
第1層7種と、全388記事が「第1層1つ・第2層1つ」を持つ構成は維持している。

閾値0.85は実測から決めた。誤りが起きたタグ対の類似度は0.57〜0.84に
散らばっており、0.80を超えていたのは1対のみだった。全ペアの中央値は
0.64前後で、0.85以上は明らかな外れ値にあたる。0.80未満の近さを
詰めても誤りは減らない。

**副次的な効果としてコストが消えた。** 再算出は36タグで16トークン・
1秒未満となり、旧方式の542Kトークン・7秒から実質ゼロになった。
`tag-vectors.json` も1.46MBから1.12MBに減っている。

### Known Limitations

- 記事を5語に圧縮する工程が Claude の判断に依存する。同じ記事でも
  選ぶ語が変われば結果が変わり、旧方式のように全記事を機械的に
  leave-one-out で測ることができない。精度の再測定には
  記事を読んで語を選ぶ工程が必要になる
- 記事の題材語がタグ名と字面で近いと、記事の主題と無関係に
  そのタグが選ばれる誤りが残る。抽象的なタグ名も同様に、
  無関係な記事を引き寄せる
- タグ名に基準を課したため、名前の自由度が下がった。
  タグを新設・改名するときは `tag-vectors.json` を再算出したうえで
  全ペアの類似度を確認する運用が必要になる
- 検証は各期間50〜73記事で、標準誤差は5〜7ポイントある。
  旧方式との差はこの範囲に収まっており、優劣は判定できない。
  採用したのは精度が高いからではなく、同水準を保ったまま
  再算出コストと記事0件タグの制約を外せたためである
- `Gadget` と `Automotive` の配下が小さいまま残った。
  記事が増えない場合は第1層ごと見直す余地がある

### Consequences

- `data/tag-vectors.json` は `schema_version` 2、`vector_source` は `tag_name` となる
- `scripts/build-tag-vectors.py` は記事を埋め込まず、タグ名のみを埋め込む
- 再算出のタイミングが「不定期・手動」から「`tagset.toml` の編集時」に変わる
- `docs/tag-rule.md` にタグ名の基準と類似度の閾値を追加する
- `.claude/commands/article-tag.md` の手順を、5語の選定と連結に置き換える
- 旧方式の `tag-vectors.json` は `data/tag-vectors.centroid-20260831.json.bak`
  に退避してある。移行が定着した時点で削除する

---

## ADR-0007: 記事の公開をGitHub FlowのPRマージに一本化

- **Status**: Accepted
- **Date**: 2026-11-25
- **Deciders**: yostos

### Context

これまで記事は `main` に直接 push して公開していた（`/article-publish` が
`git push origin main` を実行する）。

将来、GitHub Issue に書いた執筆依頼をもとに、Claude Code で下書きを作って
ブランチを push する仕組みを計画している。実行環境は Raspberry Pi か
GitHub Actions のどちらかで、まだ決めていない。
下書きはそのまま公開できる品質ではなく、必ず Mac で仕上げる必要がある。
`main` への直接 push を続けると、自動で作るブランチと公開の流れが噛み合わない。
そこで自動化より先に、ブログの運用を変える。

### Decision

**GitHub Flow** を採用する。`main` を保護し、すべての変更をブランチと PR で行い、
PR の squash merge を公開とする。誤字修正も例外とせず、
Ruleset のバイパス対象には管理者も含めて誰も登録しない。
検査はすべて PR で行い、commit 時と push 時の hook は廃止する。
運用の詳細は `docs/repository-workflow.md` に定める。

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| `main` への直接 push を続ける | 自動で作るブランチを同じ流れに乗せられない |
| `develop` ブランチを置く Git Flow | 書き手が1人のブログでは利点がなく、マージが2倍になるだけ |
| 誤字修正だけ直接 push を許す | `main` の保護に抜け道ができ、「公開はPRのマージだけ」という前提が崩れる |
| 管理者にバイパスを許す | 同上 |
| 緊急時に Ruleset を一時的に無効にする | 実質的に管理者のバイパスと同じになる。承認数 0 なので、緊急時も修正の PR をすぐマージできる |
| rebase merge / merge commit を許す | rebase merge では `bluesky-post.yml` の `HEAD~1` 差分検出から新規記事が漏れる。方式を1つに揃えるため merge commit も使わない |
| commit 時・push 時の hook で検査を続ける | 書きかけの commit や自動で作る下書きが止まる。hook はクローンごとに `npm install` で入るため、環境によって検査の有無が変わる |

### Rationale

- **自動化との整合**: 自動で作ったブランチも、Mac で作ったブランチも、同じ PR の流れで公開できる
- **既存ワークフローとの互換**: PR のマージは `main` への push として扱われるため、
  `deploy.yml` と `bluesky-post.yml` のトリガーを変えずに済む
- **検査の一元化**: 必須のステータスチェックは環境に関係なく効くため、
  どこで作った変更でも、検査を通ったものだけが公開される
- **履歴の形式を維持**: squash merge のコミットタイトルに Conventional Commits 形式の
  PR タイトルを使えば、`main` の履歴はこれまでと同じ1記事1コミットになる

### Consequences

- GitHub の Ruleset で `main` を保護する（PR 必須、承認数 0、必須のステータスチェック、
  バイパスなし、force push とブランチ削除を禁止）
- リポジトリの設定を変える（マージ方式を squash merge のみにする、
  squash のタイトルを `PR_TITLE`・本文を `PR_BODY` にする、マージ後に作業ブランチを自動で削除する）
- OGP 画像の有無を検査する `.github/workflows/ogp-check.yml` を新しく作る
- husky の hook（`.husky/pre-commit`、`.husky/pre-push`）と、`package.json` の
  `prepare`・`lint-staged` の設定、husky と lint-staged の依存を削除する
- `.claude/commands/article-publish.md` の push 手順を、ブランチ・PR・マージに書き換え、
  lint-staged の記述を直す
- `.claude/commands/blog-release.md` の `gh pr merge` に `--squash` を付ける
- `CLAUDE.md` に、作業前にブランチを確認する手順とこの運用ルールへの参照を加え、
  Hosting 節のデプロイの説明を直す
- 誤字修正でも PR を作る手間が増える。検査の結果が分かるのは PR を作った後になる
- `claude-code-review.yml` がすべての PR で動くようになる。残すかどうかは未決定である

## ADR-0008: Issue で執筆依頼を受けず、PR の必須チェックにビルドとカバー画像の検査を加える

- **Status**: Accepted
- **Date**: 2026-11-26
- **Deciders**: yostos

### Context

ADR-0007 で、記事の公開を PR のマージに一本化した。その上で、GitHub Issue に書いた執筆依頼から
Claude が下書きを作り、Draft PR として出す仕組みを検討した（`docs/draft-automation-plan.md`）。
実行環境の試験まで進めたところで、次の問題が分かった。

- このリポジトリは public である。Issue の本文とコメント、下書きのブランチ、commit、Draft PR はすべて誰でも読める。
  Draft は公開範囲を変えない。本文を書き換えても編集履歴から読め、外部のアーカイブにも本文ごと残る
- 執筆依頼には、記事にするか決まっていない構想やアイデアが入る。下書きの段階の本文も公開されることになる
- 非公開に保つ方法は二つあり、どちらも負担が大きい
  - 依頼と下書きを、ブログのリポジトリを複製した private リポジトリに置く。
    リポジトリが2つになり、`main` の追従と、公開側へ移す手順が要る
  - ブログのリポジトリを private にする。個人アカウントの private リポジトリで Ruleset を使うには GitHub Pro 以上が要る。
    全ページのフッターと「変更履歴」のリンク、および記事からスクリプトへのリンクが読者には 404 になる

あわせて、検討の中で自動化と関係なく次のことが分かった。

- PR の必須チェックは textlint と OGP の有無だけで、ビルドの失敗はマージ後の `deploy.yml` まで検出されない。
  `social_media_card` や本文冒頭の画像の行があってファイルがないと、ビルドが失敗する
  （tabi の `throw()` と、`get_url(cachebust=true)` のエラー。2026-11-26 に試験で確認）
- CLAUDE.md は新しい記事にカバー画像を必須としているが、検査がない。436記事のうち253記事には `local_image` がない。
  `local_image` があっても、本文冒頭の画像の行を意図して置かない記事もある
- 執筆と作業のルールの一部は Mac の `~/.claude` のメモリにしかない。Issue で `@claude` に頼んだ作業は
  GitHub Actions で動き、リポジトリにあるものしか読めない
- `claude.yml` は、checkout が git の設定に残す `GITHUB_TOKEN` の認証のせいで push できなかった。
  `persist-credentials: false` を指定すると、Claude GitHub App のトークンで push でき、
  その push で必須チェックも起動した（PR #13、2026-11-26 に試験で確認）

検討と試験の経緯は `docs/draft-automation-plan.md` と `docs/draft-automation-log.md` にある。

### Decision

1. **Issue で記事の執筆依頼を受けない。** Issue はブログのデザインや機能の修正に使い、記事の修正に使うこともある。
   公開する前の構想を Issue に書かない
2. **Claude に対応を頼むかどうかは、Issue に `@claude` を書くかどうかで決める。** 既存の `claude.yml` を使う。
   Claude の変更も、ブランチと PR を通してオーナーがマージする
3. **PR の必須チェックに `zola build` を加える。** `zola check` は使わない
4. **PR で追加された記事のカバー画像を、必須チェックで検査する。** `local_image` とそのファイルがあることだけを確かめ、
   本文冒頭の画像の行は求めない
5. **メモリにある執筆と作業のルールを CLAUDE.md に移す。**
   「下書き中に lint を実行しない」と「`zola build` を勝手に走らせない」は Mac での対話の作業に限り、
   Actions 上の作業では実行する
6. **`claude-code-review.yml` は残し、機能の変更の PR だけで動かす。** 記事だけを変える PR では動かさない。
   `@claude` が push した PR でも動くように、`allowed_bots` に `claude` を加える

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| Issue から下書きを自動で作り、Draft PR で出す | 構想と仕上げる前の下書きが公開される |
| 執筆依頼と下書きを private リポジトリに置く | リポジトリが2つになり、`main` の追従、公開側へ移す手順、push 前に commit をまとめる手順が要る。効果が負担に見合わない |
| ブログのリポジトリを private にする | Ruleset を残すには GitHub Pro が要る。ソースと変更履歴へのリンクが切れる。Actions も課金の対象になる |
| カバー画像の検査を全記事に適用する | 古い記事の多くにカバー画像がなく、既存の記事で失敗する |
| カバー画像の検査で本文冒頭の画像の行も求める | 新しい記事でも画像の行を意図して置かないことがあり、正しい記事が落ちる |
| `zola check` を使う | 外部リンクも確かめるので時間がかかり、相手のサイトの都合でも失敗する |
| `claude-code-review.yml` を削除する | PR #9 と PR #11 で実際に不具合を見つけており、機能の変更では役に立っている |
| `claude-code-review.yml` をすべての PR で動かす | 記事の文章は手元の `/article-review` がレビューする。コード向けの観点で記事を見る意味は薄く、利用枠を使うだけになる |
| `@claude` の PR では `claude-code-review.yml` を動かさない | Claude が書いた機能の変更こそ、マージ前に別の目で見る価値がある |
| `zola build` を手元でだけ実行する | 手元での実行を忘れた場合や、`@claude` の PR を防げない |

### Rationale

- **公開範囲は運用で守る**: Public なリポジトリで構想を非公開に保つ仕組みは、どれもリポジトリかプランを増やす。
  執筆依頼を Issue に書かなければ、構想が公開されることはなくなり、追加の仕組みは要らない
- **`@claude` は今の仕組みで足りる**: `claude.yml` は Issue の `@claude` で起動し、PR #13 の修正で push と必須チェックまで動く
- **ルールを検査で担保する**: ビルドが通ることと、新しい記事にカバー画像があることは、誰が作った PR にも当てはまる要件である。
  OGP 画像を `ogp-check.yml` で担保しているのと同じく、必須チェックでマージを止める
- **レビューは対象に合った道具で行う**: 機能の変更は `claude-code-review.yml` が、記事の文章は `/article-review` が見る
- **ルールの置き場所を一つにする**: CLAUDE.md に移せば、Mac の Claude と Actions の Claude が同じルールを読む

### Known Limitations

- 書き込み権限のない人が `@claude` を書いたときに Claude が起動しないかは、まだ確かめていない
- `claude-code-action` の既定の `bot_id` は `github-actions[bot]` のものなので、`@claude` の commit は
  GitHub の画面で `github-actions[bot]` の commit として表示される
- `claude.yml` の checkout から `persist-credentials: false` を外すと、push が `github-actions[bot]` として行われ、権限不足で失敗する
- カバー画像の検査は追加された記事だけを見るので、既存の記事から `local_image` を消しても検出しない
- `ogp.webp` が今のタイトルとタグで作られているかは検査しない（ADR-0007 から変わらない）
- これまでに public で公開した内容は取り消せない

### Consequences

- `docs/repository-workflow.md` の「Issue による執筆依頼」の節を「Issue の使い方」に書き換えた
- `.github/workflows/claude.yml` の checkout に `persist-credentials: false` を指定した（PR #13）
- `.github/workflows/zola-build.yml` と `.github/workflows/cover-check.yml` を作り、Ruleset の必須チェックに加える
- `CLAUDE.md` にメモリのルールを移す
- `.github/workflows/claude-code-review.yml` に `paths-ignore` と `allowed_bots` を加える。ADR-0007 で未決定とした扱いが、これで決まる
- 下書きの自動化の検討文書と作業ログは、取りやめた記録として残す。続ける作業は作業ログで管理する
