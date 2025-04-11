import time
import tkinter as tk

def load_api_spec(file_path):
    """Load API specification from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def update_footer(output_text, distinct_api_count, total_iterations=0, start_time=None):
    """Update footer with comparison stats."""
    if start_time is None:
        start_time = time.time()
    elapsed_time = time.time() - start_time
    footer_text = f"Distinct APIs: {distinct_api_count} | Total Comparisons: {total_iterations} | Time Elapsed: {elapsed_time:.2f} seconds"
    output_text.configure(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, footer_text)
    output_text.configure(state=tk.DISABLED)