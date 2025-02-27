# SPDX-License-Identifier: LGPL-2.1+

from mkosi.architecture import Architecture
from mkosi.distributions.debian import DebianInstaller
from mkosi.state import MkosiState


class UbuntuInstaller(DebianInstaller):
    @staticmethod
    def repositories(state: MkosiState, local: bool = True) -> list[str]:
        if state.config.local_mirror and local:
            return [f"deb [trusted=yes] {state.config.local_mirror} {state.config.release} main"]

        archives = ("deb", "deb-src")

        # From kinetic onwards, the usr-is-merged package is available in universe and is required by
        # mkosi to set up a proper usr-merged system so we add the universe repository unconditionally.
        components = ["main"] + (["universe"] if state.config.release not in ("focal", "jammy") else [])
        components = ' '.join((*components, *state.config.repositories))

        repos = [
            f"{archive} {state.config.mirror} {state.config.release} {components}"
            for archive in archives
        ]

        repos += [
            f"{archive} {state.config.mirror} {state.config.release}-updates {components}"
            for archive in archives
        ]

        # Security updates repos are never mirrored. But !x86 are on the ports server.
        if state.config.architecture in [Architecture.x86, Architecture.x86_64]:
            url = "http://security.ubuntu.com/ubuntu/"
        else:
            url = "http://ports.ubuntu.com/"

        repos += [
            f"{archive} {url} {state.config.release}-security {components}"
            for archive in archives
        ]

        return repos
