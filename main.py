import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class SimuladorRedeSocial:
    def __init__(self, num_usuarios=300, num_conteudos=200, max_steps=200):
        self.num_usuarios = num_usuarios
        self.num_conteudos = num_conteudos
        self.max_steps = max_steps

        # Inicialização do Espaço 3D [-1, 1]
        self.usuarios = np.random.uniform(-1.0, 1.0, (num_usuarios, 3))
        self.conteudos = np.random.uniform(-1.0, 1.0, (num_conteudos, 3))
        self.historico_usuarios = [self.usuarios.copy()]

    def avaliar_conteudo_nocivo(self, conteudo):
        x, y, z = conteudo
        if y > 0.6 and (x < -0.5 or x > 0.5):
            return True
        return False

    def aplicar_penalizacao(self, indice_conteudo):
        # Envia o conteúdo nocivo para o "limbo" da moderação
        self.conteudos[indice_conteudo] = np.array([0.0, -1.0, 0.0])

    def passo_simulacao(self, step):
        novas_posicoes = self.usuarios.copy()

        for i, usuario in enumerate(self.usuarios):
            amostra_conteudos = np.random.choice(self.num_conteudos, size=5, replace=False)

            for c_idx in amostra_conteudos:
                conteudo = self.conteudos[c_idx]

                if self.avaliar_conteudo_nocivo(conteudo):
                    if np.random.rand() < 0.8: # 80% de eficácia na moderação
                        self.aplicar_penalizacao(c_idx)
                        continue

                distancia = np.linalg.norm(usuario - conteudo)
                taxa_aprendizado = 0.05

                if distancia < 0.4:  # Atração (Homofilia)
                    novas_posicoes[i] += taxa_aprendizado * (conteudo - usuario)
                elif 0.4 <= distancia < 1.0: # Rejeição (Dissonância moderada)
                    novas_posicoes[i] -= (taxa_aprendizado / 2) * (conteudo - usuario)

        self.usuarios = np.clip(novas_posicoes, -1.0, 1.0)
        self.historico_usuarios.append(self.usuarios.copy())

    def executar(self):
        print("Iniciando simulação da rede social...")
        for step in range(self.max_steps):
            self.passo_simulacao(step)
        print("Simulação concluída!")
        return self.historico_usuarios


# Executando a simulação
simulador = SimuladorRedeSocial(num_usuarios=300, num_conteudos=200, max_steps=200)
historico = simulador.executar()

# Configuração da Animação 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')

historico_usuarios = simulador.historico_usuarios
num_frames = len(historico_usuarios)

def atualizar(frame):
    ax.clear()

    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.set_zlim([-1.1, 1.1])

    ax.set_title(f"Simulação 3D: Emergência de Agrupamentos (Passo {frame}/{num_frames - 1})", fontsize=12)
    ax.set_xlabel("Eixo X (Ideologia Política)", fontsize=9)
    ax.set_ylabel("Eixo Y (Agressividade / Tom)", fontsize=9)
    ax.set_zlabel("Eixo Z (Interesse Temático)", fontsize=9)

    posicoes_atuais = historico_usuarios[frame]

    # Plota os usuários com cor única, observando agrupamentos orgânicos
    ax.scatter(
        posicoes_atuais[:, 0],
        posicoes_atuais[:, 1],
        posicoes_atuais[:, 2],
        c='royalblue',
        s=60,
        alpha=0.8,
        edgecolors='w'
    )

    ax.view_init(elev=30, azim=45)


print("Gerando e salvando a animação em GIF (isso pode levar alguns segundos)...")
anim = FuncAnimation(fig, atualizar, frames=num_frames, interval=150, repeat=False)

anim.save('simulacao_clusters.gif', writer='pillow', fps=8)
print("Arquivo 'simulacao_clusters.gif' gerado e salvo com sucesso na pasta do projeto!")

plt.show()
