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

2. **Update the Script**: Open the `search.py` script and replace `<your-omnivore-api-key>` with your newly generated API key.

    ```python
    apikey = "<your-omnivore-api-key>"
    ```

3. **Execute the Script**: Run the `search.py` script to retrieve all pages' ID and URL pairs from the Omnivore API and save them as a JSON file.

    ```bash
    python search.py
    ```

### Converting JSON to CSV

Run the `json2csv.py` script to convert the JSON data to CSV format. Each cell in the CSV file will be limited to a maximum of 30,000 characters.

```bash
python json2csv.py
```

## License

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
