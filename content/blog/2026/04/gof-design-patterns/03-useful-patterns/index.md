+++
title = "GoFデザインパターンは現代でも有用か(3) — 言語に吸収されたパターンと非推奨のSingleton"
description = """GoFの残り13パターンのうち、Iteratorは言語機能として吸収され、\
Singletonは現代の設計手法により非推奨となりました。\
それぞれの経緯をGo言語のコードとともに検討します。"""
date = 2026-04-02T10:15+09:00

[taxonomies]
tags = ["Tech", "Software", "Go"]

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

## 前回までの振り返り

[第1回](@/blog/2026/04/gof-design-patterns/01-paradigm-shift/index.md)では、手続き型プログラミングからOOPへのパラダイムシフト、その中でGoFデザインパターンが「OOPでよいコードを書くためのお手本」として体系化された経緯を振り返りました。そして現代では、OOPの中核 — クラス継承、型階層、参照セマンティクス — を意図的に排除したGo言語が登場し、新たなパラダイムシフトが起きていることを確認しました。

[第2回](@/blog/2026/04/gof-design-patterns/02-unnecessary-patterns/index.md)では、Go言語の3つの設計方針がGoFの23パターンのうち10パターンを不要にしたことを検証しました。

<!-- textlint-disable -->

| Go言語の設計方針                                                                          | 不要になったパターン                                      |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| クラス継承を排除し、合成と暗黙的インターフェースで代替                                    | Template Method, Factory Method, Abstract Factory, Bridge |
| 参照セマンティクスではなく値セマンティクスをデフォルトに                                  | Prototype, Memento                                        |
| 振る舞いもオブジェクトに包む制約を廃し、第一級関数とチャネル/ゴルーチンで直接扱えるように | Strategy, Command, Visitor, Observer                      |

<!-- textlint-enable -->

これらはOOPの制約の中で生まれた処方箋であり、制約そのものを取り除いたGo言語では必要なくなったものでした。では、残る13パターンはどうでしょうか。本記事では、言語機能として取り込まれたものと、設計手法の進化で非推奨となったものを検討します。

## 言語機能として取り込まれたパターン

デザインパターンの中には、その有用性が広く認められた結果、現代の言語では標準的な機能として取り込まれたものがあります。デザインパターンが語られた当時はOOPがまだ成熟しておらず、これらの機能をユーザーで実装していたとも言えます。これらのパターンは「不要になった」のではなく、「わざわざパターンとして意識する必要がなくなった」と言えます。

Go言語も例外でなく、言語仕様としてこれらのパターンを取り込んでいます。

### コレクションの内部構造を公開せずに要素を走査する

- **Iterator** — イテレータオブジェクトを別途定義し、`hasNext()`/`next()`のようなインターフェースを実装する必要があった

『[Java言語で学ぶデザインパターン入門](https://amzn.to/4bW36Po)第3版』(結城浩著)[^affiliate]のIteratorパターンのサンプルコードを見てみます。本棚（BookShelf）に本（Book）を格納し、イテレータで順に取り出すという例です。

```java,name=Book.java
public class Book {
    private String name;

    public Book(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

```java,name=BookShelf.java
import java.util.Iterator;

public class BookShelf implements Iterable<Book> {
    private Book[] books;
    private int last = 0;

    public BookShelf(int maxsize) {
        this.books = new Book[maxsize];
    }

    public Book getBookAt(int index) {
        return books[index];
    }

    public void appendBook(Book book) {
        this.books[last] = book;
        last++;
    }

    public int getLength() {
        return last;
    }

    @Override
    public Iterator<Book> iterator() {
        return new BookShelfIterator(this);
    }
}
```

```java,name=BookShelfIterator.java
import java.util.Iterator;
import java.util.NoSuchElementException;

public class BookShelfIterator implements Iterator<Book> {
    private BookShelf bookShelf;
    private int index;

    public BookShelfIterator(BookShelf bookShelf) {
        this.bookShelf = bookShelf;
        this.index = 0;
    }

    @Override
    public boolean hasNext() {
        if (index < bookShelf.getLength()) {
            return true;
        } else {
            return false;
        }
    }

    @Override
    public Book next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        Book book = bookShelf.getBookAt(index);
        index++;
        return book;
    }
}
```

```java,name=Main.java
import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        BookShelf bookShelf = new BookShelf(4);
        bookShelf.appendBook(new Book("Around the World in 80 Days"));
        bookShelf.appendBook(new Book("Bible"));
        bookShelf.appendBook(new Book("Cinderella"));
        bookShelf.appendBook(new Book("Daddy-Long-Legs"));

        // 明示的にIteratorを使う方法
        Iterator<Book> it = bookShelf.iterator();
        while (it.hasNext()) {
            Book book = it.next();
            System.out.println(book.getName());
        }
        System.out.println();

        // 拡張for文を使う方法
        for (Book book: bookShelf) {
            System.out.println(book.getName());
        }
        System.out.println();
    }
}
```

<!-- textlint-disable -->

<!-- author-approved: MIT License sample code credit -->

上記Javaコードは結城浩氏によるサンプルコード（[MIT License](https://www.hyuki.com/dp/)、Copyright (c) 2001,2004,2021 結城浩 / Hiroshi Yuki）です。

<!-- textlint-enable -->

4つのファイル、約80行のコードが必要です。`BookShelfIterator`クラスが走査の状態（現在のインデックス）を管理し、`hasNext()`と`next()`のインターフェースを実装しています。`BookShelf`は`Iterable<Book>`を実装し、`iterator()`メソッドでイテレータを生成します。

Go言語で同じBookShelfを書くとどうなるでしょうか。Go 1.23で導入されたrange-over-function（`iter.Seq`）を使うと、Javaと同等のカスタムコレクションを以下のように実装できます。

```go,name=main.go
package main

import (
    "fmt"
    "iter"
)

type Book struct {
    Name string
}

type BookShelf struct {
    books []Book
}

func (s *BookShelf) Append(book Book) {
    s.books = append(s.books, book)
}

func (s *BookShelf) All() iter.Seq[Book] {
    return func(yield func(Book) bool) {
        for _, book := range s.books {
            if !yield(book) {
                return
            }
        }
    }
}

func main() {
    shelf := &BookShelf{}
    shelf.Append(Book{Name: "Around the World in 80 Days"})
    shelf.Append(Book{Name: "Bible"})
    shelf.Append(Book{Name: "Cinderella"})
    shelf.Append(Book{Name: "Daddy-Long-Legs"})

    for book := range shelf.All() {
        fmt.Println(book.Name)
    }
}
```

Javaでは`Iterable`インターフェース、`Iterator`実装クラス、`hasNext()`/`next()`メソッドの3層が必要でした。Go言語では`iter.Seq`型の関数を1つ返すだけで済みます。イテレータの状態管理（インデックスの保持、終端判定）はクロージャが担い、専用のクラスを書く必要がありません。

[^affiliate]: このリンクはAmazonアソシエイトのリンクです。

## 現代の設計手法により非推奨となったパターン

### インスタンスが1つだけであることを保証する

- **Singleton** — クラスのインスタンスが1つだけであることを保証し、グローバルなアクセス手段を提供する

典型的な例として、アプリケーションの設定情報（Config）をSingletonで管理するケースを見てみます。Go言語で実装した例です。

```go
var (
    instance *Config
    once     sync.Once
)

type Config struct {
    DBHost string
    DBPort int
}

func GetConfig() *Config {
    once.Do(func() {
        port, _ := strconv.Atoi(os.Getenv("DB_PORT"))
        instance = &Config{
            DBHost: os.Getenv("DB_HOST"),
            DBPort: port,
        }
    })
    return instance
}

type UserRepository struct{}

func (r *UserRepository) FindByID(id int) (*User, error) {
    // どこからでもGetConfig()でアクセスできる
    config := GetConfig()
    dsn := fmt.Sprintf("%s:%d/mydb", config.DBHost, config.DBPort)
    // ...
}
```

Configのようなオブジェクトは、システムにインスタンスを1つだけ持つのが都合よいものです。そのため、このような実装が広く行われていました。
しかし、テストのシーンを考えると、このパターンは問題があります。
`UserRepository`は`Config`に依存していますが、その依存は関数の引数に現れません。
テスト時に本番と異なる設定を注入することも困難です。

Singletonは、OOPの副作用とは無関係に、現代の多くの設計指針で非推奨とされるパターンです。問題の本質は「インスタンスが1つ」であることではなく、「グローバルなアクセス手段を提供する」という点にあります。`GetConfig()`のようなグローバル関数を通じてどこからでもアクセスできることが、隠れた依存関係を生み、テスト時のモック差し替えを困難にします。

注意すべきは、「ライフサイクルとしてのシングルトン」まで否定しているわけではないことです。DIコンテナがオブジェクトのスコープをシングルトンとして管理すること（SpringのデフォルトスコープやGoのfxにおけるライフサイクル管理など）は、依存関係が明示的である限り問題ありません。非推奨なのは、GoFが定義した「グローバルアクセスを提供するパターンとしてのSingleton」です。

現代では、依存性の注入（Dependency Injection）がこの問題に対するより優れた解法として確立されています。必要な依存を明示的に引数として渡すことで、グローバル状態を排除し、テスト容易性と可読性を確保します。同じ設計をDIで書くと次のようになります。

```go
type Config struct {
    DBHost string
    DBPort int
}

type UserRepository struct {
    config Config
}

func NewUserRepository(config Config) *UserRepository {
    return &UserRepository{config: config}
}

func (r *UserRepository) FindByID(id int) (*User, error) {
    dsn := fmt.Sprintf("%s:%d/mydb", r.config.DBHost, r.config.DBPort)
    // ...
}

func main() {
    config := Config{
        DBHost: os.Getenv("DB_HOST"),
        DBPort: 3306,
    }
    repo := NewUserRepository(config)
    // ...
}
```

`UserRepository`が何に依存しているかが`NewUserRepository`の引数として明示されています。テスト時には異なる`Config`を渡すだけで済みます。

## まとめ

本記事では、GoFの残り13パターンのうち2つを検討しました。

- **Iterator** — 言語機能として吸収され、パターンとして意識する必要がなくなった
- **Singleton** — OOPの副作用とは無関係に、グローバル状態という本質的な問題から非推奨となった。依存性の注入（DI）がより優れた解法として確立されている

次回は、残る11のパターンがなぜ現代でも有用なのかを分析し、シリーズ全体の結論としてデザインパターンの本質的価値を考察します。
