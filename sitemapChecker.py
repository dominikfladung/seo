from SEOHelper import SEOHelper
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sitemap", help="Crawl a sitemap.xml")
    parser.add_argument("--check-headings", help="Check for headings", action="store_true")
    args = parser.parse_args()
    
    seoHelper = SEOHelper(args)

    if args.sitemap:
        seoHelper.crawlSitemap(args.sitemap)

if __name__ == "__main__":
    main()
    