from flask import render_template, Blueprint, request, redirect, flash, current_app

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
    return render_template("pages/viz_template.html", viz_html=gen_network())


def gen_network():
    data = get_sheet_data("School 1")

    ids = set([d["Name"] for d in data])

    G = nx.Graph()
    for d in data:
        color = "cornflowerblue"
        if d.get("Vape", "False") == "True":
            color = "crimson"
        print(d, color)
        G.add_node(d["Name"], size=10, color=color)

    for d in data:
        friends = [
            d.get("Friend1", None),
            d.get("Friend2", None),
            d.get("Friend3", None),
        ]
        for f in friends:
            if f in ids:
                print("adding edge between", d["Name"], f)
                G.add_edge(d["Name"], f)

    pos_ = nx.spring_layout(G)

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
        node_trace["text"] += tuple(["<b>" + node[:10] + "</b>"])

    fig = go.Figure(
        data=edge_trace + [node_trace],
        layout=go.Layout(
            title="Network graph made with Python",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    return fig.to_html()


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
