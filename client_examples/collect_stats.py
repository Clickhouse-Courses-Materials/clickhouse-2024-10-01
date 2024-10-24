from cgitb import reset

from infi.clickhouse_orm import Database

import psutil
import datetime
import time

from client_examples.models import CpuStats, CpuStatsBuffer

db = Database('default')
db.create_table(CpuStats)
db.create_table(CpuStatsBuffer)


while True:
    # todo: get and insert stats
    time.sleep(1)
    timestamp = datetime.datetime.now()
    stats = psutil.cpu_percent(percpu=True)
    print(stats)
    result = []
    for i in range(len(stats)):
        cpu_stat = CpuStatsBuffer(timestamp=timestamp, cpu_id=i, cpu_percent=stats[i])
        result.append(cpu_stat)
    db.insert(result)


