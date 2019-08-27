import networkx as nx
import plotly.figure_factory as ff
import datetime


class CPM(nx.DiGraph):

    def __init__(self):
        super().__init__()
        self._dirty = True
        self._critical_path_length = -1
        self._criticalPath = None

    def add_node(self, *args, **kwargs):
        self._dirty = True
        super().add_node(*args, **kwargs)

    def add_nodes_from(self, *args, **kwargs):
        self._dirty = True
        super().add_nodes_from(*args, **kwargs)

    def add_edge(self, *args):
        self._dirty = True
        super().add_edge(*args)

    def add_edges_from(self, *args, **kwargs):
        self._dirty = True
        super().add_edges_from(*args, **kwargs)

    def remove_node(self, *args, **kwargs):
        self._dirty = True
        super().remove_node(*args, **kwargs)

    def remove_nodes_from(self, *args, **kwargs):
        self._dirty = True
        super().remove_nodes_from(*args, **kwargs)

    def remove_edge(self, *args):
        self._dirty = True
        super().remove_edge(*args)

    def remove_edges_from(self, *args, **kwargs):
        self._dirty = True
        super().remove_edges_from(*args, **kwargs)

    def _forward(self):
        for n in nx.topological_sort(self):
            es = max([self.node[j]['EF'] for j in self.predecessors(n)], default=0)
            self.add_node(n, ES=es, EF=es + self.node[n]['duration'])

    def _backward(self):
        for n in reversed(list(nx.topological_sort(self))):
            lf = min([self.node[j]['LS'] for j in self.successors(n)], default=self._critical_path_length)

            #kritinius tasku laikus paskaiciuojame nuo galo
            kl = max([self.node[j]['KL'] for j in self.successors(n)], default=0) + self.node[n]['duration']
            self.add_node(n, LS=lf - self.node[n]['duration'], LF=lf, KL=kl)


    def _compute_critical_path(self):
        graph = set()
        for n in self:
            if self.node[n]['EF'] == self.node[n]['LF']:
                graph.add(n)
        self._criticalPath = self.subgraph(graph)

    @property
    def critical_path_length(self):
        if self._dirty:
            self._update()
        return self._critical_path_length

    @property
    def critical_path(self):
        if self._dirty:
            self._update()
        return sorted(self._criticalPath, key=lambda x: self.node[x]['ES'])

    def _update(self):
        self._forward()
        self._critical_path_length = max(nx.get_node_attributes(self, 'EF').values())
        self._backward()
        self._compute_critical_path()
        self._dirty = False


def union(listas: list):
    tup1=()
    conNodes = []
    index = 1
    for n in listas:
        tup1+=((namestr(n, globals()) + '-'),)
    G = nx.union_all(listas, rename=(tup1))
    G2 = CPM()
    nodes = list(G.nodes)
    G2.add_nodes_from(G.nodes(data=True))
    G2.add_edges_from(G.edges(data=True))
    for i in range(len(nodes)):
        try:
            if tup1[index] in nodes[i]:
                conNodes.append((nodes[i-1],nodes[i]))
                index += 1
        except IndexError:
                break
    G2.add_edges_from(conNodes)
    return G2

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]

#gauname isrikiuotas uzduotis pagal kritini laika (descending)
def sortingnodes(nodeslist):
    kl_list = sorted(nodeslist, key=lambda x:x[1], reverse=True)
    kl_list_test = [x[0] for x in kl_list]
    return kl_list_test

#pridedamos uzduociu trukmes prie isrikiuoto saraso
def addingdurations(sortedNodesList, originalNodesList):
    testList = sorted(originalNodesList, key=lambda x: sortedNodesList.index(x[0]))
    return testList

def adding_tasks_dates(nodeslist: list, date: datetime.datetime):
    nodes = [i[0] for i in nodeslist]
    nodes_durations = []
    cur_date = date
    for node in nodeslist[::-1]:
        nodes_durations.append(((cur_date - datetime.timedelta(hours=node[1])).strftime('%Y-%m-%d %H:%M'),cur_date.strftime('%Y-%m-%d %H:%M')))
        cur_date = cur_date - datetime.timedelta(hours=node[1])
    #dict kur key - taskas, value - pradzia ir pabaiga
    info_dict = dict(zip(nodes,nodes_durations[::-1]))
    #print(info_dict)
    return info_dict

def build_tasks_dict(tasksdatesdict:dict):
    nodes_names = tasksdatesdict.keys()
    operations = []
    new_dict = {}
    for x in nodes_names:
        operations.append(x.split('-')[1])
    operations = list(set(operations))
    for name in operations:
        new_dict[name] = {}
        for k, v in tasksdatesdict.items():
            if name in k.split('-')[1]:
                new_dict[name][k] = v
    #print(new_dict)
    return new_dict
    
def plotting_gantt(tasksdict:dict):
    df = []
    for out_k, out_v in tasksdict.items():
        for in_k, in_v in out_v.items():
            df.append(dict(Task=out_k,Start=in_v[0], Finish=in_v[1],Resource=in_k))
    fig = ff.create_gantt(df, index_col='Task', show_colorbar=True, group_tasks=True, showgrid_x=True, showgrid_y=True, data='Resource', bar_width=0.5) 
    fig.show()


    



if __name__ == "__main__":
    G = CPM()
    G1 = CPM()
    G2 = CPM()
    G.add_node('A', duration=5)
    G.add_node('B', duration=2)
    G.add_node('C', duration=4)
    G.add_node('D', duration=4)
    G.add_node('E', duration=3)
    G.add_node('F', duration=7)
    G.add_node('G', duration=3)
    G.add_node('H', duration=2)
    G.add_node('I', duration=4)

    G1.add_node('A', duration=5)
    G1.add_node('B', duration=2)
    G1.add_node('C', duration=4)
    G1.add_node('D', duration=4)
    G1.add_node('E', duration=3)
    G1.add_node('F', duration=7)
    G1.add_node('G', duration=3)
    G1.add_node('H', duration=2)
    G1.add_node('I', duration=4)

    #grafas su tik vienu tasku be jokiu jungimu
    G2.add_node('A', duration=6)
    G.add_edges_from([
        ('A', 'C'),
        ('A', 'D'),
        ('B', 'E'),
        ('B', 'F'),
        ('D', 'G'), ('E', 'G'),
        ('F', 'H'),
        ('C', 'I'), ('G', 'I'), ('H', 'I')
    ])

    G1.add_edges_from([
        ('A', 'C'),
        ('A', 'D'),
        ('B', 'E'),
        ('B', 'F'),
        ('D', 'G'), ('E', 'G'),
        ('F', 'H'),
        ('C', 'I'), ('G', 'I'), ('H', 'I')
    ])
    
    G4 = union([G, G1, G2])
    G4.critical_path
    G4.critical_path_length
    kl_list = sortingnodes(G4.nodes.data('KL'))
    testlist = addingdurations(kl_list,list(G4.nodes.data('duration')))
    nodesdict = adding_tasks_dates(testlist, datetime.datetime(2019,8,26,23,00))
    tasks_durations = build_tasks_dict(nodesdict)
    plotting_gantt(tasks_durations)
    #print(G4.nodes.data())

