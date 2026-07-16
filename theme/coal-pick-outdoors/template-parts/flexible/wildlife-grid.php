<?php
/**
 * Flexible layout: Wildlife Grid.
 *
 * @package CoalPickOutdoors
 */

$anchor_id = get_sub_field( 'anchor_id' );
$eyebrow   = get_sub_field( 'eyebrow' );
$heading   = get_sub_field( 'heading' );
$highlight = get_sub_field( 'heading_highlight' );
$lead_text = get_sub_field( 'lead_text' );
?>
<section class="section wildlife"<?php echo $anchor_id ? ' id="' . esc_attr( $anchor_id ) . '"' : ''; ?>>
	<div class="wrap">
		<div class="wild-head">
			<?php if ( $eyebrow ) : ?>
				<p class="section-label light"><?php echo esc_html( $eyebrow ); ?></p>
			<?php endif; ?>

			<?php if ( $heading || $highlight ) : ?>
				<h2 class="section-head light-text"><?php echo esc_html( $heading ); ?><?php echo $highlight ? ' ' . esc_html( $highlight ) : ''; ?></h2>
			<?php endif; ?>

			<?php if ( $lead_text ) : ?>
				<p class="lead light-body"><?php echo esc_html( $lead_text ); ?></p>
			<?php endif; ?>
		</div>

		<?php if ( have_rows( 'cards' ) ) : ?>
			<div class="wild-grid">
				<?php
				while ( have_rows( 'cards' ) ) :
					the_row();
					$card_image = get_sub_field( 'image' );
					$name       = get_sub_field( 'name' );
					$sub_label  = get_sub_field( 'sub_label' );
					$featured   = get_sub_field( 'is_featured' );
					$card_class = $featured ? 'wild-card feature' : 'wild-card';
					?>
					<article class="<?php echo esc_attr( $card_class ); ?>">
						<?php cpo_image( $card_image, 'cpo-card' ); ?>
						<div class="wild-tag">
							<span class="wild-name"><?php echo esc_html( $name ); ?></span>
							<span class="wild-sub"><?php echo esc_html( $sub_label ); ?></span>
						</div>
					</article>
				<?php endwhile; ?>
			</div>
		<?php endif; ?>

		<?php if ( have_rows( 'species_tags' ) ) : ?>
			<ul class="species-strip">
				<?php
				while ( have_rows( 'species_tags' ) ) :
					the_row();
					?>
					<li><?php echo esc_html( get_sub_field( 'tag_text' ) ); ?></li>
				<?php endwhile; ?>
			</ul>
		<?php endif; ?>
	</div>
</section>
