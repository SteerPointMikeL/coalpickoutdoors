<?php
/**
 * Flexible layout: Hero.
 *
 * @package CoalPickOutdoors
 */

$eyebrow      = get_sub_field( 'hero_eyebrow' );
$heading      = get_sub_field( 'hero_heading' );
$highlight    = get_sub_field( 'hero_heading_highlight' );
$subheading   = get_sub_field( 'hero_subheading' );
$primary_cta  = get_sub_field( 'primary_cta' );
$secondary    = get_sub_field( 'secondary_cta' );
$background    = get_sub_field( 'background_image' );
?>
<section class="hero">
	<div class="hero-media">
		<?php cpo_image( $background, 'cpo-hero', array( 'class' => 'hero-bg' ) ); ?>
		<div class="hero-scrim"></div>
	</div>
	<div class="wrap hero-content">
		<?php if ( $eyebrow ) : ?>
			<p class="eyebrow"><?php echo esc_html( $eyebrow ); ?></p>
		<?php endif; ?>

		<?php if ( $heading || $highlight ) : ?>
			<h1 class="hero-title"><?php echo esc_html( $heading ); ?><?php echo $highlight ? ' <em>' . esc_html( $highlight ) . '</em>' : ''; ?></h1>
		<?php endif; ?>

		<?php if ( $subheading ) : ?>
			<p class="hero-sub"><?php echo esc_html( $subheading ); ?></p>
		<?php endif; ?>

		<?php if ( ! empty( $primary_cta['url'] ) || ! empty( $secondary['url'] ) ) : ?>
			<div class="hero-cta">
				<?php
				echo cpo_render_link( $primary_cta, 'btn btn-accent' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
				echo cpo_render_link( $secondary, 'btn btn-ghost' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
				?>
			</div>
		<?php endif; ?>
	</div>

	<?php if ( have_rows( 'stats' ) ) : ?>
		<div class="hero-stats wrap">
			<?php
			while ( have_rows( 'stats' ) ) :
				the_row();
				$stat_number = get_sub_field( 'stat_number' );
				$stat_label  = get_sub_field( 'stat_label' );
				?>
				<div class="hstat">
					<span class="hstat-num"><?php echo esc_html( $stat_number ); ?></span>
					<span class="hstat-label"><?php echo esc_html( $stat_label ); ?></span>
				</div>
			<?php endwhile; ?>
		</div>
	<?php endif; ?>
</section>
