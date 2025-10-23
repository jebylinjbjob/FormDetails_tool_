#!/usr/bin/env python3
"""
測試檔案 - JSONMerger 類別
"""

import json
import tempfile
from pathlib import Path

import pytest

from merge_json import JSONMerger


class TestJSONMerger:
    """JSONMerger 類別測試"""

    def setup_method(self):
        """每個測試方法前的設定"""
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = Path(self.temp_dir) / "add"
        self.output_dir = Path(self.temp_dir) / "out"
        self.append_file = Path(self.temp_dir) / "append_json.json"

        # 建立輸入資料夾
        self.input_dir.mkdir()
        self.output_dir.mkdir()

    def teardown_method(self):
        """每個測試方法後的清理"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """測試初始化"""
        merger = JSONMerger(
            append_file=str(self.append_file),
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )

        assert merger.append_file == self.append_file
        assert merger.input_dir == self.input_dir
        assert merger.output_dir == self.output_dir
        assert self.output_dir.exists()

    def test_load_append_data_success(self):
        """測試成功載入合併資料"""
        # 建立測試資料
        test_data = {
            "fieldName": "測試欄位",
            "fieldType": "dxTextBox",
            "isReadonly": True,
            "isVisible": False
        }

        with open(self.append_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        merger = JSONMerger(
            append_file=str(self.append_file),
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )

        result = merger.load_append_data()
        assert result is not None
        assert len(result) == 1
        assert result[0]["fieldName"] == "測試欄位"

    def test_load_append_data_file_not_exists(self):
        """測試檔案不存在的情況"""
        merger = JSONMerger(
            append_file=str(self.append_file),
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )

        result = merger.load_append_data()
        assert result is None

    def test_merge_form_fields(self):
        """測試合併 formFields"""
        original_fields = [
            {"fieldName": "原始欄位1", "fieldType": "dxTextBox"},
            {"fieldName": "原始欄位2", "fieldType": "dxSelectBox"}
        ]

        append_fields = [
            {"fieldName": "新增欄位1", "fieldType": "dxDateBox"},
            {"fieldName": "新增欄位2", "fieldType": "dxNumberBox"}
        ]

        merger = JSONMerger(
            append_file=str(self.append_file),
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )

        result = merger.merge_form_fields(original_fields, append_fields)

        assert len(result) == 4
        assert result[0]["fieldName"] == "原始欄位1"
        assert result[1]["fieldName"] == "原始欄位2"
        assert result[2]["fieldName"] == "新增欄位1"
        assert result[3]["fieldName"] == "新增欄位2"

    def test_process_json_file_success(self):
        """測試成功處理 JSON 檔案"""
        # 建立測試 JSON 檔案
        test_json_data = {
            "forms": [
                {
                    "formId": "test_form",
                    "formName": "測試表單",
                    "formFields": [
                        {"fieldName": "原始欄位", "fieldType": "dxTextBox"}
                    ]
                }
            ]
        }

        test_file = self.input_dir / "test.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_json_data, f, ensure_ascii=False, indent=2)

        # 建立合併資料
        append_data = [{"fieldName": "新增欄位", "fieldType": "dxSelectBox"}]

        merger = JSONMerger(
            append_file=str(self.append_file),
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )

        result = merger.process_json_file(test_file, append_data)

        assert result is not None
        assert "forms" in result
        assert len(result["forms"]) == 1
        assert len(result["forms"][0]["formFields"]) == 2

    def test_process_json_file_no_forms(self):
        """測試沒有 forms 陣列的檔案"""
        test_json_data = {"otherData": "test"}

        test_file = self.input_dir / "test.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_json_data, f, ensure_ascii=False, indent=2)

        append_data = [{"fieldName": "新增欄位", "fieldType": "dxSelectBox"}]

        merger = JSONMerger(
            append_file=str(self.append_file),
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )

        result = merger.process_json_file(test_file, append_data)
        assert result is None

    def test_save_processed_file(self):
        """測試儲存處理後的檔案"""
        test_data = {
            "forms": [
                {
                    "formId": "test_form",
                    "formName": "測試表單",
                    "formFields": []
                }
            ]
        }

        merger = JSONMerger(
            append_file=str(self.append_file),
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )

        merger.save_processed_file(test_data, "test_output.json")

        output_file = self.output_dir / "test_output.json"
        assert output_file.exists()

        with open(output_file, encoding='utf-8') as f:
            saved_data = json.load(f)

        assert saved_data == test_data


if __name__ == "__main__":
    pytest.main([__file__])
