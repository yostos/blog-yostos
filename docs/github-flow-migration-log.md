# GitHub Flow 移行ログ

**開始日**: 2026-11-25
**関連文書**: `docs/repository-workflow.md`、`docs/architectural-decision.md` ADR-0007

`main` への直接 push をやめ、PR のマージで公開する運用に移る作業の計画と記録。

## 計画

作業は次の順に進める。GitHub の設定変更は、各段階で承認を得てから行う。

### 段階1: リポジトリ全体の設定（GitHub）

移行用の PR を squash merge できるように、最初に変える。

| 項目 | 変更前 | 変更後 |
|------|------|------|
| `allow_merge_commit` | true | false |
| `allow_rebase_merge` | true | false |
| `allow_squash_merge` | true | true |
| `squash_merge_commit_title` | `COMMIT_OR_PR_TITLE` | `PR_TITLE` |
| `squash_merge_commit_message` | `COMMIT_MESSAGES` | `PR_BODY` |
| `delete_branch_on_merge` | false | true |

### 段階2: リポジトリ内のファイル変更（移行用ブランチと PR）

ブランチ `feature/github-flow` で次を変更し、PR を作って squash merge する。
この PR が新しい運用での最初の PR になる。

CI と hook

- `.github/workflows/ogp-check.yml` を新しく作る。PR で追加・変更された
  `content/blog/**/index.md` と同じディレクトリに `ogp.webp` があるかを確かめる。
  ジョブ名は `ogp-check` とする。
  ワークフローに `paths:` の絞り込みを付けない。必須のチェックは、ワークフローが
  起動しなかった PR では「待機中」のまま残り、マージできなくなるためである。
  記事を含まない PR では、ジョブの中で検査を省いて成功で終える
- `.husky/` を削除する
- `package.json` から `prepare`、`lint-staged` の設定、husky と lint-staged の依存を削除し、
  `package-lock.json` を更新する
- `README.md` の技術一覧の Git Hooks の行、CI/CD Pipeline の図、Local Hooks の節を、
  PR での検査に合わせて直す

Claude 関連

- `.claude/commands/article-publish.md`
  - `main` にいる場合は `content/<スラッグ>` のブランチを切る手順を最初に加える
  - 手順4の「lint-staged が commit 時に textlint を動かす」を削除する
  - 手順5の `git push origin main` を、ブランチの push、`gh pr create`、
    `gh pr checks --watch` で検査の完了を待つ、`gh pr merge --squash`、
    `main` に戻って `git pull`、`git branch -D` に置き換える
  - 手順6の IndexNow はマージ後のデプロイ完了を待つので、そのまま残す
  - description の「push to main」を直す
- `.claude/commands/blog-release.md` の `gh pr merge` に `--squash` を付ける
- `.claude/simple-commit.local.md` の接頭辞の表を、`docs/repository-workflow.md` の
  「PR のタイトル」の表と同じ内容にする
- `CLAUDE.md`
  - Git Operations に、作業前にブランチを確認し `main` なら切ることと、
    `docs/repository-workflow.md` への参照を加える
  - Hosting 節の「push to main triggers」を、PR のマージで `main` が更新されると
    デプロイされる、という説明に直す
  - Directory Structure の `docs/` の説明に運用ルールを加える

文書

- `docs/repository-workflow.md`、ADR-0007、このログを同じ PR に含める

### 段階3: main の Ruleset（GitHub）

段階2の PR で `textlint` と `ogp-check` のチェックが一度動き、
チェック名が GitHub に登録されてから作る。

| 項目 | 設定 |
|------|------|
| 対象 | `main`（デフォルトブランチ） |
| 状態 | Active |
| マージ前の PR | 必須、承認数 0 |
| 必須のステータスチェック | `textlint`、`ogp-check` |
| バイパス | なし |
| force push | 禁止 |
| ブランチの削除 | 禁止 |

### 段階4: 確認と後片付け

- `gh api repos/yostos/blog-yostos/rules/branches/main` で Ruleset が効いていることを確かめる
- Mac のクローンで `git config --unset core.hooksPath` を実行し、husky の設定を外す
- 次の記事の公開で、`/article-publish` の新しい手順を通しで確かめる

## 未決定

- `claude-code-review.yml` を残すかどうか
- PR のタイトルの接頭辞を検査するかどうか。接頭辞のルールは
  `docs/repository-workflow.md` の「PR のタイトル」に定めた

## 決定事項

- 段階2の PR は機能リリースとして扱わない。`/blog-release` は使わず、
  CHANGELOG への記載とタグ付けもしない
- `main` 上での `git commit` と `git push` を止める Claude Code の hook は作らない。
  `main` への push は Ruleset が拒否するので、そのときにブランチを切り直せば足りる

## 作業記録

### 2026-11-25 段階1: リポジトリ全体の設定

`gh api -X PATCH repos/yostos/blog-yostos` で計画の表のとおりに変更した。
変更後の値を API の応答で確かめた（`allow_merge_commit=false`、`allow_rebase_merge=false`、
`allow_squash_merge=true`、`squash_merge_commit_title=PR_TITLE`、
`squash_merge_commit_message=PR_BODY`、`delete_branch_on_merge=true`）。

### 2026-11-25 段階2: リポジトリ内のファイル変更

ブランチ `feature/github-flow` を作り、次を変更した。

- `.github/workflows/ogp-check.yml` を作成した。PR の base と head の差分から、
  追加・変更された `content/blog/**/index.md` を拾い、同じディレクトリの `ogp.webp` を確かめる。
  検査内容は、削除した `.husky/pre-commit` の OGP 検査と同じである
- `.husky/` をゴミ箱に移し、`npm uninstall husky lint-staged` で依存を削除した。
  `package.json` から `prepare` と `lint-staged` の設定を削除した
- `README.md` の技術一覧から Git Hooks の行を削除し、CI/CD Pipeline の図と
  Workflows の表を PR での検査に合わせて書き直した。Local Hooks の節は削除した
- `.claude/commands/article-publish.md` に、ブランチを確認する手順0と、
  PR の作成・検査待ち・squash merge・後片付けの手順5を書いた。lint-staged の記述を削除した
- `.claude/commands/blog-release.md` の `gh pr merge` に `--squash` を付けた
- `.claude/simple-commit.local.md` の接頭辞の表を、PR のタイトルの表と同じ8種類にした
- `CLAUDE.md` の Git Operations に、運用の概要、作業前のブランチ確認、PR のタイトルの3項目を加えた。
  Hosting 節のデプロイの説明と、Directory Structure の `docs/` の説明を直した

commit `b5ccc3f` を PR #9 として出した。必須にする予定の `textlint` と `ogp-check`、
および `claude-review` がすべて通ったことを確かめ、squash merge した。
`main` のコミットは `ea390cd`（`feat!: publish through PRs with required checks (#9)`）で、
GitHub が PR 番号を末尾に付けた。リモートのブランチはマージ時に自動で削除され、
ローカルのブランチは `git branch -D` で削除した。
マージ後の `deploy.yml` は成功した。記事を含まないため `bluesky-post.yml` は動かなかった。

`claude-review` のレビューで、次の指摘があった。いずれもマージを止めるものではないので、
対応するかどうかは別途判断する。

- `textlint.yml` は actor が `claude` / `claude[bot]` のときジョブをスキップし、
  スキップは必須チェックで成功扱いになる。Claude の bot が作る PR は検査されずに通る
- `ogp-check.yml` は `ogp.webp` の有無だけを確かめ、タイトル変更後の古い画像は検出できない
  （削除した hook と同じ）
- `ogp-check.yml` の `--diff-filter=ACM` はリネーム（`R`）を含まない。
  スラッグを変えた記事は検査から漏れる
- `ogp-check.yml` は `base.sha` との2点差分をとるため、`main` が進むと
  無関係なファイルを拾うことがある（過剰に検査する方向で、見逃しは起きない）
- `article-publish.md` の `git branch -D` は、PR がマージ済みかを確かめずに強制削除する

### 2026-11-25 段階3: main の Ruleset

`gh api -X POST repos/yostos/blog-yostos/rulesets` で Ruleset `protect-main`（ID 28077355）を作った。

- 対象: デフォルトブランチ（`~DEFAULT_BRANCH`）、状態: active、バイパス: なし
- ルール: `deletion`、`non_fast_forward`、`pull_request`（承認数 0、許可するマージ方式は squash のみ）、
  `required_status_checks`（`textlint` と `ogp-check`、GitHub Actions から報告されるもの）

### 2026-11-25 段階4: 確認と後片付け

- `gh api repos/yostos/blog-yostos/rules/branches/main` で、4つのルールが `main` に適用されていることを確かめた
- 空のコミットを作って `main` に直接 push し、
  `GH013: Repository rule violations found` / `Changes must be made through a pull request.`
  で拒否されることを確かめた。空のコミットは `git reset --hard origin/main` で取り消した
- このクローンで `git config --unset core.hooksPath` を実行した
- この作業記録の追記自体を、新しい運用の手順（ブランチ、PR、検査、squash merge）で反映した
- 残る確認は、次の記事の公開で `/article-publish` の新しい手順を通しで試すこと
