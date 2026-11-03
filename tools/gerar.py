"""Gera os audios dos pedidos (pedidos/*.json) no ElevenLabs e deixa prontos para o rsg-npcs.

Uso (na raiz do repositorio):
    python tools/gerar.py                 # gera todo pedido com estado "pedido"
    python tools/gerar.py --refazer <id>  # gera de novo um pedido, qualquer estado
    python tools/gerar.py --listar        # mostra os pedidos e o estado de cada um

Precisa: Python 3.10+, ffmpeg no PATH, variavel ELEVENLABS_API_KEY.
Opcional: ELEVENLABS_VOICE_ID (voz padrao quando o pedido nao traz voice_id).
So usa biblioteca padrao do Python.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PEDIDOS = RAIZ / "pedidos"
AUDIOS = RAIZ / "audios"
API = "https://api.elevenlabs.io/v1"
FORMATO = "mp3_44100_128"
MODELO_FALA = "eleven_multilingual_v2"


def chamar_api(caminho, corpo, chave):
    req = urllib.request.Request(
        f"{API}{caminho}?output_format={FORMATO}",
        data=json.dumps(corpo).encode("utf-8"),
        headers={"xi-api-key": chave, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", "replace")[:400]
        raise SystemExit(f"ElevenLabs recusou ({e.code}): {detalhe}")


def gerar_camada(camada, chave, voz_padrao, destino):
    tipo = camada.get("tipo")
    if tipo == "fala":
        voz = camada.get("voice_id") or voz_padrao
        if not voz:
            raise SystemExit("camada de fala sem voice_id e sem ELEVENLABS_VOICE_ID no PC")
        corpo = {
            "text": camada["texto"],
            "model_id": camada.get("modelo", MODELO_FALA),
            "voice_settings": {
                "stability": float(camada.get("estabilidade", 0.4)),
                "similarity_boost": float(camada.get("similaridade", 0.75)),
                "style": float(camada.get("estilo", 0.3)),
                "use_speaker_boost": True,
            },
        }
        dados = chamar_api(f"/text-to-speech/{voz}", corpo, chave)
    elif tipo == "efeito":
        dur = max(0.5, min(22.0, float(camada.get("duracao_s", 10))))
        corpo = {"text": camada["descricao"], "duration_seconds": dur, "prompt_influence": 0.5}
        dados = chamar_api("/sound-generation", corpo, chave)
    else:
        raise SystemExit(f"tipo de camada desconhecido: {tipo!r} (use 'fala' ou 'efeito')")
    destino.write_bytes(dados)


def misturar(pedido, arquivos, saida):
    """Mistura as camadas, posiciona no tempo, nivela em -18 LUFS, mono 44.1 kHz 128 kbps."""
    total = float(pedido["duracao_total_s"])
    entradas, filtros, rotulos = [], [], []
    for i, (camada, arq) in enumerate(zip(pedido["camadas"], arquivos)):
        inicio = float(camada.get("inicio_s", 0))
        if camada.get("repetir"):
            entradas += ["-stream_loop", "-1"]
        entradas += ["-i", str(arq)]
        f = f"[{i}:a]aformat=sample_rates=44100:channel_layouts=mono,volume={float(camada.get('volume', 1.0))}"
        if camada.get("repetir"):
            f += f",atrim=0:{max(0.1, total - inicio)}"
        if inicio > 0:
            f += f",adelay={int(inicio * 1000)}"
        filtros.append(f + f"[c{i}]")
        rotulos.append(f"[c{i}]")
    filtros.append(
        "".join(rotulos)
        + f"amix=inputs={len(rotulos)}:duration=longest:normalize=0,apad,atrim=0:{total},"
        + "loudnorm=I=-18:TP=-1.5:LRA=11[saida]"
    )
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *entradas,
           "-filter_complex", ";".join(filtros), "-map", "[saida]",
           "-ac", "1", "-ar", "44100", "-b:a", "128k", str(saida)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg falhou:\n{r.stderr[-1500:]}")


def processar(caminho, chave, voz_padrao):
    pedido = json.loads(caminho.read_text(encoding="utf-8"))
    arquivo = pedido["arquivo"]
    if arquivo != arquivo.lower() or " " in arquivo or not arquivo.endswith(".mp3"):
        raise SystemExit(f"{caminho.name}: 'arquivo' tem que ser minusculo, sem espaco, terminando em .mp3")
    print(f"- {pedido['id']}: {len(pedido['camadas'])} camada(s), {pedido['duracao_total_s']} s")
    AUDIOS.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        partes = []
        for i, camada in enumerate(pedido["camadas"]):
            p = Path(tmp) / f"camada{i}.mp3"
            print(f"    gerando camada {i} ({camada.get('tipo')})...")
            gerar_camada(camada, chave, voz_padrao, p)
            partes.append(p)
        saida = AUDIOS / arquivo
        misturar(pedido, partes, saida)
    pedido["estado"] = "gerado"
    caminho.write_text(json.dumps(pedido, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"    pronto: audios/{arquivo} (ouca antes de subir)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refazer", metavar="ID", help="gera de novo este pedido, qualquer estado")
    ap.add_argument("--listar", action="store_true", help="lista os pedidos e o estado")
    args = ap.parse_args()

    pedidos = sorted(p for p in PEDIDOS.glob("*.json") if not p.name.startswith("_"))
    if args.listar:
        for p in pedidos:
            d = json.loads(p.read_text(encoding="utf-8"))
            print(f"{d.get('estado', '?'):10} {d.get('id')}  ->  {d.get('arquivo')}")
        return

    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not chave:
        sys.exit("Falta a variavel ELEVENLABS_API_KEY (setx ELEVENLABS_API_KEY \"sua-chave\" e abra outro terminal).")
    if not shutil.which("ffmpeg"):
        sys.exit("Falta o ffmpeg no PATH (winget install ffmpeg e abra outro terminal).")
    voz_padrao = os.environ.get("ELEVENLABS_VOICE_ID", "")

    feitos = 0
    for p in pedidos:
        d = json.loads(p.read_text(encoding="utf-8"))
        if (args.refazer and d.get("id") == args.refazer) or (not args.refazer and d.get("estado") == "pedido"):
            processar(p, chave, voz_padrao)
            feitos += 1
    if feitos == 0:
        print("Nada para gerar." + (f" Nao achei o pedido '{args.refazer}'." if args.refazer else ""))
    else:
        print(f"\n{feitos} audio(s) pronto(s). Ouca em audios/ e depois: git add -A; git commit -m \"audios gerados\"; git push")


if __name__ == "__main__":
    main()
