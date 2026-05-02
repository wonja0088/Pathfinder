"""두 컬럼(곱할 값/기준 값)으로 설계 데이터를 만드는 CSV 변환 스크립트.

실행 환경:
    - Python 3.10+ (추가 패키지 설치 불필요)

사용 예시:
    python convert_experiment_to_design.py --input input.csv --output design.csv

입력 CSV 기본 컬럼명:
    - multiplier
    - base

출력 CSV:
    - multiplier,base,design
      (design = multiplier * base)
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="두 컬럼을 곱해 설계 데이터 CSV를 생성합니다."
    )
    parser.add_argument("--input", required=True, help="입력 CSV 파일 경로")
    parser.add_argument("--output", required=True, help="출력 CSV 파일 경로")
    parser.add_argument(
        "--left-column",
        default="multiplier",
        help="곱셈의 왼쪽 컬럼명(기본값: multiplier)",
    )
    parser.add_argument(
        "--right-column",
        default="base",
        help="곱셈의 오른쪽 컬럼명(기본값: base)",
    )
    parser.add_argument(
        "--result-column",
        default="design",
        help="결과 컬럼명(기본값: design)",
    )
    return parser.parse_args()


def convert_rows(
    rows: Iterable[dict[str, str]],
    left_column: str,
    right_column: str,
    result_column: str,
) -> list[dict[str, str | float]]:
    converted: list[dict[str, str | float]] = []

    for index, row in enumerate(rows, start=1):
        if left_column not in row or right_column not in row:
            raise ValueError(
                f"{index}번째 행에 필요한 컬럼이 없습니다: "
                f"{left_column!r}, {right_column!r}"
            )

        left = float(row[left_column])
        right = float(row[right_column])
        product = left * right

        out_row: dict[str, str | float] = dict(row)
        out_row[result_column] = product
        converted.append(out_row)

    return converted


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with input_path.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        if reader.fieldnames is None:
            raise ValueError("입력 CSV에 헤더가 없습니다.")

        converted_rows = convert_rows(
            rows=reader,
            left_column=args.left_column,
            right_column=args.right_column,
            result_column=args.result_column,
        )

    fieldnames = list(converted_rows[0].keys()) if converted_rows else [
        args.left_column,
        args.right_column,
        args.result_column,
    ]

    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(converted_rows)

    print(f"변환 완료: {output_path}")


if __name__ == "__main__":
    main()
