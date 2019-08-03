# Restful API返回值结构： 

{  
    "type": "SUCCESS"/"NOT_DATA"/"PROMPT_ERROR"/"TOKEN_ERROR"/"EXCEPTION_ERROR",  
    "code": 200/201/202/203/204,  
    "content": SUCCESS时返回的数据，其他时为空,  
    "message": 暂无数据/逻辑错误提醒/token验证失败/服务异常,  
    "detail": EXCEPTION_ERROR：代码异常详细信息,  
}


# code和type的对应关系  
{  
	200: "SUCCESS",  
	201："NOT_DATA", # 暂无数据  
	202: "PROMPT_ERROR", # 逻辑错误提醒  
	203: "TOKEN_ERROR", # token验证失败  
	204: "EXCEPTION_ERROR" # 后台拦截的服务异常  
}  


# 例子

===================================================================================  

正常:  
{  
	"type": "SUCCESS"  
	"code": 200,  
	"content": {"user_id": 1, "user_name": "王五"},  
}

===================================================================================

错误:  
{  
	"type": "EXCEPTION_ERROR",  
	"code": 204,  
	"message": "服务异常",  
	"detail": "代码异常详细信息"  
}  
