import sys
import os

# Добавляем путь к каталогу с cfg.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import xml.etree.ElementTree as ET
import requests

import cfg


def extract_test_results(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        total_tests = 0
        total_failures = 0
        failed_tests = []
        passed_tests = []

        # Проходимся по каждому testsuite
        for testsuite in root.findall('testsuite'):
            total_tests += int(testsuite.get('tests', '0'))
            total_failures += int(testsuite.get('failures', '0'))

            # Проходимся по каждому testcase
            for testcase in testsuite.findall('testcase'):
                if testcase.find('failure') is not None:
                    failed_tests.append(testcase.get('name'))
                else:
                    passed_tests.append(testcase.get('name'))

        return total_tests, total_failures, failed_tests, passed_tests

    except ET.ParseError as e:
        print(f"Ошибка парсинга XML файла: {e}")
        return 0, 0, [], []


def send_slack_message(webhook_url, total_tests, total_failures, failed_tests, passed_tests):
    headers = {'Content-Type': 'application/json'}

    # Рассчитываем количество пройденных тестов
    total_passed = total_tests - total_failures

    # Подготавливаем сообщение с использованием markdown
    message = (
        "_*ℹ️ TESTS RESULTS*_\n\n\n"
        f"TOTAL TESTS = {total_tests}\n\n"
        f"TOTAL PASSED = {total_passed}\n\n"
        f"TOTAL FAILED = {total_failures}\n\n\n"
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
        "mrkdwn": True  # Включаем рендеринг markdown
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Не удалось отправить сообщение в Slack: {response.status_code}, {response.text}")
    else:
        print("Сообщение в Slack отправлено успешно!")


if __name__ == "__main__":
    file_path = 'results/test-results.xml'  # Путь к вашему XML файлу с результатами тестов
    total_tests, total_failures, failed_tests, passed_tests = extract_test_results(file_path)

    # URL вебхука Slack
    webhook_url = cfg.SLACK_WEBHOOK

    # Отправляем сообщение в Slack с результатами тестов
    send_slack_message(webhook_url, total_tests, total_failures, failed_tests, passed_tests)
