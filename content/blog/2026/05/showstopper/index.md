+++
title = "読了『闘うプログラマー』"
description = """
伝説のプログラマーDavid Cutlerがマイクロソフト社に移籍し、WindowsNTを生み出すまでの過酷な開発物語。読了して、当時の「OSの時代」や米国でのプログラマーの地位について改めて考えさせられました。
"""
date = 2026-05-12T07:33:12+09:00
updated = 2026-05-12
[taxonomies]
tags = ["Books", "Tech", "Software"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

<!-- more -->

1980年代にMS-DOSでデスクトップパソコン市場を制し、WindowsでGUIのオペレーティング・システム(以降、「OS」と記載)も制しつつあったマイクロソフト社は、90年代、高性能コンピューター向けの「本物」のOS開発プロジェクトを立ち上げます。当時のマイクロソフト社の世界戦略を担ったOS「WindowsNT」です。そのプロジェクトに、当時DEC社のミニコン向けOS、VAX/VMSの開発者であった「伝説のプログラマー」David Neil Cutlerが招へいされました。

## 本書の概要

本書は、David Cutlerを中心とした開発物語です。

『闘うプログラマー』というタイトルから、David Cutler中心に描かれていると思って購入しました。冒頭は、彼がDEC社で担当していた新OSプロジェクト「Mica」が破棄され、1988年マイクロソフト社に移籍するシーンから描かれています。前半は彼がいかにWindowsNTプロジェクトを立ち上げたかが描かれていますが、中盤からはこのプロジェクトに参加したあらゆるレイヤーの開発者へと順次フォーカスが当てられ、エピソードが盛り込まれていきます。

全く新しいOSを、当時主流だったIntelのCPUだけでなく、まだ完成していないRISCにも対応させなければなりません。さらにDOSとの互換性、Win32系の旧来のWindowsとの互換性も維持する必要があったわけです。想像するだけでデスマーチな開発ですが、本書を読めば実際にデスマーチだったことが分かります。それでも当時は「Cutlerの元で新しいOSの開発が出来る」ことを栄誉だと考えるプログラマーが多くいたわけです。

Cutlerの伝記として読むと中途半端ですが、当時のWindowsNTの過酷な開発エピソードが盛り込まれている点は大変興味深く読めました。本書がWindowsNTの初版がリリースされた1993年に出版されたため、開発者たちのエピソードも生々しく、リアルな状況を伝えています。

## 「OSの時代」を背景に

WindowsNTの開発が始まった1980年代後半から1990年代に掛けては、まさに「OSの時代」でした。当時は、ハードウェアやネットワークの環境が大きく変化した時代でもあります。

- CPUは16ビットから32ビットに進化し、RISCという新しいアーキテクチャーも登場した
- MacintoshがGUIを一般ユーザーに広めた結果、プリエンプティブなマルチタスクが一般レベルでも要求されるようになった
- インターネットの普及により、モデムでのパソコン通信ではなく本格的なネットワーク機能が一般ユーザーでも必要となった

PCはMS-DOS上でWindows3.xが動いていましたが、16ビットアーキテクチャーを引きずっていました。IBMは「OS/2」という新しいOSをマイクロソフト社と共にリリースしていましたが、コンシューマーの世界では全く浸透していませんでした。Apple社はClassic Mac OSを何度も刷新しようとしていましたが、ことごとく失敗していました。

そんな中で開発されたWindowsNTは、その後Windows2000、WindowsXPとコンシューマー向けWindowsの核となり、最も成功したOSとなっていきました。

私自身、1995年頃に自宅のPCにWindowsNTを導入していました。とはいえ、当時実際に使っていたツールの大半はWindowsベースですらなく、DOSベースのものが中心だったように記憶しています。それでも「本物のOS」に触れられたこと自体はよいお勉強になりましたし、ファイルシステムのNTFSはFATに比べて信頼性が明らかに高く、家庭利用でもその差を実感できました。

## 米国でのプログラマーの地位

個人的に印象的だったのは、米国での「プログラマー」の地位です。WindowsNTの開発に参加していた開発者が、皆スタープログラマーという訳ではありませんでした。それでも多くの開発者はストックオプションで一財産を築き、西海岸に家を建てポルシェを購入してという経済的な成功を手に入れています。日本における「プログラマー」の扱いとは大違いです。

翻って日本では、多くのプログラマーがSIer (システムインテグレーター) を頂点とする多重下請け構造の中で受託開発に従事しています。給与水準は一般のサラリーマンと大きく変わらず、ストックオプションで一財産を築くケースは稀です。「35歳定年説」も語られるほどに、プログラマーを続けること自体、報われにくい構造でした。

この差の背景には、産業構造の違いが大きいのではないでしょうか。米国はマイクロソフト社のように自社プロダクトを開発・販売する事業会社が産業の主役で、その成功は株式を通じて開発者個人にも還元されます。一方、日本では事業会社がIT機能を外注する構造になっており、プロダクトの成功を開発者と分け合う仕組みもありません。経営層に技術者出身者が少ないことも、こうした地位の差を生む一因と感じます。

<div class="booklink-box" style="text-align:left;padding-bottom:20px;font-size:small;zoom: 1;overflow: hidden;"><div class="booklink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/yomereba_main_202605120734444595?pc=https%3A%2F%2Fbooks.rakuten.co.jp%2Frb%2F6130084%2F%3Fscid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2Fev%2Fbook%2F" target="_blank" ><img src="https://thumbnail.image.rakuten.co.jp/@0_mall/book/cabinet/7577/9784822247577.jpg?_ex=200x200" style="border: none;" /></a></div><div class="booklink-info" style="line-height:120%;zoom: 1;overflow: hidden;"><div class="booklink-name" style="margin-bottom:10px;line-height:120%"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/yomereba_main_202605120734444595?pc=https%3A%2F%2Fbooks.rakuten.co.jp%2Frb%2F6130084%2F%3Fscid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2Fev%2Fbook%2F" target="_blank" >闘うプログラマー新装版</a><div class="booklink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="https://yomereba.com" rel="nofollow" target="_blank">ヨメレバ</a></div></div><div class="booklink-detail" style="margin-bottom:5px;">グレッグ・パスカル・ザカリー/山岡洋一 日経BP 2009年07月    </div><div class="booklink-link2" style="margin-top:10px;"><div class="shoplinkrakuten" style="display:inline;margin-right:5px"><a href="https://hb.afl.rakuten.co.jp/hgc/1300574f.7d238558.13005750.4bcd8088/yomereba_main_202605120734444595?pc=https%3A%2F%2Fbooks.rakuten.co.jp%2Frb%2F6130084%2F%3Fscid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2Fev%2Fbook%2F" target="_blank" >楽天ブックス</a></div><div class="shoplinkamazon" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/exec/obidos/asin/4822247570/yostosweb-22/" target="_blank" >Amazon</a></div><div class="shoplinkkindle" style="display:inline;margin-right:5px"><a href="https://www.amazon.co.jp/gp/search?keywords=%E9%97%98%E3%81%86%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9E%E3%83%BC%E6%96%B0%E8%A3%85%E7%89%88&__mk_ja_JP=%83J%83%5E%83J%83i&url=node%3D2275256051&tag=yostosweb-22" target="_blank" >Kindle</a></div>                              	  	  	  	  	</div></div><div class="booklink-footer" style="clear: left"></div></div>
