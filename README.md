# FotosBlog CLI

FotosBlog CLI is a command-line tool to download images from school blogs. It supports both single-threaded execution (v1.0.0) and concurrent execution using Celery (v2.0.0).

## Features

- List available blog targets
- Download images from a specific target or all targets
- Configure target resources
- Set output destinations
- Supports concurrent execution with Celery (v2.0.0)

## Requirements

- Python 3.x
- Redis (must be installed but not running as a service)
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `celery`
  - `redis`

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/fotosblog-cli.git
   cd fotosblog-cli
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Install Redis (ensure it's not running as a service):
   ```sh
   sudo apt install redis
   ```
   To prevent Redis from running as a service:
   ```sh
   sudo systemctl disable redis
   sudo systemctl stop redis
   ```

## Usage

Run the CLI tool with the following options:

```sh
python app.py [-l] [-t TARGET] [-c CONFIGURE] [-o OUTPUT] [-a]
```

### Available Arguments:

- `-l, --list` : List all defined targets
- `-t, --target <name>` : Target a specific blog resource
- `-c, --configure <config>` : Configure a resource
- `-o, --output <path>` : Set output destination
- `-a, --all` : Target all available resources

### Running with Celery (v2.0.0)

1. Run the CLI tool as usual. The cli will launch the redis server and the celery workers on its own.

## Project Structure

```
── app.py
├── celery_app.py
├── config.py
├── data
│   ├── conf.json
│   └── pictures.db
├── db.py
├── requirements.txt
└── utils.py
```

## License

This project is licensed under the MIT License.


