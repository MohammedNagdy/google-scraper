# Google Scraper

A Google search automation tool with a client-server architecture using gRPC and Playwright.

## Overview

The Google Scraper project is designed to perform automated Google searches and retrieve search results using gRPC and Playwright. It consists of a client-server architecture where the client sends search queries to the server, and the server processes these queries using Playwright to scrape Google search results.

## Features

- Automated Google search using Playwright
- Client-server architecture with gRPC
- Anti-detection measures to avoid being blocked
- Structured search results with titles, links, and snippets
- Configurable timeout and browser settings
- Standalone search mode or client-server mode

## Project Structure

The project follows an object-oriented design with the following components:

### Core Components

- **GoogleScraper**: Class for performing Google searches and extracting results
- **SearchClient**: Client for sending search requests and handling responses
- **Server**: gRPC server implementation with configurable settings
- **SearchServicer**: Implementation of the gRPC search service

### Files

| File | Description |
|------|-------------|
| `google_search.py` | Contains the `GoogleScraper` class for performing searches |
| `server.py` | Implements the gRPC server and `SearchServicer` |
| `client.py` | Implements the `SearchClient` class for interacting with the server |
| `main.py` | Standalone search script for testing and demonstration |
| `search.proto` | Protocol buffer definition for gRPC service |
| `generate_grpc.py` | Utility to generate gRPC code from proto file |
| `requirements.txt` | Python dependencies |

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/google-scraper.git
   cd google-scraper
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   python -m playwright install chromium
   ```

4. Generate gRPC code:
   ```bash
   python generate_grpc.py
   ```

## Usage

### Client-Server Mode

This mode is useful when you want to separate the search functionality from your main application or when you need to distribute the load across multiple machines.

1. Start the server:
   ```bash
   python server.py
   ```

2. In another terminal, run the client:
   ```bash
   python client.py
   ```

   By default, the client will search for "python programming". You can modify the query in the `main()` function in `client.py`.

### Standalone Mode

For simple use cases, you can use the standalone mode:

```bash
python main.py
```

This will run a search using the `GoogleScraper` directly, without the need for a server.

### Custom Usage

You can also import and use the components in your own Python code:

```python
import asyncio
from playwright.async_api import async_playwright
from google_search import GoogleScraper

async def custom_search():
    async with async_playwright() as playwright:
        scraper = GoogleScraper()
        browser = await playwright.chromium.launch()
        context = await scraper.setup_browser(browser)
        page = await context.new_page()
        
        try:
            results = await scraper.search("your search query", page)
            for result in results:
                print(f"Title: {result['title']}")
                print(f"Link: {result['link']}")
                print(f"Snippet: {result['snippet']}")
        finally:
            await browser.close()

# Run the custom search
asyncio.run(custom_search())
```

For client-server usage in your own code:

```python
import asyncio
from client import SearchClient

async def custom_client():
    client = SearchClient()
    await client.connect()
    
    try:
        results = await client.search("your search query")
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
    finally:
        await client.close()

# Run the custom client
asyncio.run(custom_client())
```

## Configuration

### Server Configuration

You can configure the server address and the number of worker threads:

```python
from server import Server
import asyncio

async def custom_server():
    server = Server(address="0.0.0.0:50051", max_workers=20)
    await server.start()

asyncio.run(custom_server())
```

### Scraper Configuration

You can configure the timeout for search operations:

```python
from google_search import GoogleScraper

# Create a scraper with a 30-second timeout
scraper = GoogleScraper(timeout=30)
```

## Anti-Detection Measures

The `GoogleScraper` includes several measures to avoid detection:

- Custom user agent
- Disabling automation flags
- Simulating human-like behavior with delays
- Custom browser viewport and geolocation
- Disabling WebDriver flags

## Troubleshooting

### Common Issues

1. **Connection refused**: Make sure the server is running before starting the client.
2. **No results returned**: Google might be blocking the requests. Try adjusting the anti-detection settings.
3. **Timeout errors**: Increase the timeout value in the `GoogleScraper` constructor.

### Debugging

Enable more verbose output by adding print statements in the relevant methods:

```python
# In google_search.py
async def search(self, query: str, page: Page):
    print(f"Navigating to Google...")
    await page.goto("https://www.google.com")
    print(f"Entering search query: {query}")
    # ...
```


## Contributions are welcomed

We welcome contributions to expand the functionality of this Google scraper! Here are some planned features you can help with:

### Search Types
- [ ] Video search support - Add ability to scrape Google video search results
- [ ] News search support - Implement scraping of Google News results 
- [ ] Image search support - Add functionality to extract image search results

### Search Filters
- [ ] Add support for Google search filters like:
  - [ ] Time range filters (past hour, day, week etc.)
  - [ ] Result type filters (videos, news, images etc.)
  - [ ] Language and region filters
  - [ ] Advanced search operators

### UI/UX Improvements
- [ ] Automated cookie popup handling
  - [ ] Detect and dismiss Google cookie consent popups
  - [ ] Handle different popup variations across regions
  - [ ] Make popup handling configurable

Please feel free to:
1. Pick any of these features to work on
2. Submit bug fixes and improvements
3. Add documentation and examples
4. Suggest new features

Make sure to read our contribution guidelines below before submitting PRs.

### Guidelines

#### Creating Issues

1. Check existing issues to avoid duplicates
2. Use descriptive titles that summarize the problem/feature
3. For bug reports, include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages if any
   - Environment details (OS, Python version, etc.)
4. For feature requests, include:
   - Clear description of the proposed feature
   - Use cases and benefits
   - Any implementation ideas (optional)

#### Pull Requests

1. Create an issue first and discuss the changes
2. Fork the repository and create a branch for your feature
3. Follow the existing code style and conventions
4. Include tests for new functionality
5. Update documentation as needed
6. Keep PRs focused - one feature/fix per PR
7. Ensure all tests pass before submitting
8. Reference the related issue in your PR description
9. Be responsive to code review feedback


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
