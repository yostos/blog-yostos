#!/usr/bin/env node
/**
 * OGP画像自動生成スクリプト
 *
 * 使用方法:
 *   npm run ogp           # OGP画像を生成
 *   npm run ogp:dry-run   # 生成対象を確認（実際には生成しない）
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { glob } from 'glob';
import sharp from 'sharp';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import {
  createOverlayTemplate,
  OGP_WIDTH,
  OGP_HEIGHT,
} from './ogp-template.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..');
const CONTENT_DIR = path.join(PROJECT_ROOT, 'content', 'blog');
const TEMPLATE_IMAGE = path.join(__dirname, 'images', 'ogp-template.png');
const FONTS_DIR = path.join(__dirname, 'fonts');

const FONT_FILES = {
  latin: 'BerkeleyMono-Medium.otf',
  jp: 'IBMPlexSansJP-Medium.otf',
};

// コマンドライン引数
const isDryRun = process.argv.includes('--dry-run');
const isForce = process.argv.includes('--force');

/**
 * フォントファイルを読み込み
 */
async function loadFonts() {
  const latinPath = path.join(FONTS_DIR, FONT_FILES.latin);
  const jpPath = path.join(FONTS_DIR, FONT_FILES.jp);

  for (const [name, fontPath] of [['Latin', latinPath], ['JP', jpPath]]) {
    try {
      await fs.access(fontPath);
    } catch {
      throw new Error(
        `フォント ${name} が見つかりません: ${fontPath}\nscripts/fonts/ に配置してください。`
      );
    }
  }

  return {
    latin: await fs.readFile(latinPath),
    jp: await fs.readFile(jpPath),
  };
}

/**
 * 記事ディレクトリ一覧を取得
 */
async function getArticleDirs() {
  const indexFiles = await glob('**/index.md', { cwd: CONTENT_DIR });
  return indexFiles.map((f) => path.join(CONTENT_DIR, path.dirname(f)));
}

/**
 * frontmatterからタイトルを取得
 */
function extractTitle(frontmatter) {
  // title = """...""" (複数行)
  const multiLineMatch = frontmatter.match(/^title\s*=\s*"""([\s\S]*?)"""/m);
  if (multiLineMatch) {
    return multiLineMatch[1].trim();
  }

  // title = "..." （エスケープされた引用符に対応）
  const doubleQuoteMatch = frontmatter.match(/^title\s*=\s*"((?:[^"\\]|\\.)*)"/m);
  if (doubleQuoteMatch) {
    return doubleQuoteMatch[1].replace(/\\"/g, '"');
  }

  // title = '...'
  const singleQuoteMatch = frontmatter.match(/^title\s*=\s*'([^']*)'/m);
  if (singleQuoteMatch) {
    return singleQuoteMatch[1];
  }

  return 'Untitled';
}

/**
 * frontmatterからタグを取得
 */
function extractTags(frontmatter) {
  const match = frontmatter.match(/^tags\s*=\s*\[(.*?)\]/m);
  if (!match) return [];

  return match[1]
    .split(',')
    .map((t) => t.trim().replace(/^["']|["']$/g, ''))
    .filter((t) => t.length > 0);
}

/**
 * 記事のfrontmatterを解析してタイトルとタグを取得
 */
async function parseArticle(articleDir) {
  const indexPath = path.join(articleDir, 'index.md');
  const content = await fs.readFile(indexPath, 'utf-8');

  const fmMatch = content.match(/^\+\+\+\n([\s\S]*?)\n\+\+\+/);
  if (!fmMatch) {
    return { title: 'Untitled', tags: [] };
  }

  const frontmatter = fmMatch[1];
  return {
    title: extractTitle(frontmatter),
    tags: extractTags(frontmatter),
  };
}

/**
 * テンプレート画像にオーバーレイを合成してOGP画像を生成
 */
async function createOgpImage(outputPath, title, tags, fonts) {
  const template = createOverlayTemplate({ title, tags });

  const svg = await satori(template, {
    width: OGP_WIDTH,
    height: OGP_HEIGHT,
    fonts: [
      { name: 'Latin', data: fonts.latin, weight: 500, style: 'normal' },
      { name: 'JP', data: fonts.jp, weight: 500, style: 'normal' },
    ],
  });

  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: OGP_WIDTH },
  });
  const overlayPng = resvg.render().asPng();

  await sharp(TEMPLATE_IMAGE)
    .composite([{ input: overlayPng, top: 0, left: 0 }])
    .webp({ quality: 85 })
    .toFile(outputPath);
}

/**
 * メイン処理
 */
async function main() {
  console.log('OGP画像生成スクリプト');
  console.log(`モード: ${isDryRun ? 'dry-run（確認のみ）' : '生成'}`);
  console.log(`強制上書き: ${isForce ? 'はい' : 'いいえ'}`);
  console.log('---');

  let fonts = null;
  if (!isDryRun) {
    fonts = await loadFonts();
    console.log(`フォント読み込み完了: ${FONT_FILES.latin}, ${FONT_FILES.jp}`);
  }

  const articleDirs = await getArticleDirs();
  console.log(`記事数: ${articleDirs.length}`);
  console.log('');

  let skipped = 0;
  let generated = 0;
  let errors = 0;

  for (const articleDir of articleDirs) {
    const relativePath = path.relative(CONTENT_DIR, articleDir);
    const ogpPath = path.join(articleDir, 'ogp.webp');

    // 既存チェック
    try {
      await fs.access(ogpPath);
      if (!isForce) {
        skipped++;
        continue;
      }
    } catch {
      // ファイルが存在しない場合は続行
    }

    try {
      const { title, tags } = await parseArticle(articleDir);
      const tagStr = tags.length > 0 ? ` [${tags.slice(0, 4).join(', ')}]` : '';
      console.log(`[生成] ${relativePath} → "${title}"${tagStr}`);
      if (!isDryRun) {
        await createOgpImage(ogpPath, title, tags, fonts);
      }
      generated++;
    } catch (err) {
      console.error(`[エラー] ${relativePath}: ${err.message}`);
      errors++;
    }
  }

  console.log('');
  console.log('---');
  console.log(`完了: スキップ=${skipped}, 生成=${generated}, エラー=${errors}`);
}

main().catch((err) => {
  console.error('致命的なエラー:', err);
  process.exit(1);
});
