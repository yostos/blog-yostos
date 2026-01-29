+++
title = "生成AIでメール管理 - Claude Desktop x FastmailMCP連携"
description = "Claude Desktopの最新機能であるMCP（Model Context Protocol）を使って、プライバシー重視のメールサービス「Fastmail」とClaude Desktopを連携させ、AIアシスタントにメール管理を手伝ってもらう方法をご紹介します。"
date = 2025-06-28
aliases = ["/articles/2025/06/28/claude-desktop-fastmail-mcp"]

[taxonomies]
tags = ["Tech", "Generative AI"]
+++

![Mail with AI](mail.webp)

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

Claude Desktopの最新機能であるMCP（Model Context Protocol）を使って、プライバシー重視のメールサービス「Fastmail」とClaude Desktopを連携させ、AIアシスタントにメール管理を手伝ってもらう方法をご紹介します。

## はじめに - 生成AIがメールを扱う時代

メールの確認、返信、整理...日々の業務で避けて通れないメール管理。この作業を生成 AI に任せられたらどうでしょうか？
MCP を使って生成 AI とメールサービスを連携できれば、実は比較的簡単に実現できます。

「最近の重要なメールを要約して」「特定の人からのメールを検索して」といった指示を出すだけで、AI がメールボックスを確認し、必要な情報を提示してくれる。そんな未来がもう実現可能なのです。

## MCPとは何か - Claude Desktopの拡張機能

MCP（Model Context Protocol）は、Claude Desktop に外部ツールとの連携機能を追加するプロトコルです。これにより、Claude は単なるチャットボットから、実際にツールを操作できる AI アシスタントへと進化します。

今回使用する[fastmail-mcp-server](https://github.com/alexdiazdecerio/fastmail-mcp-server)は、Alex Diaz de Cerio 氏が開発したオープンソースの MCP サーバーです。このサーバーは、Fastmail の JMAP API（JSON Meta Application Protocol）を介してメールサービスと通信し、Claude がメールの読み取り、送信、検索、整理などを行えるようにします。TypeScript で実装されており、12 以上のツールを提供する包括的なメール管理ソリューションです。

## Fastmail MCPサーバーのセットアップ

セットアップは思ったより簡単でした。以下の手順で進めます。

### 前提条件

- Node.js 18 以上
- Fastmail アカウント（API アクセスが可能なプラン）
- Claude Desktop

### 1. MCPサーバーのインストール

```bash
npm install -g @alexdiazdecerio/fastmail-mcp-server
```

### 2. FastmailでAPIトークンを取得

1. [Fastmail](https://www.fastmail.com)にログイン
2. Settings → Privacy & Security → Integrations → [API tokens](https://www.fastmail.com/settings/security/tokens)
3. 新しいトークンを作成（Mail、Submission 権限を付与）

### 3. Claude Desktopの設定

`~/Library/Application Support/Claude/claude_desktop_config.json`を編集します。

```json
{
  "mcpServers": {
    "fastmail": {
      "command": "fastmail-mcp",
      "env": {
        "FASTMAIL_EMAIL": "あなたのメール@fastmail.com",
        "FASTMAIL_API_TOKEN": "取得したAPIトークン"
      }
    }
  }
}
```

Claude Desktop を再起動すれば準備完了です。

## 実際の使用感と活用シーン

設定が完了したら、早速使ってみましょう。Claude Desktop に依頼するだけで、様々なメール操作が可能になります。

「最近のメールの一覧を見せて。ただし広告メールは除外して。」と入力するだけで、Claude が最新のメールリストを表示してくれます。
メール種別、件名、送信者、日時が整理された形で提示されて表示されます。
「メール種別」は Claude がメールを見てカテゴライズしてくれている項目なので、従来のメールクライアントでは不可能な項目です。

注意点は、メールを表示しただけでは既読にならないという仕様です。
これはプライバシーとセキュリティを考慮した設計で、意図しない既読マークを防いでいます。
既読にしたい場合は、「このメールを既読にして」と明示的に指示する必要があります。

メールの送信も同様にシンプルです。「田中さんに以下の内容でメールを送って。
件名はプロジェクトの進捗報告、本文にお疲れ様です。今週の進捗を報告します...」といった指示で、メールの作成から送信まで一気に実行してくれます。

ただし、現時点では一部制限もあります。添付ファイルの送信、HTML メールの作成（プレーンテキストのみ対応）、送信済みメールの自動保存、カレンダー連携などは対応していません。

generate_email_analytics の機能を呼び出せば、どのようなメールがどのような分布
で来ているかを分析してくれます。

## 遭遇した課題と対処法

最大の課題は、送信したメールが送信済みフォルダに保存されないことでした。調査の結果、これは[JMAP仕様（RFC 8621）](https://datatracker.ietf.org/doc/html/rfc8621)の設計によるものだとわかりました。

JMAP では送信（EmailSubmission）とメールボックスへの保存が意図的に別操作として設計されており、送信成功時に自動的に送信済みフォルダに保存するには`onSuccessUpdateEmail`パラメータの実装が必要です。しかし、現在の fastmail-mcp-server ではこのパラメータがまだサポートされていません。

作者の方に[GitHubリポジトリ](https://github.com/alexdiazdecerio/fastmail-mcp-server/issues)で issue を作成し機能追加をリクエストしています。
暫定対応としては BCC に自分のアドレスを追加をすればよいと思います。

この問題は多くの JMAP 実装で共通の課題となっており、コミュニティでの議論が活発に行われています。

## 今後の可能性とまとめ

Claude Desktop と Fastmail の連携により、メール管理の新しい可能性が広がりました。自然言語でメールを操作できることで、以下のような未来が期待できます。

- **より高度な自動化**: 条件分岐を含む複雑なメール処理
- **他のツールとの連携**: カレンダー、タスク管理との統合
- **AI による返信提案**: 文脈を理解した返信文の自動生成
- **メールの自動分類**: AI による重要度判定とフォルダ振り分け

現時点では送信済みメールの保存など、いくつかの制限がありますが、fastmail-mcp-server は活発に開発が続けられており、MCP エコシステム全体も急速に発展しています。オープンソースコミュニティの力で、これらの課題も近い将来解決されることでしょう。

生成 AI にメール管理を任せる第一歩として、ぜひ Fastmail MCP サーバーを試してみてください。日々のルーティンワークから解放され、より創造的な業務に集中できる時間が生まれるはずです。

---

## 参考リンク

- [fastmail-mcp-server (GitHub)](https://github.com/alexdiazdecerio/fastmail-mcp-server) - 本記事で使用した MCP サーバー
- [Fastmail](https://www.fastmail.com) - プライバシー重視のメールサービス
- [Fastmail API Documentation](https://www.fastmail.com/dev/) - JMAP API の詳細
- [JMAP Specification (RFC 8621)](https://datatracker.ietf.org/doc/html/rfc8621) - JMAP プロトコル仕様
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) - MCP の公式情報
