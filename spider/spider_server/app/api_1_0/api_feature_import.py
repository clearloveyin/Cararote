from flask_restful import Resource
from app.service.service_feature_improt import ServiceFeatureImport

class ApiFeatureImport(Resource):
    def get(self):
        start_row = 14
        col_list = [5, 6, 7, 8, 9]
        excel_path = r"C:\Users\yuyin\Desktop\机能式样书Spider管理检讨_0524.xlsx"
        sheet_name = "Featurelist"
        service_obj = ServiceFeatureImport(start_row=start_row, col_list=col_list,
                                       excel_path=excel_path, sheet_name=sheet_name)
        service_obj.read_feature_excel()

