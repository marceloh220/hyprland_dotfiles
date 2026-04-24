#!/usr/bin/env python3

def print_hulk_asscii(msg):
    hulk_asscii = (r"""
    ⠀⠀⠀⠀⢀⣠⠴⠖⠛⠛⠉⠛⠓⠶⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    
⠀⠀⠀⠀⠀⣠⣔⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀    
⠀⠀⠀⠀⣪⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⡄⠀⠀⠀⠀⠀⠀⠀    
⠀⠀⠀⡸⣡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀    
⠀⠀⠀⣿⠇⠀⢀⠀⡄⠀⣄⠀⠀⠱⣤⣀⠀⠀⠱⣄⠈⣆⢸⡛⠛⠳⠶⣤⣄⡀ 
⣤⠴⠖⢻⠀⢠⢿⢰⢧⠀⢏⠑⠤⢄⣈⣢⣌⡁⠒⠻⠥⣸⢸⢦⠀⠀⠀⠀⠈⠉
⠀⠀⠀⢸⡄⡜⠘⡏⠈⠳⢜⣆⠀⠀⠀⠀⠀⠀⠀⠀⠐⢹⠫⣸⠀⠀⠀⠀⠀⠀  
⠀⠀⠀⢸⡹⣇⠀⠀⠀⠀⠀⠈⠁⠀⡀⠀⠀⠀⣀⣤⣶⣿⡟⠥⣀⠀⠀⠀⠀   
⠀⠀⠀⠀⠉⢿⠛⠛⢳⢶⣄⣀⣠⠀⢡⣀⣴⣾⡻⠁⠀⢸⠃⠀⠀⠑⠀⠀⠀⠀  
⠀⠀⠀⠀⠀⠸⣆⠀⠀⠛⠉⢀⡼⠆⢸⢲⠤⣀⠀⠀⢸⠉⡇⠀⠀⠀⠀⠀⠀⠀   
⠀⠀⠀⠀⠀⠀⣿⠑⡀⠀⡰⠁⠙⠒⡖⠁⠀⠀⠙⢆⠘⠀⢹⠀⠀⠀⠀⠀⠀⠀    
⠀⠀⠀⠀⠀⡠⢿⡀⠁⢰⠁⠀⠀⠀⠃⠀⠀⡀⠀⠀⠂⠀⡾⠉⠉⠉⠀⠀⠀⠀  
⠀⠀⠀⠔⠉⠀⠈⠻⣄⠘⢠⣒⡒⣒⣶⣊⣥⣬⣇⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⠈⢍⢁⡀⠤⠄⣀⠠⠀⣰⠃⠀⠀⠀⠀⢀⠀⠀⠀⠀  
⠀⠀⠀⠀⠀⢀⡀⠀⠀⠸⣦⣀⣀⣀⢀⣀⣀⣀⡴⠋⠀⣀⠤⠖⠊⠁⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠑⠒⠭⣉⠉⠉⠉⠉⠁⢀⠔⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠤⣀⣀⠔⠁⠋⠭⠯⠭⠧⠭⠶⠤⠄⠀⠀ 
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁
    """)

    line_counting = 0
    msg_size = len(msg.split())
    for line in hulk_asscii.splitlines():
        line_counting += 1
        msg_1 = " ".join(msg.split()[:msg_size//3])
        msg_2 = " ".join(msg.split()[msg_size//3:2*msg_size//3])
        msg_3 = " ".join(msg.split()[2*msg_size//3:])
        msg_len = len(max(msg_1, msg_2, msg_3, key=len))
        if line_counting == 4:
            i = 0
            print(f"{line} ", end='')
            while i < msg_len+4:
                print("-", end='')
                i += 1
            print()
        elif line_counting == 5:
            print(f"{line}|  {msg_1}", end=' ')
            for i in range(msg_len+1-len(msg_1)):
                print(" ", end='')
            print("|")
        elif line_counting == 6:
            print(f"{line}   |  {msg_2}", end=' ')
            for i in range(msg_len+1-len(msg_2)):
                print(" ", end='')
            print("|")
        elif line_counting == 7:
            print(f"{line}    |  {msg_3}", end=' ')
            for i in range(msg_len+1-len(msg_3)):
                print(" ", end='')
            print("|")
        elif line_counting == 8:
            i = 0
            print(f"{line}   ", end='')
            while i < msg_len+4:
                print("-", end='')
                i += 1
            print()
        else:
            print(f"{line}")

def gerador_aleatorio(modo="motivacional"):
    import random
    import subprocess
    uname_a = subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout
    pacotes_instalados = []
    if "Arch" in uname_a or "Manjaro" in uname_a or "cachyos" in uname_a:
        pacotes_instalados =[subprocess.run(["pacman", "-Qq"], capture_output=True, text=True).stdout.splitlines()]
    elif "Debian" in uname_a or "Ubuntu" in uname_a:
        pacotes_instalados =[subprocess.run(["dpkg-query", "-f", "${binary:Package}\n", "-W"], capture_output=True, text=True).stdout.splitlines()]
    frases_motivacionais = [
        "A vida é como uma caixa de chocolates, você nunca sabe o que vai encontrar.",
        "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
        "A felicidade não é algo pronto, ela vem das suas próprias ações.",
        "A única maneira de fazer um excelente trabalho é amar o que você faz.",
        "Não espere por oportunidades, crie-as.",
        "Acredite em si mesmo e todo o resto virá naturalmente.",
        "O futuro pertence àqueles que acreditam na beleza de seus sonhos.",
        "A vida é 10% o que acontece com você e 90% como você reage a isso.",
        "O único lugar onde o sucesso vem antes do trabalho é no dicionário.",
        "Não importa quantas vezes você falhe, o que importa é quantas vezes você se levanta."]
    frases_desmotivacionais = [
        "Quando a vida te der limões, esfregue-os na cada dela!",
        "A sorte é uma vadia, ela quer te foder.",
        "Quando você pensar que tudo já deu errado, você vai descobrir que estava errado.",
        "Tudo vai dar errado, da pior forma possível e no pior momento possível.",
        "Até logo e obrigado pelos peixes.",
        "Mantenha o seu patrão rico, os sócios deles ricos, os acionistas ricos e perceba que você continua pobre. É, isso é o capitalismo.",
        "Ninguém existe por um propósito. Ninguém pertence a lugar nenhum. Todo mundo vai morrer. Vem ver TV.",
        "Meu nomo é Giovani Giorjo, mas todo mundo me chama Giorjo.",
        "Existe alguém que está contando com você para lutar em seu lugar, já que nesse guerra não é ele quem vai morrer.",
        "Dá um prato de comida aí, por favor, tô com fome.",
        "Eu não sou um monstro, eu só fiz coisas monstruosas.",
        "Eu sou o rei do mundo!",
        "Eu sou o Batman.",
        "Vai chorar?",
        "Tens que acretires que es o melhor! Posso não ser, mas em minha cabeça eu sou o melhor!",
        "O que não te mata te deixa mais estranho.",
        "Uma rapariga é bom, três raparigas é bom demais. Tu tu tu tu!",
        "Meu coselho tá joando, não é joando, tá joando, não é joando, tá joando, não é joando... Tá joando!",
        "Está tudo bem.",
        "Citroen, creative technologie.",
        "Sr. Presidente, se eu aprendi alguma coisa hoje, é que as vezes você tem que ligar o f*da-se!",
        "Eu vim fazer um anúncio! Shadow o ouriço é um filho da p*ta do car*lho. Ele mij*u na minha esposa!",
        "Parece um bom momento para uma bebida e um discurso frio e calculado com um tom sinistro.",
        "Na hora certa, tudo vai dar errado.",
        "Você não pode mudar o seu passado, mas pode arruinar o seu futuro.",
        "O importante na vida é ter a quem culpar.",
        "Trabalhe enquanto eles ganham dinheiro.",
        "O não você já tem, busque a humilhação.",
        "As vezes é dificil separar a coragem da burrice. E a percistencia da falta do que fazer.",
        "O importante é competir, mas te mato de pancada se você não ganhar.",
        "Sempre que estiver em dúlvida, seja você mesmo. Depois que se lembrar de quem você é, se esforce para não ser você mesmo.",
        "Quem não odeia não tem coração.",
        "É melhor ser amado pelo que você não é do que ser odiado pelo que você é.",
        "Não esquente a cabeça com as derrotas de hoje, amanhã tem muito mais!",
        "Dinheiro não traz felicidade, mas a pobreza não traz nada.",
        "Dias melhores virão, mas não para você.",
        "O segredo do sucesso é desistir antes de tentar.",
        "Não morto abra dentro.",
        "Não há nada na vida que não possa piorar.",
        "O pior de tudo é o silêncio do Olavo de Carvalho.",
        "Pokemon, temos que escraviza-los eu sei!",
        "Yu-gi-oh Masterduel é o melhor jogo de cartas de todos os tempos!",
        "NVidia, vá se f*der!",
        "Pokemons tipo dragão são os mais fortes.",
        "Gaste todo o seu dinheiro hoje, o futuro é incerto e provavelmente não vai ser melhor.",
        "Não deixe para amanhã o que você pode fazer depois de amanhã.",
    ]
    frases_dicks = [
        "Dica de comando útil do dia: rm -rf / --no-preserve-root",
        "Dica de comando útil do dia: dd if=/dev/zero of=/dev/sda",
        "Dica de comando útil do dia: mkfs.ext4 /dev/sda",
        "Dica de comando útil do dia: yes | rm -rf /",
        "Dica de comando útil do dia: :(){ :|:& };:",
        "Dica de comando útil do dia: yay -Rnsu --noconfirm $(pacman -Qdtq)",
        "Dica de comando útil do dia: yay -Scc --noconfirm",
        "Dica de comando útil do dia: systemctl disable --now NetworkManager",
        "Instala pacotes Snap, instala!",
        "Eu uso Arch, BTW.",
        "As definições de virus foram atualizadas com sucesso.",
        "Abre esse email, não é um vírus. Confia.",
        "Já atualizou o sistema hoje? Não? Então atualiza logo, porra.",
        "Clica no arquivo nao_e_virus.exe. Confia.",
        "Dica de comando útil do dia: rm -rf /home/*",
        "Você esqueceu de incluir o .env no gitginore, né? Que amadorismo.",
        "Olha essa base de banco de dados que vazei na internet!",
        "Use senhas fracas, é mais fácil de lembrar e de digitar!",
        "Faça backup dos seus arquivos importantes, mas deixe eles na mesma partição que é mais fácil de acessar quando precisar!",
        "Guarde suas senhas em um arquivo de texto que é mais fácil de acessar quando precisar!",
        "Evite quebra de sistema, não atualize!",
        "Não se preocupe em usar um gerenciador de senhas, é só usar a mesma senha para tudo que é mais fácil de lembrar!",
        "Não se preocupe em usar autenticação de dois fatores, é só usar uma senha fraca que é mais fácil de lembrar!",
        "Pacotes de fontes de terceiros são seguros.",
        "Sempre confie nos blobs binários.",
        "Ler documentação é perda de tempo, é melhor perguntar em fóruns ou no Discord!",
        "Faça backup dos seus certificados e chaves privadas no github.",
        "Usar csv é mais fácil do que usar um banco de dados, mesmo para grandes quantidades de dados!",
        "Firewall é superestimado.",
        f"Encontraram uma vulnerabilidade crítica no pacote {random.choice(pacotes_instalados[0])}.",
        "Prefira o Bitlocker ao LUKS.",
        "Padrões fechados são os melhores!",
        "Windows ME é o melhor sistema operacional de todos os tempos!",
        "As Big Techs coletam nossos dados para a nossa seguirança.",
        "Use uma VPN gratuita.",
        "Precisamos zelar pela nossa privacidade e colocar todos nossos dados no Facebook.",
        "Binários baixados pela internet são seguros. Confia.",
        "Seu navegador de internet não precisa ser atualizado.",
        "Use IA, estudar programação é coisa do passado!",
        "Dica de comando útil do dia: curl -sL https://example.com/install.sh | bash",
        "Dica de comando útil do dia: chmod -R 777 /",
        "Adicione todos os repositórios de terceiros possíveis para ter acesso a mais pacotes!",
        "Pacotes do AUR são os mais seguros e confiáveis!",
        "Execute o script primeiro, leia depois.",
        "Não há nada nas interfaces gráficas e nenhum homem precisa de nada.",
    ]
    if modo == "motivacional":
        return str(random.choice(frases_motivacionais))
    elif modo == "desmotivacional":
        return str(random.choice(frases_desmotivacionais))
    elif modo == "dicks":
        return str(random.choice(frases_dicks))
    elif modo == "todes":
        return str(random.choice(frases_desmotivacionais + frases_dicks))

if __name__ == "__main__":
    import sys
    import argparse
    if "--mode" not in sys.argv and "-m" not in sys.argv and len(sys.argv) > 1:
        print_hulk_asscii(str(sys.argv[1:]).replace('[','').replace(']','').replace('','').replace('\'',''))
        sys.exit(0)
    parser = argparse.ArgumentParser(description="Hulk Say - A fun command-line tool to display messages in a Hulk ASCII art style.")
    parser.add_argument("message", nargs="*", help="The message to display in Hulk ASCII art style. If not provided, a random motivational, demotivational, or command tip will be generated.")
    parser.add_argument("-m", "--mode", choices=["motivacional", "desmotivacional", "dicks", "todes"], default="motivacional", help="Choose the mode for the random message if no message is provided. Options are 'motivacional', 'desmotivacional', 'dicks', and 'todes'. Default is 'motivacional'.")
    args = parser.parse_args()
    if args.message:
        print_hulk_asscii(" ".join(args.message))
    else:
        print_hulk_asscii(gerador_aleatorio(args.mode))
