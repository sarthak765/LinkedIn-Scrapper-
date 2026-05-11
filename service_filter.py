"""
Service Filter Module
Filters and categorizes LinkedIn profiles based on services and pricing models
"""

import re
import logging
from typing import Dict, List, Tuple
from config import SERVICE_CATEGORIES, TIME_BASED_KEYWORDS, CURRENCY_PATTERNS

logger = logging.getLogger(__name__)


class ServiceFilter:
    """Filter and categorize profiles based on services and pricing"""
    
    def __init__(self):
        self.service_categories = SERVICE_CATEGORIES
        self.time_keywords = TIME_BASED_KEYWORDS
        self.currencies = CURRENCY_PATTERNS
    
    def filter_profile(self, profile: Dict) -> Dict:
        """
        Filter and enhance a profile with service and pricing information
        
        Args:
            profile: Profile dictionary with name, headline, about, etc.
            
        Returns:
            Enhanced profile with service and time-based information
        """
        try:
            profile_text = self._get_profile_text(profile)
            
            # Detect services
            services = self._detect_services(profile_text)
            profile['services'] = services
            profile['is_relevant'] = len(services) > 0
            
            # Calculate relevance score
            profile['relevance_score'] = self._calculate_relevance_score(services)
            
            # Detect time-based services
            time_types = self._detect_time_types(profile_text)
            profile['time_types'] = time_types
            
            # Extract hourly rate if available
            hourly_rate = self._extract_hourly_rate(profile_text)
            profile['hourly_rate'] = hourly_rate
            
            return profile
        except Exception as e:
            logger.error(f"Error filtering profile: {str(e)}")
            return profile
    
    def _get_profile_text(self, profile: Dict) -> str:
        """Extract and combine all text from profile"""
        text_parts = []
        
        if 'headline' in profile:
            text_parts.append(str(profile.get('headline', '')))
        if 'about' in profile:
            text_parts.append(str(profile.get('about', '')))
        if 'experience' in profile:
            text_parts.append(str(profile.get('experience', '')))
        if 'skills' in profile and isinstance(profile['skills'], list):
            text_parts.append(' '.join(profile['skills']))
        
        return ' '.join(text_parts).lower()
    
    def _detect_services(self, profile_text: str) -> Dict:
        """
        Detect services offered in profile text
        
        Returns:
            Dictionary with service categories and confidence scores
        """
        services = {}
        
        for category_key, category_data in self.service_categories.items():
            matches = 0
            for keyword in category_data['keywords']:
                if keyword.lower() in profile_text:
                    matches += 1
            
            if matches > 0:
                # Calculate confidence based on number of matches
                confidence = min(0.5 + (matches * 0.1), 1.0)
                services[category_key] = {
                    'name': category_data['name'],
                    'confidence': round(confidence, 2),
                    'matches': matches
                }
        
        return services
    
    def _detect_time_types(self, profile_text: str) -> List[str]:
        """
        Detect time-based service types
        
        Returns:
            List of detected time-based service types
        """
        time_types = []
        
        for time_type_key, time_type_data in self.time_keywords.items():
            for keyword in time_type_data['keywords']:
                if keyword.lower() in profile_text:
                    time_types.append(time_type_key)
                    break
        
        return list(set(time_types))  # Remove duplicates
    
    def _extract_hourly_rate(self, profile_text: str) -> Dict:
        """
        Extract hourly rate and currency from profile text
        
        Returns:
            Dictionary with amount, currency, and original text
        """
        hourly_rate = {
            'amount': None,
            'currency': None,
            'original_text': None
        }
        
        # Pattern to match currency and numbers
        patterns = [
            r'(\$|€|£|₹|¥)(\d+(?:,\d{3})*(?:\.\d+)?)',  # Currency + amount
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:USD|EUR|GBP|INR|JPY|CAD|AUD)',  # Amount + currency code
            r'(\$|€|£|₹|¥)(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:/hr|per hour|hourly)',  # Specific hourly pattern
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, profile_text)
            if matches:
                match = matches[0]
                
                # Extract currency
                currency_symbol = match[0] if isinstance(match[0], str) else match[1]
                for currency_code, symbols in self.currencies.items():
                    if currency_symbol in symbols:
                        hourly_rate['currency'] = currency_code
                        break
                
                # Extract amount
                if isinstance(match[1], str):
                    amount_str = match[1].replace(',', '')
                    try:
                        hourly_rate['amount'] = float(amount_str)
                    except ValueError:
                        pass
                
                # Store original text
                if currency_symbol and hourly_rate['amount']:
                    hourly_rate['original_text'] = f"{currency_symbol}{hourly_rate['amount']}"
                
                if hourly_rate['amount']:
                    break
        
        return hourly_rate if hourly_rate['amount'] else None
    
    def _calculate_relevance_score(self, services: Dict) -> float:
        """
        Calculate overall relevance score for a profile
        
        Args:
            services: Dictionary of detected services
            
        Returns:
            Relevance score between 0 and 1
        """
        if not services:
            return 0.0
        
        # Average confidence scores
        confidences = [s['confidence'] for s in services.values()]
        base_score = sum(confidences) / len(confidences)
        
        # Bonus for multiple services
        service_count_bonus = min(len(services) * 0.05, 0.15)
        
        final_score = min(base_score + service_count_bonus, 1.0)
        return round(final_score, 2)
    
    def filter_profiles_batch(self, profiles: List[Dict]) -> List[Dict]:
        """
        Filter multiple profiles
        
        Args:
            profiles: List of profile dictionaries
            
        Returns:
            List of filtered profiles
        """
        filtered_profiles = []
        
        for profile in profiles:
            filtered_profile = self.filter_profile(profile)
            if filtered_profile.get('is_relevant', False):
                filtered_profiles.append(filtered_profile)
        
        return filtered_profiles
    
    def get_profiles_by_service(self, profiles: List[Dict], service_key: str) -> List[Dict]:
        """
        Get profiles offering a specific service
        
        Args:
            profiles: List of profiles
            service_key: Service category key
            
        Returns:
            Filtered profiles offering the specified service
        """
        return [p for p in profiles if service_key in p.get('services', {})]
    
    def get_profiles_by_time_type(self, profiles: List[Dict], time_type: str) -> List[Dict]:
        """
        Get profiles offering a specific time-based service type
        
        Args:
            profiles: List of profiles
            time_type: Time type key (hourly, project_based, retainer, freelance)
            
        Returns:
            Filtered profiles offering the specified time type
        """
        return [p for p in profiles if time_type in p.get('time_types', [])]
    
    def get_profiles_with_hourly_rates(self, profiles: List[Dict]) -> List[Dict]:
        """Get profiles with extracted hourly rates"""
        return [p for p in profiles if p.get('hourly_rate') and p['hourly_rate'].get('amount')]
    
    def sort_by_relevance(self, profiles: List[Dict], reverse: bool = True) -> List[Dict]:
        """Sort profiles by relevance score"""
        return sorted(profiles, key=lambda p: p.get('relevance_score', 0), reverse=reverse)
    
    def sort_by_hourly_rate(self, profiles: List[Dict], reverse: bool = False) -> List[Dict]:
        """Sort profiles by hourly rate"""
        def get_rate(profile):
            if profile.get('hourly_rate') and profile['hourly_rate'].get('amount'):
                return profile['hourly_rate']['amount']
            return 0
        
        return sorted(profiles, key=get_rate, reverse=reverse)
