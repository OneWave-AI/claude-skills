# Visual Check

Render the build at the source image's viewport and compare. This loop is what turns "roughly similar" into "matches".

## Capture the render

If a browser tool is available (for example a Chrome or Playwright MCP), open the page, resize to the source width, and screenshot.

Otherwise, with Playwright installed (`npm i -D playwright && npx playwright install chromium`):

```js
// shot.mjs - usage: node shot.mjs http://localhost:5173 1440 out.png
import { chromium } from "playwright";

const [url, width = "1440", out = "render.png"] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: Number(width), height: 900 } });
await page.goto(url, { waitUntil: "networkidle" });
await page.screenshot({ path: out, fullPage: true });
await browser.close();
```

For a single HTML file, `file:///absolute/path/index.html` works as the URL.

Match the source's device scale: for a 2x screenshot, pass `deviceScaleFactor: 2` in `newPage` and use the halved width.

## Compare

Look at the source image and the render together and list differences in this order:

1. **Structure** - missing or extra elements, wrong column count, wrong order
2. **Alignment and layout** - centered vs left-aligned, max width, element widths
3. **Spacing** - padding, gaps, section spacing (most common drift)
4. **Typography** - size, weight, line height, letter spacing
5. **Color** - backgrounds, text, borders
6. **Details** - radius, shadows, icon size

Fix the top category before moving on; spacing fixes are wasted if the layout is wrong.

## Check responsiveness

Capture again at 390px (phone) and 768px (tablet). Check that nothing overflows horizontally (`document.documentElement.scrollWidth <= innerWidth`), text stays readable, and tap targets are at least 44px tall.

## Stop condition

Stop when the remaining differences are font rendering, anti-aliasing, or content the image did not show. Report what still differs and why.
