# Coal Pick Outdoors — Installation Guide

This is a **portable handoff package**: a WordPress theme plus content (WXR),
a Gravity Forms export, and the raw media files. Nothing here is "live" — an
admin installs it onto a fresh or existing WordPress site by following the
steps below **in order**.

> **Recommended:** install onto a **clean/fresh WordPress database**. This
> package uses fixed post IDs (attachments 5001–5012, Home page 4001, menu items
> 6001+) so that the ACF image fields resolve to the right attachments after
> import. On a site that already has content in those ID slots, WordPress will
> renumber the imported posts and the ACF image references may break — see
> step 8 (ID-collision caveat).

---

## 1. Prerequisites

Install and activate the following before importing anything:

| Requirement | Notes |
|-------------|-------|
| **WordPress** 6.0+ | Core install. |
| **Advanced Custom Fields PRO** | License required — **not bundled**. The theme's field groups load automatically from `theme/coal-pick-outdoors/acf-json/` (ACF Local JSON), so you do **not** import them manually. |
| **Gravity Forms** | License required — **not bundled**. Powers the signup form. |
| **WordPress Importer** | Install via Tools → Import → WordPress → "Install Now". |
| **Coal Pick Outdoors theme** | Copy `theme/coal-pick-outdoors/` to `wp-content/themes/` and activate it (Appearance → Themes). |

After activating the theme with ACF PRO active, confirm the field groups
**"Page Builder"** and **"Theme Settings"** appear under **Custom Fields →
Field Groups** (they load from the theme's `acf-json/` folder). As of this
version, activating the theme also force-syncs these Local JSON field groups
into the database (see Troubleshooting below), so re-activating the theme is
a safe way to resolve a stale field-group definition if you ever see one.

---

## 2. Import the Gravity Forms form FIRST

The Home page references **Gravity Forms form ID 1**, so the form must exist
before the page renders.

1. Go to **Forms → Import/Export → Import Forms**.
2. Upload `gravityforms/come-along-for-the-ride-form.json`.
3. Confirm a form titled **"Come Along for the Ride"** now exists with **ID 1**.

> If your site already has a form using ID 1, Gravity Forms will assign a new
> ID on import. In that case, after importing the content (step 4), edit the
> Home page → **Follow** section → set **Gravity Form ID** to the new ID.

---

## 3. Upload the media files

The WordPress importer needs the image files to be reachable at the exact URLs
referenced by the WXR before it can pull them into the Media Library.

1. Upload **all 12 files** from `media-for-import/` to
   `wp-content/uploads/2026/07/` on the target server (create the folder if it
   does not exist), via SFTP/SSH or your host's file manager.
2. Files: `hero.png`, `hero-land.png`, `farm.png`, `wild-elk.png`,
   `wild-bison.png`, `wild-deer.png`, `host-sydney.png`, `sydney.png`,
   `exp-maine.png`, `exp-sarasota.png`, `exp-bvi.png`, `logo.jpg`.

### `{{SITE_URL}}` placeholder

The WXR file (`wxr/coal-pick-outdoors-content.xml`) uses the token
`{{SITE_URL}}` in attachment `guid` / `attachment_url` values and the base URLs.
Before importing, **find-and-replace `{{SITE_URL}}` with your site's full URL**
(no trailing slash), e.g.:

```
{{SITE_URL}}   →   https://coalpickoutdoors.com
```

This ensures the importer resolves attachment URLs to
`https://coalpickoutdoors.com/wp-content/uploads/2026/07/<file>` and matches the
files you uploaded in the step above.

---

## 4. Import the content (WXR)

1. Go to **Tools → Import → WordPress → Run Importer**.
2. Upload the (placeholder-replaced) `wxr/coal-pick-outdoors-content.xml`.
3. When prompted, **assign the author** — map to an existing user or create one.
4. **Check "Download and import file attachments"** so the 12 images are added
   to the Media Library from the files you uploaded in step 3.
5. Run the import.

This creates: the **Home** page (with all 7 ACF flexible-content sections),
the 12 image **attachments**, and the three **menus** ("Primary Menu",
"Footer Menu", "Social Menu") with all their items.

---

## 5. Assign the menus to their locations (manual — WXR cannot do this)

WXR can create menus and items, but it **cannot** assign them to theme menu
locations. Do it manually:

1. Go to **Appearance → Menus → Manage Locations**.
2. Assign:
   - **Primary Menu** → `Primary Menu` location
   - **Footer Menu** → `Footer Menu` location
   - **Social Menu** → `Social Menu` location

### Fill in real social URLs (TODO)

The **Social Menu** items (Instagram, YouTube, TikTok, Facebook) import with
placeholder `#` URLs because the source mockup contained no real profile links.
Edit each item under **Appearance → Menus** and set the real profile URLs.

---

## 6. Set the static front page

1. Go to **Settings → Reading**.
2. Set **"Your homepage displays"** → **A static page**.
3. Set **Homepage** → **Home**.

The theme's `front-page.php` then renders the ACF page builder for that page.

---

## 7. Theme Settings and Custom Logo

### Theme Settings (site chrome not stored in the WXR)

WXR cannot import `wp_options` rows, so the site-wide chrome strings must be
entered by hand. Go to **Theme Settings** (admin menu) and set:

| Field | Suggested value |
|-------|-----------------|
| Brand Subtitle | `OUTDOORS` |
| Footer Tagline | `4,200 acres · Paradise, Kentucky · Muhlenberg County` |
| Footer Legal Text | `© 2026 Coal Pick Outdoors. Mockup for design approval.` |
| Footer Secondary Text | `Bourbon · Outdoors · Adventure` |

The site title/wordmark itself comes from **Settings → General → Site Title**
(the WXR sets it to "Coal Pick Outdoors"), rendered via `bloginfo('name')`.

### Custom Logo (optional)

To use the logo image instead of the text wordmark:
**Appearance → Customize → Site Identity → Select logo** and choose the
imported `logo.jpg` (or upload it). The theme registers `custom-logo` support
and renders it via `the_custom_logo()`; if unset it falls back to the text
wordmark + brand subtitle.

---

## 8. ID-collision caveat

This package assumes import onto a **clean database** for guaranteed ACF
image-field integrity. ACF image fields store the **attachment post ID**
(5001–5012). WordPress's importer preserves original post IDs **only when those
ID slots are free**. If you import onto a site that already has content
occupying those IDs, the importer renumbers the attachments and the ACF image
fields will point at the wrong (or missing) attachments.

If importing onto a non-empty site, after import **open the Home page in the
editor and re-select each image** in the flexible-content sections (hero
background, The Land photo, the three wildlife cards, Sydney's photo, and the
four episode thumbnails) to repair the references.

---

## Troubleshooting: "Page Sections" field shows as a plain number instead of the page content

If `get_field('page_sections')` on the Home page returns a bare integer (e.g.
`7`) instead of an array of section rows, and the front end renders blank,
this is **not** a WXR/data problem — it's an ACF field-registration problem.
We verified this directly: importing this package's `wxr/coal-pick-outdoors-content.xml`
into a real WordPress install and inspecting `wp_postmeta` afterward showed
the data lands exactly as intended — `page_sections` = `7` (the row count,
per ACF's own flexible-content storage convention), `_page_sections` =
`field_page_sections` (the correct reference key), and all 7 rows'
`page_sections_N_acf_fc_layout` keys present and correctly ordered (`hero`,
`image_content`, `wildlife_grid`, `image_content`, `series_carousel`,
`story_band`, `signup_cta`). That integer is the *correct* raw value — ACF is
supposed to convert it into an array of rows at read time using the field
definition in `acf-json/group_page_builder.json`. If it doesn't, ACF could
not resolve that field definition when the page rendered. Check these causes,
in order of likelihood:

1. **A stale field-group definition already exists in the database.** ACF's
   Local JSON only lets a theme's `acf-json/*.json` file override a
   database-stored copy of the same field group when the JSON file's
   `modified` timestamp is *newer* than the database copy's. If an earlier
   import attempt, a manual field-group edit, or a previous version of this
   theme left behind a database copy of `group_page_builder` with a
   different or incomplete definition (e.g. `page_sections` saved as a plain
   number field instead of `flexible_content`), that stale copy can silently
   win. **Fix:** re-activate the theme (Appearance → Themes → activate a
   different theme, then activate Coal Pick Outdoors again) — this now
   force-imports the Local JSON field groups into the database on every
   activation, overwriting any stale copy. Or manually delete the "Page
   Builder" / "Theme Settings" entries under **Custom Fields → Field Groups**
   in wp-admin if they look wrong; they will reappear correctly from Local
   JSON.
2. **ACF PRO isn't actually active** (only the free version, or no ACF at
   all). `flexible_content` is a PRO-only field type. If ACF can't find a
   handler for that type, `get_field()` returns the raw postmeta value
   unconverted — this looks identical to symptom described above. **Fix:**
   confirm Advanced Custom Fields **PRO** (not the free plugin) is installed,
   activated, and licensed.
3. **The theme wasn't active when the field groups needed to load**, or a
   different theme is active. Local JSON is only read from the *active*
   theme's `acf-json/` folder. **Fix:** activate the Coal Pick Outdoors theme
   before checking field groups or importing content.
4. After fixing the above, open the Home page in **wp-admin's editor** (not
   just the front end) and confirm the "Page Sections" flexible-content rows
   render correctly there. This isolates the problem to ACF's field
   resolution (editor also broken) vs. a front-end template bug (editor
   fine, front end blank).

---

## Quick checklist

- [ ] ACF PRO + Gravity Forms active; theme activated
- [ ] Gravity Forms JSON imported (form ID 1)
- [ ] 12 media files uploaded to `wp-content/uploads/2026/07/`
- [ ] `{{SITE_URL}}` replaced in the WXR
- [ ] WXR imported (with "download and import file attachments" checked)
- [ ] 3 menus assigned to Primary / Footer / Social locations
- [ ] Real social profile URLs filled in
- [ ] Home set as static front page
- [ ] Theme Settings fields entered; Custom Logo set (optional)
