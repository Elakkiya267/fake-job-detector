import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import os

# Load data
dataset = load_dataset("json", data_files="data/train.jsonl", split="train")

# Tokenizer and model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Add pad token if needed
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Tokenize function
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)

# Data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Training args
training_args = TrainingArguments(
    output_dir="models/fine_tuned_generator",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=500,
    save_total_limit=2,
    prediction_loss_only=True,
    learning_rate=5e-5,
    warmup_steps=100,
    logging_steps=100,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_dataset,
)

# Train
os.makedirs("models", exist_ok=True)
trainer.train()

# Save
trainer.save_model("models/fine_tuned_generator")
tokenizer.save_pretrained("models/fine_tuned_generator")

print("Training complete! Model saved to models/fine_tuned_generator")