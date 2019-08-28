import datetime

def adding_tasks_dates(nodeslist: list, date: datetime.datetime):
    nodes = [i[0] for i in nodeslist]
    nodes_durations = []
    cur_date = date
    start = datetime.time(8)
    end = datetime.time(17)
    for node in nodeslist[::-1]:
        dur = node[1]
        #TODO: tikrinti prasisukima jei didelis uzduoties atlikimo laikas ir dur skaiciuoti
        if (start <= (cur_date - datetime.timedelta(hours=dur)).time() <= end) & ((cur_date - datetime.timedelta(hours=dur)).days()) == 0:
            nodes_durations.extend([((cur_date - datetime.timedelta(hours=node[1])).strftime('%Y-%m-%d %H:%M'),\
            cur_date.strftime('%Y-%m-%d %H:%M'))])
            cur_date = cur_date - datetime.timedelta(hours=dur)
        elif (start <= (cur_date - datetime.timedelta(hours=dur)).time() <= end) & dur > 8:
            cur_date = cur_date-datetime.timedelta(days=1)
            cur_date = cur_date.replace(hour=17)
            nodes_durations.extend([((cur_date - datetime.timedelta(hours=node[1])).strftime('%Y-%m-%d %H:%M'),\
            cur_date.strftime('%Y-%m-%d %H:%M'))])
            cur_date = cur_date - datetime.timedelta(hours=node[1])
    #dict kur key - taskas, value - pradzia ir pabaiga
    info_dict = dict(zip(nodes,nodes_durations[::-1]))
    return info_dict