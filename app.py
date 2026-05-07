from flask import Flask, render_template, request, send_file, abort
import os

app = Flask(__name__)

# --- CONFIGURATION ---
TICKETS_DIR = os.path.join(os.getcwd(), 'tickets')

# SRE Check: Ensure the persistence layer (folder) exists
if not os.path.exists(TICKETS_DIR):
    os.makedirs(TICKETS_DIR)

@app.route('/')
def index():
    """Renders the modern frontend booking form."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """
    Handles the POST request from the form, 
    populates the ticket template, and generates a PDF.
    """
    try:
        # 1. Import WeasyPrint inside the function to catch DLL errors locally
        from weasyprint import HTML
    except OSError as e:
        # If the GTK libraries are missing, return a clear error to the browser
        return (f"SRE ALERT: System Dependencies Missing.<br>"
                f"Error: {str(e)}<br><br>"
                f"<b>Fix:</b> You must install 'GTK for Windows Runtime' and restart VS Code."), 500

    # 2. Capture data from the Frontend
    # We use .get() with defaults to prevent the app from crashing on empty inputs
    data = {
        "pnr": request.form.get('pnr', 'N/A'),
        "name": request.form.get('name', 'GUEST').upper(),
        "train_name": request.form.get('train_name', '20413/MAHAKAL EXPRESS'),
        "from_stn": request.form.get('from_stn', 'VARANASI JN (BSB)'),
        "to_stn": request.form.get('to_stn', 'INDORE JN BG (INDB)'),
        "date": request.form.get('date', '09-Apr-2026')
    }

    # 3. Render the HTML Template with the data
    try:
        rendered_html = render_template('ticket.html', **data)
        
        # 4. Define PDF path
        filename = f"IRCTC_Ticket_{data['pnr']}.pdf"
        pdf_path = os.path.join(TICKETS_DIR, filename)

        # 5. Execute PDF Generation
        HTML(string=rendered_html).write_pdf(pdf_path)

        # 6. Send file to user
        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        return f"Backend Error: {str(e)}", 500

if __name__ == '__main__':
    # Running in Debug mode helps us see real-time logs in the VS Code terminal
    print("Starting IRCTC Replica Server...")
    print(f"Check your tickets at: {TICKETS_DIR}")
    app.run(debug=True, port=5000)