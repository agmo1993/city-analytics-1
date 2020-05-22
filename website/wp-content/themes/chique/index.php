<?php
/**
 * The main template file
 *
 * This is the most generic template file in a WordPress theme
 * and one of the two required files for a theme (the other being style.css).
 * It is used to display a page when nothing more specific matches a query.
 * E.g., it puts together the home page when no home.php file exists.
 *
 * @link https://codex.wordpress.org/Template_Hierarchy
 *
 * @package Chique
 */

get_header();

$enable = get_theme_mod( 'chique_header_media_option', 'entire-site' ); ?>

		<div id="primary" class="content-area">
			<main id="main" class="site-main">
				<div class="archive-content-wrap">
					<?php
					$post_title = get_theme_mod( 'chique_recent_posts_heading', esc_html__( 'Blog', 'chique' ) );

					if( ( is_home() && is_front_page() ) || ( 'homepage' === $enable && is_home() ) ) :
						if ( '' !== $post_title ) :
						?>
							<div class="section-heading-wrapper">
								<?php if ( '' !== $post_title ) : ?>
									<div class="section-title-wrapper">
										<h2 class="section-title"><?php echo esc_html( $post_title ); ?></h2>
									</div>
								<?php endif; ?>

							</div><!-- .section-heading-wrap -->
						<?php endif; ?>
					<?php endif; ?>

					<?php
					if ( have_posts() ) :

						if ( is_home() && ! is_front_page() ) : ?>
							<header>
								<h1 class="page-title screen-reader-text"><?php single_post_title(); ?></h1>
							</header>

						<?php endif; ?>

						<div class="section-content-wrapper layout-one">
							<?php
							/* Start the Loop */
							while ( have_posts() ) : the_post();

								get_template_part( 'template-parts/content/content', get_post_format() );

							endwhile;
							?>
						</div> <!-- .section-content-wrapper -->

						<?php
						chique_content_nav();

					else :

						get_template_part( 'template-parts/content/content', 'none' );

					endif; ?>
				</div> <!-- .archive-content-wrap -->
			</main><!-- #main -->
		</div><!-- #primary -->
	<?php get_sidebar(); 
get_footer(); ?>
