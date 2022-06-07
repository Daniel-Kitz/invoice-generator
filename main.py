from decimal import Decimal
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable as FlexTable
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.pdf import PDF

pdf = Document()

page = Page()
pdf.append_page(page)

page_layout = SingleColumnLayout(page)
page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)

def mainitem_table(item):
    table = Table(number_of_rows=2+int(len(item)), number_of_columns=5, column_widths=[Decimal(1.1), Decimal(1.5), Decimal(4), Decimal(1.8), Decimal(2)])
    for i in ["Anzahl", "Einheit", "Bezeichnung", "Einzelpreis", "Gesamtpreis"]:
        table.add(
            TableCell(
                Paragraph(i, font="Helvetica-Bold")
            )
        )

    for i in range(len(item)):
        current = item[i]
        for k in range(len(current)):
            match k:
                case 0:
                    table.add(
                        TableCell(
                            Paragraph(current[k], horizontal_alignment=Alignment.CENTERED)
                        )
                    )
                case 2:
                    table.add(
                        TableCell(
                            Paragraph(current[k])
                        )
                    )
                case 3:
                    value = current[k]
                    value_string = str(value).replace(".", ",")
                    temp = value_string.split(",")
                    try:
                        if len(temp[1]) == 1:
                            value_string += "0 €"
                        else:
                            value_string += " €"
                    except:
                        value_string += ",00 €" 
                    table.add(
                        TableCell(
                            Paragraph(value_string, horizontal_alignment=Alignment.RIGHT)
                        )
                    )
                case _:
                    table.add(
                        TableCell(
                            Paragraph(current[k], horizontal_alignment=Alignment.CENTERED)
                        )
                    )

        price = float(current[3].replace(",", "."))
        full_price = str(float(current[0]) * price)
        full_price = str(full_price).replace(".", ",")
        temp = full_price.split(",")
        try:
            if len(temp[1]) == 1:
                full_price += "0 €"
            else:
                full_price += " €"
        except:
            full_price += ",00 €"
        full_price_list = []
        full_price_list += [full_price]
        table.add(Paragraph(full_price, horizontal_alignment=Alignment.RIGHT))

        table.add(
            TableCell(
                Paragraph("Gesamtbetrag: ", font="Helvetica-Bold"), col_span=4
            )
        )

        total = 0
        for y in full_price_list:
            total += float(y.replace(",", ".").replace("€", " "))
        total = str(total).replace(".", ",")
        temp = total.split(",")
        try:
            if len(temp[1]) == 1:
                total += "0 €"
            else:
                total += " €"
        except:
            total += ",00 €"
        
        table.add(Paragraph(str(total), horizontal_alignment=Alignment.RIGHT))


    table.set_padding_on_all_cells(Decimal(5), Decimal(10), Decimal(5), Decimal(5))
    return table

def invoice_info(invoice_date):
    table = Table(number_of_columns=2, number_of_rows=2, column_widths=[Decimal(6), Decimal(1)])
    
    table.add(Paragraph("Rechnungsdatum: ", horizontal_alignment=Alignment.RIGHT)).add(Paragraph(invoice_date, horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph("Rechnungs-Nr.: ", horizontal_alignment=Alignment.RIGHT)).add(Paragraph(" "))
    
    table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table.no_borders()
    return table


def issuer_table_top(issuer_name, issuer_address, issuer_plz, issuer_city, issuer_id):
    table = Table(number_of_columns=2, number_of_rows=4, column_widths=[Decimal(1.7), Decimal(1.3)])
    
    table.add(Paragraph(" ")).add(Paragraph(issuer_name, horizontal_alignment=Alignment.RIGHT, font_size=Decimal(24), font="Helvetica"))
    table.add(Paragraph(" ")).add(Paragraph(issuer_address, horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(" ")).add(Paragraph("{} {}".format(issuer_plz, issuer_city), horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(" ")).add(Paragraph("Steuernummer: {}".format(issuer_id), horizontal_alignment=Alignment.RIGHT))
    
    table.set_padding_on_all_cells(
        Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table.no_borders()

    small_info = Paragraph("{} - {} - {} {}".format(issuer_name, issuer_address,  issuer_plz, issuer_city), border_bottom=True, font_size=Decimal(11)) 

    return [table, small_info]

def receiver_table_information(rec_gender, rec_name, rec_address, rec_plz, rec_city):
    table = FlexTable(number_of_columns=1, number_of_rows=4)
    
    table.add(Paragraph(rec_gender))
    table.add(Paragraph(rec_name))
    table.add(Paragraph(rec_address))
    table.add(Paragraph("{} {}".format(rec_plz, rec_city)))
    
    table.set_padding_on_all_cells(
        Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table.no_borders()
    return table

def main():
    # Document Variables
    doc: Document = Document()
    page: Page = Page()
    doc.append_page(page)
    layout: PageLayout = SingleColumnLayout(page)

    # Adding to layout
    layout.add(issuer_table_top("Max Mustermann", "musterstrasse 12", "12345", "Musterstadt", "12/34/56789")[0])
    layout.add(issuer_table_top("Max Mustermann", "musterstrasse 12", "12345", "Musterstadt", "12/34/56789")[1])
    layout.add(receiver_table_information("Herr", "Max Mustermann", "musterstrasse 12", "12345", "Musterstadt"))
    layout.add(invoice_info("19.12.2002"))
    layout.add(Paragraph("Rechnung", font="Helvetica-Bold", font_size=Decimal(18)))
    layout.add(mainitem_table([["1", "Pauschal", "Trockenbau", "2500"]]))

    # store
    with open("output.pdf", "wb") as pdf_output_file:
        PDF.dumps(pdf_output_file, doc)


if __name__ == "__main__":
    main()
