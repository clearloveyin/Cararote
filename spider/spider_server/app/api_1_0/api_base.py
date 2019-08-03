TYPE_CODE = {
	"SUCCESS": 200,
	"NOT_DATA": 201, # 暂无数据
	"PROMPT_ERROR": 202, # 逻辑错误提醒
	"TOKEN_ERROR": 203, # token验证失败
	"EXCEPTION_ERROR": 204 # 服务异常
}

def set_result_code(result):
    type = result.get("type")
    code = TYPE_CODE.get(type)
    result["code"] = code