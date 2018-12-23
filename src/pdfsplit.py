import argparse
import os
import PyPDF2


def get_page(page, writer, upper_left, lower_right, index):
    _, _, dim_x, dim_y = page.artBox
    new_page = writer.insertBlankPage(dim_x, dim_y, index)
    new_page.mergePage(page)
    new_page.cropBox.upperLeft = upper_left[0] * dim_x, upper_left[1] * dim_y
    new_page.cropBox.lowerRight = lower_right[0] * dim_x, lower_right[1] * dim_y


def process_file(input_path, output_path, crops):
    print("Processing {} -> {}".format(input_path, output_path))
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


def main(input_path, output_path, crops):
    if input_path == output_path:
        print("Input and output path can not be identical.")
        exit(-1)
    if os.path.isfile(input_path):
        process_file(input_path, output_path, crops)
    elif os.path.isdir(input_path) and os.path.isdir(output_path):
        for file_name in os.listdir(input_path):
            file_path = os.path.join(input_path, file_name)
            if os.path.isfile(file_path):
                process_file(file_path, os.path.join(output_path, file_name), crops)
    else:
        print('Invalid choice of input/output path.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split PDF handout slides.")
    parser.add_argument('input', type=str, help="The path of the input file/directory to process")
    parser.add_argument('output', type=str, help="The path to store the resulting PDF(s)")
    args = parser.parse_args()

    main(args.input, args.output,
         [((0, 1), (0.5, 0.5)), ((0, 0.5), (0.5, 0)), ((0.5, 1), (1, 0.5)), ((0.5, 0.5), (1, 0))])
