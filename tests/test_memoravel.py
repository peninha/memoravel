# tests/test_memoravel.py

import unittest
from memoravel import Memoravel

class TestMemoravel(unittest.TestCase):

    def test_preserve_initial_memories(self):
        # Testa preservação de 2 mensagens iniciais
        memoravel = Memoravel(limit=5, max_tokens=100, preserve_initial_memories=2, preserve_system_memories=False, preserve_last_memories=0)
        memoravel.add_memory("user", "Mensagem 1")
        memoravel.add_memory("user", "Mensagem 2")
        memoravel.add_memory("user", "Mensagem 3")
        memoravel.add_memory("user", "Mensagem 4")
        memoravel.add_memory("user", "Mensagem 5")
        memoravel.add_memory("user", "Mensagem 6")  # Deve remover mensagens após as iniciais

        history = memoravel.get_history()
        #print(history)
        # As duas primeiras mensagens devem ser preservadas
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")

    def test_preserve_system_memories(self):
        # Testa preservação de mensagens do sistema
        memoravel = Memoravel(limit=5, max_tokens=100, preserve_system_memories=True, preserve_last_memories=0)
        memoravel.add_memory("system", "Mensagem de sistema 1")
        memoravel.add_memory("user", "Mensagem 2")
        memoravel.add_memory("user", "Mensagem 3")
        memoravel.add_memory("user", "Mensagem 4")
        memoravel.add_memory("system", "Mensagem de sistema 5")
        memoravel.add_memory("user", "Mensagem 6")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add_memory("user", "Mensagem 7")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add_memory("user", "Mensagem 8")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add_memory("user", "Mensagem 9")  # Deve remover mensagens de usuário, não de sistema

        history = memoravel.get_history()
        #print(history)
        # A mensagem do sistema deve ser preservada
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]["role"], "system")
        self.assertEqual(history[0]["content"], "Mensagem de sistema 1")
        self.assertEqual(history[1]["role"], "system")
        self.assertEqual(history[1]["content"], "Mensagem de sistema 5")
        self.assertEqual(history[2]["role"], "user")
        self.assertEqual(history[2]["content"], "Mensagem 7")

    def test_preserve_separated_system_memories(self):
        # Testa preservação de mensagens do sistema
        memoravel = Memoravel(limit=5, max_tokens=100, preserve_system_memories=True, preserve_last_memories=0)
        memoravel.add_memory("system", "Mensagem de sistema 1")
        memoravel.add_memory("user", "Mensagem 2")
        memoravel.add_memory("user", "Mensagem 3")
        memoravel.add_memory("user", "Mensagem 4")
        memoravel.add_memory("system", "Mensagem de sistema 5")
        memoravel.add_memory("user", "Mensagem 6")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add_memory("user", "Mensagem 7")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add_memory("system", "Mensagem de sistema 8")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add_memory("user", "Mensagem 9")  # Deve remover mensagens de usuário, não de sistema

        history = memoravel.get_history()
        # A mensagem do sistema deve ser preservada
        #print(history)
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]["role"], "system")
        self.assertEqual(history[0]["content"], "Mensagem de sistema 1")
        self.assertEqual(history[1]["role"], "system")
        self.assertEqual(history[1]["content"], "Mensagem de sistema 5")
        self.assertEqual(history[2]["role"], "user")
        self.assertEqual(history[2]["content"], "Mensagem 7")
        self.assertEqual(history[3]["role"], "system")
        self.assertEqual(history[3]["content"], "Mensagem de sistema 8")

    def test_trim_based_on_max_tokens(self):
        # Testa trim baseado no número de tokens
        memoravel = Memoravel(limit=10, max_tokens=50, preserve_system_memories=False, preserve_last_memories=0)  # Define um limite de tokens relativamente baixo para teste
        memoravel.add_memory("user", "Mensagem curta")
        memoravel.add_memory("user", "Mensagem um pouco mais longa")
        memoravel.add_memory("user", "Uma mensagem consideravelmente mais longa que deveria contar mais tokens")

        # Adiciona mais uma mensagem para garantir que ultrapasse o limite de tokens
        memoravel.add_memory("user", "Uma mensagem muito, muito longa que definitivamente vai ultrapassar o limite de tokens e causar uma remoção de mensagens anteriores para se ajustar ao max_tokens")

        history = memoravel.get_history()
        #print(history)
        total_tokens = sum(len(memoravel.encoder.encode(msg["content"])) for msg in history)
        #print(total_tokens)
        # Certifique-se de que o total de tokens não excede o limite
        self.assertTrue(total_tokens <= 50)

        # Verifica se a quantidade de mensagens foi ajustada corretamente
        self.assertLess(len(history), 4)  # Certifica-se de que ao menos uma mensagem foi removida


    def test_trim_based_on_limit(self):
        # Testa que o histórico é reduzido ao limite de mensagens permitido
        memoravel = Memoravel(limit=3, max_tokens=100, preserve_system_memories=False, preserve_last_memories=0)
        memoravel.add_memory("user", "Mensagem 1")
        memoravel.add_memory("user", "Mensagem 2")
        memoravel.add_memory("user", "Mensagem 3")
        memoravel.add_memory("user", "Mensagem 4")

        history = memoravel.get_history()
        # Verifica se o histórico foi cortado corretamente
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 2")
    
    
    def test_no_limit_on_message_count_when_limit_zero(self):
        # Testa comportamento com limit=0 (sem limite de quantidade de mensagens)
        memoravel = Memoravel(limit=0, max_tokens=100, preserve_system_memories=False, preserve_last_memories=0)
        for i in range(10):
            memoravel.add_memory("user", f"Mensagem {i+1}")

        history = memoravel.get_history()
        # Deve conter todas as 10 mensagens adicionadas, pois não há limite de quantidade
        self.assertEqual(len(history), 10)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[-1]["content"], "Mensagem 10")

    def test_no_token_limit_when_max_tokens_zero(self):
        # Testa comportamento com max_tokens=0 (sem limite de tokens)
        memoravel = Memoravel(limit=5, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        memoravel.add_memory("user", "Mensagem curta")
        memoravel.add_memory("user", "Outra mensagem")
        memoravel.add_memory("user", "Mais uma mensagem")
        memoravel.add_memory("user", "Mensagem bastante longa que deveria, normalmente, contar muitos tokens")

        history = memoravel.get_history()
        # Deve conter todas as 4 mensagens adicionadas, mesmo que o total de tokens seja alto
        self.assertEqual(len(history), 4)

    def test_no_limits_when_both_zero(self):
        # Testa comportamento com limit=0 e max_tokens=0 (sem limites aplicados)
        memoravel = Memoravel(limit=0, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        for i in range(50):
            memoravel.add_memory("user", f"Mensagem {i+1}")

        history = memoravel.get_history()
        # Deve conter todas as 50 mensagens adicionadas, sem remoções
        self.assertEqual(len(history), 50)

    def test_trim_based_on_limit_only_when_tokens_zero(self):
        # Testa que apenas o limite de quantidade é aplicado quando max_tokens=0
        memoravel = Memoravel(limit=3, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        memoravel.add_memory("user", "Mensagem 1")
        memoravel.add_memory("user", "Mensagem 2")
        memoravel.add_memory("user", "Mensagem 3")
        memoravel.add_memory("user", "Mensagem 4")  # Deve remover a primeira mensagem

        history = memoravel.get_history()
        # Verifica se o histórico foi cortado corretamente para 3 mensagens
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 2")
        
    def test_cant_remove_anymore(self):
        # Testa quando não é possível remover tantas memórias quanto necessário
        memoravel = Memoravel(limit=3, max_tokens=10, preserve_initial_memories=0, preserve_system_memories=True, preserve_last_memories=0)
        memoravel.add_memory("system", "Mensagem 1")
        memoravel.add_memory("user", "Mensagem 2")
        memoravel.add_memory("system", "Mensagem 3")
        memoravel.add_memory("user", "Mensagem 4")
        memoravel.add_memory("system", "Mensagem 5")
        memoravel.add_memory("user", "Mensagem 6")
        memoravel.add_memory("user", "Mensagem 7")
        memoravel.add_memory("system", "Mensagem 8")
    
        history = memoravel.get_history()
        #print(history)
        #tokens = memoravel._count_tokens()
        #print(f"tokens: {tokens}")
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 3")
        self.assertEqual(history[2]["content"], "Mensagem 5")
        self.assertEqual(history[3]["content"], "Mensagem 8")

    def test_preserve_last_memories(self):
        # Testa se mantém as últimas memórias
        memoravel = Memoravel(limit=2, max_tokens=0, preserve_initial_memories=2, preserve_system_memories=False, preserve_last_memories=2)
        memoravel.add_memory("system", "Mensagem 1")
        memoravel.add_memory("user", "Mensagem 2")
        memoravel.add_memory("system", "Mensagem 3")
        memoravel.add_memory("user", "Mensagem 4")
        memoravel.add_memory("system", "Mensagem 5")
        memoravel.add_memory("user", "Mensagem 6")
        memoravel.add_memory("assistant", "Mensagem 7")
        memoravel.add_memory("system", "Mensagem 8")
        memoravel.add_memory("user", "Mensagem 9")
        memoravel.add_memory("user", "Mensagem 10")
        memoravel.add_memory("system", "Mensagem 11")

        history = memoravel.get_history()
        #print(history)
        #tokens = memoravel._count_tokens()
        #print(f"tokens: {tokens}")
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")
        self.assertEqual(history[2]["content"], "Mensagem 10")
        self.assertEqual(history[3]["content"], "Mensagem 11")

if __name__ == "__main__":
    unittest.main()
