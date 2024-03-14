import cv2
import os
import numpy as np
import pandas as pd



def draw_bounding_boxes(
    output_dir: str,
):
    store_name, filename = output_dir.split('/')
    if not os.path.isdir(f'outputs/{output_dir}'):
        raise FileNotFoundError(f"The file has not been textracted. Output directory '{output_dir}' does not exist in `outputs`.")
    
    # Load your image
    image = cv2.imread(f'assets/{filename}.jpg')

    df = pd.read_csv(f'outputs/{output_dir}/word_confidence.csv')

    columns_to_extract = [
        'bounding_box_point_1_x', 'bounding_box_point_1_y',
        'bounding_box_point_2_x', 'bounding_box_point_2_y',
        'bounding_box_point_3_x', 'bounding_box_point_3_y',
        'bounding_box_point_4_x', 'bounding_box_point_4_y'
    ]


    bounding_boxes = []
    for _, row in df.iterrows():
        row_data = row[columns_to_extract].values
        coordinate_list = [(row_data[i], row_data[i+1]) for i in range(0, len(row_data), 2)]
        bounding_boxes.append(coordinate_list)


    # Iterate through the list of bounding boxes
    for bounding_box in bounding_boxes:
        # Convert the tuples to numpy arrays for easier indexing
        bounding_box = np.array(bounding_box, dtype=int)

        # Draw the bounding box on the image
        cv2.rectangle(image, (bounding_box[0][0], bounding_box[0][1]), (bounding_box[2][0], bounding_box[2][1]), (0, 255, 0), 2)

    # Display the image with bounding boxes
    cv2.imshow('Image with Bounding Boxes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    draw_bounding_boxes(
        "berkeley_bowl/20231222_berkeley_bowl",
    )
