import redis

from includes import *

'''
python -m RLTest --test tests_dag.py --module path/to/redisai.so
'''


def test_dag_local_tensorset(env):
    con = env.getConnection()

    command = "AI.DAGRUN "\
    "AI.TENSORSET volative_tensor FLOAT 1 2 VALUES 5 10"

    ret = con.execute_command(command)
    env.assertEqual(ret, [b'OK'])


def test_dag_local_tensorset_tensorget(env):
    con = env.getConnection()

    command = "AI.DAGRUN "\
    "AI.TENSORSET volative_tensor FLOAT 1 2 VALUES 5 10 |> "\
    "AI.TENSORGET volative_tensor VALUES"

    ret = con.execute_command(command)
    env.assertEqual(ret, [b'OK',[b'FLOAT',[1,2],[b'5', b'10']]])


def test_dag_keyspace_tensorget(env):
    con = env.getConnection()

    ret = con.execute_command("AI.TENSORSET persisted_tensor FLOAT 1 2 VALUES 5 10")
    env.assertEqual(ret, b'OK')

    command = "AI.DAGRUN LOAD 1 persisted_tensor |> "\
    "AI.TENSORGET persisted_tensor VALUES"

    ret = con.execute_command(command)
    env.assertEqual(ret, [[b'FLOAT',[1,2],[b'5', b'10']]])


def test_dag_keyspace_and_localcontext_tensorget(env):
    con = env.getConnection()

    ret = con.execute_command("AI.TENSORSET persisted_tensor FLOAT 1 2 VALUES 5 10")
    env.assertEqual(ret, b'OK')

    command = "AI.DAGRUN LOAD 1 persisted_tensor |> "\
    "AI.TENSORSET volative_tensor FLOAT 1 2 VALUES 5 10 |> "\
    "AI.TENSORGET persisted_tensor VALUES |> "\
    "AI.TENSORGET volative_tensor VALUES"

    ret = con.execute_command(command)
    env.assertEqual(ret, [b'OK',[b'FLOAT',[1,2],[b'5', b'10']],[b'FLOAT',[1,2],[b'5', b'10']]])

