<?php
/**
 * Flexible layout: Story / Text Band.
 *
 * @package CoalPickOutdoors
 */

$anchor_id = get_sub_field( 'anchor_id' );
$eyebrow   = get_sub_field( 'eyebrow' );
$heading   = get_sub_field( 'heading' );
$lead_text = get_sub_field( 'lead_text' );
$body_text = get_sub_field( 'body_text' );
$cta       = get_sub_field( 'cta' );
?>
<section class="section story"<?php echo $anchor_id ? ' id="' . esc_attr( $anchor_id ) . '"' : ''; ?>>
	<div class="wrap narrow">
		<?php if ( $eyebrow ) : ?>
			<p class="section-label"><?php echo esc_html( $eyebrow ); ?></p>
		<?php endif; ?>

		<?php if ( $heading ) : ?>
			<h2 class="section-head"><?php echo nl2br( esc_html( $heading ) ); ?></h2>
		<?php endif; ?>

		<?php if ( $lead_text ) : ?>
			<p class="lead"><?php echo esc_html( $lead_text ); ?></p>
		<?php endif; ?>

		<?php if ( $body_text ) : ?>
			<div class="body"><?php echo wp_kses_post( $body_text ); ?></div>
		<?php endif; ?>

		<?php echo cpo_render_link( $cta, 'btn btn-ghost small' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
	</div>
</section>
