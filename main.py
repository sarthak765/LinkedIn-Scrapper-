"""
Main Pipeline Module
Orchestrates the complete scraping, filtering, and exporting workflow
"""

import logging
import sys
from typing import List
from linkedin_scraper import LinkedInScraper
from service_filter import ServiceFilter
from data_exporter import DataExporter
from config import LINKEDIN_SEARCH_KEYWORDS, SCRAPER_CONFIG, LOGGING_CONFIG
import os
from dotenv import load_dotenv

# Setup logging
load_dotenv()
logging.basicConfig(
    level=LOGGING_CONFIG['log_level'],
    format=LOGGING_CONFIG['format'],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['log_file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LinkedInScraperPipeline:
    """Complete pipeline for scraping, filtering, and exporting profiles"""
    
    def __init__(self):
        self.scraper = None
        self.filter = ServiceFilter()
        self.exporter = DataExporter()
    
    def run(self, 
            keywords: List[str] = None,
            max_profiles_per_keyword: int = None,
            export_formats: List[str] = None,
            group_by: str = None) -> dict:
        """
        Run the complete scraping pipeline
        
        Args:
            keywords: Custom keywords to search (uses config default if None)
            max_profiles_per_keyword: Max profiles per keyword
            export_formats: Export formats (excel, csv, json)
            group_by: Group results by 'category', 'service_type', or None
            
        Returns:
            Dictionary with results summary
        """
        logger.info("=" * 60)
        logger.info("Starting LinkedIn Scraper Pipeline")
        logger.info("=" * 60)
        
        try:
            # Use defaults if not provided
            if keywords is None:
                keywords = LINKEDIN_SEARCH_KEYWORDS
            
            if max_profiles_per_keyword is None:
                max_profiles_per_keyword = SCRAPER_CONFIG['max_profiles']
            
            if export_formats is None:
                export_formats = ['excel', 'csv', 'json']
            
            # Step 1: Initialize and login
            logger.info("\nStep 1: Initializing LinkedIn Scraper...")
            self.scraper = LinkedInScraper(
                headless=SCRAPER_CONFIG['headless_mode'],
                timeout=SCRAPER_CONFIG['timeout']
            )
            self.scraper.initialize_driver()
            
            if not self.scraper.login():
                logger.error("Failed to login to LinkedIn")
                return {'status': 'failed', 'message': 'Login failed'}
            
            # Step 2: Scrape profiles
            logger.info("\nStep 2: Scraping LinkedIn profiles...")
            profiles = self.scraper.search_profiles(
                keywords=keywords,
                max_profiles=max_profiles_per_keyword
            )
            logger.info(f"Scraped {len(profiles)} profiles")
            
            if not profiles:
                logger.warning("No profiles scraped")
                return {'status': 'completed', 'message': 'No profiles found', 'profiles_count': 0}
            
            # Step 3: Filter profiles
            logger.info("\nStep 3: Filtering and categorizing profiles...")
            filtered_profiles = self.filter.filter_profiles_batch(profiles)
            logger.info(f"Filtered to {len(filtered_profiles)} relevant profiles")
            
            if not filtered_profiles:
                logger.warning("No relevant profiles found after filtering")
                return {'status': 'completed', 'message': 'No relevant profiles', 'profiles_count': 0}
            
            # Step 4: Export results
            logger.info("\nStep 4: Exporting results...")
            exported_files = self.exporter.export_profiles(
                filtered_profiles,
                formats=export_formats,
                group_by=group_by
            )
            logger.info(f"Exported {len(exported_files)} files")
            
            # Step 5: Generate summary
            logger.info("\nStep 5: Generating summary report...")
            summary_file = self.exporter.generate_summary_report(filtered_profiles)
            if summary_file:
                exported_files.append(summary_file)
            
            # Print summary
            self._print_summary(filtered_profiles)
            
            return {
                'status': 'completed',
                'profiles_scraped': len(profiles),
                'profiles_filtered': len(filtered_profiles),
                'files_exported': len(exported_files),
                'exported_files': exported_files
            }
            
        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}", exc_info=True)
            return {'status': 'failed', 'message': str(e)}
        
        finally:
            # Cleanup
            if self.scraper:
                self.scraper.close()
            logger.info("\nPipeline completed")
            logger.info("=" * 60)
    
    def _print_summary(self, profiles: List[dict]):
        """Print summary statistics"""
        logger.info("\n" + "=" * 60)
        logger.info("SUMMARY")
        logger.info("=" * 60)
        
        logger.info(f"\nTotal Profiles: {len(profiles)}")
        
        # By service category
        service_counts = {}
        for profile in profiles:
            for service_key in profile.get('services', {}).keys():
                service_counts[service_key] = service_counts.get(service_key, 0) + 1
        
        if service_counts:
            logger.info("\nProfiles by Service Category:")
            for service_key, count in sorted(service_counts.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  • {service_key.replace('_', ' ').title()}: {count}")
        
        # By service type
        timetype_counts = {}
        for profile in profiles:
            for time_type in profile.get('time_types', []):
                timetype_counts[time_type] = timetype_counts.get(time_type, 0) + 1
        
        if timetype_counts:
            logger.info("\nProfiles by Service Type:")
            for time_type, count in sorted(timetype_counts.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  • {time_type.replace('_', ' ').title()}: {count}")
        
        # Hourly rates
        hourly_profiles = [p for p in profiles if p.get('hourly_rate')]
        logger.info(f"\nProfiles with Hourly Rates: {len(hourly_profiles)}")
        
        if hourly_profiles:
            rates = [p['hourly_rate']['amount'] for p in hourly_profiles if p.get('hourly_rate', {}).get('amount')]
            if rates:
                logger.info(f"  • Average Rate: ${sum(rates)/len(rates):.2f}")
                logger.info(f"  • Min Rate: ${min(rates):.2f}")
                logger.info(f"  • Max Rate: ${max(rates):.2f}")
        
        logger.info("\n" + "=" * 60)


def main():
    """Main entry point"""
    pipeline = LinkedInScraperPipeline()
    
    result = pipeline.run(
        keywords=LINKEDIN_SEARCH_KEYWORDS,
        max_profiles_per_keyword=SCRAPER_CONFIG['max_profiles'],
        export_formats=['excel', 'csv', 'json'],
        group_by='category'  # or 'service_type' or None
    )
    
    logger.info(f"\nFinal Result: {result}")


if __name__ == "__main__":
    main()
