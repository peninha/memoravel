# tests/test_memoravel.py

import unittest
import os
from memoravel import Memoravel

class TestMemoravel(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_memoria.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_preserve_initial_memories(self):
        # Test preservation of 2 initial messages
        memory = Memoravel(limit=5, max_tokens=100, preserve_initial_memories=2, preserve_system_memories=False, preserve_last_memories=0)
        memory.add("user", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("user", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("user", "Mensagem 5")
        memory.add("user", "Mensagem 6")  # Should remove messages after the initial ones

        history = memory.recall()
        #print(history)
        # The first two messages should be preserved
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")

    def test_preserve_system_memories(self):
        # Test preservation of system messages
        memory = Memoravel(limit=5, max_tokens=100, preserve_system_memories=True, preserve_last_memories=0)
        memory.add("system", "Mensagem de sistema 1")
        memory.add("user", "Mensagem 2")
        memory.add("user", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem de sistema 5")
        memory.add("user", "Mensagem 6")  # Should remove user messages, not system messages
        memory.add("user", "Mensagem 7")  # Should remove user messages, not system messages
        memory.add("user", "Mensagem 8")  # Should remove user messages, not system messages
        memory.add("user", "Mensagem 9")  # Should remove user messages, not system messages

        history = memory.recall()
        #print(history)
        # The system message should be preserved
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]["role"], "system")
        self.assertEqual(history[0]["content"], "Mensagem de sistema 1")
        self.assertEqual(history[1]["role"], "system")
        self.assertEqual(history[1]["content"], "Mensagem de sistema 5")
        self.assertEqual(history[2]["role"], "user")
        self.assertEqual(history[2]["content"], "Mensagem 7")

    def test_preserve_separated_system_memories(self):
        # Test preservation of system messages
        memory = Memoravel(limit=5, max_tokens=100, preserve_system_memories=True, preserve_last_memories=0)
        memory.add("system", "Mensagem de sistema 1")
        memory.add("user", "Mensagem 2")
        memory.add("user", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem de sistema 5")
        memory.add("user", "Mensagem 6")  # Should remove user messages, not system messages
        memory.add("user", "Mensagem 7")  # Should remove user messages, not system messages
        memory.add("system", "Mensagem de sistema 8")  # Should remove user messages, not system messages
        memory.add("user", "Mensagem 9")  # Should remove user messages, not system messages

        history = memory.recall()
        # The system message should be preserved
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
        # Test trim based on the number of tokens
        memory = Memoravel(limit=10, max_tokens=50, preserve_system_memories=False, preserve_last_memories=0)  # Set a relatively low token limit for testing
        memory.add("user", "Mensagem curta")
        memory.add("user", "Mensagem um pouco mais longa")
        memory.add("user", "Uma mensagem consideravelmente mais longa que deveria contar mais tokens")

        # Add another message to ensure it exceeds the token limit
        memory.add("user", "Uma mensagem muito, muito longa que definitivamente vai ultrapassar o limite de tokens e causar uma remoção de mensagens anteriores para se ajustar ao max_tokens")

        history = memory.recall()
        #print(history)
        total_tokens = sum(len(memory.encoder.encode(msg["content"])) for msg in history)
        #print(total_tokens)
        # Ensure that the total number of tokens does not exceed the limit
        self.assertTrue(total_tokens <= 50)

        # Verify if the number of messages was adjusted correctly
        self.assertLess(len(history), 4)  # Ensure at least one message was removed


    def test_trim_based_on_limit(self):
        # Test that the history is reduced to the allowed message limit
        memory = Memoravel(limit=3, max_tokens=100, preserve_system_memories=False, preserve_last_memories=0)
        memory.add("user", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("user", "Mensagem 3")
        memory.add("user", "Mensagem 4")

        history = memory.recall()
        # Verify if the history was trimmed correctly
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 2")
    
    
    def test_no_limit_on_message_count_when_limit_zero(self):
        # Test behavior with limit=0 (no limit on the number of messages)
        memory = Memoravel(limit=0, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        for i in range(10):
            memory.add("user", f"Mensagem {i+1}")

        history = memory.recall()
        # Should contain all 10 added messages, as there is no limit on the number
        self.assertEqual(len(history), 10)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[-1]["content"], "Mensagem 10")

    def test_no_token_limit_when_max_tokens_zero(self):
        # Test behavior with max_tokens=0 (no token limit)
        memory = Memoravel(limit=5, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        memory.add("user", "Mensagem curta")
        memory.add("user", "Outra mensagem")
        memory.add("user", "Mais uma mensagem")
        memory.add("user", "Mensagem bastante longa que deveria, normalmente, contar muitos tokens")

        history = memory.recall()
        # Should contain all 4 added messages, even if the total token count is high
        self.assertEqual(len(history), 4)

    def test_no_limits_when_both_zero(self):
        # Test behavior with limit=0 and max_tokens=0 (no limits applied)
        memory = Memoravel(limit=0, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        for i in range(50):
            memory.add("user", f"Mensagem {i+1}")

        history = memory.recall()
        # Should contain all 50 added messages without removals
        self.assertEqual(len(history), 50)

    def test_trim_based_on_limit_only_when_tokens_zero(self):
        # Test that only the message count limit is applied when max_tokens=0
        memory = Memoravel(limit=3, max_tokens=0, preserve_system_memories=False, preserve_last_memories=0)
        memory.add("user", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("user", "Mensagem 3")
        memory.add("user", "Mensagem 4")  # Should remove the first message

        history = memory.recall()
        # Verify if the history was correctly trimmed to 3 messages
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 2")
        
    def test_cant_remove_anymore(self):
        # Test when it is not possible to remove as many memories as necessary
        memory = Memoravel(limit=3, max_tokens=10, preserve_initial_memories=0, preserve_system_memories=True, preserve_last_memories=0)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
    
        history = memory.recall()
        
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 3")
        self.assertEqual(history[2]["content"], "Mensagem 5")
        self.assertEqual(history[3]["content"], "Mensagem 8")

    def test_preserve_last_memories(self):
        # Test if the last memories are preserved
        memory = Memoravel(limit=2, max_tokens=0, preserve_initial_memories=2, preserve_system_memories=False, preserve_last_memories=2)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("assistant", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        memory.add("user", "Mensagem 9")
        memory.add("user", "Mensagem 10")
        memory.add("system", "Mensagem 11")

        history = memory.recall()

        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")
        self.assertEqual(history[2]["content"], "Mensagem 10")
        self.assertEqual(history[3]["content"], "Mensagem 11")

    def test_add_and_recall(self):
        memory = Memoravel()
        memory.add("assistant", "Test message")
        history = memory.recall()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "assistant")
        self.assertEqual(history[0]["content"], "Test message")

    def test_save_and_load(self):
        memory = Memoravel()
        memory.add("assistant", "Test message")
        memory.save(self.test_file)

        new_memory = Memoravel()
        new_memory.load(self.test_file)
        history = new_memory.recall()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "assistant")
        self.assertEqual(history[0]["content"], "Test message")

    def test_save_and_load_with_multiple_messages(self):
        memory = Memoravel()
        memory.add("assistant", "Message 1")
        memory.add("user", "Message 2")
        memory.save(self.test_file)

        new_memory = Memoravel()
        new_memory.load(self.test_file)
        history = new_memory.recall()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "assistant")
        self.assertEqual(history[0]["content"], "Message 1")
        self.assertEqual(history[1]["role"], "user")
        self.assertEqual(history[1]["content"], "Message 2")
        
    def test_recall_last_n(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        history = memory.recall(last_n=3)

        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 6")
        self.assertEqual(history[1]["content"], "Mensagem 7")
        self.assertEqual(history[2]["content"], "Mensagem 8")

    def test_recall_first_n(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        history = memory.recall(first_n=3)

        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")
        self.assertEqual(history[2]["content"], "Mensagem 3")

    def test_recall_first_and_last(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Message 1")
        memory.add("user", "Message 2")
        memory.add("system", "Message 3")
        memory.add("user", "Message 4")
        memory.add("system", "Message 5")
        memory.add("user", "Message 6")
        memory.add("user", "Message 7")
        memory.add("system", "Message 8")
        
        with self.assertRaises(ValueError) as context:
            memory.recall(first_n=2, last_n=3)
        self.assertEqual(str(context.exception), "Only one of the parameters 'last_n', 'first_n', or 'slice_range' can be used at a time.")

    def test_recall_index(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        history = memory.recall(index_or_slice = 2)
    
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["content"], "Mensagem 3")

    def test_recall_slice(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        history = memory.recall(index_or_slice = slice(3, 5, 1))

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "Mensagem 4")
        self.assertEqual(history[1]["content"], "Mensagem 5")
    
    def test_recall_slice_negative(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        history = memory.recall(index_or_slice = slice(-5, -3, 1))

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "Mensagem 4")
        self.assertEqual(history[1]["content"], "Mensagem 5")
    
    def test_recall_invert_list(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        history = memory.recall(index_or_slice = slice(-1, -3, -1))

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "Mensagem 8")
        self.assertEqual(history[1]["content"], "Mensagem 7")

    def test_recall_slice_out_of_bounds(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        history = memory.recall(index_or_slice = slice(12, 15, 1))
    
        self.assertEqual(len(history), 0)
    
    def test_delete(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        memory.delete(2)
        memory.delete(slice(3, 5))
        
        history = memory.recall()
    
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")
        self.assertEqual(history[2]["content"], "Mensagem 4")
        self.assertEqual(history[3]["content"], "Mensagem 7")
        self.assertEqual(history[4]["content"], "Mensagem 8")
    
    def test_delete_slice_negative(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 2")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        
        memory.delete(slice(-3, -5, -1))
        
        history = memory.recall()
    
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "Mensagem 1")
        self.assertEqual(history[1]["content"], "Mensagem 2")
        self.assertEqual(history[2]["content"], "Mensagem 5")
        self.assertEqual(history[3]["content"], "Mensagem 6")
    
    def test_insert(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("system", "Mensagem 3")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        memory.insert(1, {"role": "user", "content": "Mensagem 2"})
        
        history = memory.recall()
    
        self.assertEqual(history[1]["content"], "Mensagem 2")
    
    def test_insert_list(self):
        memory = Memoravel(limit=10)
        memory.add("system", "Mensagem 1")
        memory.add("user", "Mensagem 4")
        memory.add("system", "Mensagem 5")
        memory.add("user", "Mensagem 6")
        memory.add("user", "Mensagem 7")
        memory.add("system", "Mensagem 8")
        
        memory.insert(1, [{"role": "user", "content": "Mensagem 2"},
                          {"role": "user", "content": "Mensagem 3"}])
        
        history = memory.recall()
    
        self.assertEqual(history[1]["content"], "Mensagem 2")
        self.assertEqual(history[2]["content"], "Mensagem 3")

if __name__ == "__main__":
    unittest.main()
