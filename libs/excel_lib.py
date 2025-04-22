from pathlib import Path
from typing import List
import xlsxwriter

def create_xlsx(file_name: Path,
                ph_list: List[float],
                pKA: float,
                acid_name: str,
                base_name: str):

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({"bold": 1})

    headings = ["pH", f"Acide {acid_name} (%)", f"Base {base_name} (%)"]
    worksheet.write_row("A1", headings, bold)

    # pH col (A)
    worksheet.write_column("A2", ph_list)

    # Acid col (B)
    row = 1
    for i in range(2, len(ph_list)+2):
        worksheet.write(row, 1, f"=100/(1+10^(A{i}-{pKA}))")
        row += 1

    # Base col (C)
    row = 1
    for i in range(2, len(ph_list) + 2):
        worksheet.write(row, 2, f"=100-B{i}")
        row += 1

    # Graphique
    chart = workbook.add_chart({'type': 'scatter', "subtype": "smooth",
                                'marker': {'type': 'cross', 'size': 2}
                                })

    chart.add_series(
        {
            "name": "=Sheet1!$B$1",
            "categories": f"=Sheet1!$A$2:$A${len(ph_list)+1}",
            "values": f"=Sheet1!$B$2:$B${len(ph_list)+1}",
        }
    )

    # Configure second series.
    chart.add_series(
        {
            "name": "=Sheet1!$C$1",
            "categories": f"=Sheet1!$A$2:$A${len(ph_list)+1}",
            "values": f"=Sheet1!$C$2:$C${len(ph_list)+1}",
        }
    )

    chart.set_title({
        'name': f"Diagramme de distribution de l'acide ({acid_name}) et de la base ({base_name})",
        'name_font': {
            'name': 'Calibri',
        },
    })

    chart.set_x_axis({
        'name': 'pH',
        'name_font': {
            'name': 'Calibri',
        }
    })

    chart.set_y_axis({
        'name': '%',
        'name_font': {
            'name': 'Calibri',
        }
    })

    worksheet.insert_chart('E1', chart)

    # save xlsx
    workbook.close()