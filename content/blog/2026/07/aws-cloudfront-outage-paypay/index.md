+++
title = "AWS障害でPayPayが利用不可に フランクフルトの一AZが世界に波及"
description = "2026年7月16日、AWSのCDN「CloudFront」で障害が発生し、PayPayの決済やニコニコ生放送、はてなブログなど多数のサービスに影響が出ました。発生源はフランクフルトの単一AZという局所的な障害でしたが、なぜ日本を含む世界9か国に波及したのか、その仕組みを整理します。"
date = 2026-07-16
[taxonomies]
tags = ["Tech", "Cloud"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = """
2026年7月16日17時40分頃、AWSのCDN「CloudFront」で障害が発生し、PayPayの決済やニコニコ生放送、はてなブログなど日本国内のサービスを含め世界9か国で影響が出ました。直接の原因はCloudFrontの「VPC Origins」機能の不具合で、発生源はフランクフルトの単一アベイラビリティゾーンでした。CloudFrontがグローバルに一体運用されるCDNであるため、地理的に無関係な地域まで影響が波及しました。
"""
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

2026年7月16日17時40分頃、Amazon Web Services(AWS)のCDNサービス「Amazon CloudFront」で大規模な障害が発生しました。日本の決済サービス「PayPay」をはじめ、ニコニコ生放送、はてなブログ、noteなど多数のサービスに影響が出ています。PayPayではアプリの読み込みや決済処理ができなくなり、公式サイトや障害情報ページ自体にもアクセスできない状態に陥りました。障害発生後、PayPay側は決済手段として「オフライン支払いモード」への切り替えを利用者に案内しています。

## 障害詳細

発生時刻は日本時間で2026年7月16日17時40分頃(AWS公式の調査開始は現地時間1:44 AM PDT)です。症状としては、CloudFront経由のアクセスで504 Gateway Timeoutなどの5xxエラーが多発しました。日本国内ではPayPay、ニコニコ生放送、はてなブログ、noteなどが影響を受けたほか、日本、スペイン、ドイツ、オーストラリア、スウェーデン、フランス、米国、英国など世界9か国39都市以上で障害が報告されています。

日本国内で影響を受けた主なサービスは次のとおりです。

| サービス | 影響内容 |
|---|---|
| PayPay | アプリの読み込み・決済処理不可、公式サイト・障害情報ページも接続不可 |
| ニコニコ生放送 | 接続しにくい状態 |
| はてなブログ | 接続しにくい状態 |
| note | 接続しにくい状態 |

AWSのステータスサイトによると、障害の直接的な引き金はCloudFrontの「VPC Origins」機能でした。VPC Originsは、CloudFrontから顧客のプライベートVPC内にあるバックエンドリソースへ安全に接続するための機能で、これを利用している顧客側でエラーが多発しました。一方、標準的なS3オリジンなど、VPC Originsを使わない構成は影響を受けていません。AWSは応急的な回避策として、VPC Originsを使わない構成に切り替えることでエラーを回避できるとアナウンスしています。

## 一地域の障害が世界規模に広がった理由

今回の障害で興味深いのは、技術的な発生源が非常に局所的だった点です。障害の起点は、EU-CENTRAL-1(フランクフルト)リージョンの単一アベイラビリティゾーン「euc1-az2」に限定されていました。

つまり、物理的な不具合はドイツの1つのデータセンター群(AZ)内で起きたものにすぎません。しかし、CloudFrontはグローバルに分散した単一のCDNネットワークとしてVPC Origins接続を提供する仕組みになっているため、フランクフルトの一部で生じた問題が、世界中のエッジロケーション経由で各国のサービスへ波及する結果となりました。

これは、CDNのようにグローバルに一体運用されるインフラでは、1つのリージョンやAZの障害が地理的に無関係な地域にまで影響しうることを示す典型例といえます。東京リージョン自体には障害の原因はなく、あくまでフランクフルト発、世界巻き込み型の障害でした。

## 障害を事前に防げたか

クラウドを利用したシステム設計では、どのような機能であっても一時的に利用できなくなる可能性を前提に、二重化やフェイルオーバーの仕組みを組み込むのが一般的な考え方です。

今回の件で言えば、CDNをCloudFrontという単一のサービスに依存し、単一障害点になっていたことが技術的な問題点だったと考えられます。

しかし、CloudFrontは多くの技術者にとって自システムの外側に当たり前に存在するインフラという感覚に近く、これ自体が障害点になり得るという認識を持てていなかったのではないかと思います。

仮にその認識を持てていたとしても、実際に設計へ組み込むにはマルチCDN構成、例えばCloudflareなど別系統のCDNとの併用が必要になります。これはコストとのバランスから、多くの企業にとって現実的な選択肢とは言いにくいのが実情です。

## まとめ

今回のPayPay障害は、PayPay自体のシステム不具合ではなく、利用しているAWS CloudFrontの障害が波及したものです。直接の原因はCloudFrontの「VPC Origins」機能における不具合で、発生源はフランクフルト(EU-CENTRAL-1)の単一AZでしたが、CloudFrontのグローバル構成により世界規模で影響が拡大しました。東京リージョン固有の問題ではなく、VPC Originsを使わないオリジン構成(S3など)は影響を受けていません。

大規模なグローバルCDNに依存するサービスが増える中、一地域の局所的な障害が世界中の決済・コンテンツサービスに連鎖する構造的リスクを改めて浮き彫りにした事例といえます。

このブログも以前は[Amazon Amplify + CloudFrontで運用していました](@/blog/2026/01/blog-to-zola-aws-cleanup/index.md)が、現在はCloudflareに移行しているため今回の障害の影響は受けませんでした。ただし、CloudFrontとCloudflareはどちらも巨大なグローバルAnycast網であり、同種の相関障害リスク構造を持っています。実際、Cloudflare自体も過去に世界規模の障害を起こしています。今回無傷だったのはたまたまで、CDNの選定自体がこの種のリスクを下げるわけではありません。

## References

<!-- textlint-disable -->

{% references() %}

- ITmedia NEWS.「AWSで障害 「CloudFront」世界規模で不調 PayPayに影響、noteやニコニコ生放送もつながりにくく」
- ケータイ Watch.「PayPayの障害はAWSが原因、決済は「オフライン支払いモード」を」
- BigGo ファイナンス.「PayPayで大規模障害、AWSのCDN不調が波及 公式サイトもダウン」
- GIGAZINE.「AWSのCDNサービスで大規模障害発生、各種ウェブサイトに接続しにくい状態が発生」
- [note - zephel01](https://note.com/zephel01/n/n274043a396db?hl=en). "Summary of AWS (Mainly CloudFront) Outage (July 16, 2026)"
- Sunday Guardian Live.「AWS CloudFront Outage Today: Amazon Web Services Confirms Service Disruption as '5xx Errors' Hit Websites Across Multiple Regions」
- The Nightly.「AWS outage update: CloudFront experience global outage, operation issue」

{% end %}

<!-- textlint-enable -->
