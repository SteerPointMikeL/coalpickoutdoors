<?php
/**
 * Flexible layout: Signup / Gravity Form CTA.
 *
 * @package CoalPickOutdoors
 */

$anchor_id = get_sub_field( 'anchor_id' );
$heading   = get_sub_field( 'heading' );
$lead_text = get_sub_field( 'lead_text' );
$form_id   = get_sub_field( 'gravity_form_id' );
$bg_style  = get_sub_field( 'background_style' ); // field | dark.

$section_classes = 'section follow';
if ( 'dark' === $bg_style ) {
	$section_classes .= ' bg-dark';
}
?>
<section class="<?php echo esc_attr( $section_classes ); ?>"<?php echo $anchor_id ? ' id="' . esc_attr( $anchor_id ) . '"' : ''; ?>>
	<div class="wrap narrow center">
		<?php if ( $heading ) : ?>
			<h2 class="section-head light-text"><?php echo esc_html( $heading ); ?></h2>
		<?php endif; ?>

		<?php if ( $lead_text ) : ?>
			<p class="lead light-body"><?php echo esc_html( $lead_text ); ?></p>
		<?php endif; ?>

		<?php
		if ( $form_id && function_exists( 'gravity_form' ) ) {
			gravity_form( (int) $form_id, false, false, false, '', true );
		}
		?>

		<?php
		if ( has_nav_menu( 'social' ) ) {
			wp_nav_menu(
				array(
					'theme_location'  => 'social',
					'container'       => 'div',
					'container_class' => 'social-row',
					'menu_class'      => 'social-menu',
					'depth'           => 1,
					'fallback_cb'     => false,
				)
			);
		}
		?>
	</div>
</section>
