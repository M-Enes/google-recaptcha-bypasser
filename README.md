# Google reCAPTCHA Bypasser

## Overview
This project aims to provide a method to bypass Google reCAPTCHA challenges. It is intended for educational purposes only.

## Features
- Automated reCAPTCHA solving
- Easy integration with web scraping tools
- Customizable solving strategies

It also includes image captcha solver with specific prompt. You can use any llm api for that.

## Installation
To install the necessary dependencies, run:
```bash
pip install -r requirements.txt
```
Also, please install ffmpeg for photo processing. You can find installation instructions for ffmpeg [here](https://ffmpeg.org/download.html).

## Usage
Before use, ensure you have the necessary API keys for the LLM service you intend to use. You can set these by creating a `.env` file in the root directory of the project with the following content:
```
OPENAI_API_KEY=your_llm_api_key
```

You need to have a simple web server running to test the bypasser. You can use Python's built-in HTTP server for this purpose. Navigate to the captchahtml folder and run:
```bash
python -m http.server 8000
```

To use the bypasser on localhost, run the following command:
```bash
python test.py
```

## Customization
You can edit the image-solving prompt and specify the LLM model or LLM request delay in the `CaptchaImageSolver` class.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## Disclaimer
This tool is for educational purposes only. Misuse of this tool can lead to legal consequences. Use responsibly.

## Contact
For any inquiries, please open an issue on the GitHub repository.