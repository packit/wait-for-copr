#!/usr/bin/env python3

# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT


import click
import time
import sys

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
    "There is INTERVAL number of seconds between checks.",
)
@click.option(
    "--interval",
    default=10,
    type=int,
    help="How much time we should wait between each try.",
)
@click.argument(
    "dependency",
    required=True,
)
@click.argument(
    "release",
)
def wait_for_copr(owner, project, max_tries, interval, dependency, release):
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
        f"(max_tries={max_tries} * {interval}s)"
    )

    for _ in range(max_tries):
        try:
            builds = client.build_proxy.get_list(owner, project, dependency)
            click.echo(
                f"{len(builds)} build(s) found "
                f"for {dependency} in {owner}/{project}"
            )

            for build in builds:
                if build["source_package"].get("version") and release in (
                    built_version := build["source_package"]["version"]
                ):
                    if build["state"] == "succeeded":
                        click.echo(f"Build found: {built_version}")
                        return
                    if build["state"] in ["failed", "canceled"]:
                        click.echo(f"Build found but failed: {built_version}", err=True)
                        sys.exit(3)

            click.echo(f"Build with release '{release}' not found for {dependency}.")
        except CoprNoResultException as ex:
            # Might be caused by package/project not being present in Copr yet.
            click.echo(str(ex))

        time.sleep(interval)

    click.echo("timeout waiting for build", err=True)
    sys.exit(2)


if __name__ == "__main__":
    wait_for_copr()
