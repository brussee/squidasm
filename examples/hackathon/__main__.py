import os
import logging

from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run

from ProgramA import ProgramA
from ProgramB import ProgramB


def configure_logging(default_level: str = 'INFO') -> None:
    logging.basicConfig(
        level=os.environ.get('LOGLEVEL', default_level).upper(),
    )


def main() -> None:
    network_config = StackNetworkConfig.from_file("network.yaml")
    node1_id = network_config.stacks[0].name
    node2_id = network_config.stacks[1].name
    run(
        config=network_config,
        programs={
            node1_id: ProgramA(node1_id, node2_id),
            node2_id: ProgramB(node2_id, node1_id),
        },
        num_times=1
    )



if __name__ == "__main__":
    configure_logging()
    main()
