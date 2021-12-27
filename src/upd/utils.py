from typing import Dict, List
import time

class RNode:
    def __init__(self, id=None):
        if not id:
            id = str(time.time())
        self.id = id
        self.from_relations = []
        self.to_relations = []
        self.name = None
        self.attributes = None


class RRelation:
    def __init__(self):
        self.from_node = None
        self.to_node = None
        self.name = None
        self.attributes = None


class RGraph:
    def __init__(self):
        self.nodes = {}
        self.relations = {}

    def nodes(self, nodes: List[Dict]):
        for node_data in nodes:
            node = RNode(**node_data)
            self.nodes[node.id] = node

    def relations(self, relations: List[Dict]):
        pass
