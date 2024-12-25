# Year-End Party Quiz Game 🎄🎮

연말 파티를 위한 인터랙티브 퀴즈 게임입니다. 문제가 타자기처럼 하나씩 나타나며, 참가자들이 함께 답을 맞추는 방식으로 진행됩니다.

웹에서도 사용 가능합니다. https://runningman-relay-quiz-game-8f0d96f722ee.herokuapp.com/

![Quiz Game Preview](preview.gif)

## ✨ 특징

- 🎯 타자기 효과로 문제가 하나씩 나타나는 인터랙티브한 출제 방식
- 🎲 매 게임마다 랜덤으로 섞이는 문제 순서
- 🎨 크리스마스와 연말 파티에 어울리는 화려한 UI
- 🎅 눈/폭죽 효과 등 다양한 시각적 요소
- 📱 모바일을 포함한 모든 디바이스 지원
- 🔄 실시간 소켓 통신으로 즉각적인 반응
- 📝 JSON 파일을 통한 손쉬운 문제 관리

## 🔧 시스템 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)
- 웹 브라우저 (Chrome, Firefox, Safari, Edge 등 최신 버전 권장)

## 📦 설치 방법

### Windows 사용자

1. 이 저장소를 다운로드하거나 클론합니다

```bash
git clone https://github.com/WoongTech/YearEndPartyQuiz
cd quiz-game
```

2. 동봉된 실행 스크립트를 실행합니다

```bash
run.bat
```

### macOS/Linux 사용자

1. 이 저장소를 다운로드하거나 클론합니다

```bash
git clone [repository-url]
cd quiz-game
```

2. 실행 스크립트에 실행 권한을 부여하고 실행합니다

```bash
chmod +x run.sh
./run.sh
```

### 수동 설치 (모든 운영체제)

1. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

3. 게임 실행

```bash
python app.py
```

## 🎮 게임 실행 방법

1. 설치 완료 후 자동으로 웹 브라우저가 열립니다
2. 열리지 않는 경우 브라우저에서 다음 주소로 접속:
   - 로컬 접속: http://localhost:5000
   - 네트워크 접속: http://[컴퓨터IP]:5000

## 🎯 게임 진행 방법

1. **시작하기**: "Start" 버튼을 클릭하여 문제 출제 시작
2. **문제 확인**: 카테고리가 표시된 후 문제가 한 글자씩 나타남
3. **답변**: 참가자들이 함께 답을 맞추기
4. **정답 확인**: "Show Answer" 버튼으로 정답 확인
5. **다음 문제**: "Next" 버튼으로 다음 문제로 이동

## 📝 문제 수정 방법

`quiz_data.json` 파일을 수정하여 문제를 추가하거나 변경할 수 있습니다:

```json
{
  "questions": [
    {
      "category": "카테고리명",
      "text": "문제 내용을 여기에 작성합니다.\n여러 줄로 작성 가능합니다.",
      "answer": "정답"
    }
  ]
}
```

## 🔧 문제 해결

1. **포트 5000번이 이미 사용 중인 경우**

   - app.py 파일에서 port 번호를 변경하여 사용 (예: 5001, 8000 등)

2. **한글 깨짐 발생 시**

   - 모든 파일이 UTF-8 인코딩으로 저장되었는지 확인

3. **모듈 설치 오류 발생 시**
   - pip를 최신 버전으로 업그레이드 후 재시도
   ```bash
   python -m pip install --upgrade pip
   ```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🤝 기여하기

1. 이 저장소를 포크합니다
2. 새로운 브랜치를 생성합니다
3. 변경사항을 커밋합니다
4. 브랜치에 푸시합니다
5. Pull Request를 생성합니다

## 📮 문의사항

문제점을 발견하셨거나 기능 제안이 있으시다면 GitHub Issues에 등록해 주세요.
