# utils.py

import logging
from dotenv import load_dotenv
import os
import requests
from typing import Optional
from urllib.parse import urlparse

def setup_logging(verbose: bool = False):
    """
    Configure logging for the QuantCLI application.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("quantcli.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up.")

def load_api_key():
    """
    Load the OpenAI API key from the .env file.
    Note: API key is now managed by LLMClient class, not set globally.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    logger = logging.getLogger(__name__)
    if not api_key:
        logger.warning("OPENAI_API_KEY not found in environment variables.")
        logger.warning("Set OPENAI_API_KEY in .env file or environment.")
    else:
        logger.info("OpenAI API key loaded from environment.")


def get_pdf_url_via_unpaywall(doi: str, email: str) -> Optional[str]:
    """
    Retrieve the free PDF URL of an article using Unpaywall API.

    Args:
        doi (str): The DOI of the article.
        email (str): Your email address (required by Unpaywall).

    Returns:
        Optional[str]: The direct PDF URL if available, else None.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Attempting to retrieve PDF URL for DOI: {doi}")
    api_url = f"https://api.unpaywall.org/v2/{doi}"
    params = {
        "email": email
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('is_oa') and data.get('best_oa_location') and data['best_oa_location'].get('url_for_pdf'):
            return data['best_oa_location']['url_for_pdf']
        else:
            logger.warning("No free PDF available via Unpaywall.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Unpaywall API request failed: {e}")
        return None

def download_pdf(article_url: str, save_path: str, doi: Optional[str] = None) -> bool:
    """
    Attempt to download the PDF from the article URL or Unpaywall.

    Args:
        article_url (str): The URL of the article.
        save_path (str): The path where the PDF will be saved.
        doi (Optional[str]): DOI of the article for Unpaywall.

    Returns:
        bool: True if download is successful, False otherwise.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Attempting to download PDF from URL: {article_url}")
    headers = {
        "User-Agent": "QuantCLI/1.0 (mailto:your.email@example.com)"
    }
    try:
        # First, attempt to download directly
        response = requests.get(article_url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        # Check if the response is a PDF
        if 'application/pdf' in response.headers.get('Content-Type', ''):
            with open(save_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"PDF downloaded successfully to {save_path}")
            return True
        else:
            logger.info("Direct download unsuccessful. Attempting to use Unpaywall.")
            if doi:
                # Get email from environment variable
                unpaywall_email = os.getenv("UNPAYWALL_EMAIL", "your.email@example.com")
                pdf_url = get_pdf_url_via_unpaywall(doi, unpaywall_email)
                if pdf_url:
                    response = requests.get(pdf_url, headers=headers)
                    response.raise_for_status()
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"PDF downloaded successfully via Unpaywall to {save_path}")
                    return True
                else:
                    logger.warning("No PDF available via Unpaywall.")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download PDF: {e}")
        return False


def validate_url(url: str) -> bool:
    """
    Validate if a URL is safe to open in a web browser.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if URL is valid and safe, False otherwise.
    """
    logger = logging.getLogger(__name__)
    try:
        if not url or not isinstance(url, str):
            logger.warning("Invalid URL: empty or not a string")
            return False

        parsed = urlparse(url)

        # Check if scheme is http or https
        if parsed.scheme not in ['http', 'https']:
            logger.warning(f"Invalid URL scheme: {parsed.scheme}")
            return False

        # Check if netloc (domain) exists
        if not parsed.netloc:
            logger.warning("Invalid URL: missing domain")
            return False

        return True
    except Exception as e:
        logger.error(f"Error validating URL: {e}")
        return False
