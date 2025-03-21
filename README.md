# Google Scraper

## Overview

The Google Scraper project is designed to perform automated Google searches and retrieve search results using gRPC and Playwright. It consists of a client-server architecture where the client sends search queries to the server, and the server processes these queries using Playwright to scrape Google search results.

## Components

### 1. `client.py`

- **Purpose**: Acts as the client in the gRPC architecture. It sends search queries to the server and receives search results.
- **Key Functions**:
  - `run()`: Establishes a connection to the gRPC server and sends a search request. It handles the response and prints the search results.

### 2. `server.py`

- **Purpose**: Implements the gRPC server that processes search requests and returns search results.
- **Key Classes**:
  - `SearchService`: A gRPC service that handles search requests. It uses Playwright to perform Google searches and returns the results.
- **Key Functions**:
  - `serve()`: Starts the gRPC server and listens for incoming requests.

### 3. `google_search.py`

- **Purpose**: Contains the logic for performing Google searches using Playwright.
- **Key Functions**:
  - `google_search(query, page)`: Navigates to Google, performs a search, and extracts search results.

### 4. `generate_grpc.py`

- **Purpose**: Generates Python code from the `search.proto` file using gRPC tools.
- **Key Functions**:
  - `protoc.main()`: Executes the gRPC tools to generate necessary Python files for gRPC communication.

### 5. `main.py`

- **Purpose**: A standalone script to test the Google search functionality using Playwright.
- **Key Functions**:
  - `run(playwright)`: Launches a browser and performs a Google search.
  - `main()`: Entry point for running the script.

### 6. `search.proto`

- **Purpose**: Defines the gRPC service and messages for search requests and responses.
- **Key Definitions**:
  - `SearchService`: The gRPC service definition.
  - `SearchRequest`: Message containing the search query.
  - `SearchResponse`: Message containing the search results.

## Installation

To set up the project, ensure you have Python installed and follow these steps:

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate gRPC code:
   ```bash
   python generate_grpc.py
   ```

3. Run the server:
   ```bash
   python server.py
   ```

4. Run the client:
   ```bash
   python client.py
   ```

## Usage

- **Client**: Sends a search query and prints the results.
- **Server**: Processes search requests and returns results using Playwright.

## Dependencies

- `playwright`: For browser automation.
- `grpcio` and `grpcio-tools`: For gRPC communication.
- `protobuf`: For protocol buffer support.

## Notes

- Ensure that Playwright is properly installed and set up on your system.
- The server must be running before the client can send requests.
