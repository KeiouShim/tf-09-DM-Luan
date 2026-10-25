# tf-09: a classe Atalho e os 3 pilares

- **Encapsulamento:** quem usa o Atalho so precisa saber de `destino` (leitura) e `redirecionar()`; a implementacao (o `__destino` privado, o `__slots__` e a checagem de ancestrais) fica escondida.
- **Heranca:** o Atalho herda de Item o nome, o pai, o `caminho` e o `mover_para()`, sem precisar copiar nada; so acrescenta o destino.
- **Polimorfismo:** `tamanho()` devolve 1 no Atalho e a soma do conteudo na Pasta, mas `espaco_total()` chama todos do mesmo jeito.
- **Interface x implementacao:** a interface do Medivel e so o contrato `tamanho()`; o Atalho cumpre esse contrato sem nenhuma mudanca em `espaco_total()`.