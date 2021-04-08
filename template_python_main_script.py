from browser import document, html


version = "##VERSION##"

raw_transcriptions = {
##RAW_TRANSCRIPTIONS##
}

characters = [  # TODO
    "LE DOCTEUR STOCKMANN",
    "MADAME STOCKMANN",
    "PETRA",
    "EILIF",
    "MORTEN",
    "LE BOURGMESTRE",
    # "MORTEN KILL",
    "HOVSTAD",
    "MADAME BILLING",
    "HORSTER",
    # "ASLAKSEN",

    "MADAME HOVSTAD"  # TODO delete this
]

didascalie_str = "Didascalie"

n_actes = 5
n_parts = [4, 5, 2, 3, 5]

scene_ids = []
scene_pretty_names = {}
for i_acte in range(1, n_actes+1):
    for i_part in range(1, n_parts[i_acte-1]+1):
        scene_id = f"acte_{i_acte}_part_{i_part}"
        scene_ids.append(scene_id)
        scene_pretty_names[scene_id] = f"Acte {i_acte} - Partie {i_part}"


def deepcopy(e):
    if isinstance(e, list):
        return [deepcopy(a) for a in e]
    elif isinstance(e, dict):
        return {deepcopy(k): deepcopy(v) for k, v in e.items()}
    else:
        return e


# inspired from https://stackoverflow.com/questions/3062746/special-simple-random-number-generator
seed = 0


def randint(n):
    global seed
    seed = (1103515245 * seed + 12345) % 2**31
    return seed % n


# Observer pattern implementation adapted from
# https://stackoverflow.com/questions/1904351/python-observer-pattern-examples-tips/1925836#1925836
# and https://stackoverflow.com/questions/6190468/how-to-trigger-function-on-value-change
class Observable(object):
    def __init__(self, value):
        self._old_value = None
        self._value = value
        self.callbacks = []

    @property
    def old_value(self):
        return self._old_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._old_value = self._value
        self._value = value
        self.fire()

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def fire(self):
        for fn in self.callbacks:
            fn(self)


def get_question_button_action(panel, button_index, callback):
    def question_button_action(event):
        panel.remove()
        callback(button_index)
    return question_button_action


def create_question_panel(message, button_contents, callback):
    panel = html.DIV()
    panel <= message
    panel <= html.HR()

    for button_index, button_content in enumerate(button_contents):
        button = html.BUTTON(button_content)
        button.bind("click", get_question_button_action(panel, button_index, callback))
        panel <= button

    return panel


class SelectionScreen:
    def __init__(self, transcriptions):
        self.transcriptions = transcriptions
        self.character_observable = Observable(None)
        self.scene_observable = Observable(None)
        self.start_observable = Observable(False)

        self.html_root = self.create_root()

        self.character_observable.fire()
        self.scene_observable.fire()

    def get_html_component(self):
        return self.html_root

    def create_root(self):
        root = html.DIV()
        root <= html.DIV(html.B(f"Replicator - Un Ennemi du peuple ({version})")) + html.BR()
        table = html.TABLE()
        table <= html.TR(html.TD("1. Sélectionner le personnage", Id="char_sel_panel_title")
                        + html.TD("2. Sélectionner la scène", Id="scene_sel_panel_title"))
        table <= html.TR(html.TD(self.create_character_selection_panel(), Id="char_sel_panel_td")
                        + html.TD(self.create_scene_selection_panel(), Id="scene_sel_panel_td"))
        root <= table
        root <= html.HR()
        root <= html.DIV("3. Jouer", Id="start_game_panel_title")
        root <= html.DIV(self.create_start_game_panel(), Id="start_game_panel")
        return root

    def remove_root(self):
        self.html_root.remove()

    def create_character_selection_panel(self):
        character_selection_panel = html.DIV(Id="char_sel")
        for character in characters:
            button = html.BUTTON(character, Class="char_button")

            def get_button_action(character):
                def button_action(event):
                    self.character_observable.value = character
                    self.scene_observable.value = None
                    # print(self.character_observable.value)
                return button_action

            button.bind("click", get_button_action(character))

            def get_character_callback(button, character):
                def callback(observable):
                    if character == observable.value:
                        if "char_button_selected" not in button.classList:
                            button.classList.add("char_button_selected")
                    else:
                        if "char_button_selected" in button.classList:
                            button.classList.remove("char_button_selected")
                return callback

            self.character_observable.subscribe(get_character_callback(button, character))

            character_selection_panel <= html.DIV(button)
        return character_selection_panel

    def create_scene_selection_panel(self):
        scene_selection_panel = html.DIV()
        for scene_id in scene_ids:
            scene_pretty_name = scene_pretty_names[scene_id]
            if scene_id in self.transcriptions:
                button = html.BUTTON(scene_pretty_name, Class="scene_button")

                def get_button_action(scene_id):
                    def button_action(event):
                        self.scene_observable.value = scene_id
                    return button_action

                button.bind("click", get_button_action(scene_id))

                def get_character_callback(button, scene_id):
                    def callback(observable):
                        if observable.value in self.transcriptions[scene_id]["characters"]:
                            if "disabled" in button.attrs:
                                del button.attrs["disabled"]
                        else:
                            button.attrs["disabled"] = None
                    return callback

                self.character_observable.subscribe(get_character_callback(button, scene_id))

                def get_scene_callback(button, scene_id):
                    def callback(observable):
                        if scene_id == observable.value:
                            if "scene_button_selected" not in button.classList:
                                button.classList.add("scene_button_selected")
                        else:
                            if "scene_button_selected" in button.classList:
                                button.classList.remove("scene_button_selected")
                    return callback

                self.scene_observable.subscribe(get_scene_callback(button, scene_id))

                scene_selection_panel <= html.DIV(button)
            else:
                scene_selection_panel <= html.DIV(f"({scene_pretty_name} - manquant)", Class="missing_scene")
        return scene_selection_panel

    def create_start_game_panel(self):
        start_game_panel = html.DIV()

        button = html.BUTTON("Commencer !", Id="start_game_button")

        def button_action(event):
            self.start_observable.value = True

        button.bind("click", button_action)

        def get_scene_callback(button):
            def callback(observable):
                if observable.value:
                    if "disabled" in button.attrs:
                        del button.attrs["disabled"]
                else:
                    button.attrs["disabled"] = None
            return callback

        self.scene_observable.subscribe(get_scene_callback(button))

        start_game_panel <= button

        return start_game_panel


class App:

    HISTORY_LENGTH = 4

    def __init__(self):
        self.selected_character = None
        self.selected_scene = None
        self.selected_blocs = None
        self.selected_bloc_lines = None
        self.sequential_progress = None
        self.base_line_scores = None
        self.base_line_score_resume = None
        self.total_line_scores = None
        self.final_line_scores = None
        self.final_line_score_resume = None

        self.transcriptions = {}
        for scene, raw_transcription in raw_transcriptions.items():
            blocs = []
            scene_characters = set()
            new_character = True
            for file_line in raw_transcription["text"].split("\n"):
                file_line = file_line.strip()
                if not file_line:
                    new_character = True
                elif file_line[0] != "#":
                    if new_character:
                        blocs.append({"character": file_line, "lines": []})
                        scene_characters.add(file_line)
                        new_character = False
                    else:
                        blocs[-1]["lines"].append(file_line)

            self.transcriptions[scene] = {
                "blocs": blocs,
                "characters": scene_characters
            }

    def start(self):
        self.start_selection()

    def start_selection(self):
        selection_screen = SelectionScreen(self.transcriptions)

        def start_observable_callback(observable):
            if observable.value:
                selection_screen.remove_root()

                self.selected_character = selection_screen.character_observable.value
                self.selected_scene = selection_screen.scene_observable.value
                self.selected_blocs = self.transcriptions[self.selected_scene]["blocs"]

                self.selected_bloc_lines = [(bloc_index, line_index)
                                            for bloc_index, bloc in enumerate(self.selected_blocs)
                                            if bloc["character"] == self.selected_character
                                            for line_index in range(len(bloc["lines"]))]

                self.base_evaluation_introduction()

        selection_screen.start_observable.subscribe(start_observable_callback)
        document <= selection_screen.get_html_component()

    def base_evaluation_introduction(self):
        message = html.DIV("""\
            Le jeu commence d'abord en mode séquentiel.
            Les répliques du personnage sont présentées dans l'ordre.""")
        button_contents = ["C'est parti !"]

        def callback(button_index):
            self.base_evaluation()

        document <= create_question_panel(message, button_contents, callback)

    def base_evaluation(self):
        def callback(line_scores):
            self.base_line_scores = line_scores
            self.total_line_scores = deepcopy(self.base_line_scores)
            self.set_random_seed()
            self.show_base_scores()
        self.evaluation(callback)

    def set_random_seed(self):
        global seed
        seed = 0
        for line_score in self.base_line_scores.values():
            seed *= 3
            seed += line_score["almost"] + 2*line_score["ko"]
            seed %= 2**31

    def evaluation(self, parent_callback, bloc_line_index=0, line_scores=None):
        if line_scores is None:
            line_scores = {line: {"perfect": 0, "almost": 0, "ko": 0} for line in self.selected_bloc_lines}
        if bloc_line_index < len(self.selected_bloc_lines):
            def callback(result):
                line_scores[self.selected_bloc_lines[bloc_line_index]][result] += 1
                self.evaluation(parent_callback, bloc_line_index=bloc_line_index+1, line_scores=line_scores)
            self.line_evaluation(callback, bloc_line_index)
        else:
            parent_callback(line_scores)

    def line_evaluation(self, parent_callback, bloc_line_index):
        # construct text
        text = []
        bloc_index, line_index = self.selected_bloc_lines[bloc_line_index]
        for back_count in range(self.HISTORY_LENGTH):
            raw_line = self.selected_blocs[bloc_index]["lines"][line_index]
            end = raw_line.find(')')
            div = html.DIV(Class=f"bloc_line_back_{back_count}")
            div <= html.EM(raw_line[:end+1]) + html.SPAN(raw_line[end+1:])
            character = self.selected_blocs[bloc_index]["character"]
            if character == didascalie_str:
                div.classList.add("didascalie")
            text.insert(0, div)
            if line_index == 0 or back_count == self.HISTORY_LENGTH - 1:
                if character != didascalie_str:
                    text.insert(0, html.DIV(character, Class="character_in_text"))
                text.insert(0, html.BR())
            if line_index > 0:
                line_index -= 1
            else:
                if bloc_index > 0:
                    bloc_index -= 1
                    line_index = len(self.selected_blocs[bloc_index]["lines"]) - 1
                else:
                    break

        def autonote_callback(button_index):
            result = ["perfect", "almost", "ko"][button_index]
            if button_index == 0:
                parent_callback(result)
            else:
                text.extend([html.HR(), html.DIV("Répéter les phrases en couleur jusqu'à les connaître par cœur.")])
                button_contents = ["C'est fait."]
                document <= create_question_panel(text, button_contents, lambda i: parent_callback(result))

        def question_callback(button_index):
            text[-1].classList.remove("hidden")
            if button_index == 0:
                button_contents = ["J'ai tout bon 😁", "Presque 😊", "Pas bon 😓"]
                document <= create_question_panel(text, button_contents, autonote_callback)
            else:
                autonote_callback(2)

        # question
        question_button_contents = ["Je me souviens de la suite et je l'ai récitée.",
                                    "Je ne me souviens pas de la suite 😔"]
        text[-1].classList.add("hidden")
        document <= create_question_panel(text, question_button_contents, question_callback)

    def show_base_scores(self):
        self.base_line_score_resume = {"perfect": 0, "almost": 0, "ko": 0}
        for v in self.base_line_scores.values():
            for k in self.base_line_score_resume:
                self.base_line_score_resume[k] += v[k]
        # print("show_base_scores")
        # print(self.base_line_scores)
        # print(self.base_line_score_resume)

        message = html.DIV()
        message <= html.DIV("Voici votre score de base :")
        message <= html.DIV(f"😁 (Parfait !!!) : {self.base_line_score_resume['perfect']}")
        message <= html.DIV(f"😊  (Presque !)  : {self.base_line_score_resume['almost']}")
        message <= html.DIV(f"😔  (À réviser)  : {self.base_line_score_resume['ko']}")

        message <= html.BR() + html.DIV("Maintenant, le programme va vous soumettre des répliques dans un ordre "
                                        "aléatoire, en privilégiant celles posant difficultés.")

        button_contents = ["Ok, c'est parti !"]

        def callback(button_index):
            self.random_focus(0, None)

        document <= create_question_panel(message, button_contents, callback)

    def random_focus(self, progress, last_bloc_line_index):
        progress += 1
        if progress == 2 * len(self.selected_bloc_lines):
            self.show_final_evaluation_message()
        else:
            print("choosing random bloc line")
            print(self.total_line_scores)
            # choose bloc line. Lexicographic order. Don't choose last bloc/line
            worst_score_number = 1000000000
            worst_indexes = []
            for bloc_line_index, (bloc, line) in enumerate(self.selected_bloc_lines):
                if bloc_line_index == last_bloc_line_index:
                    continue
                score = self.total_line_scores[(bloc, line)]
                score_number = score["perfect"]*1000000 + score["almost"]*1000 + score["ko"]
                if score_number < worst_score_number:
                    worst_score_number = score_number
                    worst_indexes = []
                if score_number == worst_score_number:
                    worst_indexes.append(bloc_line_index)
            bloc_line_index = worst_indexes[randint(len(worst_indexes))]
            print(self.selected_bloc_lines[bloc_line_index])

            def callback(result):
                self.total_line_scores[self.selected_bloc_lines[bloc_line_index]][result] += 1
                self.random_focus(progress, bloc_line_index)

            self.line_evaluation(callback, bloc_line_index)

    def show_final_evaluation_message(self):
        message = html.DIV()
        message <= html.DIV("On y est presque !")
        message <= html.BR()
        message <= html.DIV("La dernière étape reprend le texte dans l'ordre pour remettre les choses en place "
                            "et évaluer la progression.")

        button_contents = ["Allons-y ! [Alonzo]"]

        def callback(button_index):
            self.final_evaluation()

        document <= create_question_panel(message, button_contents, callback)

    def final_evaluation(self):
        def callback(line_scores):
            self.final_line_scores = line_scores
            for k, v in line_scores.items():
                for result in ["perfect", "almost", "ko"]:
                    self.total_line_scores[k][result] += v[result]
            self.show_final_scores()
        self.evaluation(callback)

    def show_final_scores(self):
        self.final_line_score_resume = {"perfect": 0, "almost": 0, "ko": 0}
        for v in self.final_line_scores.values():
            for k in self.final_line_score_resume:
                self.final_line_score_resume[k] += v[k]

        message = html.DIV()
        message <= html.DIV("Bravo ! Vous êtes allé jusqu'au bout !")
        message <= html.BR()
        message <= html.DIV("Voici votre progression :")
        message <= html.DIV(f"😁 (Parfait !!!) : {self.base_line_score_resume['perfect']} => {self.final_line_score_resume['perfect']}")
        message <= html.DIV(f"😊  (Presque !)  : {self.base_line_score_resume['almost']} => {self.final_line_score_resume['almost']}")
        message <= html.DIV(f"😔  (À réviser)  : {self.base_line_score_resume['ko']} => {self.final_line_score_resume['ko']}")
        message <= html.BR()
        message <= html.DIV("Vous pouvez maintenant continuer à travailler sur cette scène ou revenir à l'écran de "
                            "sélection.")

        button_contents = ["Continuer avec cette scène", "Revenir à l'écran de sélection"]

        def callback(button_index):
            if button_index == 0:
                self.random_focus(0, None)
            else:
                self.start_selection()

        document <= create_question_panel(message, button_contents, callback)


if __name__ == '__main__':
    app = App()
    app.start()
