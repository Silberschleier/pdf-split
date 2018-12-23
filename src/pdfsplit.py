import PyPDF2


def get_page(page, writer, upper_left, lower_right, index):
    _, _, dim_x, dim_y = page.artBox
    new_page = writer.insertBlankPage(dim_x, dim_y, index)
    new_page.mergePage(page)
    new_page.cropBox.upperLeft = upper_left[0] * dim_x, upper_left[1] * dim_y
    new_page.cropBox.lowerRight = lower_right[0] * dim_x, lower_right[1] * dim_y


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
         [((0, 1), (0.5, 0.5)), ((0, 0.5), (0.5, 0)), ((0.5, 1), (1, 0.5)), ((0.5, 0.5), (1, 0))])
