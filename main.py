from decimal import Decimal
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.square_annotation import SquareAnnotation
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable as FlexTable
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.pdf import PDF

pdf = Document()

page = Page()
pdf.append_page(page)

page_layout = SingleColumnLayout(page)
page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)


def get_information():
    sample = [[{'issuername': 'Stratulat Simion', 'issueraddress': 'Fichtenstr. 24', 'issuerzip': '56626', 'issuercity': 'Andernach', 'issuerid': '14 459 267 081'}, {'clientgender': 'Herr', 'clientname': 'Igor Jmurko', 'clientaddress': 'Korretsweg 26', 'clientzip': '56642', 'clientcity': 'Kruft'}, {'date': '27.05.2022', 'bank': 'KSK Mayen', 'blz': '-', 'iban': 'DE37 5765 0010 0198 5997 22'}], [['1', 'Pauschal', 'Fenstermontage BV. Mainz Hindenmithstr. 8', '1000']]] 
    main_dict = [[{'issuername': "", 'issueraddress': "", 'issuerzip': "", 'issuercity': "", 'issuerid': ""},
                  {'clientgender': "", 'clientname': "", 'clientaddress': "",
                      'clientzip': "", 'clientcity': ""},
                  {"date": "", "bank": "", "blz": "", "iban": ""}],
                 []]

    debug = input('debug? ')
    if debug == "y":
        return sample

    for i in main_dict[0]:
        for k in i:
            typedvalue = input(k + ": ")
            main_dict[0][main_dict[0].index(i)][k] = typedvalue
        print('---------')

    x = "y"
    while x == "y":
        x = input("add an item? (y/n) ")
        if x == "y":
            item = []
            for i in range(4):
                a = input()
                item.append(a)
            main_dict[1].append(item)

    print(main_dict)

    return main_dict


def bottom_payment_info(infoDict):
    table = Table(number_of_columns=2, number_of_rows=4)

    table.add(Paragraph("Bankverbindung: "))
    table.add(Paragraph(" "))

    for key, value in infoDict[2].items():
        match key:
            case "date":
                pass
            case "bank":
                table.add(
                    TableCell(
                        Paragraph(value, font_size=Decimal(11))
                    )
                )
                table.add(
                    TableCell(
                        Paragraph("Steuernummer: " + infoDict[0]['issuerid'], font_size=Decimal(11))
                    )
                )
            case "blz":
                if value != " ":
                    table.add(
                        TableCell(
                            Paragraph(str(key).upper() + ": " + value, font_size=Decimal(11))
                        )
                    )
                    table.add(
                        TableCell(
                            Paragraph(" ", font_size=Decimal(11))
                        )
                    ) 
                else:
                    table.add(
                        TableCell(
                            Paragraph(" ", font_size=Decimal(11))
                        )
                    )
                    table.add(
                        TableCell(
                            Paragraph(" ", font_size=Decimal(11))
                        )
                    )
            case _:
                table.add(
                    TableCell(
                        Paragraph(str(key).upper() + ": " + value, font_size=Decimal(11))
                    )
                )
                table.add(
                    TableCell(
                        Paragraph(" ", font_size=Decimal(11))
                    )
                )

    table.set_padding_on_all_cells(
        Decimal(1), Decimal(1), Decimal(1), Decimal(1))
    table.no_borders()
    return table


def mainitem_table(item):
    table = Table(number_of_rows=2+len(item), number_of_columns=5, column_widths=[
                  Decimal(1.1), Decimal(1.5), Decimal(4), Decimal(1.8), Decimal(2)])
    for i in ["Anzahl", "Einheit", "Bezeichnung", "Einzelpreis", "Gesamtpreis"]:
        table.add(
            TableCell(
                Paragraph(i, font="Helvetica-Bold")
            )
        )

    full_price_list = []

    for i in range(len(item)):
        current = item[i]
        for k in range(len(current)):
            match k:
                case 0:
                    table.add(
                        TableCell(
                            Paragraph(
                                current[k], horizontal_alignment=Alignment.CENTERED)
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
                            Paragraph(value_string,
                                      horizontal_alignment=Alignment.RIGHT)
                        )
                    )
                case _:
                    table.add(
                        TableCell(
                            Paragraph(
                                current[k], horizontal_alignment=Alignment.CENTERED)
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

    table.set_padding_on_all_cells(
        Decimal(5), Decimal(10), Decimal(5), Decimal(5))
    return table


def invoice_info(invoice_date):
    table = Table(number_of_columns=2, number_of_rows=2,
                  column_widths=[Decimal(5.5), Decimal(1.2)])

    table.add(Paragraph("Rechnungsdatum: ", horizontal_alignment=Alignment.RIGHT)).add(
        Paragraph(invoice_date, horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph("Rechnungs-Nr.: ",
              horizontal_alignment=Alignment.RIGHT)).add(Paragraph(" "))

    table.set_padding_on_all_cells(
        Decimal(1), Decimal(1), Decimal(1), Decimal(1))
    table.no_borders()
    return table


def issuer_table_top(issuerDict):
    table = Table(number_of_columns=2, number_of_rows=4,
                  column_widths=[Decimal(1), Decimal(2)])

    table.add(Paragraph(" ")).add(Paragraph(
        issuerDict['issuername'], horizontal_alignment=Alignment.RIGHT, font_size=Decimal(24), font="Helvetica"))
    table.add(Paragraph(" ")).add(
        Paragraph(issuerDict['issueraddress'], horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(" ")).add(Paragraph("{} {}".format(
        issuerDict['issuerzip'], issuerDict['issuercity']), horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(" ")).add(Paragraph("Steuernummer: {}".format(
        issuerDict['issuerid']), horizontal_alignment=Alignment.RIGHT))

    table.set_padding_on_all_cells(
        Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table.no_borders()

    small_info = Paragraph("{} - {} - {} {}".format(issuerDict['issuername'], issuerDict['issueraddress'],
                           issuerDict['issuerzip'], issuerDict['issuercity']), border_bottom=True, font_size=Decimal(12))

    return [table, small_info]


def receiver_table_information(clientDict):
    table = FlexTable(number_of_columns=1, number_of_rows=4)

    table.add(Paragraph(clientDict['clientgender']))
    table.add(Paragraph(clientDict['clientname']))
    table.add(Paragraph(clientDict['clientaddress']))
    table.add(Paragraph("{} {}".format(
        clientDict['clientzip'], clientDict['clientcity'])))

    table.set_padding_on_all_cells(
        Decimal(1), Decimal(1), Decimal(1), Decimal(1))
    table.no_borders()
    return table


def main():

    mainDict = get_information()

    # Document Variables
    doc: Document = Document()
    page: Page = Page()
    doc.append_page(page)
    layout: PageLayout = SingleColumnLayout(page)

    # Adding to layout
    layout.add(issuer_table_top(mainDict[0][0])[0])
    layout.add(issuer_table_top(mainDict[0][0])[1])
    layout.add(receiver_table_information(mainDict[0][1]))
    layout.add(invoice_info(mainDict[0][2]['date']))
    layout.add(Paragraph("Rechnung", font="Helvetica-Bold", font_size=Decimal(18)))
    layout.add(mainitem_table(mainDict[1]))
    layout.add(Paragraph(
        "Die Umsatzsteuer für diese Leistung schuldet nach §13b UStG der Leistungempfänger"))
    layout.add(Paragraph("Wir danken für Ihren Auftrag."))

    r: Rectangle = Rectangle(
        Decimal(59),                # x: 0 + page_margin
        Decimal(848 - 84 - 750),    # y: page_height - page_margin - height_of_textbox
        Decimal(595 - 59 * 2),      # width: page_width - 2 * page_margin
        Decimal(100),               # height
    )

    page.append_annotation(SquareAnnotation(r, stroke_color=HexColor("#ffffff")))

    bottom_payment_info(mainDict[0]).layout(page, r)

    filename = mainDict[0][0]['issuername'] + "-" + mainDict[0][1]['clientname'] + "-" + mainDict[0][2]['date'] + ".pdf"

    # store
    with open(filename, "wb") as pdf_output_file:
        PDF.dumps(pdf_output_file, doc)


if __name__ == "__main__":
    main()
