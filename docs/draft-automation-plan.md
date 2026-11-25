# 記事の下書き自動化（取りやめ）

**作成日**: 2026-11-26
**状態**: 取りやめ（2026-11-26）。この文書は検討の記録として残し、以降は更新しない
**関連**: `docs/repository-workflow.md`、`docs/architectural-decision.md` ADR-0008、
`docs/draft-automation-log.md`（作業計画と記録）、`docs/github-flow-migration-log.md`

GitHub Issue に書いた執筆依頼から、記事の下書きを自動で作り、Draft PR として出す仕組みを検討した。
`main` への変更はすべて PR のマージで行うという `docs/repository-workflow.md` のルールを前提とした。

## 取りやめた理由

このリポジトリは public なので、Issue の本文、下書きのブランチ、commit、Draft PR はすべて誰でも読める。
執筆依頼には記事にするか決まっていない構想が入り、仕上げる前の下書きも公開されることになる。
非公開に保つには、private リポジトリを別に作るか、ブログのリポジトリを private にする必要があり、
どちらも効果に見合わない（ADR-0008）。

このため、Issue で執筆依頼を受けないことにした。Issue はデザインや機能の修正、場合によっては記事の修正に使い、
Claude に頼むときは `@claude` を書く（`docs/repository-workflow.md`「Issue の使い方」）。

検討の中で見つけた課題のうち、自動化と関係なく対応すべきものは、`docs/draft-automation-log.md` の作業として続ける。
以下の節は取りやめた時点の内容のままで、「未決定の事項」などは決めないまま終えた。

## 手順案

1. **依頼を書く。** オーナー、またはオーナーの依頼を受けた Claude が、執筆依頼を Issue の本文に書き、
   `article-request` ラベルを付ける
2. **下書きを作る。** GitHub Actions か Raspberry Pi 4 上の Claude Code が、Issue をもとに下書きを書き、
   Draft PR を作る。詳細は「ステップ 2 の詳細手順」の節に定める
3. **仕上げる。** オーナーが Draft PR の作成を通知で知り、Mac の Claude Code でそのブランチをチェックアウトして仕上げる。
   タグと画像の指定（カバー画像、`local_image`、本文冒頭の画像の行、`social_media_card`）もここで付ける。
   画像の指定は `/article-images` で行う（`docs/draft-automation-log.md` 作業 1-4）
4. **公開する。** `/article-publish` で OGP 画像を作り、Draft を Ready for review に変え、
   検査が通ったら squash merge して `main` を更新する（Ready への変更は作業 1-5 で加える）
5. **自動で動く。** CI がビルドしてデプロイし、Bluesky に投稿する。Issue は `Closes` によって自動で閉じる

## ステップ 2 の詳細手順

下書きを作る Claude（以下、下書き担当）が行う手順である。無人で動くので、途中でオーナーに質問しない。

0. **受け付ける。** open の Issue に `article-request` ラベルが付いていることを確かめる。
   同じ Issue を二重に処理しないよう、処理中であることを Issue に記録する（方法は未決定）
1. **依頼の主旨を理解する。** 読むのは Issue の本文だけで、コメントは読まない。
   曖昧な点があっても止まらず、置いた前提を書き留めて進める
2. **記事のパスを決め、ブランチを切る。** スラッグを決め、記事を `content/blog/YYYY/MM/<slug>/index.md` に置く。
   ブランチは `content/<slug>` とする。ブランチ名と記事のディレクトリ名はスラッグから作るので、ブランチより先に決める
3. **既存の記事を調べる。** 同じ題材の記事がないか、内部リンクを張るべき関連記事やシリーズの前回がないかを調べる。
   シリーズの記事では前回へのリンクを張り、次回予告は書かない
4. **調べて情報をまとめる。** Issue の参考情報を中心に調べる。一次情報で裏を取り、裏が取れないことは書かない。
   報道機関のサイトは References に載せない
5. **ルールに従って書く。** CLAUDE.md の執筆ルール（frontmatter、description、敬体、目次、コンポーネントなど）に従う
   - タグは書かない。記事の完成後にオーナーが付ける
   - `social_media_card`、`local_image`、本文冒頭の画像の行は書かない。OGP 画像とカバー画像も作らない
     （「カバー画像と OGP 画像の扱い」の節）
   - 本文中の `{{ }}`、`{% %}`、`{# #}` は `{% raw %}` で囲む
6. **自己レビューをする。** `/article-review` の観点で見直す。ただし、タグと画像の指定がないことの指摘は、
   仕上げで足すものなので対応しない。最後に通して読み直す
7. **機械的な検査をする。** 次をすべて通す
   - `npm run lint`。指摘は直す。`textlint-disable` で回避しない
   - frontmatter が TOML として読めること
   - `lychee` による記事内の外部リンクの確認
   - `zola build`（出力先は一時ディレクトリ）
8. **commit して push する。** `git add .` で追加し、接頭辞 `content:` で commit して、ブランチを push する
9. **Draft PR を作る。** タイトルは `content: add <topic> article` の形にする。説明には次を書く
   - `Closes #<Issue 番号>`
   - 使った出典
   - 置いた前提と、裏が取れなかった点
   - 直せなかった lint の指摘
10. **Issue に結果を書く。** PR へのリンクを Issue にコメントする。途中で失敗したら、理由をコメントし、処理中の記録を外す

PR を作った後の CI の結果は待たない。ステップ 2 を終えた Draft PR で失敗する必須チェックは、
`ogp-check.yml` とカバー画像の検査だけになるはずである。それ以外が失敗していたら、下書きの作成に誤りがある。

## 手順案の根拠

- **処理の条件はラベルだけとし、作成者は問わない。** 個人アカウントのリポジトリでラベルを付けられるのは
  オーナーとコラボレーターだけで、このリポジトリのコラボレーターはオーナーだけである（2026-11-26 に `gh api` で確認）。
  REST API の Issue 作成でも、push 権限のない人が指定したラベルはエラーなしで捨てられる。
  作成者を問わないので、ステップ 1 で Claude が `claude[bot]` などの別アカウントで Issue を書いてもよい
  - 例外は Issue Forms の `labels:` で、作成者の権限にかかわらずラベルが付く。
    テンプレートでこのラベルを自動で付けない、という `docs/repository-workflow.md` の禁止事項は引き続き必要である
  - オーナーが第三者の Issue にラベルを付けると、その本文が依頼として処理される。
    Issue の作成者は後から本文を書き換えられるので、ラベルを付けた後の書き換えも処理される。
    このため、他人の Issue にはラベルを付けない。採用したい依頼は、オーナーが自分の Issue に書き直す
  - `docs/repository-workflow.md` はまだ「オーナー自身が立てた Issue」を条件にしている。統合するときに直す
- **二重処理を防ぐ。** ポーリングでもイベント駆動でも、同じ Issue を2回拾うことがありうる。
  処理中のラベルを付けるか、コメントを残すかは実装時に決める
- **`Closes #N` で Issue と PR を結ぶ。** マージ時に Issue が自動で閉じ、依頼と記事の対応も残る
- **タグと OGP 画像はステップ 2 で作らない。** タグは記事の完成後にオーナーが付ける。
  OGP 画像にはタイトルとタグが入るので、下書きの段階で作っても仕上げで作り直すことになる
- **ステップ 3 の起点は通知である。** 人の作業はイベントで自動的に始まらない
- **ステップ 4 は承認ではなくマージである。** GitHub では自分の PR を自分で承認できないため、
  Ruleset で必要な承認数を 0 にしている。`/article-publish` が OGP 画像の生成、検査の待機、
  squash merge、ブランチの削除までを行う

## 実行環境の比較

ステップ 2 を GitHub Actions（`claude-code-action`）と Raspberry Pi 4 上の Claude Code のどちらで行うかを比べた。
GitHub Actions に決めた（2026-11-26、ADR-0008）。

| 観点 | GitHub Actions | Raspberry Pi 4 |
|------|------|------|
| 起動 | `issues` の `labeled` イベントで即座に動く | `gh issue list --label article-request` を数分おきにポーリングする |
| 保守 | 不要。毎回きれいな環境で動く | OS や Claude Code の更新、停電や SD カードの故障への備えが要る。止まっても気づきにくい |
| 認証と権限 | `permissions:` で必要な権限だけを与え、環境は使い捨てになる | オーナーの全権限を持つ `gh` トークンを無人の機器に常時置く。無人で動かすため広い許可も要る |
| 必須チェックの起動 | Claude GitHub App のトークンで push すれば動く（2026-11-26 に試験で確認。checkout に `persist-credentials: false` が必要） | オーナーの認証で push するので動く |
| コミットの作者 | bot になり、自動の下書きだと分かる（既定では `github-actions[bot]` と表示される。2026-11-26 の試験で確認） | オーナーになり、手作業と区別できない |
| 記録 | 実行ログと失敗の通知が Actions に残る | 自前で用意する |
| 環境の自由度 | 追加のツールや MCP はワークフローに書いて用意する | 自由に組める |

Claude のサブスクリプションの利用枠は、どちらでも同じように消費する。

Mac の `~/.claude` にあるメモリの執筆ルールは Actions からは読めないが、比較の材料にはしない。
メモリのルールは暗黙のものになりがちで、本来は CLAUDE.md に書くべきものである。
自動化の作業として CLAUDE.md へ移す（`docs/draft-automation-log.md` 作業 1-1）。

## 検査との関係

検査は PR の上だけで行い、commit や push の時点では行わない（`docs/repository-workflow.md`「検査」）。

| タイミング | 動くもの |
|------|------|
| ブランチへの commit・push | なし |
| PR の作成時と、PR への push のたび | `textlint.yml`、`ogp-check.yml`（いずれも必須）、`claude-code-review.yml` |
| マージ後（`main` への push） | `deploy.yml`、`bluesky-post.yml`、`textlint.yml` |

ステップ 2 で作った Draft PR に残るエラーは、`ogp.webp` がないことによる `ogp-check.yml` の失敗だけになるはずである。
これは仕上げ前であることの目印として扱う。下書きを作った Claude は、PR を作った後の CI の結果を待たない。
textlint の指摘と TOML の誤りは、push の前に手元で直す。CI の textlint は `npm run lint` を実行しているだけなので、
手元で実行しても結果は同じである。
OGP 以外のエラーが PR に出ていたら、下書きの作成で何かが失敗したと判断できる。

`textlint-disable` で指摘を回避することは、既存のルールどおり禁止する。

`zola build` も同じ考え方で、下書きの段階で実行し、PR の必須チェックにも加える。
下書きで起きやすいのは、`{% raw %}` の囲み忘れやコンポーネントの書き誤りといった Tera の構文エラーである。
今の必須チェックにはビルドがなく、ビルドの失敗はマージ後の `deploy.yml` まで検出されない。
下書きで実行するのは自分で直すため、必須チェックは手作業の PR も含めてマージを止めるためである。
`zola check` は外部リンクも確かめるので時間がかかり、相手のサイトの都合でも失敗するため使わない。

## カバー画像と OGP 画像の扱い

画像の指定があってファイルがない状態では、Zola のビルドが失敗する（2026-11-26 にテンプレートと Zola 0.23.6 のソースで確認）。

- `social_media_card` を書き、`ogp.webp` がない場合: tabi の `partials/social_media_images.html` が `throw()` でエラーを出す
- 本文冒頭に `{{< image src="cover.avif" … />}}` を書き、ファイルがない場合: `templates/components/image.html` のフォールバックが
  `get_url(cachebust=true)` を呼び、Zola がファイルを見つけられずにエラーを返す
- frontmatter の `local_image` だけなら、記事一覧のサムネイルは `cachebust` なしの `get_url` を使うので、エラーにならない

このため、下書きでは `social_media_card`、`local_image`、本文冒頭の画像の行のいずれも書かない。
3つの記述は、ステップ 3 でカバー画像を作るときに足す。仮の画像は置かない。検査が通り、仮の画像のままマージされる恐れがあるためである。

書かないことで公開されてしまわないかは、画像ごとに次のとおりである。

- OGP 画像: `ogp-check.yml` が `ogp.webp` と `social_media_card` の両方を必須にしているので、仕上げるまでマージできない
- カバー画像: 今は確かめる検査がなく、カバー画像のない記事が公開されうる。
  全記事を対象にはできない。`content/blog/` の436記事のうち253記事に `local_image` がなく、古い記事にカバー画像がないのは普通である

そこで、PR で追加された記事（base との差分で `--diff-filter=A`）だけを対象に、
frontmatter に `local_image` があり、そのファイルが記事のディレクトリにあることを確かめる必須チェックを加える。
`ogp-check.yml` とは別のジョブとし、Ruleset の必須チェックにも加える。

本文冒頭の画像の行は、この検査で求めない。`local_image` があって本文冒頭に画像の行がない記事が11件あり
（`content/blog/2026/11/izumo/`、`content/blog/2026/06/bark/` など）、いずれも意図した形である。

## Draft PR と検査

Draft PR も検査の対象になる。`pull_request` で `types:` を指定しない場合に反応するのは
`opened`、`synchronize`、`reopened` で、Draft かどうかは区別しない。

Draft にして変わるのは、Ready for review に変えるまでマージできないことと、PR 一覧で仕上げ前だと見分けられることである。

Draft のあいだも必須の検査は止めない。止める場合は、ジョブに `if: github.event.pull_request.draft == false` を付け、
`types:` に `ready_for_review` を加える必要がある。`if:` で飛ばされたジョブは skipped となり、
GitHub は必須チェックの skipped を成功として扱う。`ready_for_review` を加えないと Ready に変えても検査が動き直さず、
一度も検査されていない PR をマージできてしまう。検査は短時間で終わり、仕上げ中に残りの指摘を PR で確かめられるので、
止める利点はない。

利用枠を消費する `claude-code-review.yml` は、Draft のあいだ止める候補になる。必須チェックではないので、上の問題は起きない。

## 検討中に見つけた課題

- **`GITHUB_TOKEN` で作った PR では検査が動かない。** GitHub は、`GITHUB_TOKEN` による push や PR の作成では
  ワークフローを起動しない。必須チェックは待機のまま止まり、ステップ 3 でオーナーが push した時点で初めて動く。
  作成時から検査を動かすには、PAT か GitHub App のトークンを使う。Pi4 でオーナーの認証情報を使う場合も動く
- **CLAUDE.md の lint のルールと矛盾する。** CLAUDE.md には「下書き中に `npm run lint` を実行しない（ユーザーが頼んだときだけ）」とある。
  自動化の Claude も CLAUDE.md を読むので、ステップ 2 の詳細手順 7 と矛盾する。このルールはオーナーが書いている文章を
  途中で機械的に直させないためのもので、Claude が一から書く下書きには当てはまらない。
  CLAUDE.md の文言を対話での執筆に限る書き方に変える（ADR-0008）
- **`claude-code-review.yml` の利用枠。** 下書きの PR と、仕上げ中の push のたびに動く。
  残すかどうかは `docs/repository-workflow.md` でも未決定である
- **`textlint.yml` の `push: main` は役目がない。** `main` への直接 push を禁止したので、マージ後に同じ検査を繰り返すだけである。
  削除の候補とする

## 作業計画

この自動化のための作業と、それぞれの完了条件は `docs/draft-automation-log.md` に定める。

## 決定した事項

- 実行環境: GitHub Actions（「実行環境の比較」の節、ADR-0008）
- 認証方式: Claude GitHub App のトークン。checkout に `persist-credentials: false` を指定する
- Issue の検知方法: `issues` の `labeled` イベント

## 未決定の事項

- 処理中であることの記録方法: ラベルかコメントか
- 下書きのコミットの author 名
- Draft PR の作成をオーナーに知らせる方法
- 下書き用の指示をプロンプトにするかスキルにするか
- `claude-code-review.yml` を残すか、Draft のあいだ止めるか
