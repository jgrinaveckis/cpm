import datetime

def adding_tasks_dates(nodeslist: list, date):
    nodes = [i[0] for i in nodeslist]
    nodes_durations = []
    cur_date = date
    s = datetime.time(8)
    e = datetime.time(17)
    for node in nodeslist[::-1]:
        dur = node[1]
        times_list = []
        a = cur_date - datetime.timedelta(hours=dur)
        b = int(a.strftime('%H'))
        if (s <= datetime.time(b) <= e):
            if int(cur_date.strftime('%H')) == 8:
                cur_date = cur_date-datetime.timedelta(days=1)
                cur_date = cur_date.replace(hour=17)
            while dur > 9:
                cur_date, times_list, dur = list_appending(times_list, cur_date, dur)
            else:
                if dur > 0:
                    times_list.append(((cur_date - datetime.timedelta(hours=dur)).strftime('%Y-%m-%d %H:%M'),\
                    cur_date.strftime('%Y-%m-%d %H:%M')))
                nodes_durations.extend([times_list[::-1]])
                cur_date = cur_date - datetime.timedelta(hours=dur)
        else:
            if int(cur_date.strftime('%H')) == 8:
                cur_date = cur_date-datetime.timedelta(days=1)
                cur_date = cur_date.replace(hour=17)
            while dur > 9:
                cur_date, times_list, dur = list_appending(times_list, cur_date, dur)
            if int(cur_date.strftime('%H')) == 17:
                finish = cur_date
                start = cur_date - datetime.timedelta(hours=dur)
                times_list.append((start.strftime('%Y-%m-%d %H:%M'),finish.strftime('%Y-%m-%d %H:%M')))
                dur -= int(((finish - start).total_seconds())/3600)
                #datai atnaujinti
                cur_date = start
            else:
                cur_date, times_list, dur = list_appending(times_list, cur_date, dur)
            if dur > 0:
                times_list.append(((cur_date - datetime.timedelta(hours=dur)).strftime('%Y-%m-%d %H:%M'),\
                cur_date.strftime('%Y-%m-%d %H:%M')))
            cur_date = cur_date - datetime.timedelta(hours=dur)
            nodes_durations.extend([times_list[::-1]])
    #dict kur key - taskas, value - pradzia ir pabaiga
    info_dict = dict(zip(nodes,nodes_durations[::-1]))
    return info_dict

def list_appending(times_list:list, cur_date, dur):
    finish = cur_date
    start = cur_date.replace(hour=8)
    times_list.append((start.strftime('%Y-%m-%d %H:%M'),finish.strftime('%Y-%m-%d %H:%M')))
    dur -= int(((finish - start).total_seconds())/3600)
    cur_date = cur_date-datetime.timedelta(days=1)
    cur_date = cur_date.replace(hour=17)
    return cur_date, times_list, dur