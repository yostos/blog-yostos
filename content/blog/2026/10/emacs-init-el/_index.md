+++
title = "AI時代のEmacs設定術"
description = """
生成AIを日常的に使ういま、エディタにはあちこちに散らばるテキストを集めるハブの役割が求められます。私のinit.elをもとに、Emacsをテキスト作業の拠点にする設定を機能ごとに解説します。
"""
template = "series.html"
sort_by = "slug"
transparent = true

[extra]
series = true

[extra.series_intro_templates]
next_only = "この記事は「$SERIES_HTML_LINK」シリーズの第$SERIES_PAGE_INDEX回です。\n\n- 次回: 「$NEXT_HTML_LINK」"
middle = "この記事は「$SERIES_HTML_LINK」シリーズの第$SERIES_PAGE_INDEX回です。\n\n- 前回: 「$PREV_HTML_LINK」\n- 次回: 「$NEXT_HTML_LINK」"
prev_only = "この記事は「$SERIES_HTML_LINK」シリーズの第$SERIES_PAGE_INDEX回です。\n\n- 前回: 「$PREV_HTML_LINK」"
default = "この記事は「$SERIES_HTML_LINK」シリーズの第$SERIES_PAGE_INDEX回です。"

[extra.series_outro_templates]
next_only = "次回は「$NEXT_HTML_LINK」です。"
middle = "次回は「$NEXT_HTML_LINK」です。"
prev_only = ""
default = ""
+++

生成AIを日常的に使ういま、エディタに求められる役割は変わりつつあります。散らばるテキストを集めて加工し、生成AIと連携して成果物に仕上げる作業の拠点には、優れたエディタであるだけでなく、あらゆるテキストを同じ操作で扱えるハブであることが求められます。いま全盛のVS CodeではなくEmacsを選ぶ理由はそこにあります。

想定する読者は、プログラミングに限らず、日常のテキスト作業をすべてEmacsで済ませたい人です。連載では私のinit.elをもとに、ほかでは解説が見当たらないテーマを選び、機能ごとに紹介します。動作環境はEmacs 31とmacOSです。

この連載が、これからEmacsを始めようという方の一助になればと思います。
