from SEOHelper import SEOHelper
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sitemap", help="Crawl a sitemap.xml")
    parser.add_argument("--url", help="Check a specific url")
    parser.add_argument("--check-headings", help="Check for headings", action="store_true")
    parser.add_argument("--only-errors", help="Display only the errors", action="store_true")
    args = parser.parse_args()
    
    seoHelper = SEOHelper(args)
    
    if args.sitemap:
        seoHelper.crawlSitemap(args.sitemap)
    elif args.url:
        seoHelper.checkURL(args.url)

if __name__ == "__main__":
    main()
    