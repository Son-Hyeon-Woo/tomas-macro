# tomas-macro

Korean Tomas bro (SRT/KTX)에게 명령을 내리는 GUI 기반 매크로 프로그램

## Architecture

BE: Python Eel
FE: JS Svelte

---

CSS lib : shadcn-svelte

## Connet Eel and Svelte in Dev Env

빌드 후에는 문제가 되지 않겠지만(static한 파일이 생성되니깐 빌드한 파일을 eel 프로젝트로 이동해주면 됨)
front 개발 중이라면 svelte 개발서버에서 eel.js를 import 하지 못해 매번 빌드후에 디버깅해야하는 어려움이 있다.
그래서 개발환경에서는

> 1.  eel을 실행
> 2.  vite.config 에서 eel.js 경로에 대해서 proxy 설정을 수정하여 localhost:8000을 참조하도록 수정함 (Eel 실행시 localhost:8000에 eel.js 자동으로 생성됨)
> 3.  같은 원리로 웹소켓 (web과 python 사이의 연결) 경로도 proxy에 추가해줌

이렇게 해결했다.
