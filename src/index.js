const FONTS_PREFIX = "/fonts/";

export default {
  async fetch(req, env) {
    const url = new URL(req.url);

    if (url.pathname.startsWith(FONTS_PREFIX)) {
      const key = decodeURIComponent(url.pathname.slice(FONTS_PREFIX.length));
      // Only flat keys in R2 (no subdir, no traversal). Anything else falls
      // through to static assets — the theme also publishes under /fonts/.
      if (key && !key.includes("..") && !key.includes("/")) {
        const obj = await env.FONTS.get(key);
        if (obj) {
          const headers = new Headers();
          obj.writeHttpMetadata(headers);
          headers.set("Content-Type", "font/woff2");
          headers.set("Cache-Control", "public, max-age=31536000, immutable");
          headers.set("ETag", obj.httpEtag);
          return new Response(obj.body, { headers });
        }
      }
    }

    return env.ASSETS.fetch(req);
  },
};
