import redis

from includes import *

'''
python -m RLTest --test tests_dag.py --module path/to/redisai.so
'''


def test_dag_local_tensorset_tensorget(env):
    con = env.getConnection()

    command = "AI.DAGRUN LOCALS t1 |> "\
    "AI.TENSORSET t1 float 1 2 values 5 20 |> "\
    "AI.TENSORGET t1 values"

    ret = con.execute_command(command)
    env.assertEqual(ret, [b'OK',[b'5', b'20']])

def test_dag_multilocal_tensorset_tensorget(env):
    con = env.getConnection()

    command = "AI.DAGRUN LOCALS t1 t2 t3 |> "\
    "AI.TENSORSET t1 float 1 2 values 5 20 |> "\
    "AI.TENSORGET t1 values |> "\
    "AI.TENSORGET t1 blob |> "\
    "AI.TENSORGET t1 meta"

    ret = con.execute_command(command)
    env.assertEqual(ret, [b'OK',[b'5', b'20']])
