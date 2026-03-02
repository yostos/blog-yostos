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
  DEFAULT_AUTHOR,
  BLOG_NAME,
} from './ogp-template.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..');
const CONTENT_DIR = path.join(PROJECT_ROOT, 'content', 'blog');
const DEFAULT_BG_IMAGE = path.join(
  PROJECT_ROOT,
  'static',
  'images',
  'coded-chords.webp'
);
const FONTS_DIR = path.join(__dirname, 'fonts');

const IMAGE_EXTENSIONS = ['.webp', '.jpg', '.jpeg', '.png'];
const FONT_EXTENSIONS = ['.ttf', '.otf'];
const MIN_WIDTH = 1200;
const MIN_HEIGHT = 630;

// コマンドライン引数
const isDryRun = process.argv.includes('--dry-run');
const isForce = process.argv.includes('--force');

/**
 * フォントディレクトリからフォントファイル一覧を取得
 * Berkeley Mono（ラテン文字用）を優先、Kadoma（日本語用）をフォールバックとする
 */
async function findFontFiles() {
  const files = await fs.readdir(FONTS_DIR);
  const fontFiles = files
    .filter((f) => FONT_EXTENSIONS.includes(path.extname(f).toLowerCase()))
    .sort((a, b) => {
      // Berkeley Mono を先頭にソート（ラテン文字・スペース優先）
      const aIsBerkeley = a.toLowerCase().includes('berkeley') ? 0 : 1;
      const bIsBerkeley = b.toLowerCase().includes('berkeley') ? 0 : 1;
      return aIsBerkeley - bIsBerkeley;
    });
  if (fontFiles.length === 0) {
    throw new Error(
      `フォントが見つかりません。scripts/fonts/ に .ttf または .otf を配置してください。`
    );
  }
  return fontFiles.map((f) => path.join(FONTS_DIR, f));
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
 * Zolaのfrontmatter (TOML) から title を正規表現で抽出
 */
async function getArticleTitle(articleDir) {
  const indexPath = path.join(articleDir, 'index.md');
  const content = await fs.readFile(indexPath, 'utf-8');

  // +++で囲まれたfrontmatter部分を抽出
  const fmMatch = content.match(/^\+\+\+\n([\s\S]*?)\n\+\+\+/);
  if (!fmMatch) {
    return 'Untitled';
  }

  const frontmatter = fmMatch[1];

  // title = """...""" (複数行) を抽出
  const multiLineMatch = frontmatter.match(/^title\s*=\s*"""([\s\S]*?)"""/m);
  if (multiLineMatch) {
    return multiLineMatch[1].trim();
  }

  // title = "..." を抽出（エスケープされた引用符に対応）
  const doubleQuoteMatch = frontmatter.match(/^title\s*=\s*"((?:[^"\\]|\\.)*)"/m);
  if (doubleQuoteMatch) {
    // エスケープされた引用符を戻す
    return doubleQuoteMatch[1].replace(/\\"/g, '"');
  }

  // title = '...' を抽出
  const singleQuoteMatch = frontmatter.match(/^title\s*=\s*'([^']*)'/m);
  if (singleQuoteMatch) {
    return singleQuoteMatch[1];
  }

  return 'Untitled';
}

/**
 * ディレクトリ内の画像ファイルを取得（ogp.webpを除く）
 */
async function getImageFiles(articleDir) {
  const files = await fs.readdir(articleDir);
  return files
    .filter((f) => {
      const ext = path.extname(f).toLowerCase();
      const name = path.basename(f, ext).toLowerCase();
      return IMAGE_EXTENSIONS.includes(ext) && name !== 'ogp';
    })
    .map((f) => path.join(articleDir, f));
}

/**
 * 最大ファイルサイズの画像を取得
 */
async function getLargestImage(imagePaths) {
  if (imagePaths.length === 0) return null;

  let largest = null;
  let largestSize = 0;

  for (const imgPath of imagePaths) {
    const stats = await fs.stat(imgPath);
    if (stats.size > largestSize) {
      largestSize = stats.size;
      largest = imgPath;
    }
  }

  return largest;
}

/**
 * 画像がOGPサイズ要件を満たすか確認
 */
async function meetsMinSize(imagePath) {
  try {
    const metadata = await sharp(imagePath).metadata();
    return metadata.width >= MIN_WIDTH && metadata.height >= MIN_HEIGHT;
  } catch {
    return false;
  }
}

/**
 * 画像をリサイズしてタイトルオーバーレイ付きOGP画像を生成
 * @param {string} imagePath - 元画像パス
 * @param {string} outputPath - 出力パス
 * @param {string} title - 記事タイトル
 * @param {Buffer[]} fontsData - フォントデータ配列（優先順）
 */
async function createOgpFromImage(imagePath, outputPath, title, fontsData) {
  // satoriでオーバーレイSVGを生成
  const template = createOverlayTemplate({
    title,
    author: DEFAULT_AUTHOR,
    blogName: BLOG_NAME,
  });

  const svg = await satori(template, {
    width: OGP_WIDTH,
    height: OGP_HEIGHT,
    fonts: [
      { name: 'Latin', data: fontsData[0], weight: 400, style: 'normal' },
      { name: 'JP', data: fontsData[1] || fontsData[0], weight: 400, style: 'normal' },
    ],
  });

  // SVGをPNGに変換
  const resvg = new Resvg(svg, {
    fitTo: {
      mode: 'width',
      value: OGP_WIDTH,
    },
  });
  const overlayPng = resvg.render().asPng();

  // 元画像にオーバーレイを合成
  await sharp(imagePath)
    .resize(OGP_WIDTH, OGP_HEIGHT, {
      fit: 'cover',
      position: 'center',
    })
    .composite([
      {
        input: overlayPng,
        top: 0,
        left: 0,
      },
    ])
    .webp({ quality: 85 })
    .toFile(outputPath);
}

/**
 * デフォルト背景にタイトルをオーバーレイしてOGP画像を生成
 * @param {string} title - 記事タイトル
 * @param {string} outputPath - 出力パス
 * @param {Buffer[]} fontsData - フォントデータ配列（優先順）
 */
async function createOgpWithOverlay(title, outputPath, fontsData) {
  // satoriでSVGを生成
  const template = createOverlayTemplate({
    title,
    author: DEFAULT_AUTHOR,
    blogName: BLOG_NAME,
  });

  const svg = await satori(template, {
    width: OGP_WIDTH,
    height: OGP_HEIGHT,
    fonts: [
      { name: 'Latin', data: fontsData[0], weight: 400, style: 'normal' },
      { name: 'JP', data: fontsData[1] || fontsData[0], weight: 400, style: 'normal' },
    ],
  });

  // SVGをPNGに変換
  const resvg = new Resvg(svg, {
    fitTo: {
      mode: 'width',
      value: OGP_WIDTH,
    },
  });
  const overlayPng = resvg.render().asPng();

  // デフォルト背景画像にオーバーレイを合成
  await sharp(DEFAULT_BG_IMAGE)
    .resize(OGP_WIDTH, OGP_HEIGHT, { fit: 'cover' })
    .composite([
      {
        input: overlayPng,
        top: 0,
        left: 0,
      },
    ])
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

  // フォントを事前に読み込み（メモリ効率化）
  let fontsData = [];
  if (!isDryRun) {
    const fontPaths = await findFontFiles();
    for (const fontPath of fontPaths) {
      console.log(`フォントを読み込み中: ${path.basename(fontPath)}`);
      fontsData.push(await fs.readFile(fontPath));
    }
  }

  const articleDirs = await getArticleDirs();
  console.log(`記事数: ${articleDirs.length}`);
  console.log('');

  let skipped = 0;
  let fromImage = 0;
  let fromDefault = 0;
  let errors = 0;

  for (const articleDir of articleDirs) {
    const relativePath = path.relative(CONTENT_DIR, articleDir);
    const ogpPath = path.join(articleDir, 'ogp.webp');

    // 既存チェック
    try {
      await fs.access(ogpPath);
      if (!isForce) {
        console.log(`[スキップ] ${relativePath} (既存)`);
        skipped++;
        continue;
      }
    } catch {
      // ファイルが存在しない場合は続行
    }

    try {
      const title = await getArticleTitle(articleDir);
      const images = await getImageFiles(articleDir);
      const largestImage = await getLargestImage(images);

      let useDefault = true;
      if (largestImage) {
        const meetsSize = await meetsMinSize(largestImage);
        if (meetsSize) {
          useDefault = false;
        }
      }

      if (useDefault) {
        console.log(`[デフォルト] ${relativePath} → "${title}"`);
        if (!isDryRun) {
          await createOgpWithOverlay(title, ogpPath, fontsData);
        }
        fromDefault++;
      } else {
        const imgName = path.basename(largestImage);
        console.log(`[画像使用] ${relativePath} → ${imgName} + "${title}"`);
        if (!isDryRun) {
          await createOgpFromImage(largestImage, ogpPath, title, fontsData);
        }
        fromImage++;
      }
    } catch (err) {
      console.error(`[エラー] ${relativePath}: ${err.message}`);
      errors++;
    }
  }

  console.log('');
  console.log('---');
  console.log(`完了: スキップ=${skipped}, 画像使用=${fromImage}, ` +
    `デフォルト=${fromDefault}, エラー=${errors}`);
}

main().catch((err) => {
  console.error('致命的なエラー:', err);
  process.exit(1);
});
