<?php
/**
 * ACF integration: options page + template helpers.
 *
 * @package CoalPickOutdoors
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Register the "Theme Settings" ACF options page.
 */
function cpo_register_options_page() {
	if ( ! function_exists( 'acf_add_options_page' ) ) {
		return;
	}

	acf_add_options_page(
		array(
			'page_title' => __( 'Theme Settings', 'coal-pick-outdoors' ),
			'menu_title' => __( 'Theme Settings', 'coal-pick-outdoors' ),
			'menu_slug'  => 'theme-settings',
			'capability' => 'edit_theme_options',
			'redirect'   => false,
			'post_id'    => 'options',
		)
	);
}
add_action( 'acf/init', 'cpo_register_options_page' );

/**
 * Force this theme's Local JSON field groups to sync into the database
 * whenever the theme is activated.
 *
 * Without this, a field group previously saved to the database (for example
 * by an earlier WXR import attempt, a manual field-group edit, or a prior
 * version of this theme) can silently take precedence over the field group
 * defined in acf-json/, because ACF only lets Local JSON override the
 * database copy when the JSON file's `modified` timestamp is newer than the
 * database copy's. If a stale database copy of "page_sections" exists with
 * an incompatible or missing flexible_content definition, get_field() falls
 * back to returning the raw postmeta value unconverted -- which is exactly
 * the "page_sections field stored as a simple integer" symptom. Force-
 * importing on every theme activation guarantees the JSON files in this
 * theme are always the source of truth.
 */
function cpo_sync_acf_json_on_activation() {
	if ( ! function_exists( 'acf_get_local_json_files' ) || ! function_exists( 'acf_import_field_group' ) ) {
		return;
	}

	$json_files = acf_get_local_json_files();

	foreach ( $json_files as $file ) {
		$json_content = file_get_contents( $file );
		$field_group  = json_decode( $json_content, true );

		if ( empty( $field_group ) || empty( $field_group['key'] ) ) {
			continue;
		}

		acf_import_field_group( $field_group );
	}
}
add_action( 'after_switch_theme', 'cpo_sync_acf_json_on_activation' );

/**
 * Render an ACF link array as an anchor tag. Returns empty string if no URL.
 *
 * @param array|null $link    ACF link field value (url/title/target).
 * @param string     $classes Extra CSS classes for the anchor.
 * @param string     $fallback_title Title to use when the link array has none.
 * @return string
 */
function cpo_render_link( $link, $classes = '', $fallback_title = '' ) {
	if ( empty( $link ) || empty( $link['url'] ) ) {
		return '';
	}

	$url    = $link['url'];
	$title  = ! empty( $link['title'] ) ? $link['title'] : $fallback_title;
	$target = ! empty( $link['target'] ) ? $link['target'] : '';

	$rel = ( '_blank' === $target ) ? ' rel="noopener"' : '';

	return sprintf(
		'<a href="%1$s" class="%2$s"%3$s%4$s>%5$s</a>',
		esc_url( $url ),
		esc_attr( trim( $classes ) ),
		$target ? ' target="' . esc_attr( $target ) . '"' : '',
		$rel,
		esc_html( $title )
	);
}

/**
 * Echo an ACF image array as a responsive <img> using its attachment ID.
 *
 * @param array|int|null $image ACF image field (array return format) or ID.
 * @param string         $size  Registered image size.
 * @param array          $attr  Extra img attributes.
 */
function cpo_image( $image, $size = 'large', $attr = array() ) {
	$attachment_id = 0;

	if ( is_array( $image ) && ! empty( $image['ID'] ) ) {
		$attachment_id = (int) $image['ID'];
	} elseif ( is_numeric( $image ) ) {
		$attachment_id = (int) $image;
	}

	if ( ! $attachment_id ) {
		return;
	}

	echo wp_get_attachment_image( $attachment_id, $size, false, $attr );
}
