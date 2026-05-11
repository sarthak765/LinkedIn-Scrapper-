"""
Configuration file for LinkedIn Scraper
Defines service categories, keywords, and scraper settings
"""

# Service Categories and Keywords
SERVICE_CATEGORIES = {
    "digital_marketing": {
        "name": "Digital Marketing",
        "keywords": [
            "digital marketing", "digital marketer",
            "SEO specialist", "SEM expert",
            "PPC manager", "google ads",
            "growth marketing", "marketing consultant",
            "conversion optimization", "marketing strategist"
        ]
    },
    "content_writing": {
        "name": "Content & Writing",
        "keywords": [
            "content writer", "content writing",
            "copywriter", "copywriting",
            "blog writer", "technical writer",
            "content strategist", "content strategy",
            "content creator", "ghostwriter"
        ]
    },
    "social_media": {
        "name": "Social Media Management",
        "keywords": [
            "social media manager", "social media management",
            "instagram manager", "facebook manager",
            "tiktok creator", "community manager",
            "social media strategist", "social media specialist",
            "content calendar", "social media growth"
        ]
    },
    "ecommerce": {
        "name": "E-commerce",
        "keywords": [
            "shopify expert", "shopify store",
            "amazon fba", "amazon seller",
            "dropshipping", "ecommerce",
            "store management", "product listing",
            "inventory management", "ecommerce consultant"
        ]
    },
    "influencer": {
        "name": "Influencer Marketing",
        "keywords": [
            "influencer", "influencer marketing",
            "brand ambassador", "content creator",
            "micro influencer", "influencer partnership",
            "influencer campaign", "brand collaboration"
        ]
    }
}

# Time-Based Service Keywords
TIME_BASED_KEYWORDS = {
    "hourly": {
        "name": "Hourly Rate",
        "keywords": ["hourly", "per hour", "/hr", "per hr", "$/hr", "€/hr", "£/hr", "₹/hr"]
    },
    "project_based": {
        "name": "Project-Based",
        "keywords": ["project", "fixed price", "project-based", "fixed-price", "one-time"]
    },
    "retainer": {
        "name": "Retainer/Monthly",
        "keywords": ["retainer", "monthly", "/month", "recurring", "subscription", "per month"]
    },
    "freelance": {
        "name": "Freelance",
        "keywords": ["freelance", "freelancer", "contract", "gig", "available for hire"]
    }
}

# Currency Patterns
CURRENCY_PATTERNS = {
    "USD": ["$", "USD"],
    "EUR": ["€", "EUR"],
    "GBP": ["£", "GBP"],
    "INR": ["₹", "INR"],
    "JPY": ["¥", "JPY"],
    "CAD": ["CAD", "C$"],
    "AUD": ["AUD", "A$"]
}

# Scraper Configuration
SCRAPER_CONFIG = {
    "max_profiles": 50,
    "headless_mode": True,
    "scroll_pause_time": 1,
    "delay_between_requests": 2,
    "timeout": 30,
    "retries": 3
}

# LinkedIn Configuration
LINKEDIN_CONFIG = {
    "base_url": "https://www.linkedin.com",
    "search_url": "https://www.linkedin.com/search/results/people/",
    "headless": True,
    "window_size": "1920,1080"
}

# Output Configuration
OUTPUT_CONFIG = {
    "output_directory": "./output",
    "export_formats": ["excel", "csv", "json"],
    "timestamp_format": "%Y%m%d_%H%M%S",
    "excel_sheet_name": "Profiles"
}

# Excel Formatting
EXCEL_FORMAT = {
    "header_bg_color": "1F4E78",  # Dark blue
    "header_font_color": "FFFFFF",  # White
    "header_font_bold": True,
    "border_style": "thin",
    "auto_adjust_columns": True,
    "wrap_text": True
}

# Logging Configuration
LOGGING_CONFIG = {
    "log_file": "scraper.log",
    "log_level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# Search Keywords for LinkedIn
LINKEDIN_SEARCH_KEYWORDS = [
    "digital marketing",
    "content writer",
    "social media manager",
    "shopify expert",
    "influencer marketing",
    "SEO specialist",
    "copywriter",
    "freelance consultant",
    "ecommerce specialist",
    "marketing consultant"
]
