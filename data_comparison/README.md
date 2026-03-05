# Data Comparison Service

A standalone Flask web application for comparing CSV datasets side by side. Upload two or more CSV files, join them on a shared key column, explore the result in a filterable table, and visualise it with an interactive chart — all in the browser.

## Features

- **Incremental resource loading** — start with a single CSV, then join additional files one at a time
- **Automatic left-join** on the first shared column across datasets
- **DataTables** table with SearchBuilder, pagination, and column-level filtering
- **Interactive charts** via Plotly — line, scatter, and bar with optional log scale
- **Chart series control** — choose x-axis column and toggle y-axis series individually
- **Filtered data mode** — plot only the rows currently visible in the table

## Tech Stack

| Layer | Library |
|---|---|
| Backend | Flask 3, Gunicorn |
| Table | DataTables 2.x + SearchBuilder |
| Charts | Plotly.js |
| CSV parsing | PapaParse |
| Container | Docker |

## Project Structure

```
datacomparison_app/
├── app.py                        # Flask application
├── requirements.txt              # Python dependencies
├── Dockerfile
├── .dockerignore
├── Makefile                      # start / stop helpers
├── templates/
│   └── datacomparison.html       # Main UI
└── static/
    ├── datacomparison.css        # App styles
    ├── datacomparison.js         # Join logic, DataTables, chart builder
    ├── dataTables.bundle.min.css # DataTables + SearchBuilder bundle
    ├── dataTables.bundle.min.js  #   "
    ├── jquery.min.js             # jQuery    
    ├── papaparse.min.js          # PapaParse
    └── plotly.min.js             # Plotly 
```

## Getting Started

### Prerequisites

- Docker, **or** Python 3.10+

### Run with Docker

```bash
make start   # builds the image and starts the container on http://localhost:5009
make stop    # stops and removes the container and image
```

### Run locally (without Docker)

```bash
pip install -r requirements.txt
python app.py
```

The app will be available at `http://localhost:5000`.

## Usage

1. Enter a label and select a CSV file for **Resource 1**, then click **Add resource**.
2. The table is populated immediately. A **Resource 2** row appears in the form.
3. Enter a label and select a second CSV, then click **Add resource** again to join it.
4. Repeat for as many resources as needed — each is left-joined on the first shared column.
5. Use the **SearchBuilder** above the table to filter rows, then switch to the **Graph** tab to build a chart from the (optionally filtered) data.
