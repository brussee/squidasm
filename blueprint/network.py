from __future__ import annotations

from typing import Dict

from netsquid.components import Port
from netsquid_magic.link_layer import (
    MagicLinkLayerProtocolWithSignaling,
)

from squidasm.sim.stack.egp import EgpProtocol
from squidasm.sim.stack.stack import ProcessingNode


class ProtocolContext:
    def __init__(self, node: ProcessingNode,
                 links: Dict[str, MagicLinkLayerProtocolWithSignaling],
                 egp: Dict[str, EgpProtocol],
                 node_id_mapping: Dict[str, int],
                 in_ports: Dict[str, Port],
                 out_ports: Dict[str, Port]):
        self.node = node
        self.links = links
        self.egp = egp
        self.node_id_mapping = node_id_mapping
        self.in_ports = in_ports
        self.out_ports = out_ports


class Network:
    def __init__(self):
        self.nodes: Dict[str, ProcessingNode] = {}
        self.links: Dict[(str, str), MagicLinkLayerProtocolWithSignaling] = {}
        self.egp: Dict[(str, str), EgpProtocol] = {}
        self.node_name_id_mapping: Dict[str, int] = {}
        self.out_ports: Dict[(str, str), Port] = {}
        self.in_ports: Dict[(str, str), Port] = {}

    def get_protocol_context(self, node_id: str) -> ProtocolContext:
        node = self.nodes[node_id]
        links = self.filter_for_id(node_id, self.links)
        egp = self.filter_for_id(node_id, self.egp)
        in_ports = self.filter_for_id(node_id, self.in_ports)
        out_ports = self.filter_for_id(node_id, self.out_ports)

        return ProtocolContext(node, links, egp, self.node_name_id_mapping, in_ports, out_ports)

    @staticmethod
    def filter_for_id(node_id: str, dictionary: Dict[(str, str), any]) -> Dict[str, any]:
        keys = dictionary.keys()
        keys = filter(lambda key_tuple: key_tuple[0] == node_id, keys)
        return {key[1]: dictionary[key] for key in keys}

