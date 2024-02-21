# Secret Generator Script Usage Guide

This script is a simple tool designed to generate a random secret (password or token) and copy it directly to your clipboard. It uses a combination of letters, punctuation, and digits to create a secure and unique secret. Here's how to use it:

## Prerequisites

Before you start, ensure you have Python installed on your computer and the `pyperclip` module available. You can install `pyperclip` using pip and the requirements file:

## Installation

1. `pip install -r requirements.txt`

## How to Use

1. **Run the Script**: Use the command line to navigate to the directory containing the script. Execute it by providing the desired length of the secret string as an argument:

    ```
    ./generate_secret.py <length>
    ```

    Replace `<length>` with the number of characters you want your secret string to have.

2. **Retrieve the Secret**: The script will output the generated secret string to the terminal and copy it to your clipboard. You can paste it wherever you need.