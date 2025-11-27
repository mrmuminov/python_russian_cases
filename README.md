# Python Russian Cases API

This is a simple FastAPI application to decline Russian words.

## Running the project

1.  **Build the Docker image:**
    ```bash
    docker build -t russian-cases-api .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 80:80 russian-cases-api
    ```

The API will be available at `http://localhost`.

## Example

The root endpoint can be used as a health check:

## API

The API has the following endpoints to decline a word (`q` parameter) into a specific case:

*   `/{case}`: Returns the word declined in the specified case.

### Valid Cases

*   `nomn` (Именительный)
*   `gent` (Родительный)
*   `datv` (Дательный)
*   `accs` (Винительный)
*   `ablt` (Творительный)
*   `loct` (Предложный)
*   `all` (Returns all cases)

### Example Usage

```bash
curl "http://localhost/gent?q=слово"
```

Response:
```json
{
  "result": "слова",
  "time": 0.000123456
}
```

```bash
curl "http://localhost/all?q=слово"
```

Response:
```json
{
  "result": {
    "nomn": "слово",
    "gent": "слова",
    "datv": "слову",
    "accs": "слово",
    "ablt": "словом",
    "loct": "слове"
  },
  "time": 0.000123456
}
```

> See updates: https://github.com/mrmuminov/python_russian_cases