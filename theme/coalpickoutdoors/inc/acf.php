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
