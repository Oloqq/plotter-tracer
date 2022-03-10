from typing import Callable
VerbHandler = Callable[[list[str]], None]

# Continuous Command Line Interface
class CCLI:
    funcs: dict[str, VerbHandler] = {}
    descriptions: dict[str, str] = {}

    def __init__(self) -> None:
        self.add('help', self.help, 'Display this message')

    def add(self, keys: str|list[str], function: VerbHandler, description: str):
        if type(keys) == str:
            keys = [keys]
        for key in keys:
            self.funcs[key] = function
            self.descriptions[key] = description

    def loop(self):
        while True:
            user_data = input('\n: ').split()
            command = user_data[0]
            if command in self.funcs:
                self.funcs[command](user_data)
            elif command in ['quit', 'exit', 'q']:
                print("cya")
                return
            else:
                print('Unrecognized command')

    def help(self, args):
        print('\n=== Tracer handbook ===')
        print('exit: exit\n')
        for k, v in self.descriptions.items():
            print(f'{k}: {v}\n')

if __name__ == "__main__":
    ccli = CCLI()
    ccli.loop()