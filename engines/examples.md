```sql

select * from system.data_type_families
where name like '%Date%';

CREATE table events (
	account_id UInt64,
	device_id UInt64,
	event_type Enum8 ('login' = 1, 'logout' =2),
	country String,
	time_ns  UInt64,
	date_time DateTime MATERIALIZED toDateTime(time_ns / 1000000000)
) Engine = MergeTree()
ORDER By account_id
PARTITION BY toYYYYMM(date_time); 


CREATE table events2 (
	account_id UInt64,
	device_id UInt64,
	event_type Enum8 ('login' = 1, 'logout' =2),
	country String,
	time_ns  UInt64,
	date_time DateTime MATERIALIZED toDateTime(time_ns / 1000000000)
) Engine = MergeTree()
ORDER By account_id
PARTITION BY toYYYYMM(date_time)
SETTINGS min_rows_for_wide_part=0, min_bytes_for_wide_part=0; 


DROP TABLE IF EXISTS events3;

CREATE table events3 (
	account_id UInt64,
	device_id UInt64,
	event_type Enum8 ('login' = 1, 'logout' =2),
	country String,
	time_ns  UInt64,
	date_time DateTime MATERIALIZED toDateTime(time_ns / 1000000000)
) Engine = MergeTree()
ORDER By account_id
SETTINGS min_rows_for_wide_part=0, min_bytes_for_wide_part=0; 

INSERT into events3 values(1, 2, 'login', 'us', 1234567891234567);
INSERT into events3 values(1, 1, 'login', 'ru', 1234234891234567);


CREATE TABLE users (
	user_id UInt64,
	age UInt8,
	name String,
	country String,
	sign Int8
) engine = CollapsingMergeTree(sign)
ORDER BY user_id;

INSERT INTO users values(1, 25, 'Alex', 'Russia', 1);
INSERT INTO users values(2, 30, 'Artem', 'Russia', 1);

INSERT INTO users values(1, 25, 'Alex', 'Russia', -1);
INSERT INTO users values(1, 26, 'Alex', 'Russia', 1);

CREATE TABLE users3 (
	user_id UInt64,
	age UInt8,
	name String,
	country String,
	ver Int8
) engine = ReplacingMergeTree()
ORDER BY user_id;

INSERT INTO users2 values(1, 26, 'Alex', 'Russia', 2);
INSERT INTO users2 values(1, 26, 'Alex', 'USA', 1);


SELECT * FROM users3 FINAL;

CREATE TABLE sum_test (
	key UInt32,
	value1 UInt32,
	value2 String,
	value3 UInt32
) engine = SummingMergeTree()
ORDER BY key;

--- SELECT KEY, sum(value1), sum(value2) FROM TABLE GROUP BY KEY;


INSERT INTO sum_test values(1,1,'1', 1),(2,1,'1', 1);
INSERT INTO sum_test values(1,2,'2', 2),(2,2,'2', 2);

CREATE TABLE visit_statistics(
	user_id UInt64,
	date_in DateTime,
	views UInt32,
	duration UInt32
) engine = MergeTree()
ORDER BY (user_id, date_in);


INSERT INTO visit_statistics values(1,'2024-10-20 10:00:00',5, 100),(2,'2024-10-20 10:00:00',10, 150);
INSERT INTO visit_statistics values(1,'2024-10-20 09:00:00',10, 150),(2,'2024-10-20 08:00:00', 10, 170);

-- SELECT sum(visits), avg(duration) FROM TABLE GROUP BY user_id, date_in
CREATE TABLE visits_aggr (
	user_id UInt64,
	date_in DateTime,
	sum_views AggregateFunction(sum, UInt32),
	avg_duration AggregateFunction(avg, UInt32)
 ) engine = AggregatingMergeTree()
 ORDER BY  (user_id, date_in);

INSERT INTO visits_aggr 
SELECT user_id, date_in, sumState(views) AS sum_views, avgState(duration) AS avg_duration FROM visit_statistics GROUP BY user_id, date_in;

SELECT 
	user_id, date_in,
	sumMerge(sum_views) AS sum_views, 
	avgMerge(avg_duration) AS avg_duration 
FROM visits_aggr 
GROUP BY user_id, date_in;
```
