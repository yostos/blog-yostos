+++
title = "MCP接続でClaudeにBlenderで3Dモデリングさせてみた"
description = "Blender界隈でBlenderとClaudeをMCP接続してClaudeに3Dモデリングさせるというのが話題なので実際に試してみました。自然言語で依頼するとClaudeがモデリングツールを操作してくれます。"
date = 2025-04-23
aliases = ["/articles/2025/04/23/blender-mcp"]

[taxonomies]
tags = ["Tech", "Generative AI"]
+++

Blender界隈でBlenderとClaudeをMCP接続してClaudeに3Dモデリングさせるというのが話題なので実際に試してみました。自然言語で依頼するとClaudeがモデリングツールを操作してくれます。

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

## 前提

前提は次の通りです。

- Blender 3.0 以降
- Python 3.10 以降
- uv package manager

Blender は無料の 3D モデリングツールなので、[公式サイト](https://www.blender.org/)からダウンロードしてインストールしておきます。

Python の環境は整えておきましょう。

`uv`は Python のパッケージなので、以下のようにインストールできます。

```bash
# Windowの場合
pip install uv

# Macの場合はHomebrewでも可
brew install uv
```

## Claudeの設定

使用するのは例によって Claude Desktop です。

いつものごとく、`claude_desktop_config.json`を編集します。
Claude Desktop から Settings > Developer > Edit Config で開けます。次のように
`blender-mcp`の設定を追加します。

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

## Blender MCP サーバーのインストール

Blender MCP の[配布サイト](https://blender-mcp.com/download.html)から最新版を
ダウンロードします。Zip でダウンロードされるので、展開しておきます。

Blender を起動して、Preferences から Add-ons を開きます。"Install Add-on from
File"を選択して、先ほど展開したフォルダから`addon.py`を選びます。

インストールが完了すると、3D View の Sidebar に"Blender MCP"のアイコンが追加さ
れます。
"BlenderMCP"のタブを開いて、`Poly Haven`のチェックボックスにチェックして
`start mcp server`をクリックします。

これで、Blender MCP が起動しています。

## Claudeにモデリングしてもらう

Claude にモデリングを依頼してみましょう。

Claude には以下のように依頼しています。

> BlenderでPoly HavenのHDRI、テクスチャ、そして岩や植生のようなモデルを使っ
> て、ビーチの雰囲気を作り出してください。

実際にやっているところを見たほうが早いと思うので、動画にしました。

{{ youtube(id="a6-DmRtty_8") }}

## まとめ

今回はアセットを使っているとは言え「風景」だったので、3D 画像として成立させる
モデリングは結構ハードルが高かったと思います。レンダリングした結果もちょっと
微妙でした。正直リアルな画像を得るだけであれば、Midjourney など画像生成 AI を使
ったほうが良い結果になるでしょう。

ただ、シンプルなポリゴンモデルなら結構ちゃんとモデルを作ってくれます。
3D モデルがあると、画角や視点を変えたシーンを何度も調整できるメリットがありま
す。

3D モデリングはツールの使い方もハードルが高く、習得に時間がかかります。
AI を使って自然言語でモデリングできるようになれば結構革新的かなと思います。

MCP でいろいろ拡がっていきますね。
