<?php
/**
 * Theme setup: supports, menus, image sizes, ACF Local JSON points.
 *
 * @package CoalPickOutdoors
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Register theme supports and nav menu locations.
 */
function cpo_theme_setup() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
	add_theme_support(
		'custom-logo',
		array(
			'height'      => 92,
			'width'       => 92,
			'flex-height' => true,
			'flex-width'  => true,
		)
	);

	register_nav_menus(
		array(
			'primary' => __( 'Primary Menu', 'coal-pick-outdoors' ),
			'footer'  => __( 'Footer Menu', 'coal-pick-outdoors' ),
			'social'  => __( 'Social Menu', 'coal-pick-outdoors' ),
		)
	);
}
add_action( 'after_setup_theme', 'cpo_theme_setup' );

/**
 * Custom image sizes used by the layouts.
 */
function cpo_image_sizes() {
	add_image_size( 'cpo-hero', 2000, 1200, true );
	add_image_size( 'cpo-card', 900, 1125, true );
	add_image_size( 'cpo-episode', 900, 563, true );
}
add_action( 'after_setup_theme', 'cpo_image_sizes' );

/**
 * Tell ACF to load field groups from the theme's acf-json folder.
 *
 * @param array $paths Existing load paths.
 * @return array
 */
function cpo_acf_json_load_point( $paths ) {
	$paths[] = CPO_THEME_DIR . '/acf-json';
	return $paths;
}
add_filter( 'acf/settings/load_json', 'cpo_acf_json_load_point' );

/**
 * Save ACF field group changes back into the theme's acf-json folder.
 *
 * @param string $path Default save path.
 * @return string
 */
function cpo_acf_json_save_point( $path ) {
	return CPO_THEME_DIR . '/acf-json';
}
add_filter( 'acf/settings/save_json', 'cpo_acf_json_save_point' );
