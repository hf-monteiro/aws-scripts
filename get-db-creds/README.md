# AWS Secrets Manager Script

This README provides a simple guide on how to use the provided Python script to retrieve secrets (such as database credentials) from AWS Secrets Manager for different environments (e.g., development, staging).


## Installation/Requirements

1. `pip install -r requirements.txt`

## Usage

The script is designed to be executed from the command line and accepts a single optional argument to specify the environment. If no argument is provided, it defaults to the development environment.


1. **Running the Script**:
  - To run the script for the development environment (default):
    ```
    ./get-db-creds.py
    ```
  - To specify an environment explicitly, pass it as an argument (dev or stage):
    ```
    ./get-db-creds.py dev
    ```
    or
    ```
    ./get-db-creds.py stage
    ```
