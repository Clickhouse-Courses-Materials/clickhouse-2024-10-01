-- postgresql
create table sales (
    event_date date,
    order_id integer,
    price numeric,
    qty integer,
    PRIMARY KEY (event_date, order_id)
);

-- clickhouse
create table sales (
 event_date Date,
 order_id UInt32,
 price Decimal(15,4),
 qty UInt32
) engine = MergeTree()

create table aggr_sales (
    event_date Date,
    total_price Decimal(15,4)
)

