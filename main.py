import json
from scraper import CongaIdeasScraper
from claude_analyzer import ClaudeAnalyzer
from loading_indicator import start_loading_indicator
from markdown_converter import convert_markdown_to_pdf
import os
import logging
import sys

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    scraper = CongaIdeasScraper()
    categorized_ideas = scraper.get_ideas()
    logging.info("Scraped Ideas:")
    logging.info(json.dumps(categorized_ideas, indent=2))

    analyzer = ClaudeAnalyzer()

    pdf_output_folder = "reports/pdf_output"
    markdown_folder = "reports/markdown"
    ideas_data_folder = "reports/ideas-data"

    os.makedirs(pdf_output_folder, exist_ok=True)
    os.makedirs(markdown_folder, exist_ok=True)
    os.makedirs(ideas_data_folder, exist_ok=True)

    for project_name, project_ideas in categorized_ideas.items():
        project_file = f"{ideas_data_folder}/{project_name}_ideas.json"
        project_pdf_file = f"{pdf_output_folder}/{project_name}_ideas_summary.pdf"

        if os.path.exists(project_pdf_file):
            logging.info(f"Summary for project {project_name} already exists. Skipping.")
            continue

        logging.info(f"\nAnalyzing ideas for project: {project_name}")

        stop_event, loading_thread = start_loading_indicator("Waiting for response")
        summary = analyzer.analyze_ideas(json.dumps(project_ideas))
        if summary is None:
            logging.error(f"Failed to generate summary for project: {project_name}. Exiting.")
            sys.exit(1)
        stop_event.set()
        loading_thread.join()

        logging.info(f"\nIdeas Summary and Analysis for project: {project_name}")

        if summary:
            for section in summary["sections"]:
                logging.info(f"\n{section['title']}:")
                logging.info(section['content'])

            project_summary_file = f"{markdown_folder}/{project_name}_ideas_summary.md"
            with open(project_summary_file, "w") as file:
                for section in summary["sections"]:
                    file.write(f"# {section['title']}\n\n")
                    file.write(f"{section['content']}\n\n")
                file.write(summary["table"])

            logging.info(f"\nSummary for project {project_name} saved as {project_summary_file}")

            convert_markdown_to_pdf(project_summary_file, project_pdf_file)
            logging.info(f"Summary for project {project_name} converted to {project_pdf_file}")
        else:
            logging.warning(f"No summary generated for project: {project_name}")

