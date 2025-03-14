def read_class_file(filename):
    EMAIL_CLASSES = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            EMAIL_CLASSES.append(line.strip())
    EMAIL_CLASSES = list(set(EMAIL_CLASSES))
    print(EMAIL_CLASSES)
    return EMAIL_CLASSES