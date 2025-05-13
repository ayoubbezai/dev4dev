"""
GUI Application for Resume PDF Processor
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import json
from datetime import datetime

# Import the main processing function
try:
    from main import main
except ImportError:
    # If running as a standalone executable
    print("Running in standalone mode")

class PDFProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume PDF Processor")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set the application icon if available
        try:
            if getattr(sys, 'frozen', False):
                # If running as compiled exe
                application_path = sys._MEIPASS
            else:
                # If running in a normal Python environment
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass  # If icon setting fails, continue without icon
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create widgets
        self.create_widgets(main_frame)
        
        # Status variables
        self.is_processing = False
        self.pdf_path = None
        
    def create_widgets(self, parent):
        # Title
        title_label = ttk.Label(
            parent, 
            text="Resume Opportunity Matcher", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_text = "Upload your resume PDF to find matching opportunities"
        desc_label = ttk.Label(parent, text=desc_text, wraplength=500)
        desc_label.pack(pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        # File path display
        self.file_var = tk.StringVar(value="No file selected")
        file_entry = ttk.Entry(file_frame, textvariable=self.file_var, state="readonly", width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT)
        
        # Process button
        self.process_btn = ttk.Button(parent, text="Process Resume", command=self.process_pdf)
        self.process_btn.pack(pady=(0, 20))
        
        # Progress bar
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, length=400, mode="indeterminate")
        self.progress.pack(pady=(0, 20), fill=tk.X)
        
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(parent, textvariable=self.status_var)
        status_label.pack(pady=(0, 10))
        
        # Result preview (scrollable text area)
        preview_frame = ttk.LabelFrame(parent, text="Preview of Results")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to the preview text
        scroll = ttk.Scrollbar(preview_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.preview_text = tk.Text(preview_frame, wrap=tk.WORD, yscrollcommand=scroll.set)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.preview_text.yview)
        
    def browse_file(self):
        """Open file dialog to select a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select Resume PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if file_path:
            self.pdf_path = file_path
            # Show only the filename in the display
            file_name = os.path.basename(file_path)
            self.file_var.set(file_name)
            self.status_var.set(f"Selected: {file_name}")
        
    def process_pdf(self):
        """Process the selected PDF file"""
        if not self.pdf_path:
            messagebox.showwarning("No File Selected", "Please select a PDF file first.")
            return
        
        if self.is_processing:
            messagebox.showinfo("Processing", "Already processing a file. Please wait.")
            return
        
        # Clear previous results
        self.preview_text.delete(1.0, tk.END)
        
        # Update UI for processing state
        self.is_processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.status_var.set("Processing... This may take a few minutes.")
        self.progress.start(10)
        
        # Start processing in a separate thread to keep UI responsive
        threading.Thread(target=self._run_processing, daemon=True).start()
    
    def _run_processing(self):
        """Run the PDF processing in a background thread"""
        try:
            # Call the main processing function with the selected PDF file
            result = main(self.pdf_path)
            
            # Format the result
            if isinstance(result, str):
                formatted_result = result
            else:
                # If result is an object, convert to pretty JSON
                try:
                    formatted_result = json.dumps(result, indent=2)
                except (TypeError, ValueError):
                    formatted_result = str(result)
            
            # Save the result to a text file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
            output_filename = f"{pdf_name}_results_{timestamp}.txt"
            
            # Get the directory of the PDF file
            pdf_dir = os.path.dirname(self.pdf_path)
            output_path = os.path.join(pdf_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_result)
            
            # Update UI with success message and results preview
            self.root.after(0, self._update_ui_success, formatted_result, output_path)
            
        except Exception as e:
            # Handle errors and update UI
            error_msg = f"Error processing file: {str(e)}"
            self.root.after(0, self._update_ui_error, error_msg)
    
    def _update_ui_success(self, result_text, output_path):
        """Update UI after successful processing"""
        self.progress.stop()
        self.is_processing = False
        self.process_btn.config(state=tk.NORMAL)
        
        # Show results in preview area
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, result_text)
        
        # Update status
        self.status_var.set(f"Processing complete! Results saved to: {os.path.basename(output_path)}")
        
        # Show completion message with file path
        messagebox.showinfo(
            "Processing Complete", 
            f"The resume has been analyzed and results have been saved to:\n\n{output_path}"
        )
    
    def _update_ui_error(self, error_msg):
        """Update UI after processing error"""
        self.progress.stop()
        self.is_processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.status_var.set("Error processing file")
        
        # Show error message in preview
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, f"ERROR:\n{error_msg}")
        
        # Show error dialog
        messagebox.showerror("Processing Error", error_msg)


# Main entry point
if __name__ == "__main__":
    # Set up the root window
    root = tk.Tk()
    
    # Apply a theme if available
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="arc")  # Other good themes: "arc", "equilux", "breeze"
    except ImportError:
        # If ttkthemes is not available, use standard Tk
        root = tk.Tk()
    
    # Initialize the app
    app = PDFProcessorApp(root)
    
    # Start the main event loop
    root.mainloop()