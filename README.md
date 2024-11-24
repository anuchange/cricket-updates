# Cricket Daily Digest 🏏

An automated cricket newsletter service that scrapes live cricket updates from Cricbuzz and delivers curated content directly to your inbox. Perfect for cricket enthusiasts who want to stay updated without visiting multiple websites.

![Cricket Daily Digest Demo](demo.gif)

## 🌟 Features

### 🤖 Automated Web Scraping
- **Live Data from Cricbuzz**: Automated scraping of cricket updates
- **Real-time Processing**: Continuous monitoring of cricket news and updates
- **Content Curation**: Smart filtering and organization of cricket information

### 📰 Daily Updates
- **Latest Cricket News**: Breaking news, team announcements, and player updates
- **Match Summaries**: Detailed match reports and highlights
- **Live Scores**: Real-time match status and scorecards

### 📧 Email Features
- **Personalized Newsletters**: Beautifully formatted HTML emails
- **Match Updates**: Daily match schedules and results
- **News Digests**: Curated cricket news from around the world

### 🛠️ Technical Features
- Built with Flask (Python 3.11)
- Web scraping using Scrapy
- Responsive HTML email templates
- Automated daily email delivery
- Docker containerization for easy deployment

## 🔄 How It Works

1. **Data Collection**
   - Scrapes cricket updates from Cricbuzz
   - Monitors live matches and news sections
   - Collects detailed match statistics

2. **Processing**
   - Filters relevant information
   - Structures data for email format
   - Generates readable summaries

3. **Delivery**
   - Formats content into HTML emails
   - Schedules and sends daily digests
   - Handles subscriber management

## 🚀 Potential Extensions and Use Cases

### 💡 Similar Applications

1. **Industry-Specific News Aggregators**
   - **Tech News Digest**: Scraping from tech blogs and news sites
   - **Financial Markets Daily**: Stock market summaries and financial news
   - **Healthcare Updates**: Medical research and healthcare industry news
   - **Academic Research Digest**: Latest papers and research findings

2. **Content Summarization Services**
   - **Blog Post Summaries**: Key points from lengthy articles
   - **Research Paper Abstracts**: Simplified academic content
   - **News Roundups**: Multi-source news compilation
   - **Industry Reports**: Business intelligence summaries

3. **Vertical-Specific Applications**
   - **Recipe Collections**: Daily cooking inspiration
   - **Job Listings**: Curated job opportunities
   - **Real Estate Updates**: Property listings and market trends
   - **Movie/TV Show Reviews**: Entertainment summaries

## 🎯 Future Roadmap

### Planned Features
- Multiple news source integration
- Custom topic filtering
- Multi-language support

### Potential Integrations
- Social media platforms
- RSS feeds
- API providers
- Analytics tools

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python 3.11
python --version  # Should be 3.11 or higher

# Install Docker (optional)
docker --version
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cricket-updates.git
cd cricket-updates
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Running Locally

```bash
# Run with Python
python src/wsgi.py

# Or with Docker
docker build -t cricket-digest .
docker run -p 5000:5000 cricket-digest
```

## 📝 Usage

### Subscriber Signup
1. Visit the website
2. Enter your email address
3. Click "Subscribe"
4. Check your inbox for a welcome email

### Email Schedule
- **Daily Digest**: Sent every evening at 10 PM
- **Match Updates**: Real-time notifications for followed matches
- **Breaking News**: Sent as events occur

## 🏗️ Brief Project Structure

```plaintext
cricket-daily-digest/
├── src/
│   ├── __init__.py
│   ├── app.py           # Main Flask application
│   ├── wsgi.py         # WSGI entry point
│   └── templates/      # Email templates
├── static/             # Static assets
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── README.md
```

## 🚀 Deployment

### Vercel Deployment
1. Fork this repository
2. Connect to Vercel
3. Deploy with zero configuration
4. Use vercel.json to update versions
5. Enter environment variables

### Render Deployment (Alternative)
1. Fork this repository
2. Connect to Render
3. Deploy with zero configuration using docker image
4. Enter environment variables


### Email Template Development
- Templates are in `src/static/`
- Use inline CSS for email compatibility
- Test with different email clients

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔒 Legal Considerations

### Web Scraping
- Follows robots.txt guidelines
- Implements rate limiting
- Respects website terms of service
- Proper attribution of sources

### Data Privacy
- GDPR compliance
- Data retention policies
- User consent management
- Secure data handling

## 📚 Resources

### Web Scraping Best Practices
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Web Scraping Ethics](https://www.scrapehero.com/web-scraping-ethics/)


## 📮 Contact

Anurag Vishwakarma - [Anurag Vishwakarma](https://www.linkedin.com/in/anurag-vishwakarma-4a9a37168/)

Project Link: [https://github.com/anuchange/cricket-updates/](https://github.com/anuchange/cricket-updates/)
