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
