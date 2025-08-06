import os
import stat
import shutil
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset
import torch


#Delete the file before training
def remove_file_or_directory(path):
    try:
        if os.path.isfile(path):
            # Remove file
            os.remove(path)
            print(f"File '{path}' deleted successfully.")
        elif os.path.isdir(path):
            # Remove directory and its contents
            shutil.rmtree(path, onerror=handle_permission_error)
            print(f"Directory '{path}' deleted successfully.")
        else:
            print(f"Path '{path}' does not exist.")
    except PermissionError:
        print(f"Permission denied: Unable to delete '{path}'. Try running as an administrator.")
    except Exception as e:
        print(f"An error occurred while deleting '{path}': {e}")

def handle_permission_error(func, path, exc_info):
    # Handle permission errors during rmtree
    exc_type, exc_value, _ = exc_info
    if exc_type is PermissionError:
        # Change the permission and retry
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        print(f"Error while accessing '{path}': {exc_value}")

# Example usage
paths = [
    r"C:\Users\sr310\OneDrive\Desktop\MPP 5\logs",
    r"C:\Users\sr310\OneDrive\Desktop\MPP 5\gpt2-project-ideas-tools"
]

for path in paths:
    remove_file_or_directory(path)
#----------------------------------------------------------------------------------------------------------------------------->
# Function to read dataset from file
def load_dataset_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            data = [line.strip() for line in lines if line.strip()]  # Remove empty lines and strip whitespace
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")
        return []

# Check GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("\nDevice:", "GPU" if torch.cuda.is_available() else "CPU")
print("\n")
# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Ensure the tokenizer has a padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token or "[PAD]"
    if tokenizer.pad_token == "[PAD]":
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# Load the model and move it to the appropriate device (GPU or CPU)
model = GPT2LMHeadModel.from_pretrained(model_name).to(device)

# Load dataset from file (Make sure you have a 'projectideas.txt' with data in the required format)
file_path = "projectideas.txt"  # Specify the file path
data = load_dataset_from_file(file_path)

# Check if data was loaded
if not data:
    raise ValueError("No data found in the file. Please ensure the file contains valid project ideas.")

# Prepare the dataset by converting the text data into the right format
formatted_data = []
for line in data:
    # Split the input line into "Project Idea", "Description", and "Tools Used"
    try:
        project_idea, description_and_tools = line.split("Description: ")
        description, tools = description_and_tools.split("Tools Used: ")
        formatted_data.append(f"Project Idea: {project_idea.strip()} Description: {description.strip()} Tools Used: {tools.strip()}")
    except ValueError:
        print(f"Skipping improperly formatted line: {line}")

# Prepare the dataset
dataset = Dataset.from_dict({"text": formatted_data})
print(f"Loaded {len(formatted_data)} project ideas from the file.")

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=256, return_tensors="pt")

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Add labels (copy of input_ids)
tokenized_dataset = tokenized_dataset.map(
    lambda examples: {'labels': examples['input_ids']},
    batched=True
)

# Ensure the final columns include 'input_ids', 'attention_mask', and 'labels'
tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# Define the data collator
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./gpt2-project-ideas-tools",
    eval_strategy="no",
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    num_train_epochs=15,
    save_strategy="epoch",
    fp16=torch.cuda.is_available(),  # Use FP16 if CUDA (GPU) is available
    logging_dir="./logs",
    logging_steps=10,
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,  # Use data_collator instead of tokenizer
)

print("Fine-tuning the model...")
trainer.train()

# Save the fine-tuned model
trainer.save_model("./gpt2-project-ideas-tools")
tokenizer.save_pretrained("./gpt2-project-ideas-tools")

print("Fine-tuning complete. Model saved!")