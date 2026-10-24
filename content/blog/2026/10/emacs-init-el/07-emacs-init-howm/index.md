+++
title = "AI時代のEmacs設定術(7): Emacsでメモ - Howm"
description = """
思いついたことを書き留めようとしても、どのファイルに、どんな見出しで書くかを考えた時点で手が止まります。日本発のメモ環境Howmなら、1行から書き始められます。Org modeと併用するHowmの設定を、私のinit.elをもとに紹介します。
"""
date = 2026-10-24T14:16:00+09:00
[taxonomies]
tags = ["Tech", "Editor"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.avif"
+++

<!-- textlint-disable -->

{{< image src="cover.avif" alt="Cover" />}}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

<!-- more -->

思いついたことを書き留めるとき、どのファイルに、どんな見出しで書くかを考えた時点で手が止まります。Howmは、そうしたことに迷わず、1行から書き始められるEmacsのメモ環境です。

連載「AI時代のEmacs設定術」の7回目となるこの記事では、Org modeとHowmを併用する私の設定を紹介します。コード中の`……（省略）……`は、その節の話題に関係しない設定を省いた箇所です。init.elの全体は[Gist](https://gist.github.com/yostos/631d858c283b1a15fc487f474c837a86)で公開しています。

## Howmとは

Howmは、「一人お手軽Wikiもどき」の頭文字から名付けられた、Emacsのメモ環境です。2002年に公開され、いまも開発が続いています。MELPAにあるので、`use-package`で入れられます。

Howmの考え方は「整理しない、後から探す」です。メモは1件1ファイルのテキストとして溜めていき、フォルダーやタグで分類しません。必要になったら、検索で引き出します。

ファイル名を考えなくてよいのも、Howmの大きな利点です。新しいメモのファイル名は、作った日時から自動で付きます。org-roamのノードと同じく、ファイル名にはメモの中身を表す言葉が入りません。1件1ファイルで書いていくと、ふつうはファイルを作るたびに名前を考えることになり、それが書き始める前の小さな負担になります。Howmでは、この負担がありません。メモを探すときもファイル名ではなく、タイトルや本文、キーワードで探します。

メモ同士は、キーワードでつながります。行に`<<< Emacs`と書くと、「Emacs」がキーワードになります。以後、どのメモに書いた「Emacs」という文字にも下線が付き、そこで`RET`を押すと、キーワードを含むメモの一覧が出ます。`>>> Emacs`と書けば、その語を検索するリンクになります。Wikiのようにページを作らなくても、書いた語がそのままほかのメモとつながります。はてなブログのキーワードの自動リンクに近い仕組みですが、キーワードの辞書はサービス全体で共有するものではなく、自分のメモの中だけのものです。

予定やToDoも、メモの中に書きます。行頭に`[2026-10-25]+`のように日付と記号を書くと、その行がToDoになり、Howmのメニューに並びます。記号によって、日付が近づくにつれて上に浮いてくるもの、日付が過ぎると少しずつ沈んでいくものなど、並び方が変わります。終わったら記号を`.`に変えれば、一覧から消えます。

## Howm vs Org mode

[2回目](@/blog/2026/10/emacs-init-el/02-emacs-init-org/index.md)で紹介したように、私はOrg modeでタスクと知識を管理していました。それでもHowmを併用し始めたのは、書き始めるまでの手間を減らしたかったからです。org-roamでは、ノードを作るたびにタイトルを決め、タグを付けます。知識を整理するにはこの手間が意味を持ちますが、ちょっとしたメモにはおおげさです。Howmなら、`C-c ; c`で新しいメモを開いて書き始めるだけです。

タスクの管理も、Howmのほうがシンプルだと感じています。Org modeでは、TODOを書くファイルを決め、org-agendaに登録しておく必要があります。Howmでは、どのメモに書いたToDoも、日付と記号さえあればメニューに集まります。会議のメモの途中にToDoを1行書いておくだけで済みます。

メモ同士のつながり方も違います。Howmでは、キーワードがメモを勝手につなぎます。メモを開くと、別の日に別の文脈で書いたメモとの関係が見え、思いがけない組み合わせがアイデアになることがあります。分類しないまま書き溜めたメモが、キーワードを通して育っていきます。Howmの「整理しない、後から探す」という考え方が、最もよく表れているところだと思います。

一方、org-roamでは、どのノードとどのノードをつなぐかを自分で決めてリンクを張ります。1本ずつリンクを張るのは、白紙に自分で道を書き込んでいく作業に似ています。ときどき全体を見渡すと、書き込んできた道がそのまま自分の知識の地図になっています。

いまは、次のように使い分けています。

- Howm：普段のメモ、日誌、タスク
- Org mode：org-roamで整理して残したい知識やアイデア、ブログ記事のドラフト

Howmは、日々のメモを書き溜め、つながりの中でアイデアを育てる場所です。org-roamは、育ったアイデアのうち残したいものをノードにまとめ、知識の地図に書き込む場所です。2回目で紹介したorg-roam-dailiesの日誌も、いまはHowmに移しました。

## 自由なフォーマット

Howmが決めている書式は、キーワード、リンク、予定とToDoの記号、1行目をタイトルとして扱うことくらいです。それ以外は、メモに何をどう書いてもかまいません。

Howmの既定では、メモは拡張子`.txt`のプレーンテキストで、タイトル行の頭に`=`を付けます。覚える書式が少ないので、このまま使っても十分です。

MarkdownやOrg modeで書きたい人のために、Howmにはhowm-markdownとhowm-orgが付属しています。howm-markdownを読み込むと、メモの拡張子が`.md`に、タイトルの記号がMarkdownの見出しの`#`に変わります。ふだんMarkdownでメモを書いている人には、こちらが馴染みやすいでしょう。howm-markdownとhowm-orgは、どちらか一方だけを使います。

私は、HowmのメモをOrg modeの形式で書いています。howm-orgを読み込むと、メモの拡張子が`.org`になり、タイトルの記号がOrgの見出しの`*`に、日時がOrgのタイムスタンプの書式に変わります。メモはOrg modeで開くので、見出しの折りたたみ、表、コードブロックなど、Org modeの機能がそのまま使えます。私のメモは、たとえば次のようになります。

```org
* Mew の設定メモ
[2026-10-20 Tue 09:12]
<<< Mew

送信の設定は >>> Fastmail を参照する。

[2026-10-25]+ アドレス帳を整理する
[2026-10-30]! 設定をブログ記事にまとめる
```

howm-orgは、Howmより先に読み込む必要があります。`use-package`の`:init`は、パッケージを読み込む前に実行されるので、ここで`require`します。howm-orgは、Howmのキーの接頭辞も、Org modeの`C-c ,`とぶつからない`C-c ;`に移します。メニューは`C-c ; ;`、新しいメモは`C-c ; c`で開きます。ただし、Howmのメモの中では、Org modeの`C-c ;`（`org-toggle-comment`）は使えなくなります。Wiki風の`[[...]]`のリンクも、Org modeのリンクと書式が重なるので無効になります。

howm-orgは、メモを`~/howm/`の直下へ並べる形にファイル名の書式を変えます。私はメモを年と月のディレクトリに分けたいので、howm-orgを読み込んだ後、`howm-file-name-format`を書き直しています。`howm-directory`など4つの変数は、Howmを読み込むときに参照されるので、これも`:init`で設定します。キーワードの一覧と検索の履歴は、既定ではホームディレクトリの直下に作られるので、`~/howm/`にまとめました。

Howmのメモでhowm-modeが有効になるのは、Howmのメニューや一覧から開いたときだけです。`C-x C-f`や最近開いたファイルの一覧から開くと、キーワードに下線が付きません。そこで、`find-file-hook`に`howm-set-mode`を登録し、`~/howm/`の下のファイルなら、どこから開いてもhowm-modeにしています。

最後の2行のフックは、警告を避けるためのものです。howm-orgは、メモの一覧と内容を表示するバッファにもOrg modeの色付けを持ち込みます。この色付けのうち、コードブロックを言語ごとに色付けする処理は、Org mode以外のバッファで動くと警告を出します。そこで、この2つのバッファでは、言語ごとの色付けをしないようにしています。

```emacs-lisp,name=init.el
(use-package howm
  ;; 自動読み込みの定義（autoload）が無く、読み込み時に C-c ; の各キーが作られるので起動時に読む
  :demand t
  :init
  ;; org 形式にする。howm より先に読み込む必要がある。
  ;; 見出し記号（*）、日時の書式、メニューファイルの拡張子、キーの接頭辞などを org 向けに変える
  (require 'howm-org)
  ;; howm-org はファイル名を ~/howm/ 直下に並べる形にするので、年・月のディレクトリに分ける形に戻す
  (setq howm-file-name-format "%Y/%m/%Y-%m-%d-%H%M%S.org")
  ;; この 4 つは読み込み時に参照されるので、読み込む前に設定する
  (setq howm-directory "~/howm/"
        ;; キーワード一覧と検索履歴は既定だと ~/ 直下に作られるので howm-directory にまとめる
        howm-keyword-file "~/howm/.howm-keys"
        howm-history-file "~/howm/.howm-history"
        ;; メニューを英語にする（既定は言語環境で決まる）。
        ;; 変えるときは ~/howm/0000-00-00-000000.org を消して作り直す
        ;; （中のボタン名は言語ごとの対応表で引くので、古い言語のままだと押しても動かない）
        howm-menu-lang 'en)
  :config
  ;; howm-mode になるのは howm のメニューや一覧から開いたときだけなので、
  ;; C-x C-f や最近のファイルから開いたときも ~/howm/ 配下なら howm-mode にする
  (add-hook 'find-file-hook #'howm-set-mode)
  ;; howm-org は一覧（*howmS*）と内容表示（*howmC*）に org の色付けを持ち込むが、
  ;; コードブロックを言語ごとに色付けする処理は org-element-at-point を呼び、
  ;; org 以外のバッファでは警告が出る。この 2 つのバッファでは言語別の色付けをしない
  (defun my/howm-view-disable-src-fontify ()
    (setq-local org-src-fontify-natively nil))
  ;; howm-org の色付け（howm-org-font-lock-minor-mode）より先に動くよう depth を負にする
  (add-hook 'howm-view-summary-mode-hook #'my/howm-view-disable-src-fontify -50)
  (add-hook 'howm-view-contents-mode-hook #'my/howm-view-disable-src-fontify -50)
  ;; ……（省略）……
  )
```

## その他便利なHowm機能

`C-c ; ;`で開くメニューは、Howmの入口です。上にはメモの作成や検索のボタンが並び、その下に予定（Schedule）、ToDo、最近のメモが続きます。既定では、日付がまだ来ていないToDoや済んだToDoも、沈んだ状態で件数の上限まで表示されます。私はこれを出さないように`howm-menu-todo-priority`を変え、いま気にするべきToDoだけが並ぶようにしました。予定は、既定の1週間先ではなく2週間先まで表示します。

<!-- textlint-disable -->

{{< image src="howm-menu.webp" alt="Howmのメニュー画面" caption="Howmのメニュー。ボタンの下に予定、ToDo、最近のメモが並ぶ" />}}

<!-- textlint-enable -->

```emacs-lisp,name=init.el
(use-package howm
  ;; ……（省略）……
  :config
  ;; ……（省略）……
  ;; メニューの Todo 欄に、日付がまだ来ていない（眠っている）項目と済みの項目を出さない。
  ;; 既定は (- howm-huge+) で、沈んではいるが件数の上限まで表示される
  (setq howm-menu-todo-priority (- howm-huge-))
  ;; メニューの Schedule 欄に出す予定を、今日から 2 週間先までにする（既定は 7 日）
  (setq howm-menu-schedule-days 14)
  (keymap-global-set "C-c ; j" #'my/howm-journal-today)
  ;; メニューの [Journal] ボタン。ボタン自体はメニューファイル（~/howm/0000-00-00-000000.org）の
  ;; Create: 行に %"j"[Journal] と書いてある。作り直したときは書き足す
  (with-eval-after-load 'howm-lang-en
    (add-to-list 'howm-menu-command-table-en
                 '("[Journal]" my/howm-journal-today))))
```

日誌は、自作のコマンド`my/howm-journal-today`で書いています。`C-c ; j`を押すと、今日の日誌を開き、Logの見出しの末尾にカーソルを移します。今日の日誌がまだなければ、タイトル、日時、`<<< JOURNAL`、Logの見出しを入れた新しいメモを作ります。日誌に`JOURNAL`というキーワードを入れておくと、どの日誌でも`JOURNAL`の上で`RET`を押すだけで、日誌の一覧が出ます。

新しいメモを作る`howm-create`は、雛形を入れてからメモを開きます。日誌では自分の書式を使いたいので、雛形を入れない`howm-create-file`でファイルを作り、書式を書き込んでから`howm-create-finish`でhowm-modeを有効にしています。ファイル名の決め方や、年と月のディレクトリを作る処理は、Howmに任せています。曜日を英語で書くのは、org-roam-dailiesから移した日誌に書式を揃えるためです。

```emacs-lisp,name=init.el
(defun my/howm-journal-today ()
  "今日の日誌（タイトルが「* YYYY-MM-DD Sun Journal」のメモ）を開き、Log の末尾に移る。
無ければ、タイトル・日時・<<< JOURNAL・** Log を入れた新しいメモを作る。"
  (interactive)
  (let* ((today (format-time-string "%Y-%m-%d"))
         ;; 曜日は移行した日誌に合わせて英語（Sat など）で書く
         (title (let ((system-time-locale "C"))
                  (format-time-string "* %Y-%m-%d %a Journal")))
         (dir (expand-file-name (file-name-directory
                                 (format-time-string howm-file-name-format))
                                howm-directory))
         (file (and (file-directory-p dir)
                    (seq-find
                     (lambda (f)
                       (with-temp-buffer
                         (insert-file-contents f nil 0 200)
                         (looking-at-p (concat (regexp-quote title) "$"))))
                     (directory-files dir t (concat "\\`" today "-.*\\.org\\'"))))))
    (if file
        (find-file file)
      ;; ファイル名の決定・年月ディレクトリの作成・オープンは howm に任せる。
      ;; howm-create と違い雛形（howm-template）を入れないので、日誌の書式をそのまま書ける
      (howm-create-file)
      ;; 曜日は移行した日誌に合わせて英語（Sat など）で書く
      (let ((system-time-locale "C"))
        (insert title "\n"
                (format-time-string "[%Y-%m-%d %a %H:%M] ") "\n"
                "<<< JOURNAL\n\n** Log\n"))
      ;; howm-create と同じく howm-mode を有効にして howm-create-hook を動かす
      (howm-create-finish))
    ;; Log の最後の行の末尾に移る（RET で次の行を書き始められる）
    (goto-char (point-min))
    (when (re-search-forward "^\\*\\* Log$" nil t)
      (org-end-of-subtree t)
      (skip-chars-backward " \t\n"))))
```

日誌は、メニューの[Journal]ボタンからも開けます。メニューのボタンは、メニューファイル（`~/howm/0000-00-00-000000.org`）に`%"j"[Journal]`と書き、ボタン名と押したときに呼ぶコマンドの対応表`howm-menu-command-table-en`に登録して作ります。[6回目](@/blog/2026/10/emacs-init-el/06-emacs-init-ui/index.md)で紹介したdashboardにも、JournalとHowmのボタンを置き、`J`と`H`の1キーで開けるようにしました。同じ行にorg-roamのRoamのボタンも並べているので、Emacsを起動した画面から、HowmとOrg modeのどちらにもすぐ書き始められます。

書き溜めたメモは、検索で探します。`C-c ; s`で文字列を、`C-c ; g`で正規表現を検索し、ヒットしたメモを一覧します。一覧では、カーソルを動かすだけで、隣のウィンドウにメモの中身が表示されます。キーワードを入れておけば、その語の上で`RET`を押すだけで、関係するメモがすべて集まります。

## まとめ

この記事では、Org modeと併用するHowmの設定を紹介しました。

- 使い分け：普段のメモ、日誌、タスクはHowmに書き、キーワードのつながりからアイデアを育てる。整理して残す知識やブログ記事のドラフトはorg-roamに書き、自分で張ったリンクによって知識の地図にする
- 書式：howm-orgで、HowmのメモをOrg modeの形式で書く
- 日誌：自作のコマンドで今日の日誌を開き、メニューとdashboardからも1キーで呼ぶ
- 探し方：キーワードと全文検索で、整理しないまま後から引き出す

Org modeと別にHowmを置く一番の理由は、1行から書き始められる気軽さです。メモとToDoのどちらも、ファイル名や置き場所を考えずに書けます。メモはOrg modeの形式なので、Org modeの操作がそのまま使え、育ったアイデアをorg-roamへ移すのも簡単です。

必要な設定は、howm-orgの読み込みと、数か所の調整だけです。Org modeを使っていて、ちょっとしたメモの置き場所に迷っているなら、試してみる価値があります。

## References

確認日はいずれも2026年10月24日です。

<!-- textlint-disable -->

{% <references> %}

- [howm](https://kaorahi.github.io/howm/)
- [howm（GitHub）](https://github.com/kaorahi/howm)

{% </references> %}

<!-- textlint-enable -->
