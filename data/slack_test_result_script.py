import xml.etree.ElementTree as ET


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


if __name__ == "__main__":
    file_path = 'results/test-results.xml'
    total_tests, total_failures, failed_tests = extract_test_results(file_path)

    print(f"TOTAL_TESTS={total_tests}")
    print(f"TOTAL_FAILURES={total_failures}")
    print("FAILED_TESTS:")
    for failed_test in failed_tests:
        print(failed_test)
