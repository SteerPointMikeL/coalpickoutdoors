# Coal Pick Outdoors — WordPress Build Spec

## Repository setup
This repo (github.com/SteerPointMikeL/coalpickoutdoors) is currently empty. Build everything fresh and commit it directly to the `main` branch (create it if needed). Do not assume any existing WordPress install — this is a portable handoff package (theme + content export + form export) meant to be installed on a fresh or existing WordPress site by an admin later. We have no WP admin/SSH access to any live server, so nothing here can be "deployed" — only committed to the repo as files, well organized and documented.

## Source design
A single static HTML mockup (`Coal-Pick-Outdoors-Static-Theme.zip`, already extracted to `/home/user/workspace/static_site/`) defines the design and copy. Its files:
- `/home/user/workspace/static_site/index.html` — full markup/copy for one long-scrolling home page
- `/home/user/workspace/static_site/assets/style.css` — all design CSS (colors, type, layout)
- `/home/user/workspace/static_site/assets/app.js` — header shadow-on-scroll + scroll-reveal enhancement
- `/home/user/workspace/static_site/assets/img/*` — all photography (hero.png, hero-land.png, farm.png, wild-elk.png, wild-bison.png, wild-deer.png, host-sydney.png, sydney.png, exp-maine.png, exp-sarasota.png, exp-bvi.png, logo.jpg)

Read `index.html` and `style.css` fully before building — they contain the exact copy, classnames, and layout structure the theme templates must reproduce pixel-for-pixel. Reuse the CSS almost verbatim (adapt only where WordPress markup requires it, e.g. `wp_nav_menu()` output structure, `the_content()` wrapping, image `srcset`).

The page has these sections in this order (top to bottom): Header/nav, Hero, "The Land" (Where the river meets the ridge), "Wildlife" (The wildlife of 4,200 acres), "Host" (Meet Sydney), "The Series" (episode cards), "Our Story", "Follow" (Come along for the ride — signup form + social links), Footer.

## Hard requirements (do not deviate)
1. **WordPress theme** using **Advanced Custom Fields PRO** with a **flexible content field** that defines each page section, its content, and its order. Every section on the home page (hero, land, wildlife, host, series, story, follow) must be one row/layout in that flexible content field — nothing about section content is hardcoded in PHP templates.
2. **No hardcoded fallback/placeholder content anywhere in templates** — not in flexible-content layout partials, not in header.php/footer.php. All copy, images, links, and menu items must come from data (ACF fields via `get_field()`/`have_rows()`, or `wp_nav_menu()` menu locations) that is populated by the WXR import. Templates only contain markup/logic (loops, conditionals, escaping), never literal copy text.
3. **Menus**: register 3 nav menu locations — `primary` (header nav incl. the "Watch the Series" CTA as a menu item with CSS class `menu-cta`), `footer` (footer nav incl. "The Distillery" external link), `social` (Instagram/YouTube/TikTok/Facebook row in the Follow section). Render all three with `wp_nav_menu()` using their registered locations — never hardcode `<a>` tags for these.
4. **Gravity Forms** powers the "Come along for the ride" email signup form. The `signup_cta` flexible-content layout stores a Gravity Forms form ID (plain field) and the template renders it via `gravity_form( (int) get_sub_field('gravity_form_id'), false, false, false, '', true )` guarded by `if ( function_exists( 'gravity_form' ) )`.
5. **WXR import required**: every piece of real content (the Home page + its flexible-content field values, all menus + menu items, all media/attachments referenced by ACF image fields) must ship as a WordPress WXR (`.xml`) file that an admin imports via Tools → Import → WordPress. Do not rely on any content existing in the database already.
6. Use **ACF Local JSON** (`acf-json/` folder in the theme) to define field groups in version control — this is code, not content, and is fine to ship in the theme.

## ACF field group: "Page Builder" (group key `group_page_builder`)
- Location rule: Post Type == Page
- One field: `page_sections` (key `field_page_sections`), type `flexible_content`, button label "Add Section". Layouts (in this exact order of definition, sub-field names must match exactly since the WXR postmeta will use them):

### Layout `hero` — "Hero"
- `hero_eyebrow` (text)
- `hero_heading` (text) — the non-highlighted part of the H1
- `hero_heading_highlight` (text) — the emphasized word/phrase, wrapped in `<em>` by the template
- `hero_subheading` (textarea)
- `primary_cta` (link)
- `secondary_cta` (link)
- `background_image` (image, return format array)
- `stats` (repeater) → `stat_number` (text), `stat_label` (text)

### Layout `image_content` — "Image + Content" (reused for both "The Land" and "Host/Sydney" sections)
- `anchor_id` (text) — e.g. `land`, `host`
- `eyebrow` (text)
- `heading` (text)
- `heading_highlight` (text, optional)
- `lead_text` (textarea)
- `body_text` (wysiwyg)
- `bullet_list` (repeater) → `item_text` (text) — optional, only used on "The Land"
- `image` (image)
- `image_caption` (text, optional)
- `image_position` (select: `left` / `right`, default `right`) — controls whether the image column renders before or after the copy column
- `background_style` (select: `cream` / `sand`, default `cream`)
- `cta` (link, optional)

### Layout `wildlife_grid` — "Wildlife Grid"
- `anchor_id` (text)
- `eyebrow` (text)
- `heading` (text)
- `heading_highlight` (text)
- `lead_text` (textarea)
- `cards` (repeater) → `image` (image), `name` (text), `sub_label` (text), `is_featured` (true_false)
- `species_tags` (repeater) → `tag_text` (text)

### Layout `series_carousel` — "Series / Episodes"
- `anchor_id` (text)
- `eyebrow` (text)
- `heading` (text)
- `heading_highlight` (text)
- `lead_text` (textarea)
- `view_all_link` (link)
- `episodes` (repeater) → `image` (image), `badge_label` (text), `title` (text), `description` (text), `meta_text` (text), `duration_label` (text), `episode_link` (link, optional)

### Layout `story_band` — "Story / Text Band"
- `anchor_id` (text)
- `eyebrow` (text)
- `heading` (text)
- `lead_text` (textarea)
- `body_text` (wysiwyg)
- `cta` (link)

### Layout `signup_cta` — "Signup / Gravity Form CTA"
- `anchor_id` (text)
- `heading` (text)
- `lead_text` (textarea)
- `gravity_form_id` (number)
- `background_style` (select: `field` / `dark`, default `field`)

## ACF Options Page: "Theme Settings" (`acf-options-theme-settings`, menu slug `theme-settings`)
For the handful of site-wide chrome strings that aren't page sections (footer brand line, legal line). Fields:
- `brand_subtitle` (text) — small word under the wordmark in the header (e.g. "OUTDOORS")
- `footer_tagline` (text) — e.g. "4,200 acres · Paradise, Kentucky · Muhlenberg County"
- `footer_legal_text` (text)
- `footer_secondary_text` (text) — e.g. "Bourbon · Outdoors · Adventure"
Use `get_field('field_name', 'option')` in templates. The site title/wordmark itself must come from `bloginfo('name')` (set via the WXR `<title>`), not a hardcoded string.

## Theme structure to build (`/theme/coal-pick-outdoors/` in this repo)
```
style.css                 (theme header comment block + reused design CSS)
functions.php             (theme setup: menus, image sizes, enqueue assets, ACF options page registration, ACF JSON save/load points, theme support for title-tag/custom-logo/post-thumbnails)
header.php
footer.php
front-page.php            (or page.php used as the flexible-content template — pick whichever is more idiomatic; front-page.php checked first by WP)
page.php
index.php
inc/setup.php             (menus, image sizes, misc)
inc/acf.php                (options page + any helper fns)
template-parts/flexible/hero.php
template-parts/flexible/image-content.php
template-parts/flexible/wildlife-grid.php
template-parts/flexible/series-carousel.php
template-parts/flexible/story-band.php
template-parts/flexible/signup-cta.php
assets/css/style.css       (ported from the static mockup's assets/style.css)
assets/js/app.js           (ported from the static mockup's assets/app.js)
acf-json/group_page_builder.json
acf-json/group_theme_settings.json  (options page field group)
screenshot.png             (optional, skip if no time)
```
The flexible-content loop in front-page.php/page.php must call `get_template_part('template-parts/flexible/...', null, ['section' => $layout])` (or similar) per layout name, passing sub-field data through — do not print any copy directly in the loop file itself.

Copy the source images into `theme/coal-pick-outdoors/assets/img/` ONLY if they are pure design chrome (there should be none — check the CSS/HTML; every image in the mockup is real page content and must instead ship via the media package below and be referenced by ACF image fields, not the theme). The only exception: `logo.jpg` may be wired up via WordPress's native Custom Logo support (`the_custom_logo()`) rather than hardcoded — do not hardcode it in header.php either; register `custom-logo` theme support and call `the_custom_logo()`, falling back to nothing if unset (no fallback text/image).

## Media package (`/media-for-import/` — already contains the 12 image files copied from the mockup)
These are the raw files an admin uploads to the target site's `wp-content/uploads/2026/07/` directory (matching the paths referenced by the WXR attachment `<guid>` values below) BEFORE running the WXR import, so the WordPress importer can successfully fetch/copy them into the Media Library. Do not move/rename this folder's contents; just reference it from the docs.

## WXR content export (`/wxr/coal-pick-outdoors-content.xml`)
Build a valid WordPress eXtended RSS (WXR version 1.2) file containing:
1. **Site header info**: `<title>Coal Pick Outdoors</title>`, `<wp:wxr_version>1.2</wp:wxr_version>`, a `<wp:base_site_url>` / `<wp:base_blog_url>` set to the placeholder token `{{SITE_URL}}` (documented for admins to find-and-replace with their real domain before import if their importer needs absolute paths — WordPress's own importer mostly ignores these, but attachment guids matter, see below).
2. **Attachments**: one `<item>` per image in `/media-for-import/`, `post_type` = `attachment`, with a real, sequential `<wp:post_id>` (start attachment IDs at 5001 to reduce collision risk with any existing site content), `<guid>` = `{{SITE_URL}}/wp-content/uploads/2026/07/<filename>`, `<wp:attachment_url>` same, and appropriate `<title>`/`<wp:post_name>` (slugified filename) and alt text (`_wp_attachment_image_alt` postmeta) taken from the corresponding `alt=""` attribute in `index.html`.
3. **Menus**: three `<wp:term>` entries (taxonomy `nav_menu`) — "Primary Menu", "Footer Menu", "Social Menu" — plus one `nav_menu_item` `<item>` per link, in order, with correct `_menu_item_url`, `_menu_item_type` (custom for anchors/external, e.g. `#land`; `post_type` if ever pointing at a page), `_menu_item_menu_item_parent`, `_menu_item_classes` postmeta, and menu order:
   - Primary: The Land (#land) · Wildlife (#wildlife) · The Series (#series) · Our Story (#story) · Follow (#follow) · "Watch the Series" (#series, class `menu-cta`)
   - Footer: The Land (#land) · Wildlife (#wildlife) · The Series (#series) · Our Story (#story) · The Distillery (https://coalpickdistillery.com, target _blank)
   - Social: Instagram, YouTube, TikTok, Facebook — use `#` as placeholder URL only if index.html itself has no real URLs (it doesn't — check and use `#`, since we cannot invent real social profile URLs; note this in docs as a TODO for the client to fill in real URLs after import)
   Also include a `<wp:base_blog_url>`-relative `theme_mods` style is not exportable via WXR — instead document in INSTALL.md that after import the admin must assign these 3 menus to the `primary`/`footer`/`social` locations via Appearance → Menus (WXR cannot assign menu *locations*, only create the menus/items — this is a standard, unavoidable manual step, document it clearly).
4. **The Home page**: one `<item>` post_type `page`, title "Home", with `<wp:postmeta>` entries for `_wp_page_template` (front-page or your chosen template file) and the full ACF flexible-content postmeta set for `page_sections` — this means: `page_sections` = 7 (row count), `page_sections_0_acf_fc_layout` = `hero`, all `page_sections_0_*` sub-field meta keys/values, then `page_sections_1_acf_fc_layout` = `image_content` (The Land) ... through `page_sections_6_acf_fc_layout` = `signup_cta` (Follow), following ACF's standard flexible-content postmeta serialization pattern (flat meta keys per row/sub-field, repeaters get their own `_N` indexed sub-keys, image fields store the attachment post ID as the meta value, link fields store a serialized PHP array `{"url":..,"title":..,"target":..}` — use ACF's actual serialization format for the `link` field type, which is a serialized array via `serialize()`/PHP maybe-serialize, not JSON — verify current ACF Pro output format and match it exactly). Pull every value from the copy in `index.html` (exact text, not paraphrased) . Map:
   - hero → eyebrow "Paradise, Kentucky · Muhlenberg County", heading "4,200 acres", highlight "wild.", subheading, primary_cta "Explore the Land"→#land, secondary_cta "Watch the Series"→#series, background_image → hero-land.png attachment, 4 stats (4,200/Acres of Wild, 7/Game Species, 25+/Lakes & Waters, 12/Episodes a Year)
   - image_content (Land) → anchor `land`, eyebrow "The Home Ground", heading "Where the river", highlight "meets the ridge.", lead + body text verbatim, 4 bullet items, image farm.png, caption "The Green River bottom at first light · Paradise, KY", image_position `right`, background `cream`
   - wildlife_grid → anchor `wildlife`, eyebrow "What Roams Here", heading "The wildlife of", highlight "4,200 acres.", lead text, 3 cards (elk/bison/deer with their names+sub-labels, elk `is_featured`=true), 7 species tags
   - image_content (Host) → anchor `host`, eyebrow "Your Host", heading "Meet", highlight "Sydney.", body text (both paragraphs — put in body_text as two `<p>`), image host-sydney.png, image_position `left`, background `sand`, cta "Watch the Series →"→#series
   - series_carousel → anchor `series`, eyebrow "The Coal Pick Series", heading "Where's Coal Pick going", highlight "next?", lead text, view_all_link "All Episodes →"→#, 4 episodes exactly as in index.html (Home Ground/farm.png/Featured, Maine/exp-maine.png/Next Up, Sarasota/exp-sarasota.png/Upcoming, BVI/exp-bvi.png/Upcoming) with their descriptions/meta/duration labels
   - story_band → anchor `story`, eyebrow "It Starts in Paradise", heading "A ghost town, a river,", (note: no highlight word here — leave heading_highlight blank or fold "and the ground beneath it." into heading, match the visual: whole heading has no `<em>` in this section, only the lead's implicit style — just put full two-line heading in `heading` field, blank highlight), lead + body text verbatim, cta "Visit Coal Pick Distillery →" → https://coalpickdistillery.com (target _blank)
   - signup_cta → anchor `follow`, heading "Come along for the ride.", lead text verbatim, gravity_form_id 1 (matches the Gravity Forms export below), background `field`

## Gravity Forms export (`/gravityforms/come-along-for-the-ride-form.json`)
A valid Gravity Forms form-export JSON (the format produced by Forms → Import/Export → Export Forms — a JSON array containing one form object) for form ID 1, title "Come Along for the Ride", one field: Email field (type `email`, label "Email Address", required, placeholder "your@email.com"), submit button text "Sign Me Up", a basic confirmation message ("Thanks — you're on the list."), and a notification to the site admin email on submission. Match Gravity Forms' real export JSON schema/structure as closely as possible (field `id`, `type`, `label`, `isRequired`, `size`, `formId`; top-level `id`, `title`, `fields`, `button`, `confirmations`, `notifications`, `is_active`, `date_created`).

## Docs (`/docs/INSTALL.md`)
Write clear step-by-step install instructions covering, in order:
1. Prereqs: WordPress core, ACF PRO plugin (license required, not bundled), Gravity Forms plugin (license required, not bundled), active theme = coal-pick-outdoors.
2. Import the Gravity Forms JSON first (Forms → Import/Export → Import) so form ID 1 exists before the page that references it renders.
3. Upload all files from `/media-for-import/` to `wp-content/uploads/2026/07/` on the target server (matching the WXR guids) — explain the `{{SITE_URL}}` placeholder find-and-replace step in the WXR file before import if needed.
4. Import `/wxr/coal-pick-outdoors-content.xml` via Tools → Import → WordPress importer, mapping/creating an author.
5. Assign the 3 imported menus to Appearance → Menus locations: Primary, Footer, Social (manual step, WXR can't set this).
6. Set the imported Home page as the site's static front page (Settings → Reading), and set a Custom Logo (Appearance → Customize) if desired.
7. Note the ID-collision caveat: this package assumes import onto a clean/fresh WordPress database for guaranteed ACF image-field ID integrity; if importing onto a site with pre-existing content, verify ACF image fields resolve correctly after import (WordPress's importer preserves original post IDs only when those ID slots are free).

## Final steps
- Also add a top-level `README.md` summarizing the repo layout and linking to `docs/INSTALL.md`.
- Zip the whole repo contents (theme + wxr + gravityforms + media-for-import + docs) into `/home/user/workspace/coalpickoutdoors/coal-pick-outdoors-handoff.zip` for the human to download directly (in addition to committing everything to git and pushing to `main` on GitHub).
- Commit and push all files to `main` on `https://github.com/SteerPointMikeL/coalpickoutdoors`.
- At the end, report back exactly which files you created (with paths) and confirm the push succeeded (include the commit SHA/URL).
