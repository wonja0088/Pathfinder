# Pathfinder CSV 변환 스크립트 실행 가이드

이 저장소의 `convert_experiment_to_design.py`는 **CSV의 두 컬럼을 곱해서**
결과 컬럼(기본값 `design`)을 추가한 새 CSV를 생성합니다.

## 1) 권장 실행 환경

- **Python 3.10 이상** (3.11/3.12 권장)
- 추가 패키지 설치 **불필요** (표준 라이브러리만 사용)
- 운영체제: macOS / Linux / Windows 모두 가능

## 2) 빠른 실행

```bash
python convert_experiment_to_design.py \
  --input input_values.csv \
  --output design_values.csv
```

기본 계산식:
- `design = multiplier * base`

## 3) 컬럼명 변경해서 실행

입력 CSV의 컬럼명이 다르면 아래처럼 지정할 수 있습니다.

```bash
python convert_experiment_to_design.py \
  --input your_input.csv \
  --output your_output.csv \
  --left-column 곱할열1 \
  --right-column 곱할열2 \
  --result-column 결과열명
```

## 4) 입력 CSV 형식

- 헤더가 반드시 있어야 합니다.
- 기본 헤더 예시:

```csv
multiplier,base
2.6,4
3,620
```

## 5) 에러가 나는 경우

- `입력 CSV에 헤더가 없습니다.`: 헤더 행(첫 줄 컬럼명)을 추가하세요.
- `필요한 컬럼이 없습니다`: `--left-column`, `--right-column` 옵션과 실제 CSV 헤더를 맞추세요.
