API Comparison Tool
A sleek Python desktop app to compare API specifications using BERT for semantic similarity. Powered by a modern CustomTkinter GUI, it offers intuitive single and batch comparisons with real-time metrics.
✨ **Features**
  Compare two API specs with BERT-driven similarity scores.
  Batch compare .txt files in a folder.
  Choose BERT models (e.g., bert-base-uncased, bert-large-cased).
  Dark-mode GUI with animated loading, file selection, and metrics.
  Reset fields and scalable UI.
  Customizable branding (default: HSBC logo).
🚀 **Get Started**
  Prerequisites
  Python 3.8+
  Sufficient memory (GPU optional)
  Installation
  Clone the repo:
  bash
  git clone https://github.com/your-username/api-comparison-tool.git
  cd api-comparison-tool
  Install dependencies:
  bash
  pip install torch transformers sentence-transformers customtkinter pillow
  Add assets:
  Place OpenSans-Regular.ttf at C:/Users/Ravi/Downloads/static/ (adjust path if needed).
  Place hsbc_logo.png at C:/Users/Ravi/Desktop/ (or your logo).
🎯 **Usage**
  Run:
  bash
  python api_comparison_tool.py
  In the GUI:
  Select: Pick two .txt API specs.
  Model: Choose a BERT model.
  Compare: View similarity score.
  Full Scan: Analyze all .TXT files in C:/Users/Ravi/Desktop/Sample.
  Reset: Clear fields.
  Example:
  Select api1.txt, api2.txt.
  Choose bert-base-uncased.
  Get score: 0.8923.
🛠️ **How It Works**
  Loads .txt API specs.
  Encodes text in BERT chunks (512 tokens, 50 overlap).
  Computes cosine similarity.
  Shows scores and metrics (APIs, comparisons, time).
🔧 **Customize**
  Folder: Edit folder_path for batch scans.
  UI: Adjust scaling_factor (default: 1.2).
  Models: Add BERT variants to dropdown.
  Branding: Swap hsbc_logo.png.
⚠️ **Troubleshooting**
  Files: Check paths for specs, font, logo.
  Memory: Use smaller models or GPU.
  Output: Ensure files are selected.
📌 **Limitations**
  .txt files only.
  Fixed folder for batch scans.
  BERT is resource-heavy.
🌟 **Credits**
  Hugging Face Transformers
  CustomTkinter
