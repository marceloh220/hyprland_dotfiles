#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import subprocess
from typing import List

from config.hypr.scripts.whatthedouchesay.whatthedouchesay_quotes import get_phrase_catalog


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


def gerador_aleatorio(modo: str = "desmotivacional", lang: str = "pt-br") -> str:
    user = _run_command_output(["whoami"]).strip() or "unknown-user"
    pacotes_instalados = _get_installed_packages()
    pacote_aleatorio = random.choice(pacotes_instalados) if pacotes_instalados else "unknown-package"

    frases_desmotivacionais, frases_dicks = get_phrase_catalog(user, pacote_aleatorio)

    idioma = lang.lower()
    frases_desmotivacionais_idioma = frases_desmotivacionais.get(idioma, frases_desmotivacionais["pt-br"])
    frases_dicks_idioma = frases_dicks.get(idioma, frases_dicks["pt-br"])

    if modo == "desmotivacional":
        return random.choice(frases_desmotivacionais_idioma)
    if modo == "dicks":
        return random.choice(frases_dicks_idioma)
    return random.choice(frases_desmotivacionais_idioma + frases_dicks_idioma)
