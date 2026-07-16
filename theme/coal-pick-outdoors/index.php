<?php
/**
 * Fallback template.
 *
 * @package CoalPickOutdoors
 */

get_header();

if ( have_posts() ) :
	?>
	<main class="section">
		<div class="wrap">
			<?php
			while ( have_posts() ) :
				the_post();
				?>
				<article <?php post_class(); ?>>
					<h2 class="section-head"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
					<div class="body"><?php the_excerpt(); ?></div>
				</article>
				<?php
			endwhile;

			the_posts_pagination();
			?>
		</div>
	</main>
	<?php
endif;

get_footer();
