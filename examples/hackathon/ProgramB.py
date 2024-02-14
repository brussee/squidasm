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
        self._logger.setLevel('INFO')

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name=f"ProgramB('{self._my_id}','{self._peer_id}')",
            csockets=[self._peer_id],
            epr_sockets=[self._peer_id],
            max_qubits=20,
        )

    def run(self, ctx: ProgramContext):
        qnpu = ctx.connection
        c_peer = ctx.csockets[self._peer_id]
        epr_peer = ctx.epr_sockets[self._peer_id]

        msg: str = yield from c_peer.recv()
        self._logger.info(f"Received message: {msg}")

        cmd, args = msg.split(sep=':', maxsplit=1)
        argv = args.split(sep=',')

        if cmd == 'epr_request':
            qubits = epr_peer.create_keep(number=int(argv[0]))
            self._logger.info(f"Created {len(qubits)} EPR pairs on request")

            measurements = [qubit.measure() for qubit in qubits]
            yield from qnpu.flush()
            self._logger.info(measurements)

        # TODO
        return {}
