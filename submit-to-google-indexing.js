#!/usr/bin/env node
/**
 * Submit all agentcollect.com sitemap URLs to Google Indexing API.
 * Usage: node submit-to-google-indexing.js
 */

const fs = require('fs');
const path = require('path');
const { GoogleAuth } = require('google-auth-library');

const SITEMAP_PATH = path.join(__dirname, 'sitemap.xml');
const CREDENTIALS_PATH = path.join('/Users/jonathanbanner/Downloads', 'chrome-courage-490502-g0-c1f14db004a4.json');
const INDEXING_ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish';
const SCOPES = ['https://www.googleapis.com/auth/indexing'];

// Rate limit: 200ms between requests to stay well within quotas
const DELAY_MS = 200;

function extractUrls(sitemapXml) {
  const urls = [];
  const regex = /<loc>(.*?)<\/loc>/g;
  let match;
  while ((match = regex.exec(sitemapXml)) !== null) {
    urls.push(match[1]);
  }
  return urls;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  // Read sitemap
  const sitemapContent = fs.readFileSync(SITEMAP_PATH, 'utf8');
  const urls = extractUrls(sitemapContent);
  console.log(`Found ${urls.length} URLs in sitemap\n`);

  if (urls.length > 200) {
    console.warn(`WARNING: ${urls.length} URLs exceeds Google's 200/day quota. Only first 200 will be submitted.\n`);
  }

  // Authenticate with service account
  const auth = new GoogleAuth({
    keyFile: CREDENTIALS_PATH,
    scopes: SCOPES,
  });
  const client = await auth.getClient();

  let success = 0;
  let failed = 0;
  const errors = [];
  const urlsToSubmit = urls.slice(0, 200);

  for (let i = 0; i < urlsToSubmit.length; i++) {
    const url = urlsToSubmit[i];
    try {
      const response = await client.request({
        url: INDEXING_ENDPOINT,
        method: 'POST',
        data: {
          url: url,
          type: 'URL_UPDATED',
        },
      });

      success++;
      const notifyTime = response.data?.urlNotificationMetadata?.latestUpdate?.notifyTime || 'N/A';
      console.log(`[${i + 1}/${urlsToSubmit.length}] OK  ${url}  (notifyTime: ${notifyTime})`);
    } catch (err) {
      failed++;
      const status = err.response?.status || 'unknown';
      const message = err.response?.data?.error?.message || err.message;
      errors.push({ url, status, message });
      console.error(`[${i + 1}/${urlsToSubmit.length}] FAIL ${url}  (${status}: ${message})`);

      // If we hit quota limit, stop
      if (status === 429) {
        console.error('\nQuota exceeded (429). Stopping.');
        break;
      }
    }

    // Rate limit
    if (i < urlsToSubmit.length - 1) {
      await sleep(DELAY_MS);
    }
  }

  // Summary
  console.log('\n========== SUMMARY ==========');
  console.log(`Total URLs in sitemap: ${urls.length}`);
  console.log(`Submitted: ${success + failed}`);
  console.log(`Success: ${success}`);
  console.log(`Failed: ${failed}`);

  if (errors.length > 0) {
    console.log('\nFailed URLs:');
    errors.forEach(e => console.log(`  ${e.url} — ${e.status}: ${e.message}`));
  }

  if (urls.length > 200) {
    console.log(`\nSkipped ${urls.length - 200} URLs (over 200/day quota). Re-run tomorrow for the rest.`);
  }
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
