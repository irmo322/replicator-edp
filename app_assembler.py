import os
import json


def main():
    version = "v0.2.0"

    res_folder = "transcriptions"
    template_app_file_path = "template_app.html"
    template_python_main_script_file_path = "template_python_main_script.py"
    brython_script_file_path = "deps/Brython-3.9.0/brython.min.js"
    app_file_path = f"webapp/replicator-edp_{version}.html"
    github_app_file_path = "index.html"

    transcriptions = {}

    for file_name in next(os.walk(res_folder))[2]:
        file_path = os.path.join(res_folder, file_name)
        name = os.path.splitext(file_name)[0]

        with open(file_path, "r", encoding='utf-8') as f:
            text = f.read()

        transcriptions[name] = {
            "text": text
        }

    transcriptions_script = json.dumps(transcriptions, indent=4, ensure_ascii=False)

    with open(template_python_main_script_file_path, "r", encoding='utf-8') as f:
        template_python_main_script = f.read()
    python_main_script = template_python_main_script.replace("##RAW_TRANSCRIPTIONS##", transcriptions_script[1:-1])
    python_main_script = python_main_script.replace("##VERSION##", version)

    with open(brython_script_file_path, "r", encoding='utf-8') as f:
        brython_script = f.read()

    with open(template_app_file_path, "r", encoding='utf-8') as f:
        template_app_script = f.read()
    app_script = template_app_script.replace("##PYTHON_MAIN_SCRIPT##", python_main_script)
    app_script = app_script.replace("##VERSION##", version)
    app_script = app_script.replace("<!--##BRYTHON_SCRIPT##-->", brython_script)

    with open(app_file_path, "w", encoding='utf-8') as f:
        f.write(app_script)

    with open(github_app_file_path, "w", encoding='utf-8') as f:
        f.write(app_script)


if __name__ == '__main__':
    main()
