+++
title = "コロナの時代"
description = "まだ連休中ですが、連休明けに解除予定だった緊急事態宣言が月末まで延長になりました。"
date = 2020-05-06T15:32:22+09:00
updated = 2020-05-07T20:26:00+09:00

[taxonomies]
tags = ["Current Affairs"]

[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
katex = true
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

緊急事態宣言下で連休中ですが、ほぼ家に籠った状態です。連休明けを目処に設定されていた
緊急事態宣言も月末まで延長となりました。

個人的にはそう簡単に収束しないのかなと、もうぼくらは「コロナの時代」に入ってしまったの
だなと感じています。

## COVID-19について

報道では「新型コロナウイルス感染症」、英語が好きなうちのような会社ではCODID-19
とされています。 当初は発生した地域に因んで「武漢肺炎」などと記載されていました。

昨年11月末に武漢で初めて検出されてから、2ヶ月も経たない年初にはWHOから
注意喚起の声明がなされ、その2ヶ月後の3月には既に世界中で感染が広がっていました。
この感染症を引き起こす新型コロナウィルス(SARS-CoV-2)は、これだけの短期間で世界的
流行を果した最初のウィルスでしょう。

今日の時点で、Googleのまとめている統計によれば、3,663,911人が感染し、
亡くなった方は257,301人です。

つい先日まではどこか遠くの話と感じていましたが、
私の部下も1名感染し1週間ほど入院しました。当初は肺炎を起こしていて大変だった
ようですが、3日ほどで安定しました。5日ほどで検査でも陰性となり連休中に退院と
なっています。

ご本人は日頃から感染には気をつけていた方で、
職場には感染者はおらず本人も感染元に心あたりはないとのことでした。
数字からは意識できなかったこのウィルスの広まりをみせつけられた感じでした。

実際緊急事態宣言の最初の週は、仕事先も「それと仕事は別」という感じで通常運転でしたが、
2週目からは勤務日を3日/週として、すべてのプロジェクトは勤務日が減る前提で
再スケジュールということになりました。

4月末で空気が変った印象です。

## いつ収束するんだろう

延長された緊急事態宣言は5月末までですが、
多くの人が言うように個人的には5月末に収束しないのではと予想しています。

以下は素人が俄仕込みで理解した内容なので、鵜呑みにしないでください。
間違いがあれば是非ご指摘をお願いします。

ウィルスから見ると人類は3種類に分類できます。感受性人口(Susceptibles)、
感染人口(Infectious)、隔離人口(Removed)です。簡単言うと、

- 感染する可能性がある人
- 感染している人
- 一度感染して回復し免疫を持つか亡くなった人で感染する可能性がない人

また、ウィルスを持った感染者が自然な状態で感染力を失しなうまでに何人を
感染させるかを「基本再生数」といいますが、WHOによればCoV-2
の基本再生産数は1.5 - 2.5なのだそうです。
ここでは悲観的に見て、基本再生産数を2.5とします。

シンプルに考えると、感染拡大が収まる条件は以下の2つしかないことが
わかります。

1. 一人の感染者からの実際の感染者数の「実効生産数」を基本再生産数2.5
   のところを1.0以下にする。
2. 感受性人口を減らし、隔離人口を増やすと感染機会が減らし感染拡大を防ぐ。

前者は緊急事態宣言の外出自粛などまさに今やっていることですね。
医療崩壊を防ぐなどの意味で実効再生数を抑えていくことは重要です。
ただし、あくまで短期的な対応です。過去数ヶ月の感染拡大を見ると、
一時的にこういった処置で実効生産数を抑えても、
決定的な治療薬の開発などがなければ状況は変わりません。
処置を解除した途端に基本再生産数へ戻ってしまい、
最終的な解決にはならないのは明らかです。

後者は「集団免疫閾値」というそうですが、ある程度免疫を持った人が社会に
入ればウィルスが感染拡大できないということです。たとえば、ワクチンなどは
感染することなく免疫力を持たせて人工的に隔離人口を上げているということです。

集団免疫率には計算式があり、

<!-- textlint-disable -->

$$\text{集団免疫閾値} = \left(1 - \frac{1}{\text{再生産数}}\right) \times 100$$

<!-- textlint-enable -->

で計算できます。再生産数を2.5とすると、60%となります。
つまり、WHOの悲観的な基本再生産数をとると、60%の人が感染するまで
収束しないことになります。

ワクチンなく実効再生産数を押さえる対応を取るなかで、人口60%の隔離人口
を確保するには一体何ヶ月かかるのでしょう？

現在発表されている感染確認数から再生産数を2.5としてグラフにしてみました。
日本の人口については総務省統計局の
[人口推計（令和元年（2019年）11月確定値，令和2年（2020年）4月概算値）　（2020年4月20日公表）](https://www.stat.go.jp/data/jinsui/new.html)
のデータを使用しました。

<!-- textlint-disable -->

{{ image(src="covid19-graph1.png", alt="再生産数2.5の場合の隔離人口率推移予測") }}

<!-- textlint-enable -->

_再生産数2.5の場合の隔離人口率推移予測_

9月には60%に達するので意外に早い印象ですが、最後の週は国民の半数が罹患するという状況です。
こんな選択は出来ないことが明白です。

「
[【新型コロナ】感染確認者数、死亡者数について、ECDCのデータを利用したダッシュボード](https://scitechlabo.blogspot.com/2020/04/ecdc.html)
」を公開されている方がいらいしたので、このサイトで日本の再生産数( Estimated Reproduction number )
を確認してみました。
緊急事態宣言がなされた以降は0.7程度に落ちていますが、その前のなんとなく自粛ムードだった3月から4月にかけては
およそ再生産数は1.5前後と読めます。再生産数1.5を前提にすると、閾値は33%となります。同様にグラフにしてみました。

<!-- textlint-disable -->

{{ image(src="covid19-graph2.png", alt="再生産数1.5の場合の隔離人口率推移予測") }}

<!-- textlint-enable -->

_再生産数1.5の場合の隔離人口率推移予測_

この場合閾値は低くなりましたが、閾値に達するのは来年の2月です。
なおかつ、このケースも最終週は30%の人が罹患している状況ですから、考えづらいですね。

南半球でも同時に進行していることを考えると自然にウィルスが拡大を止めることはなさそうです。
つまり、「もう大丈夫」という集団免疫閾値に達する状況は、自然な状態では直近に実現しそうに
ありません。

ワクチンにしても年単位で時間がかかるといわれていますし、
治療薬はもう少し早くできるようですが、高い重症化率をみると「治療できるからOK」とは
ならない気がします。

わたしはもう楽観しないことにしました。長期戦です。

## 自作マスク

いつまで続くかわからないこのパンデミックですが、マスクもそろそろ一月
くらいしかストックがなくなってきたので代替のマスクを試しに作ってみました。

Amazonで購入した [マスクホルダー](https://amzn.to/3b9c5vo) を利用して
キッチンペーパーで作ったものです。

<!-- textlint-disable -->

{{ image(src="mask.jpg", alt="キッチンペーパーで作るマスク") }}

<!-- textlint-enable -->

_キッチンペーパーで作るマスク_

長期戦の備えです。

## 『コロナの時代の僕ら』( 2020-05-07 追記 )

この記事を書いた後にAmazonで『
[コロナの時代の僕ら](https://amzn.to/35ETA0y)
』という本を見つけました。

 <div class="booklink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="booklink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/yomereba_main_202607160949469749?pc=https%3A%2F%2Fbooks.rakuten.co.jp%2Frb%2F16291909%2F%3Fscid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2Fev%2Fbook%2F" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/book/cabinet/9457/9784152099457.jpg?_ex=64x64" style="border: none;" /></a></div><div class="booklink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="booklink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/yomereba_main_202607160949469749?pc=https%3A%2F%2Fbooks.rakuten.co.jp%2Frb%2F16291909%2F%3Fscid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2Fev%2Fbook%2F" target="_blank" >コロナの時代の僕ら</a><div class="booklink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://yomereba.com" rel="nofollow" target="_blank">ヨメレバ</a></div></div><div class="booklink-detail" style="margin-bottom:5px;">パオロ・ジョルダーノ/飯田　亮介 早川書房 2020年04月24日頃    </div><div class="booklink-link2" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/yomereba_main_202607160949469749?pc=https%3A%2F%2Fbooks.rakuten.co.jp%2Frb%2F16291909%2F%3Fscid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2Fev%2Fbook%2F" target="_blank" >楽天ブックス</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/exec/obidos/asin/4152099453/yostosweb-22/" target="_blank" >Amazon</a></div><div class="shoplinkkindle" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=%E3%82%B3%E3%83%AD%E3%83%8A%E3%81%AE%E6%99%82%E4%BB%A3%E3%81%AE%E5%83%95%E3%82%89&__mk_ja_JP=%83J%83%5E%83J%83i&url=node%3D2275256051&tag=yostosweb-22" target="_blank" >Kindle</a></div>                                           </div></div><div class="booklink-footer" style="clear: left"></div></div>

素粒子物理学を専攻したイタリアの小説家パオロ・ジョルダーノが2月末から3月初旬に
書き下ろした、新型コロナ感染症をめぐるエッセイです。

タイトルで同じ言葉を使っていたので気になったのですが、「感染症の数学」で書かれていることは
私が思っていたことをもっとわかりやすく言葉にされています。毎日テレビに出てくる感染症の
専門家よりも、この作者の説明のほうが確実にわかりやすいのはなぜでしょう。

当時もイタリアではヨーロッパの中でも感染症の拡大が進んでいましたが、
まだそれほど切迫感がない中で作者が感じている不安や懸念が簡潔な言葉で書かれています。
そして、現在米国、スペインについで最も多くの感染者を出しているイタリアの状況と、まだ若干の余裕を感じる初期のエッセイを比べると、感染症の進行の速さに驚かされます。

最後に収録されている「コロナウイルスが過ぎたあとも、僕が忘れたくないこと」は他の
エッセイから少し日にちが進んだ3月20日の文章で、明らかにメッセージが切迫している
のが印象的でした。

今回のパンデミックが如何に人々の生活を変え、今後も元へは戻らず
新しい時代になるだろうこと、その中で何を残し何を捨てるかの選択を迫られるだろうことを
ストレートに書き表しています。これは私たちが感じていたことなんだと思いました。
