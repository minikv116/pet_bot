import torch

# Максимальная длина сообщения минус 14 символов на "Полный текст: " 
tg_message_lenght = 4082

# Определение процессора
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
