<?php
/**
 * Site footer.
 *
 * @package CoalPickOutdoors
 */

$footer_tagline   = function_exists( 'get_field' ) ? get_field( 'footer_tagline', 'option' ) : '';
$footer_legal     = function_exists( 'get_field' ) ? get_field( 'footer_legal_text', 'option' ) : '';
$footer_secondary = function_exists( 'get_field' ) ? get_field( 'footer_secondary_text', 'option' ) : '';
?>

<footer class="site-footer">
	<div class="wrap footer-inner">
		<div class="footer-brand">
			<span class="brand-name"><?php bloginfo( 'name' ); ?></span>
			<?php if ( $footer_tagline ) : ?>
				<p><?php echo esc_html( $footer_tagline ); ?></p>
			<?php endif; ?>
		</div>

		<?php
		if ( has_nav_menu( 'footer' ) ) {
			wp_nav_menu(
				array(
					'theme_location'  => 'footer',
					'container'       => 'nav',
					'container_class' => 'footer-nav',
					'container_aria_label' => __( 'Footer', 'coal-pick-outdoors' ),
					'menu_class'      => 'footer-menu',
					'depth'           => 1,
					'fallback_cb'     => false,
				)
			);
		}
		?>
	</div>

	<div class="wrap footer-legal">
		<?php if ( $footer_legal ) : ?>
			<span><?php echo esc_html( $footer_legal ); ?></span>
		<?php endif; ?>
		<?php if ( $footer_secondary ) : ?>
			<span><?php echo esc_html( $footer_secondary ); ?></span>
		<?php endif; ?>
	</div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
