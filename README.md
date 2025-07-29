## 환경 설정
- git clone 후 폴더 내 .env 파일 생성, openai api 키 등록 필요
- aws에서 chromadb의 인스턴스인 i-012f43937d17035e8 id 의 인스턴스에서 보안그룹 편집 필요
- 본인 컴퓨터 공인 IP를 8000포트 인바운드 규칙에 추가 (일정 시간 이후 공인 IP가 바뀌는 경우 매번 바꿔줘야 하는듯)


## chromadb 테스트
1. chroma_test/app 경로에서 npm run dev 실행
2. connect_chroma.py 파일이 있는 경로에서 uvicorn connect_chroma:app --reload --port 9000 실행
3. http://localhost:3000 접속 시 아래의 화면 확인 가능
4. <img width="716" height="307" alt="스크린샷 2025-07-29 오후 7 58 16" src="https://github.com/user-attachments/assets/eef89717-b990-46e9-b08e-60b93cd23a09" />
   
