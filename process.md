## 환경 설정

### 1. uv 설치

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