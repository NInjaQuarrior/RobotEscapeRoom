# Import necessary libraries
from flask import Flask, render_template, redirect, request, url_for, session, send_file
from flask_session import Session
import pdfkit

# Initialize the Flask app
app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATE_FOLDER'] = 'templates/'
app.config['PDF_FOLDER'] = 'pdfs/'
Session(app)
app.secret_key = 'RobotEscapeRoomMQP2324'

def get_initial_room_state():
    initial_state = [[{"floor": "floor", "walls": ["wall", None, "wall", None]}] * 5] * 5
    print("Initial Room State:", initial_state)
    return initial_state

def separate_sections(input_content):
    sections = {}

    lines = input_content.split('\r\n')

    section_name = None
    section_content = []

    for line in lines:
        # Split each line into words
        words = line.strip().split(':')

        if len(words) >= 2:
            # If a new section is encountered, store the previous section's data
            if section_name is not None:
                sections[section_name] = {'title': section_name, 'content': section_content}
                section_content = []

            section_name = words[0].strip()
            section_content.append(words[1].strip())
        else:
            # If the line doesn't have a colon, assume it's part of the content
            section_content.append(line.strip())

    # Store the last section
    if section_name is not None:
        sections[section_name] = {'title': section_name, 'content': section_content}

    # Print each section to the console
    for section, data in sections.items():
        print(f"Section: {data['title']}")
        print(f"Content: {data['content']}")
        print("-" * 30)

    return sections

# --- Flask templates ---
@app.route('/', methods=["GET", "POST"])
def build():
    # Retrieve the file content from the session
    file_content = session.get('file_content', '')
    sections = separate_sections(file_content)

    # Retrieve the room state from the session
    room_state = session.get('room_state')

    # If room_state is not in the session, set it
    if room_state is None:
        room_state = get_initial_room_state() # doesn't work
        session['room_state'] = room_state

    return render_template('roomLayout.html', sections=sections, file_content=file_content, room_state=room_state)

@app.route('/planner', methods=["GET", "POST"])
def planner():
    # Retrieve the file content from the session
    file_content = session.get('file_content', '')
    sections = separate_sections(file_content)
    
    return render_template('htnp.html', sections=sections, file_content=file_content)

@app.route('/finalProduct', methods=["GET", "POST"])
def finalProduct():
    # Retrieve the file content from the session
    file_content = session.get('file_content', '')
    sections = separate_sections(file_content)

    # Retrieve the room state from the session
    room_state = session.get('room_state')
    
    # Retrieve the room state from the session
    theme = session.get('CSStheme')
    
    return render_template('finalProduct.html', sections=sections, file_content=file_content, room_state=room_state, theme=theme)

@app.route('/generatePDF', methods=['POST'])
def generate_pdf():
    canvas_content = request.form.get('canvas_content')
    console_output = request.form.get('console_output')
    
    config = pdfkit.configuration(wkhtmltopdf="C:\\Users\\Kaelin\\OneDrive - Worcester Polytechnic Institute (wpi.edu)\\Desktop\\RobotEscapeRoom23-24_wizard\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    
    htmlfile = app.config['TEMPLATE_FOLDER'] + 'finalProduct.html'
    pdffile = app.config['PDF_FOLDER'] + 'demo.pdf'
    print(htmlfile, pdffile)
    
    # Convert to pdffile
    pdfkit.from_file(htmlfile, pdffile, configuration=config, options={"enable-local-file-access": ""})
    
    return send_file("pdfs\\demo.pdf", as_attachment=False)

# --- Flask templates Ends ---


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
