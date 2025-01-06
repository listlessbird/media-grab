# Media Grab

A Python utility for downloading media from X (formerly Twitter) using the GraphQL API.

## Requirements

- Python 3.12+
- `requests` library

## Installation

1. Clone this repository
2. Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

```sh
python main.py --cookie "your_cookie_here" --user "username"
```

## Arguments

- `--cookie`: Authentication cookie from X (required to set on first run)
- `--user`: Username to download media from

## Cookie Storage

The authentication cookie will be saved to cookie.txt after first use, so you don't need to provide it on subsequent runs.

## Note

This tool is for educational purposes only. Please respect X's terms of service and API usage guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
