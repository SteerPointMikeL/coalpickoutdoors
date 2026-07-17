<?php
/**
 * Front page — renders the ACF flexible-content page builder.
 *
 * All section content comes from the `page_sections` flexible content field.
 * This loop contains no copy; each layout is delegated to a template part.
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
		endif;

	endwhile;
endif;

get_footer();
