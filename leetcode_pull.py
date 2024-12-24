import os
import requests

# API Configuration
BASE_URL = "https://leetcode.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
}

# Map LeetCode languages to file extensions
LANGUAGE_TO_EXTENSION = {
    "python3": ".py",
    "java": ".java",
    "java8": ".java",
    "java11": ".java",
    "cpp": ".cpp",
    "c": ".c",
    "javascript": ".js",
    "typescript": ".ts",
    "ruby": ".rb",
    "swift": ".swift",
    "kotlin": ".kt",
    "go": ".go",
}

# Prompt user for LEETCODE_SESSION token
def prompt_for_session_cookie():
    print("\n")
    print("=" * 50)
    print("LeetCode Session Cookie Required")
    print("=" * 50)
    print(
        "To retrieve your LeetCode session cookie, follow these steps:\n"
        "1. Open a web browser and log in to your LeetCode account.\n"
        "2. Open the browser's developer tools (right-click > 'Inspect' or press F12).\n"
        "3. Navigate to the 'Application' or 'Storage' tab in the developer tools.\n"
        "4. Select 'Cookies' under 'Storage' and look for 'leetcode.com'.\n"
        "5. Find the cookie named 'LEETCODE_SESSION' and copy its value.\n"
        "6. Paste the cookie value below."
    )
    print("=" * 50)
    return input("Enter your LEETCODE_SESSION cookie: ").strip()

# Step 1: Fetch submissions (without code)
def fetch_submissions():
    query = """
    query submissions($offset: Int!) {
      submissionList(offset: $offset, limit: 20) {
        submissions {
          id
          title
          lang
          statusDisplay
          timestamp
        }
      }
    }
    """
    offset = 0
    submissions = []

    while True:
        print(f"Fetching submissions with offset {offset}...")
        response = requests.post(
            BASE_URL,
            json={"query": query, "variables": {"offset": offset}},
            headers=HEADERS
        )
        if response.status_code == 401:
            print("Session expired or invalid. Please try again with a valid session cookie.")
            return []
        print(f"Response status code: {response.status_code}")

        if response.status_code != 200:
            print(f"Failed to fetch submissions: {response.status_code}")
            print(f"Response body: {response.text}")
            break

        data = response.json()
        fetched = data.get("data", {}).get("submissionList", {}).get("submissions", None)

        if fetched is None:
            print("Unexpected response structure:")
            print(response.text)
            break

        print(f"Fetched {len(fetched)} submissions.")
        submissions.extend(fetched)

        if len(fetched) < 20:  # Break if fewer than 20 submissions were returned
            break

        offset += 20

    print(f"Total submissions fetched: {len(submissions)}")
    return submissions

# Step 2: Fetch code for a submission
def fetch_code(submission_id):
    query = """
    query submissionDetails($id: Int!) {
      submissionDetails(submissionId: $id) {
        code
        question {
          questionFrontendId
        }
      }
    }
    """
    response = requests.post(
        BASE_URL,
        json={"query": query, "variables": {"id": submission_id}},
        headers=HEADERS
    )
    print(f"Fetching code for submission ID: {submission_id}, Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to fetch code for submission ID {submission_id}: {response.status_code}")
        print(f"Response body: {response.text}")
        return None, None

    data = response.json()
    code = data.get("data", {}).get("submissionDetails", {}).get("code", None)
    question_id = data.get("data", {}).get("submissionDetails", {}).get("question", {}).get("questionFrontendId", None)
    return code, question_id

# Step 3: Filter for the most recent accepted solutions
def get_recent_accepted_solutions(submissions):
    accepted_solutions = {}

    for sub in submissions:
        if sub["statusDisplay"] == "Accepted":
            problem_title = sub["title"]
            current_solution = accepted_solutions.get(problem_title)

            if current_solution is None or sub["timestamp"] > current_solution["timestamp"]:
                accepted_solutions[problem_title] = sub

    print(f"Filtered {len(accepted_solutions)} accepted solutions.")
    return accepted_solutions.values()

# Step 4: Save solutions to the LEETCODE directory
def save_solutions_to_files(solutions):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    leetcode_dir = os.path.join(os.path.dirname(script_directory), "LEETCODE")

    os.makedirs(leetcode_dir, exist_ok=True)
    print(f"Saving solutions to: {leetcode_dir}")

    for solution in solutions:
        submission_id = solution["id"]
        title = solution["title"]
        language = solution["lang"]

        print(f"Processing submission: {title}, Language: {language}")
        normalized_lang = language.lower().split(" ")[0]

        code, question_id = fetch_code(submission_id)
        if not code or not question_id:
            print(f"Skipping solution for {title}: Code or question ID not available.")
            continue

        extension = LANGUAGE_TO_EXTENSION.get(normalized_lang, ".txt")
        if extension == ".txt":
            print(f"Warning: Unrecognized language '{language}' for '{title}'. Defaulting to .txt.")

        filename = f"{question_id}. {title.replace(' ', '_')}{extension}"
        filepath = os.path.join(leetcode_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(code)
            print(f"Saved: {filepath}")
        except Exception as e:
            print(f"Failed to save {filename}: {e}")

# Main Function
def main():
    print("Starting LeetCode Pull...")
    LEETCODE_SESSION = prompt_for_session_cookie()

    if not LEETCODE_SESSION:
        print("Session cookie not provided. Exiting...")
        return

    HEADERS["cookie"] = f"LEETCODE_SESSION={LEETCODE_SESSION}"

    try:
        print("Fetching submissions...")
        submissions = fetch_submissions()

        if not submissions:
            print("No submissions found.")
            return

        print("Filtering most recent accepted solutions...")
        solutions = get_recent_accepted_solutions(submissions)

        print("Saving solutions to files in the LEETCODE directory...")
        save_solutions_to_files(solutions)
        print("All solutions saved successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
