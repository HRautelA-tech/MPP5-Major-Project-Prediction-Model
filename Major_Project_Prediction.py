import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Path to the saved model and tokenizer directory
model_path = "./gpt2-project-ideas-tools"

# Load the model
model = GPT2LMHeadModel.from_pretrained(model_path)

# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

# Move the model to the appropriate device (GPU or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Generate new project ideas
def generate_project(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],  # Ensure attention mask is included
        max_length=max_length,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.9,
        top_k=50,
        top_p=0.95,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Default prompt for random projects
prompt = "Project Idea:"

print(f"\nGenerated Random Project Ideas with Descriptions and Tools:\n")

generated_projects = []
for _ in range(12):
    project = generate_project(prompt)
    generated_projects.append(project)

# Remove duplicates
unique_projects = list(set(generated_projects))

# HTML output file path
html_file_path = "ProjectUI/Output.html"

# Create HTML file and write the output
with open(html_file_path, "w") as html_file:
    # Write the beginning of the HTML structure
    html_file.write("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="Output.css">
        <title>Interactive Course Cards</title>
    </head>
    <body>
        <h1>New AI Generated Ideas</h1>
        <a href="../interface/UI1.html"><button>Back</button></a>
        <div class="ag-format-container">
            <div class="ag-courses_box">
    """)

    # Write each project idea into the HTML file
    for project in unique_projects:
        if "Description" in project and "Tools Used" in project:
            project = project.replace("Project Idea:", "").strip()
            try:
                project_idea, description_and_tools = project.split('Description:')
                description, tools = description_and_tools.split('Tools Used:')
                html_file.write(f"""
                <div class="ag-courses_item">
                    <a class="ag-courses-item_link">
                        <div class="ag-courses-item_bg"></div>
                        <div class="ag-courses-item_title">{project_idea.strip()}</div>
                        <div class="ag-courses-item_date-box">
                            {description.strip()} 
                            <span class="ag-courses-item_date">{tools.strip()}</span>
                        </div>
                    </a>
                </div>
                """)
            except ValueError:
                print(f"\nSkipping malformed project: {project}")

    # Write the end of the HTML structure
    html_file.write("""
            </div>
        </div>
    </body>
    </html>
    """)

print(f"\nGenerated random project ideas saved to {html_file_path}")
