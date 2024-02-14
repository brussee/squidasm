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
        self._logger.setLevel('INFO')

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name=f"ProgramA('{self._my_id}', '{self._peer_id}')",
            csockets=[self._peer_id],
            epr_sockets=[self._peer_id],
            max_qubits=20,
        )

    def run(self, ctx: ProgramContext):
        qnpu = ctx.connection
        c_peer = ctx.csockets[self._peer_id]
        epr_peer = ctx.epr_sockets[self._peer_id]

        req_nr_of_pairs = 1
        msg = f"epr_request:{req_nr_of_pairs}"
        self._logger.info(f"Sending message: {msg}")
        c_peer.send(msg)

        ###

        epr_pairs = epr_peer.recv_keep(number=req_nr_of_pairs)
        measurements = [qubit.measure() for qubit in epr_pairs]
        yield from qnpu.flush()
        self._logger.info(measurements)

        # TODO
        return {}
