"""Serve a plain HTML interface for the in-memory inspection logger."""

from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
from urllib.parse import parse_qs

from inspection_logger import Inspection, acceptance_limits


HOST = "127.0.0.1"
PORT = 8000
current_inspection: Optional[Inspection] = None


def render_page(message: str = "") -> str:
    """Build the page using plain HTML and the current in-memory inspection."""
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Inspection Defect Logger</title>",
        "</head>",
        "<body>",
        "<h1>Inspection Defect Logger</h1>",
    ]

    if message:
        parts.append(f'<p role="alert"><strong>{escape(message)}</strong></p>')

    if current_inspection is None:
        parts.extend(
            [
                "<p>Inspect the real items, then enter the batch and sample information here.</p>",
                "<h2>Start an inspection</h2>",
                '<form action="/start" method="post">',
                '<p><label>Batch ID <input name="batch_id" type="text" required></label></p>',
                '<p><label>Sample size <input name="sample_size" type="number" min="1" step="1" required></label></p>',
                '<p><button type="submit">Start inspection</button></p>',
                "</form>",
            ]
        )
    else:
        inspection = current_inspection
        parts.extend(
            [
                f"<h2>Batch {escape(inspection.batch_id)}</h2>",
                f"<p>Sample size: {inspection.sample_size}</p>",
                "<h2>Record a defect</h2>",
                '<form action="/record" method="post">',
                '<p><label>Severity '
                '<select name="severity" required>'
                '<option value="" selected disabled>Choose severity</option>'
                '<option value="critical">Critical</option>'
                '<option value="major">Major</option>'
                '<option value="minor">Minor</option>'
                "</select></label></p>",
                '<p><label>Short description <input name="description" type="text" required></label></p>',
                '<p><button type="submit">Record defect</button></p>',
                "</form>",
                "<p>Recorded defects cannot be edited or deleted. Check the severity and description before submitting.</p>",
                "<h2>Defects recorded</h2>",
            ]
        )

        if inspection.defects:
            parts.append("<ol>")
            for defect in inspection.defects:
                severity = escape(defect["severity"].capitalize())
                description = escape(defect["description"])
                parts.append(f"<li>{severity}: {description}</li>")
            parts.append("</ol>")
        else:
            parts.append("<p>No defects recorded.</p>")

        parts.extend(
            [
                "<h2>Verdict</h2>",
                f"<p><strong>{inspection.verdict()}</strong></p>",
                "<p>This inspection is held in memory and will be cleared when the server stops.</p>",
            ]
        )

    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)


class InspectionHandler(BaseHTTPRequestHandler):
    def send_page(self, page: str, status: int = 200) -> None:
        body = page.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def redirect_to_main(self) -> None:
        """Return to GET / after a successful form submission."""
        self.send_response(303)
        self.send_header("Location", "/")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        if self.path != "/":
            self.send_page("<h1>Not found</h1>", status=404)
            return
        self.send_page(render_page())

    def do_POST(self) -> None:
        global current_inspection

        length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)

        def value(name: str) -> str:
            return form.get(name, [""])[0].strip()

        if self.path == "/start":
            if current_inspection is not None:
                self.send_page(render_page("An inspection is already active. Its recorded defects have been preserved."), status=409)
                return
            batch_id = value("batch_id")
            raw_sample_size = value("sample_size")
            try:
                sample_size = int(raw_sample_size)
                acceptance_limits(sample_size)
                if not batch_id:
                    raise ValueError("Batch ID cannot be empty.")
            except ValueError as error:
                message = str(error)
                if raw_sample_size and not raw_sample_size.isdigit():
                    message = "Sample size must be a whole number of at least 1."
                self.send_page(render_page(message))
                return

            current_inspection = Inspection(batch_id=batch_id, sample_size=sample_size)
            self.redirect_to_main()
            return

        if self.path == "/record":
            if current_inspection is None:
                self.send_page(render_page("Start an inspection before recording defects."))
                return
            try:
                current_inspection.record_defect(value("severity"), value("description"))
            except ValueError as error:
                self.send_page(render_page(str(error)))
                return
            self.redirect_to_main()
            return

        self.send_page("<h1>Not found</h1>", status=404)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), InspectionHandler)
    print(f"Inspection Defect Logger is running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped. The in-memory inspection was cleared.")
    finally:
        server.server_close()
