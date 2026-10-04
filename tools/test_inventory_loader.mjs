/* Record successful loads, including cases imported by other case modules. */
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
export async function load(url, context, nextLoad) {
  const result = await nextLoad(url, context);
  if (url.startsWith('file:') && /\/tests\/cases\/[^/]+\.cases\.js(?:\?|$)/.test(url)) {
    const path = fileURLToPath(new URL(url));
    fs.appendFileSync(process.env.TEST_INVENTORY_MODULE_LOG,
      path.slice(process.cwd().length + 1) + '\n');
  }
  return result;
}
