from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Texturas
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')

BLOCK_SIZE = 1.0

# Lista de blocos e "save simulado"
voxels = []
simulated_save = []

# Classe de bloco
class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            scale=BLOCK_SIZE,
            collider='box'
        )
        voxels.append(self)

    def input(self, key):
        if self.hovered:
            # destruir bloco
            if key == 'left mouse down':
                voxels.remove(self)
                destroy(self)

            # colocar bloco de acordo com a camada
            if key == 'right mouse down':
                y = self.position.y
                target_pos = self.position + mouse.normal
                if y < 0:            # subterrâneo -> pedregulho
                    Voxel(position=target_pos, texture=stone_texture)
                elif y == 0:         # camada de grama -> grama
                    Voxel(position=target_pos, texture=grass_texture)
                else:                # acima da superfície -> pedregulho
                    Voxel(position=target_pos, texture=stone_texture)

# Gerar terreno inicial
WORLD_SIZE = 16
for x in range(-WORLD_SIZE//2, WORLD_SIZE//2):
    for z in range(-WORLD_SIZE//2, WORLD_SIZE//2):
        Voxel(position=(x, -1, z), texture=stone_texture)  # subterrâneo
        Voxel(position=(x, 0, z), texture=grass_texture)   # superfície

# Jogador FPS
player = FirstPersonController()
player.gravity = 0.5
player.jump_height = 2.5
player.speed = 5
player.cursor.visible = True

# Salvar "simulado" na memória
def save_simulated():
    global simulated_save
    simulated_save = [(v.position, v.texture) for v in voxels]
    print("Save simulado realizado!")

# Carregar o save simulado
def load_simulated():
    if not simulated_save:
        print("Nenhum save simulado encontrado!")
        return
    # destruir blocos atuais
    for v in voxels[:]:
        destroy(v)
        voxels.remove(v)
    # recriar blocos do save simulado
    for pos, tex in simulated_save:
        Voxel(position=pos, texture=tex)
    print("Save simulado carregado!")

# Teclas End e Home
def input(key):
    if key == 'end':
        save_simulated()    # salva
    elif key == 'home':
        load_simulated()    # carrega

app.run()