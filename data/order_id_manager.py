import logging
import os
import xml.etree.ElementTree as ET
import re


class OrderIDManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self._initialize_file()

    def _initialize_file(self):
        # Создаем директорию, если ее нет
        dir_name = os.path.dirname(self.file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Если файла нет, создаем новый файл с корневым элементом
        if not os.path.exists(self.file_path):
            root = ET.Element("orders")
            tree = ET.ElementTree(root)
            tree.write(self.file_path)

    def update_order_id(self, test_name, order_id):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        # Удаляем старую запись, если существует
        for elem in root.findall('order'):
            if elem.get('test_name') == test_name:
                root.remove(elem)

        # Добавляем новую запись
        order_elem = ET.SubElement(root, 'order', test_name=test_name, order_id=order_id)
        tree.write(self.file_path)

    def get_order_ids(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return {elem.get('test_name'): elem.get('order_id') for elem in root.findall('order')}

    def validate_order_id(self, page_url: str, test_name: str) -> bool:
        """
        Проверяет, что Order ID не попадает в диапазон 700000-701000 и обновляет order_id_manager.

        :param page_url: URL страницы, содержащий Order ID.
        :param test_name: Название теста для обновления order_id_manager.
        :return: True если проверка прошла, False если Order ID в диапазоне 700000-701000.
        """
        match = re.search(r"/confirm-order/(\d+)/", page_url)
        if match:
            order_id = match.group(1)
            self.update_order_id(test_name, order_id)
            if 700000 <= int(order_id) <= 701000:
                return False
            return True
        else:
            raise ValueError("Order ID не найден в URL")
