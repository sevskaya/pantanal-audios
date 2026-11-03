# Pantanal: áudios de cena

Caixa de correio entre o **servidor** (onde o Claude monta as cenas) e o **PC do
dono** (onde o ElevenLabs gera o áudio). Repositório **privado**: tem texto de
lore das cenas.

## O caminho de um áudio

```
SERVIDOR (Claude)                 PC DO DONO                      SERVIDOR (Claude)
escreve pedidos/<id>.json  ──►  python tools/gerar.py      ──►  copia audios/<arquivo>
estado: "pedido"                 gera, mistura, nivela            para rsg-npcs/sounds/,
git push                         estado: "gerado"                 casa o horário com o
                                 git push                         nss_npc, estado: "instalado"
```

1. **Pedido** (servidor): um JSON em `pedidos/`, no formato de
   `pedidos/_MODELO.json`. Diz a cena, o que se ouve, o nome do arquivo e para
   onde ele vai.
2. **Geração** (PC): `git pull`, depois `python tools/gerar.py`. O script
   gera cada camada no ElevenLabs (fala e efeito), mistura, nivela o volume,
   grava em `audios/` e marca o pedido como `gerado`. Ouvir antes de subir;
   se não ficou bom, mudar o texto ou a voz no pedido e rodar de novo com
   `--refazer <id>`. Depois `git add -A`, `git commit`, `git push`.
3. **Instalação** (servidor): o Claude puxa, copia para
   `resources/[sevs]/rsg-npcs/sounds/`, liga no `config.lua` do `rsg-npcs`
   com o mesmo horário do NPC do `nss_npc` e marca `instalado`.

## Preparar o PC (uma vez)

- **Python 3.10+** (python.org, marcar "Add to PATH").
- **ffmpeg** no PATH (`winget install ffmpeg`). Ele mistura as camadas e
  nivela o volume.
- **Chave do ElevenLabs** numa variável de ambiente, **nunca no repositório**:
  `setx ELEVENLABS_API_KEY "sua-chave"` (abrir um terminal novo depois).
- Opcional: `setx ELEVENLABS_VOICE_ID "<id da voz padrão>"`. O pedido pode
  trazer a voz dele em `voice_id`.

## Regras do som (para todo pedido)

- **Saída:** mp3, mono, 44,1 kHz, 128 kbps, volume nivelado em -18 LUFS. O
  `rsg-npcs` toca em 3D pelo xsound; mono soa certo na posição do bicho.
- **Nome do arquivo:** minúsculo, sem acento e sem espaço (`segredo_braithwaite.mp3`).
- **Texto falado:** registro 1492, português, sem travessão.
- **Loop:** o `rsg-npcs` repete o áudio enquanto o jogador está perto. O
  pedido diz a duração total, com silêncios entre as falas, para o loop não
  cansar.
- **Volume no jogo** fica no config do `rsg-npcs` (`audioVolume`), não no arquivo.

## Pastas

| pasta | o que mora |
|---|---|
| `pedidos/` | um JSON por áudio; `_MODELO.json` explica cada campo |
| `audios/` | o mp3 pronto, gerado pelo PC |
| `tools/gerar.py` | o gerador (ElevenLabs + ffmpeg) |
