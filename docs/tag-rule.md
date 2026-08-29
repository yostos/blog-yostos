# ブログタグ体系

## 構造

タグは2つのレイヤーに分けます。

- **第1層**: 記事の大分類
- **第2層**: いずれか1つの第1層に所属する下位分類

## 第1層

第1層は以下の7種のみです。

- Tech
- Current Affairs
- Creative
- Entertainment
- Gadget
- Trivialities
- Automotive

## 第2層

第2層のタグは、必ずいずれかの第1層に所属させます。

（未定）

## タグセットの管理

タグセットは以下の2ファイルで管理します。形式の選定理由は
`docs/architectural-decision.md` の ADR-0003 を参照してください。

| ファイル | 役割 | 編集方法 |
|---|---|---|
| `data/tagset.toml` | 第1層・第2層の定義と所属関係 | 手動 |
| `data/tag-vectors.json` | 第2層タグのベクター値 | スクリプトで生成 |

### `data/tagset.toml`

第1層は `[[layer1]]`、第2層は `[[layer2]]` で記述します。
第2層の `parent` には、所属する第1層の `name` を1つだけ指定します。

```toml
schema_version = 1

[[layer1]]
name = "Tech"
description = "ソフトウェア、クラウド、AI、開発ツールなど技術全般。"

[[layer1]]
name = "Guitar"
description = "ギターの演奏、機材、練習。"

[[layer2]]
name = "Generative AI"
parent = "Tech"
description = "生成AIモデルとその活用。LLM、画像生成、プロンプト設計。"

[[layer2]]
name = "Guitar Pedals"
parent = "Guitar"
description = "エフェクターペダルのレビューとセッティング。"
```

タグを追加するときは `[[layer2]]` のブロックを書き足すだけです。
ベクター値はこのファイルには書きません。
`name` は英語、`description` は日本語で記述します。

### `data/tag-vectors.json`

第2層タグごとのベクター値を保持します。手では編集しません。

```json
{
  "schema_version": 1,
  "model": "voyage-4",
  "dim": 1024,
  "input_type": "document",
  "normalized": true,
  "updated": "2026-08-29",
  "tags": {
    "Generative AI": {
      "article_count": 54,
      "vector": [0.0132, -0.0451]
    },
    "Guitar Pedals": {
      "article_count": 0,
      "vector": null
    }
  }
}
```

`vector` は実際には `dim` で示した要素数の配列です。上記は例のため省略しています。

`vector` はそのタグを持つ全記事のベクターを平均し、
L2再正規化した値です。

算出は常に全記事を対象とした一括更新で、
ファイル全体を書き直します。タグ単位での部分更新は行いません。
記事が0件のタグは平均を取れないため `vector` を `null` とし、
推薦の候補から外します。

`model` と `dim` は、埋め込みモデルを変更した際に
全タグの再計算が必要だと判定するために保持します。
モデルの選定理由と呼び出し方は
`docs/architectural-decision.md` の ADR-0004 を参照してください。

## ベクター値の算出

算出は `scripts/build-tag-vectors.py` が行います。
全記事を Voyage AI で埋め込み、第2層タグごとに平均して
`data/tag-vectors.json` を書き出します。

```bash
python3 scripts/build-tag-vectors.py            # 算出して書き出す
python3 scripts/build-tag-vectors.py --dry-run  # 対象と概算トークン数のみ表示、APIは呼ばない
```

`VOYAGE_API_KEY` を環境変数に設定して実行します。
未設定なら API を呼ぶ前に終了します。キーはコマンドライン引数では受け取りません。
算出はローカルで実行するため、GitHub Actions のシークレットには登録しません。

### 入力

`content/**/index.md` のうち、第2層タグをちょうど1つ持つ記事が対象です。
frontmatter の `title` と `description` に本文の全文を続けたものを埋め込みます。

除去するのは HTML タグとショートコード（`{{ }}`、`{% %}`、HTML コメント）だけです。
Markdown 記法は意味を変えないため、コードブロックは技術記事の主題を
直接示すため、いずれも残します。切り詰めもしません。

第2層タグが0個または2個以上の記事は対象から外し、
理由とともに標準エラー出力に一覧を出します。

### 呼び出し

| 項目 | 値 |
|---|---|
| モデル | `voyage-4` |
| `output_dimension` | 1024 |
| `input_type` | `document` |
| `truncation` | `true` |
| バッチ | 48件ずつ、並列3 |

429 が返った場合は最大6回まで指数バックオフで再試行します。
選定理由と API の詳細は `docs/architectural-decision.md` の ADR-0004 を参照してください。

### 出力

タグごとに、そのタグを持つ記事のベクターを平均し、L2再正規化した値を
`data/tag-vectors.json` に書き出します。ファイル全体を毎回書き直すため、
タグ単位の部分更新はありません。記事が0件のタグは `vector` を `null` にします。

### 実行のタイミング

不定期に、必要になった時点で手動で実行します。
タグの新設・改名や記事の追加がまとまった段階が目安です。

全記事は1,054,461文字で、1回の実行に約538Kトークンを消費します。
無料枠200Mトークンの範囲で約370回実行できます。

### 実行実績

| 日付 | 記事 | タグ | 消費トークン | 所要 | 出力 |
|---|---:|---:|---:|---:|---:|
| 2026-08-30 | 388 | 47 | 542,400 | 7秒 | 1.4 MB |

初回の算出です。全47タグに記事があり、`vector` が `null` のタグはありません。
全タグのベクターの長さは1.0、次元は1024で、`tagset.toml` の定義と過不足なく一致します。

## タグ付けスキル

記事のタグを決めて frontmatter にセットするスキルです。
`.claude/commands/article-tag.md` に置きます。

### 手順

1. `data/tag-vectors.json` を読み、`model` と `dim` が
   `scripts/build-tag-vectors.py` の設定と一致するか確認する。
   一致しなければ比較が成立しないため、再算出を促して止める
2. 対象記事の埋め込み対象テキストを作る。
   `title` + `description` + 本文全文、除去は HTML タグとショートコードのみ。
   centroid の算出と同じ作り方でなければ比較が成立しないため、
   `build-tag-vectors.py` と処理を共有する
3. Voyage AI で埋め込む。`voyage-4`、`output_dimension` 1024、
   `input_type` は `document`
4. 各第2層タグのベクターと内積を取る。双方とも長さ1なのでこれがコサイン類似度になる。
   `vector` が `null` のタグは候補から外す
5. 最も類似度の高い第2層タグと、その親の第1層タグを frontmatter に書き込む。
   第1層を先頭に置く

セットしたタグをそのまま使うか書き換えるかは著者が判断します。
参考として、実測では最上位のタグが正解と一致する割合は75.0%、
上位3件のいずれかが正解である割合は88.9%でした。

### 注意点

- 執筆直後の記事は `tag-vectors.json` に含まれていないが、
  問題はない。自分自身を含まない条件は実測（leave-one-out）と同じである
- 既存のどのタグとも類似度が低い記事は、タグ新設の検討対象になる。
  新設は `tagset.toml` を手で編集し、その後に再算出する

## TODO

1. `data/tagset.toml` の最終化（Toshiyuki）── 完了
2. `tagset.toml` から逸脱する記事の一覧作成 ── 完了
3. 逸脱記事のタグの補正実施（Toshiyuki）── 完了
4. ベクター値算出ロジックの作成（Voyage AI の `voyage-4` を使用）── 完了
5. 記事内容から推奨タグをベクター値で算出するスキルの開発
6. `VOYAGE_API_KEY` の取得と保管方法の決定（項目4の前提）── 完了
7. ベクター値の更新タイミングと実行者の決定 ── 完了（不定期・手動実行）

タグ補正の前に centroid を算出すると誤ったタグ付けを取り込むため、
項目3が完了してから項目4に進みます。残るは項目5です。

## 進捗（2026-08-30 時点）

項目1から項目3が完了しました。全388記事のタグを月ごとに確認し、
`tagset.toml` を並行して整理しています。

### 記事タグの原則

見直しを通じて、記事のタグは次の形に統一しました。

- 第1層タグを1つ、第2層タグを1つ持つ
- 第1層タグを先頭に置く
- 第2層タグの親は、その記事の第1層タグと一致する

388記事すべてがこの形に揃っており、逸脱はありません。
`tagset.toml` に定義のないタグを持つ記事もありません。

### 現在の構成

第1層は7種、第2層は47件です。括弧内は記事数です。

| 第1層 | 第2層 |
|---|---|
| Tech (15) | Generative AI(49), Cloud(18), Weblog(14), Security(13), CLI(12), Software(7), Web(5), IT Governance(4), Software Engineering(4), Font(4), Certification(4), Documentation(2), API(2), Programming(1), Editor(1) |
| Current Affairs (7) | Politics(16), Business(12), Weekly Buzz(10), Geopolitics(7), Disaster(6), Media(3), Show Business(2) |
| Creative (3) | Guitar Play(47), Photography(16), Movie(15) |
| Entertainment (7) | Game(15), Films(10), Books(4), Concerts(2), Art(2), Manga(1), Music(1) |
| Gadget (8) | Guitar(26), Drone(11), Peripherals(5), Camera(3), Computers(3), Apparel(1), Everyday Goods(1), Mobile(1) |
| Trivialities (5) | Gourmet(9), Travel(6), Life(6), Insights(3), Seasons(2) |
| Automotive (2) | Cars(1), SUBARU(1) |

初期化時の第1層は10種でしたが、Guitar・Drone・Photography を第2層に降ろしました。
Guitar と Drone は Gadget 配下、Photography は Creative 配下です。

### 実施した統合・改名

| 変更前 | 変更後 | 理由 |
|---|---|---|
| SSG, Zola | Weblog | ブログ運営に集約 |
| Python, Node, Go の一部 | Programming | 言語別タグを廃止 |
| Go の一部 | CLI | コマンドラインツールの記事 |
| Claude Code, Claude, Anthropic | Generative AI | 製品名・企業名タグを廃止 |
| AWS, Cloudflare, Google Cloud | Cloud | ベンダー別タグを廃止 |
| DNS, Network | Security | メール認証・通信の記事を集約 |
| Note-taking | Documentation | 文書の作成と管理に一般化 |
| Mac, Apple | 削除 | 内容に応じ Software / CLI へ分配 |
| Takaichi | Politics | 人物名タグを廃止 |
| China, Korea | Geopolitics | 国別から国家間の力学へ |
| Old Media | Media | 評価を含む語を避け、対象を広げた |
| Splatoon | Game | 作品名タグを廃止 |
| Movies, Anime, Video | Films / Movie | 鑑賞は Films、制作は Movie |
| HHKB, Keyboard, Mouse | Peripherals | PC周辺機器に集約 |
| Guitar Pedals | Guitar | 機材として一体に扱う |
| Music | Guitar Play | 演奏記事に集約 |
| Photo Friday | Photography | 企画名タグを廃止 |
| Motor Cycle | 削除 | 該当記事が Business へ移ったため |
| PDF, Chiba, Career, Writing, Sea, River, Lake, Waterfall, IBM, Flickr, Governance, Ibaraki, tag, Tips | 削除 | 記事の性格を他タグで表せるため |

記事が0件になった TypeScript, Productivity, Mail, Accessibility, OSS,
Task Management, Hardware, Music Production, Design, Sake も削除しました。

新設したタグは Politics, Geopolitics, Media, Show Business, Disaster, Business,
Peripherals, Camera, Computers, Mobile, Apparel, Everyday Goods, Movie,
Guitar Play, Insights, Concerts, Music, Documentation, Cars, SUBARU です。

### タグ名を決めるときの基準

新設時は、ベクターでの推薦精度を落とさないことを基準にしました。

- 親と意味が重なる広い語を避ける（Social Issues を Current Affairs 配下に置かない）
- 既存タグと語彙が重なる語を避ける。Gadget 配下の日用品タグに Gear や Tools を
  使うと、centroid が Guitar や CLI と近接して判別できなくなるため
  `Everyday Goods` とした
- 製品名・企業名・人物名・作品名はタグにしない

### 残っている作業

- `Automotive` 配下が2件と少ない。「Goodbye Super Cub!」は二輪を手放す記事だが
  `Motor Cycle` の削除に伴い `Current Affairs, Business` にしてある
- 第2層を1つに絞った結果、Tech 配下の Programming と Editor が各1件になっている
- 推薦スキル（項目5）は未着手
