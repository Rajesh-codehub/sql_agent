# SQL Query Assistant with LLM

This project implements a natural language to SQL query interface using Streamlit, LangChain, and Ollama. Users can ask questions in natural language about their MySQL database, and the application will convert these questions into SQL queries and return the results.

## Prerequisites

- Python 3.8+
- MySQL Server
- Ollama

## Installation Steps

### 1. Install Ollama

1. Visit the [Ollama GitHub repository](https://github.com/ollama/ollama) and follow the installation instructions for your operating system.
2. After installation, run the following command to download and start the Llama 3 model:
   ```bash
   ollama run llama3
   ```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 3. Database Setup

1. Open MySQL Workbench
2. Create and populate the database using the scripts provided in `demo_sql_script.txt`
3. Update database configuration:
   - Create a `db_config.json` file in the project root:
   ```json
   {
       "host": "localhost",
       "username": "root",
       "password": "your_password",
       "db_name": "your_database_name"
   }
   ```

### 4. Python Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv envname
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     .\envname\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source envname/bin/activate
     ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

   Main dependencies include:
   - streamlit
   - langchain
   - langchain_community

## Running the Application

1. Ensure your virtual environment is activated
2. Start the Streamlit application:
   ```bash
   streamlit run sql_agent.py
   ```

## Usage Example

Once the application is running, you can ask questions in natural language. For example:

Query: "What is the last name of Malva from the employees table?"

The application will:
1. Convert your question to SQL
2. Execute the query
3. Display the results

## Project Structure

```
.
├── README.md
├── requirements.txt
├── sql_agent.py
├── demo_sql_script.txt
└── db_config.json
```

## Troubleshooting

- Ensure Ollama is running before starting the application
- Verify database credentials in `db_config.json`
- Check if all required packages are installed
- Make sure MySQL server is running and accessible

## Contributing

Please feel free to submit issues and pull requests.

## License

[Your chosen license]