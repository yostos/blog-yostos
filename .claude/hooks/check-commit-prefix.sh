#!/bin/sh
# git commit の prefix を検査する PreToolUse フック。
#
# ステージされたファイルがすべて content/ 配下（＝記事の変更のみ）なのに
# コミットメッセージに content: が含まれていなければブロックする。
# ルールの出典: .claude/simple-commit.local.md
set -u

cmd=$(jq -r '.tool_input.command // empty')

# git commit 以外は素通し
case "$cmd" in
*"git commit"*) ;;
*) exit 0 ;;
esac

staged=$(git diff --cached --name-only 2>/dev/null)
[ -n "$staged" ] || exit 0

# content/ 以外が1つでも混ざっていれば判定しない
echo "$staged" | grep -qv '^content/' && exit 0

# content: が含まれていれば OK
echo "$cmd" | grep -q 'content:' && exit 0

printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"ステージされているのは content/ 配下だけです。記事の追加・更新は content: prefix を使ってください（feat: は機能追加のみ）。出典: .claude/simple-commit.local.md"}}'
