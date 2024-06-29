import json
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def extract_test_results(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        total_tests = 0
        total_failures = 0
        failed_tests = []
        passed_tests = []

        # Loop through each testsuite
        for testsuite in root.findall('testsuite'):
            total_tests += int(testsuite.get('tests', '0'))
            total_failures += int(testsuite.get('failures', '0'))

            # Loop through each testcase
            for testcase in testsuite.findall('testcase'):
                if testcase.find('failure') is not None:
                    failed_tests.append(testcase.get('name'))  # ❌ is the red cross symbol
                else:
                    passed_tests.append(testcase.get('name'))

        return total_tests, total_failures, failed_tests, passed_tests

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return 0, 0, [], []


def send_slack_message(webhook_url, total_tests, total_failures, failed_tests, passed_tests):
    headers = {'Content-Type': 'application/json'}

    # Calculate total passed tests
    total_passed = total_tests - total_failures

    # Prepare the message using markdown
    message = (
        "_*ℹ️ TESTS RESULTS*_\n\n\n"
        f"TOTAL TESTS = {total_tests}\n\n"
        f"TOTAL PASSED = {total_passed}\n\n"
        f"TOTAL FAILURES = {total_failures}\n\n\n"
        "*PASSED TESTS:*\n\n"
    )

    for test in passed_tests:
        message += f"   :white_check_mark: {test}\n\n\n"

    message += "*FAILED TESTS:*\n\n"
    for test in failed_tests:
        message += f"   :x: {test}\n\n"
    message += "───────────────────────────\n\n\n"

    payload = {
        "text": message,
        "mrkdwn": True  # Enable markdown rendering
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Failed to send Slack message: {response.status_code}, {response.text}")
    else:
        print("Slack message sent successfully!")


if __name__ == "__main__":
    file_path = 'results/test-results.xml'  # Path to your XML test results file
    total_tests, total_failures, failed_tests, passed_tests = extract_test_results(file_path)

    # Slack webhook URL
    webhook_url = os.getenv('SLACK_WEBHOOK')

    # Send Slack message with test results
    send_slack_message(webhook_url, total_tests, total_failures, failed_tests, passed_tests)
