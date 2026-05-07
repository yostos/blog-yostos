+++
title = "Cloudflare Workers AI + Vectorize で RAG"
description = """\
ブログ記事をナレッジベースにして、著者のペルソナで質問に答える\
AI Q&Aページを Cloudflare Workers AI と Vectorize で構築しました。\
BGE-M3 による日本語 embedding、Llama 3.3 70B によるペルソナ付き回答生成、\
差分 ingest パイプラインまで、Cloudflare スタックだけで完結しています。\
"""
date = 2026-03-20T00:00:01+09:00
updated = 2026-05-07
[taxonomies]
tags = ["Tech", "Generative AI", "Weblog","Cloudflare"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
mermaid = true
tldr = """\
ブログ記事を BGE-M3 で embedding して Vectorize に格納し、\
質問時に Llama 3.3 70B でペルソナ付き回答を生成する RAG Q&A を\
Cloudflare スタックだけで構築しました。ask.codedchords.dev で公開中です。\
"""
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

<!-- more -->

## 何を作ったのか

このブログのナビゲーションに「ask」というメニューを追加しました。
私のデジタル分身(bot)に質問できるページが表示されます。質問を入力すると、ブログ記事の内容を踏まえて私っぽい回答を返します。

ブログに書いてある話題はもちろん、書いていない話題についても「私ならこう答えるだろう」という推測で回答を生成します。
ただし、たかだか個人ブログの文書量ですから大した学習量ではないため、平気で嘘をつきます。それも含めて楽しんでもらえればと思います。

たとえば、こんな質問を投げてみます。

<!-- textlint-disable -->

{% admonition(type="tip", title="Q&A の例") %}
**Q:** CIOも設置せず、IT Governanceの取り組みを行なわない理事長が「生成AIを導入したい」と言っています。どうすべきですか？

**A:** その理事長に、生成AIの導入が「新しいシステムの導入」と違うことを説明する必要があります。生成AIは、組織の判断の中枢に組み込まれ、自社固有の文脈で動く必要があります。そのためには、IT部門だけでなく、業務部門の理解と協力が必要です。
また、生成AIの導入には、データの整備、セキュリティの確保、コンプライアンスの確保などの準備が必要です。CIOを設置せず、IT Governanceの取り組みを行なわない組織では、これらの準備を十分に整えることが難しいでしょう。（以下、省略）
{% end %}

<!-- textlint-enable -->

私が答えそうな回答を返してきました。ブログ記事の内容をベースにしつつ、ペルソナの設定に基づいた回答を生成しています。

ソースコードはGitHubで公開しています。

<!-- textlint-disable -->

{{ linkcard(url="https://github.com/yostos/yostos-persona") }}

<!-- textlint-enable -->

## 動機

仕事を終えて職場を変えることになったとき、同僚が「質問できなくなるので、あなたのbotがあればいいのに」と言ってくれました。ありがたい話です。真に受けました。

もう1つの動機は、せっかくブログをCloudflare Pagesに移行したのでWorkers AIも試してみようという技術的な興味です。Workers AI、Vectorize、Workersを組み合わせたRAGシステムを自分で組んでみたかったですし、構築過程がそのままブログのネタになるのも都合が良いと思いました。

## アーキテクチャ

処理フローはシンプルなRAGパターンです。

まず事前処理として、ブログ記事をVectorizeに投入しておきます。

<!-- textlint-disable -->

{% mermaid() %}
graph LR
Articles[ブログ記事<br>Markdown]--> Parse[front matter解析<br>+ セクション分割]--> EMB1[BGE-M3<br>embedding]--> V[(Vectorize)]
{% end %}

<!-- textlint-enable -->

質問時は、入力をベクトル化して類似チャンクを検索し、ペルソナ設定と合わせてLLMに渡します。

<!-- textlint-disable -->

{% mermaid() %}
graph LR
Q[質問]--> EMB2[BGE-M3<br>embedding]--> V[(Vectorize)]
V -->|類似チャンク| LLM[Llama 3.3 70B]
Persona[ペルソナ設定]--> LLM
LLM --> A[回答 +<br>参考記事リンク]
{% end %}

<!-- textlint-enable -->

1. ユーザーが質問を入力
2. WorkersがBGE-M3で質問をベクトル化
3. Vectorizeで類似チャンクを検索（上位5件、スコア閾値0.3）
4. システムプロンプト（ペルソナ設定）＋ 取得したチャンク ＋ 質問をLlama 3.3 70Bに渡す
5. 回答テキスト＋参考記事リンクをフロントエンドに返す

使用しているCloudflareサービスはWorkers、Workers AI（EmbeddingとLLM）、Vectorizeの3つだけです。フロントエンドはWorkersのAssets機能で配信しています。フレームワークは使わず、素のHTML/CSS/JSで構築しました。

## モデル選定

EmbeddingモデルはBGE-M3（`@cf/baai/bge-m3`）を採用しました。BAAI開発の多言語対応モデルで、出力は1024次元です。日本語と英語が混在するブログ記事に対応できることが決め手でした。当初はPLaMo-Embedding-1Bを検討しましたが、出力が2048次元でVectorizeの上限（1536次元）を超えるため断念しています。

LLMはLlama 3.3 70B Instruct FP8 Fast（`@cf/meta/llama-3.3-70b-instruct-fp8-fast`）です。128Kトークンのコンテキストウィンドウを持ち、日本語でのペルソナ付き回答生成は概ね良好です。中国語文字の混入が発生すると既知の問題として上がっています。今回は、システムプロンプトで抑制しています。

## 事前処理: ナレッジベースの構築

ブログのMarkdownファイル群をナレッジとして使用しており、これらを解析して事前にVectorizeする処理スクリプト(ingest)が行う処理は以下の通りです。

1. 記事のファイルパス、front matterからslug、title、date、tagsを抽出し、本文を見出し（`##`）単位でセクション分割
2. 各チャンクにメタデータ（ファイルパス、slug、title、section、URL）を付与
3. BGE-M3でベクトル化してVectorizeにアップサート

差分検出にはマニフェストファイル（slug → MD5ハッシュのマッピング）を使い、変更のあった記事のみ再処理します。初回ingestでは286記事を処理しました。Vectorizeのメタデータ上限（10,240 bytes）対策として、チャンク本文を8,000 bytesに切り詰めています。

## 質問(Request)対応: Workers AI のコード

### Vectorize処理

Workers AIの特徴は `env.AI.run()` というバインディング呼び出しです。APIキーの管理もSDKのインストールも不要で、`wrangler.toml` の `[ai]` セクションに `binding = "AI"` と書くだけで使えます。

RAGの検索部分（rag.ts）を丸ごと載せます。Embedding生成からVectorize検索まで、これだけで完結しています。

```typescript,name=src/worker/rag.ts
import type { Env } from "./types";

export interface RetrievedChunk {
  text: string;
  meta: {
    slug: string;
    title: string;
    section: string;
    url: string;
  };
  score: number;
}

const SCORE_THRESHOLD = 0.3;
const TOP_K = 5;

export async function retrieveChunks(
  question: string,
  env: Env
): Promise<RetrievedChunk[]> {
  // Embed the question
  const embeddingResult = await env.AI.run("@cf/baai/bge-m3", {
    text: [question],
  });

  const queryVector = embeddingResult.data[0];

  // Search Vectorize
  const results = await env.VECTORIZE.query(queryVector, {
    topK: TOP_K,
    returnValues: false,
    returnMetadata: "all",
  });

  // Filter by score threshold and map to chunks
  return results.matches
    .filter((m) => m.score >= SCORE_THRESHOLD)
    .map((m) => ({
      text: (m.metadata?.text as string) || "",
      meta: {
        slug: (m.metadata?.slug as string) || "",
        title: (m.metadata?.title as string) || "",
        section: (m.metadata?.section as string) || "",
        url: (m.metadata?.url as string) || "",
      },
      score: m.score,
    }));
}
```

### LLM呼び出し

LLMの呼び出しも同じパターンです。`env.AI.run()` にモデル名とメッセージを渡すだけで回答が返ってきます。

```typescript,name=src/worker/index.ts（抜粋）
const llmResult = await env.AI.run(
  "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  {
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: question },
    ],
    max_tokens: 512,
  }
);

const answer = (llmResult as { response?: string }).response
  || "回答を生成できませんでした。";
```

外部APIを叩いている感覚がなく、Workersの中でAIを呼んでいるだけという体験は新鮮です。

### ペルソナ設定

コードの `systemPrompt` として渡しているのがペルソナ設定です。回答は私のキャラクタ設定に基づいて生成されます。元IBM/AWSのエンジニア、ギター愛好家、CLIツール開発が趣味といったプロフィールに加えて、口調や回答スタイルも定義しています。敬語ベースで、好きな話題には熱量が上がり、知らないことでもぺらぺら喋るという設定です。こうしてみると、オタクそのものですね。

回答スタイルとして、簡潔に答えるだけでなく、ときどき脱線したり問い返したりするような振る舞いも仕込んでいます。200〜300文字程度を目安にしていますが、実際の挙動はモデル次第です。

## コスト

個人ブログのQ&Aという用途なので、非機能要件は「1日数十件の質問を無料枠内で処理できること」に設定しています。

Workers AIの課金単位はNeuronsです。1リクエストあたりの消費量を見積もります。

| 処理                                   | モデル        | トークン数（概算） |   Neurons |
| -------------------------------------- | ------------- | -----------------: | --------: |
| Embedding（質問文）                    | BGE-M3        |            50 入力 |      0.05 |
| LLM 入力（プロンプト＋チャンク＋質問） | Llama 3.3 70B |         2,000 入力 |        53 |
| LLM 出力（回答生成）                   | Llama 3.3 70B |           512 出力 |       105 |
| **合計**                               |               |                    | **約160** |

Workers AIの無料枠は10,000 Neurons/日なので、**約60リクエスト/日**が上限になります。

Vectorizeも無料枠に十分収まります。

| リソース                          | 使用量 |  無料枠 |   消費率 |
| --------------------------------- | -----: | ------: | -------: |
| 格納次元数（286記事 × 1,024次元） | 約29万 |   500万 |       6% |
| クエリ次元数/月                   |   数千 | 3,000万 | 0.1%未満 |

超過した場合はWorkers Paidプラン（月$5）で$0.011/1,000 Neuronsの従量課金になりますが、現在の利用量では発生しない見込みです。仮に想定の倍（120リクエスト/日）が30日続いたとしても、超過分は月約288,000 Neuronsで約$3.2、プラン基本料と合わせて月$8程度です。

悪用防止として、KVベースでIPあたり60秒間10リクエストのレート制限をかけています。単一IPからの過剰なリクエストは抑制できますが、分散アクセスに対しては無力なので、無料枠の維持を保証するものではありません。個人ブログの自然なトラフィックであれば問題ない想定です。

## 今後の課題

現時点で把握している課題は、BGE-M3の日本語検索精度、チャンク分割の粒度、LLMのmax_tokens最適値（回答品質とコストのバランス）、同一質問に対するキャッシュによる重複推論の回避です。

いずれの改善も、実際にどんな質問が来るかわからない段階では手の打ちようがありません。精度を上げるには実際の質問パターンに基づいた評価用クエリが必要で、つまりフィードバックループを回す必要があります。ただし、面白半分で作ったお遊びですし、質問内容を保持するのはプライバシーの観点で望ましくないため、質問内容のロギングは行っていません。一方で、ブログ記事が増えればナレッジベースが厚くなり、検索精度は自然と改善していく可能性があります。

完璧なものを作ってから公開するよりも、動くものを出して改善していくほうが性に合っています。質問を投げてみて、変な回答が返ってきたら、それはそれで面白いと思ってください。

## References

<!-- textlint-disable -->

{% references() %}

- [Cloudflare](https://developers.cloudflare.com/workers-ai/). "Workers AI"
- [Cloudflare](https://developers.cloudflare.com/vectorize/). "Vectorize"
- [BAAI](https://huggingface.co/BAAI/bge-m3). "BGE-M3"

{% end %}

<!-- textlint-enable -->
