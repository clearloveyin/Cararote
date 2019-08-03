from app.ctrl.ctrl_base import CtrlBase


class CtrlDiff(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def diff_col(self, diff_col, old_data, new_data):
        """
        每次更新之前比较是否有变化
        :param diff_col:
        :param old_data:
        :param new_data:
        :return:action
        """
        action = 'same'
        if new_data and not old_data:
            action = 'add'
        elif old_data and not new_data:
            action = 'delete'
        else:
            for col in diff_col:
                old_value = old_data.get(col)
                new_value = new_data.get(col)
                if old_value or new_value:
                    if str(old_value) != str(new_value):
                        action = 'change'
        return action

    def match_list(self, old_datas, new_datas, key_col):
        """
        :param from_datas:
        :param to_datas:
        :return:
        """
        if not old_datas:
            old_datas = []
        if not new_datas:
            new_datas = []
        match_list = []
        # 先比较主键相同的
        new_compared, old_compared = dict(), dict()
        for i, new_data in enumerate(new_datas, 0):
            old_data = self._match_by_id(new_data, old_datas, key_col, old_compared)
            if old_data:
                match_list.append({"new_data": new_data, "old_data": old_data})
                new_compared[i] = None
        # 再比较id相同的
        for i, new_data in enumerate(new_datas, 0):
            if i in new_compared:
                continue
            match_list.append({"new_data": new_data, "old_data": None})
            # old_data = self._match_by_id(new_data, old_datas, self._id_col, old_compared)
            # if old_data:
            #     match_list.append({"new_data": new_data, "old_data": old_data})
            # else:
            #     match_list.append({"new_data": new_data, "old_data": None})
        for i, old_data in enumerate(old_datas, 0):
            if i not in old_compared:
                match_list.append({"new_data": None, "old_data": old_data})
        return match_list

    def _match_by_id(self, new_data, old_datas, id_col, compared):
        new_id = new_data.get(id_col)
        if new_id:
            for j, old_data in enumerate(old_datas, 0):
                if j in compared:
                    continue
                if new_id == old_data.get(id_col):
                    compared[j] = None
                    return old_data
        return None
