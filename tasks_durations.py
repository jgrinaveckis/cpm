import datetime

def adding_tasks_dates(nodeslist: list, date, start_time, end_time):
    nodes = [i[0] for i in nodeslist]
    nodes_durations = []
    cur_date = date
    s = datetime.time(start_time)
    e = datetime.time(end_time)
    for node in nodeslist[::-1]:
        dur = node[1]
        times_list = []
        a = cur_date - datetime.timedelta(hours=dur)
        b = int(a.strftime('%H'))
        if (s <= datetime.time(b) <= e):
            if int(cur_date.strftime('%H')) == start_time:
                cur_date = cur_date-datetime.timedelta(days=1)
                cur_date = cur_date.replace(hour=end_time)
            while dur > end_time - start_time:
                cur_date, times_list, dur = list_appending(times_list, cur_date, dur, start_time, end_time)
            else:
                if dur > 0:
                    times_list.append(((cur_date - datetime.timedelta(hours=dur)).strftime('%Y-%m-%d %H:%M'),\
                    cur_date.strftime('%Y-%m-%d %H:%M')))
                nodes_durations.extend([times_list[::-1]])
                cur_date = cur_date - datetime.timedelta(hours=dur)
        else:
            if int(cur_date.strftime('%H')) == start_time:
                cur_date = cur_date-datetime.timedelta(days=1)
                cur_date = cur_date.replace(hour=end_time)
            while dur > end_time - start_time:
                cur_date, times_list, dur = list_appending(times_list, cur_date, dur, start_time, end_time)
            if int(cur_date.strftime('%H')) == end_time:
                finish = cur_date
                start = cur_date - datetime.timedelta(hours=dur)
                times_list.append((start.strftime('%Y-%m-%d %H:%M'),finish.strftime('%Y-%m-%d %H:%M')))
                dur -= int(((finish - start).total_seconds())/3600)
                #datai atnaujinti
                cur_date = start
            else:
                cur_date, times_list, dur = list_appending(times_list, cur_date, dur, start_time, end_time)
            if dur > 0:
                times_list.append(((cur_date - datetime.timedelta(hours=dur)).strftime('%Y-%m-%d %H:%M'),\
                cur_date.strftime('%Y-%m-%d %H:%M')))
            cur_date = cur_date - datetime.timedelta(hours=dur)
            nodes_durations.extend([times_list[::-1]])
    #dict kur key - taskas, value - pradzia ir pabaiga
    info_dict = dict(zip(nodes,nodes_durations[::-1]))
    return info_dict

def list_appending(times_list:list, cur_date, dur, start_time, end_time):
    finish = cur_date
    start = cur_date.replace(hour=start_time)
    times_list.append((start.strftime('%Y-%m-%d %H:%M'),finish.strftime('%Y-%m-%d %H:%M')))
    dur -= int(((finish - start).total_seconds())/3600)
    cur_date = cur_date-datetime.timedelta(days=1)
    cur_date = cur_date.replace(hour=end_time)
    return cur_date, times_list, dur