+++
title = "ジェンスン・フアンの辞任と創業者なきNVIDIA"
description = """NVIDIAを33年率いたジェンスン・フアン氏が、不倫と中国スパイ疑惑の渦中で辞任しました。\
なぜ私生活の問題が安全保障の問題にまで発展したのでしょうか。\
ソフトウェアを含むエコシステムで強みを築いてきたNVIDIAは、創業者を失って何を問われるのでしょうか。"""
date = 2026-11-13

[extra]
social_media_card = "ogp.webp"
local_image = "cover.avif"

[taxonomies]
tags = ["Tech", "IT Governance"]
+++

<!-- textlint-disable -->

{{< image src="cover.avif" alt="Cover" />}}

<!-- textlint-enable -->

11月12日、ジェンスン・フアンがNVIDIAのCEOを辞任しました。AIブームの象徴だった人物が、不倫と中国スパイ疑惑で33年務めた座を降りるという衝撃の幕切れです。何が起き、何が問題なのかを整理してみましょう。

## 辞任に至った2週間

発端は10月29日のニューヨーク・タイムズ（以下、NYT）の報道です。経緯を簡単にまとめると次のとおりです。

- 10月29日、NYTがフアン氏とAlice Huang氏の関係を報道
- 11月8日、フアン氏が社員全員に向けたメールで不倫を認めて謝罪。取締役会は続投を支持しつつ、外国の情報機関の標的にされた疑いについて独立調査を始めた。トランプ大統領も「高潔」な人物だと擁護した
- 11月11日、NYTが直属の部下でヘルスケア担当副社長のKimberly Powell氏との関係を報道し、取締役会が進退を協議
- 11月12日に辞任を発表し、取締役も退いた。会社は理由を示さず、CFOのColette Kress氏が暫定CEOに就任

最初の報道の時点では、取締役会と大統領はそろって続投を支持していました。流れを変えたのは2件目の報道です。相手が直属の部下だったことで利益相反の懸念も加わり、報道の翌日には辞任が発表されました。

## Alice Huang氏とMegaspeedをめぐる疑惑

米国の情報機関は、Alice Huang氏を中国の情報機関の協力者とみています。ただし、フアン氏がいわゆるハニートラップにかかったのかどうかは、現時点では分かっていません。

Alice Huang氏は2023年に8か月間、シンガポールのクラウド事業者Megaspeedでマネージングディレクターを務めました。Megaspeedは東南アジアにおけるNVIDIAの大口顧客で、マレーシアの子会社Speedmatrixを通じてNVIDIAの先端チップを大量に購入しています。購入額は約20億ドルから75億ドル以上まで報道によって開きがあります。チップを置いたマレーシアとインドネシアのデータセンターは、中国の顧客に遠隔でサービスしているように見えたと報じられています。

東南アジアに置いたチップの計算能力を中国企業に貸すこと自体は、現行の規則では違法ではありません。問題になるのは、チップそのものを中国へ持ち込むことです。米当局はMegaspeedを輸出規制違反の疑いで調べています。チップの使い先としては、Alice Huang氏の妹が創業株主に名を連ねる中国のShanghai Century Litongの名前も報じられています。Megaspeedは違反を否定し、マレーシア政府も国内法に違反した証拠はないとしています。

この件がただの不倫で済まなかったのは、フアン氏が長年、対中輸出規制の緩和を訴えてきたからです。2025年12月には、トランプ大統領がH200の対中輸出を承認しています。規制の緩和を求めてきた経営者が、規制をすり抜けた疑いのある企業の関係者と親密だったことで、私生活の問題が安全保障の問題として扱われることになりました。なお、NVIDIAの取締役会は、国家安全保障が損なわれたと考える理由はないとしています。

## ジェンスン・フアンの功罪と今後のNVIDIA

フアン氏の功績は疑いようがありません。1993年に共同創業したNVIDIAを、グラフィックカードの会社からAIチップ市場の約9割を握る企業に育て上げました。売上高はこの10年余りで50倍を超え、時価総額は約4兆ドルに達しています。

<!-- author-approved: 慣用句「良くも悪くも」 -->
<!-- textlint-disable -->
一方で、NVIDIAは良くも悪くもフアン氏の会社でした。
<!-- textlint-enable -->

60人を超える幹部が直属するフラットな組織で、日々の経営判断は本人に集中していました。2人の子どもも社内の要職に就いています。サプライチェーンやワシントンとの関係も、フアン氏個人に依存していました。この体制は急成長を支えた一方で、本人がいなくなったときに引き継ぐのが難しい構造でもあります。

フアン氏の不在がこれほど重く受け止められるのは、NVIDIAがハードウェアの強みだけで成長した企業ではないからです。NVIDIAには強力なGPUのイメージがありますが、その強みはソフトウェアも含めたエコシステムにあります。

2006年に発表したCUDAは、GPUを画像処理以外の計算に使うためのプログラミング基盤で、NVIDIAによれば数百万人規模の開発者が利用しています。AIの研究者や企業が書いてきたコードやライブラリの多くはCUDAを前提にしており、他社のチップに乗り換えるには、性能の差だけでなくこの蓄積を手放す覚悟が要ります。

このエコシステムは、目先の収益だけを見ていたら築けなかったものです。CUDAが本格的に稼ぎ始めたのは、ディープラーニングが広まった2010年代半ば以降です。それまでの長い期間、NVIDIAは用途の定まらない基盤に投資を続けました。株主に説明しにくい長期の賭けを続けられたのは、創業者が強い権限を握る会社だったからでしょう。

そう考えると、NVIDIAのかじ取りには、一般的な半導体メーカーとは違う経営が求められます。NVIDIAは製造をTSMCに委託しており、自ら担っているのは、チップ、ソフトウェア、ネットワーク機器を一体の計算基盤として設計し、その上に開発者と顧客をつなぎとめることです。必要なのは、技術の行き先を読んで何年も先に賭ける判断と、それを社内外に納得させる力です。60人を超える幹部と直接やり取りするフアン氏の経営は、この判断を一人に集約する仕組みでもありました。後任に問われるのは、優れた経営者であること以上に、この賭けを引き継げるかどうかだと私は考えます。

当面は、CFOのColette Kress氏が暫定CEOを兼務し、取締役会が社内外から後任を探すとされています。Kress氏はウォール街にはなじみがあるものの、フアン氏が築いてきた取引先や政府との関係は持っていません。トランプ大統領はApple前CEOのTim Cook氏を後任に推していますが、本人が関心を示した兆しはありません。Cook氏はAppleでサプライチェーンの運営に手腕を発揮してきた経営者で、技術の賭けを自ら主導してきたフアン氏とは型が異なります。影響はNVIDIAにとどまらず、買収で合意しているHugging Faceや、上場に合わせて約100億ドルの投資を予定しているAnthropicなど、AI業界全体に及びます。

## まとめ

フアン氏の辞任は、ただの不倫スキャンダルでは終わりませんでした。米中のAI競争の要にある企業のトップには、私生活も含めて安全保障上の責任が伴います。今回の件は、そのことをはっきりと示しました。創業者頼みだった企業には、その創業者を失ったとき何が残るのか。NVIDIAはこれから、この問いと向き合うことになります。

フアン氏は創業初期、セガとの開発契約に行き詰まりながらも自らの判断の誤りを認めて資金援助を頼み、会社を存続させました。この経緯は以前の記事「[NVIDIAを救った入交昭一郎氏](@/blog/2026/05/sega-nvidia/index.md)」で紹介しています。フアン氏は、その逸話を披露した今年5月の卒業式のスピーチで、誠実さと謙虚さの大切さを説いていました。皮肉にも、それからわずか半年で、本人が私生活の不誠実さによって会社を去ることになりました。

私はNVIDIA株を保有しており、彼はNVIDIAにとって欠くことのできない人物だと考えているので、非常に残念です。ただ、CEOとは権力を振るう存在ではなく、会社を存続させる責任を負う立場だと卒業生に語ったのは、フアン氏自身でした。NVIDIAがこれから問われるのは、まさにその存続です。創業者がいなくなっても、フアン氏が築いたエコシステムを守り、次の賭けに出られるかどうか。株主として、その答えを見届けたいと思います。

## References

<!-- author-approved: 報道機関を情報保持のため列記。URLはリンクにせずテキスト表示 -->

<!-- textlint-disable -->

{% <references> %}

- BBC. "The rise and fall of Jensen Huang - how the tech superstar became mired in scandal" `https://www.bbc.com/news/articles/cmze750zg0jeo`
- The New York Times. "What to Know About Colette Kress, Nvidia's New Interim Chief Executive" `https://www.nytimes.com/2026/11/12/business/nvidia-colette-kress-jensen-huang.html`
- Al Jazeera. "Why did Nvidia CEO Jensen Huang resign, and who is Colette Kress?" `https://www.aljazeera.com/news/2026/11/12/why-did-nvidia-ceo-jensen-huang-resign-and-who-is-colette-kress`
- CNBC. "What we know so far about Nvidia partner Megaspeed's Asia footprint" `https://www.cnbc.com/2026/11/12/nvidia-megaspeed-alice-huang-jensen-.html`
- Fortune. "How Megaspeed built a network in Singapore and Malaysia to move $7.5 billion of Nvidia chips to Chinese companies" `https://fortune.com/2026/11/11/megaspeed-nvidia-chips-china-singapore-malaysia/`
- Asia Times. "Nvidia GPU crackdown hits China-linked Southeast Asia data centers" `https://asiatimes.com/2026/06/nvidia-gpu-crackdown-hits-china-linked-southeast-asia-data-centers/`

{% </references> %}

<!-- textlint-enable -->
