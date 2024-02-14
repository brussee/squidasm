import logging

from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket
from netqasm.sdk.qubit import Qubit

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


class ProgramA(Program):

    def __init__(self, my_id: str, peer_id: str) -> None:
        self._my_id = my_id
        self._peer_id = peer_id
        self._logger = logging.getLogger(name=self.meta.name)

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name=f"ProgramA('{self._my_id}', '{self._peer_id}')",
            csockets=[self._peer_id],
            epr_sockets=[self._peer_id],
            max_qubits=20,
        )

    def run(self, context: ProgramContext):
        peer = context.csockets[self._peer_id]

        msg = f"Hello from {self._my_id}"
        self._logger.info(f"Sending message: {msg}")
        peer.send(msg)

        # TODO
        return {}
