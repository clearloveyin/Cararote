from flask_restful import Resource


class ApiTestDsQuotation(Resource):
    """获取Function和GroupID的合并
    """
    def get(self, quotation_id):
        from app.data_server.ds_quotation import get_ds_quotation
        obj_quotation = get_ds_quotation(quotation_id)
        summary_df = obj_quotation.summary_manday_by_func()
        func_list = summary_df.to_dict(orient="records")
        # for func in func_list:
        #     print(func)
        return func_list


class ApiTestDsQuotationSummary(Resource):
    """获取Function工数汇总信息
    """
    def get(self, quotation_id):
        from app.data_server.ds_quotation import get_ds_quotation
        obj_quotation = get_ds_quotation(quotation_id)
        summary_df = obj_quotation.summary_manday_by_func()
        func_list = summary_df.to_dict(orient="records")
        # for func in func_list:
        #     print(func)
        return func_list


class ApiTestDsQuotationFilterSplitManday(Resource):
    """过滤和分割工数信息。
    """
    def get(self, quotation_id):
        from app.data_server.ds_quotation import get_ds_quotation
        obj_quotation = get_ds_quotation(quotation_id)
        # obj_quotation.load_function_task_manday_df()
        # func_df = obj_quotation.get_func_df()
        func_task_df = obj_quotation.get_func_task_df()
        group_ids = [1, 2]
        option_ids = [1]
        option_group_dict = obj_quotation.filter_and_split_manday_df(func_task_df=func_task_df,
                                                                     group_ids=group_ids,
                                                                     option_ids=option_ids)
        # func_task_manday_df = obj_quotation.merge_func_task_manday(group_ids=[1, 2])
        for (op, gp), df in option_group_dict.items():
            print(op, gp, '================================\n')
            func_list = df.to_dict(orient="records")
            for func in func_list:
                print(func)
            return func_list


class ApiTestDsQuotationFuncTask(Resource):
    """获取Function和Task的合并
    """
    def get(self, quotation_id):
        from app.data_server.ds_quotation import get_ds_quotation
        obj_quotation = get_ds_quotation(quotation_id)
        func_df = obj_quotation.get_func_df()
        # Func和Task合并
        task_df = obj_quotation.get_task_df()
        func_task_df = obj_quotation.merge_func_task(func_df, task_df)
        func_list = func_task_df.to_dict(orient="records")
        # b = obj_quotation.manday_df.to_dict(orient="records")
        # for func in func_list:
        #     print(func)

        print(obj_quotation.get_func_columns())
        print(obj_quotation.get_func_column_num())
        print(obj_quotation.get_task_columns())
        return func_list


class ApiTestDsQuotation2(Resource):
    """获取Function和GroupID的合并
    """
    def get(self, quotation_id):
        from app.data_server.ds_quotation import DSQuotation
        obj_quotation = DSQuotation(quotation_id)
        obj_quotation.load_function_task_manday_df()
        func_df = obj_quotation.get_func_df()
        func_group_df = obj_quotation.get_func_group_df()
        # Func和Group ID合并
        merged_func_df = obj_quotation.merge_func_group_id(func_df, func_group_df)
        func_list = merged_func_df.to_dict(orient="records")
        # b = obj_quotation.manday_df.to_dict(orient="records")
        for func in func_list:
            print(func)
        print(obj_quotation.get_func_columns())
        print(obj_quotation.get_func_column_num())
        return func_list
