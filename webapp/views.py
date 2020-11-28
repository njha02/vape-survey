from flask import render_template, Blueprint, request, redirect, flash, current_app

import json
import functools

import hashlib
import numpy
import plotly.graph_objects as go
import networkx as nx
import os

from .forms import SurveyForm
from .sheets import write_to_sheet, get_sheet_data

blueprint = Blueprint("pages", __name__)


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = SurveyForm(request.form)

    if form.validate_on_submit():
        submit_to_sheet(form.data)
        return redirect("/thankyou")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in the %s field - %s"
                    % (getattr(form, field).label.text, error),
                    "error",
                )
    return render_template("forms/survey.html", form=form)


@blueprint.route("/thankyou", methods=["GET"])
def thankyou():
    return render_template("pages/thankyou_template.html")


def submit_to_sheet(data):
    del data["csrf_token"]

    def encrypt_string(s):
        s = s.lower().strip()
        return hashlib.sha512(str.encode(s)).hexdigest()

    for x in [
        "School",
        "Name",
        "Email",
        "Age",
        "Grade",
        "Gender",
        "Closest 1",
        "Closest 2",
        "Closest 3",
        "Influence",
        "Vape",
    ]:
        assert x in data

    data["Name"] = encrypt_string(data["Name"].strip().lower())
    data["Closest 1"] = encrypt_string(data["Closest 1"].strip().lower())
    data["Closest 2"] = encrypt_string(data["Closest 2"].strip().lower())
    data["Closest 3"] = encrypt_string(data["Closest 3"].strip().lower())
    if "Email" in data:
        email = data["Email"]
        write_to_sheet(f"{data['School']} Emails", [email])
        del data["Email"]
    write_to_sheet(
        data["School"],
        [
            data["School"],
            data["Name"],
            data["Age"],
            data["Grade"],
            data["Gender"],
            data["Closest 1"],
            data["Closest 2"],
            data["Closest 3"],
            data["Influence"],
            data["Vape"],
        ],
    )


@blueprint.route("/about", methods=["GET"])
def about():
    return render_template("pages/about_template.html")


@blueprint.route("/viz", methods=["GET"])
def viz():
    schools = [
        "North Cross",
        "School 1",
        "School 2",
    ]
    return render_template(
        "pages/viz_template.html",
        graphs=[(s, gen_network(s)) for s in schools],
    )


def gen_network(tab_name: str):
    data = get_sheet_data(tab_name)

    # To use cache need to pass hashable data
    @functools.lru_cache(maxsize=10)
    def _gen_network(jsonified_data):
        _data = json.loads(jsonified_data)
        data = [json.loads(j) for j in _data]
        ids = set([d["Name"] for d in data])

        G = nx.Graph()
        for d in data:
            color = "cornflowerblue"
            if d.get("Vape", "False") == "True":
                color = "crimson"
            G.add_node(
                d["Name"],
                size=5,
                color=color,
                label=f"""
                <br>Id: {d["Name"]}</br>
                <br>Influence: {d["Influence"]}</br>
                <br>Age: {d["Age"]}</br>
                <br>Grade: {d["Grade"]}</br>
                <br>Gender: {d["Gender"]}</br>
                <extra></extra>
                """,
            )

        for d in data:
            friends = [
                d.get("Friend1", None),
                d.get("Friend2", None),
                d.get("Friend3", None),
            ]
            for f in friends:
                if f in ids:
                    G.add_edge(d["Name"], f)

        pos_ = nx.spring_layout(G, seed=12)

        def make_edge(x, y, text, width):
            return go.Scatter(
                x=x,
                y=y,
                line=dict(width=width, color="cornflowerblue"),
                hoverinfo="text",
                text=([text]),
                mode="lines",
            )

        edge_trace = []
        for edge in G.edges():
            char_1 = edge[0]
            char_2 = edge[1]
            x0, y0 = pos_[char_1]
            x1, y1 = pos_[char_2]
            text = char_1 + "--" + char_2
            trace = make_edge(
                [x0, x1, None],
                [y0, y1, None],
                text,
                width=0.3,
            )
            edge_trace.append(trace)

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            textposition="top center",
            textfont_size=10,
            mode="markers+text",
            hoverinfo="none",
            marker=dict(color=[], size=[], line=None),
        )
        for node in G.nodes():
            x, y = pos_[node]
            node_trace["x"] += tuple([x])
            node_trace["y"] += tuple([y])
            node_trace["marker"]["color"] += tuple([G.nodes()[node]["color"]])
            node_trace["marker"]["size"] += tuple([5 * G.nodes()[node]["size"]])
            # node_trace["text"] += tuple(["<b>" + node[:10] + "</b>"])
            node_trace["text"] += tuple([""])
            node_trace["hovertemplate"] = G.nodes()[node]["label"]

        fig = go.Figure(
            data=edge_trace + [node_trace],
            layout=go.Layout(
                title="",
                titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                width=1000,
                height=800,
            ),
        )
        return fig.to_html()

    return _gen_network(json.dumps([json.dumps(s) for s in data]))


# def gen_friends_list():
#     names = [
#         "a",
#         "b",
#         "c",
#         "d",
#         "e",
#         "f",
#         "g",
#         "h",
#         "i",
#         "j",
#         "k",
#         "l",
#         "m",
#         "n",
#         "o",
#         "p",
#     ]
#     ids = [encrypt_string(s) for s in names]
#     print("\n".join(ids))
#     for i in ids:
#         options = set(ids)
#         options.discard(i)
#         friend1 = random.choice(list(options))
#         options.discard(friend1)
#         friend2 = random.choice(list(options))
#         options.discard(friend2)
#         friend3 = random.choice(list(options))
#         options.discard(friend3)
#         print("\t".join([friend1, friend2, friend3]))
