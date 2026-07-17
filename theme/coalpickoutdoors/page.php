<?php
/**
 * Generic page template — also renders the ACF flexible-content page builder
 * when a page has `page_sections`, so any page can use the builder.
 *
 * @package CoalPickOutdoors
 */

get_header();

if ( have_posts() ) :
	while ( have_posts() ) :
		the_post();

		if ( function_exists( 'have_rows' ) && have_rows( 'page_sections' ) ) :
			while ( have_rows( 'page_sections' ) ) :
				the_row();

				$layout = get_row_layout();
				$slug   = str_replace( '_', '-', $layout );

				get_template_part( 'template-parts/flexible/' . $slug, null, array( 'layout' => $layout ) );
			endwhile;
		else :
			?>
			<main class="section">
				<div class="wrap narrow">
					<h1 class="section-head"><?php the_title(); ?></h1>
					<div class="body"><?php the_content(); ?></div>
				</div>
			</main>
			<?php
		endif;

	endwhile;
endif;

get_footer();
