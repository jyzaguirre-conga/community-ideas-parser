import json
from scraper import CongaIdeasScraper
from claude_analyzer import ClaudeAnalyzer
from loading_indicator import start_loading_indicator
from markdown_converter import convert_markdown_to_pdf

if __name__ == "__main__":
    scraper = CongaIdeasScraper()
    ideas = scraper.get_ideas()
    print("Scraped Ideas:")
    print(json.dumps(ideas, indent=2))

    analyzer = ClaudeAnalyzer()
    print("\nAnalyzing ideas with Claude...")
    stop_event, loading_thread = start_loading_indicator("Waiting for response")
    summary = analyzer.analyze_ideas(json.dumps(ideas))
    stop_event.set()
    loading_thread.join()

    print("\nIdeas Summary and Analysis:")

    if summary:
        for section in summary["sections"]:
            print(f"\n{section['title']}:")
            print(section['content'])

        with open("ideas_summary.md", "w") as file:
            for section in summary["sections"]:
                file.write(f"# {section['title']}\n\n")
                file.write(f"{section['content']}\n\n")
            file.write(summary["table"])

        print("\nSummary saved as ideas_summary.md")

        convert_markdown_to_pdf("ideas_summary.md", "ideas_summary.pdf")
        print("Summary converted to ideas_summary.pdf")
    else:
        print("No summary generated.")

