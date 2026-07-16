<?php
/**
 * Site header.
 *
 * @package CoalPickOutdoors
 */

?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header" id="top">
	<div class="wrap header-inner">
		<?php if ( has_custom_logo() ) : ?>
			<div class="brand brand-logo">
				<?php the_custom_logo(); ?>
			</div>
		<?php else : ?>
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="brand" aria-label="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>">
				<span class="brand-emblem" aria-hidden="true">
					<svg viewBox="0 0 48 48" width="30" height="30" fill="none">
						<path d="M8 40 L40 8 M8 8 L40 40" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
						<path d="M6 42 L14 34 M42 6 L34 14 M42 42 L34 34 M6 6 L14 14" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
						<rect x="18" y="18" width="12" height="12" rx="1.5" fill="currentColor"/>
					</svg>
				</span>
				<span class="brand-word">
					<span class="brand-name"><?php bloginfo( 'name' ); ?></span>
					<?php
					$brand_subtitle = function_exists( 'get_field' ) ? get_field( 'brand_subtitle', 'option' ) : '';
					if ( $brand_subtitle ) :
						?>
						<span class="brand-sub"><?php echo esc_html( $brand_subtitle ); ?></span>
					<?php endif; ?>
				</span>
			</a>
		<?php endif; ?>

		<?php
		if ( has_nav_menu( 'primary' ) ) {
			wp_nav_menu(
				array(
					'theme_location' => 'primary',
					'container'      => 'nav',
					'container_class' => 'site-nav',
					'container_aria_label' => __( 'Primary', 'coal-pick-outdoors' ),
					'menu_class'     => 'primary-menu',
					'depth'          => 1,
					'fallback_cb'    => false,
				)
			);
		}
		?>
	</div>
</header>
