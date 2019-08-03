--删除manday
delete from func.func_man_day where task_id in (
	select task_id from func.task as t1 left join 
	func.functions as t2 on t1.func_id = t2.func_id
	left join func.quotations as t3 
	on t2.quotation_id = t3.quotation_id
	where t3.proj_id in (15, 18, 19)
);
--删除task
delete from func.task where func_id in(
	select func_id from func.functions as t1
	left join func.quotations as t2
	on t1.quotation_id = t2.quotation_id
	where t2.proj_id in (15, 18, 19)
);
--删除function
delete from func.func_group where func_id in(
	select func_id from func.functions as t1
	left join func.quotations as t2
	on t1.quotation_id = t2.quotation_id
	where t2.proj_id in (15, 18, 19)
);
delete from func.functions where quotation_id in(
	select quotation_id from func.quotations 
	where proj_id in (15, 18, 19)
);
--删除option

delete from func.option_combination where quotation_id in (
	select quotation_id from func.quotations
	where proj_id in (15, 18, 19)
);
delete from func.option_value where option_id in (
	select option_id from func.options as t1 left join
	func.quotations as t2 on t1.quotation_id = t2.quotation_id 
	where t2.proj_id in (15, 18, 19)
);
delete from func.options where quotation_id in (
	select quotation_id from func.quotations
	where proj_id in (15, 18, 19)
);
--删除前提
delete from func.preconditions where proj_id in (15, 18, 19);
--删除quotations
delete from func.quotations where proj_id in (15, 18, 19);
--删除体制
delete from user_role where proj_id in (15, 18, 19);
--删除项目
delete from func.projects where proj_id in (15, 18, 19);

