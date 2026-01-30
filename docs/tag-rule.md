# ブログタグ体系 - 確定版

このドキュメントは、ブログ全記事のタグを分析し、確定したタグ付けルールをまとめたものです。

## タグ付けの基本ルール

### 1. Movies タグのルール
- **Moviesタグを持つ記事には必ずEntertainmentタグも付ける**
- 例外: 映画主題歌など音楽が主題の記事は例外を認める場合がある

### 2. ギター関連タグのルール
- **ギター演奏記事**: `["Music", "Guitar"]`
- **エフェクター専門記事**: `["Guitar Pedals"]` のみ
- **エフェクター + ギター言及**: `["Guitar", "Guitar Pedals"]`
- **ギターブランド/モデル名タグは使用しない**（Epiphone, Texan, Fender, YAMAHA, Stratocaster等）

### 3. 写真関連タグのルール
- **"Photo" は "Photography" に統一**
- **"Photo Friday"** は固有タグとして継続（Photo Friday企画の投稿用）

### 4. 固有名詞タグの使用ルール

#### 使用禁止の固有名詞タグ
以下のタグは使用せず、親カテゴリーに統合：
- **音楽**: Beatles → 削除
- **製品**: Claude → 削除、SNS → Techに統合、NOSTR → 削除
- **組織**: NHK → 削除
- **ギターブランド/モデル**: Epiphone, Texan, Revstar, Stratocaster, Fender, YAMAHA等 → 削除

#### 使用可能な固有名詞タグ
以下のタグは継続使用可：
- **ツール**: Claude Code
- **ゲーム**: Splatoon（必ずGameタグと併用）
- **企業**: IBM
- **カテゴリー**: Old Media
- **地域**: Chiba
- **製品カテゴリー**: Drone

## タグ使用頻度（上位30）

| タグ | 記事数 | カテゴリー | 備考 |
|------|--------|-----------|------|
| Tech | 73 | Technology | 最頻出タグ |
| Guitar | 37 | Music | 音楽関連2位 |
| Current Affairs | 37 | News | 時事ネタ |
| Music | 34 | Music | 音楽総合 |
| Generative AI | 28 | Technology | AI関連 |
| Drone | 15 | Gadget/Hobby | ドローン |
| Game | 15 | Entertainment | ゲーム総合 |
| Photography | 14 | Creative | 写真撮影 |
| Movies | 12 | Entertainment | 映画（複数形） |
| Splatoon | 12 | Entertainment | 固有名詞（ゲーム） |
| Software | 11 | Technology | ソフトウェア |
| Guitar Pedals | 11 | Music | エフェクター（複数形統一） |
| Security | 11 | Technology | セキュリティ |
| Weekly Buzz | 10 | News | 定期連載 |
| AWS | 10 | Technology | クラウド |
| Travel | 8 | Lifestyle | 旅行（単数形） |
| Gadget | 8 | Technology | ガジェット |
| Career | 7 | Lifestyle | キャリア |
| CLI | 6 | Technology | コマンドライン |
| Weblog | 6 | Technology | ブログ運営 |
| Music Production | 5 | Music | 音楽制作 |
| Claude Code | 5 | Technology | ツール名（使用可） |
| Entertainment | 5 | Entertainment | 娯楽総合 |
| Certification | 5 | Career | 資格（単数形） |
| Web | 5 | Technology | Web技術 |
| Font | 4 | Design | フォント |
| Anime | 4 | Entertainment | アニメ |
| Gourmet | 4 | Lifestyle | グルメ |
| Books | 3 | Culture | 書籍（複数形） |
| Mac | 3 | Technology | Apple Mac |

## カテゴリー別タグ体系

### 1. Technology (テクノロジー)

#### 主要タグ
- **Tech** (73) - テクノロジー総合
- **Software** (11) - ソフトウェア全般
- **Security** (11) - セキュリティ
- **CLI** (6) - コマンドラインツール
- **Web** (5) - Web技術
- **Weblog** (6) - ブログ運営技術

#### サブカテゴリー
- **Generative AI** (28) - 生成AI
  - Claude Code (5) ✓ 使用可
- **Cloud**
  - AWS (10)
  - Google Cloud (1)
- **プログラミング言語**
  - Python (3)
  - TypeScript (1)
  - Go (1)
  - Node (3)
- **その他**
  - API (2)
  - IT Governance (1)
  - OSS (1)

### 2. Music (音楽)

#### 主要タグ
- **Music** (34) - 音楽総合
- **Guitar** (37) - ギター
- **Music Production** (5) - 音楽制作

#### サブカテゴリー
- **Guitar Pedals** (11) - エフェクターペダル（複数形統一）

**注意**: ギターブランド/モデル名タグ（Epiphone, Texan, Fender, YAMAHA等）は廃止

### 3. Entertainment (エンターテインメント)

#### 主要タグ
- **Entertainment** (5) - 娯楽総合
- **Movies** (12) - 映画（複数形）
  - ⚠️ Moviesタグには必ずEntertainmentタグも付ける
- **Anime** (4) - アニメ
- **Game** (15) - ゲーム
- **Manga** (1) - マンガ（単数形）

#### サブカテゴリー
- **Splatoon** (12) - 固有名詞、必ずGameと併用 ✓ 使用可

### 4. Creative (クリエイティブ)

#### 主要タグ
- **Photography** (14) - 写真撮影（Photoは廃止）
- **Design** (3) - デザイン
- **Font** (4) - フォント
- **Art** (2) - アート

#### サブカテゴリー
- **Photo Friday** (3) - 定期企画（固有タグとして継続）

### 5. Lifestyle (ライフスタイル)

#### 主要タグ
- **Travel** (8) - 旅行（単数形）
- **Career** (7) - キャリア
- **Gourmet** (4) - グルメ
- **Life** (3) - 生活
- **Gadget** (8) - ガジェット

#### サブカテゴリー
- **Certification** (5) - 資格（単数形）
- **Drone** (15) - ドローン（ホビー/テクノロジー両面） ✓ 使用可
- **Seasons** (2) - 季節
- **Motor Cycle** (1) - モーターサイクル
- **Keyboard** (1) - キーボード

### 6. News/Culture (ニュース・文化)

#### 主要タグ
- **Current Affairs** (37) - 時事ネタ（第2位頻出）
- **Weekly Buzz** (10) - 定期連載
- **Books** (3) - 書籍（複数形）
- **Korea** (1) - 韓国

#### サブカテゴリー
- **Old Media** (2) - 旧メディア ✓ 使用可

#### 固有名詞（組織）
- **IBM** (3) ✓ 使用可

### 7. Location (地域)

- **Chiba** (2) - 千葉県 ✓ 使用可

### 8. Tools & Productivity (ツール・生産性)

#### 主要タグ
- **Productivity** (2) - 生産性（不可算名詞）
- **Note-taking** (2) - ノートテイキング（ハイフン付き）

### 9. Accessibility (アクセシビリティ)

- **Accessibility** (1) - アクセシビリティ（不可算名詞）

## タグ命名規則（CLAUDE.mdベース + 追加ルール）

### 複数形ルール
| カテゴリー | 形式 | 使用状況 | 備考 |
|-----------|------|----------|------|
| Books | 複数形（確立） | ✓ Books (3) | |
| Movies | 複数形（確立） | ✓ Movies (12) | 必ずEntertainmentも付ける |
| Guitar Pedals | 複数形（確立） | ✓ Guitar Pedals (11) | "Pedals"単体は廃止 |
| Manga | 単数形 | ✓ Manga (1) | |
| Music | 単数形/不可算 | ✓ Music (34) | |
| Guitar | 単数形 | ✓ Guitar (37) | ブランド名タグは廃止 |
| Travel | 単数形 | ✓ Travel (8) | |
| Certification | 単数形 | ✓ Certification (5) | |
| Photography | 単数形/活動 | ✓ Photography (14) | "Photo"は廃止 |
| Security | 単数形 | ✓ Security (11) | |
| Design | 単数形 | ✓ Design (3) | |
| Korea | 国名 | ✓ Korea (1) | |
| Accessibility | 不可算 | ✓ Accessibility (1) | |
| Seasons | 複数形 | ✓ Seasons (2) | |
| Productivity | 不可算 | ✓ Productivity (2) | |
| Note-taking | ハイフン | ✓ Note-taking (2) | |
| Game | 単数形 | ✓ Game (15) | |

### 廃止されたタグ

| タグ | 理由 | 代替 |
|------|------|------|
| Pedals | Guitar Pedalsに統一 | Guitar Pedals |
| Photo | Photographyに統一 | Photography |
| Epiphone, Texan, Revstar, Stratocaster | ギターブランド/モデル名は廃止 | Music, Guitar |
| Beatles | アーティスト名は廃止 | 削除（親タグで対応） |
| NOSTR | プロトコル名は廃止 | 削除（親タグで対応） |
| Claude | 製品名（Claude Codeと重複） | Claude Code（または削除） |
| NHK | 組織名（個別性不要） | 削除（親タグで対応） |
| SNS | Techに統合 | Tech |
| Progmraming | タイポ | Programming |
| Music Procution | タイポ | Music Production |

## タグ階層構造

```
Entertainment
├── Movies (⚠️ 必ずEntertainmentも付ける)
│   └── Anime (一部重複)
├── Game
│   └── Splatoon (固有名詞) ✓
└── Manga

Technology (Tech)
├── Generative AI
│   └── Claude Code ✓
├── Cloud
│   ├── AWS
│   └── Google Cloud
├── Security
├── Software
├── Web
│   └── Weblog
└── CLI

Music
├── Music Production
├── Guitar
│   └── Guitar Pedals
└── ❌ ブランド/モデル名タグは廃止

Creative
├── Photography (⚠️ Photoは廃止)
│   └── Photo Friday ✓
├── Design
│   └── Font
└── Art

Lifestyle
├── Travel
│   └── Chiba ✓
├── Career
│   └── Certification
├── Gourmet
├── Gadget
│   └── Drone ✓
└── Seasons

News & Culture
├── Current Affairs
│   ├── Weekly Buzz
│   └── Old Media ✓
├── Books
├── Korea
└── IBM ✓

Productivity
├── Note-taking
└── Task Management
```

## タグ付けの実践原則

### 1. 親子関係の一貫性
✓ **良い例**:
- Splatoon → 100% Gameタグと併用
- Movies → 100% Entertainmentタグと併用（新ルール）

### 2. 固有名詞タグの制限
- 使用可能: Claude Code, Splatoon, IBM, Old Media, Chiba, Drone, Photo Friday
- 使用禁止: ギターブランド/モデル名、アーティスト名、プロトコル名、個別組織名（NHK等）

### 3. 詳細度のレベル
- 一般カテゴリー（Tech, Music）
- サブカテゴリー（Generative AI, Guitar Pedals）
- 固有名詞（Claude Code, Splatoon） - 制限的に使用
- 通常は2-3レベルの組み合わせ

### 4. タグ数の目安
- 平均: 2-3タグ/記事
- 最小: 1タグ
- 最大: 5タグ程度

## 修正が必要なパターン

### 即座に修正すべきもの
1. タイポ（Progmraming, Music Procution）
2. Movies単体（Entertainmentを追加）
3. "Pedals" → "Guitar Pedals"
4. "Photo" → "Photography"
5. ギターブランド/モデル名タグの削除
6. 廃止固有名詞タグの削除（Beatles, NOSTR, Claude, NHK, SNS）

### タグ付けの判断基準

**ギター関連記事の判断**:
- エフェクターのレビュー/解説 → `["Guitar Pedals"]`
- エフェクターを使ったギター → `["Guitar", "Guitar Pedals"]`
- ギターで曲を弾く → `["Music", "Guitar"]`

**Movies関連記事の判断**:
- 映画のレビュー → `["Movies", "Entertainment"]`
- 映画主題歌の演奏 → `["Music", "Guitar"]` または `["Music", "Guitar", "Movies", "Entertainment"]`
- アニメ映画 → `["Anime", "Movies", "Entertainment"]`

**固有名詞タグの判断**:
- 頻出かつ検索価値が高い → 使用可（Claude Code, Splatoon等）
- 単発または親タグで十分 → 廃止（Beatles, NHK等）
- ブランド/モデル名 → 全面廃止

## CLAUDE.md への追加推奨事項

以下のタグをCLAUDE.mdのタグ命名規則に追加することを推奨：

| タグ | 形式 | 参考 |
|------|------|------|
| Game | 単数形 | ゲーム総合 |
| Generative AI | 複合語 | 生成AI（Techのサブカテゴリー） |
| Current Affairs | 複合語 | 時事ネタ |
| Drone | 単数形 | ドローン（固有名詞ではなくカテゴリー） |
| Software | 単数形 | ソフトウェア（Techのサブカテゴリー） |
| Entertainment | 単数形 | 娯楽総合（Movies/Animeの親カテゴリー） |
| Guitar Pedals | 複数形 | エフェクターペダル（"Pedals"単体は不可） |
| CLI | 頭字語 | コマンドライン（Techのサブカテゴリー） |
| Weblog | 単数形 | ブログ運営 |
| Gadget | 単数形 | ガジェット |

## 補足: 固有名詞タグ使用ガイドライン

### 使用可能な固有名詞タグの条件
1. **頻出性**: 5記事以上で使用されている
2. **検索価値**: そのタグで絞り込む需要がある
3. **カテゴリー性**: 単なる固有名詞ではなくカテゴリーとして機能する

### 具体例
- ✓ **Claude Code** (5記事): ツール固有の情報、十分な記事数
- ✓ **Splatoon** (12記事): ゲーム固有のコンテンツ、多数の記事
- ✓ **IBM** (3記事): 企業分析記事で有用
- ✗ **Beatles** (1記事): 記事数少、Musicで十分
- ✗ **NHK** (2記事): 記事数少、Current Affairsで十分
- ✗ **Epiphone** (3記事): ギターブランドは方針として廃止
