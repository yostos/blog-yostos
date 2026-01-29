+++
title = "OpenAI will support MCP"
description = "MCPをサポートしたAnthropicのClaudeで試しましたが、その可能性に驚きました。3月末にはOpenAIもMCP対応を表明していたので楽しみです。"
date = 2025-04-08
aliases = ["/articles/2025/04/08/openai-mcp-support"]
+++

## AltmanのツイートによるMCP対応のアナウンス

以下が 3 月末の Altman のツイート(X)です。

<blockquote cite="https://x.com/sama/status/1904957253456941061">
  people love MCP and we are excited to add support across our products.
  available today in the agents SDK and support for chatgpt desktop app +
  responses api coming soon!
  <footer>
    <cite>
      <a href="https://x.com/sama/status/1904957253456941061">
        &mdash; Sam Altman (March 26, 2025)
      </a>
    </cite>
  </footer>
</blockquote>

MCP(Model Context Protocol)は Anthropic が提唱しているフレームワーク
ですが、上記は**OpenAIもMCPをサポートする**というアナウンスです。

とても重要な意味を持つアナウンスだと思います。
Anthropic は OpenAI の強力なライバルで競合関係にあります。
デファクト・スタンダードが無い現状では対応する規格を提唱できたはずですが、
それをせず MCP サポートに舵を切ったのは素晴らしい経営判断だと思います。

これにより、MCP がほぼ業界のデファクト・スタンダードになると思います。

## MCP(Model Context Protocol)とは

以前いくつか記事を書いていますが、ちゃんと MCP の説明を書いていませんでした。

Model Context Protocol (MCP)は、大規模言語モデル(LLM)に対する指示を構造化す
るためのフレームワークです。

次のような要素から構成されています。

- **Model（モデル）** - AI モデルがどのように自分自身を認識し、振る舞うべきかを定義する
- **Context（コンテキスト）** - モデルが参照すべき情報や知識を提供する
- **Protocol（プロトコル）** - モデルの動作や応答方法のルールを設定する

[以前の記事](/articles/2025/03/28/claude-integration-with-inkdrop)では、
**Context**を使って独自のナレッジ(Inkdrop)を Claude に追加するということをやっただけですが、
Claude 活用の可能性が途端に広がりものすごい効果を体感できました。これまでも
Context の部分にだけ限ると RAG (Retrieval-Augmented Generation)という手法があ
りましたが、こんなに簡単にはできなかったと思います。

MCP では Context だけでなく、Protocol を通じて行動規範の設定や、Model を通じた企業の
ブランドトーンに合わせた応答スタイルなどに応用できます。

MCP により、明確に分離された要素(Model/Context/Protocol)に整理され、
単なるプロンプトエンジニアリングを超えて体系化されたアプローチで
AI の応答をより予測可能で一貫性のあるものにすることが可能となりました。

## MCPがデファクト・スタンダードになると

MCP がデファクト・スタンダードとなれば AI 関連ツール間の標準化された通信パターンを
提供していることになるでしょう。

この事実を踏まえると Claude デスクトップが Claude Code をナレッジソースとして扱えるように、次のよう
なことが可能になるかもしれません。

- **ChatGPT-Claudeクロス連携**: ChatGPT の回答を Claude が評価するような AI システム間の直接的な情報交換や連携
- **AIオーケストレーション**: 複数の生成 AI がそれぞれ
  の強みを生かした連携し、結果を統合するようなワークフロー構築の可能性。例え
  ば、データ解析は ChatGPT、文章生成は Claude、検証は Gemini などの役割分担するイ
  メージ。
- **統一ナレッジアクセス**: マーケットに MCP 準拠した多数のナレッジベースが
  登場し、簡単に新しいナレッジを自社の AI に追加できる可能性

いずれも現時点で実現できるかどうか検証が必要というレベルです。
AI オーケストレーションなどは追加の標準化やツールが必要でしょう。
また、技術的に標準化の方向で協力できたからと言って、今後ビジネス上の判断で
その適用範囲が制限される可能性はあります。

しかし、このような動きを見ていると、加速度的に AI の世界が拡がっていくのを実感しています。楽しみです。
