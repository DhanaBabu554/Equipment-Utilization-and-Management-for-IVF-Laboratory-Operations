select * from project1;

describe project1;

---- mean -----
select avg(max_capacity_hrs) as mean
from project1;

select avg(technical_downtime_hrs) as mean
from project1;

select avg(workflow_delay_events) as mean
from project1;

select round(avg(total_cases_day_lab)) as mean
from project1;

/***** Median *****/
SELECT 
    AVG(max_capacity_hrs) AS median
FROM (
    SELECT 
        max_capacity_hrs,
        ROW_NUMBER() OVER (ORDER BY max_capacity_hrs) AS rn,
        COUNT(*) OVER () AS total
    FROM project1
) t
WHERE rn IN (FLOOR((total + 1) / 2), CEIL((total + 1) / 2));

/***** Mode *****/

SELECT 
    max_capacity_hrs AS mode
FROM project1
GROUP BY max_capacity_hrs
ORDER BY count(*) DESC
LIMIT 1;

/**** variance ****/

select  
    variance(max_capacity_hrs) AS variance
FROM project1;

/**** standard deviation *****/
select  
    stddev(max_capacity_hrs) AS std_deviation
FROM project1;

/**** skewness****/

SELECT
    SUM(POWER(t.max_capacity_hrs - t.mean, 3)) / COUNT(*)
    / POWER(MAX(t.std_dev), 3) AS skewness
FROM (
    SELECT 
        p.max_capacity_hrs,
        s.mean,
        s.std_dev
    FROM project1 p
    CROSS JOIN (
        SELECT
            AVG(max_capacity_hrs)    AS mean,
            STDDEV(max_capacity_hrs) AS std_dev
        FROM project1
    ) s
) t;

/******* kurtosis *****/

SELECT
    (
        SUM(POWER(t.max_capacity_hrs - t.mean, 4)) / COUNT(*)
        / POWER(MAX(t.std_dev), 4)
    ) - 3 AS excess_kurtosis
FROM (
    SELECT 
        p.max_capacity_hrs,
        s.mean,
        s.std_dev
    FROM project1 p
    CROSS JOIN (
        SELECT
            AVG(max_capacity_hrs)    AS mean,
            STDDEV(max_capacity_hrs) AS std_dev
        FROM project1
    ) s
) t;


/****** data cleaning *****/

/**Check NULL values**/

SELECT
    SUM(date IS NULL) as null_date,
    sum(lab_id is null) as null_lab_id,
    sum(equipment_id is null) as null_equipment_id,
    sum(equipment_type is null) as null_equipment_type,
    sum(max_capacity_hrs is null) as null_max_capacity_hrs,
    SUM(utilization_hrs IS NULL) as null_utilization,
    SUM(utilization_pct IS NULL) as null_utilization_pct,
    SUM(idle_hrs IS NULL) as null_idle_hrs,
    sum(technical_downtime_hrs is null) as null_technical_downtime_hrs,
    sum(planned_maintenance_hrs is null) as null_planned_maintenance_hrs,
    sum(workflow_delay_events is null) as null_workflow_delay_events,
    sum(avg_delay_minutes is null) as null_avg_delay_minutes,
    sum(primary_procedure is null) as null_primary_procedure,
    sum(redundancy_available is null) as null_redundancy_available,
    sum(total_cases_day_lab is null) as null_total_cases_day_lab
FROM project1;

/***Check for Duplicate Records***/

SELECT date, lab_id, equipment_id, COUNT(*) AS cnt
FROM project1
GROUP BY date, lab_id, equipment_id
HAVING COUNT(*) > 1;

/*** remove duplicate records ***/

ALTER TABLE project1
ADD COLUMN temp_id INT NOT NULL AUTO_INCREMENT,
ADD PRIMARY KEY (temp_id);

desc project1;

DELETE FROM project1
WHERE temp_id NOT IN (
    SELECT temp_id FROM (
        SELECT temp_id,
               ROW_NUMBER() OVER (
                   PARTITION BY date, lab_id, equipment_id
                   ORDER BY temp_id
               ) AS rn
        FROM project1
    ) AS x
    WHERE rn = 1
);
 
ALTER TABLE project1 DROP COLUMN temp_id;

select count(*) from project1;

select * from project1
where utilization_pct < 100;
 
/*** data preprocessing ***/

ALTER TABLE project1 ADD COLUMN outlier_flag BOOLEAN DEFAULT 0;

UPDATE project1
SET outlier_flag = 1
WHERE utilization_pct < 5 OR utilization_pct > 95;

select* from project1;

select * from project1 where outlier_flag=0;

select * from project1 where outlier_flag=1;

create table project1_clean as 
select * from project1;

select * from project1_clean;

























