+++
title = "GoFデザインパターンは現代でも有用か — Go言語から再考する"
description = """OOPの不完全さを補う処方箋として生まれたGoFデザインパターン。\
OOP自体を捨てたGo言語の登場は、新たなパラダイムシフトを示しています。\
23のパターンをGo言語の視点から再検討し、デザインパターンの本質的価値を考察します。"""
template = "series.html"
sort_by = "slug"
transparent = true

[extra]
series = true

[extra.series_intro_templates]
next_only = "この記事は「$SERIES_HTML_LINK」シリーズの第$SERIES_PAGE_INDEX回（全$SERIES_PAGES_NUMBER回）です。"
middle = "この記事は「$SERIES_HTML_LINK」シリーズの第$SERIES_PAGE_INDEX回（全$SERIES_PAGES_NUMBER回）です。前回: 「$PREV_HTML_LINK」"
prev_only = "この記事は「$SERIES_HTML_LINK」シリーズの最終回（全$SERIES_PAGES_NUMBER回）です。前回: 「$PREV_HTML_LINK」"
default = "この記事は「$SERIES_HTML_LINK」シリーズの第$SERIES_PAGE_INDEX回（全$SERIES_PAGES_NUMBER回）です。"

[extra.series_outro_templates]
next_only = "次回: 「$NEXT_HTML_LINK」"
middle = "次回: 「$NEXT_HTML_LINK」"
prev_only = ""
default = ""
+++
