# ========================================
# 📊 MODULO: esg_visuals.py
# Funzioni per generare grafici e tabelle ESG personalizzati
# ========================================

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64

# ========================================
# 🎨 UTILITÀ: Funzione per applicare colori brand
# ========================================

def apply_brand_colors(ax, colors):
    """
    Applica i colori forniti ai grafici (in ordine).
    """
    for i, bar in enumerate(ax.patches):
        bar.set_color(colors[i % len(colors)])


# ========================================
# 📊 BAR CHART ESG
# ========================================

def generate_bar_chart(data, x_col, y_col, title, colors):
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=data, x=x_col, y=y_col)
    apply_brand_colors(ax, colors)
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig_to_base64(plt)


# ========================================
# 📈 LINE CHART ESG
# ========================================

def generate_line_chart(data, x_col, y_col, title, colors):
    plt.figure(figsize=(8, 5))
    for i, column in enumerate(y_col):
        plt.plot(data[x_col], data[column], label=column, color=colors[i % len(colors)])

    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel("Valore")
    plt.legend()
    plt.tight_layout()

    return fig_to_base64(plt)


# ========================================
# 🥧 PIE CHART ESG
# ========================================

def generate_pie_chart(labels, values, title, colors):
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')

    return fig_to_base64(plt)


# ========================================
# 📋 TABELLA ESG
# ========================================

def generate_table(data, title):
    """
    Genera una tabella in HTML a partire da un DataFrame.
    """
    table_html = f"<h4>{title}</h4>" + data.to_html(classes='esg-table', index=False)
    return table_html


# ========================================
# 💾 CONVERSIONE GRAFICO IN BASE64 PER STREAMLIT
# ========================================

def fig_to_base64(plt_obj):
    buf = BytesIO()
    plt_obj.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode()
    plt_obj.close()
    return image_base64
