#!/usr/bin/env python3
"""
FormDetails Tool - 主入口點
提供統一的命令列介面來執行 JSON 處理功能
"""

import sys
import argparse
from pathlib import Path

# 添加 src 目錄到 Python 路徑
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from merge_json import main as merge_main
from optimized_process_json import main as optimize_main


def main():
    """主函數 - 提供統一的命令列介面"""
    parser = argparse.ArgumentParser(
        description="FormDetails Tool - JSON 檔案處理工具集",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例用法:
  python -m formdetails_tool merge      # 執行 JSON 合併
  python -m formdetails_tool optimize   # 執行 C# 結構優化
  python -m formdetails_tool all       # 執行完整處理流程
        """
    )

    parser.add_argument(
        "command",
        choices=["merge", "optimize", "all"],
        help="要執行的命令"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="FormDetails Tool 1.0.0"
    )

    args = parser.parse_args()

    print("🚀 FormDetails Tool 啟動...")
    print("=" * 60)

    if args.command == "merge":
        print("📋 執行 JSON 合併功能...")
        merge_main()
    elif args.command == "optimize":
        print("⚡ 執行 C# 結構優化...")
        optimize_main()
    elif args.command == "all":
        print("🔄 執行完整處理流程...")
        print("\n步驟 1: JSON 合併")
        merge_main()
        print("\n步驟 2: C# 結構優化")
        optimize_main()

    print("=" * 60)
    print("✅ 處理完成！")


if __name__ == "__main__":
    main()
