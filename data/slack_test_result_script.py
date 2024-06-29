import json
import xml.etree.ElementTree as ET

import requests


def extract_test_results(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        total_tests = 0
        total_failures = 0
        failed_tests = []

        # Loop through each testsuite
        for testsuite in root.findall('testsuite'):
            total_tests += int(testsuite.get('tests', '0'))
            total_failures += int(testsuite.get('failures', '0'))

            # Loop through each testcase to find failed ones
            for testcase in testsuite.findall('testcase'):
                if testcase.find('failure') is not None:
                    failed_tests.append(f"❌ {testcase.get('name')}")  # ❌ is the red cross symbol

        return total_tests, total_failures, failed_tests

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return 0, 0, []


def send_slack_message(webhook_url, total_tests, total_failures, failed_tests):
    headers = {'Content-Type': 'application/json'}

    # Prepare the message
    message = "✅ Tests completed:\n"
    message += "\n"
    message += f"TOTAL_TESTS={total_tests}\n"
    message += f"TOTAL_FAILURES={total_failures}\n"

    # Append failed tests
    message += "FAILED_TESTS:\n\n"
    for test in failed_tests:
        message += f"{test}\n\n"

    payload = {'text': message.strip()}  # Strip to remove any leading/trailing whitespace
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Failed to send Slack message: {response.status_code}, {response.text}")
    else:
        print("Slack message sent successfully!")


if __name__ == "__main__":
    file_path = 'results/test-results.xml'  # Path to your XML test results file
    total_tests, total_failures, failed_tests = extract_test_results(file_path)

    # Slack webhook URL
    webhook_url = "https://hooks.slack.com/services/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"

    # Send Slack message with test results
    send_slack_message(webhook_url, total_tests, total_failures, failed_tests)
