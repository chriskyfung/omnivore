# Omnivore Data Fetcher and Converter

This project contains two Python scripts:

1. `search.py`: Fetches all pages' ID and URL pairs from the Omnivore API and saves them as a JSON file.
2. `json2csv.py`: Converts the JSON data to CSV format, ensuring each cell is limited to a maximum of 30,000 characters to prevent data truncation when importing to Microsoft Excel.

## Prerequisites

- Python 3.x
- `requests` library for making API calls

You can install the required libraries using pip:

```bash
pip install requests
```

## Usage

### Fetching Data from Omnivore API

1. **Generate an API Key**: Log in to your Omnivore account and navigate to [Omnivore API Settings](https://omnivore.app/settings/api). Generate a new API key.

2. **Execute the Script**: Run the script from the command line using the following command:

   ```shell
   python query_all.py --apikey your-api-key
   ```

   If the `--apikey` option is not provided, the script will search for the `OMNIVORE_API_KEY` environment variable.
   The `query_all.py` script retrieves all pages' ID and URL pairs from the Omnivore API and saves them as a JSON file.

### Converting JSON to CSV

Run the `json2csv.py` script to convert the JSON data to CSV format. Each cell in the CSV file will be limited to a maximum of 30,000 characters.

```bash
python json2csv.py
```

## License

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
