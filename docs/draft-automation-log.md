# 記事の下書き自動化 作業ログ

**開始日**: 2026-11-26
**状態**: 下書きの自動化は取りやめた（2026-11-26）。検討の中で見つけた、自動化と関係なく必要な作業を続ける
**関連文書**: `docs/draft-automation-plan.md`（取りやめた検討の記録）、`docs/architectural-decision.md` ADR-0008、
`docs/repository-workflow.md`

Issue の執筆依頼から下書きの Draft PR を自動で作る仕組みを検討し、取りやめた。その計画と記録、
および検討の中で見つけた課題に対応する作業の計画と記録を残す。
取りやめた理由と決定事項は ADR-0008 に、検討の経緯は `docs/draft-automation-plan.md` にある。

## 計画

各作業は `docs/repository-workflow.md` に従い、ブランチと PR で行う。
GitHub の設定（Ruleset、App）を変えるときは、その都度オーナーの承認を得る。
作業の番号は、取りやめる前の計画から変えていない。

作業は次の順に進め、作業ごとに1つの PR にする（2026-11-26 にオーナーが承認）。
必須チェックを加える 1-2 と 1-3 で、失敗させる試験の PR をほかの変更と混ぜないためである。
PR の作成は Claude が行う。マージは、PR ごとにオーナーの承認を得てから行う。
当初は検査が通ればマージまで Claude が行うとしていたが、サイトの出力を変えない PR を立て続けにマージして
デプロイを6回余分に起こしたため、2026-11-26 にオーナーが承認なしのマージを禁止した。
Ruleset の変更（1-2、1-3）とメモリの削除（1-1）は、そのつどオーナーの承認を得る。

| 順序 | PR | 作業 |
|------|------|------|
| 1 | docs | ADR-0008 とこのログなど、取りやめと続ける作業の文書 |
| 2 | 1-6 の2本 | `image.html` のコメント、`hifi-guitar-lofi-music` のパス |
| 3 | 1-7 | `ogp-check.yml` を `main` への push でも動かす |
| 4 | 1-8 | `claude-code-review.yml` の絞り込みと `allowed_bots` |
| 5 | 1-5 | `/article-publish` の `trash` の修正 |
| 6 | 1-2 | `zola-build.yml` と Ruleset |
| 7 | 1-3 | `cover-check.yml` と Ruleset |
| 8 | 1-9 | `@claude` の権限の確認 |
| 9 | 1-10 | `@claude` の commit の表示名 |
| 10 | 1-1 と 2-1 の残り | メモリのルールの移動と、「draft branch created by automation」の修正 |

### 続ける作業

#### 作業 1-1: メモリのルールを CLAUDE.md に移す

Issue で `@claude` に頼んだ作業は GitHub Actions で動き、リポジトリにあるものしか読めない。
メモリのルールは暗黙のものになりがちなので、CLAUDE.md に明文化する。

変更するもの

- `CLAUDE.md`: `~/.claude/projects/…/memory/` にある執筆と作業のルールを、該当する節（Writing Style など）に書き加える
- `CLAUDE.md`: 「下書き中に `npm run lint` を実行しない」と、メモリの「`zola build` を勝手に走らせない」を、
  Mac での対話の作業に限る書き方にする。Actions 上の作業では実行することを明記する
- メモリ: CLAUDE.md に移したものを削除し、`MEMORY.md` の索引からも外す

完了条件

- [ ] メモリのすべての項目について、CLAUDE.md に移したか、移さない理由を PR の説明に書いた
- [ ] CLAUDE.md に個人的な情報（メールアドレス、私生活の詳細など）が含まれていない。CLAUDE.md は公開される
- [ ] lint と `zola build` のルールが Mac での対話の作業に限られ、Actions 上の作業では実行すると読める
- [ ] 移したメモリが削除され、`MEMORY.md` に残っていない

#### 作業 1-2: PR の必須チェックに `zola build` を加える

今はビルドの失敗がマージ後の `deploy.yml` まで検出されない。

変更するもの

- `.github/workflows/zola-build.yml` を新しく作る
  - `pull_request`（`branches: [main]`）で起動する。`paths:` の絞り込みは付けない。
    必須チェックのワークフローが起動しないと、待機のまま残ってマージできなくなるためである
  - テーマのサブモジュールを取得し、`deploy.yml` と同じ版の Zola（0.23.6）を入れる
  - 出力先を一時ディレクトリにして `zola build` を実行する。`zola check` は使わない
- Ruleset `protect-main` の必須チェックに、このジョブを加える
- `docs/repository-workflow.md` の「検査」「リポジトリの設定」「PR とマージで動くワークフロー」の表に加える
- `.claude/commands/article-publish.md` の手順 5 の、失敗したときに直すチェックの一覧に加える

完了条件

- [x] 記事を含まない PR でもジョブが起動し、成功する
- [x] `{% raw %}` を外すなどしてビルドを壊した試験の PR で、ジョブが失敗し、マージできない
- [x] Ruleset の必須チェックに加わっている（`gh api repos/yostos/blog-yostos/rules/branches/main` で確認）
- [x] 上の文書とコマンドが更新されている

#### 作業 1-3: PR で追加された記事のカバー画像を検査する

CLAUDE.md は新しい記事にカバー画像を必須としているが、検査がない。`ogp-check` と同じく必須チェックで担保する。
作るきっかけは、画像の指定を書かない下書きだった。

変更するもの

- `.github/workflows/cover-check.yml` を新しく作る
  - `pull_request`（`branches: [main]`）で起動し、`paths:` の絞り込みは付けない
  - base との差分（`--diff-filter=A`）で、PR で追加された `content/blog/**/index.md` を取り出す
  - それぞれについて、frontmatter の `[extra]` に `local_image` があり、そのファイルが記事のディレクトリにあることを確かめる。
    frontmatter は TOML として読む
  - 本文冒頭の画像の行は求めない。意図して置かない記事がある
  - 追加された記事がなければ、検査を省いて成功で終える
- Ruleset の必須チェックに加える
- `docs/repository-workflow.md` の各表に加える
- `.claude/commands/article-publish.md` の手順 5 のチェックの一覧に加える

完了条件

- [ ] `local_image` のない記事を追加した試験の PR で失敗する
- [ ] `local_image` はあるがファイルがない記事を追加した試験の PR で失敗する
- [ ] カバー画像のある記事を追加した PR と、既存の記事だけを変えた PR で成功する
- [ ] Ruleset の必須チェックに加わっている
- [ ] 上の文書とコマンドが更新されている

#### 作業 1-5: `/article-publish` が OGP 画像のない記事で止まらないようにする

変更するもの

- `.claude/commands/article-publish.md` の手順 2: `ogp.webp` がなければ `trash` を飛ばし、`npm run ogp` だけを実行する。
  今は `trash` が失敗して、新しい記事の公開の手順が止まる

完了条件

- [ ] `ogp.webp` のない記事で、手順 2 が止まらずに OGP 画像を作る

#### 作業 1-6: 検討中に見つけた誤りを直す

それぞれ別の PR にする。

変更するもの

- `templates/components/image.html`: 「画像が見つからなくてもページは壊れない」というコメントを直す。
  `get_url(cachebust=true)` はファイルがないとエラーを返す
- `content/blog/2026/03/hifi-guitar-lofi-music/index.md`: `local_image` の絶対パス
  `/blog/2026/03/hifi-guitar-lofi-music/cover.webp` を直す

完了条件

- [ ] `image.html` のコメントが実際の動作と一致している
- [ ] `hifi-guitar-lofi-music` のカバー画像が記事一覧と記事のページで表示される（オーナーがプレビューで確認）

#### 作業 1-7: `ogp-check.yml` を `main` への push でも動かす

当初は「`textlint.yml` の `push: main` を削除する」としていた。マージ後に同じ検査を繰り返すだけだと考えたためである。
これは誤りだった。Ruleset はマージの前にブランチを最新にすることを求めていないので、
PR の検査の後に別の PR がマージされると、実際に `main` にできる組み合わせは検査されない。
`main` での実行には、マージ後の状態を確かめるという役目がある。削除の PR #17 は閉じた。

あわせて検査ごとに見直し、PR と `main` への push のどちらで動かすかを `docs/repository-workflow.md`
「PR とマージで動くワークフロー」の表にまとめた（2026-11-26 にオーナーが承認）。
リポジトリ全体を見る `ogp-check.yml` が、`main` で動いていなかった。

- `zola-build.yml`（1-2）は `main` で動かさない。`deploy.yml` が同じビルドをする
- `cover-check.yml`（1-3）は `main` で動かさない。PR で追加された記事だけを見るので、`main` では対象を決められない

変更するもの

- `.github/workflows/ogp-check.yml`: `on:` に `push: branches: [main]` を加える
- `README.md` の Workflows の表と CI/CD Pipeline の図: OGP Check のトリガーを直す
- `docs/repository-workflow.md` の表: 「作業 1-7 で加える」を消す

完了条件

- [x] PR と、マージ後の `main` の両方で `ogp-check` が動き、成功する
- [x] `textlint.yml` の `push: main` が残っている
- [x] 上の文書が実際の動作と一致している

#### 作業 1-8: `claude-code-review.yml` を機能の変更の PR だけで動かす

ADR-0007 から未決定だった扱いを、2026-11-26 にオーナーと決めた（ADR-0008 の決定6）。

- 今は、すべての PR の作成時と push のたびに、汎用のコードレビューの観点でレビューしてコメントする。
  2026-11-25 からはすべての変更が PR を通るので、記事の公開でも毎回動く
- PR #9 と PR #11 では実際に不具合を見つけたので、削除はしない
- 記事の文章のレビューは、手元の `/article-review` が担う。コード向けの観点で記事を見る意味は薄い
- `@claude` が push した PR では、bot が起動した実行を拒むので必ず失敗する（2026-11-26 の試験で確認）。
  Claude が書いた機能の変更こそ、マージ前に別の目で見る価値がある

変更するもの

- `.github/workflows/claude-code-review.yml`
  - `on.pull_request` に `paths-ignore: ['content/**']` を付ける。記事だけを変える PR では動かず、
    記事と機能の両方を変える PR では動く。必須チェックではないので、絞り込みで PR が「待機中」のまま残ることはない
  - `claude-code-action` の `allowed_bots` に `claude` を加える。試験のエラーで示された actor 名である
- `docs/repository-workflow.md` の「PR とマージで動くワークフロー」の表と、「残すかどうかは未決定」の記述を直す

完了条件

- [ ] 記事だけを変える PR で、`claude-review` が動かない
- [ ] 機能の変更を含む PR で、`claude-review` が動いてコメントを残す
- [ ] `@claude` が push した PR で、`claude-review` が失敗せずにコメントを残す
- [ ] `docs/repository-workflow.md` の記述が実際の動作と一致している

#### 作業 1-9: 書き込み権限のない人の `@claude` で Claude が起動しないことを確かめる

このリポジトリは public で、誰でも Issue を立て、コメントできる。

作業

- `claude-code-action` が依頼者の権限を確かめているかを、ソースで調べる
- 確かめていない、または確信が持てない場合は、`claude.yml` の起動条件に、
  依頼者がオーナーであること（`author_association`）を加える

完了条件

- [x] 書き込み権限のない人の依頼で起動しないことが、根拠とともにこの文書の「記録」に書かれている
- [x] `docs/repository-workflow.md`「Issue の使い方」の「まだ確かめていない」という記述が直っている

#### 作業 1-10: `@claude` の commit を `claude[bot]` として表示する（優先度は低い）

`claude-code-action` の既定の `bot_id` は `github-actions[bot]` のものなので、
`@claude` の commit がほかの自動処理の commit と区別できない。

作業

- `claude.yml` で `bot_id` と `bot_name` を `claude[bot]` のものにする

完了条件

- [ ] `@claude` が作った commit が、GitHub の画面で `claude[bot]` の commit として表示される

#### 作業 2-1: 取りやめに合わせて文書を直す

完了条件

- [x] `docs/repository-workflow.md` の「Issue による執筆依頼」が、Issue の使い方と `@claude` での依頼の仕方に書き換わっている
- [x] ADR-0008 が、執筆依頼を受けない決定と、続ける作業の決定を記録している
- [x] `docs/draft-automation-plan.md` の状態が「取りやめ」になり、理由が書かれている
- [ ] `CLAUDE.md` の Git Operations と `.claude/commands/article-publish.md` の手順 0 にある
  「draft branch created by automation」を、`@claude` が作ったブランチの例に直している

### 済んだ作業

#### 段階2: Claude GitHub App のトークンによる push の確認

下書き担当の実行環境を決めるために行った。下書きの自動化は取りやめたが、確認した内容は Issue の `@claude` の作業にそのまま当てはまる。

- [x] App の有無と、App のトークンで必須チェックが起動するかが、この文書の「記録」に書かれている
- [x] 実行環境と認証方式が決まり、ADR に記録されている（その後、自動化の取りやめに伴い ADR-0008 から外した）

### 取りやめた作業

下書きの自動化を取りやめたので、次の作業は行わない。

- 作業 1-4: `/article-images` を作る。画像の指定を書かない下書きを仕上げるためのコマンドだった
- 作業 1-5 のうち、Draft PR を `gh pr ready` で Ready for review に変える手順
- 段階3: 下書き担当の実装
- 段階4: 通し試験
- 段階5: 検討文書の `docs/repository-workflow.md` への統合（作業 2-1 に置き換えた）
- 未決定だった、処理中の記録方法、下書きの commit の author 名、Draft PR の通知の方法、下書き担当への指示の形

## 記録

### 2026-11-26 段階2: Claude GitHub App の確認

App が入っているかと、その権限を確かめた。

- オーナーの GitHub の設定画面（Installed GitHub Apps）で、Claude（developed by anthropics）が入っていることを確かめた。
  Repository access は「Only select repositories」で、`yostos/blog-yostos` が含まれている
- 設定画面に表示された App の権限は次のとおり
  - Read: Dependabot alerts、administration、commit statuses、merge queues、metadata
  - Read and write: actions、checks、code、discussions、issues、pull requests、repository creation、repository hooks、workflows
- ブランチの作成、Draft PR の作成、Issue へのコメントに必要な権限（code、pull requests、issues の書き込み）はそろっている。
  administration は読み取りだけなので、App のトークンで Ruleset を変えることはできない
- workflows の書き込み権限があるので、App のトークンでは `.github/workflows/` のファイルも変更できる。
  下書き担当が触ってよいのは記事のディレクトリだけなので、許可するツールで絞る必要がある。
  ワークフローを変えた PR も、`main` に入るには必須チェックとマージを通る
- PR #11 のコメントは `claude` App を経由して `claude[bot]` が書いている。
  `claude[bot]` のコメントで `claude.yml` が15回起動している（いずれも `if:` で skipped）。
  App のトークンによる操作でワークフローが起動することの証拠になる。ただし PR への push での起動は、まだ確かめていない
- `claude-code-action` の既定では Claude は PR を作らず、作成ページへのリンクを返す。
  `claude_args` で `gh pr create` を許可すれば作れる（action の `docs/faq.md`、`docs/security.md`）
- action の、書き込み権限のない作成者に対してコマンドを禁止する制限（`restrict_untrusted_prs`）は、
  PR にだけ適用され、Issue には適用されない（`src/github/validation/untrusted-pr.ts:192` の `!context.isPR`）

### 2026-11-26 段階2: App のトークンによる push の試験（1回目、push に失敗）

App のトークンで PR に push したときに、必須チェックが起動するかを試した。

- `main` から `test/app-token-trigger` ブランチを API で作り、`docs/app-token-test.md` を追加して Draft PR #12 を作った。
  オーナーの認証で作った Draft PR でも、`textlint`、`ogp-check`、`claude-review` が起動し、成功した
- PR に `@claude` でファイルに1行足して push するよう依頼した。`claude.yml` が起動し、Claude は commit したが、push は
  `403: Permission to yostos/blog-yostos.git denied to github-actions[bot]` で失敗した
- 実行ログでは、action は OIDC で App のトークンを取得し（`App token successfully obtained`）、remote の URL にそのトークンを設定している。
  一方、その前の `actions/checkout@v6` が `persist-credentials: true`（既定）で `GITHUB_TOKEN` の認証ヘッダー
  （`http.https://github.com/.extraheader`）を git の設定に残している。git はこのヘッダーを優先したため、
  push は `GITHUB_TOKEN`（`claude.yml` では `contents: read`）で行われ、拒否された
- このため、App のトークンによる push で必須チェックが起動するかは、まだ確かめられていない。
  checkout に `persist-credentials: false` を指定すれば、App のトークンで push されるはずである。
  `issue_comment` で起動するワークフローは `main` の定義で動くので、再試験には `claude.yml` を直す PR のマージが要る
- 下書き担当のワークフローを作るときも、checkout に `persist-credentials: false` を指定する必要がある

### 2026-11-26 段階2: App のトークンによる push の試験（2回目、成功）

PR #13 で `claude.yml` の checkout に `persist-credentials: false` を指定し、squash merge した。その後、PR #12 で再び試した。

- 1回目の再依頼は `@claude（再試験）` と全角の括弧を続けて書いたため、action がトリガーとして認識しなかった
  （`No trigger was met for @claude`）。`@claude` の後に空白を置いて依頼し直した
- `claude[bot]` が commit `eb740d7` を push した。push は成功した
- この push で、次のワークフローが `pull_request` イベント、actor `claude[bot]` で起動した
  - `textlint`: 成功
  - `ogp-check`: 成功
  - `claude-review`: 失敗。`Workflow initiated by non-human actor: claude (type: Bot). Add bot to allowed_bots list` で、
    action が bot の起動を既定で拒否するためである。必須チェックではないので、マージは妨げない
- 結論: App のトークンによる push では、必須チェックが起動する。下書き担当を Actions で動かしても、
  Draft PR の作成時から検査が動く
- 下書き担当の Draft PR では `claude-review` が毎回失敗する。`claude-code-review.yml` を残すなら、
  bot の PR では動かさないか、`allowed_bots` に `claude` を加えるかを決める必要がある（未決定の事項に関わる）
- commit の git の author は `claude[bot] <41898282+claude[bot]@users.noreply.github.com>` だった。
  41898282 は `github-actions[bot]` のユーザー ID なので、GitHub の画面では `github-actions[bot]` の commit として表示される。
  action の `bot_id` の既定値によるもので、下書きのコミットの author 名を決めるときに考慮する
- 試験の後、PR #12 をマージせずに閉じ、`test/app-token-trigger` ブランチを削除した

### 2026-11-26 画像の指定とファイルの食い違いによるビルドの試験

`docs/draft-automation-plan.md`「カバー画像と OGP 画像の扱い」の、テンプレートと Zola のソースから導いた推論を、実際のビルドで確かめた。

リポジトリをスクラッチ領域に複製し（`node_modules`、`public`、`.git` を除く）、試験用の記事
`content/blog/2026/11/zz-build-test/index.md` を追加して、ケースごとに `zola build -o <一時ディレクトリ>` を実行した。
Zola は 0.23.6。作業ツリーには触れていない。

| ケース | 結果 | エラー |
|------|------|------|
| A: 画像の指定なし | 成功 | なし |
| B: `social_media_card = "ogp.webp"` あり、`ogp.webp` なし | 失敗（exit 1） | `Could not find social media card image. Tried: …` |
| C: `local_image = "cover.avif"` だけあり、`cover.avif` なし | 成功 | なし |
| D: 本文冒頭に `{{< image src="cover.avif" … />}}` あり、`cover.avif` なし | 失敗（exit 1） | `` `get_url`: Could not find or open file cover.avif `` |

いずれも推論どおりで、下書きでは画像の指定を3つとも書かないという決定（ADR-0008 の決定 4）の前提が確かめられた。
B と D のエラーはサイト全体のビルドを止める。C は記事一覧のサムネイルがリンク切れになるだけで、ビルドは止まらない。

### 2026-11-26 段階2: 実行環境と認証方式の決定

2回目の試験の結果を受けて、オーナーが GitHub Actions と Claude GitHub App のトークンに決めた。
ADR-0008 に決定7として加え、Status から「実行環境は未決定」を外した。段階2の完了条件はすべて満たした。

### 2026-11-26 下書きの自動化の取りやめ

このリポジトリは public なので、Issue の執筆依頼と下書きの Draft PR が誰でも読めることを、オーナーが指摘した。
非公開に保つ案として、private リポジトリを別に作る案と、ブログのリポジトリを private にする案を調べた。

- 個人アカウントの private リポジトリで Ruleset を使うには GitHub Pro 以上が要る
- private リポジトリの Actions は、標準の Linux ランナーが1分 $0.006 で、無料プランには月 $12 の枠が含まれる
- `config.toml` の `show_remote_source` と `show_remote_changes` により、全ページにリポジトリへのリンクがある。
  記事本文からスクリプトにリンクしている記事も3本ある

オーナーは、Issue で執筆依頼を受けないことに決めた。Issue はデザインや機能の修正、場合によっては記事の修正に使い、
Claude に頼むかどうかは `@claude` を書くかどうかで決める。
前の記録で ADR-0008 に加えた決定7（Actions と App のトークンの採用）は、ADR-0008 の書き直しで外した。
計画を、自動化と関係なく続ける作業と、取りやめる作業に分け直した。

### 2026-11-26 `claude-code-review.yml` の扱いの決定

ADR-0007 から未決定だった扱いを、オーナーと決めた。削除せず、記事だけを変える PR では動かさず、
`@claude` が push した PR でも動くようにする。理由と変更内容は作業 1-8 に、決定は ADR-0008 の決定6に書いた。

### 2026-11-26 作業 1-7 の見直し

`textlint.yml` の `push: main` を削除する PR #17 を作ったところで、README の Textlint のバッジが `main` での実行結果を表示しており、
更新されなくなることに気づいた。一般的な運用を調べる中で、`main` での実行が、PR の検査とマージ後の状態の食い違いを拾う役目を持つことが分かった。
このリポジトリの Ruleset は `strict_required_status_checks_policy` が false で、食い違いが起こりうる。
PR #17 は閉じ、作業 1-7 を「`ogp-check.yml` を `main` への push でも動かす」に書き換えた。

### 2026-11-26 作業 1-7: `ogp-check.yml` を `main` でも動かす

PR #20 で `ogp-check.yml` に `push: main` を加え、README の表と図、`docs/repository-workflow.md` の表を直した。
マージ後の `main`（`92370ea`）で `OGP Check` が動き、成功した。`Textlint` も引き続き `main` で動いている。

### 2026-11-26 作業 1-8: `claude-code-review.yml` の絞り込み

PR #21 で `paths-ignore: content/**` と `allowed_bots: claude` を加えた。
`allowed_bots` は bot 名の末尾の `[bot]` を無視して比べるので、`claude` と `claude[bot]` のどちらでも同じである（`src/github/validation/actor.ts`）。

PR #21 自身では、`claude-review` は成功と表示されたがレビューは行われなかった。`claude-code-action` は、
ワークフローのファイルがデフォルトブランチのものと一致しないと実行を飛ばす
（`Skipping action due to workflow validation`）。変更はマージ後の PR から効くので、完了条件は後の PR で確かめる。

### 2026-11-26 作業 1-5: `/article-publish` の手順 2

`trash` は存在しないファイルを渡すと終了コード 5 で失敗することを確かめた。
`ogp.webp` がない新しい記事では `trash` を飛ばし、`npm run ogp` だけを実行する手順にした。
完了条件は、次に新しい記事を公開するときに確かめる。

### 2026-11-26 作業 1-9: 書き込み権限のない人の `@claude`

`claude-code-action` のソースで確かめた。`claude.yml` は `@v1` を使っており、確認した時点の `v1` タグは commit `c148296601107048fe24605a3dfb32a317a6f4c7` を指していた。
`v1` は新しい版が出ると指す先が変わるので、見直すときはこの commit のソースを読む。`claude.yml` は変えない。

- `src/entrypoints/run.ts` は、Issue と PR のイベントで `checkWritePermissions` を呼び、
  権限がなければ `Actor does not have write permissions to the repository` で終える
- `src/github/validation/permissions.ts` は、依頼者（コメントや Issue を書いた人）の権限を
  collaborator の API で調べ、`admin` か `write` のときだけ通す
- この確認を外す `allowed_non_write_users` は、`claude.yml` で指定していない
- bot の依頼は、別の確認（`checkHumanActor`）で `allowed_bots` にないものが拒否される。`claude.yml` は `allowed_bots` を指定していない

ワークフローの起動条件は `@claude` を含むかだけなので、第三者が書いた場合も実行は始まり、権限の確認で失敗して終わる。
Claude は動かず、Secrets も使われない。失敗した実行が Actions に残るだけなので、起動条件に作成者の条件は加えない。

### 2026-11-26 作業 1-10: `@claude` の commit の表示名

`claude-code-action` の `bot_id` の既定値は `41898282` で、これは `github-actions[bot]` のユーザー ID である。
`gh api 'users/claude[bot]'` で `claude[bot]` の ID が `209825114` であることを確かめ、`claude.yml` に `bot_id` と `bot_name` を指定した。
完了条件は、次に `@claude` が commit したときに確かめる。

### 2026-11-26 作業 1-2: `zola build` を PR の必須チェックに加える

PR #23 で `.github/workflows/zola-build.yml` を作った。Zola は `deploy.yml` と同じ 0.23.6 で、出力先は `$RUNNER_TEMP/public` にした。
あわせて `docs/repository-workflow.md`、README、`/article-publish` の手順 5 を直した。

- PR #23（記事を含まない PR）で `zola-build` が起動し、15秒で成功した
- オーナーの承認を得て、Ruleset `protect-main` の必須チェックに `zola-build` を加えた。
  `gh api repos/yostos/blog-yostos/rules/branches/main` で、必須チェックが `textlint`、`ogp-check`、`zola-build` の3つであることを確かめた
- 試験の PR #24 で、`image.html` に存在しない関数の呼び出しを入れた。`zola-build` が
  `Unknown function this_function_does_not_exist` で失敗し、PR の状態が `BLOCKED` になった。PR #24 はマージせずに閉じた
