# LeetCode Solutions Fetcher

## Overview
The LeetCode Solutions Fetcher is a Python script designed to automate the process of fetching accepted solutions from your LeetCode account and saving them locally in organized files. This script interacts with the LeetCode GraphQL API and requires a valid session cookie for authentication.

## Features
- Fetch all submissions from your LeetCode account.
- Filter and retrieve only the most recent accepted solutions.
- Save solutions to files with appropriate extensions based on the programming language used.
- Automatically creates a directory (`LEETCODE`) to store your solutions.

## Prerequisites
- Python 3.x installed on your system.
- A valid LeetCode session cookie.
- Basic knowledge of how to retrieve cookies from your browser (instructions provided by the script).

## Installation
1. Clone or download this repository.
2. Ensure all dependencies are installed. The script uses the `requests` library. Install it with:
   ```bash
   pip install requests
   ```

## Usage
1. Run the script:
   ```bash
   python script_name.py
   ```
2. Follow the on-screen instructions to provide your LeetCode session cookie.
3. The script will fetch your submissions, filter for the most recent accepted solutions, and save them in the `LEETCODE` directory.

## Directory Structure
The solutions will be saved in the `LEETCODE` directory, located in the parent directory of the script. File names will follow the format:
```
<question_id>. <problem_title>.<extension>
```
Examples:
```
1. Two_Sum.py
42. Trapping_Rain_Water.java
```

## Supported Languages
The script maps LeetCode programming languages to file extensions. If a language is unrecognized, the solution is saved with a `.txt` extension.
Supported languages include:
- Python
- Java
- C++
- JavaScript
- TypeScript
- Ruby
- Swift
- Kotlin
- Go

## How It Works
1. **Session Cookie Prompt**:
   The script guides you to retrieve your `LEETCODE_SESSION` cookie.

2. **Fetching Submissions**:
   The script sends GraphQL queries to fetch your submissions from LeetCode.

3. **Filtering Solutions**:
   Only accepted solutions are retained, and the most recent submission for each problem is selected.

4. **Saving to Files**:
   Solutions are saved with appropriate file names and extensions in the `LEETCODE` directory.

## Error Handling
- If the session cookie is invalid or expired, the script will prompt you to re-enter it.
- In case of unrecognized programming languages, solutions are saved as `.txt` files with a warning message.
- Any issues with saving files are logged to the console.

## Example Run
1. Start the script:
   ```
   Starting LeetCode Pull...
   ==============================
   LeetCode Session Cookie Required
   ==============================
   [Instructions on retrieving session cookie]
   Enter your LEETCODE_SESSION cookie:
   ```
2. The script fetches and filters submissions:
   ```
   Fetching submissions...
   Fetched 20 submissions.
   Total submissions fetched: 35
   Filtering most recent accepted solutions...
   Filtered 10 accepted solutions.
   ```
3. Solutions are saved locally:
   ```
   Saving solutions to: /path/to/LEETCODE
   Processing submission: Two Sum, Language: python3
   Saved: /path/to/LEETCODE/1. Two_Sum.py
   All solutions saved successfully!
   ```
