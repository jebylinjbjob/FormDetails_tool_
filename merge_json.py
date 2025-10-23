#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON檔案合併腳本
功能：將append_json.json中的內容合併到add資料夾中JSON檔案的formFields陣列
"""

import json
import os
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('merge_json.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class JSONMerger:
    """JSON檔案合併器"""

    def __init__(self, append_file="append_json.json", input_dir="add", output_dir="out"):
        """
        初始化合併器

        Args:
            append_file (str): 要合併的JSON檔案名稱
            input_dir (str): 輸入資料夾路徑
            output_dir (str): 輸出資料夾路徑
        """
        self.append_file = Path(append_file)
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

        # 確保輸出資料夾存在
        self.output_dir.mkdir(exist_ok=True)

    def load_append_data(self) -> Optional[List[Dict[str, Any]]]:
        """
        載入要合併的JSON資料

        Returns:
            list: 要合併的formFields列表，失敗時返回None
        """
        try:
            if not self.append_file.exists():
                logging.error(f"合併檔案不存在: {self.append_file}")
                return None

            with open(self.append_file, 'r', encoding='utf-8') as f:
                # 讀取檔案內容
                content = f.read().strip()

                # 處理可能的格式問題（移除末尾的逗號）
                if content.endswith(','):
                    content = content[:-1]

                # 嘗試解析為JSON陣列
                try:
                    append_data = json.loads(f"[{content}]")
                except json.JSONDecodeError:
                    # 如果不是陣列格式，嘗試解析為單一物件
                    append_data = json.loads(content)
                    if not isinstance(append_data, list):
                        append_data = [append_data]

            logging.info(f"成功載入 {len(append_data)} 個要合併的formFields")
            return append_data

        except json.JSONDecodeError as e:
            logging.error(f"JSON解析錯誤 {self.append_file}: {e}")
            return None
        except Exception as e:
            logging.error(f"載入合併檔案時發生錯誤 {self.append_file}: {e}")
            return None

    def merge_form_fields(self, original_form_fields: List[Dict[str, Any]],
                         append_form_fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        合併formFields陣列

        Args:
            original_form_fields (list): 原始的formFields
            append_form_fields (list): 要新增的formFields

        Returns:
            list: 合併後的formFields
        """
        # 複製原始陣列
        merged_fields = original_form_fields.copy()

        # 新增要合併的欄位
        merged_fields.extend(append_form_fields)

        logging.info(f"合併完成：原有 {len(original_form_fields)} 個欄位，新增 {len(append_form_fields)} 個欄位，總計 {len(merged_fields)} 個欄位")

        return merged_fields

    def process_json_file(self, file_path: Path, append_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        處理單個JSON檔案

        Args:
            file_path (Path): JSON檔案路徑
            append_data (list): 要合併的資料

        Returns:
            dict: 處理後的資料，失敗時返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logging.info(f"正在處理檔案: {file_path.name}")

            # 檢查是否有forms陣列
            if "forms" not in data or not data["forms"]:
                logging.warning(f"檔案 {file_path.name} 沒有forms陣列，跳過處理")
                return None

            # 處理每個form
            for form in data["forms"]:
                if "formFields" in form and form["formFields"]:
                    # 合併formFields
                    form["formFields"] = self.merge_form_fields(form["formFields"], append_data)
                else:
                    # 如果沒有formFields，直接新增
                    form["formFields"] = append_data.copy()

            return data

        except json.JSONDecodeError as e:
            logging.error(f"JSON解析錯誤 {file_path.name}: {e}")
            return None
        except Exception as e:
            logging.error(f"處理檔案時發生錯誤 {file_path.name}: {e}")
            return None

    def save_processed_file(self, processed_data: Dict[str, Any], original_filename: str):
        """
        儲存處理後的檔案

        Args:
            processed_data (dict): 處理後的資料
            original_filename (str): 原始檔案名稱
        """
        output_path = self.output_dir / original_filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)

            logging.info(f"已儲存合併後的檔案: {output_path}")

        except Exception as e:
            logging.error(f"儲存檔案時發生錯誤 {output_path}: {e}")

    def merge_all_files(self):
        """
        合併所有JSON檔案
        """
        # 載入要合併的資料
        append_data = self.load_append_data()
        if append_data is None:
            logging.error("無法載入合併資料，終止處理")
            return

        # 檢查輸入資料夾是否存在
        if not self.input_dir.exists():
            logging.error(f"輸入資料夾不存在: {self.input_dir}")
            return

        # 尋找所有JSON檔案
        json_files = list(self.input_dir.glob("*.json"))

        if not json_files:
            logging.warning(f"在 {self.input_dir} 中沒有找到JSON檔案")
            return

        logging.info(f"找到 {len(json_files)} 個JSON檔案")

        # 處理每個檔案
        processed_count = 0

        for json_file in json_files:
            processed_data = self.process_json_file(json_file, append_data)

            if processed_data is not None:
                self.save_processed_file(processed_data, json_file.name)
                processed_count += 1

        logging.info(f"合併完成！成功處理 {processed_count}/{len(json_files)} 個檔案")

def main():
    """
    主函數
    """
    print("JSON檔案合併腳本啟動...")
    print("=" * 60)
    print("功能：將append_json.json的內容合併到add資料夾中JSON檔案的formFields")
    print("=" * 60)

    # 創建合併器實例
    merger = JSONMerger()

    # 執行合併
    merger.merge_all_files()

    print("=" * 60)
    print("合併完成！請檢查out資料夾中的結果。")

if __name__ == "__main__":
    main()
