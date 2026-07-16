<?php
/**
 * Flexible layout: Series / Episodes.
 *
 * @package CoalPickOutdoors
 */

$anchor_id     = get_sub_field( 'anchor_id' );
$eyebrow       = get_sub_field( 'eyebrow' );
$heading       = get_sub_field( 'heading' );
$highlight     = get_sub_field( 'heading_highlight' );
$lead_text     = get_sub_field( 'lead_text' );
$view_all_link = get_sub_field( 'view_all_link' );
?>
<section class="section series"<?php echo $anchor_id ? ' id="' . esc_attr( $anchor_id ) . '"' : ''; ?>>
	<div class="wrap">
		<div class="series-head">
			<div>
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
			<?php echo cpo_render_link( $view_all_link, 'btn btn-ghost light small' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
		</div>

		<?php if ( have_rows( 'episodes' ) ) : ?>
			<div class="ep-row">
				<?php
				while ( have_rows( 'episodes' ) ) :
					the_row();
					$ep_image    = get_sub_field( 'image' );
					$badge_label = get_sub_field( 'badge_label' );
					$ep_title    = get_sub_field( 'title' );
					$ep_desc     = get_sub_field( 'description' );
					$ep_meta     = get_sub_field( 'meta_text' );
					$duration    = get_sub_field( 'duration_label' );
					$ep_link     = get_sub_field( 'episode_link' );

					// "Featured" and "Next Up" get the highlighted badge style.
					$badge_class = 'ep-badge';
					if ( in_array( strtolower( (string) $badge_label ), array( 'featured', 'next up' ), true ) ) {
						$badge_class .= ' next';
					}
					?>
					<article class="ep-card">
						<div class="ep-thumb">
							<?php cpo_image( $ep_image, 'cpo-episode' ); ?>
							<?php if ( $duration ) : ?>
								<span class="ep-dur"><?php echo esc_html( $duration ); ?></span>
							<?php endif; ?>
							<span class="ep-play" aria-hidden="true">&#9654;</span>
						</div>
						<div class="ep-body">
							<?php if ( $badge_label ) : ?>
								<span class="<?php echo esc_attr( $badge_class ); ?>"><?php echo esc_html( $badge_label ); ?></span>
							<?php endif; ?>
							<?php if ( $ep_title ) : ?>
								<h3>
									<?php if ( ! empty( $ep_link['url'] ) ) : ?>
										<a href="<?php echo esc_url( $ep_link['url'] ); ?>"<?php echo ! empty( $ep_link['target'] ) ? ' target="' . esc_attr( $ep_link['target'] ) . '" rel="noopener"' : ''; ?>><?php echo esc_html( $ep_title ); ?></a>
									<?php else : ?>
										<?php echo esc_html( $ep_title ); ?>
									<?php endif; ?>
								</h3>
							<?php endif; ?>
							<?php if ( $ep_desc ) : ?>
								<p><?php echo esc_html( $ep_desc ); ?></p>
							<?php endif; ?>
							<?php if ( $ep_meta ) : ?>
								<span class="ep-meta"><?php echo esc_html( $ep_meta ); ?></span>
							<?php endif; ?>
						</div>
					</article>
				<?php endwhile; ?>
			</div>
		<?php endif; ?>
	</div>
</section>
