# Scrapy Dataminer

A Scrapy-based datamining package for scraping and storing data.

## Installation

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- [Git](https://git-scm.com/) for version control
- Optional: Azure Cosmos DB credentials (if using Azure integration)
- [Docker](https://www.docker.com/) to run the package in a containerized environment

### Setup

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Install Dependencies**

   Use Poetry to install project dependencies and generate the lock file:

   ```bash
   poetry install
   ```

   This command will create a `poetry.lock` file (if it doesn't exist) and install all dependencies defined in `pyproject.toml`.

3. **Activate the Virtual Environment**

   Activate the virtual environment managed by Poetry:

   ```bash
   poetry shell
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory to store environment variables:

   ```bash
   touch .env
   ```

   Populate the `.env` file with the necessary variables:

   ```env
   # .env file example

   # ScraperAPI keys:
   SCRAPERAPI_KEY = "your_scraperapi_key"
   SCRAPERAPI_URL = "http://api.scraperapi.com/?api_key=YOUR_API_KEY&url=" # leave this as it is

   # Azure Cosmos DB settings (if using Azure)
   COSMOS_DB_URI="your_cosmos_db_uri"
   COSMOS_DB_KEY="your_cosmos_db_key"
   COSMOS_DB_DATABASE="your_database_name"
   COSMOS_DB_CONTAINER="your_container_name"
   ```

   *Note: Ensure the `.env` file is included in your `.gitignore` to prevent sensitive information from being committed.*

## Usage

### Running the Spider Locally

To run the spider and save scraped data to a CSV file:

```bash
scrapy crawl {YOUR-SPIDER} -o output/{OUTPUT-CSV}.csv -t csv
```

Replace `{YOUR-SPIDER}` with the name of your spider and `{OUTPUT-CSV}` with your desired output filename.

To run the spider and pass scraped data to the Azure backend:

```bash
scrapy crawl {YOUR-SPIDER} --set USE_AZURE=True
```

### Running Different Pipelines

You can configure which pipelines to activate by editing the `ITEM_PIPELINES` setting in `settings.py`:

```python
# settings.py

ITEM_PIPELINES = {
    'your_project.pipelines.AzureCosmosDBPipeline': 300,  # Enable Azure pipeline
    'your_project.pipelines.CsvExportPipeline': 400,      # Enable CSV export pipeline
}
```

Adjust the pipelines and their priorities (`300`, `400`, etc.) according to your needs.

### Running with Docker

1. **Build the Docker Image**

   Build the Docker container with Poetry and your code:

   ```bash
   docker build -t scrapy-dataminer .
   ```

2. **Run the Docker Container**

   Run the container with a mounted volume to enable access to local project files and output storage:

   ```bash
   docker run -v $(pwd):/app -it scrapy-dataminer
   ```
   ```shell
   docker run -v "%cd%":/app -it scrapy-dataminer
   ```

   The `-v $(pwd):/app` option mounts your current directory to the `/app` directory in the container, allowing the containerized scraper to read and write files directly in your local project directory.

3. **Run Specific Commands in Docker**

   To run the spider within the Docker container and save to CSV:

   ```bash
   docker run -v $(pwd):/app -it scrapy-dataminer poetry run scrapy crawl {YOUR-SPIDER} -o output/{OUTPUT-CSV}.csv -t csv
   ```

   To run the spider with Azure integration in Docker:

   ```bash
   docker run -v $(pwd):/app -it scrapy-dataminer poetry run scrapy crawl {YOUR-SPIDER} --use-azure
   ```

   To utilize proxies from ScraperAPI:

   ```bash
   docker run -v $(pwd):/app -it scrapy-dataminer poetry run scrapy crawl {YOUR-SPIDER} --use-scraperapi
   ```

## Development

### Checklist:
- Create a new spider (dataminer/spiders/{spider_name}_spider.py) using the "template_spider.py" as a template.
- Create a new url resource json (dataminer/resources/{spider_name.py}) using the "template_urls.json" as template.
- Fill the TODOS your new spider.
- Replace the example parsing logic your new spider.
- Populate url resource json with sites you wish to parse.
- Create a .env file to the project root and populate it with your azure and scraperapi details.
- Run the spider.

### Pushing to Git

After making changes, you can push your code to the Git repository:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

*Replace `main` with your branch name if necessary.*

### Building the Package

To build the package using Poetry:

```bash
poetry build
```

*Ensure you have the appropriate credentials and permissions before publishing.*

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

