# Conga Community Ideas Parser

This project scrapes ideas from the Conga community website, analyzes them using the Claude API, and generates a summary and analysis of the ideas in Markdown and PDF formats.

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/your-username/community-ideas-parser.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

-  Install ChromeDriver compatible with your OS


3. Create a `.env` file in the root directory of the project and add the following variables:

   ```
   USERNAME=your-conga-username
   PASSWORD=your-conga-password
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

   Replace `your-conga-username`, `your-conga-password`, and `your-anthropic-api-key` with your actual Conga username, password, and Anthropic API key, respectively.

4. Run the `main.py` script:

   ```
   python main.py
   ```

   The script will scrape the ideas from the Conga community website, analyze them using the Claude API, and generate a summary and analysis in Markdown (`ideas_summary.md`) and PDF (`ideas_summary.pdf`) formats.

## Configuration

The `config.py` file contains additional configuration variables that you can modify as needed:

- `PAGE_DELAY`: The delay (in seconds) between loading each page during scraping.
- `IDEA_DELAY`: The delay (in seconds) between scraping each idea.
- `DEVELOPMENT_TESTING`: Set to `True` for development and testing purposes.
- `HEADLESS_MODE`: Set to `False` to run the browser in headless mode.

Make sure to review and update these variables according to your requirements.

## License

This project is licensed under the [MIT License](LICENSE).

