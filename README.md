# joblib tqdm parallel

A lightweight utility to execute functions in parallel using `joblib` while providing an accurate `tqdm` progress bar with Google-style documentation.

## Features

- **Accurate Progress:** Synchronizes progress updates via `joblib`'s `BatchCompletionCallBack`.
- **Universal Arguments:** Automatically unpacks positional (tuple) and keyword (dict) arguments.
- **Google Style:** Docstrings follow the Google Python Style Guide.

## Usage

```python
from parallel_run import parallel_run

def my_function(a, b):
    return a + b

# Pass arguments as a list of tuples
tasks = [(1, 2), (3, 4), (5, 6)]
results = parallel_run(my_function, tasks, n_jobs=-1, batch_size=1)

```

## License

This project is licensed under the MIT License.

## Author

kei0822kei
