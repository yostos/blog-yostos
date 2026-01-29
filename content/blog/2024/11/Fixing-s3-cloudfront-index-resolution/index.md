+++
title = "S3静的ウェブサイトのインデックス解決をCloudFront Functionsで修正"
description = "CloudFlareからブログを移行した際に、パスの指定で問題がでていたので修正しました。"
date = 2024-11-05
aliases = ["/articles/2024/11/05/Fixing-s3-cloudfront-index-resolution"]

[taxonomies]
tags = ["Tech", "AWS","Weblog"]
+++

メインブログを Cloudflare から AWS S3 へと移行した際、
S3 の Block pubic access をオフ、Static website hosting をオンにしていたので、
CloudFront が S3 の REST API エンドポイントを使用するよう修正しました。

この場合 CloudFront はサブディレクトリの index.html ファイルを自動的に解決できないので、以下の URL のパスを適切に変換する CloudFront Functions を追加しました。

ありがちな事ですね。

```javascript
function handler(event) {
  var request = event.request;
  var uri = request.uri;

  // URIが/で終わる場合、index.htmlを追加
  if (uri.endsWith("/")) {
    request.uri += "index.html";
  }
  // 拡張子がない場合もindex.htmlを追加
  else if (!uri.includes(".")) {
    request.uri += "/index.html";
  }

  return request;
}
```
