#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for
import argparse

app = Flask(__name__)

# Path to the kanjidic file will be loaded here from a cmd-line argument
kanjidic_path = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    if not request.args.get("q"):
        return redirect(url_for("home"))

    all_defs = []
    with open(kanjidic_path, "r", encoding="euc-jp") as file:
        for kanji in request.args.get("q"):
            file.seek(0)
            for line in file:
                # The kanji is expected to be at the beginning of the line
                if not line.find(kanji) == 0:
                    continue

                # Find the definitions - they are enclosed within curly braces
                def_beg = line.find("{")
                def_end = line.rfind("}")
                if def_beg == -1 or def_end == 0 or def_beg > def_end:
                    break

                def_str = line[def_beg:def_end]
                # Replace the curly braces with commas for a nicer presentation
                def_str = def_str.replace("{", "").replace("}", ",")

                # Display the kanji alongside its definition
                all_defs += [kanji + " " + def_str]

                # Since this kanji was found, no need to search further
                break

    return render_template("search.html", defs=all_defs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web app for finding kanji meanings in Japanese sentences.")
    parser.add_argument("-k", "--kanjidic", help="kanjidic file", required=True)
    parser.add_argument("-p", "--port", nargs="?", type=int, help="server port (default 9019)", default=9019)
    args = parser.parse_args()

    kanjidic_path = args.kanjidic
    app.run(port=args.port)
