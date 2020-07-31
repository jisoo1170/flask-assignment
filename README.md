# flask-assignment

**필수 기술 스택**

- Flask
- PyMongo or MongoEngine

**스펙**

- 게시판 목록
- 글쓰기, 수정
- 읽기
- 회원가입/로그인
- 내 정보 수정, 삭제
- 마이페이지 - 내가 쓴 글, 댓글, 대댓글 조회
- 댓글
- 대댓글
- 태그
- 태그 검색
- 글, 댓글, 대댓글 좋아요

## Step2
**깔끔한 명세 만들기**
- Rest API
- Board → Post
- 필드명
- 클래스의 Input/Output

**Test Code**
- 라이브러리
    - pytest
    - factoryboy
    - mongomock 등
- 환경설정
    - TestConfig 생성
    - env 변수를 보고 적절한 Config Load
    - library 추가 : mongomock, pytest류

**패키지 매니져 변경**
- poetry