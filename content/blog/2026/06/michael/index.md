+++
title = "映画『Michael』を観た"
description = """
やっと映画『Michael』を観ることができました。彼がポップスターへ駆け上がっていく時代をIMAXのオリジナル音源で追体験しながら、急遽1988年で幕を閉じることになった制作の裏側、そしてThrillerの突出ぶりをチャートの数字から分析します。
"""
date = 2026-06-26T20:04:49+09:00
[taxonomies]
tags =[ "Entertainment","Films" ]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

{{ image(src="cover.webp",alt="Cover") }}

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

先日、公開を楽しみにMichael Jacksonの曲「[Black or White](/blog/2026/06/black-or-white/)」をカバーしましたが、やっと昨日映画を観ることができました。

## 映画の印象

映画では、彼の幼少期から1988年のBad Tour - Londonで行われたWembley Stadiumまでが描かれています。

アルバム「Thriller」発表の後、1984年冒頭のペプシCMでの負傷、
その年に行なったJacksonsとしてVictory Tourくらいまでは詳しく描かれています。

1985年のチャリティ・シングル「We Are the World」のスタジオ録音は結構話題がありそうですが、
全く触れられていません。

<!-- textlint-disable -->

{% aside(position="right") %}
1987年の9月か10月の横浜スタジアムのコンサートに行ったのを懐かしく思い出しました。
{% end %}

<!-- textlint-enable -->

エンディングは父親と決別し、新たな出発をするシーンとして「Bad」を歌うステージで幕を閉じます。実際にはBad Tourは1987年9月12日に日本の後楽園球場で開幕しています。

内容も知っているエピソードばかりですが、
丁度彼がポップスターとして駆け上がっていく時代が描かれているので大変楽しめました。
主演のJaafar Jacksonの再現度やダンスの完成度も大したものでした。そして、曲はオリジナルの
音源がIMAXで聞けるのです。もうそれだけでも満足と言うものです。

ちょっと引っかかったのは、兄弟たちがプロデューサーとして名前を並べていますが、
よくもまぁ自分たちの父親をあのように描けるものだなとは思いました。

## 続編について

もともと本作は1993年あたりまで描くことを想定したようです。
Michaelが13歳のジョーダン・チャンドラーへの性的虐待で告発され、警察がネバーランドを家宅捜索する場面から始まり、そこから生い立ちを回想し、告発とチャンドラー家の
訴訟（最終的に2,300万ドルで和解）へ戻っていく流れだったようです。

ところが和解契約で「チャンドラーをいかなる作品でも描写、言及してはならない」という条項があり(家族は忘れていた)、1988年で完結させるようかなり撮り直しをした
そうです。

このオクラになった撮影シーンが多くあるので、チャンドラーに関するシーンを除外して仕上げるのでしょうか？

ただ、ここからはMichaelに逆風の時期ですから、本作のように楽しめるか疑問です。

## 数字で見る Michael

そう言えば、アルバム「Dangerous」くらいまでは知っていますが、それ以降ってどういう活動をやっていたかあまり知らないなと思い調査してみました。

累計売上枚数は後年の売上も入っているので、アルバムがビルボード1位に居座った期間、収録曲が何曲Hot 100でトップ10入りしたかを調べてみました。

<div style="display:flex; flex-wrap:wrap; gap:14px; margin-bottom:10px; font-size:12px; color:var(--text-secondary);">
  <span style="display:flex; align-items:center; gap:6px;"><span style="width:12px; height:12px; border-radius:2px; background:#2a78d6;"></span>全世界累計売上枚数（横棒・百万枚）</span>
  <span style="display:flex; align-items:center; gap:6px;"><span style="width:14px; height:3px; background:#eb6834;"></span>ビルボード200で1位の週数</span>
  <span style="display:flex; align-items:center; gap:6px;"><span style="width:9px; height:9px; background:#008300;"></span>Hot 100でトップ10入りした曲数</span>
</div>
<div style="position: relative; width: 100%; height: 420px;">
  <canvas id="mjT10" role="img" aria-label="縦軸が年代の複合グラフ。横棒は全世界累計売上で1979年Off the Wall約2000万枚、1982年Thriller約7000万枚、1987年Bad約3500万枚、1991年Dangerous約3200万枚、1995年HIStory約2000万枚、2001年Invincible約800万枚。オレンジの折れ線はビルボード200で1位の週数で0,37,6,4,2,1。緑の折れ線はHot 100トップ10入り曲数で4,7,6,4,2,1。">売上(百万枚)20,70,35,32,20,8。1位週数0,37,6,4,2,1。トップ10入り曲数4,7,6,4,2,1。年代は上から1979,1982,1987,1991,1995,2001。</canvas>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
(function(){
  var lbl={
    id:'lbl',
    afterDatasetsDraw:function(c){
      var ctx=c.ctx; ctx.save(); ctx.font='500 12px sans-serif';
      var b=c.getDatasetMeta(0);
      ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.fillStyle='#185fa5';
      b.data.forEach(function(p,i){ ctx.fillText(c.data.datasets[0].data[i], p.x+6, p.y); });
      var w=c.getDatasetMeta(1);
      ctx.textAlign='center'; ctx.textBaseline='bottom'; ctx.fillStyle='#c0451c';
      w.data.forEach(function(p,i){ ctx.fillText(c.data.datasets[1].data[i]+'週', p.x, p.y-7); });
      var s=c.getDatasetMeta(2);
      ctx.textAlign='center'; ctx.textBaseline='top'; ctx.fillStyle='#006300';
      s.data.forEach(function(p,i){ ctx.fillText(c.data.datasets[2].data[i]+'曲', p.x, p.y+7); });
      ctx.restore();
    }
  };
  new Chart(document.getElementById('mjT10'),{
    data:{
      labels:[['1979','Off the Wall'],['1982','Thriller'],['1987','Bad'],['1991','Dangerous'],['1995','HIStory'],['2001','Invincible']],
      datasets:[
        {type:'bar',label:'全世界累計売上枚数',data:[20,70,35,32,20,8],xAxisID:'xSales',backgroundColor:'#2a78d6',borderRadius:4,maxBarThickness:22,order:3},
        {type:'line',label:'1位週数',data:[0,37,6,4,2,1],xAxisID:'xWeeks',borderColor:'#eb6834',backgroundColor:'#eb6834',borderWidth:2,pointRadius:5,pointStyle:'circle',tension:0,order:1},
        {type:'line',label:'トップ10入り曲数',data:[4,7,6,4,2,1],xAxisID:'xSongs',borderColor:'#008300',backgroundColor:'#008300',borderWidth:2,pointRadius:5,pointStyle:'rect',tension:0,order:2}
      ]
    },
    options:{
      indexAxis:'y',
      responsive:true, maintainAspectRatio:false,
      layout:{padding:{right:40,top:6}},
      plugins:{legend:{display:false}, tooltip:{callbacks:{label:function(x){var u=x.datasetIndex===0?'百万枚':(x.datasetIndex===1?'週':'曲');return x.dataset.label+' '+x.parsed.x+u;}}}},
      scales:{
        y:{ticks:{color:'#52514e',font:{size:12}},grid:{display:false}},
        xSales:{position:'bottom',beginAtZero:true,max:80,title:{display:true,text:'全世界累計売上枚数（百万枚）',color:'#185fa5',font:{size:11}},ticks:{color:'#898781'},grid:{color:'#e1e0d9'}},
        xWeeks:{position:'top',beginAtZero:true,max:40,title:{display:true,text:'ビルボード200で1位の週数',color:'#c0451c',font:{size:11}},ticks:{color:'#898781'},grid:{display:false}},
        xSongs:{position:'top',beginAtZero:true,max:8,title:{display:true,text:'Hot 100でトップ10入りした曲数',color:'#006300',font:{size:11}},ticks:{color:'#898781',stepSize:2},grid:{display:false}}
      }
    },
    plugins:[lbl]
  });
})();
</script>

こうしてみると、アルバム「Thriller」がどれだけ突出して売れたかがよくわかりますね。
37週に渡ってチャート1位でアルバムから7曲もチャートインしています。

Bad Tourを観た影響かアルバム「Bad」も「売れた」という印象があります。
1987年ですから、丁度リスナーがCDに移行した時期なのでみんな買ってた印象がありますが、
「Thriller」ほどは売れなかったのですね。
ただ、アルバムから6曲も収録曲がチャートインしているので、体感的に「売れてた」と感じていたのもうなずけます。

その後は見事に下降線を描いており、これも感覚と合っています。

2001年以降アルバムをリリースしていませんが、これはソニーとのトラブルのためです。

第一に過去作品のマスター権で揉めて契約更新をMichaelが拒否しました。

第二に2003年から未成年への性的虐待などでの刑事裁判で時間的にも財政的に余裕がなかったのでしょう(無罪判決は勝ち取っています)。

第三にレコード会社との契約がないためか、アルバムという形でなく数ヶ月ごとにデジタル・シングルをリリースする形態は晩年考えていたようです。

## まとめ

映画『Michael』は、彼がポップスターとして頂点へ駆け上がっていく時代を、オリジナル音源とともにIMAXで追体験できる作品でした。知っているエピソードばかりとはいえ、Jaafar Jacksonの再現度の高さもあって最後まで楽しめました。

一方で、こうして数字を並べてみると「Thriller」の突出ぶりと、その後の下降線がはっきり見えてきます。本作が1988年で幕を閉じたのは制作上の事情によるものですが、結果として彼のもっとも輝いていた時期だけを切り取った一作になっています。続編が逆風の時代をどう描くのか、楽しめる作品になるのかは、正直なところまだ見えません。
