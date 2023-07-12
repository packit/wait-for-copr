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
        copr_package_proxy = client.package_proxy

        if not copr_package_proxy:
            # Might be caused by a network issue.
            click.echo("Issue with initiating Copr package proxy. Retrying.")
            time.sleep(interval)
            continue

        try:
            built_version = copr_package_proxy.get(
                owner, project, dependency, with_latest_succeeded_build=True
            ).builds["latest_succeeded"]["source_package"]["version"]
        except CoprNoResultException as ex:
            # Might be caused by package/project not being present in Copr yet.
            click.echo(str(ex))
            time.sleep(interval)
            continue

        click.echo(f"Last successful: {built_version}")

        if release in built_version:
            click.echo(f"Built found: {built_version}")
            return

        time.sleep(interval)

    click.echo("timeout waiting for build")


if __name__ == "__main__":
    wait_for_copr()
