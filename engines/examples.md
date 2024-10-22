```sql

CREATE TABLE events (
 account_id UInt64,
 device_id UInt64 PRIMARY KEY,
 event_type Enum8(
 'Login' = 1,
 'Logout' = 2),
 country String,
 time_ns Int64,
 date_time DateTime MATERIALIZED toDateTime(time_ns / 1000000000)
)
ENGINE = MergeTree()
ORDER BY (device_id , account_id)
PARTITION BY toYYYYMM(date_time);

insert into events values(1, 2, 'Login', 'USA', 1614612171033000000);
insert into events values(1, 3, 'Logout', 'USA', 1614612171053000000);

select partition, name, part_type, partition_id
from system.parts
where table='events';

optimize table events final

select partition, name, part_type, partition_id
from system.parts
where table='events';
```
