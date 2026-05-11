````markdown name=README.md
# LinkedIn Scraper - Service Provider Discovery Tool

Find LinkedIn professionals offering **Digital Marketing, Content, Social Media, E-commerce, and Influencer** services with **time-based pricing models** (hourly, project-based, retainer, freelance).

## 🎯 Features

✅ **Service Category Detection**
- Digital Marketing (SEO, SEM, PPC, growth marketing)
- Content Services (writing, copywriting, strategy)
- Social Media Management (Instagram, Facebook, TikTok)
- E-commerce Solutions (Shopify, Amazon FBA, dropshipping)
- Influencer Services (marketing, brand ambassadors)

✅ **Time-Based Service Identification**
- Hourly Rate Extraction
- Project-Based Pricing
- Retainer Models
- Freelance Offerings

✅ **Multi-Format Export**
- Excel (.xlsx) with professional formatting
- CSV (.csv) for data analysis
- JSON (.json) for API integration

✅ **Smart Categorization**
- Filter by service type
- Filter by pricing model
- Relevance scoring
- Hourly rate parsing (multiple currencies)

## 📋 Requirements

- Python 3.8+
- Chrome/Chromium browser
- LinkedIn account (for scraping)
- Valid email and password

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/sarthak765/LinkedIn-Scrapper-.git
cd LinkedIn-Scrapper-
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your LinkedIn credentials:
```env
LINKEDIN_EMAIL=your_email@gmail.com
LINKEDIN_PASSWORD=your_password
MAX_PROFILES=50
```

## 💡 Usage

### Basic Usage
```bash
python main.py
```

This will:
1. Scrape LinkedIn profiles with relevant keywords
2. Filter profiles based on service type
3. Extract time-based pricing models
4. Export results to multiple formats
5. Generate summary statistics

### Output Files

All results are saved in the `output/` directory:

```
output/
├── all_relevant_profiles_20250511_101800.xlsx
├── all_relevant_profiles_20250511_101800.csv
├── all_relevant_profiles_20250511_101800.json
├── service_digital_marketing_20250511_101800.xlsx
├── service_content_20250511_101800.xlsx
├── timetype_hourly_20250511_101800.xlsx
├── timetype_project_based_20250511_101800.xlsx
├── summary_report_20250511_101800.txt
└── scraper.log
```

## 📊 Data Structure

Each profile includes:

```json
{
  "name": "John Doe",
  "url": "https://linkedin.com/in/johndoe",
  "headline": "Digital Marketing Expert | SEO Specialist",
  "about": "10+ years in digital marketing...",
  "experience": "Experience section content...",
  "skills": ["SEO", "PPC", "Analytics"],
  "is_relevant": true,
  "relevance_score": 0.85,
  "services": {
    "digital_marketing": {
      "name": "Digital Marketing",
      "confidence": 0.95,
      "matches": 3
    }
  },
  "time_types": ["hourly", "project_based"],
  "hourly_rate": {
    "amount": 50,
    "currency": "USD",
    "original_text": "$50/hr"
  }
}
```

## 🔍 Search Keywords

The scraper searches for profiles mentioning:

**Services:**
- Digital Marketing, SEO, SEM, PPC, Google Ads
- Content writing, copywriting, content strategy
- Social media management, Instagram, TikTok
- E-commerce, Shopify, Amazon FBA, dropshipping
- Influencer marketing, brand ambassadors

**Time Types:**
- Hourly, per hour, $XX/hr
- Project, fixed price, project-based
- Retainer, monthly, recurring, subscription
- Freelance, contract, gig

## 📈 Excel Export Features

Professional formatting with:
- ✨ Colored headers (blue with white text)
- 📏 Auto-adjusted column widths
- 🔲 Borders and cell formatting
- 📋 Wrapped text for better readability

## 🛡️ Security & Best Practices

- Credentials stored in `.env` (never committed)
- Sensitive data ignored via `.gitignore`
- Rate limiting between requests
- Headless browser mode for speed
- Proper error handling and logging

## ⚠️ Limitations & Important Notes

1. **LinkedIn Terms of Service**: Web scraping may violate LinkedIn's ToS. Use responsibly.
2. **Rate Limiting**: Scraper includes delays to avoid detection
3. **Authentication**: Requires valid LinkedIn credentials
4. **Data Accuracy**: Profile information depends on completeness of LinkedIn profiles
5. **Currency Support**: Currently supports USD, EUR, INR, GBP, JPY, CAD, AUD

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Maximum profiles to scrape
SCRAPER_CONFIG['max_profiles'] = 100

# Delay between requests (seconds)
SCRAPER_CONFIG['delay_between_requests'] = 2

# Headless browser mode
LINKEDIN_CONFIG['headless'] = True

# Output directory
OUTPUT_DIR = './output'
```

## 📝 Logging

All activities logged to `scraper.log`:
- Successful scrapes and exports
- Error tracking
- Timing information
- Profile filtering details

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is provided as-is for educational purposes.

## ⚡ Quick Tips

1. **Optimize Search**: Use more specific keywords for targeted results
2. **Adjust Max Profiles**: Increase `MAX_PROFILES` for broader results (slower)
3. **Export Formats**: Use Excel for presentations, JSON for APIs
4. **Rate Extraction**: Profiles must explicitly mention pricing in headline/about
5. **Relevance Score**: Higher scores indicate better matches

## 🐛 Troubleshooting

### Login Failed
- Verify credentials in `.env`
- Check if 2FA is enabled (disable or use app password)
- Try manual login on LinkedIn first

### No Profiles Found
- Check keywords match your requirements
- Increase `MAX_PROFILES` value
- Try broader search terms

### Rate Not Extracted
- Ensure profiles mention pricing explicitly
- Check for currency symbols ($, €, ₹, etc.)
- Look for "hourly", "/hr", "per hour" text

## 📞 Support

For issues or questions:
1. Check the logs: `scraper.log`
2. Review configuration: `config.py`
3. Test with smaller `MAX_PROFILES` first

## 🎉 Success Metrics

After running the scraper, you'll have:
- ✅ Lists of service providers by category
- ✅ Hourly rates extracted and organized
- ✅ Time-based offerings classified
- ✅ Summary statistics and insights
- ✅ Multiple export formats for different uses

---

**Happy Scraping!** 🚀
````
