import PyPDF2


def get_page(page, writer, upper_left, lower_right, index):
    dimensions = page.artBox
    new_page = writer.insertBlankPage(dimensions[2], dimensions[3], index)
    new_page.mergePage(page)
    new_page.cropBox.upperLeft = upper_left
    new_page.cropBox.lowerRight = lower_right


def main(input_path, output_path, crops):
    reader = PyPDF2.PdfFileReader(input_path)
    writer = PyPDF2.PdfFileWriter()

    current_output_page = 0
    for i in range(reader.getNumPages()):
        page = reader.getPage(i)

        for upper_left, lower_right in crops:
            get_page(page, writer, upper_left, lower_right, current_output_page)
            current_output_page += 1

    with open(output_path, 'wb') as fp:
        writer.write(fp)


if __name__ == '__main__':
    main("../TNN_WS18_01_Intro_slides.pdf", 'results.pdf',
         [((0, 595), (421, 298)), ((0, 298), (421, 0)), ((421, 595), (842, 298)), ((421, 298), (842, 0))])
