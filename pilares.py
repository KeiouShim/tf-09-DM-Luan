from abc import ABC, abstractmethod


class Medivel(ABC):
    """Interface: qualquer coisa que consegue dizer o proprio tamanho."""

    @abstractmethod
    def tamanho(self):
        """Devolve quantos bytes o item ocupa."""
        pass


class Item(Medivel):
    """Base de todo item da arvore: guarda nome e pasta pai."""

    def __init__(self, nome, pai=None):
        # Nome e pai sao privados; quem usa a classe le pelas properties
        self.__nome = nome
        self.__pai = pai

    @property
    def nome(self):
        """Nome do item (somente leitura)."""
        return self.__nome

    @property
    def pai(self):
        """Pasta que contem este item, ou None se ele for a raiz."""
        return self.__pai

    @property
    def caminho(self):
        """Monta o caminho completo subindo pelos pais, ex.: C:/Users/fulano/a.txt."""
        if self.__pai is None:
            return self.__nome
        return self.__pai.caminho + "/" + self.__nome

    def mover_para(self, nova_pasta):
        """Tira o item da pasta atual e o coloca dentro de nova_pasta."""
        if self.__pai is not None:
            self.__pai.remover(self)
        self.__pai = nova_pasta
        nova_pasta.adicionar(self)

    @abstractmethod
    def mostrar(self, recuo=0):
        """Imprime o item com o recuo indicado."""
        pass


class Arquivo(Item):
    """Arquivo comum: tem um tamanho fixo informado na criacao."""

    def __init__(self, nome, tamanho, pai=None):
        super().__init__(nome, pai)
        self.__tamanho = tamanho

    def tamanho(self):
        """Devolve o tamanho guardado do arquivo."""
        return self.__tamanho

    def mostrar(self, recuo=0):
        """Imprime o nome do arquivo com recuo."""
        print("  " * recuo + self.nome)


class Pasta(Item):
    """Item que guarda outros itens dentro de si."""

    def __init__(self, nome, pai=None):
        super().__init__(nome, pai)
        self.__filhos = []

    def adicionar(self, item):
        """Coloca um item dentro da pasta."""
        self.__filhos.append(item)

    def remover(self, item):
        """Tira um item de dentro da pasta."""
        self.__filhos.remove(item)

    def tamanho(self):
        """Soma o tamanho de tudo que esta dentro da pasta."""
        return espaco_total(self.__filhos)

    def mostrar(self, recuo=0):
        """Imprime a pasta e, logo abaixo, cada filho com um nivel a mais de recuo."""
        print("  " * recuo + self.nome + "/")
        for filho in self.__filhos:
            filho.mostrar(recuo + 1)


class Lixeira(Medivel):
    """Lixeira: onde ficam os itens apagados. Vazia, nao ocupa espaco."""

    def tamanho(self):
        """Devolve 0, porque a lixeira nao conta no espaco."""
        return 0


def espaco_total(itens):
    """Soma o tamanho de uma lista de itens que sabem medir (Medivel)."""
    total = 0
    for item in itens:
        total += item.tamanho()
    return total


def tentar(acao):
    """Executa a acao; se ela der erro, imprime a mensagem em vez de parar o programa."""
    try:
        acao()
    except Exception as erro:
        print("Erro:", erro)


class Atalho(Item):
    """Item que aponta para outro item (o destino), como um atalho do Windows."""

    __slots__ = ("__destino",)

    def __init__(self, nome, destino, pai=None):
        super().__init__(nome, pai)
        self.__destino = None
        self.redirecionar(destino)

    @property
    def destino(self):
        """Item para onde o atalho aponta (somente leitura)."""
        return self.__destino

    def redirecionar(self, novo_destino):
        """Troca o destino, recusando apontar para si mesmo ou para uma pasta que o contem."""
        if novo_destino is self:
            raise ValueError("Um atalho nao pode apontar para si mesmo.")
        ancestral = self.pai
        while ancestral is not None:
            if ancestral is novo_destino:
                raise ValueError("Um atalho nao pode apontar para uma pasta que o contem.")
            ancestral = ancestral.pai
        self.__destino = novo_destino

    def tamanho(self):
        """Atalho ocupa sempre 1 byte, nao importa o tamanho do destino."""
        return 1

    def mostrar(self, recuo=0):
        """Imprime 'nome -> caminho do destino' com o recuo indicado."""
        print("  " * recuo + self.nome + " -> " + self.__destino.caminho)


# ---------- Testes ----------
NOME_USUARIO = "seu_usuario"  # troque pelo seu nome de usuario do Windows

disco = Pasta("C:")
usuarios = Pasta("Users", disco)
disco.adicionar(usuarios)
usuario = Pasta(NOME_USUARIO, usuarios)
usuarios.adicionar(usuario)
desktop = Pasta("Desktop", usuario)
usuario.adicionar(desktop)
documentos = Pasta("Documentos", usuario)
usuario.adicionar(documentos)

relatorio = Arquivo("relatorio.txt", 120, desktop)
desktop.adicionar(relatorio)
foto = Arquivo("foto.png", 4096, documentos)
documentos.adicionar(foto)

atalho_relatorio = Atalho("atalho_relatorio", relatorio, desktop)
desktop.adicionar(atalho_relatorio)
atalho_documentos = Atalho("atalho_documentos", documentos, desktop)
desktop.adicionar(atalho_documentos)

print("=== Arvore completa ===")
disco.mostrar()

print("\n=== Espaco total ===")
arquivo_solto = Arquivo("solto.txt", 50)
pasta_teste = Pasta("Teste")
pasta_teste.adicionar(Atalho("atalho_foto", foto, pasta_teste))
lixeira = Lixeira()
print("Total:", espaco_total([arquivo_solto, pasta_teste, lixeira]))

print("\n=== Tentativas que devem FALHAR ===")


def trocar_destino_direto():
    atalho_relatorio.destino = foto


tentar(trocar_destino_direto)
tentar(lambda: atalho_relatorio.redirecionar(atalho_relatorio))
tentar(lambda: Atalho("loop", desktop, desktop))
