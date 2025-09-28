import os
from typing import Dict, Optional

import requests
from flask import Flask, render_template, request


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    @app.route("/", methods=["GET", "POST"])
    def index():
        context: Dict[str, Optional[str]] = {
            "api_url": "",
            "api_key": "",
            "header_name": "Authorization",
            "error": None,
            "preview": None,
            "content_type": None,
            "content_length": None,
        }

        if request.method == "POST":
            api_url = request.form.get("api_url", "").strip()
            api_key = request.form.get("api_key", "").strip()
            header_name = request.form.get("header_name", "Authorization").strip() or "Authorization"

            context.update({
                "api_url": api_url,
                "api_key": api_key,
                "header_name": header_name,
            })

            if not api_url:
                context["error"] = "API URL is required."
                return render_template("index.html", **context)

            headers = {}
            if api_key:
                headers[header_name] = api_key if header_name.lower() != "authorization" else f"Bearer {api_key}"

            try:
                response = requests.get(api_url, headers=headers, timeout=30)
                response.raise_for_status()
            except requests.RequestException as exc:
                context["error"] = f"Failed to fetch the file: {exc}"
                return render_template("index.html", **context)

            content_type = response.headers.get("Content-Type")
            content_length = response.headers.get("Content-Length")
            raw_content = response.content

            preview = None
            if content_type and ("text" in content_type or "json" in content_type or "xml" in content_type):
                encoding = response.encoding or "utf-8"
                preview = raw_content.decode(encoding, errors="replace")
                # Limit preview length to avoid rendering huge files
                if len(preview) > 5000:
                    preview = preview[:5000] + "\n... (truncated)"

            context.update(
                {
                    "preview": preview,
                    "content_type": content_type,
                    "content_length": content_length,
                }
            )

        return render_template("index.html", **context)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
