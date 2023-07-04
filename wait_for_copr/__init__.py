#!/usr/bin/env python3

# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT


import click
import time
from copr.v3 import Client
from copr.v3.exceptions import CoprNoResultException


@click.command()
@click.option("--owner", help="Owner of the Copr repository.")
@click.option("--project", help="Name of the Copr project.")
@click.option(
    "--max-tries",
    default=180,
    type=int,
    help="How many times we should check the dependency before exiting. "
    "There is 10s interval between checks.",
)
@click.argument(
    "dependency",
    required=True,
)
@click.argument(
    "release",
)
def wait_for_copr(owner, project, max_tries, dependency, release):
    """
    This command periodically checks Copr
    for the last build of the given DEPENDENCY package
    until the last build contains the given RELEASE.

    (The substring is checked.)

    Example usage:

    $ wait-for-copr --owner packit --project fedora-copr-copr-2720 python-copr 007c498c
    """
    client = Client.create_from_config_file()

    click.echo(
        f"Waiting for {dependency} release `{release}` in {owner}/{project} "
        f"(max_tries={max_tries} * 10s)"
    )

    for _ in range(max_tries):
        try:
            built_version = client.package_proxy.get(
                owner, project, dependency, with_latest_succeeded_build=True
            ).builds["latest_succeeded"]["source_package"]["version"]

            click.echo(f"Last successul: {built_version}")

            if release in built_version:
                click.echo(f"Built found: {built_version}")
                return

        except CoprNoResultException as ex:
            click.echo(str(ex))

        time.sleep(10)

    click.echo("timeout waiting for build")


if __name__ == "__main__":
    wait_for_copr()
