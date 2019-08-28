import datetime

def adding_tasks_dates(nodeslist: list, date):
    nodes = [i[0] for i in nodeslist]
    nodes_durations = []
    cur_date = date
    start = datetime.time(8)
    end = datetime.time(17)
    for node in nodeslist[::-1]:
        dur = node[1]
        times_list = []
        #TODO:sutvarkyti laika 'datetime.datetime' ir 'datetime.time'
        if (start <= datetime.time((cur_date - datetime.timedelta(hours=dur)).hour) <= end):
            while dur > 9:
                start = cur_date.replace(hour=8)
                finish = cur_date
                times_list.append((start.strftime('%Y-%m-%d %H:%M'),finish.strftime('%Y-%m-%d %H:%M')))
                dur = dur - ((start - finish).hour())
                cur_date = cur_date-datetime.timedelta(days=1)
                cur_date = cur_date.replace(hour=17)
            else:
                times_list.append(((cur_date - datetime.timedelta(hours=dur)).strftime('%Y-%m-%d %H:%M'),\
                cur_date.strftime('%Y-%m-%d %H:%M')))
                nodes_durations.extend(times_list[::-1])
                cur_date = cur_date - datetime.timedelta(hours=dur)
        else:
            while dur > 9:
                start = cur_date.replace(hour=8)
                finish = cur_date
                times_list.append((start.strftime('%Y-%m-%d %H:%M'),finish.strftime('%Y-%m-%d %H:%M')))
                dur = dur - ((start - finish).hour())
                cur_date = cur_date-datetime.timedelta(days=1)
                cur_date = cur_date.replace(hour=17)
            else:
                start = cur_date.replace(hour=8)
                finish = cur_date
                times_list.append((start.strftime('%Y-%m-%d %H:%M'),finish.strftime('%Y-%m-%d %H:%M')))
                dur = dur - (finish.hour - start.hour)
                cur_date = cur_date-datetime.timedelta(days=1)
                cur_date = cur_date.replace(hour=17)
                times_list.append((((cur_date - datetime.timedelta(hours=dur)).strftime('%Y-%m-%d %H:%M'),\
                cur_date.strftime('%Y-%m-%d %H:%M'))))
                nodes_durations.extend(times_list[::-1])
                cur_date = cur_date - datetime.timedelta(hours=dur)
    #dict kur key - taskas, value - pradzia ir pabaiga
    info_dict = dict(zip(nodes,nodes_durations[::-1]))
    return info_dict