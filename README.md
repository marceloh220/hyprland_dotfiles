# hyprland_dotfiles

Meus dotfiles para Hyprland e ferramentas do desktop.

## Instalador

Este repositório inclui um instalador em Bash:

`./install.sh --help`
`./install.sh --list-packages-groups`

Exemplos principais:

- Listar grupos de pacotes disponíveis:
	`./install.sh --list-packages-groups`
- Instalar todos os pacotes:
	`./install.sh --install-packages`
- Instalar apenas um grupo:
	`./install.sh --install-packages --install-packages-group hyprland`
- Copiar dotfiles padrão:
	`./install.sh --copy-dotfiles`
- Copiar dotfiles Lua/experimental:
	`./install.sh --copy-dotfiles-lua`
- Configurar tema do SDDM:
	`./install.sh --sddm-theme-config`
- Conectar ao Wi-Fi:
	`./install.sh --connect-wifi --wifi-ssid YOUR_SSID --wifi-password YOUR_PASSWORD`

O instalador em Python continua disponível:

`python install.py --help`

## Avisos

- Leia o script antes de executar.
- Este script é para distribuições base Arch.
- Não execute como root.
- Leia os avisos e informações exibidos durante a execução.
- Faça backup antes de alterar seu sistema.

## Exemplos por cenário

- Instalação mínima (base + hyprland + extras de terminal):

```bash
./install.sh --install-packages --install-packages-group base
./install.sh --install-packages --install-packages-group hyprland
./install.sh --install-packages --install-packages-group terminal-extra
./install.sh --copy-dotfiles
```

- Instalação completa:

```bash
./install.sh --install-packages
./install.sh --copy-dotfiles
./install.sh --sddm-theme-config
```

- Apenas aplicar dotfiles (sem instalar pacotes):

```bash
./install.sh --copy-dotfiles
```

- Apenas aplicar dotfiles Lua/experimental:

```bash
./install.sh --copy-dotfiles-lua
```

## Guia Rápido (manual)

1. Instale o repositório Chaotic-AUR seguindo a documentação oficial:
   https://aur.chaotic.cx/docs
2. Instale os pacotes necessários (ou use o instalador Bash).
3. Copie os arquivos de configuração para seu diretório de configuração.
4. Copie os wallpapers para seu diretório de imagens.
5. Habilite os serviços essenciais no systemd:

```bash
sudo systemctl enable sddm
sudo systemctl enable NetworkManager
sudo systemctl enable bluetooth
```

6. Ative o firewall:

```bash
sudo ufw enable
```

7. Reinicie o sistema.

## Troubleshooting

- sudo pede senha e falha com "user is not in the sudoers file":
	Use uma conta com privilégios para adicionar seu usuário ao grupo wheel.
	Depois, garanta que exista a linha `%wheel ALL=(ALL) ALL` em `/etc/sudoers`.
- pacman bloqueado (db.lck):
	Feche processos do pacman/yay em execução e remova o lock apenas se tiver certeza.
	Comando: `sudo rm -f /var/lib/pacman/db.lck`
- erro de chave/assinatura no pacman:
	Atualize o keyring e sincronize novamente.
	Comando: `sudo pacman -Sy archlinux-keyring && sudo pacman -Syu`
- yay não instalado:
	Execute `./install.sh --install-packages` (ele tenta instalar yay automaticamente)
	ou instale manualmente com `sudo pacman -S yay`.
- pacote AUR falha no build:
	Verifique se `base-devel` e `git` estão instalados.
	Comando: `sudo pacman -S --needed base-devel git`

## Licença / Isenção

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
