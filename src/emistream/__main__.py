import typer

from emistream.api.app import AppBuilder
from emistream.cli import CliBuilder
from emistream.config.builder import ConfigBuilder
from emistream.config.errors import ConfigError
from emistream.console import FallbackConsoleBuilder
from emistream.server import Server

cli = CliBuilder().build()


@cli.command()
def main() -> None:
    """Main entry point."""

    console = FallbackConsoleBuilder().build()

    try:
        config = ConfigBuilder().build()
    except ConfigError as ex:
        console.print("Failed to build config!")
        console.print_exception()
        raise typer.Exit(1) from ex

    try:
        app = AppBuilder(config).build()
    except Exception as ex:
        console.print("Failed to build app!")
        console.print_exception()
        raise typer.Exit(2) from ex

    try:
        server = Server(app, config.server)
        server.run()
    except Exception as ex:
        console.print("Failed to run server!")
        console.print_exception()
        raise typer.Exit(3) from ex


if __name__ == "__main__":
    cli()
