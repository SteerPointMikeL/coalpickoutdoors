# Coal Pick Outdoors — WordPress Handoff Package

A portable WordPress build for **Coal Pick Outdoors** — 4,200 acres of Kentucky
wild in Paradise, Muhlenberg County. This repo is a **handoff package** (theme +
content export + form export + media), not a live site. An admin installs it
onto a fresh or existing WordPress site.

The design is data-driven end to end: **all** page copy, images, links, and menu
items flow through **Advanced Custom Fields PRO** (a flexible-content page
builder + an options page) and **WordPress nav menus** — nothing is hardcoded in
the PHP templates. The signup form is powered by **Gravity Forms**.

## Repository layout

```
theme/coal-pick-outdoors/          WordPress theme
  style.css                        Theme header + design CSS
  functions.php                    Bootstrap (enqueue, includes)
  header.php / footer.php          Chrome (custom logo, nav menus, options fields)
  front-page.php / page.php        Flexible-content render loop (no copy in the loop)
  index.php                        Fallback template
  inc/setup.php                    Menus, image sizes, theme supports, ACF JSON points
  inc/acf.php                      ACF options page + link/image render helpers
  template-parts/flexible/*.php    One partial per flexible-content layout
  assets/css/style.css             Ported design CSS (enqueued)
  assets/js/app.js                 Header shadow + scroll reveal
  acf-json/                        ACF Local JSON field groups (version-controlled)
    group_page_builder.json        "Page Builder" flexible content (7 layouts)
    group_theme_settings.json      "Theme Settings" options page

wxr/coal-pick-outdoors-content.xml WordPress content export (WXR 1.2):
                                   Home page + ACF sections, 12 attachments, 3 menus

gravityforms/come-along-for-the-ride-form.json  Gravity Forms export (form ID 1)

media-for-import/                  12 raw images to upload before importing the WXR

docs/INSTALL.md                    Step-by-step installation guide
build_assets.py                    Generator for acf-json + WXR (provenance/regeneration)
```

## The page builder

The `page_sections` flexible-content field defines the whole home page, one row
per section, in this order:

1. **hero** — Hero (eyebrow, heading + highlight, subheading, two CTAs, background image, 4 stats)
2. **image_content** — "The Land" (image right, cream)
3. **wildlife_grid** — "The wildlife of 4,200 acres" (3 cards + species tags)
4. **image_content** — "Meet Sydney" (image left, sand)
5. **series_carousel** — "The Coal Pick Series" (4 episode cards)
6. **story_band** — "Our Story"
7. **signup_cta** — "Come along for the ride" (Gravity Form + social menu)

## Menus (3 locations)

- **primary** — header nav incl. the "Watch the Series" CTA (`menu-cta` class)
- **footer** — footer nav incl. "The Distillery" external link
- **social** — Instagram / YouTube / TikTok / Facebook row in the Follow section

All three render via `wp_nav_menu()`; the WXR creates the menus and items, and the
admin assigns them to locations after import.

## Installation

See **[docs/INSTALL.md](docs/INSTALL.md)** for the full step-by-step guide
(prerequisites, import order, `{{SITE_URL}}` replacement, menu assignment,
static front page, Theme Settings, and the ID-collision caveat).

## Requirements

- WordPress 6.0+
- Advanced Custom Fields **PRO** (license required, not bundled)
- Gravity Forms (license required, not bundled)
