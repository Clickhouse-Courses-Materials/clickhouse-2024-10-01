from infi.clickhouse_orm import Model, MergeTree, UInt32Field, DecimalField, DateTimeField, BufferModel, Buffer


class CpuStats(Model):
    cpu_id = UInt32Field()
    cpu_percent = DecimalField(10, 5)
    timestamp = DateTimeField()

    engine = MergeTree(order_by=[cpu_id], date_col='timestamp')

class CpuStatsBuffer(BufferModel, CpuStats):
    engine = Buffer(CpuStats)