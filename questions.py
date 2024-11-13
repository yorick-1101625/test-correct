class Questions:
    def __init__(self, question_id: str, question: str):
        self.question_id = question_id
        self.question = question

        def __repr__(self) -> str:
            return "{}({})".format(type(self).__name__, ", ".join([f'{key}={value!r}' for key, value in self.__dict__.items()]))