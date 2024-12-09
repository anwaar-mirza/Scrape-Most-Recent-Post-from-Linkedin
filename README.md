# LinkedIn Most Recent Post Scraping Bot

This Python project uses Selenium with `undetected_chromedriver` to automate the scraping of the most recent posts from LinkedIn profiles or company pages. The bot navigates through provided LinkedIn URLs, extracts information about posts, and stores the data in a CSV file. It also includes functionality to handle interruptions and save unsaved links for later processing.

## Features

- **Automated Login with Cookies**: Automates login to LinkedIn using saved cookies for efficient navigation.
- **Most Recent Post Extraction**:
  - Retrieves the post description, time of posting, posted by, and follower count.
  - Interacts with posts (like, comment, open reactions, etc.) based on user input.
- **Error Handling**:
  - Saves unprocessed links to a separate file for reprocessing.
- **Time Parsing**:
  - Processes LinkedIn timestamps (e.g., "3h", "2w", "1mo") into standard dates.
- **CSV Export**:
  - Saves scraped data to a CSV file in append mode, ensuring no data is lost.
- **Driver Reinitialization**:
  - Automatically reinitializes the Selenium WebDriver after processing 100 URLs to prevent timeouts and IP blocking.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.7+
- Google Chrome
- Required Python libraries (install with the command below):

```bash
pip install selenium undetected-chromedriver webdriver-manager fake-useragent python-dateutil pandas
```

## Usage

1. **Set Up Cookies**:
   - Log in to LinkedIn using your browser and save the session cookies to a file named `cookies.pkl` in the script's directory.

2. **Prepare the Input File**:
   - Create a `remaining_links.csv` file with the following columns:
     - **Index**: Serial number for each entry.
     - **Company LinkedIn URL**: The URL of the LinkedIn profile or company page to scrape.

3. **Run the Script**:
   - Execute the script to scrape the most recent posts:
     ```bash
     python linkedin_scrape.py
     ```
   - The script will:
     - Open each URL from `remaining_links.csv`.
     - Navigate to the "Posts" section.
     - Extract data for the most recent post and save it to `test.csv`.
     - Handle errors gracefully and save problematic URLs in `remaining_links.csv`.

4. **Post Interaction Options**:
   - The bot provides the following interactions for each post:
     - **Like (1)**: Likes the post.
     - **Comment (2)**: Clicks the comment button.
     - **View Total Likes (3)**: Opens the reactions count.
     - **Open Menu (4)**: Opens the post's options menu.

5. **Output**:
   - Scraped data is saved to `test.csv` with the following fields:
     - `Posted By`: Name of the user or company who posted.
     - `Followers`: Total followers of the profile.
     - `Posted On`: Date the post was published.
     - `Description`: Content of the post.
     - `Profile URL`: The LinkedIn profile or company page URL.

## File Management

- **`test.csv`**:
  - Contains all successfully scraped post data.
- **`remaining_links.csv`**:
  - Stores URLs that failed during processing for future reprocessing.

## Error Handling

The script includes mechanisms to:

1. **Save Remaining Links**: Saves unprocessed URLs to `remaining_links.csv`.
2. **Reinitialize Driver**: Automatically restarts the WebDriver to reduce the risk of IP blocking.

## Example Outputs

### Input File: `remaining_links.csv`

| Index | Company LinkedIn URL                |
|-------|-------------------------------------|
| 1     | https://www.linkedin.com/company/xyz |
| 2     | https://www.linkedin.com/in/abc     |

### Output File: `test.csv`

| Posted By       | Followers   | Posted On  | Description           | Profile URL                     |
|------------------|-------------|------------|-----------------------|---------------------------------|
| Company ABC      | 12,000      | 2024-12-08 | This is a sample post | https://www.linkedin.com/xyz   |
| John Doe         | 1,500       | 2024-12-07 | Another sample post   | https://www.linkedin.com/abc   |
