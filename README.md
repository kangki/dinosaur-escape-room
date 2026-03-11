# Dinosaur Escape Room

2D 플랫폼 스타일 미니 게임입니다.  
플레이어 캐릭터를 이동/점프해서 발판을 타고 아이템을 획득하는 구조입니다.

## 프로그램 설명

- 배경, 발판, 캐릭터 스프라이트 기반의 단일 윈도우 게임
- 체력(HP)이 시간에 따라 감소
- 아이템 획득 시 HP 리셋

### 조작 방법

- `Left`: 왼쪽 이동
- `Right`: 오른쪽 이동
- `Space`: 점프 (이동 중 점프 시 캐릭터 스킨 변경)
- `Esc`: 종료 확인

## 설치 방법

### 1) 가상환경 생성 및 활성화 (권장)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) 프로젝트 설치 (editable)

```powershell
python -m pip install -e .
```

## 실행 방법

아래 둘 중 하나를 사용합니다.

### 방법 A: 콘솔 스크립트 실행

```powershell
dino-escape
```

### 방법 B: 모듈 직접 실행

```powershell
python -m dino_escape_room.main
```
