#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import subprocess
from typing import List

from whatthedouchesay_quotes import get_douche_catalog


def _run_command_output(command: List[str]) -> str:
    try:
        return subprocess.run(command, capture_output=True, text=True, check=False).stdout
    except FileNotFoundError:
        return ""


def _get_installed_packages() -> List[str]:
    uname_a = _run_command_output(["uname", "-a"]).lower()

    if any(distro in uname_a for distro in ("arch", "manjaro", "cachyos")):
        output = _run_command_output(["pacman", "-Qq"])
        return output.splitlines() if output else []

    if any(distro in uname_a for distro in ("debian", "ubuntu")):
        output = _run_command_output(["dpkg-query", "-f", "${binary:Package}\\n", "-W"])
        return output.splitlines() if output else []

    return []


def douche_generator(modo: str = "desmotivational", lang: str = "en") -> str:
    user = _run_command_output(["whoami"]).strip() or "douche"
    pkg_installed = _get_installed_packages()
    pkg_random = random.choice(pkg_installed) if pkg_installed else "douche-cli"

    quote_desmotivational, quote_dicks = get_douche_catalog(user, pkg_random)

    douche_language = lang.lower()
    quote_desmotivational_language = quote_desmotivational.get(douche_language, quote_desmotivational["pt-br"])
    quote_dicks_language = quote_dicks.get(douche_language, quote_dicks["pt-br"])

    if modo == "desmotivational":
        return random.choice(quote_desmotivational_language)
    if modo == "dicks":
        return random.choice(quote_dicks_language)
    return random.choice(quote_desmotivational_language + quote_dicks_language)
