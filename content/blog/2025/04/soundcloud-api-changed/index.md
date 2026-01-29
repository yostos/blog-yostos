+++
title = "SoundCloud API仕様の変更"
description = "直近数日の内にSoundCloudはAPIの仕様を変更したようです。自作のTypeScriptコンポーネントがうまく機能しなくなったために対応しました。"
date = 2025-04-28
aliases = ["/articles/2025/04/28/soundcloud-api-changed"]

[taxonomies]
tags = ["Tech","API"]
+++

直近数日の内にSoundCloudはAPIの仕様を変更したようです。自作のTypeScriptコンポーネントがうまく機能しなくなったために対応しました。

## 変更のポイント

以下のコードは以前使用していたもので SoundCloud の曲を Web に埋め込むためのコー
ドです。

```javascript
export const SoundCloudEmbed: React.FC<SoundCloudEmbedProps> = ({ url }) => {
  // SoundCloud の埋め込み URL 形式に変換
  const embedUrl = `https://w.soundcloud.com/player/?url=${encodeURIComponent(url)}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true`;

  return (
    <div className="w-full">
      <iframe
        width="100%"
        height="166"
        scrolling="no"
        frameBorder="no"
        allow="autoplay"
        src={embedUrl}
      ></iframe>

      <div className="text-[10px] text-gray-400 overflow-hidden whitespace-nowrap text-ellipsis font-light">
        <a
          href="https://soundcloud.com/yostos"
          title="Yostos"
          target="_blank"
          rel="noopener noreferrer"
          className="text-gray-400 no-underline"
        >
          Yostos
        </a>
        &nbsp;·&nbsp;
        <a
          href={url}
          title="Yostos"
          target="_blank"
          rel="noopener noreferrer"
          className="text-gray-400 no-underline"
        >
          Blackbird
        </a>
      </div>
    </div>
  );
};
```

以前は iframe の src に指定する url は曲ページへのリンクと同じリンクを指定すればよかった
のですが、ここ数日の変更で iframe の src の指定は API 専用の URL でなければならなく
なったようです。

この変更は既にアップロードされている曲には遡及していないようで、直近にアップ
ロードした曲のみに影響しています。

## SoundCloudEmbed コンポーネントの変更

本来は SoundCloud で Javascript のコードを取得すべきです。
このブログでは MDX を使っている関係で取得したコードでは修正が必要なため、
`SoundCloudEmbed`というコンポーネントを作っていました。
この変更で Share Link のみ指定していた SoundCloudEmbed は動かなくなりました。

仕方がないので API 用の URL を指定できようように修正しました。またタイトルの固定
でなく曲名を指定できるよう変更しています。

```typescript

type SoundCloudEmbedProps = {
  url: string;
  apiurl?: string; // Optional API URL
  title?: string;  // Optional title
};

export const SoundCloudEmbed: React.FC<SoundCloudEmbedProps> = ({
  url,
  apiurl,
  title
}) => {
  // SoundCloud の埋め込み URL 形式に変換
  // If apiurl is provided, use it for the iframe source, otherwise use the url
  const sourceUrl = apiurl || url;
  const embedUrl = `https://w.soundcloud.com/player/?url=${encodeURIComponent(sourceUrl)}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true`;

  // Prepare the display title
  const displayTitle = title ? `Yostos - ${title}` : "Yostos";

  return (
    <div className="w-full">
      <iframe
        width="100%"
        height="166"
        scrolling="no"
        frameBorder="no"
        allow="autoplay"
        src={embedUrl}
      ></iframe>

      <div className="text-[10px] text-gray-400 overflow-hidden whitespace-nowrap text-ellipsis font-light">
        <a
          href={url}
          title={displayTitle}
          target="_blank"
          rel="noopener noreferrer"
          className="text-gray-400 no-underline"
        >
          {displayTitle}
        </a>
      </div>
    </div>
  );
};
```

API 用 URL だけ取得はできないので、結局埋め込み用の Javascript のコードを SoundCloud から取得して URL を取り出して貼り付けることになります。
手間は貼り付けるより面倒なので、コンポーネントにした意味がないかもしれません。
