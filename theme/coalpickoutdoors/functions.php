<?php
/**
 * Coal Pick Outdoors — theme bootstrap.
 *
 * @package CoalPickOutdoors
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'CPO_THEME_VERSION', '1.0.0' );
define( 'CPO_THEME_DIR', get_template_directory() );
define( 'CPO_THEME_URI', get_template_directory_uri() );

/**
 * Enqueue front-end styles and scripts.
 */
function cpo_enqueue_assets() {
	// Google Fonts used by the design.
	wp_enqueue_style(
		'cpo-fonts',
		'https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Sora:wght@400;500;600;700;800&display=swap',
		array(),
		null
	);

	// Design CSS (ported from the static mockup).
	wp_enqueue_style(
		'cpo-style',
		CPO_THEME_URI . '/assets/css/style.css',
		array( 'cpo-fonts' ),
		CPO_THEME_VERSION
	);

	// Progressive enhancement: header shadow + scroll reveal.
	wp_enqueue_script(
		'cpo-app',
		CPO_THEME_URI . '/assets/js/app.js',
		array(),
		CPO_THEME_VERSION,
		true
	);
}
add_action( 'wp_enqueue_scripts', 'cpo_enqueue_assets' );

require_once CPO_THEME_DIR . '/inc/setup.php';
require_once CPO_THEME_DIR . '/inc/acf.php';
