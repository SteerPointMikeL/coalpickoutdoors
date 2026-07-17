<?php
/**
 * Flexible layout: Image + Content (used for "The Land" and "Meet Sydney").
 *
 * @package CoalPickOutdoors
 */

$anchor_id  = get_sub_field( 'anchor_id' );
$eyebrow    = get_sub_field( 'eyebrow' );
$heading    = get_sub_field( 'heading' );
$highlight  = get_sub_field( 'heading_highlight' );
$lead_text  = get_sub_field( 'lead_text' );
$body_text  = get_sub_field( 'body_text' );
$image      = get_sub_field( 'image' );
$caption    = get_sub_field( 'image_caption' );
$image_pos  = get_sub_field( 'image_position' ); // left | right.
$bg_style   = get_sub_field( 'background_style' ); // cream | sand.
$cta        = get_sub_field( 'cta' );

$section_classes = 'section image-content';
if ( 'sand' === $bg_style ) {
	$section_classes .= ' bg-sand';
}

$grid_classes = 'wrap land-grid';
if ( 'left' === $image_pos ) {
	$grid_classes .= ' image-left';
}

$figure = '';
ob_start();
?>
<figure class="land-figure">
	<?php cpo_image( $image, 'large' ); ?>
	<?php if ( $caption ) : ?>
		<figcaption><?php echo esc_html( $caption ); ?></figcaption>
	<?php endif; ?>
</figure>
<?php
$figure = ob_get_clean();

$copy = '';
ob_start();
?>
<div class="land-copy">
	<?php if ( $eyebrow ) : ?>
		<p class="section-label"><?php echo esc_html( $eyebrow ); ?></p>
	<?php endif; ?>

	<?php if ( $heading || $highlight ) : ?>
		<h2 class="section-head"><?php echo esc_html( $heading ); ?><?php echo $highlight ? ' <em>' . esc_html( $highlight ) . '</em>' : ''; ?></h2>
	<?php endif; ?>

	<?php if ( $lead_text ) : ?>
		<p class="lead"><?php echo esc_html( $lead_text ); ?></p>
	<?php endif; ?>

	<?php if ( $body_text ) : ?>
		<div class="body"><?php echo wp_kses_post( $body_text ); ?></div>
	<?php endif; ?>

	<?php if ( have_rows( 'bullet_list' ) ) : ?>
		<ul class="land-list">
			<?php
			while ( have_rows( 'bullet_list' ) ) :
				the_row();
				?>
				<li><span><?php echo esc_html( get_sub_field( 'item_text' ) ); ?></span></li>
			<?php endwhile; ?>
		</ul>
	<?php endif; ?>

	<?php echo cpo_render_link( $cta, 'btn btn-accent' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
</div>
<?php
$copy = ob_get_clean();
?>
<section class="<?php echo esc_attr( $section_classes ); ?>"<?php echo $anchor_id ? ' id="' . esc_attr( $anchor_id ) . '"' : ''; ?>>
	<div class="<?php echo esc_attr( $grid_classes ); ?>">
		<?php
		if ( 'left' === $image_pos ) {
			echo $figure; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
			echo $copy;   // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		} else {
			echo $copy;   // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
			echo $figure; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		}
		?>
	</div>
</section>
