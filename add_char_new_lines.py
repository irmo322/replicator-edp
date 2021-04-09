import os


all_characters = {  # TODO
    "LE DOCTEUR STOCKMANN",
    "MADAME STOCKMANN",
    "PETRA",
    "EILIF",
    "MORTEN",
    "LE BOURGMESTRE",
    "MORTEN KILL",
    "HOVSTAD",
    "MADAME BILLING",
    "HORSTER",
    "ASLAKSEN",
    "Didascalie",

    "MADAME HOVSTAD",  # TODO delete this
    "LE MAIRE",
}


def add_linebreak_after_char(scene_file_name):
    print(f"scene {scene_file_name}")

    with open(os.path.join("transcriptions", scene_file_name)) as f:
        file_content = f.read()

    for character in all_characters:
        for plop in [". -", " -", " .-", ".-", " . -", "-"]:
            file_content = file_content.replace(character + plop, character + "\n-")

    with open(os.path.join("transcriptions", scene_file_name), "w") as f:
        f.write(file_content)


def main():
    scenes = [
        # "acte_1_part_1",
        # "acte_1_part_2",
        # "acte_1_part_3",
        # "acte_1_part_4",
        # "acte_2_part_1",
        # "acte_2_part_2",
        # "acte_2_part_3",
        # "acte_2_part_4",
        # "acte_2_part_5",
        # "acte_3_part_1",
        # "acte_3_part_2",
        # "acte_3_part_3",
        "acte_3_part_4",
        # "acte_4_part_1",
        # "acte_4_part_2",
        # "acte_4_part_3",
        # "acte_5_part_1",
        # "acte_5_part_2",
        # "acte_5_part_3",
        # "acte_5_part_4",
        # "acte_5_part_5",
    ]
    scene_file_names = [
        f"{scene}.txt"
        for scene in scenes
    ]
    for scene_file_name in scene_file_names:
        add_linebreak_after_char(scene_file_name)


if __name__ == '__main__':
    main()
