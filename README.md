# Conga Community Ideas Parser 📝🔍

This project scrapes ideas from the Conga community website, analyzes them using Anthropic's Claude AI, and generates summary reports in Markdown and PDF formats. 🚀

## Features ✨

- Scrapes idea details from the Conga community website 🕷️
- Categorizes ideas by project 📊
- Generates concise summaries and analyses using Claude AI 🤖
- Outputs reports in Markdown and PDF formats 📄
- Handles timeouts and retries for robust scraping 💪
- Provides a loading indicator during AI analysis ⏳
- Supports headless mode for server-side execution 🖥️

## Prerequisites 📋

- Python 3.x
- Chrome WebDriver (compatible with your Chrome version)
- Anthropic API key

## Installation 🛠️

1. Clone the repository:
git clone https://github.com/yourusername/conga-community-ideas-parser.git

<TEXT>
2. Install the required dependencies:
pip install -r requirements.txt

<TEXT>
3. Set up the configuration:
- Create a `.env` file in the project root directory.
- Add the following variables to the `.env` file:
  ```
  USERNAME=your_conga_username
  PASSWORD=your_conga_password
  ANTHROPIC_API_KEY=your_anthropic_api_key
  ```

## Usage 🚀

1. Run the main script:
python main.py

<TEXT>
The script will scrape ideas from the Conga community website, analyze them using Claude AI, and generate summary reports in the `reports` directory.
2. Check the generated Markdown and PDF reports for insights and summaries of the scraped ideas. 📈

## Configuration ⚙️

The project uses a `config.py` file for configuration. You can modify the following variables:

- `DEVELOPMENT_TESTING`: Set to `True` to parse only one page during development (default: `False`).
- `HEADLESS_MODE`: Set to `True` to run the browser in headless mode (default: `False`).

## Project Structure 📁

- `main.py`: The main script that orchestrates the scraping, analysis, and report generation.
- `scraper.py`: Contains the `CongaIdeasScraper` class for scraping ideas from the Conga community website.
- `claude_analyzer.py`: Contains the `ClaudeAnalyzer` class for analyzing ideas using Anthropic's Claude AI.
- `config.py`: Configuration file for setting up environment variables.
- `.env`: File for storing sensitive information like usernames, passwords, and API keys.
- `requirements.txt`: List of required Python dependencies.

## Contributing 🤝

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License 📄

This project is licensed under the MIT License.

## Acknowledgements 🙏

- Anthropic for providing the Claude AI platform.
- Selenium for web scraping capabilities.
- BeautifulSoup for HTML parsing.
- markdown-pdf for converting Markdown to PDF.

Happy idea parsing! 😄🎉
