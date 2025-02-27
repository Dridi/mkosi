# SPDX-License-Identifier: LGPL-2.1+

from mkosi.config import MkosiConfig
from mkosi.distributions.centos import CentosInstaller
from mkosi.installer.dnf import Repo


class AlmaInstaller(CentosInstaller):
    @staticmethod
    def gpgurls() -> tuple[str, ...]:
        return ("https://repo.almalinux.org/almalinux/RPM-GPG-KEY-AlmaLinux-$releasever",)

    @classmethod
    def repository_variants(cls, config: MkosiConfig, repo: str) -> list[Repo]:
        if config.mirror:
            url = f"baseurl={config.mirror}/almalinux/$releasever/{repo}/$basearch/os"
        else:
            url = f"mirrorlist=https://mirrors.almalinux.org/mirrorlist/$releasever/{repo.lower()}"

        return [Repo(repo, url, cls.gpgurls())]

    @classmethod
    def sig_repositories(cls, config: MkosiConfig) -> list[Repo]:
        return []
