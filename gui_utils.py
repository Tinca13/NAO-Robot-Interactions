import webbrowser as wb

def load_webpage(url):
    wb.open_new(url)

def toggle_checkbox_state(checkbox, toggle_text):
    if checkbox.text() == toggle_text[0]:
        checkbox.setText(toggle_text[1])
    elif checkbox.text() == toggle_text[1]:
        checkbox.setText(toggle_text[0])

def toggle_label_status(label, text_options, colours):
    if label.text() == text_options[0]:
        idx = 1
    elif label.text() == text_options[1]:
        idx = 0
        
    label.setStyleSheet("background-color: rgb{}".format(colours[idx]))
    label.setText(text_options[idx])