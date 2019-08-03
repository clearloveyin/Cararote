
-- DROP MATERIALIZED VIEW public.lastest_man_day_id;

CREATE MATERIALIZED VIEW public.lastest_man_day_id
TABLESPACE pg_default
AS
 SELECT func_man_day.task_id,
    func_man_day.group_id,
    func_man_day.option_id,
    max(func_man_day.version) AS lastet_ver_id
   FROM func.func_man_day
  GROUP BY func_man_day.task_id, func_man_day.group_id, func_man_day.option_id
WITH DATA;

ALTER TABLE public.lastest_man_day_id
    OWNER TO postgres;


CREATE UNIQUE INDEX lastest_man_day_idex
    ON public.lastest_man_day_id USING btree
    (task_id, group_id, option_id, lastet_ver_id)
    TABLESPACE pg_default;