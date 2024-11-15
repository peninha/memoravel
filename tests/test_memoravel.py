# tests/test_memoravel.py

import unittest
import os
import json
from memoravel import Memoravel

class TestMemoravel(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_memoria.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_preserve_initial_memories(self):
        # Testa preservação de 2 mensagens iniciais
        memoravel = Memoravel(limit=5, max_tokens=100, preserve_initial_memories=2, preserve_system_memories=False, preserve_last_memories=0)
        memoravel.add("user", "Mensagem 1")
        memoravel.add("user", "Mensagem 2")
        memoravel.add("user", "Mensagem 3")
        memoravel.add("user", "Mensagem 4")
        memoravel.add("user", "Mensagem 5")
        memoravel.add("user", "Mensagem 6")  # Deve remover mensagens após as iniciais

        history = memoravel.recall()
        #print(history)
        # As duas primeiras mensagens devem ser preservadas
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")

    def test_preserve_system_memories(self):
        # Testa preservação de mensagens do sistema
        memoravel = Memoravel(limit=5, max_tokens=100, preserve_system_memories=True, preserve_last_memories=0)
        memoravel.add("system", "Mensagem de sistema 1")
        memoravel.add("user", "Mensagem 2")
        memoravel.add("user", "Mensagem 3")
        memoravel.add("user", "Mensagem 4")
        memoravel.add("system", "Mensagem de sistema 5")
        memoravel.add("user", "Mensagem 6")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add("user", "Mensagem 7")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add("user", "Mensagem 8")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add("user", "Mensagem 9")  # Deve remover mensagens de usuário, não de sistema

        history = memoravel.recall()
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
        memoravel.add("system", "Mensagem de sistema 1")
        memoravel.add("user", "Mensagem 2")
        memoravel.add("user", "Mensagem 3")
        memoravel.add("user", "Mensagem 4")
        memoravel.add("system", "Mensagem de sistema 5")
        memoravel.add("user", "Mensagem 6")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add("user", "Mensagem 7")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add("system", "Mensagem de sistema 8")  # Deve remover mensagens de usuário, não de sistema
        memoravel.add("user", "Mensagem 9")  # Deve remover mensagens de usuário, não de sistema

        history = memoravel.recall()
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
        memoravel.add("user", "Mensagem curta")
        memoravel.add("user", "Mensagem um pouco mais longa")
        memoravel.add("user", "Uma mensagem consideravelmente mais longa que deveria contar mais tokens")

        # Adiciona mais uma mensagem para garantir que ultrapasse o limite de tokens
        memoravel.add("user", "Uma mensagem muito, muito longa que definitivamente vai ultrapassar o limite de tokens e causar uma remoção de mensagens anteriores para se ajustar ao max_tokens")

        history = memoravel.recall()
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
        memoravel.add("user", "Mensagem 1")
        memoravel.add("user", "Mensagem 2")
        memoravel.add("user", "Mensagem 3")
        memoravel.add("user", "Mensagem 4")

        history = memoravel.recall()
        # Verifica se o histórico foi cortado corretamente
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 2")
    
    
    def test_no_limit_on_message_count_when_limit_zero(self):
        # Testa comportamento com limit=0 (sem limite de quantidade de mensagens)
        memoravel = Memoravel(limit=0, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        for i in range(10):
            memoravel.add("user", f"Mensagem {i+1}")

        history = memoravel.recall()
        # Deve conter todas as 10 mensagens adicionadas, pois não há limite de quantidade
        self.assertEqual(len(history), 10)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[-1]["content"], "Mensagem 10")

    def test_no_token_limit_when_max_tokens_zero(self):
        # Testa comportamento com max_tokens=0 (sem limite de tokens)
        memoravel = Memoravel(limit=5, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        memoravel.add("user", "Mensagem curta")
        memoravel.add("user", "Outra mensagem")
        memoravel.add("user", "Mais uma mensagem")
        memoravel.add("user", "Mensagem bastante longa que deveria, normalmente, contar muitos tokens")

        history = memoravel.recall()
        # Deve conter todas as 4 mensagens adicionadas, mesmo que o total de tokens seja alto
        self.assertEqual(len(history), 4)

    def test_no_limits_when_both_zero(self):
        # Testa comportamento com limit=0 e max_tokens=0 (sem limites aplicados)
        memoravel = Memoravel(limit=0, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        for i in range(50):
            memoravel.add("user", f"Mensagem {i+1}")

        history = memoravel.recall()
        # Deve conter todas as 50 mensagens adicionadas, sem remoções
        self.assertEqual(len(history), 50)

    def test_trim_based_on_limit_only_when_tokens_zero(self):
        # Testa que apenas o limite de quantidade é aplicado quando max_tokens=0
        memoravel = Memoravel(limit=3, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        memoravel.add("user", "Mensagem 1")
        memoravel.add("user", "Mensagem 2")
        memoravel.add("user", "Mensagem 3")
        memoravel.add("user", "Mensagem 4")  # Deve remover a primeira mensagem

        history = memoravel.recall()
        # Verifica se o histórico foi cortado corretamente para 3 mensagens
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 2")
        
    def test_cant_remove_anymore(self):
        # Testa quando não é possível remover tantas memórias quanto necessário
        memoravel = Memoravel(limit=3, max_tokens=10, preserve_initial_memories=0, preserve_system_memories=True, preserve_last_memories=0)
        memoravel.add("system", "Mensagem 1")
        memoravel.add("user", "Mensagem 2")
        memoravel.add("system", "Mensagem 3")
        memoravel.add("user", "Mensagem 4")
        memoravel.add("system", "Mensagem 5")
        memoravel.add("user", "Mensagem 6")
        memoravel.add("user", "Mensagem 7")
        memoravel.add("system", "Mensagem 8")
    
        history = memoravel.recall()
        #print(history)
        tokens = memoravel._count_tokens()
        #print(f"tokens: {tokens}")
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 3")
        self.assertEqual(history[2]["content"], "Mensagem 5")
        self.assertEqual(history[3]["content"], "Mensagem 8")

    def test_preserve_last_memories(self):
        # Testa se mantém as últimas memórias
        memoravel = Memoravel(limit=2, max_tokens=0, preserve_initial_memories=2, preserve_system_memories=False, preserve_last_memories=2)
        memoravel.add("system", "Mensagem 1")
        memoravel.add("user", "Mensagem 2")
        memoravel.add("system", "Mensagem 3")
        memoravel.add("user", "Mensagem 4")
        memoravel.add("system", "Mensagem 5")
        memoravel.add("user", "Mensagem 6")
        memoravel.add("assistant", "Mensagem 7")
        memoravel.add("system", "Mensagem 8")
        memoravel.add("user", "Mensagem 9")
        memoravel.add("user", "Mensagem 10")
        memoravel.add("system", "Mensagem 11")

        history = memoravel.recall()
        #print(history)
        #tokens = memoravel._count_tokens()
        #print(f"tokens: {tokens}")
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")
        self.assertEqual(history[2]["content"], "Mensagem 10")
        self.assertEqual(history[3]["content"], "Mensagem 11")

    def test_add_and_recall(self):
        memoria = Memoravel()
        memoria.add("assistant", "Test message")
        history = memoria.recall()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "assistant")
        self.assertEqual(history[0]["content"], "Test message")

    def test_save_and_load(self):
        memoria = Memoravel()
        memoria.add("assistant", "Test message")
        memoria.save(self.test_file)

        nova_memoria = Memoravel()
        nova_memoria.load(self.test_file)
        history = nova_memoria.recall()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "assistant")
        self.assertEqual(history[0]["content"], "Test message")

    def test_save_and_load_with_multiple_messages(self):
        memoria = Memoravel()
        memoria.add("assistant", "Message 1")
        memoria.add("user", "Message 2")
        memoria.save(self.test_file)

        nova_memoria = Memoravel()
        nova_memoria.load(self.test_file)
        history = nova_memoria.recall()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "assistant")
        self.assertEqual(history[0]["content"], "Message 1")
        self.assertEqual(history[1]["role"], "user")
        self.assertEqual(history[1]["content"], "Message 2")

if __name__ == "__main__":
    unittest.main()
