import logging
# 로그를 찍기 위한 파이썬 기본 모듈
# print보다 더 체계적 출력 가능
# Logger (총괄 관리자)
#  ├── Handler (출력 담당)
#  │     └── Formatter (출력 형식 담당)

# | 구성요소    | 역할                                     
# | --------- | ------------------------------------    
# | Logger    | 로그를 생성 (logger.info, logger.error 등) 
# | Handler   | 어디에 출력할지 결정 (콘솔, 파일 등)            
# | Formatter | 출력 형식 결정                             

from google.cloud import bigquery
import os
def create_client(key_path):
    return bigquery.Client.from_service_account_json(key_path)

# [출처(name), 형식(format), 출력 위치(handler)를 정의한 로그 시스템을 만드는 과정]
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # logger가 어느 수준 이상의 로그를 보여줄지 정하는 것
    # INFO로 설정하면 logger.info(), warning(), error() 보임

    if not logger.handlers:
        # handler: 로그를 어디에 어떻게 출력할지 담당하는 장치
        handler=logging.StreamHandler()
        # 로그를 터미널(콘솔)에 출력하는 핸들러 만듦 _ print처럼 화면에 보이게
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger