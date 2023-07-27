import os

import click
import uvicorn

from atumm.app.infra.config import get_config


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)

def main(env: str, debug: bool):
    os.environ["STAGE"] = env
    os.environ["DEBUG"] = str(debug)
    config = get_config()
    uvicorn.run(
        app="atumm.app.infra.app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.STAGE != "production" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
