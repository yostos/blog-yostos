+++
title = "なぜAnthropicは排除されたのか"
description = """
2026年2月、トランプ政権はAnthropicを米国政府から排除し、
OpenAIと新たな契約を締結しました。両社とも同じ安全性の原則を
掲げていたにもかかわらず、なぜ明暗が分かれたのか。
経緯と争点を一次ソースから整理し、技術者への影響を考察します。
"""
date = 2026-03-02T08:37:01+09:00
[taxonomies]
tags = ["Current Affairs", "Generative AI"]
[extra]
local_image = "cover.webp"
social_media_card = "ogp.webp"
tldr = """
AnthropicとOpenAIは同じ2つのレッドライン（自律型兵器禁止・大規模監視禁止）を
掲げていたが、その担保方法の違い — 契約的禁止か技術的セーフガードか — と
政治的背景が排除/選択を分けた。サプライチェーンリスク指定の民間への波及や
政治リスクという新たな評価軸には注意が必要だが、
今回の米国政府の判断がOpenAI/Anthropicの決定的な優劣を意味するわけではない。
"""
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

## 経緯

### 政府・防衛市場への参入

Anthropicは排除以前から米国政府・防衛市場に深く関与していました。

- 2024年11月にPalantir[^palantir]・AWSと三社提携を結び、最高機密レベル（IL-6）認証環境でClaudeを情報機関・国防機関に提供を開始
- 2025年6月にはAmazon Bedrock[^bedrock]上のClaudeが連邦政府の高セキュリティ基準の認証[^fedramp]を取得し、同年7月にはCDAO（最高デジタル・AI責任者室）と最大2億ドルのPrototype OTA契約[^ota]を締結
- 2025年8月にはGSA[^gsa]とのOneGov協定で連邦政府全体に年間1ドルでClaude for Governmentを提供

[^palantir]: Palantir Technologies — 米国の防衛・情報機関向けデータ分析企業。CIAの投資部門In-Q-Telの出資で設立され、軍・情報機関に深いパイプを持つ。

[^bedrock]: Amazon Bedrock — AWSが提供するフルマネージド型の基盤モデルサービス。ClaudeやLlama等のAIモデルをAPI経由で利用できる。AWS GovCloud（米国政府専用のクラウド環境）リージョンでの提供により政府機関の利用が可能になる。

[^ota]: Prototype OTA（Other Transaction Agreement）— 通常の連邦調達規則（FAR）を経由しない柔軟な契約形式。プロトタイプ開発を目的とし、迅速な契約締結が可能なため、国防総省が先端技術の実証に多用している。

[^fedramp]: FedRAMP HighおよびDoD IL4/5。FedRAMPは連邦政府のクラウドサービスに求められるセキュリティ認証制度で、Highは機密性の高いデータを扱える最上位区分。IL4/5は国防総省が定める影響レベルで、管理対象の非機密情報や国家安全保障関連データの処理が許可される。

[^gsa]: GSA（General Services Administration、一般調達局）— 米連邦政府の調達を一元管理する機関。GSAスケジュール契約を通じて各省庁が製品・サービスを購入する仕組みを運営している。

<!-- textlint-disable -->
<details>
  <summary>情報元</summary>
{% references() %}
- Palantir. "[Anthropic and Palantir Partner to Bring Claude AI Models to AWS for U.S. Government Intelligence and Defense Operations](https://investors.palantir.com/news-details/2024/Anthropic-and-Palantir-Partner-to-Bring-Claude-AI-Models-to-AWS-for-U.S.-Government-Intelligence-and-Defense-Operations/)". 2024-11-07
- Anthropic. "[Claude in Amazon Bedrock achieves FedRAMP High authorization](https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high)". 2025-06-11
- AWS. "[Amazon Bedrock models achieve FedRAMP High and DoD IL 4/5](https://aws.amazon.com/about-aws/whats-new/2025/05/amazon-bedrock-models-fedramp-high-dod-il-4-5-govcloud/)". 2025-05-23
- Anthropic. "[Anthropic and the Department of Defense to advance responsible AI in defense operations](https://www.anthropic.com/news/anthropic-and-the-department-of-defense-to-advance-responsible-ai-in-defense-operations)". 2025-07-14
- GSA. "[GSA Strikes OneGov Deal with Anthropic](https://www.gsa.gov/about-us/newsroom/news-releases/gsa-strikes-onegov-deal-with-anthropic-08122025)". 2025-08-12
- Anthropic. "[Offering expanded Claude access across all three branches of government](https://www.anthropic.com/news/offering-expanded-claude-access-across-all-three-branches-of-government)". 2025-08-12
{% end %}

</details>
<!-- textlint-enable -->

### 対立の構図

対立の構図は、以下のようなものだったと推定します。

- AnthropicのAUP（利用規約）には、兵器開発への利用、戦場管理アプリケーション、同意のない個人の追跡・監視など、軍事利用に関する複数の制限が含まれる。国防総省との契約にも同様の利用上の制約が存在していたと考えられる[^aup]
- 2026年1月3日、米軍によるベネズエラのマドゥロ拿捕作戦が実行される。Semaforの報道によれば、この作戦でClaudeが使用され、Anthropicの上級幹部が定期ミーティングの場でPalantirの上級幹部に使用の有無を問い合わせたとされる。
- Semaforによれば、Palantirはこの問い合わせを国防総省に報告した。ただし、Anthropicはこの報道を「虚偽」と明確に否定しており、「技術的事項に関するルーティンな議論以外で、業界パートナーとこの件について議論したり懸念を表明したりしたことはない」と述べる。
- 報道の真偽はともかく、国防総省側の懸念は明確で、ヘグセス国防長官は2026年1月9日付のメモ「Artificial Intelligence Strategy for the Department of War」で、「合法的な軍事用途を制限する可能性のある使用ポリシー上の制約がないモデル」を活用するよう省内に指示。AIベンダーが利用上の制約を根拠にサービスを制限・停止しうる状況を解消する意図と読める。
- これがAnthropicに対する直接的な要求に発展。国防総省はAnthropicにClaudeを「あらゆる合法的目的」に使用できるよう求め、2月27日を期限とする最後通牒を行なう
- Anthropic CEO Dario Amodeiは2月26日付の公式声明で「良心に従い、彼らの要求に応じることはできない」と拒否を表明

[^aup]: 商用AUPがそのまま政府契約に適用されていたかどうかは公開情報からは確認できていません。

[^ama]: AMA（Ask Me Anything）— SNS上で質問を受け付け回答する形式の公開Q&A。

<!-- textlint-disable -->

<details>
  <summary>情報元</summary>
{% references() %}
- Anthropic. "[Usage Policy](https://www.anthropic.com/legal/aup)"
- Semafor. "[Exclusive: Palantir partnership is at heart of Anthropic, Pentagon rift](https://www.semafor.com/article/02/17/2026/palantir-partnership-is-at-heart-of-anthropic-pentagon-rift)". 2026-02-17
- NBC News. "[Tensions between the Pentagon and AI giant Anthropic reach a boiling point](https://www.nbcnews.com/tech/security/anthropic-ai-defense-war-venezuela-maduro-rcna259603)". 2026-02
- Lawfare. "[Hegseth Memo Instructs Defense Dept. to Use Military AI Platform](https://www.lawfaremedia.org/article/hegseth-memo-instructs-defense-dept.-to-use-military-ai-platform)". 2026-01
- Anthropic. "[Statement from Dario Amodei on Department of War Discussions](https://www.anthropic.com/news/statement-department-of-war)". 2026-02-26
{% end %}

</details>
<!-- textlint-enable -->

### 排除命令

翌2月27日、トランプ大統領は全連邦機関にAnthropicの即時利用停止を命じ、ヘグセス長官はAnthropicを「サプライチェーン安全保障上のリスク」に指定しました。

この「サプライチェーンリスク」指定は、これまで下表のような外国の敵対国に関連する企業にのみ適用されてきた措置です。米国企業への適用は前例がありません。

| 企業               | 国     | 対象               | 措置                           |
| ------------------ | ------ | ------------------ | ------------------------------ |
| Huawei / ZTE       | 中国   | 通信機器           | 連邦調達禁止                   |
| Kaspersky Lab      | ロシア | ウイルス対策ソフト | 米国内での販売・更新を全面禁止 |
| Hikvision / Dahua  | 中国   | 監視カメラ         | 連邦調達禁止                   |
| TikTok / ByteDance | 中国   | SNSアプリ          | 売却命令、アプリストア禁止     |

指定の法的根拠は10 U.S.C. § 3252（国防総省のサプライチェーンリスク管理権限）とみられますが、この条文の適用範囲はDoD調達契約に限定されています。法律専門家からは、ヘグセス長官による「すべての商業取引の禁止」という解釈は法の範囲を大幅に超えている可能性が高いとの指摘が出ており、Anthropicも法的異議申し立てを表明しています。

<!-- textlint-disable -->
<details>
  <summary>情報元</summary>
{% references() %}
- Donald Trump. Truth Social post（全連邦機関へのAnthropic即時利用停止指示）. 2026-02-27
- Pete Hegseth (@SecWar). "[This week, Anthropic delivered a master class in arrogance...](https://x.com/SecWar/status/2027507717469049070)". X. 2026-02-27
- Anthropic. "[Statement on the comments from Secretary of War Pete Hegseth](https://www.anthropic.com/news/statement-comments-secretary-war)". 2026-02-27
- U.S. Code. "[10 U.S.C. § 3252 — Supply chain risk](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section3252)"
{% end %}

</details>
<!-- textlint-enable -->

## 争点 — 2つのレッドライン

今回の対立の核心にあったのは、次の2つのレッドラインです。

- 完全自律型兵器への使用禁止（**技術的限界**：現在のAIでは信頼性が不十分）
- 米国市民の大規模監視への使用禁止（**倫理的原則**：民主的価値と相容れない）

これらの制限はAnthropic独自のものではありません。

完全自律型兵器については、現在のフロンティアAIは殺傷に関わる判断を独立して行えるほど信頼性が確立されていないという技術的認識に基づいた制約です。
この認識は業界全体で共有されており、実際Anthropicに代わりペンタゴンと契約を結んだOpenAIも、自律型兵器禁止・大規模監視禁止を含む同様のセーフガードを契約条件に盛り込んでいます。

大規模監視については、生成AIが市民監視に繋がる潜在的なリスクを排除するため倫理的な理由で設けられた制約です。こちらも、主要AI企業の利用規約には類似の制限が含まれています。

つまり、 **レッドラインの内容自体は生成AI業界では一般的な制約事項であり、Anthropicだけが特異な主張をしていたわけではありません** 。

Anthropicがこれらの制約の遵守に特に強く拘った背景には、同社固有の事情があります。

Anthropicは2021年、Dario AmodeiとDaniela Amodeiが「AI開発においてスケーリングと安全性を両立させるべきだ」という立場からOpenAIを離れて設立した企業です。「人類の長期的な利益のための先進AIの責任ある開発と維持」をミッションに掲げ、AI安全性を企業の中核に据えています。

さらに、同社はデラウェア州のPublic Benefit Corporation（公益法人）として設立されており、株主利益だけでなく社会的便益の実現を法的義務として負っています。加えて、Long-Term Benefit Trust（LTBT）という独自のガバナンス機構を設けており、AI安全・公共政策の専門家5名が取締役選任・解任権を持つ構造になっています。AmazonやGoogleといった大口投資家も議決権株式を保有していません。この構造により、Anthropicは「民主的価値と相容れない用途を拒否すること」を単なる経営判断ではなく、制度に根ざした義務として説明できる立場にあります。

こうした設立理念と制度的構造が相まって、Anthropicは国防総省の要求に対して譲歩できなかったと考えられます。CEO Amodeiは2月26日の公式声明で「我々は愛国的なアメリカ人であり、米国の防衛に貢献する意思がある」としつつも、「良心に従い、彼らの要求に応じることはできない」と拒否を表明しました。なお、ウクライナで使用されているような部分的自律兵器については防衛に不可欠として支持しており、すべての軍事利用を拒否しているわけではありません。

<!-- textlint-disable -->
<details>
  <summary>情報元</summary>
{% references() %}
- Anthropic. "[Company](https://www.anthropic.com/company)"
- Anthropic. "[Core Views on AI Safety](https://www.anthropic.com/news/core-views-on-ai-safety)". 2023
- Anthropic. "[The Long-Term Benefit Trust](https://www.anthropic.com/news/the-long-term-benefit-trust)". 2023
- Anthropic. "[Statement from Dario Amodei on Department of War Discussions](https://www.anthropic.com/news/statement-department-of-war)". 2026-02-26
- OpenAI. "[Our agreement with the Department of War](https://openai.com/index/our-agreement-with-the-department-of-war/)". 2026-02-27
- Dario Amodei. "[Machines of Loving Grace](https://darioamodei.com/essay/machines-of-loving-grace)". 2024-10
{% end %}

</details>
<!-- textlint-enable -->

## なぜAnthropicが排除され、OpenAIが選ばれたのか

Anthropic排除と同日の2月27日、OpenAIはペンタゴンと新たな契約を締結しました。前節で述べたとおり、2つのレッドライン（自律型兵器禁止・大規模監視禁止）は業界共通の制約であり、OpenAIも同様の原則を掲げています。では、なぜAnthropicだけが排除されたのでしょうか。

国防総省は両社に対し、AIを「あらゆる合法的目的（any lawful purpose）」に使用できるよう求めました。2つのレッドラインに対する両社の対応は以下のとおりです。

- 完全自律型兵器への使用禁止（技術的限界）
  - **Anthropic** — 契約条項として自律型兵器への使用を明示的に禁止し、違反時にはサービスを停止できる形を求める。「あらゆる合法的目的」という文言はこの禁止と矛盾するとして拒否している。
  - **OpenAI** —「あらゆる合法的目的」を受け入れた。自律型兵器禁止については、契約上の明示的禁止ではなく、モデルがタスクを拒否した場合に利用者が強制できない仕組みなどの技術的セーフガードで担保するアプローチを取った。Altman CEOはX上のAMA[^ama]で「We accepted the 'all lawful uses' language proposed by the Department」と明言している。
- 米国市民の大規模監視への使用禁止（倫理的原則）
  - **Anthropic** — 大規模監視の禁止に加え、公開情報の大規模収集・統合も実質的な監視になりうるとして、その明示的禁止を契約に盛り込むよう求めた。
  - **OpenAI** — 大規模監視禁止を原則として掲げているが、その担保は憲法修正第4条や外国情報監視法（FISA）など既存の法律への参照で行っている。Anthropicが求めた公開情報の大規模収集の明示的禁止は含まれない。

両社の違いは、レッドラインの内容ではなく担保の方法にあります。Anthropicは契約条項による明示的禁止を求め、OpenAIは既存の法律への参照と技術的手段で対処しました。この違いは両社の公式声明で確認できます。ただし、契約の完全な文言は非公開のため、技術的セーフガードが契約上の禁止と同等の保護を提供するかどうかは検証できません。

こうした契約アプローチの違いに加え、政治的背景も無視できません。Anthropic CEO Amodeiは連邦選挙委員会（FEC）の公開記録によれば民主党候補への寄付を継続的に行っており、2024年大統領選ではハリス前副大統領を公式に支持しています。トランプ大統領はTruth Socialへの投稿でAnthropicを「RADICAL LEFT, WOKE COMPANY」と呼びました。一方、OpenAIはStargate計画（5000億ドル規模のAIインフラ投資、2025年1月にトランプ大統領自ら発表）の中核パートナーであり、Altman CEOはトランプの就任基金に100万ドルを個人寄付しています。

<!-- textlint-disable -->
<details>
  <summary>情報元</summary>
{% references() %}
- OpenAI. "[Our agreement with the Department of War](https://openai.com/index/our-agreement-with-the-department-of-war/)". 2026-02-28
- Sam Altman (@sama). "[Tonight, we reached an agreement with the Department of War...](https://x.com/sama/status/2027578652477821175)". X. 2026-02-27
- Sam Altman (@sama). AMA on Pentagon deal. X. 2026-03-01
- Anthropic. "[Statement from Dario Amodei on Department of War Discussions](https://www.anthropic.com/news/statement-department-of-war)". 2026-02-26
- Anthropic. "[Statement on the comments from Secretary of War Pete Hegseth](https://www.anthropic.com/news/statement-comments-secretary-war)". 2026-02-27
- FEC. "[Individual contributions — Dario Amodei](https://www.fec.gov/data/receipts/individual-contributions/?contributor_name=dario+amodei)"
- The White House. "[The Stargate Project](https://www.whitehouse.gov/briefings-statements/2025/01/the-stargate-project/)". 2025-01-21
{% end %}

</details>
<!-- textlint-enable -->

## 技術者から見た影響

### Claude 使用継続の是非

今回のサプライチェーンリスクの指定により、一般の企業でのClaude利用に何らかの影響がでるのではないかという懸念があります。

Anthropic自身の声明（2/27）では、10 U.S.C. § 3252に基づくサプライチェーンリスク指定は「国防総省の契約に限定され、他の顧客へのClaude提供に
は影響しない」と主張しています。更にAnthropicはこの決定自体を法的に争う姿勢を示しており、その法廷闘争の決着時期は不明です。
法的には民間企業への波及はないはずです。
ただし「安全保障上のリスク」と名指しされた企業の生成AIについては、多くの日本の顧客が懸念を抱くでしょう。
特にエージェント型で先進的なClaudeとなると、組織内で使用継続の是非について議論となる可能性があります。事前に合意を形成しておく必要があります。

### 「政治リスク」という評価軸

この直接的な影響に加え、より広い視点では、AIベンダーの選定に「政治リスク」という新たな評価軸が加わったことを意味します。

これまでAIモデルの選定基準は、性能・コスト・APIの安定性といった技術的要素が中心でした。しかしベンダーの政治的立場や政府との関係によって、ある日突然サービス利用できなくなるリスクが現実化したのです。AIモデルに深く依存しているシステムは、こうした非技術的要因による中断に対して脆弱になります。

特定のAIベンダーへの依存度を意識し、必要に応じて別のモデルやエージェントに切り替えられる体制を整えておくことが重要になります。

### 今回の件で生成AIの選定を変えるべきか

報道ではAnthropicは善良な企業、OpenAIは政権に迎合したように描かれがちですが、この構図に引きずられて生成AIの選定判断を大きく変える必要はないと考えます。

今回の政府契約において両社を分けたのは、2つのレッドライン（技術的限界と倫理的原則）の内容ではなく、その担保方法の違い — 契約条項による明示的禁止か、技術的セーフガードによる制限か — でした。加えて、各社の政治的背景が排除の規模と速度に影響した可能性もあります。

しかし、商用利用においてはこの分岐点は当てはまりません。AnthropicとOpenAIはいずれも、AUPによる契約的制約とモデル自体のタスク拒否による技術的制約を備えています。政府契約のように「あらゆる合法的目的」を受け入れるかどうかという択一を迫られる場面は、一般の利用者には生じません。

技術的限界と倫理的原則に関するレッドラインは業界共通であり、どちらのベンダーを選んでもその点は変わりません。今回の一件は、米国政府との契約交渉という特殊な文脈で起きた対立であり、民間での生成AI選定の基準を根本から見直す理由にはなりません。
