import logging

from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket
from netqasm.sdk.qubit import Qubit

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


class ProgramB(Program):

    def __init__(self, my_id: str, peer_id: str) -> None:
        self._my_id = my_id
        self._peer_id = peer_id
        self._logger = logging.getLogger(name=self.meta.name)

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name=f"ProgramB('{self._my_id}','{self._peer_id}')",
            csockets=[self._peer_id],
            epr_sockets=[self._peer_id],
            max_qubits=20,
        )

    def run(self, context: ProgramContext):
        peer = context.csockets[self._peer_id]

        msg = yield from peer.recv()
        self._logger.info(f"Received message: {msg}")

        # TODO
        return {}
