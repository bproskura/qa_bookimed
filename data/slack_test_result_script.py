import sys
import os

# Добавляем путь к каталогу с cfg.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import xml.etree.ElementTree as ET
import requests
import cfg

def extract_order_ids(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        order_ids = {}

        # Проходимся по каждому order
        for order in root.findall('order'):
            test_name = order.get('test_name')
            order_id = order.get('order_id', 'N/A')
            order_ids[test_name] = order_id

        return order_ids

    except ET.ParseError as e:
        print(f"Ошибка парсинга XML файла: {e}")
        return {}

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
                test_name = testcase.get('name')
                if testcase.find('failure') is not None:
                    failed_tests.append(test_name)
                else:
                    passed_tests.append(test_name)

        return total_tests, total_failures, failed_tests, passed_tests

    except ET.ParseError as e:
        print(f"Ошибка парсинга XML файла: {e}")
        return 0, 0, [], []

def send_slack_message(webhook_url, total_tests, total_failures, failed_tests, passed_tests, order_ids):
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
        order_id = order_ids.get(test, 'N/A')
        message += f"   :white_check_mark: {test} (Order ID: {order_id})\n\n\n"

    message += "*FAILED TESTS:*\n\n"
    for test in failed_tests:
        order_id = order_ids.get(test, 'N/A')
        message += f"   :x: {test} (Order ID: {order_id})\n\n"
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
    # Вывод текущей рабочей директории
    print(f"Current working directory: {os.getcwd()}")

    # Определение путей к файлам относительно корня проекта
    results_file_path = '../results/test-results.xml'  # Путь к вашему XML файлу с результатами тестов
    order_ids_file_path = '../results/order_ids.xml'  # Путь к файлу с order_ids

    # Вывод абсолютных путей к файлам
    print(f"Results file absolute path: {os.path.abspath(results_file_path)}")
    print(f"Order IDs file absolute path: {os.path.abspath(order_ids_file_path)}")

    # Проверяем существование файла с результатами тестов
    if os.path.exists(results_file_path):
        total_tests, total_failures, failed_tests, passed_tests = extract_test_results(results_file_path)
    else:
        print(f"Файл {results_file_path} не найден. Пропускаем извлечение результатов тестов.")
        total_tests, total_failures, failed_tests, passed_tests = 0, 0, [], []

    # Проверяем существование файла с order_ids
    if os.path.exists(order_ids_file_path):
        order_ids = extract_order_ids(order_ids_file_path)
    else:
        print(f"Файл {order_ids_file_path} не найден. Пропускаем извлечение order_ids.")
        order_ids = {}

    # URL вебхука Slack
    webhook_url = cfg.SLACK_WEBHOOK

    # Отправляем сообщение в Slack с результатами тестов
    send_slack_message(webhook_url, total_tests, total_failures, failed_tests, passed_tests, order_ids)
