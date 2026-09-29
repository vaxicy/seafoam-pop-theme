# Asset notes

Two English screenshots at 1280x800 (browser view + palette card); promos at 440x280 and 1400x560. HTML illustrations rendered with headless Chromium, not actual Chrome UI screenshots.

Layout, proportions and every browser-owned colour come from a real Chrome screenshot with this theme installed (1080x645, scaled to 1280x800): Google new-tab wordmark `#665BFF`, toolbar icons `#5B7C77` (the theme's own tint), Customize Chrome pill text `#202124`, omnibox placeholder `#70757A`, Lens icon `#4285F4`. That real screenshot has no bookmarks bar, so the mock-up has none either, and the active tab takes the toolbar colour while inactive tabs take the mint tab colour.

Icon drawn with code (PIL, `scripts/generate-logo.py`) from the manifest palette: an outlined soap bubble with a shine arc on a deep teal rounded tile, 128x128, one flat colour set.

Every asset is regenerated from `manifest.json` — change a colour there and re-run the scripts to keep the theme, the icon, the promo and the screenshots in sync.
