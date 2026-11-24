# Saber Roubado: o que você precisa criar (23/11/2026)

Eu já fiz o código. Falta só o áudio. As artes (36) já estão instaladas e os objetos do cenário vêm do próprio jogo.

## Como gerar (no seu PC)

1. Clonar ou atualizar: `git clone https://github.com/sevskaya/pantanal-audios.git` (ou `git pull` se já tiver).
2. `python tools/gerar.py` (ElevenLabs + ffmpeg). Ele gera os mp3 de todos os pedidos com `estado: pedido` e sobe em `audios/`.
3. `git push` e me avise. Eu instalo no Saber Roubado, ligo no código e marco `instalado`.

Enquanto não existirem, o script funciona: os sons usam os do Ritual e as vozes ficam em silêncio, só com a legenda.

## 1. Sons (15 pedidos, já escritos desde 17/11)

| arquivo | quando toca |
|---|---|
| `sr_anotado.mp3` | toca quando a investigação termina ("Segredo anotado"). |
| `sr_aviso_tribo.mp3` | toca para o membro da tribo que recebe o aviso de profanação. |
| `sr_caderno_abrir.mp3` | toca ao abrir o Caderno de Estudos (tela de papel velho). |
| `sr_climax.mp3` | toca no clímax da Reza Roubada (os entalhes acendem, os espíritos aparecem). |
| `sr_investigar_ambiente.mp3` | fundo dos 20 s em que ele agacha e copia os símbolos da pedra (repete). |
| `sr_pagina.mp3` | toca ao trocar de aba no Caderno. |
| `sr_profanacao_ambiente.mp3` | fundo das 3 fases do ritual roubado (repete). Algo errado acontecendo na pedra sagrada. |
| `sr_quebrado.mp3` | toca quando o ritual quebra ou a investigação é interrompida. |
| `sr_resgate_armadilha.mp3` | a armadilha de ferro abre (salvamento: preso na armadilha). |
| `sr_resgate_ave.mp3` | a ave se debate no colo do jogador (salvamento: ave de asa quebrada). |
| `sr_resgate_aviso.mp3` | aviso de que um animal precisa de ajuda por perto (salvamento). |
| `sr_resgate_perdido.mp3` | o animal não resistiu (salvamento perdido). |
| `sr_resgate_salvo.mp3` | o animal foi salvo e volta para a mata. |
| `sr_ritual_abertura.mp3` | toca uma vez quando o ritual roubado começa (as faixas pretas entram). |
| `sr_roubado.mp3` | toca quando o ritual roubado se cumpre (ele aprende o Arandu). |

## 2. Vozes (27 pedidos, novos)

Duas vozes: o **Etnógrafo** (naturalista estrangeiro, culto, calmo) e o **Pesquisador** (o jogador pensando em voz baixa, com variação de tom: sério, com medo no ritual, terno com os animais). Português do Brasil, só a voz, sem música.

| arquivo | quem | fala |
|---|---|---|
| `sr_voz_abertura_1.mp3` | Pesquisador (pensamento) | Ninguém me convidou para esta pedra. |
| `sr_voz_abertura_2.mp3` | Pesquisador (pensamento) | Mas eu li os sinais, e trouxe o que eles pedem. |
| `sr_voz_abertura_3.mp3` | Pesquisador (pensamento) | Se o saber é deles, que me prove a pedra. |
| `sr_voz_fase_1.mp3` | Pesquisador (pensamento) | Deposito as oferendas na ordem do caderno. Não sei se a ordem importa. Para eles, importava. |
| `sr_voz_fase_2.mp3` | Pesquisador (pensamento) | Repito os passos que vi desenhados. O corpo erra. A pedra percebe. |
| `sr_voz_fase_3.mp3` | Pesquisador (pensamento) | As palavras não são minhas. Digo assim mesmo. |
| `sr_voz_investigar_1.mp3` | Pesquisador (pensamento) | Marcas de fogo antigas na pedra. Alguém vinha aqui com frequência. |
| `sr_voz_investigar_2.mp3` | Pesquisador (pensamento) | Restos de oferenda entre as frestas. Anoto o que reconheço. |
| `sr_voz_investigar_3.mp3` | Pesquisador (pensamento) | Copio os símbolos no caderno, um por um. |
| `sr_voz_npc_devolve_1.mp3` | Etnógrafo (NPC) | Perdeu o caderno? Suas anotações eu guardei de memória. |
| `sr_voz_npc_devolve_2.mp3` | Etnógrafo (NPC) | Tome outro. Não deixe ele cair nas mãos erradas. |
| `sr_voz_npc_inicio_1.mp3` | Etnógrafo (NPC) | Você não é deles. Ótimo. Eles não falariam comigo. |
| `sr_voz_npc_inicio_2.mp3` | Etnógrafo (NPC) | Há dez pedras sagradas nestas terras. Cada uma guarda um saber. |
| `sr_voz_npc_inicio_3.mp3` | Etnógrafo (NPC) | Vá até elas, investigue, anote o que pedem. Depois, faça o que eles fazem. |
| `sr_voz_npc_inicio_4.mp3` | Etnógrafo (NPC) | Leve este caderno. O resto é com você, e com a sua consciência. |
| `sr_voz_npc_jatem_1.mp3` | Etnógrafo (NPC) | Você já tem o caderno. Volte quando tiver algo a me contar. |
| `sr_voz_npc_tribo_1.mp3` | Etnógrafo (NPC) | Não tenho nada para alguém do seu povo. |
| `sr_voz_npc_tribo_2.mp3` | Etnógrafo (NPC) | Os seus já sabem o que eu passei a vida tentando aprender. |
| `sr_voz_resgate_ande_devagar.mp3` | Pesquisador (pensamento) | Ande devagar, a pé. Cada tranco machuca a asa. |
| `sr_voz_resgate_armadilha.mp3` | Pesquisador (pensamento) | Caçadores prenderam o bicho numa jaula. Ele se debate contra as grades. |
| `sr_voz_resgate_armadilha_cede.mp3` | Pesquisador (pensamento) | A armadilha cede. O bicho manca, mas corre. |
| `sr_voz_resgate_ave.mp3` | Pesquisador (pensamento) | A asa pende torta. Leve no colo, a pé e devagar, ou ela se machuca mais. |
| `sr_voz_resgate_confia.mp3` | Pesquisador (pensamento) | Ele confia em você agora. Leve-o até a mãe. |
| `sr_voz_resgate_ferida_fechada.mp3` | Pesquisador (pensamento) | A ferida está fechada. Leve-o até um lugar seguro, e não o deixe para trás. |
| `sr_voz_resgate_ferido.mp3` | Pesquisador (pensamento) | Está sangrando e mal fica de pé. Primeiro a ferida, depois um lugar seguro. |
| `sr_voz_resgate_filhote.mp3` | Pesquisador (pensamento) | Pequeno demais para estar sozinho. A mãe não deve estar longe. |
| `sr_voz_resgate_jaula_aberta.mp3` | Pesquisador (pensamento) | O cadeado cede. A porta range, e o bicho dispara para o mato. |

## 3. Opcional: ajustar o cenário

O cenário do salvamento (jaula, acampamento dos caçadores, armadilhas, rede) fica em `config.lua` do Saber Roubado, em `Config.Resgate.cenas`. Cada objeto tem `x` (direita), `y` (frente), `h` (giro). Se algo ficar torto ou dentro de outro objeto quando testar, me diga qual e eu acerto.

## 24/11/2026: a voz da pedra (pedido do dono: nível AAA, cada pedra com a sua história)
O dono achou que as falas se repetiam em toda pedra. Agora cada uma das 10 pedras tem a sua história, sussurrada pela **voz da pedra** (um ancestral):
- `sr_hist_<pedra>_1..3`: 3 sussurros durante a investigação (30 arquivos, até 5 s cada);
- `sr_resp_<pedra>`: a pedra responde quando o saber é roubado (10 arquivos).

Cada arquivo tem duas camadas: o sussurro e, por baixo, um sopro de vento nas pedras.

Refeitos com camadas de cinema: `sr_investigar_ambiente` (vento, drone e lápis) e `sr_anotado` (caderno fechando e impacto).

**No PC:** `git pull`, `python tools/gerar.py`, ouvir, `git add audios pedidos`, commit e push.
A voz é a `Hsrdp9vv51A8JfLqfIH8`, a mesma dos sussurros da profanação. Se não ficar boa, trocar o `voice_id` nos `sr_hist_*` e `sr_resp_*` e rodar `--refazer`.
