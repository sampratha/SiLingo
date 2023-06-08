import cv2, os
dataset_path=r"C:\Users\USER\PycharmProjects\SiLingo\static\dataset_new"
labels_list=os.listdir(dataset_path)
print(labels_list)
for label in labels_list:
    print(label)
    for root, dirs, files_list in os.walk(dataset_path + "\\" + label):
        for fname in files_list:

            image=cv2.imread(dataset_path + "\\" + label + "\\" + fname)
            invert = cv2.bitwise_not(image) # OR
            # cv2.imwrite(r"C:\Users\USER\PycharmProjects\SiLingo\static\dataset_inverted" + "\\"+ label + "\\" + fname,invert)

            # Setting parameter values
            t_lower = 50  # Lower Threshold
            t_upper = 150  # Upper threshold

            # Applying the Canny Edge filter
            edge = cv2.Canny(invert, t_lower, t_upper)

            # cv2.imwrite("sample.jpg",edge)
            invert = cv2.bitwise_not(edge) # OR
           # print("Hiiiiiiiiiiiiiiiiiiiiiiiiii")
            cv2.imwrite(r"C:\Users\USER\PycharmProjects\SiLingo\static\dataset_new_inverted\\"+ label + "\\" + fname, invert)
    print("Completed folder "+ label)