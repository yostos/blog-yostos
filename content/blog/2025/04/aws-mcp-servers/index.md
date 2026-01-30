+++
title = "AWS Document MCP Serverを試す"
description = "4月1日のAWS公式ブログで、AWS MCP Serversの記事が掲載されました。早速AWS公式ドキュメントをMCPサーバーとして利用できるAWS Documentation MCP Serverを試してみました。"
date = 2025-04-16
aliases = ["/articles/2025/04/16/aws-mcp-servers"]

[taxonomies]
tags = ["Tech", "AWS", "Generative AI"]
+++

## 公式ブログ記事の概要

公開されたのは「[Introducting AWS MCP Servers for code assistants(Part1)](https://aws.amazon.com/blogs/machine-learning/introducing-aws-mcp-servers-for-code-assistants-part-1/)
」という記事です。AWS MCP サーバーが紹介されています。

これらは、AWS のベストプラクティスを開発ワークフローに直接統合する特化型の
Model Context Protocol（MCP）サーバーのオープンソーススイートです。
このサーバー群は、AI アシスタントと AWS の深い知識を組み合わせ、開発時間を大幅に
短縮しながら、セキュリティコントロール、コスト最適化、AWS Well-Architected の
ベストプラクティスを取り入れることを目的としているようです。

主要な特化型 MCP サーバーとして以下が提供されています。

- **コア：** AI プロセスパイプライン機能を提供する基盤サーバー
- **AWS CDK：** CDK の知識とベストプラクティス実装ツールを提供
- **Amazon Bedrock Knowledge Bases：** 企業の知識ベースへシームレスにアクセス
- **Amazon Nova Canvas：** Amazon Bedrock を通じた画像生成機能を提供
- **コスト分析：** AWS サービスのコストを分析し、詳細なレポートを生成

具体的にどのような MCP サーバーが提供されているかは、[GitHub](https://github.com/awslabs/mcp/)で公開されています。

## AWS Documentation MCP Serverを試す

手っ取り早そうなので、AWS Documentation MCP Server を試してみました。

この API では、AWS の公式ドキュメントとベストプラクティスにアクセスしたり、
ドキュメントを Markdown 形式にコンバートできるようです。

AWS の提供する設定サンプルを見ると、Astral 社が開発した Python 向けのツール管理
コマンド `uv`を使用しているようです。まず、`uv`をインストールします。

```bash
# 公式インストーラー
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# MacでHomebrewでインストールする場合
$ brew install uv
```

デスクトップ版 Claude からアクセスする想定で設定します。
設定メニュー内の開発者メニューから、`claude_desktop_config.json`を開いて編集
します。

```json
  "mcpServers": {
    "inkdrop": {
      "command": "/Users/hogehoge/bin/inkdrop-mcp",
      "args": [],
      "env": {
        "INKDROP_LOCAL_SERVER_URL": "http://localhost:19840",
        "INKDROP_LOCAL_USERNAME": "hogehoge",
        "INKDROP_LOCAL_PASSWORD": "hagehage"
      }
    },
    "claude_code": {
      "command": "/Users/hogehoge/bin/claude-code-mcp",
      "args": [],
      "env": {}
    },
    "aws_document": {
      "command": "/opt/homebrew/bin/uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

この例では、Inkdrop, Claude Code も MCP サーバーとして登録していますが、
必要なのは最後の例だけです。なお、上記は Homebrew でインストールした場合です。
公式インストーラーを使用した場合、パスが異なりますから注意してください。

上記の設定後、Claude の再起動が必要です。

早速確認してみましょう。

デスクトップ版 Claude から、
「aws_document から東京リージョンで現在 Bedrock で利用可能なモデルの一覧を作成してください」と依頼してみました。

以下ように、MCP 使用の許可を求めてながら処理を行っています。

```txt
お手伝いします。AWS Bedrockで現在利用可能なモデルの一覧を作成するために、AWS
公式ドキュメントから情報を検索しましょう。

モデル情報の詳細を確認するために、関連するAWSドキュメントページを読み取りま
しょう。

モデルの詳細情報を取得するために、利用可能なモデルの一覧に関するドキュメント
を検索します：

サポートされているモデルのリストを確認するために、もう一つのドキュメントを読
み取ります：

基本的なモデル一覧を確認するドキュメントを検索します：

もう少し具体的に検索します：

Converseで利用可能なモデルを確認します：

モデルのリージョン対応を確認するために、追加のドキュメントを読み取ります：

これで十分な情報が得られました。収集した情報に基づいて、AWS Bedrockで現在利
用可能なモデルの一覧を作成します。

AWS Bedrockで現在利用可能なモデルの一覧をまとめました。
```

結果、完成したドキュメント[^1]は、AWS の Solution Architect が作成したような丁寧な回答でした。

[^1]: Claude Artifactsで生成されたドキュメント（一時URLのため現在はアクセス不可）

## まとめ

今回は AWS Documentation MCP Server をデスクトップ版 Claude からアクセスすること
を試してみました。

最近の Claude は Web 検索をやってくれるので、MCP サーバーを使用
しなくても同様の結果は得ることができそうです。
しかし、ソースを限定して「公式ドキュメントから」と指定できるのは安心です。

Core MCP Server というものが提供されており、一連の MCP サーバーのオーケストレー
ションを行うようです。もしかすると今回の使い方は想定と違うのかもしれません。

AWS Diagram MCP Server は AWS ダイアグラムを生成してくれるようなのです。
実際の環境からその各種ダイアグラムを GraphViz で描いてくれるなら、
取っても便利そうです。

やっぱり、今 MCP は熱いですね。
