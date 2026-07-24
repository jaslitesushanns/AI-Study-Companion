import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(title, content, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            title,
            styles["Heading1"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            content.replace("\n","<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename



def weekly_chart():

    data = pd.DataFrame({
        "Day":[
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ],

        "Hours":[
            2,
            3,
            4,
            2,
            5,
            6,
            4
        ]
    })


    fig = px.bar(
        data,
        x="Day",
        y="Hours",
        title="Weekly Study Hours"
    )

    return fig



def monthly_chart():

    data = pd.DataFrame({

        "Month":[
            "Jan",
            "Feb",
            "Mar",
            "Apr"
        ],

        "Progress":[
            40,
            55,
            70,
            85
        ]
    })


    fig = px.line(
        data,
        x="Month",
        y="Progress",
        markers=True,
        title="Monthly Progress"
    )

    return fig
