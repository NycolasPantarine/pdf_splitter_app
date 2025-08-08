from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
from pathlib import Path
import zipfile
import uuid

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB (ajuste se quiser)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("pdf_file")
        if not file or not file.filename.lower().endswith(".pdf"):
            return "Envie um arquivo PDF válido.", 400

        # pastas isoladas por sessão
        session_id = str(uuid.uuid4())
        upload_dir = Path("uploads") / session_id
        output_dir = Path("output") / session_id
        upload_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        # salva o PDF enviado
        pdf_path = upload_dir / file.filename
        file.save(pdf_path)

        # lê e separa
        leitor = PdfReader(str(pdf_path))
        for i, page in enumerate(leitor.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)
            out_path = output_dir / f"pagina_{i}.pdf"
            with open(out_path, "wb") as f_out:
                writer.write(f_out)   # <<< CORRETO

        # cria ZIP
        zip_path = output_dir.with_suffix(".zip")
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(output_dir.glob("*.pdf")):
                zf.write(p, arcname=p.name)

        # oferece o zip pra download
        return send_file(str(zip_path), as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)