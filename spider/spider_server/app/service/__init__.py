from flask import current_app
SUCCESS = "SUCCESS" #成功
NOT_DATA = "NOT_DATA" #暂无数据
PROMPT_ERROR = "PROMPT_ERROR" #逻辑错误提示
TOKEN_ERROR = "TOKEN_ERROR" #token验证失败
EXCEPTION_ERROR = "EXCEPTION_ERROR" #代码异常错误

def return_exception_message(e):
    result = dict()
    current_app.logger.error('%s' % str(e))
    result["type"] = EXCEPTION_ERROR
    result["message"] = "服务异常！"
    result["detail"] = str(e)
    return result