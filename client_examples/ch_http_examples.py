import requests
import pandas as pd
from io import StringIO

HOST = 'http://localhost:8123'

query_ddl = """
create table http_test (
    a UInt8,
    b String,
    c enum('one'=1, 'two'=2)
) engine = MergeTree() ORDER BY a;
"""

query_insert = """
    insert into http_test values (1, 'abc', 'one') (2, 'abc', 'two') (1, 'dfsdfd', 'one') (2, 'dfdsfd', 'two') (1, 'abc', 'two')
"""

query_select = """
select * from http_test where c = 'two'
"""

def query(q, host=HOST, conn_timeout=1500, **kwargs):
    r = requests.post(host, data=q, params=kwargs, timeout=conn_timeout)
    if r.status_code == 200:
        return r.text
    else:
        raise ValueError(r.text)

if __name__ == '__main__':
    #query(query_insert)
    r = query(query_select)
    print(type(r))
    df = pd.read_csv(StringIO(r), sep='\t', names=['a', 'b', 'c'])
    print(df.head())
    print(df.shape)
