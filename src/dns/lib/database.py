import sqlite3 as db
import sys

latencydb = db.connect("sql/latency.db")

def get_latency(**kwargs):
    query_string = "SELECT * from latency WHERE ip=%s and server=%s" % get_ip_server(**kwargs)
    try:
        execute(query_string)
    except db.Error as e:
        print e
        exit()

def upsert_latency(**kwargs):
    query_string = "INSERT INTO latency (%s) values (%s)" %\
            (", ".join(kwargs.keys()), ", ".join(map(str, kwargs.values())))
    try:
        execute(query_string)
    except db.Error as e:
        update_latency(**kwargs)

def update_latency(**kwargs):
    try:
        ip, server = get_ip_server(**kwargs)
        update_strings = []

        if 'latency' in kwargs.keys():
            update_strings.append("latency=%s" % kwargs['latency'])
        if 'timestamp' in kwargs.keys():
            update_strings.append("timestamp=%s" % kwargs['timestamp'])
        if 'authority' in kwargs.keys():
            update_strings.append("authority=%s" % kwargs['authority'])

        update_string  = ", ".join(update_strings)
        query_string = "UPDATE latency SET %s WHERE ip=%s AND server=%s" %\
                        (update_string, ip, server)
        execute(query_string)
    except db.Error as e:
        print e
        exit()

def delete_latency(**kwargs):
    try:
        ip, server = get_ip_server(kwargs)
        query_string = "DELETE from latency where ip=%s and server=%s" % get_ip_server(kwargs)
    except db.Error as e:
        print e
        exit()

def execute(query_string):
    print 'executing %s' % query_string
    cur = latencydb.cursor()
    cur.execute(query_string)
    latencydb.commit()


def get_ip_server(**kwargs):
    try:
        ip = kwargs['ip']
        server = kwargs['server']
        return (ip, server)
    except KeyError as e:
        raise Exception("Could not retrieve ip server from kwargs")


def upsert_active_server(**kwargs):
    pass

def delete_active_server(**kwargs):
    pass

def get_active_servers(**kwargs):
    pass


