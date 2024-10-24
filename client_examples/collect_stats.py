from infi.clickhouse_orm import Database

import psutil

from client_examples.models import CpuStats, CpuStatsBuffer

db = Database('default')
db.create_table(CpuStats)
db.create_table(CpuStatsBuffer)


while True:
    psutil.cpu_percent(percpu=True)


