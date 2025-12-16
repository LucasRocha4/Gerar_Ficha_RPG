from django.db import models
from django.contrib.auth.models import User

# --- FICHA DE PERSONAGEM ---
class FichaPersonagem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fichas')
    
    nome_personagem = models.CharField(max_length=100)
    classe = models.CharField(max_length=100)
    nivel = models.IntegerField(default=1)
    
    dados_ficha = models.JSONField() 
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_personagem} - {self.classe}"

# --- MESAS DE JOGO ---
class Mesa(models.Model):
    mestre = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mesas_mestradas')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class ParticipacaoMesa(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='participantes')
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    ficha = models.ForeignKey(FichaPersonagem, on_delete=models.SET_NULL, null=True, blank=True)
    data_entrada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mesa', 'jogador')

# --- FEEDBACK ---
class Feedback(models.Model):
    TIPO_CHOICES = [
        ('bug', 'Reportar Erro (Bug)'),
        ('sugestao', 'Sugestão de Melhoria'),
        ('elogio', 'Elogio / Outros'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='sugestao')
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.tipo}] {self.usuario}"