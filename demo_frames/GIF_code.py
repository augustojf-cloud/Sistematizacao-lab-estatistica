import os
from PIL import Image
import glob

# Pasta onde este proprio script esta salvo (independente de onde for chamado)
pasta_script = os.path.dirname(os.path.abspath(__file__))

# Busca as imagens PNG dentro dessa mesma pasta
arquivos = sorted(glob.glob(os.path.join(pasta_script, "*.png")))

if not arquivos:
    raise SystemExit(f"Nenhuma imagem encontrada em {pasta_script}. Verifique se os PNGs estao na mesma pasta do script.")

frames = [Image.open(img) for img in arquivos]

# Padroniza a largura de todos os frames (evita GIF "tremido")
largura = 800
frames_redimensionados = []
for frame in frames:
    proporcao = largura / frame.width
    altura = int(frame.height * proporcao)
    frames_redimensionados.append(frame.convert("RGB").resize((largura, altura)))

# Salva o GIF na MESMA pasta do script (demo_frames/), mantendo tudo junto
caminho_saida = os.path.join(pasta_script, "demo.gif")

frames_redimensionados[0].save(
    caminho_saida,
    save_all=True,
    append_images=frames_redimensionados[1:],
    duration=1200,   # tempo (ms) que cada imagem fica na tela
    loop=0
)

print(f"GIF gerado com sucesso: {caminho_saida} ({len(arquivos)} frames)")

