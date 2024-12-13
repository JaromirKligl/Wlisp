from flask import Flask, render_template, request, json, redirect
import pathlib


import tree_direcory
import reader
import lisp_eval


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',title="WLISP",tree_html= tree_direcory.get_tree_from_path(pathlib.Path.cwd() / 'user_dir'))

def save_file(text,url):
    with open(url,"w") as file:
        file.write(text)

def load_file(url):
    with open(url,"r") as file:
        text = file.read()
    return text

def editor(editor_text, listener_text):
    return render_template('ide.html', title="WLISP-IDE", listener_text = listener_text, editor_text = editor_text)

@app.route('/<path:filepath>', methods=["GET", "POST"])
def evaluate(filepath):
    if request.method == "POST":
        editor_text = request.form.get("editor_text", "")
        listener_text = request.form.get("listener_text", "")
        if "save" in request.form:
            save_file(editor_text, filepath)
            return editor(editor_text, listener_text)

        if "save_and_close" in request.form:
            save_file(editor_text, filepath)
            return redirect("/")

        if "close" in request.form:
            return redirect("/")

        if "submit_editor" in request.form:
            try:
                listener_text = lisp_eval.evaluate(reader.reader(editor_text))
            except Exception as expt:
                return editor(editor_text, str(expt))
            return editor(editor_text, listener_text)

        try:
            listener_text = lisp_eval.evaluate(reader.reader(listener_text))
        except Exception as expt:
            return editor(editor_text, str(expt))

        return editor(editor_text, listener_text)

    return render_template('ide.html', title="WLISP-IDE", editor_text = load_file(filepath))


if __name__ == '__main__':
    app.run(port=4444,debug=True)