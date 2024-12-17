# Sales Dashboard

A Python-based sales dashboard application that visualizes sales data and provides insights through interactive charts and analytics. The application now includes database support and can be compiled into a standalone executable.

## Features
- Interactive data visualization
- Sales analytics and metrics
- CSV data import support
- SQLite database integration
- File upload interface
- Standalone executable option

## Setup
1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```

## Data Management
- The application uses SQLite database to store sales data
- You can import data through the web interface using CSV files
- Initial sample data is provided in 'Sales Dataset.csv'
- You can generate new sample data using `generate_sample_data.py`

## Usage
1. Launch the application
2. Use the file upload interface to import CSV data
3. View and analyze sales data through the interactive dashboard
4. Switch between table view and visualization tabs for different perspectives on the data
