import fileinput
import glob
import os
import string


def load_input(input_directory):
    """Funcion load_input"""
    sequence = []
    print("Cargando files")
    files = glob.glob(f"{input_directory}/*")
    with fileinput.input(files=files) as f:
        for line in f:
            print(line)
            sequence.append((fileinput.filename(), line.strip()))
    return sequence


def line_preprocessing(sequence):
    """Line Preprocessing"""
    return [
        (key, value.translate(str.maketrans("", "", string.punctuation)).lower().strip())
        for key, value in sequence
    ]


def mapper(sequence):
    """Mapper"""
    return [(word, 1) for _, value in sequence for word in value.split()]


def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    return sorted(sequence, key=lambda x: x[0])


def reducer(sequence):
    """Reducer: Reducir los valores con la misma clave."""
    result = {}
    for key, value in sequence:
        if key not in result:
            result[key] = 0
        result[key] += value
    return list(result.items())


def create_output_directory(output_directory):
    """Create Output Directory"""
    if os.path.exists(output_directory):
        for file in glob.glob(f"{output_directory}/*"):
            os.remove(file)
        os.rmdir(output_directory)
    os.makedirs(output_directory)


def save_output(output_directory, sequence):
    """Save Output"""
    with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")


def create_marker(output_directory):
    """Create Marker"""
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")


def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = line_preprocessing(sequence)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_output_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":
    run_job("input", "output")
