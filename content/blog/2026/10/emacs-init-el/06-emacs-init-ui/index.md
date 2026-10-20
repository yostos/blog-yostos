+++
title = "AI時代のEmacs設定術(6): Emacsを楽しく彩る"
description = """
Emacsを起動すると、GNUのロゴと案内文が出るだけです。設定を少し加えれば、起動画面も配色も自分好みに彩れます。起動画面を入口に変えるdashboard、doom-themesとdoom-modelineによる配色とモードライン、括弧を色分けするrainbow-delimiters、遊び心のnyan-modeを、私のinit.elをもとに紹介します。
"""
date = 2026-10-20T12:57:20+09:00
[extra]
social_media_card = "ogp.webp"
local_image = "cover.avif"

[taxonomies]
tags = ["Tech", "Editor"]
+++

<!-- textlint-disable -->

{{< image src="cover.avif" alt="Cover" />}}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

<!-- more -->

Emacsを起動するとGNUのロゴと案内文が表示されるだけです。この見た目から、Emacsを古いエディタだと思う人も多いでしょう。しかし設定を少し加えれば、遊び心のあるユニークな見た目を与えることもできます。

連載「AI時代のEmacs設定術」の6回目となるこの記事では、Emacsを楽しく彩る設定を紹介します。設定は私のinit.elから抜き出しています。コード中の`……（省略）……`は、話題に関係しない設定を省いた箇所です。init.elの全体は[Gist](https://gist.github.com/yostos/631d858c283b1a15fc487f474c837a86)で公開しています。

## 起動画面を彩る

dashboardは、Emacsの起動画面を、よく使うものへの入口に変えるパッケージです。見た目が楽しいだけでなく、よく使うファイルや機能を並べておけるので、生産性の向上にも役立ちます。

MELPAにあるので、`use-package`に書いて`dashboard-setup-startup-hook`を呼んでおけば、起動したときにGNUの案内文の代わりにdashboardの画面が開きます。

バナーは`dashboard-startup-banner`で、同梱の4種類の文字バナーやEmacsのロゴから選ぶか、画像ファイルを指定します。画面に並べる部品とその順番は`dashboard-startupify-list`で決めます。私は既定の並びに、後で説明するボタンの行（`dashboard-insert-navigator`）を加えました。

一覧には、最近開いたファイル、プロジェクト、ブックマークを5件ずつ表示します。`r`、`p`、`m`でそれぞれの一覧に移り、`RET`で開きます。一覧の見出しとファイルには、[1回目](@/blog/2026/10/emacs-init-el/01-emacs-init-japanese/index.md)で設定したnerd-iconsのアイコンを付けています。

<!-- textlint-disable -->

{{< image src="dashboard.webp" alt="dashboardの起動画面" caption="dashboardを設定したEmacsの起動画面" />}}

<!-- textlint-enable -->

```emacs-lisp,name=init.el
(use-package dashboard
  :custom
  ;; 同梱の文字バナー（1〜4）の 3 番。等幅フォントで描かれ、色はテーマに従う
  (dashboard-startup-banner 3)
  (dashboard-banner-logo-title "Welcome back")
  (dashboard-center-content t)
  (dashboard-vertically-center-content t)
  ;; 並べる部品（フッターは起動のたびに冗談メッセージを 1 つ選んで出す）
  (dashboard-startupify-list '(dashboard-insert-banner
                               dashboard-insert-newline
                               dashboard-insert-banner-title
                               dashboard-insert-newline
                               dashboard-insert-navigator
                               dashboard-insert-newline
                               dashboard-insert-init-info
                               dashboard-insert-items
                               dashboard-insert-newline
                               dashboard-insert-footer))
  ;; 一覧と件数。r / p / m で各一覧に飛ぶ
  (dashboard-items '((recents   . 5)
                     (projects  . 5)
                     (bookmarks . 5)))
  ;; 長いパスは真ん中を省く
  (dashboard-path-style 'truncate-middle)
  (dashboard-path-max-length 60)
  ;; アイコンは nerd-icons を使う
  (dashboard-display-icons-p t)
  (dashboard-icon-type 'nerd-icons)
  (dashboard-set-heading-icons t)
  (dashboard-set-file-icons t)
  :config
  ;; ……（省略）……
  (dashboard-setup-startup-hook))
```

バナーの下には、よく開くものへのボタンを1行に並べています。今日の日誌を開くJournal、org-roamのノードを探すRoam、howmのメニューを開くHowm、[5回目](@/blog/2026/10/emacs-init-el/05-emacs-init-reading/index.md)で紹介したMewとElfeed、[3回目](@/blog/2026/10/emacs-init-el/03-emacs-init-claude-code/index.md)で紹介したghostelのターミナルを開くTerminalの6つです。ボタンは、`dashboard-navigator-buttons`に、アイコン、タイトル、マウスを重ねたときの説明、押したときに呼ぶ関数を1組にして並べます。

ボタンのアイコンもnerd-iconsです。アイコンは`nerd-icons-mdicon`などの関数を呼んで作るので、リストをバッククォートで書き、関数を呼ぶところにカンマを付けています。関数を呼ぶ以上、nerd-iconsが読み込まれている必要があるため、`:custom`ではなく、パッケージを読み込んだ後に実行される`:config`で設定しました。

ボタンは、カーソルを合わせて`RET`を押すか、クリックすれば動きます。ただ、そのたびにカーソルを動かすのは手間なので、ボタンと同じ操作を、カーソルの位置に関係なく1キーで呼べるようにしました。dashboardの画面では、小文字の`j`、`k`、`r`、`p`、`m`、`a`、`e`、`g`と数字がすでに使われています。一覧のショートカットの大文字も、dashboardが一覧を逆の順で移るのに使います。そこで、これらを避けた大文字の`J`、`O`、`H`、`W`、`F`、`T`を割り当てました。ボタンのタイトルの括弧の中にキーを書いておくと、画面を見るだけでキーがわかります。

```emacs-lisp,name=init.el
(use-package dashboard
  ;; ……（省略）……
  :config
  ;; よく開くものへのボタン。アイコンは nerd-icons の関数で作るので :config で設定する。
  ;; タイトルの（）内は下で割り当てる 1 キーのショートカット
  (setq dashboard-navigator-buttons
        `(((,(nerd-icons-mdicon "nf-md-calendar_today")
            "Journal(J)" "今日の日誌を開く"
            (lambda (&rest _) (my/howm-journal-today)))
           (,(nerd-icons-mdicon "nf-md-notebook_outline")
            "Roam(O)" "org-roam のノードを探す"
            (lambda (&rest _) (org-roam-node-find)))
           (,(nerd-icons-mdicon "nf-md-note_text_outline")
            "Howm(H)" "howm のメニューを開く"
            (lambda (&rest _) (howm-menu)))
           (,(nerd-icons-mdicon "nf-md-email_outline")
            "Mew(W)" "Mew を起動する"
            (lambda (&rest _) (mew)))
           (,(nerd-icons-mdicon "nf-md-rss")
            "Elfeed(F)" "elfeed を開いてフィードを更新する"
            (lambda (&rest _) (my/elfeed-open-and-update)))
           (,(nerd-icons-mdicon "nf-md-console")
            "Terminal(T)" "ghostel でターミナルを開く"
            (lambda (&rest _) (ghostel))))))
  ;; ボタンと同じ操作をカーソル位置に関係なく 1 キーで呼ぶ。
  ;; 小文字（j k r p m a e g）と数字は dashboard が使っているので大文字にする。
  ;; 一覧のショートカット（r m p a e）の大文字は dashboard が逆順移動に使うので避ける
  (keymap-set dashboard-mode-map "J" #'my/howm-journal-today)
  (keymap-set dashboard-mode-map "O" #'org-roam-node-find)
  (keymap-set dashboard-mode-map "H" #'howm-menu)
  (keymap-set dashboard-mode-map "W" #'mew)
  (keymap-set dashboard-mode-map "F" #'my/elfeed-open-and-update)
  (keymap-set dashboard-mode-map "T" #'ghostel)
  (dashboard-setup-startup-hook))
```

## 見た目を整える

Emacsにも、ほかのエディタと同じく配色を切り替えるテーマがあります。modus-themesなど20あまりが標準で入っていて、`M-x customize-themes`で試せます。MELPAにも多くのテーマがあります。

数あるテーマの中から私が選んだのは、doom-themesです。doom-themesは、Vimのキー操作を標準にしたEmacsの設定集Doom Emacsのために作られたテーマ集ですが、テーマだけを単体のパッケージとして使えます[^1]。doom-themesを選んだのは、色を変えるだけでなく、太字や斜体の使い分けまで作り込まれているからです。`doom-themes-enable-bold`と`doom-themes-enable-italic`を`t`にすれば、キーワードやコメントなどに太字や斜体が付きます。`doom-themes-org-config`を呼べば、Org modeの見出しなどもテーマに合わせて表示されます。どのテーマもこの作り込みが共通なので、テーマを替えても同じ見やすさを保てます。私はその中から、明るい配色のdoom-oksolar-lightを使っています。

ほかのエディタのステータスバーにあたるモードラインは、doom-modelineに替えています。doom-modelineは、Doom Emacsのモードラインを単体のパッケージにしたもので、ファイルの種類やGitのブランチ、エラーの数などをアイコンと一緒に表示します。doom-themesのテーマはdoom-modelineの部品の色まで定義しているので、モードラインだけが浮くことなく、画面全体の配色が揃います。アイコンにはnerd-iconsを使います。アイコンのフォントの入れ方は、[1回目](@/blog/2026/10/emacs-init-el/01-emacs-init-japanese/index.md)で説明しました。同じnerd-iconsで、補完候補、diredのファイル一覧、corfuのポップアップにもアイコンを付けています。この設定も1回目に載せています。

rainbow-delimitersは、括弧を深さごとに色分けするパッケージです。Emacs Lispのように括弧が何重にも重なる言語でも、対応する括弧を色で見分けられます。`prog-mode`のフックに登録して、プログラムを書くバッファで有効にしています。

このほか、`frame-resize-pixelwise`を`t`にしています。Emacsでは、OSのウィンドウにあたるものをフレームと呼びます。フレームは、既定では文字の幅と高さを単位に大きさを変えます。そのため、最大化したり、画面の半分に並べたりすると、画面の端との間に隙間ができます。この変数を`t`にすると、フレームがピクセル単位で大きさを変えるので、隙間なく画面に収まります。

```emacs-lisp,name=init.el
;; フレームを文字単位でなくピクセル単位で伸縮させ、最大化や並べたときの隙間をなくす
(setq frame-resize-pixelwise t)

(use-package doom-themes
  :custom
  (doom-themes-enable-bold t)
  (doom-themes-enable-italic t)
  :config
  (load-theme 'doom-oksolar-light t)
  ;; ……（省略）……
  ;; org-mode の見出しなどを doom-themes の配色に合わせる
  (doom-themes-org-config))

;; モードライン（アイコンは nerd-icons を使う）
(use-package doom-modeline
  :init
  (doom-modeline-mode 1))

;; 括弧を深さごとに色分けする
(use-package rainbow-delimiters
  :hook (prog-mode . rainbow-delimiters-mode))
```

## 遊び心を加える

最後に、遊び心のあるパッケージを1つ加えています。nyan-modeは、カーソルがバッファのどこにいるかを、虹を引いて飛ぶニャンキャットで表示するパッケージです。ニャンキャットは、2011年ごろにインターネットで流行した、虹を引きながら宇宙を飛ぶ猫のアニメーションです。バッファの先頭にいるときは虹が短く、末尾に近づくほど虹が伸びていきます。見た目は遊びですが、スクロールバーの代わりとして実用にもなります。虹のバーをクリックすると、バッファのその位置へジャンプできます。

doom-modelineはnyan-modeに対応していて、`nyan-mode`を有効にすると、行番号の横にニャンキャットを表示します。設定は、`use-package`で読み込んで有効にするだけです。既定では猫は止まっていますが、`nyan-animate-nyancat`を`t`にすれば猫が動き、`nyan-wavy-trail`を`t`にすれば虹が波打ちます。

```emacs-lisp,name=init.el
;; モードラインの位置表示を虹色のバーと猫にする（doom-modeline が行番号の横に出す）
(use-package nyan-mode
  :init
  (nyan-mode 1))
```

## まとめ

この記事では、Emacsの見た目を整え、楽しく彩る設定を紹介しました。

- 起動画面：dashboardで、最近開いたファイルやプロジェクト、ブックマークの一覧と、よく開くものへのボタンを並べる。ボタンと同じ操作は大文字の1キーで呼ぶ
- 配色：doom-themesで、色だけでなく太字や斜体まで作り込まれたテーマを使う
- モードライン：doom-modelineで、ファイルの種類やGitのブランチをアイコンと一緒に表示する
- 括弧：rainbow-delimitersで、深さごとに色を変える
- 遊び心：nyan-modeで、バッファの位置をニャンキャットで表示する

見た目の設定は、なくてもEmacsは使えます。それでも、毎日長い時間向き合う道具だからこそ、開くのが楽しくなる見た目にしておく価値があります。dashboardは、見た目を整えるだけでなく、よく使うファイルや機能への入口にもなります。

[^1]: Vimのキー操作を使いたいならVimを使うので、Doom Emacs自体は使っていません。

## References

確認日はいずれも2026年10月20日です。

<!-- textlint-disable -->

{% <references> %}

- [dashboard](https://github.com/emacs-dashboard/dashboard)
- [doom-themes](https://github.com/doomemacs/themes)
- [doom-modeline](https://github.com/seagle0128/doom-modeline)
- [rainbow-delimiters](https://github.com/Fanael/rainbow-delimiters)
- [nyan-mode](https://github.com/TeMPOraL/nyan-mode)

{% </references> %}

<!-- textlint-enable -->
