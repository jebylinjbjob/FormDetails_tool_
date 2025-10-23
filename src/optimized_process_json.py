#!/usr/bin/env python3
"""
JSON檔案處理腳本 - 針對C# FormDetail類別結構優化
功能：處理add資料夾中的JSON檔案，確保輸出符合C#類別定義
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('process_json.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class FormFieldProcessor:
    """FormField處理器，對應C# FormField類別"""

    @staticmethod
    def process_form_field(field_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        處理單個FormField，確保符合C#類別定義

        Args:
            field_data (dict): 原始欄位資料

        Returns:
            dict: 處理後的欄位資料
        """
        processed_field = {}

        # 必填欄位
        processed_field["formFieldId"] = field_data.get("formFieldId", "")
        processed_field["fieldName"] = field_data.get("fieldName", "")
        processed_field["fieldType"] = field_data.get("fieldType", "")
        processed_field["isReadonly"] = field_data.get("isReadonly", False)
        processed_field["isVisible"] = field_data.get("isVisible", False)
        processed_field["infoDisplayCondition"] = field_data.get("infoDisplayCondition", False)
        processed_field["sort"] = field_data.get("sort", 0)
        processed_field["specialFieldCode"] = field_data.get("specialFieldCode", "")

        # 可選欄位 - 只保留非空值
        if field_data.get("defaultValue") is not None:
            processed_field["defaultValue"] = field_data["defaultValue"]

        if field_data.get("relatedSource") is not None:
            processed_field["relatedSource"] = field_data["relatedSource"]

        if field_data.get("fieldOptions") and len(field_data["fieldOptions"]) > 0:
            processed_field["fieldOptions"] = field_data["fieldOptions"]

        if field_data.get("fieldGroup"):
            processed_field["fieldGroup"] = field_data["fieldGroup"]

        if field_data.get("parentField"):
            processed_field["parentField"] = field_data["parentField"]

        if field_data.get("displayCondition") is not None:
            processed_field["displayCondition"] = field_data["displayCondition"]

        if field_data.get("relatedFormsExtend"):
            processed_field["relatedFormsExtend"] = field_data["relatedFormsExtend"]

        if field_data.get("flowNodeCode"):
            processed_field["flowNodeCode"] = field_data["flowNodeCode"]

        # 處理擴展資料 (ExtensionData)
        extension_fields = {}
        for key, value in field_data.items():
            if key not in processed_field and value is not None and key in ["colSpan", "translation"]:
                # 保留額外的欄位作為擴展資料
                extension_fields[key] = value

        if extension_fields:
            processed_field["extensionData"] = extension_fields

        return processed_field

class FormProcessor:
    """Form處理器，對應C# Form類別"""

    @staticmethod
    def process_form(form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        處理單個Form，確保符合C#類別定義

        Args:
            form_data (dict): 原始表單資料

        Returns:
            dict: 處理後的表單資料
        """
        processed_form = {}

        # 必填欄位
        processed_form["formId"] = form_data.get("formId", "")
        processed_form["formName"] = form_data.get("formName", "")
        processed_form["description"] = form_data.get("description", "")

        # 處理FormFields
        if "formFields" in form_data and form_data["formFields"]:
            processed_form["formFields"] = [
                FormFieldProcessor.process_form_field(field)
                for field in form_data["formFields"]
            ]
        else:
            processed_form["formFields"] = []

        # 處理FieldGroups
        if "fieldGroups" in form_data and form_data["fieldGroups"]:
            processed_form["fieldGroups"] = form_data["fieldGroups"]
        else:
            processed_form["fieldGroups"] = []

        return processed_form

class FormDetailProcessor:
    """FormDetail處理器，對應C# FormDetail類別"""

    def __init__(self, input_dir="add", output_dir="out"):
        """
        初始化處理器

        Args:
            input_dir (str): 輸入資料夾路徑
            output_dir (str): 輸出資料夾路徑
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

        # 確保輸出資料夾存在
        self.output_dir.mkdir(exist_ok=True)

    def process_form_detail(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        處理FormDetail資料，確保符合C#類別定義

        Args:
            data (dict): 原始資料

        Returns:
            dict: 處理後的資料
        """
        processed_data = {}

        # 處理Forms陣列
        if "forms" in data and data["forms"]:
            processed_data["forms"] = [
                FormProcessor.process_form(form)
                for form in data["forms"]
            ]
        else:
            processed_data["forms"] = []

        return processed_data

    def process_json_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        處理單個JSON檔案

        Args:
            file_path (Path): JSON檔案路徑

        Returns:
            dict: 處理後的資料，失敗時返回None
        """
        try:
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)

            logging.info(f"正在處理檔案: {file_path.name}")

            # 處理資料
            processed_data = self.process_form_detail(data)

            return processed_data

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

            logging.info(f"已儲存處理後的檔案: {output_path}")

        except Exception as e:
            logging.error(f"儲存檔案時發生錯誤 {output_path}: {e}")

    def process_all_files(self):
        """
        處理所有JSON檔案
        """
        if not self.input_dir.exists():
            logging.error(f"輸入資料夾不存在: {self.input_dir}")
            return

        json_files = list(self.input_dir.glob("*.json"))

        if not json_files:
            logging.warning(f"在 {self.input_dir} 中沒有找到JSON檔案")
            return

        logging.info(f"找到 {len(json_files)} 個JSON檔案")

        processed_count = 0

        for json_file in json_files:
            processed_data = self.process_json_file(json_file)

            if processed_data is not None:
                self.save_processed_file(processed_data, json_file.name)
                processed_count += 1

        logging.info(f"處理完成！成功處理 {processed_count}/{len(json_files)} 個檔案")

def main():
    """
    主函數
    """
    print("JSON檔案處理腳本啟動...")
    print("針對C# FormDetail類別結構優化")
    print("=" * 60)

    # 創建處理器實例
    processor = FormDetailProcessor()

    # 處理所有檔案
    processor.process_all_files()

    print("=" * 60)
    print("處理完成！請檢查out資料夾中的結果。")
    print("處理後的JSON檔案已優化以符合C#類別定義。")

if __name__ == "__main__":
    main()
