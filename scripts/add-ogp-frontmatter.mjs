#!/usr/bin/env node
/**
 * 各記事のfrontmatterに social_media_card = "ogp.webp" を追加するスクリプト
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { glob } from 'glob';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..');
const CONTENT_DIR = path.join(PROJECT_ROOT, 'content', 'blog');

const isDryRun = process.argv.includes('--dry-run');

async function main() {
  console.log('frontmatterにsocial_media_cardを追加');
  console.log(`モード: ${isDryRun ? 'dry-run（確認のみ）' : '実行'}`);
  console.log('---');

  const indexFiles = await glob('**/index.md', { cwd: CONTENT_DIR });
  console.log(`記事数: ${indexFiles.length}`);
  console.log('');

  let updated = 0;
  let skipped = 0;
  let errors = 0;

  for (const relPath of indexFiles) {
    const filePath = path.join(CONTENT_DIR, relPath);
    const dirPath = path.dirname(relPath);

    try {
      let content = await fs.readFile(filePath, 'utf-8');

      // すでにsocial_media_cardがあるかチェック
      if (content.includes('social_media_card')) {
        console.log(`[スキップ] ${dirPath} (既存)`);
        skipped++;
        continue;
      }

      // [extra]セクションがあるかチェック
      if (content.includes('[extra]')) {
        // [extra]の次の行に追加
        content = content.replace(
          /(\[extra\]\n)/,
          '$1social_media_card = "ogp.webp"\n'
        );
      } else {
        // [extra]セクションがない場合、+++の前に追加
        content = content.replace(
          /(\n\+\+\+\n)/,
          '\n[extra]\nsocial_media_card = "ogp.webp"\n+++\n'
        );
      }

      console.log(`[更新] ${dirPath}`);

      if (!isDryRun) {
        await fs.writeFile(filePath, content, 'utf-8');
      }
      updated++;
    } catch (err) {
      console.error(`[エラー] ${dirPath}: ${err.message}`);
      errors++;
    }
  }

  console.log('');
  console.log('---');
  console.log(`完了: 更新=${updated}, スキップ=${skipped}, エラー=${errors}`);
}

main().catch((err) => {
  console.error('致命的なエラー:', err);
  process.exit(1);
});
