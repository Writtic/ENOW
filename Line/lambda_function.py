#!/usr/bin/python
#-*- encoding: utf-8 -*-
# 로그를 기록하기 위한 메소드

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
"""
Lambda > Functions > 내 함수 > Configuration > Handler 에서 input을
[파일명.메소드명]으로 한다.
예시 : lambda_function.lambda_handler
"""

def lambda_handler(event, context):
    # 이벤트 로그를 기록
    logger.info('got event{}'.format(event))
    # event는 딕셔너리형태로 넘어옴. 커멘드(/wiki) 뒤의 텍스트를 받아오려면 event['text']
    text = event['text']
    # 리턴은 JSON 타입으로 맞춰준다.
    return {
        "response_type": "in_channel",
        "text": "I found some about \"" + text + "\"",
        "attachments": [
            {
                "text": "For more info please visit to \nhttps://ko.wikipedia.org/wiki/" + text,
                "color": "#7CD197"
            }
        ]
    }
