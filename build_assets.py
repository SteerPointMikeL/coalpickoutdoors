#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate ACF Local JSON field groups + the WXR content export for
Coal Pick Outdoors from a single shared schema, so field keys/names stay
consistent between the theme's acf-json and the WordPress import file."""

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ACF_DIR = os.path.join(ROOT, "theme", "coal-pick-outdoors", "acf-json")
WXR_PATH = os.path.join(ROOT, "wxr", "coal-pick-outdoors-content.xml")

SITE = "{{SITE_URL}}"
UPLOAD_BASE = SITE + "/wp-content/uploads/2026/07/"
DATE = "2026-07-16 10:00:00"
AUTHOR = "coalpick"

# --------------------------------------------------------------------------
# PHP serialization helpers (byte-length aware, matches WP/ACF storage)
# --------------------------------------------------------------------------
def php_str(s):
    b = s.encode("utf-8")
    return 's:%d:"%s";' % (len(b), s)

def php_link(link):
    if not link or not link.get("url"):
        return ""
    title = link.get("title", "")
    url = link.get("url", "")
    target = link.get("target", "")
    inner = php_str("title") + php_str(title) + php_str("url") + php_str(url) + php_str("target") + php_str(target)
    return "a:3:{%s}" % inner

def php_classes(cls):
    val = cls if cls else ""
    return "a:1:{i:0;%s}" % php_str(val)

# --------------------------------------------------------------------------
# Attachments (id -> filename, alt, mime)
# --------------------------------------------------------------------------
ATTACHMENTS = [
    (5001, "exp-bvi.png", "A sailboat in the British Virgin Islands", "image/png"),
    (5002, "exp-maine.png", "A lobster boat off the coast of Maine", "image/png"),
    (5003, "exp-sarasota.png", "A tarpon leaping off Sarasota", "image/png"),
    (5004, "farm.png", "The Green River valley on the Coal Pick property wrapped in morning light", "image/png"),
    (5005, "hero-land.png", "A sweeping view of the 4,200-acre Coal Pick property — the Green River valley, hardwood ridges, and open fields in autumn", "image/png"),
    (5006, "hero.png", "The Coal Pick Outdoors property in Kentucky", "image/png"),
    (5007, "host-sydney.png", "The host of Coal Pick Outdoors walking a Kentucky field above the river valley", "image/png"),
    (5008, "logo.jpg", "Coal Pick Outdoors", "image/jpeg"),
    (5009, "sydney.png", "Sydney Shrewsberry, host of Coal Pick Outdoors", "image/png"),
    (5010, "wild-bison.png", "An American bison grazing in a tallgrass meadow", "image/png"),
    (5011, "wild-deer.png", "A mature whitetail buck in a green clearing", "image/png"),
    (5012, "wild-elk.png", "A bull elk in a sunlit autumn meadow", "image/png"),
]

# --------------------------------------------------------------------------
# Schema: layout name -> (layout key, label, [fields])
# field = (name, key, type, extra)
# --------------------------------------------------------------------------
SCHEMA = {
    "hero": ("layout_hero", "Hero", [
        ("hero_eyebrow", "field_hero_eyebrow", "text", {}),
        ("hero_heading", "field_hero_heading", "text", {}),
        ("hero_heading_highlight", "field_hero_heading_highlight", "text", {}),
        ("hero_subheading", "field_hero_subheading", "textarea", {}),
        ("primary_cta", "field_primary_cta", "link", {}),
        ("secondary_cta", "field_secondary_cta", "link", {}),
        ("background_image", "field_background_image", "image", {}),
        ("stats", "field_stats", "repeater", {"sub": [
            ("stat_number", "field_stat_number", "text", {}),
            ("stat_label", "field_stat_label", "text", {}),
        ]}),
    ]),
    "image_content": ("layout_image_content", "Image + Content", [
        ("anchor_id", "field_ic_anchor_id", "text", {}),
        ("eyebrow", "field_ic_eyebrow", "text", {}),
        ("heading", "field_ic_heading", "text", {}),
        ("heading_highlight", "field_ic_heading_highlight", "text", {}),
        ("lead_text", "field_ic_lead_text", "textarea", {}),
        ("body_text", "field_ic_body_text", "wysiwyg", {}),
        ("bullet_list", "field_ic_bullet_list", "repeater", {"sub": [
            ("item_text", "field_ic_item_text", "text", {}),
        ]}),
        ("image", "field_ic_image", "image", {}),
        ("image_caption", "field_ic_image_caption", "text", {}),
        ("image_position", "field_ic_image_position", "select", {"choices": {"left": "Left", "right": "Right"}, "default": "right"}),
        ("background_style", "field_ic_background_style", "select", {"choices": {"cream": "Cream", "sand": "Sand"}, "default": "cream"}),
        ("cta", "field_ic_cta", "link", {}),
    ]),
    "wildlife_grid": ("layout_wildlife_grid", "Wildlife Grid", [
        ("anchor_id", "field_wg_anchor_id", "text", {}),
        ("eyebrow", "field_wg_eyebrow", "text", {}),
        ("heading", "field_wg_heading", "text", {}),
        ("heading_highlight", "field_wg_heading_highlight", "text", {}),
        ("lead_text", "field_wg_lead_text", "textarea", {}),
        ("cards", "field_wg_cards", "repeater", {"sub": [
            ("image", "field_wg_card_image", "image", {}),
            ("name", "field_wg_card_name", "text", {}),
            ("sub_label", "field_wg_card_sub_label", "text", {}),
            ("is_featured", "field_wg_card_is_featured", "true_false", {}),
        ]}),
        ("species_tags", "field_wg_species_tags", "repeater", {"sub": [
            ("tag_text", "field_wg_tag_text", "text", {}),
        ]}),
    ]),
    "series_carousel": ("layout_series_carousel", "Series / Episodes", [
        ("anchor_id", "field_sc_anchor_id", "text", {}),
        ("eyebrow", "field_sc_eyebrow", "text", {}),
        ("heading", "field_sc_heading", "text", {}),
        ("heading_highlight", "field_sc_heading_highlight", "text", {}),
        ("lead_text", "field_sc_lead_text", "textarea", {}),
        ("view_all_link", "field_sc_view_all_link", "link", {}),
        ("episodes", "field_sc_episodes", "repeater", {"sub": [
            ("image", "field_sc_ep_image", "image", {}),
            ("badge_label", "field_sc_ep_badge_label", "text", {}),
            ("title", "field_sc_ep_title", "text", {}),
            ("description", "field_sc_ep_description", "textarea", {}),
            ("meta_text", "field_sc_ep_meta_text", "text", {}),
            ("duration_label", "field_sc_ep_duration_label", "text", {}),
            ("episode_link", "field_sc_ep_link", "link", {}),
        ]}),
    ]),
    "story_band": ("layout_story_band", "Story / Text Band", [
        ("anchor_id", "field_sb_anchor_id", "text", {}),
        ("eyebrow", "field_sb_eyebrow", "text", {}),
        ("heading", "field_sb_heading", "text", {}),
        ("lead_text", "field_sb_lead_text", "textarea", {}),
        ("body_text", "field_sb_body_text", "wysiwyg", {}),
        ("cta", "field_sb_cta", "link", {}),
    ]),
    "signup_cta": ("layout_signup_cta", "Signup / Gravity Form CTA", [
        ("anchor_id", "field_su_anchor_id", "text", {}),
        ("heading", "field_su_heading", "text", {}),
        ("lead_text", "field_su_lead_text", "textarea", {}),
        ("gravity_form_id", "field_su_gravity_form_id", "number", {}),
        ("background_style", "field_su_background_style", "select", {"choices": {"field": "Field (green)", "dark": "Dark forest"}, "default": "field"}),
    ]),
}

LAYOUT_ORDER = ["hero", "image_content", "wildlife_grid", "series_carousel", "story_band", "signup_cta"]

# --------------------------------------------------------------------------
# Content values for the Home page (verbatim from the static mockup)
# --------------------------------------------------------------------------
SECTIONS = [
    ("hero", {
        "hero_eyebrow": "Paradise, Kentucky · Muhlenberg County",
        "hero_heading": "4,200 acres of Kentucky",
        "hero_heading_highlight": "wild.",
        "hero_subheading": "River bottom and hardwood ridge. Elk, bison, and whitetail. This is the home ground behind Coal Pick — and the start of every adventure.",
        "primary_cta": {"title": "Explore the Land", "url": "#land", "target": ""},
        "secondary_cta": {"title": "Watch the Series", "url": "#series", "target": ""},
        "background_image": 5005,
        "stats": [
            {"stat_number": "4,200", "stat_label": "Acres of Wild"},
            {"stat_number": "7", "stat_label": "Game Species"},
            {"stat_number": "25+", "stat_label": "Lakes & Waters"},
            {"stat_number": "12", "stat_label": "Episodes a Year"},
        ],
    }),
    ("image_content", {
        "anchor_id": "land",
        "eyebrow": "The Home Ground",
        "heading": "Where the river",
        "heading_highlight": "meets the ridge.",
        "lead_text": "Tucked into the Green River bottom of Muhlenberg County, the Coal Pick property runs 4,200 acres of managed hardwood forest, open field, and water — one of the top Boone & Crockett counties in the nation.",
        "body_text": "<p>White oak, red oak, hickory, black walnut, and cedar stands give way to more than twenty-five lakes and swamps. It's been under private herd management for two decades, and it shows in every season.</p>",
        "bullet_list": [
            {"item_text": "Oak-hickory hardwood forest"},
            {"item_text": "Green River bottomland"},
            {"item_text": "25+ lakes, ponds & swamps"},
            {"item_text": "Managed food plots & open field"},
        ],
        "image": 5004,
        "image_caption": "The Green River bottom at first light · Paradise, KY",
        "image_position": "right",
        "background_style": "cream",
        "cta": {"title": "", "url": "", "target": ""},
    }),
    ("wildlife_grid", {
        "anchor_id": "wildlife",
        "eyebrow": "What Roams Here",
        "heading": "The wildlife of",
        "heading_highlight": "4,200 acres.",
        "lead_text": "Elk bugling in the fall. Bison on the tallgrass. Whitetail, turkey, waterfowl, quail, and bass in twenty-five waters. This is a working wildlife refuge as much as it is a hunting ground.",
        "cards": [
            {"image": 5012, "name": "Rocky Mountain Elk", "sub_label": "Fall bugle · September–October", "is_featured": 1},
            {"image": 5010, "name": "American Bison", "sub_label": "Year-round on the prairie", "is_featured": 0},
            {"image": 5011, "name": "Whitetail Deer", "sub_label": "Boone & Crockett country", "is_featured": 0},
        ],
        "species_tags": [
            {"tag_text": "Elk"}, {"tag_text": "Bison"}, {"tag_text": "Whitetail"},
            {"tag_text": "Wild Turkey"}, {"tag_text": "Waterfowl"},
            {"tag_text": "Bobwhite Quail"}, {"tag_text": "Largemouth Bass"},
        ],
    }),
    ("image_content", {
        "anchor_id": "host",
        "eyebrow": "Your Host",
        "heading": "Meet",
        "heading_highlight": "Sydney.",
        "lead_text": "",
        "body_text": "<p>Sydney Shrewsberry is the one taking you across the land and out on the road — Miss Indiana 2025, marketing degree in hand, equally at home on a hunting stand or the bow of a fishing boat.</p><p>Each episode of the series follows her onto the property and beyond it, chasing the seasons and the adventures behind the brand.</p>",
        "bullet_list": [],
        "image": 5007,
        "image_caption": "",
        "image_position": "left",
        "background_style": "sand",
        "cta": {"title": "Watch the Series →", "url": "#series", "target": ""},
    }),
    ("series_carousel", {
        "anchor_id": "series",
        "eyebrow": "The Coal Pick Series",
        "heading": "Where's Coal Pick going",
        "heading_highlight": "next?",
        "lead_text": "Twelve episodes a year. From the home ground in Kentucky to wild country coast to coast.",
        "view_all_link": {"title": "All Episodes →", "url": "#", "target": ""},
        "episodes": [
            {"image": 5004, "badge_label": "Featured", "title": "The Home Ground — 4,200 Acres", "description": "A season on the land: elk, bison, and the Green River bottom.", "meta_text": "Kentucky · Ep. 01", "duration_label": "Home", "episode_link": {"title": "", "url": "", "target": ""}},
            {"image": 5002, "badge_label": "Next Up", "title": "Maine — The Lobster Boat", "description": "Out on the Atlantic hauling traps off the ocean floor.", "meta_text": "Maine · Ep. 02", "duration_label": "Aug '26", "episode_link": {"title": "", "url": "", "target": ""}},
            {"image": 5003, "badge_label": "Upcoming", "title": "Sarasota — Tarpon Season", "description": "Chasing the silver king on the Gulf Coast flats.", "meta_text": "Florida · Ep. 03", "duration_label": "Jun '27", "episode_link": {"title": "", "url": "", "target": ""}},
            {"image": 5001, "badge_label": "Upcoming", "title": "British Virgin Islands", "description": "Island to island across the Caribbean.", "meta_text": "Caribbean · Ep. 04", "duration_label": "Feb '27", "episode_link": {"title": "", "url": "", "target": ""}},
        ],
    }),
    ("story_band", {
        "anchor_id": "story",
        "eyebrow": "It Starts in Paradise",
        "heading": "A ghost town, a river,\nand the ground beneath it.",
        "lead_text": "Paradise, Kentucky isn't on most maps anymore — but it's on ours. In 1820, the first commercial coal mine in America opened right here in Muhlenberg County. A few miles up the Green River, a Scottish lord built the Airdrie Ironworks in 1855. This county was once called the Saudi Arabia of coal.",
        "body_text": "<p>That's the ground Coal Pick sits on. Coal Pick Outdoors is how we share it — the land, the animals, and the adventures that come with them. When you're ready for the bottle, the distillery is one click away.</p>",
        "cta": {"title": "Visit Coal Pick Distillery →", "url": "https://coalpickdistillery.com", "target": "_blank"},
    }),
    ("signup_cta", {
        "anchor_id": "follow",
        "heading": "Come along for the ride.",
        "lead_text": "New episodes, behind-the-scenes footage, and first looks at where Coal Pick heads next.",
        "gravity_form_id": "1",
        "background_style": "field",
    }),
]

# --------------------------------------------------------------------------
# Meta emission
# --------------------------------------------------------------------------
def php_serialize_string(s):
    b = s.encode("utf-8")
    return 's:%d:"%s";' % (len(b), s)

def php_serialize_array_of_strings(items):
    parts = ["a:%d:{" % len(items)]
    for i, item in enumerate(items):
        parts.append("i:%d;" % i)
        parts.append(php_serialize_string(item))
    parts.append("}")
    return "".join(parts)

def serialize_value(ftype, value):
    if ftype == "link":
        return php_link(value)
    if ftype == "image":
        return "" if not value else str(value)
    if ftype == "true_false":
        return "1" if value in (1, "1", True) else "0"
    return "" if value is None else str(value)

def emit_fields(prefix, fields, values, out):
    for name, key, ftype, extra in fields:
        meta_key = "%s_%s" % (prefix, name)
        if ftype == "repeater":
            rows = values.get(name, []) or []
            out.append((meta_key, str(len(rows))))
            out.append(("_" + meta_key, key))
            for i, row in enumerate(rows):
                emit_fields("%s_%d" % (meta_key, i), extra["sub"], row, out)
        else:
            out.append((meta_key, serialize_value(ftype, values.get(name, ""))))
            out.append(("_" + meta_key, key))

def emit_page_sections():
    out = []
    layout_names = [layout for layout, _vals in SECTIONS]
    out.append(("page_sections", php_serialize_array_of_strings(layout_names)))
    out.append(("_page_sections", "field_page_sections"))
    for i, (layout, vals) in enumerate(SECTIONS):
        _lkey, _label, fields = SCHEMA[layout]
        emit_fields("page_sections_%d" % i, fields, vals, out)
    return out

# --------------------------------------------------------------------------
# ACF JSON generation
# --------------------------------------------------------------------------
def acf_field(name, key, ftype, extra, order):
    base = {
        "key": key,
        "label": " ".join(w.capitalize() for w in name.split("_")),
        "name": name,
        "type": ftype,
        "instructions": "",
        "required": 0,
        "conditional_logic": 0,
        "wrapper": {"width": "", "class": "", "id": ""},
    }
    if ftype in ("text",):
        base.update({"default_value": "", "placeholder": "", "maxlength": ""})
    elif ftype == "textarea":
        base.update({"default_value": "", "placeholder": "", "rows": "", "new_lines": ""})
    elif ftype == "wysiwyg":
        base.update({"default_value": "", "tabs": "all", "toolbar": "full", "media_upload": 1, "delay": 0})
    elif ftype == "number":
        base.update({"default_value": "", "placeholder": "", "min": "", "max": "", "step": ""})
    elif ftype == "image":
        base.update({"return_format": "array", "preview_size": "medium", "library": "all", "min_width": "", "min_height": "", "min_size": "", "max_width": "", "max_height": "", "max_size": "", "mime_types": ""})
    elif ftype == "link":
        base.update({"return_format": "array"})
    elif ftype == "true_false":
        base.update({"message": "", "default_value": 0, "ui": 1, "ui_on_text": "", "ui_off_text": ""})
    elif ftype == "select":
        base.update({"choices": extra.get("choices", {}), "default_value": extra.get("default", ""), "allow_null": 0, "multiple": 0, "ui": 0, "return_format": "value", "ajax": 0, "placeholder": ""})
    elif ftype == "repeater":
        base.update({
            "layout": "block",
            "min": 0,
            "max": 0,
            "collapsed": "",
            "button_label": "Add Row",
            "sub_fields": [acf_field(n, k, t, e, j) for j, (n, k, t, e) in enumerate(extra["sub"])],
        })
    return base

def build_page_builder_group():
    layouts = {}
    for layout in LAYOUT_ORDER:
        lkey, label, fields = SCHEMA[layout]
        layouts[lkey] = {
            "key": lkey,
            "name": layout,
            "label": label,
            "display": "block",
            "sub_fields": [acf_field(n, k, t, e, j) for j, (n, k, t, e) in enumerate(fields)],
            "min": "",
            "max": "",
        }
    group = {
        "key": "group_page_builder",
        "title": "Page Builder",
        "fields": [{
            "key": "field_page_sections",
            "label": "Page Sections",
            "name": "page_sections",
            "type": "flexible_content",
            "instructions": "",
            "required": 0,
            "conditional_logic": 0,
            "wrapper": {"width": "", "class": "", "id": ""},
            "layouts": layouts,
            "button_label": "Add Section",
            "min": "",
            "max": "",
        }],
        "location": [[{"param": "post_type", "operator": "==", "value": "page"}]],
        "menu_order": 0,
        "position": "normal",
        "style": "default",
        "label_placement": "top",
        "instruction_placement": "label",
        "hide_on_screen": ["the_content"],
        "active": True,
        "description": "",
        "show_in_rest": 0,
        "modified": 1752660000,
    }
    return group

def build_theme_settings_group():
    fields_def = [
        ("brand_subtitle", "field_brand_subtitle", "text"),
        ("footer_tagline", "field_footer_tagline", "text"),
        ("footer_legal_text", "field_footer_legal_text", "text"),
        ("footer_secondary_text", "field_footer_secondary_text", "text"),
    ]
    return {
        "key": "group_theme_settings",
        "title": "Theme Settings",
        "fields": [acf_field(n, k, t, {}, j) for j, (n, k, t) in enumerate(fields_def)],
        "location": [[{"param": "options_page", "operator": "==", "value": "theme-settings"}]],
        "menu_order": 0,
        "position": "normal",
        "style": "default",
        "label_placement": "top",
        "instruction_placement": "label",
        "hide_on_screen": "",
        "active": True,
        "description": "",
        "show_in_rest": 0,
        "modified": 1752660000,
    }

# --------------------------------------------------------------------------
# WXR generation
# --------------------------------------------------------------------------
def cdata(s):
    return "<![CDATA[%s]]>" % s

def postmeta_xml(pairs, indent="\t\t\t"):
    out = []
    for k, v in pairs:
        out.append("%s<wp:postmeta>\n%s\t<wp:meta_key>%s</wp:meta_key>\n%s\t<wp:meta_value>%s</wp:meta_value>\n%s</wp:postmeta>"
                   % (indent, indent, cdata(k), indent, cdata(v), indent))
    return "\n".join(out)

MENUS = [
    (2001, "Primary Menu", "primary-menu", [
        ("The Land", "#land", "", ""),
        ("Wildlife", "#wildlife", "", ""),
        ("The Series", "#series", "", ""),
        ("Our Story", "#story", "", ""),
        ("Follow", "#follow", "", ""),
        ("Watch the Series", "#series", "", "menu-cta"),
    ]),
    (2002, "Footer Menu", "footer-menu", [
        ("The Land", "#land", "", ""),
        ("Wildlife", "#wildlife", "", ""),
        ("The Series", "#series", "", ""),
        ("Our Story", "#story", "", ""),
        ("The Distillery", "https://coalpickdistillery.com", "_blank", ""),
    ]),
    (2003, "Social Menu", "social-menu", [
        ("Instagram", "#", "", ""),
        ("YouTube", "#", "", ""),
        ("TikTok", "#", "", ""),
        ("Facebook", "#", "", ""),
    ]),
]

def build_wxr():
    items = []

    # --- Attachments ---
    for pid, fname, alt, mime in ATTACHMENTS:
        slug = os.path.splitext(fname)[0]
        title = slug.replace("-", " ").title()
        url = UPLOAD_BASE + fname
        meta = [
            ("_wp_attached_file", "2026/07/" + fname),
            ("_wp_attachment_image_alt", alt),
        ]
        items.append(
            "\t<item>\n"
            "\t\t<title>%s</title>\n"
            "\t\t<link>%s</link>\n"
            "\t\t<pubDate>Thu, 16 Jul 2026 10:00:00 +0000</pubDate>\n"
            "\t\t<dc:creator>%s</dc:creator>\n"
            "\t\t<guid isPermaLink=\"false\">%s</guid>\n"
            "\t\t<description></description>\n"
            "\t\t<content:encoded>%s</content:encoded>\n"
            "\t\t<excerpt:encoded>%s</excerpt:encoded>\n"
            "\t\t<wp:post_id>%d</wp:post_id>\n"
            "\t\t<wp:post_date>%s</wp:post_date>\n"
            "\t\t<wp:post_date_gmt>%s</wp:post_date_gmt>\n"
            "\t\t<wp:comment_status>closed</wp:comment_status>\n"
            "\t\t<wp:ping_status>closed</wp:ping_status>\n"
            "\t\t<wp:post_name>%s</wp:post_name>\n"
            "\t\t<wp:status>inherit</wp:status>\n"
            "\t\t<wp:post_parent>0</wp:post_parent>\n"
            "\t\t<wp:menu_order>0</wp:menu_order>\n"
            "\t\t<wp:post_type>attachment</wp:post_type>\n"
            "\t\t<wp:post_password></wp:post_password>\n"
            "\t\t<wp:is_sticky>0</wp:is_sticky>\n"
            "\t\t<wp:attachment_url>%s</wp:attachment_url>\n"
            "%s\n"
            "\t</item>"
            % (cdata(title), url, cdata(AUTHOR), url, cdata(""), cdata(""),
               pid, DATE, DATE, cdata(slug), url, postmeta_xml(meta))
        )

    # --- Home page ---
    page_meta = [("_wp_page_template", "default")] + emit_page_sections()
    items.append(
        "\t<item>\n"
        "\t\t<title>%s</title>\n"
        "\t\t<link>%s/</link>\n"
        "\t\t<pubDate>Thu, 16 Jul 2026 10:00:00 +0000</pubDate>\n"
        "\t\t<dc:creator>%s</dc:creator>\n"
        "\t\t<guid isPermaLink=\"false\">%s/?page_id=4001</guid>\n"
        "\t\t<description></description>\n"
        "\t\t<content:encoded>%s</content:encoded>\n"
        "\t\t<excerpt:encoded>%s</excerpt:encoded>\n"
        "\t\t<wp:post_id>4001</wp:post_id>\n"
        "\t\t<wp:post_date>%s</wp:post_date>\n"
        "\t\t<wp:post_date_gmt>%s</wp:post_date_gmt>\n"
        "\t\t<wp:comment_status>closed</wp:comment_status>\n"
        "\t\t<wp:ping_status>closed</wp:ping_status>\n"
        "\t\t<wp:post_name>home</wp:post_name>\n"
        "\t\t<wp:status>publish</wp:status>\n"
        "\t\t<wp:post_parent>0</wp:post_parent>\n"
        "\t\t<wp:menu_order>0</wp:menu_order>\n"
        "\t\t<wp:post_type>page</wp:post_type>\n"
        "\t\t<wp:post_password></wp:post_password>\n"
        "\t\t<wp:is_sticky>0</wp:is_sticky>\n"
        "%s\n"
        "\t</item>"
        % (cdata("Home"), SITE, cdata(AUTHOR), SITE, cdata(""), cdata(""),
           DATE, DATE, postmeta_xml(page_meta))
    )

    # --- Menu terms ---
    terms = []
    for tid, name, slug, _ in MENUS:
        terms.append(
            "\t<wp:term>\n"
            "\t\t<wp:term_id>%d</wp:term_id>\n"
            "\t\t<wp:term_taxonomy>nav_menu</wp:term_taxonomy>\n"
            "\t\t<wp:term_slug>%s</wp:term_slug>\n"
            "\t\t<wp:term_name>%s</wp:term_name>\n"
            "\t</wp:term>" % (tid, slug, cdata(name))
        )

    # --- Menu items ---
    item_id = 6001
    for tid, name, slug, links in MENUS:
        for order, (mtitle, murl, mtarget, mclass) in enumerate(links, start=1):
            meta = [
                ("_menu_item_type", "custom"),
                ("_menu_item_menu_item_parent", "0"),
                ("_menu_item_object_id", str(item_id)),
                ("_menu_item_object", "custom"),
                ("_menu_item_target", mtarget),
                ("_menu_item_classes", php_classes(mclass)),
                ("_menu_item_xfn", ""),
                ("_menu_item_url", murl),
            ]
            items.append(
                "\t<item>\n"
                "\t\t<title>%s</title>\n"
                "\t\t<link>%s</link>\n"
                "\t\t<pubDate>Thu, 16 Jul 2026 10:00:00 +0000</pubDate>\n"
                "\t\t<dc:creator>%s</dc:creator>\n"
                "\t\t<guid isPermaLink=\"false\">%s/?p=%d</guid>\n"
                "\t\t<description></description>\n"
                "\t\t<content:encoded>%s</content:encoded>\n"
                "\t\t<excerpt:encoded>%s</excerpt:encoded>\n"
                "\t\t<wp:post_id>%d</wp:post_id>\n"
                "\t\t<wp:post_date>%s</wp:post_date>\n"
                "\t\t<wp:post_date_gmt>%s</wp:post_date_gmt>\n"
                "\t\t<wp:comment_status>closed</wp:comment_status>\n"
                "\t\t<wp:ping_status>closed</wp:ping_status>\n"
                "\t\t<wp:post_name>%d</wp:post_name>\n"
                "\t\t<wp:status>publish</wp:status>\n"
                "\t\t<wp:post_parent>0</wp:post_parent>\n"
                "\t\t<wp:menu_order>%d</wp:menu_order>\n"
                "\t\t<wp:post_type>nav_menu_item</wp:post_type>\n"
                "\t\t<wp:post_password></wp:post_password>\n"
                "\t\t<wp:is_sticky>0</wp:is_sticky>\n"
                "\t\t<category domain=\"nav_menu\" nicename=\"%s\">%s</category>\n"
                "%s\n"
                "\t</item>"
                % (cdata(mtitle), SITE, cdata(AUTHOR), SITE, item_id, cdata(""), cdata(""),
                   item_id, DATE, DATE, item_id, order, slug, cdata(name), postmeta_xml(meta))
            )
            item_id += 1

    header = (
        '<?xml version="1.0" encoding="UTF-8" ?>\n'
        "<!--\n"
        "  Coal Pick Outdoors — WordPress content export (WXR 1.2).\n"
        "  Replace the {{SITE_URL}} token with your site's URL (e.g. https://example.com)\n"
        "  before import if your importer needs absolute attachment URLs.\n"
        "-->\n"
        '<rss version="2.0"\n'
        '\txmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"\n'
        '\txmlns:content="http://purl.org/rss/1.0/modules/content/"\n'
        '\txmlns:wfw="http://wellformedweb.org/CommentAPI/"\n'
        '\txmlns:dc="http://purl.org/dc/elements/1.1/"\n'
        '\txmlns:wp="http://wordpress.org/export/1.2/">\n'
        "<channel>\n"
        "\t<title>Coal Pick Outdoors</title>\n"
        "\t<link>%s</link>\n"
        "\t<description>4,200 acres of Kentucky wild.</description>\n"
        "\t<pubDate>Thu, 16 Jul 2026 10:00:00 +0000</pubDate>\n"
        "\t<language>en-US</language>\n"
        "\t<wp:wxr_version>1.2</wp:wxr_version>\n"
        "\t<wp:base_site_url>%s</wp:base_site_url>\n"
        "\t<wp:base_blog_url>%s</wp:base_blog_url>\n"
        "\t<wp:author>\n"
        "\t\t<wp:author_id>1</wp:author_id>\n"
        "\t\t<wp:author_login>%s</wp:author_login>\n"
        "\t\t<wp:author_email>admin@example.com</wp:author_email>\n"
        "\t\t<wp:author_display_name>%s</wp:author_display_name>\n"
        "\t\t<wp:author_first_name>%s</wp:author_first_name>\n"
        "\t\t<wp:author_last_name>%s</wp:author_last_name>\n"
        "\t</wp:author>\n"
        "\t<generator>https://github.com/SteerPointMikeL/coalpickoutdoors</generator>\n"
        % (SITE, SITE, SITE, cdata(AUTHOR), cdata("Coal Pick Outdoors"), cdata(""), cdata(""))
    )

    footer = "</channel>\n</rss>\n"
    return header + "\n".join(terms) + "\n" + "\n".join(items) + "\n" + footer

# --------------------------------------------------------------------------
def main():
    os.makedirs(ACF_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(WXR_PATH), exist_ok=True)

    with open(os.path.join(ACF_DIR, "group_page_builder.json"), "w", encoding="utf-8") as f:
        json.dump(build_page_builder_group(), f, indent=4, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(ACF_DIR, "group_theme_settings.json"), "w", encoding="utf-8") as f:
        json.dump(build_theme_settings_group(), f, indent=4, ensure_ascii=False)
        f.write("\n")

    with open(WXR_PATH, "w", encoding="utf-8") as f:
        f.write(build_wxr())

    print("Wrote ACF JSON + WXR")

if __name__ == "__main__":
    main()
