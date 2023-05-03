from flask import Flask, render_template, request, redirect, send_file
from extractors.re import extract_remoteok_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("job")

db = {}

@app.route("/")
def home():
    return render_template("home.html", name="msg")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
        len_jobs = len(jobs)
    else:
        remoteok = extract_remoteok_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = remoteok + wwr
        db[keyword] = jobs
        len_jobs = len(jobs)
    if len_jobs == 0:
        return render_template("search.html", keyword=keyword, len_jobs=len_jobs)
    else:
        return render_template("search.html", keyword=keyword, jobs=jobs, len_jobs=len_jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")