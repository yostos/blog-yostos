+++
title = "pCloud DriveのmacOS Tahoe問題"
description = """
pCloudを長らく使用していますが、macOS TahoeにしてからpCloud Driveが機能せずMac全体が一時的に不安定になりました。
他のユーザーでも同様らしくアプリの改善は時間がかかりそうなので、別の方法を検討しました。
"""
date = 2026-06-27T10:00:00+09:00
[taxonomies]
tags =[ "Tech","Mac","Apple","CLI" ]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = "macOS TahoeでpCloud Driveが起動せず、開こうとするとOS全体が一時的に不安定になりました。原因はファイルシステム拡張(pCloudFS / macFUSE)とmacOS Tahoeの相性の問題です。macOSの拡張機能に依存しているので、Apple Siliconに移行してからは問題が多い為、pCloud Driveはアンインストールし、別経路として持っていたrcloneに一本化しました。rcloneのコマンド転送はカーネル拡張に依存せずCLIで完結するため、OSアップデートの影響を受けにくいのが利点です。"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp",alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

macOS Tahoe(macOS 26)に上げてから、pCloud Driveが起動するが機能しない状態となりました。
やっかいなのは、アプリ単体では済まず、うっかりpCloud Driveを開こうとするとキーボードが効かなくなるなどMac全体が一時的に不安定になる点です。

## pCloudとは

pCloudは、スイスのpCloud AGが提供するクラウドストレージサービスです。買い切りの生涯プランがあること、ファイルを暗号化して預けられること、そしてアカウントを作ると無料枠から使い始められることで知られています。

Macで使う場合、もっとも手軽なのは公式のpCloud Driveアプリです。これはクラウド上のファイルを、ローカルの仮想ドライブ(`~/pCloud Drive`)としてマウントして見せてくれます。Finderから普通のフォルダのように開けるので、クラウドを意識せずに使えるのが利点です。

一方で、この「仮想ドライブとして見せる」仕組みは、macOSのファイルシステム拡張に依存します。後述するように、ここがOSのアップデートで影響を受けやすい部分でもあります。

## macOS Tahoeでの不具合

私の環境はApple SiliconのMacで、OSはTahoe(macOS 26)です。アップデート後、pCloud Driveが機能せず、開こうとするとOS全体の挙動が一時的に不安定になりました。

同様の現象が一般に報告されているか調べたところ、Tahoe環境での不具合報告が複数見つかりました。代表的なものは次の通りです。

- アップデート後に「Enable Disk(仮想ドライブのマウント)」が機能しない
- メニューバーのアイコンが表示されない
- ドライブは見えてもマウント・同期ができない
- ドライブ有効化時に「outdated(古い)」と表示され有効化できない

これらはフォーラムでの報告であり、「同様の事例が存在する」ことの裏付けにはなりますが、原因や解決を断定する根拠にはなりません。pCloud公式が症状ごとの原因を断定して公表しているわけでもありません。そのため、ここから先に書く原因は、あくまで私の推測として読んでください。

pCloud Driveは、クラウドをローカルの仮想ドライブとして見せるために、ファイルシステム拡張(pCloudFS / macFUSE)を使います。この低レベルの拡張がロードに失敗したり、カーネル側で引っかかったりすると、アプリ単体のクラッシュにとどまらず、OS全体の挙動に波及することがあります。私が遭遇した「開こうとすると全体が不安定」という症状は、このパターンと整合します。OSのメジャーアップデート直後は、こうした低レベル拡張の互換性が崩れやすく、不安定になりがちです。

## pCloud Driveのアンインストール

macOS向けのpCloud DriveはApple Siliconになってから問題も多く、macOSの変更による影響も受けやすいのでうんざりしていました。

OS全体を巻き込んで不安定になるアプリの回復に時間をかけるより、他の方法に移行しpCloud Driveはアンインストールすることにしました。

アンインストールは次の2ステップが必要です。

1. ログイン項目からpCloud Driveを外してmacOSを再起動
2. pCloud Driveの削除

まずシステム設定 → 一般 → ログイン項目と機能拡張からpCloud Driveを外し、いったんmacOSを再起動して拡張の常駐を切ります。

次にアプリ本体を削除です。

手動で削除する場合は、pCloud Driveを完全終了(できればアプリ内でログアウト/Unlink)してから、アプリ本体をゴミ箱へ移し、`~/Library`配下の残骸を削除します。主な残骸は次の場所です。

```bash,name=leftovers.txt
~/Library/Application Support/pCloud
~/Library/Application Support/com.pcloud.pcloud.macos
~/Library/Caches/com.pcloud.pcloud.macos
~/Library/Preferences/com.pcloud.pcloud.macos.plist
```

私が実際に使ったのは、CLIのアンインストーラであるMole(`tw93/Mole`)です。Homebrewで導入でき、コマンド名は`mo`になります。

```bash,name=install-mole.sh
brew install mole
```

`mo uninstall`は、アプリ本体に加えて、launch agentやPreferences、Cachesといった関連ファイルもまとめて削除してくれます。安全のため、まず`--dry-run`で削除対象を確認してから本実行しました。対象アプリの正確な名前は`--list`で確認できます。

```bash,name=uninstall.sh
mo uninstall --list                   # mo uninstall が受け付ける正確なアプリ名を一覧表示
mo uninstall --dry-run "pCloud Drive"  # 削除対象を事前確認(変更は行わない)
mo uninstall                           # 対話形式の一覧から pCloud Drive を選んで実行
```

引数なしの`mo uninstall`は対話形式のセレクタを開くので、一覧からpCloud Driveを選んで実行します。アプリ名を引数で渡せば、対話なしで直接アンインストールできます。削除されたファイルは既定でゴミ箱へ送られるため、必要なら復元できます。

Moleが消すのは、主にユーザーレベルの関連ファイルです。macOSにシステム拡張として登録された部分(pCloudFS / システム拡張)は対象外になることがあります。通常はmacOSを再起動するとクリアされますが、残っていないかは次のコマンドで確認できます。

```bash,name=check-extensions.sh
systemextensionsctl list   # pCloud AG の拡張が残っていないか確認
```

Mole自身も、macOS 15以降では一部の拡張系の権限エントリがアプリ削除後も残ること、そしてその種のリセットはグローバルかつリカバリモードを要するため自動では行わないことを、警告として明示しています。ツール任せにせず、最後は再起動と`systemextensionsctl list`での確認で締めるのが現実的です。私の環境では、ログイン項目から外して再起動したあとにアンインストールしたこともあり、最終的にpCloud AGの拡張は1つも残りませんでした。

なお、pCloud Driveアプリをアンインストールしても、pCloudアカウント自体は消えません。Web(my.pcloud.com)からファイルにはアクセスできますし、消えるのは有効化済みの同期設定とカスタム設定だけです。

## rcloneでの設定方法とメリット

[rclone](https://rclone.org/)は、各種クラウドストレージをコマンドラインから統一的に扱えるツールです。以前「[rcloneとS3ライフサイクルで作る個人データのコールドアーカイブ](@/blog/2026/04/rclone/index.md)」でAmazon S3を使った長期保管の構成をまとめましたが、pCloudもバックエンドとして公式にサポートされています。

設定は`rclone config`の対話で行います。ブラウザ認証を済ませると、設定ファイル`~/.config/rclone/rclone.conf`が作られ、内容は次のようになります。

```toml,name=rclone.conf
[pcloud]
type = pcloud
hostname = eapi.pcloud.com
token = {"access_token":"<rclone config の認証で自動生成されるアクセストークン>","token_type":"bearer","expiry":"0001-01-01T00:00:00Z"}
```

ここで`token`は`rclone config`のOAuth認証で自動生成されるものです。手で書く必要はありませんし、アクセストークンそのものなので、他人に見せたりリポジトリにコミットしたりしないよう注意してください。この記事でも実際の値はプレースホルダに置き換えています。

<!-- textlint-disable -->

{% aside(position="right") %}
私はプライバシーを重視しているので、ヨーロッパリージョン(`eapi.pcloud.com`)を使っています。
{% end %}

<!-- textlint-enable -->

`hostname`はリージョンを指します。`eapi.pcloud.com`はヨーロッパリージョン、`api.pcloud.com`(デフォルト)は米国リージョンです。アカウントがヨーロッパリージョンの場合は、ここを`eapi.pcloud.com`に設定しておかないとトークンエラーになることがあります。通常はOAuth認証の過程で適切に設定されますが、うまくいかないときはこの値を疑ってください。

設定できたら、まずは中身が見えるか確認します。

```bash,name=verify.sh
rclone lsd pcloud:                                # トップ階層のディレクトリ一覧
rclone copy pcloud:My\ Pictures ~/Downloads/pics  # 取り出し(ダウンロード)
rclone sync ~/work pcloud:work                    # ローカルからクラウドへ同期(送信)
```

Finderのようにフォルダとしてマウントしたい場合は`rclone mount`も使えますが、こちらはmacFUSEを必要とします。日常的なファイルの取り出しや同期は、マウントせずとも上記のコマンドだけで完結します。

pCloud Driveからrcloneへ寄せる利点は、大きく2つです。

macOSへの非依存
: コマンドベースの転送(`copy`、`sync`、`lsd`、`cat`)はファイルシステム拡張を使わず、ユーザーランドだけで完結する。今回の不具合の原因だったpCloudFS / macFUSEとは無縁で、OSのメジャーアップデートにも振り回されない。

CLIでの自動化
: CLIとなることで、`launchd`やシェルスクリプトに組み込みが自由になる。バックアップや定期同期などを自動化して回せる。

## pCloudのサービス継続性について

ここで、pCloudというサービス自体の信頼性にも触れておきます。

pCloudの大きなウリは、一度の支払いで使い続けられる**買い切り(Lifetime)プラン**です。
ただし、その「Lifetime」が何を指すのかは、規約を読むと印象より限定的です。pCloudの利用規約は、買い切りプランの有効期間を「アカウント所有者の生存期間か99年のいずれか短い方」と定義しています。さらに「pCloudが事業を停止した場合、アカウントは終了し、サービスは提供されない」とも明記されています。買い切りは、永久でも、企業の存続から独立した保証でもありません。

そうなると運営元の規模が気になります。

pCloudを提供するpCloud AGはスイスの非上場企業で社員は数十人規模、外部資本を入れないブートストラップ経営です。
非上場企業のため正確な業績は外から分かりません。出回っている年商も10億円程度[^1]です。

[^1]: 創業者の自己申告(約16.5億円)と第三者の推計(約6.6億円)で2倍以上の開きがあり、健全性を客観的に確かめる手段がありません。

pCloudサービスは設立から10年以上続き、ユーザーも2,000万を超えて伸びており、「経営が危ない」という状況ではなさそうです。

しかし、規模の小ささ自体が構造的な継続性リスクになります。買収や方針転換、大手との競争で、サービスの将来を一個人が見通すことはできません。また、規模の小ささが、今回の様な新しいmacOSへの対応の遅れの要因ともなっているかと思います。

だからこそ、買い切りだからと唯一の保管先にはせず、今回のrcloneのような別経路や、ローカル・別クラウドにもコピーを持っておくのが現実的だと考えています。

## まとめ

macOS Tahoeとの互換性によるpCloud Drive不具合から、一旦rcloneに移行しました。

とはいえ、pCloud DriveはDropboxのSmart Syncのようにキャッシュだけのローカルに置く方式で便利なので、いつか安定したら戻りたいものです。

振り返ってみると、pCloudの2TBライフタイムを購入したのは2021年です。350ドル（当時のレート1ドル約109円で約38,200円）の一括払いでした。仮に、Dropbox Plusの2TBを使用していたとしたら、年額15,840円（税込）かかります。
2年半足らずで買い切りが追いつき、購入から約5年が経った今では、Dropboxなら累計8万円ほどかかっていた計算です。円で累計コストを並べると、その差がはっきりします。

<!-- textlint-disable -->

{{ image(src="cost-comparison.svg", alt="2TBストレージの累計コスト。pCloudは2021年に約38,200円の買い切り、Dropboxは年額15,840円で累計が増え、約2.4年でpCloudが有利になる。") }}

<!-- textlint-enable -->

あまりヘビーに依存せず上手に使っていきたいと思います。

## References

<!-- textlint-disable -->

{% references() %}

- [pCloud](https://www.pcloud.com/release-notes/mac-os.html). 「pCloud for macOS リリースノート」
- [pCloud](https://www.pcloud.com/ja/help/general-help-center/what-if-i-uninstall-pcloud-from-my-computer). 「コンピュータからpCloudをアンインストールするとどうなりますか」
- [pCloud](https://www.pcloud.com/terms_and_conditions.html). "Terms and Conditions"
- [Apple Support](https://support.apple.com/en-us/102610). "Delete apps on your Mac"
- [rclone](https://rclone.org/pcloud/). "pCloud backend documentation"
- [Mole](https://github.com/tw93/mole). "tw93/Mole"

{% end %}

<!-- textlint-enable -->
