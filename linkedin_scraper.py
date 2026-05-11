"""
LinkedIn Scraper Module
Uses Selenium to scrape LinkedIn profiles
"""

import logging
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class LinkedInScraper:
    """Scraper for LinkedIn profiles using Selenium"""
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        """
        Initialize LinkedIn scraper
        
        Args:
            headless: Run browser in headless mode
            timeout: Timeout for operations in seconds
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.email = os.getenv('LINKEDIN_EMAIL')
        self.password = os.getenv('LINKEDIN_PASSWORD')
    
    def initialize_driver(self):
        """Initialize Selenium WebDriver"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing WebDriver: {str(e)}")
            raise
    
    def login(self) -> bool:
        """
        Login to LinkedIn
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            if not self.email or not self.password:
                logger.error("LinkedIn credentials not found in .env file")
                return False
            
            logger.info("Logging into LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for email input
            email_input = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_input.send_keys(self.email)
            
            # Password input
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(self.password)
            
            # Submit login
            login_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Sign in']")
            login_button.click()
            
            # Wait for homepage to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "global-nav"))
            )
            
            logger.info("Successfully logged in to LinkedIn")
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False
    
    def search_profiles(self, keywords: List[str], max_profiles: int = 50) -> List[Dict]:
        """
        Search for profiles on LinkedIn
        
        Args:
            keywords: List of search keywords
            max_profiles: Maximum profiles to scrape per keyword
            
        Returns:
            List of profile data
        """
        profiles = []
        
        for keyword in keywords:
            logger.info(f"Searching for: {keyword}")
            keyword_profiles = self._search_keyword(keyword, max_profiles)
            profiles.extend(keyword_profiles)
            time.sleep(2)  # Delay between searches
        
        return profiles
    
    def _search_keyword(self, keyword: str, max_profiles: int) -> List[Dict]:
        """Search profiles for a specific keyword"""
        profiles = []
        
        try:
            # Build search URL
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={keyword}"
            self.driver.get(search_url)
            
            # Wait for profiles to load
            time.sleep(3)
            
            # Scroll to load more profiles
            profiles_loaded = 0
            while profiles_loaded < max_profiles:
                try:
                    profile_elements = self.driver.find_elements(By.CLASS_NAME, "base-card")
                    
                    for element in profile_elements[profiles_loaded:]:
                        if profiles_loaded >= max_profiles:
                            break
                        
                        try:
                            profile_data = self._extract_profile_data(element)
                            if profile_data:
                                profiles.append(profile_data)
                                profiles_loaded += 1
                        except Exception as e:
                            logger.warning(f"Error extracting profile: {str(e)}")
                            continue
                    
                    # Scroll down to load more
                    self.driver.execute_script("window.scrollBy(0, 300);")
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"Error during scroll: {str(e)}")
                    break
            
            logger.info(f"Found {len(profiles)} profiles for keyword: {keyword}")
            
        except Exception as e:
            logger.error(f"Error searching for keyword {keyword}: {str(e)}")
        
        return profiles
    
    def _extract_profile_data(self, element) -> Dict:
        """Extract profile data from a profile element"""
        try:
            profile = {}
            
            # Extract name
            name_element = element.find_element(By.CLASS_NAME, "base-search-card__title")
            profile['name'] = name_element.text.strip()
            
            # Extract headline
            headline_element = element.find_element(By.CLASS_NAME, "base-search-card__subtitle")
            profile['headline'] = headline_element.text.strip()
            
            # Extract URL
            link_element = element.find_element(By.CLASS_NAME, "base-card__full-link")
            profile['url'] = link_element.get_attribute('href')
            
            # Extract location if available
            try:
                location_element = element.find_element(By.CLASS_NAME, "base-search-card__metadata")
                profile['location'] = location_element.text.strip()
            except:
                profile['location'] = None
            
            # Click on profile to get more details (optional - can be skipped for speed)
            profile['about'] = None
            profile['experience'] = None
            profile['skills'] = []
            
            return profile
            
        except Exception as e:
            logger.error(f"Error extracting profile data: {str(e)}")
            return None
    
    def get_profile_details(self, profile_url: str) -> Dict:
        """
        Get detailed information from a profile
        
        Args:
            profile_url: LinkedIn profile URL
            
        Returns:
            Detailed profile information
        """
        try:
            self.driver.get(profile_url)
            time.sleep(2)
            
            profile = {'url': profile_url}
            
            # Extract name
            try:
                name = self.driver.find_element(By.CLASS_NAME, "text-heading-xlarge").text
                profile['name'] = name
            except:
                pass
            
            # Extract headline
            try:
                headline = self.driver.find_element(By.CLASS_NAME, "text-body-medium").text
                profile['headline'] = headline
            except:
                pass
            
            # Extract about
            try:
                about = self.driver.find_element(By.ID, "about").text
                profile['about'] = about
            except:
                pass
            
            # Extract skills
            try:
                skills_elements = self.driver.find_elements(By.CLASS_NAME, "skill-category-entity__name")
                profile['skills'] = [skill.text for skill in skills_elements]
            except:
                profile['skills'] = []
            
            return profile
            
        except Exception as e:
            logger.error(f"Error getting profile details: {str(e)}")
            return {'url': profile_url}
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
    
    def __enter__(self):
        """Context manager entry"""
        self.initialize_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
