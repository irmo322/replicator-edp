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


def check_scene(scene_file_name):
    print(f"scene {scene_file_name}")

    with open(os.path.join("transcriptions", scene_file_name)) as f:
        file_lines = [line.strip() for line in f.readlines()]

    theatrical_lines = []
    new_character = True
    for file_line in file_lines:
        if not file_line:
            new_character = True
        elif file_line[0] != "#":
            if new_character:
                line_characters = file_line.split(" & ")
                theatrical_lines.append({"characters": line_characters, "lines": []})
                new_character = False
            else:
                theatrical_lines[-1]["lines"].append(file_line)

    characters = set.union(*[set(plop["characters"]) for plop in theatrical_lines])

    print(f"Characters : {characters}")

    assert characters.issubset(all_characters)

    # while True:
    #     chosen_character = input("Choose character : ")
    #     if chosen_character not in characters:
    #         print(f"{chosen_character} is not available.")
    #     else:
    #         break
    #
    # totos = [(i, j)
    #          for i, plop in enumerate(theatrical_lines) if plop["character"] == chosen_character
    #          for j, line in enumerate(plop["lines"])]
    # while True:
    #     input("\nAppuie sur Enter pour un nouveau test...")
    #
    #     i, j = random.choice(totos)
    #
    #     if i > 0:
    #         plop = theatrical_lines[i-1]
    #         print("**", plop["character"], "**")
    #         lines = plop["lines"]
    #         if len(lines) > 3:
    #             lines = ["[...]"] + lines[-3:]
    #         print(*lines, sep="\n")
    #
    #     plop = theatrical_lines[i]
    #     print("**", plop["character"], "**")
    #     print(*plop["lines"][:j], sep="\n")
    #
    #     input("Appuie sur Enter pour vérifier ce qui vient ensuite...")
    #
    #     print(plop["lines"][j])


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
        check_scene(scene_file_name)


if __name__ == '__main__':
    main()
