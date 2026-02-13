#!/usr/bin/env node
/**
 * リンクカード用 GitHub リポジトリ情報取得スクリプト
 *
 * 使用方法:
 *   npm run linkcard           # メタデータを取得・更新
 *   npm run linkcard:dry-run   # 取得対象を確認（実行しない）
 *   npm run linkcard -- --force  # 全件再取得
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { glob } from 'glob';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..');
const CONTENT_DIR = path.join(PROJECT_ROOT, 'content', 'blog');
const DATA_FILE = path.join(PROJECT_ROOT, 'data', 'linkcard.json');

const SHORTCODE_PATTERN =
  /\{\{\s*linkcard\(url="([^"]+)"\)\s*\}\}/g;

const FETCH_TIMEOUT = 10000;
const USER_AGENT =
  'Mozilla/5.0 (compatible; LinkCardBot/1.0)';

// コマンドライン引数
const isDryRun = process.argv.includes('--dry-run');
const isForce = process.argv.includes('--force');

/**
 * 既存の linkcard.json を読み込む
 */
async function loadExistingData() {
  try {
    const content = await fs.readFile(DATA_FILE, 'utf-8');
    return JSON.parse(content);
  } catch {
    return {};
  }
}

/**
 * 記事ファイルからショートコードの GitHub URL を抽出
 */
async function extractGitHubUrls() {
  const indexFiles = await glob('**/index.md', {
    cwd: CONTENT_DIR,
  });
  const urls = new Set();

  for (const file of indexFiles) {
    const filePath = path.join(CONTENT_DIR, file);
    const content = await fs.readFile(filePath, 'utf-8');
    let match;
    while ((match = SHORTCODE_PATTERN.exec(content))) {
      const gh = parseGitHubRepo(match[1]);
      if (gh) urls.add(match[1]);
    }
    SHORTCODE_PATTERN.lastIndex = 0;
  }

  return [...urls];
}

/**
 * GitHub リポジトリURLかどうか判定し、owner/repo を返す
 */
function parseGitHubRepo(url) {
  const match = url.match(
    /^https?:\/\/github\.com\/([^/]+)\/([^/]+)\/?$/
  );
  if (!match) return null;
  return { owner: match[1], repo: match[2] };
}

/**
 * GitHub API からリポジトリ情報を取得
 */
async function fetchGitHubData(owner, repo) {
  const apiUrl =
    `https://api.github.com/repos/${owner}/${repo}`;
  const response = await fetch(apiUrl, {
    headers: {
      'User-Agent': USER_AGENT,
      Accept: 'application/vnd.github.v3+json',
    },
    signal: AbortSignal.timeout(FETCH_TIMEOUT),
  });

  if (!response.ok) {
    throw new Error(`GitHub API ${response.status}`);
  }

  const data = await response.json();
  return {
    type: 'github',
    owner: data.owner.login,
    repo: data.name,
    description: data.description || null,
    language: data.language || null,
    fetched_at: new Date().toISOString(),
  };
}

/**
 * メイン処理
 */
async function main() {
  console.log('リンクカード GitHub リポジトリ情報取得');
  console.log(
    `モード: ${isDryRun ? 'dry-run（確認のみ）' : '取得'}`
  );
  console.log(`強制再取得: ${isForce ? 'はい' : 'いいえ'}`);
  console.log('---');

  const existingData = await loadExistingData();
  const urls = await extractGitHubUrls();

  console.log(`GitHub URL数: ${urls.length}`);
  console.log('');

  let skipped = 0;
  let fetched = 0;
  let errors = 0;

  for (const url of urls) {
    if (!isForce && existingData[url]) {
      console.log(`[スキップ] ${url} (既存)`);
      skipped++;
      continue;
    }

    const gh = parseGitHubRepo(url);

    if (isDryRun) {
      console.log(
        `[取得予定] ${gh.owner}/${gh.repo}`
      );
      fetched++;
      continue;
    }

    try {
      console.log(
        `[取得中] ${gh.owner}/${gh.repo}`
      );
      const data = await fetchGitHubData(
        gh.owner, gh.repo
      );
      existingData[url] = data;
      console.log(`  → ${data.description || '(説明なし)'}`);
      fetched++;
    } catch (err) {
      console.error(
        `[エラー] ${gh.owner}/${gh.repo}: ${err.message}`
      );
      errors++;
    }
  }

  if (!isDryRun && fetched > 0) {
    await fs.writeFile(
      DATA_FILE,
      JSON.stringify(existingData, null, 2) + '\n',
      'utf-8'
    );
    console.log('');
    console.log(`${DATA_FILE} を更新しました。`);
  }

  console.log('');
  console.log('---');
  console.log(
    `完了: スキップ=${skipped}, ` +
      `取得=${fetched}, エラー=${errors}`
  );
}

main().catch((err) => {
  console.error('致命的なエラー:', err);
  process.exit(1);
});
