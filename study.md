# 환경 설정

## 1. uv 설치

[uv](https://docs.astral.sh/uv/)는 Python 패키지/프로젝트 매니저

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```
> - **curl**: Client URL\
    URL로부터 데이터를 가져오는 클라이언트 도구

> - **LsSf**
>   - **L**: Location\
>        redirect된 위치로 따라가라
>   - **s**: Silent\
>        조용히 실행 progress bar 숨김
>   - **S**: Show Error\
>        -s랑 같이 써야 의미 있음\
>        에러는 보여줘라
>   - **f**: Fail\
>        HTTP error시 실패 처리\
>        404,500 나오면 출력 안 하고 종료

> - **https** = HyperText Transfer Protocol Secure
>   - hypertext: 문서 안에서 다른 문서로 연결(link) 할 수 있는 text 구조 = 링크를 통한 비선형 구조

> **| (pipe)**\
>   unix 개념 _ 앞 program 출력 -> 뒤 program 입력

> **sh**\
> Shell 실행기
> shell script 실행하는 program

```
curl (Client URL)
-L (Location 따라가고)
-s (Silent 모드로)
-S (Show Error는 유지하고)
-f (Fail 시 종료하면서)
URL에서 install.sh (Shell script)를 가져와서
|
sh (Shell)로 바로 실행
```

## 2. project setting
**uv sync**
(uv.lock)

```
[uv 공식문서 (Astral Docs)]

> “An extremely fast Python package and project manager, written in Rust.”

   Rust
   - C/C++처럼 빠른 시스템 프로그래밍 언어
   - 메모리 안전성 
   - 성능 + 안정성 둘 다 잡은 언어
```
uv는 보통 따로따로 하던 것들을 한데 묶음
- python 버전 설치: 
    ```
    uv python install
    ```
- 가상환경 생성/관리
- 패키지 설치
- 프로젝트 의존성 관리
- 잠금 파일 생성
- 스크립트 실행
- 프로젝트 실행

**before uv**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

**after uv**
```bash
uv sync
uv run app.py
```

1) **requirements.txt는 파일일 뿐, 환경 관리자는 아니라**
- 어떤 Python 버전(requirements는 패키지 목록 파일임_환경 설정서가 아니라)을 써야 하는지
- 가상환경을 어떻게 만들지
- 팀원마다 같은 환경이 보장되는지
- 잠금된 재현 가능한 환경을 어떻게 유지할지 등의 문제 직접 해결 불가

    반면 uv는 pyproject.toml, uv.lock, .venv, Python 버전 요구사항까지 포함한 프로젝트 단위 관리 흐름을 제공
    공식 문서도 프로젝트는 pyproject.toml(toml: Tom's Obvious, Minimal Language_설정config 파일을 쓰기 위한 포맷) 기반으로 관리하고, requires-python 설정을 권장

    > **toml**\
    > =로 값 할당\
    > [section]으로 그룹 나눔

2) **재현성 측면**\
    requirements.txt는 잘 쓰면 어느 정도 재현 가능하지만, 프로젝트 전체 맥락까지 강하게 묶어주진 않는다. uv는 프로젝트용 uv.lock을 두고, 스크립트도 별도로 lock할 수 있게 제공한다. 공식 문서에서 프로젝트에는 uv.lock이 생성되고, 스크립트도 uv lock --script로 잠글 수 있다고 안내한다.
    
    ```
    uv는 dependency를 “고정(lock)”해서 항상 같은 환경을 재현하게 만든다
    그리고 그걸 두 가지 방식으로 제공함:

    - 프로젝트 단위 → uv.lock
    - 스크립트 단위 → uv lock --script

    [lock]

    requests >=2.0 
    이렇게 재현성 깨질 수 있게 말고

    requests==2.31.0
    urllib3==1.26.18
    ...
    => 정확한 버전 + 의존성까지 완전히 고정
    ```
3) **기본적으로 격리된 환경을 유도**

    공식 문서에 따르면 uv는 pip와 달리 기본적으로 가상환경 사용을 요구한다. 

4) **스크립트 실행도 편하다**

    단순 프로젝트뿐 아니라 단일 스크립트도 uv run으로 실행하면서 의존성을 관리할 수 있다

[정리]

- requirements.txt = 의존성 목록 파일
- pip = 패키지 설치 도구
- venv = 가상환경 도구
- uv = 위 여러 흐름을 더 통합적으로 다루는 빠른 패키지/프로젝트 관리자

    | 항목        | 기존 방식            | uv                       |
    | --------- | ---------------- | ------------------------ |
    | 패키지 설치    | pip              | uv                       |
    | 가상환경      | venv             | 자동 관리                    |
    | 의존성 파일    | requirements.txt | pyproject.toml + uv.lock |
    | Python 버전 | 별도 관리            | uv에서 관리                  |
    | 속도        | 보통               | 매우 빠름                    |

## 3. GCP 서비스 계정 키 
    환경변수 'GCP_KEY_PATH'에 키 파일 경로 설정

## 4. GitHub token
    repo metadata 수집 시 github api 사용
    gh가 CLI login되어 있으면 자동으로 토큰 가져올 수 있음

**GitHub API**
> API: Appilication Programming Interface
> REST API: Representational State Transfer

    [URL] = 무엇(resource)
        
        ex) 
        /users/1
        -> 의미: “유저 1번”

    [HTTP Method] = 무엇을 할지(action)

| Method | 의미    | 행동         |
| ------ | ----- | ---------- |
| GET    | 조회    | 유저 정보 가져오기 |
| POST   | 생성    | 유저 생성      |
| PUT    | 수정    | 유저 전체 수정   |
| PATCH  | 부분 수정 | 일부만 수정     |
| DELETE | 삭제    | 유저 삭제      |


옛날 방식:

    /getUser
    /deleteUser
    /updateUser

    -> URL에 동작까지 넣음 (비REST)

REST 방식:

    /users/1 + GET
    /users/1 + DELETE

    -> 역할 분리:

    URL → “대상”
    Method → “행동”

**HTTP method = CRUD 행동을 표현하는 표준**

    GET → Read
    POST → Create
    PUT/PATCH → Update
    DELETE → Delete

*“HTTP method로 행동 정의” = 같은 resource에 대해 어떤 작업을 할지 method로 구분한다는 뜻*

**GitHub REST API Structure**

    https://api.github.com/

    뒤에 resource를 붙여서 사용

    주요 endpoint
    /repos/{owner}/{repo}
    /issues
    /pulls
    /commits
    /contributors

    [예시]

        GET /repos/pandas-dev/pandas

        -> repository 기본 정보

        GET /repos/pandas-dev/pandas/issues

        -> issue 데이터

    
**Authentication**
GitHub API는 인증 없이도 사용 가능
- 인증 x: rate limit 낮음 (~60 요청/hour)
- 인증 o: rate limit 증가
(~5000 요청/hour)

**GitHub Token**
개인 인증 키
```bash
Authorization: Bearer <TOKEN>
```
**gh CLI**
```bash
gh auth login
```
로그인하면:
- 내부적으로 토큰 저장됨
- API 호출 시 자동 사용 가능

**Python에서 API 호출 예시**
```python
import requests
url = "https://api.github.com/repos/pandas-dev/pandas"
headers = {
    "Authorization":"Bearer YOUR_TOKEN",
    # Bearer token: 소지자에게 권한을 부여한다
    "Accept": "application/vnd.github+json"
}
response = requests.get(url, headers=headers)
data=response.json()
pritn(data["stargazrs_count"])
```
**API 호출 → 데이터 수집 전체 흐름**
1. GitHub API endpoint 선택
2. HTTP 요청 (GET)
3. JSON 응답 수신
4. 필요한 데이터 추출
5. 전처리 및 저장

**REST API vs 기타 API**
- REST API → 가장 기본적인 데이터 조회 방식
- GraphQL → 필요한 데이터만 정밀 조회
- Webhook → 이벤트 기반 자동 처리

**Why REST API?**

REST API는 URL 기반으로 자원이 명확하게 표현되어 있어\
repository, issue, commit 등의 데이터를 직관적으로 조회할 수 있고,\
현재 프로젝트에서는 단순 메타데이터 수집이 목적이었기 때문에 REST API로 충분

또한 GraphQL 대비 학습 비용이 낮고, endpoint 단위로 디버깅이 용이하다는 점에서
초기 개발 단계에서는 REST API가 더 적합하다고 판단했습니다.

추후 데이터 요청 구조가 복잡해질 경우 GraphQL 도입도 고려할 수 있음

> **REST** = 여러 endpoint에서 데이터 가져와서 조합\
> **GraphQL** = 한 번에 원하는 데이터만 정확히 가져옴

```
[REST API]

자원(Resource) 중심

    /repos/{owner}/{repo}
    /issues
    /commits
    URL = 데이터 위치
    HTTP method = 행동
```
```
[GraphQL]

Query 중심

    {
    repository(owner: "pandas-dev", name: "pandas") {
        stargazerCount
        issues(first: 5) {
        nodes {
            title
                }
            }
        }
    }
```

### 정밀 비교
**(1) 요청 횟수**
```
    [REST]
    (/repos/{owner}/{repo}
    /issues
    /commits)

    repo 정보 → 1번
    issues → 1번
    commits → 1번

    => 총 3번 요청

    URL = 데이터 위치
    HTTP method = 행동

----------------------------------------------------------------

    [GraphQL]
    {
        repository(owner: "pandas-dev", name: "pandas") {
            stargazerCount
            issues(first: 5) {
            nodes {
                title
            }
            }
        }
    }
    어떤 데이터가 필요한지 직접 정의
    => 한 번에 다 가져옴

    (네트워크 효율)
```
**(2) 데이터 낭비**
```
[REST]
{
  "id": 1,
  "name": "repo",
  "owner": "...",
  "url": "...",
  "created_at": "...",
  ...
}
=> 필요 없는 데이터까지 다 옴

[GraphQL]
{
  repository {
    name
  }
}
=> 필요한 것만 가져옴
```
**(3) Underfetching 문제**
```
[REST]
필요한 데이터가 여러 endpoint에 흩어짐

[GraphQL]
한 번에 해결
```
**(4) 학습 난이도**\
    ```REST is better```

**(5) Debugging**
```
[REST]
endpoint 단위로 문제 확인 가능

[GraphQL]
한 쿼리에 다 들어 있어서 문제 위치 파악 어려움
```

**(6) cashing**\
캐싱(Cache) = 이미 계산/요청한 결과를 저장해두고, 다시 쓰는 것

[REST]
> URL 기반 → 캐싱 쉬움

[GraphQL]
> 쿼리 기반 → 캐싱 어려움

**(7) 유연성**

[REST]
> 정해진 구조

[GraphQL]
> 원하는 구조로 요청 가능


| 항목     | REST API    | GraphQL  |
| ------ | ----------- | -------- |
| 구조     | resource 중심 | query 중심 |
| 요청 횟수  | 많음          | 적음       |
| 데이터 낭비 | 있음          | 없음       |
| 구현 난이도 | 쉬움          | 어려움      |
| 디버깅    | 쉬움          | 어려움      |
| 캐싱     | 쉬움          | 어려움      |
| 유연성    | 낮음          | 높음       |
